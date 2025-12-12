import streamlit as st
import json
import os
import time
import threading
import queue
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import google.generativeai as genai

# Try to import speech recognition
try:
    import speech_recognition as sr
    import whisper
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ Speech/Whisper not found. pip install SpeechRecognition openai-whisper")

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(page_title="Universal Agent Assistant", layout="wide", page_icon="🌐")

STATE_FILE = "live_state.json"
KB_DIR = "Knowledge_Base"
HTTP_PORT = 8765

# Gemini API Setup
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    model = None

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if 'accumulated_links' not in st.session_state: 
    st.session_state.accumulated_links = []
if 'current_client' not in st.session_state: 
    st.session_state.current_client = "NeoBank"
if 'current_agent' not in st.session_state:
    st.session_state.current_agent = "Demo Agent"
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'pilot_doc_components' not in st.session_state:
    st.session_state.pilot_doc_components = {}
if 'server_started' not in st.session_state:
    st.session_state.server_started = False
if 'listening_active' not in st.session_state:
    st.session_state.listening_active = False
if 'last_transcript' not in st.session_state:
    st.session_state.last_transcript = "Listening..."
if 'stop_event' not in st.session_state:
    st.session_state.stop_event = threading.Event()

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def search_kb(client, query_text):
    """Search knowledge base files for relevant content"""
    if not client or not os.path.exists(os.path.join(KB_DIR, client)):
        return []
    
    if not query_text:
        return []
    
    words = query_text.lower().split()
    keywords = [w for w in words if len(w) > 2]
    
    if not keywords:
        return []
    
    hits = []
    client_path = os.path.join(KB_DIR, client)
    
    for filename in os.listdir(client_path):
        if filename.endswith(".md"):
            try:
                with open(os.path.join(client_path, filename), "r", encoding="utf-8") as f:
                    content = f.read().lower()
                
                score = 0
                for k in keywords:
                    if k in content: score += 1
                    if k in filename.lower(): score += 3
                
                if score > 0:
                    html_file = filename.replace(".md", ".html")
                    file_to_serve = html_file if os.path.exists(os.path.join(client_path, html_file)) else filename
                    
                    hits.append({
                        "id": filename,
                        "name": filename.replace(".md", "").replace("_", " ").title(),
                        "link": f"http://localhost:{HTTP_PORT}/{client}/{file_to_serve}",
                        "score": score,
                        "count": 1
                    })
            except Exception:
                pass
    
    hits.sort(key=lambda x: x['score'], reverse=True)
    return hits[:5]

# ==========================================
# FRAGMENTS (THE FIX IS HERE)
# ==========================================

@st.fragment(run_every=1)
def render_knowledge_stream():
    """
    This fragment runs every 1 second independently of the rest of the app.
    It DRAINS the queue and updates the session state locally.
    """
    st.subheader("📚 Knowledge Stream")
    st.caption("Live-triggered articles")

    # 1. PROCESS QUEUE INSIDE THE FRAGMENT
    # This prevents the main app from needing to rerun
    if st.session_state.listening_active and 'listener_queue' in st.session_state:
        try:
            while not st.session_state.listener_queue.empty():
                data = st.session_state.listener_queue.get_nowait()
                transcript = data['transcript']
                
                # Update Last Heard for other fragments
                st.session_state.last_transcript = transcript
                
                # Search KB
                hits = search_kb(st.session_state.current_client, transcript)
                
                # Update Global State (Accumulated Links)
                current_ids = [item['id'] for item in st.session_state.accumulated_links]
                for hit in hits:
                    if hit['id'] not in current_ids:
                        st.session_state.accumulated_links.insert(0, hit)
                    else:
                        for existing in st.session_state.accumulated_links:
                            if existing['id'] == hit['id']:
                                st.session_state.accumulated_links.remove(existing)
                                existing['count'] = existing.get('count', 1) + 1
                                st.session_state.accumulated_links.insert(0, existing)
                                break
        except queue.Empty:
            pass

    # 2. RENDER UI
    if st.session_state.accumulated_links:
        for item in st.session_state.accumulated_links:
            freq_badge = ""
            if isinstance(item.get('count'), int) and item['count'] > 1:
                freq_badge = f"🔥 {item['count']}"
            elif item.get('count') == 'Manual':
                freq_badge = "🔍"
            
            st.markdown(
                f"""
                <a href="{item['link']}" target="_blank" style="
                display:block; background:#1e2126; padding:12px; border-radius:6px; 
                text-decoration:none; color:#4A90E2; border-left: 4px solid #4A90E2; 
                margin-bottom:8px; transition: all 0.2s;">
                <b>{item['name']}</b> 
                <span style='float:right; font-size:0.9em; color: #ccc;'>{freq_badge}</span>
                </a>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("🎯 Waiting for triggers...")

@st.fragment(run_every=1)
def render_last_heard_box():
    """Updates just the blue box without reloading chat"""
    last_text = st.session_state.get('last_transcript', 'Listening...')
    st.info(f"**🎧 Last Heard:** \"{last_text}\"")

# ==========================================
# DATA & CONFIG
# ==========================================

CLIENT_CONFIG = {
    "NeoBank": {
        "industry": "Banking",
        "tone": "Professional, Empathetic",
        "directive": "Frame all solutions as protecting the customer's assets.",
        "key_rules": "NEVER read card numbers aloud.",
        "sops": {"Fraud Alert": "1. Freeze card. 2. Verify transactions."}
    },
    "GlowCosmetics": {
        "industry": "Retail",
        "tone": "High Energy, 'Bestie' Vibe",
        "directive": "Frame selling as 'Treating yourself'.",
        "key_rules": "Offer 10% discount on competitor mention.",
        "sops": {"Returns": "1. Check window. 2. Issue label."}
    }
}

AGENT_DATABASE = {
    "Demo Agent": {"role": "L2 Senior Associate", "manager": "SysAdmin", "focus_area": "Competency", "latest_review": "Demo Mode"},
    "Alex Chen": {"role": "L1 Associate", "manager": "Sarah C", "focus_area": "Confidence", "latest_review": "Enthusiastic but nervous"}
}

# ==========================================
# SERVER & LISTENER LOGIC
# ==========================================

class KnowledgeBaseHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=KB_DIR, **kwargs)
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        super().end_headers()
    def log_message(self, format, *args): pass

def start_file_server():
    if st.session_state.server_started: return
    def run_server():
        try:
            server = HTTPServer(('localhost', HTTP_PORT), KnowledgeBaseHandler)
            st.session_state.server_started = True
            server.serve_forever()
        except: pass
    t = threading.Thread(target=run_server, daemon=True)
    t.start()

def get_cable_index():
    if not SPEECH_AVAILABLE: return None
    try:
        mics = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mics):
            if "CABLE Output" in name or "Stereo Mix" in name: return i
    except: pass
    return None

def run_listener(state_queue, stop_event):
    if not SPEECH_AVAILABLE: return
    try:
        audio_model = whisper.load_model("base")
        r = sr.Recognizer()
        mic = sr.Microphone(device_index=get_cable_index())
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
            while not stop_event.is_set():
                try:
                    audio = r.listen(source, timeout=2, phrase_time_limit=6)
                    text = r.recognize_whisper(audio, model="base", load_options=dict(device="cpu"))
                    if text.strip():
                        state_queue.put({"transcript": text, "timestamp": time.time()})
                except: continue
    except Exception as e:
        print(f"Listener failed: {e}")

# ==========================================
# AI GENERATION
# ==========================================

def build_pilot_components(agent_name, client_key, transcript, agent_context=""):
    agent = AGENT_DATABASE.get(agent_name, AGENT_DATABASE["Demo Agent"])
    client = CLIENT_CONFIG.get(client_key, CLIENT_CONFIG["NeoBank"])
    return {
        "agent_profile": agent,
        "client_profile": client,
        "live_context": {"transcript": transcript, "agent_question": agent_context},
        "available_sops": client.get('sops', {})
    }

def generate_guidance(components):
    if not model: return "⚠️ API Key Missing"
    prompt = f"""
    ACT AS A LIVE AGENT ASSISTANT.
    CLIENT: {components['client_profile']['industry']}
    TONE: {components['client_profile']['tone']}
    CUSTOMER SAID: "{components['live_context']['transcript']}"
    AGENT ASKED: "{components['live_context']['agent_question']}"
    
    Provide:
    1. SCRIPT (What to say)
    2. CHECKLIST (What to verify)
    3. NEXT STEP
    """
    try:
        response = model.generate_content(prompt)
        return response.text
    except: return "⚠️ Generation Failed"

# ==========================================
# UI LAYOUT
# ==========================================

start_file_server()

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Console")
    
    # Selection Logic
    st.markdown("#### 👤 Profile")
    new_agent = st.selectbox("Agent", list(AGENT_DATABASE.keys()), index=list(AGENT_DATABASE.keys()).index(st.session_state.current_agent))
    if new_agent != st.session_state.current_agent:
        st.session_state.current_agent = new_agent
        st.rerun()

    new_client = st.selectbox("Client", list(CLIENT_CONFIG.keys()), index=list(CLIENT_CONFIG.keys()).index(st.session_state.current_client))
    if new_client != st.session_state.current_client:
        st.session_state.current_client = new_client
        st.session_state.accumulated_links = []
        st.rerun()

    # Listener Controls
    st.divider()
    st.markdown("#### 🎤 Transcription")
    
    if SPEECH_AVAILABLE:
        if st.button("🔴 Start" if not st.session_state.listening_active else "⏹️ Stop"):
            st.session_state.listening_active = not st.session_state.listening_active
            
            if st.session_state.listening_active:
                st.session_state.stop_event.clear()
                if 'listener_queue' not in st.session_state:
                    st.session_state.listener_queue = queue.Queue()
                
                # Only start thread if not alive
                if 'listener_thread' not in st.session_state or not st.session_state.listener_thread.is_alive():
                    st.session_state.listener_thread = threading.Thread(
                        target=run_listener, 
                        args=(st.session_state.listener_queue, st.session_state.stop_event),
                        daemon=True
                    )
                    st.session_state.listener_thread.start()
            else:
                st.session_state.stop_event.set()
                st.rerun()
        
        st.caption(f"Status: {'🟢 ACTIVE' if st.session_state.listening_active else '⚫ IDLE'}")
    else:
        st.warning("Speech Libs Missing")

    # Manual Search
    st.divider()
    m_search = st.text_input("Manual Search")
    if st.button("Go"):
        hits = search_kb(st.session_state.current_client, m_search)
        for h in hits: 
            h['count'] = 'Manual'
            st.session_state.accumulated_links.insert(0, h)
        st.rerun()

# --- MAIN LAYOUT ---
st.title(f"🌐 Universal Agent | {st.session_state.current_client}")

left, middle, right = st.columns([1, 1.5, 1.5])

# LEFT: KNOWLEDGE STREAM (Updates independently!)
with left:
    render_knowledge_stream()

# MIDDLE: CHAT INTERFACE
with middle:
    st.subheader("💬 Agent Buddy")
    st.caption("Ask questions, get context")
    
    # Fragment for the status box
    render_last_heard_box()
    
    # Chat Container
    chat_container = st.container(height=400)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
    
    # Chat Input
    # NOTE: Inputs in fragments can be tricky, so we keep the main chat input 
    # in the MAIN BODY (here), but because the Left Column manages its own 
    # updates via fragment, this input won't lose focus/disappear.
    if prompt := st.chat_input("Ask for guidance..."):
        # 1. Add User Message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # 2. Generate Response
        transcript_context = st.session_state.get('last_transcript', '')
        components = build_pilot_components(
            st.session_state.current_agent,
            st.session_state.current_client,
            transcript_context,
            prompt
        )
        st.session_state.pilot_doc_components = components
        
        # Show spinner only in this column
        with st.spinner("Thinking..."):
            response_text = generate_guidance(components)
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        st.rerun()

# RIGHT: X-RAY
with right:
    st.subheader("🔬 Context X-Ray")
    st.caption("Live Data Injection")
    
    if st.session_state.pilot_doc_components:
        comp = st.session_state.pilot_doc_components
        with st.expander("Live Context", expanded=True):
            st.json(comp['live_context'])
        with st.expander("Agent & Client", expanded=False):
            st.write(comp['agent_profile'])
            st.write(comp['client_profile'])
    else:
        st.info("Ask a question to see X-Ray")