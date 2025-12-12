import streamlit as st
import json
import os
import time
import threading
import queue
import datetime
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

st.set_page_config(page_title="Universal Agent | Pro Dashboard", layout="wide", page_icon="🎧")

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
# DATA & CONFIG (Expanded for "Quick Actions")
# ==========================================

CLIENT_CONFIG = {
    "NeoBank": {
        "industry": "Banking",
        "tone": "Professional, Empathetic, Secure",
        "directive": "Frame all solutions as protecting the customer's assets.",
        "key_rules": "NEVER read card numbers aloud. ALWAYS verify DOB.",
        "scripts": {
            "Greeting": "Thank you for calling NeoBank Security. My name is [Name], how can I protect your assets today?",
            "Hold": "I need to securely verify that information. May I place you on a brief hold?",
            "Closing": "Thank you for choosing NeoBank. Please keep your password safe. Have a secure day."
        },
        "sops": {
            "Fraud Alert": "1. Freeze card. 2. Verify last 3 transactions. 3. Issue provisional credit.",
            "Wire Transfer": "1. Authenticate Voice ID. 2. Confirm recipient IBAN. 3. Read back disclaimer."
        }
    },
    "GlowCosmetics": {
        "industry": "Retail",
        "tone": "High Energy, 'Bestie' Vibe, Excited",
        "directive": "Frame selling as 'Treating yourself'. Use emojis. Focus on discounts.",
        "key_rules": "Offer 10% discount on competitor mention. No returns on open lipstick.",
        "scripts": {
            "Greeting": "Hey there! Thanks for calling GlowCosmetics! This is [Name], ready to help you glow! ✨",
            "Hold": "Ooh, let me check the stockroom for that shade! Hang tight one sec! 💄",
            "Closing": "You're gonna look amazing! Tag us on Insta when you get it! Bye bestie! 💖"
        },
        "sops": {
            "Returns": "1. Check 30-day window. 2. Verify product condition. 3. Issue label.",
            "Damaged Item": "1. Apologize profusely. 2. Send replacement + free sample. 3. Log quality issue."
        }
    }
}

AGENT_DATABASE = {
    "Demo Agent": {"role": "L2 Senior Associate", "manager": "SysAdmin", "focus_area": "Competency", "latest_review": "Demo Mode"},
    "Alex Chen": {"role": "L1 Associate", "manager": "Sarah C", "focus_area": "Confidence", "latest_review": "Enthusiastic but nervous"},
    "Jordan Smith": {"role": "L3 Specialist", "manager": "Kyle R", "focus_area": "Compliance", "latest_review": "Fast but skips disclosures"}
}

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if 'accumulated_links' not in st.session_state: st.session_state.accumulated_links = []
if 'current_client' not in st.session_state: st.session_state.current_client = "NeoBank"
if 'current_agent' not in st.session_state: st.session_state.current_agent = "Demo Agent"
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'server_started' not in st.session_state: st.session_state.server_started = False
if 'listening_active' not in st.session_state: st.session_state.listening_active = False
if 'stop_event' not in st.session_state: st.session_state.stop_event = threading.Event()

# NEW: Transcript Log
if 'transcript_log' not in st.session_state: st.session_state.transcript_log = []
if 'call_start_time' not in st.session_state: st.session_state.call_start_time = None

# ==========================================
# HELPER FUNCTIONS
# ==========================================

def search_kb(client, query_text):
    """Search knowledge base files for relevant content"""
    if not client or not os.path.exists(os.path.join(KB_DIR, client)): return []
    if not query_text: return []
    
    words = query_text.lower().split()
    keywords = [w for w in words if len(w) > 3] # Increased filter length slightly
    if not keywords: return []
    
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
            except Exception: pass
    
    hits.sort(key=lambda x: x['score'], reverse=True)
    return hits[:5]

# ==========================================
# FRAGMENTS
# ==========================================

@st.fragment(run_every=1)
def render_knowledge_stream():
    """Independent Knowledge Stream & Transcript Processor"""
    st.subheader("📚 Knowledge Stream")
    
    # 1. PROCESS QUEUE INSIDE THE FRAGMENT
    if st.session_state.listening_active and 'listener_queue' in st.session_state:
        try:
            while not st.session_state.listener_queue.empty():
                data = st.session_state.listener_queue.get_nowait()
                transcript = data['transcript']
                ts = datetime.datetime.fromtimestamp(data['timestamp']).strftime('%H:%M:%S')
                
                # Update Transcript Log
                entry = f"[{ts}] {transcript}"
                st.session_state.transcript_log.append(entry)
                
                # Search KB
                hits = search_kb(st.session_state.current_client, transcript)
                
                # Update Accumulated Links
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

    # 2. RENDER LINKS
    if st.session_state.accumulated_links:
        for item in st.session_state.accumulated_links:
            freq_badge = f"🔥 {item['count']}" if isinstance(item.get('count'), int) and item['count'] > 1 else ("🔍" if item.get('count') == 'Manual' else "")
            
            st.markdown(
                f"""
                <a href="{item['link']}" target="_blank" style="
                display:block; background:#1e2126; padding:10px; border-radius:5px; 
                text-decoration:none; color:#4A90E2; border-left: 3px solid #4A90E2; 
                margin-bottom:6px; font-size: 0.9rem;">
                <b>{item['name']}</b> 
                <span style='float:right; color: #ccc;'>{freq_badge}</span>
                </a>
                """,
                unsafe_allow_html=True
            )
    else:
        st.caption("Waiting for triggers...")

@st.fragment(run_every=1)
def render_transcript_log():
    """Updates the scrolling transcript log independently"""
    
    # Timer
    if st.session_state.listening_active and st.session_state.call_start_time:
        elapsed = datetime.datetime.now() - st.session_state.call_start_time
        mins, secs = divmod(elapsed.seconds, 60)
        timer_str = f"{mins:02}:{secs:02}"
        st.markdown(f"**⏱️ Call Duration:** `{timer_str}`")
    else:
        st.markdown("**⏱️ Call Duration:** `00:00`")

    # The Log
    if st.session_state.transcript_log:
        # Join the last 10 entries for display to keep it clean
        log_text = "\n".join(st.session_state.transcript_log[-15:])
        st.text_area("Live Transcript", value=log_text, height=200, disabled=True, key=f"log_{len(st.session_state.transcript_log)}")
    else:
        st.info("Waiting for speech...")

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
        # Load Whisper (User Note: Can switch to Vosk here later)
        audio_model = whisper.load_model("base")
        r = sr.Recognizer()
        mic = sr.Microphone(device_index=get_cable_index())
        with mic as source:
            r.adjust_for_ambient_noise(source, duration=1)
            # Dynamic thresholding helps with silence
            r.dynamic_energy_threshold = True 
            
            while not stop_event.is_set():
                try:
                    # Phrase time limit ensures we get frequent updates (chunks) rather than one long block
                    audio = r.listen(source, timeout=2, phrase_time_limit=5)
                    text = r.recognize_whisper(audio, model="base", load_options=dict(device="cpu"))
                    if text.strip():
                        state_queue.put({"transcript": text, "timestamp": time.time()})
                except: continue
    except Exception as e:
        print(f"Listener failed: {e}")

# ==========================================
# AI GENERATION
# ==========================================

def generate_guidance(client_name, agent_name, transcript_history, user_query):
    if not model: return "⚠️ API Key Missing"
    
    client = CLIENT_CONFIG.get(client_name)
    agent = AGENT_DATABASE.get(agent_name)
    
    # Grab last 5 turns of transcript for context
    recent_context = "\n".join(transcript_history[-5:]) if transcript_history else "No transcript yet."
    
    prompt = f"""
    ROLE: Real-time Call Center Coach.
    
    CONTEXT:
    - Client: {client_name} ({client['industry']})
    - Agent: {agent_name} ({agent['role']})
    - Tone: {client['tone']}
    - Recent Transcript: "{recent_context}"
    - Agent Query: "{user_query}"
    
    TASK: Provide a short script, a verification checklist, and the next logical step.
    Keep it formatted for immediate reading.
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
    
    # 1. Profile Selectors
    st.markdown("#### 👤 Configuration")
    new_agent = st.selectbox("Agent", list(AGENT_DATABASE.keys()), index=list(AGENT_DATABASE.keys()).index(st.session_state.current_agent))
    if new_agent != st.session_state.current_agent:
        st.session_state.current_agent = new_agent
        st.rerun()

    new_client = st.selectbox("Client", list(CLIENT_CONFIG.keys()), index=list(CLIENT_CONFIG.keys()).index(st.session_state.current_client))
    if new_client != st.session_state.current_client:
        st.session_state.current_client = new_client
        st.session_state.accumulated_links = []
        st.session_state.transcript_log = [] # Clear log on client switch
        st.rerun()

    st.divider()
    
    # 2. Transcription Control
    st.markdown("#### 📞 Call Controls")
    if SPEECH_AVAILABLE:
        if st.button("🟢 Start Call" if not st.session_state.listening_active else "⏹️ End Call", use_container_width=True):
            st.session_state.listening_active = not st.session_state.listening_active
            
            if st.session_state.listening_active:
                st.session_state.call_start_time = datetime.datetime.now()
                st.session_state.stop_event.clear()
                if 'listener_queue' not in st.session_state: st.session_state.listener_queue = queue.Queue()
                
                if 'listener_thread' not in st.session_state or not st.session_state.listener_thread.is_alive():
                    st.session_state.listener_thread = threading.Thread(
                        target=run_listener, 
                        args=(st.session_state.listener_queue, st.session_state.stop_event),
                        daemon=True
                    )
                    st.session_state.listener_thread.start()
            else:
                st.session_state.stop_event.set()
                st.session_state.call_start_time = None
                st.rerun()
    else:
        st.warning("Speech Libs Missing")

    # 3. Manual Search
    st.divider()
    m_search = st.text_input("Manual KB Search")
    if st.button("Search KB"):
        hits = search_kb(st.session_state.current_client, m_search)
        for h in hits: 
            h['count'] = 'Manual'
            st.session_state.accumulated_links.insert(0, h)
        st.rerun()

# --- MAIN LAYOUT ---
st.title(f"🌐 Universal Agent | {st.session_state.current_client}")

left, middle, right = st.columns([1, 1.8, 1.2])

# LEFT: KNOWLEDGE STREAM (Independent Fragment)
with left:
    render_knowledge_stream()

# MIDDLE: TRANSCRIPT & CHAT
with middle:
    # 1. Transcript Log (Independent Fragment)
    render_transcript_log()
    
    st.divider()
    
    # 2. Chat Interface
    st.subheader("💬 AI Coach")
    chat_container = st.container(height=300)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
    
    if prompt := st.chat_input("Ask for help..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        with st.spinner("Analyzing..."):
            response_text = generate_guidance(
                st.session_state.current_client,
                st.session_state.current_agent,
                st.session_state.transcript_log,
                prompt
            )
        
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        st.rerun()

# RIGHT: STATIC PILOT DOC (Always Visible)
with right:
    client_data = CLIENT_CONFIG[st.session_state.current_client]
    agent_data = AGENT_DATABASE[st.session_state.current_agent]
    
    st.subheader("📋 Pilot Document")
    
    # 1. Quick Actions (New Feature)
    st.markdown("##### ⚡ Quick Scripts")
    c1, c2, c3 = st.columns(3)
    if c1.button("👋 Hello"): st.toast("Copied Greeting!")
    if c2.button("✋ Hold"): st.toast("Copied Hold Script!")
    if c3.button("👋 Bye"): st.toast("Copied Closing!")
    
    with st.expander("📝 View Scripts", expanded=False):
        st.code(client_data['scripts']['Greeting'], language="text")
        st.code(client_data['scripts']['Hold'], language="text")
        st.code(client_data['scripts']['Closing'], language="text")

    # 2. Client Profile (Always Visible)
    with st.expander("🏢 Client Profile", expanded=True):
        st.markdown(f"**Tone:** {client_data['tone']}")
        st.info(f"**Directive:** {client_data['directive']}")
        st.error(f"**CRITICAL:** {client_data['key_rules']}")

    # 3. Agent Profile
    with st.expander("👤 My Stats", expanded=False):
        st.write(f"**Role:** {agent_data['role']}")
        st.write(f"**Focus:** {agent_data['focus_area']}")

    # 4. SOP Lookup (Static)
    with st.expander("📚 SOP Quick Reference", expanded=False):
        st.json(client_data['sops'])