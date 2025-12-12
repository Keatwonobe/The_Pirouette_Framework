import streamlit as st
import json
import os
import time
import threading
import queue
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
import google.generativeai as genai
from streamlit_autorefresh import st_autorefresh

# Try to import speech recognition (optional if not available)
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
HTTP_PORT = 8765  # Static file server port

# Gemini API Setup
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    # Use the correct model name for the current API
    model = genai.GenerativeModel('gemini-2.0-flash')
else:
    model = None

# ==========================================
# CLIENT PROFILES
# ==========================================

st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        .stApp { background-color: #0e1117; } /* Match your dark theme */
    </style>
""", unsafe_allow_html=True)

CLIENT_CONFIG = {
    "NeoBank": {
        "industry": "Banking",
        "tone": "Professional, Empathetic, Secure",
        "directive": "Frame all solutions as protecting the customer's assets. Use terms like 'Security', 'Verification', 'Peace of Mind'.",
        "kb_folder": "NeoBank",
        "key_rules": "NEVER read card numbers aloud. ALWAYS verify DOB.",
        "sops": {
            "Fraud Alert": "1. Freeze card immediately. 2. Verify last 3 transactions. 3. Issue provisional credit.",
            "Account Closure": "1. Check retention offers. 2. If declined, process close. 3. Send confirmation email.",
            "Password Reset": "1. Verify identity via DOB + last 4 SSN. 2. Send OTP to registered phone. 3. Guide through reset process."
        }
    },
    "GlowCosmetics": {
        "industry": "E-Commerce Retail",
        "tone": "High Energy, 'Bestie' Vibe, Excited",
        "directive": "Frame selling as 'Treating yourself'. Use emojis. Focus on discounts and exclusives. Terms: 'Glow', 'Fam', 'Love that for you'.",
        "kb_folder": "GlowCosmetics",
        "key_rules": "Offer 10% discount if they mention a competitor. No returns on open lipstick.",
        "sops": {
            "Order Status": "1. Search Order ID. 2. Check shipping partner status. 3. Empathize with delays.",
            "Product Recommendation": "1. Ask skin type. 2. Upsell the 'Glow Kit'. 3. Mention vegan ingredients.",
            "Returns": "1. Check return window (30 days). 2. Verify product condition. 3. Issue prepaid label."
        }
    }
}

# Mock Agent Database (would connect to HR system in production)
AGENT_DATABASE = {
    "Alex Chen": {
        "role": "L1 Associate",
        "manager": "Sarah Connor",
        "tenure": "2 Weeks",
        "latest_review": "High enthusiasm, but struggles with system navigation. Fumbles when customers ask distinct technical questions.",
        "focus_area": "Confidence & Tool Usage",
        "kpis": {"AHT": "High", "CSAT": "Average"}
    },
    "Jordan Smith": {
        "role": "L3 Specialist",
        "manager": "Kyle Reese",
        "tenure": "3 Years",
        "latest_review": "Excellent product knowledge. Sometimes skips compliance disclosures in favor of speed.",
        "focus_area": "Compliance Adherence",
        "kpis": {"AHT": "Low", "CSAT": "High"}
    },
    "Demo Agent": {
        "role": "L2 Senior Associate",
        "manager": "System Admin",
        "tenure": "Demo Mode",
        "latest_review": "Demonstration profile for executive review.",
        "focus_area": "Universal Competency",
        "kpis": {"AHT": "Optimal", "CSAT": "High"}
    }
}

# ==========================================
# SESSION STATE INITIALIZATION
# ==========================================

if 'accumulated_links' not in st.session_state: 
    st.session_state.accumulated_links = []
if 'last_processed_time' not in st.session_state: 
    st.session_state.last_processed_time = 0
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

# ==========================================
# STATIC FILE SERVER (Fix for 404 errors)
# ==========================================

class KnowledgeBaseHandler(SimpleHTTPRequestHandler):
    """Custom handler that serves from Knowledge_Base directory"""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=KB_DIR, **kwargs)
    
    def end_headers(self):
        # Add CORS headers for web compatibility
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Cache-Control', 'no-store, no-cache, must-revalidate')
        super().end_headers()
    
    def guess_type(self, path):
        # Ensure HTML files are served with correct MIME type
        if path.endswith('.html'):
            return 'text/html'
        elif path.endswith('.md'):
            return 'text/markdown'
        return super().guess_type(path)
    
    def log_message(self, format, *args):
        pass  # Suppress console spam

def start_file_server():
    """Start HTTP server in background thread"""
    if st.session_state.server_started:
        return
    
    def run_server():
        try:
            server = HTTPServer(('localhost', HTTP_PORT), KnowledgeBaseHandler)
            st.session_state.server_started = True
            print(f"📁 Knowledge Base server running on http://localhost:{HTTP_PORT}")
            server.serve_forever()
        except OSError as e:
            if "Address already in use" in str(e):
                st.session_state.server_started = True
                print(f"✓ Server already running on port {HTTP_PORT}")
            else:
                print(f"⚠️ Server error: {e}")
    
    if not st.session_state.server_started:
        server_thread = threading.Thread(target=run_server, daemon=True)
        server_thread.start()
        time.sleep(0.5)  # Give server time to start

# ==========================================
# KNOWLEDGE BASE SEARCH
# ==========================================

def search_kb(client, query_text):
    """Search knowledge base files for relevant content"""
    if not client or not os.path.exists(os.path.join(KB_DIR, client)):
        print(f"⚠️ Client path not found: {KB_DIR}/{client}")
        return []
    
    if not query_text:
        return []
    
    words = query_text.lower().split()
    keywords = [w for w in words if len(w) > 2]  # Basic filtering - just length check
    
    if not keywords:
        print(f"⚠️ No keywords extracted from: {query_text}")
        return []
    
    print(f"🔍 Searching {client} for keywords: {keywords}")
    
    hits = []
    client_path = os.path.join(KB_DIR, client)
    
    # Scan files
    for filename in os.listdir(client_path):
        if filename.endswith(".md"):
            try:
                with open(os.path.join(client_path, filename), "r", encoding="utf-8") as f:
                    content = f.read().lower()
                
                # Scoring: filename matches worth more
                score = 0
                for k in keywords:
                    if k in content: 
                        score += 1
                    if k in filename.lower(): 
                        score += 3
                
                if score > 0:
                    # Check if HTML version exists, otherwise use MD
                    html_file = filename.replace(".md", ".html")
                    if os.path.exists(os.path.join(client_path, html_file)):
                        file_to_serve = html_file
                    else:
                        file_to_serve = filename
                    
                    hit = {
                        "id": filename,
                        "name": filename.replace(".md", "").replace("_", " ").title(),
                        "link": f"http://localhost:{HTTP_PORT}/{client}/{file_to_serve}",
                        "score": score,
                        "timestamp": time.time()
                    }
                    hits.append(hit)
                    print(f"  ✓ Found: {filename} (score: {score})")
            except Exception as e:
                print(f"  ❌ Error reading {filename}: {e}")
    
    hits.sort(key=lambda x: x['score'], reverse=True)
    print(f"  → Returning {len(hits)} results")
    return hits[:5]  # Return top 5

# ==========================================
# SPEECH RECOGNITION BACKGROUND THREAD
# ==========================================

def get_cable_index():
    """Find virtual audio cable device index"""
    if not SPEECH_AVAILABLE:
        return None
    try:
        mics = sr.Microphone.list_microphone_names()
        for i, name in enumerate(mics):
            if "CABLE Output" in name or "Stereo Mix" in name:
                return i
    except:
        pass
    return None

def run_listener(state_queue, stop_event):
    """Background speech recognition thread using Local Whisper"""
    if not SPEECH_AVAILABLE:
        print("⚠️ Speech recognition dependencies missing")
        return
    
    print("⏳ Loading Whisper Model (this may take a moment)...")
    try:
        # Load model only once
        audio_model = whisper.load_model("base") 
        print("✅ Whisper Model Loaded")
    except Exception as e:
        print(f"❌ Error loading Whisper: {e}")
        return

    r = sr.Recognizer()
    mic_index = get_cable_index()
    
    try:
        mic = sr.Microphone(device_index=mic_index)
    except Exception as e:
        print(f"⚠️ Microphone error: {e}")
        return
    
    print(f"🎧 Listener active on device index {mic_index}...")
    
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        r.dynamic_energy_threshold = True
        
        # CHANGED: Loop runs while the event is NOT set
        while not stop_event.is_set():
            try:
                print("👂 Listening...")
                # Shorter phrase time limit helps responsiveness
                audio = r.listen(source, timeout=2, phrase_time_limit=8)
                
                print("🧠 Transcribing...")
                text = r.recognize_whisper(audio, model="base", load_options=dict(device="cpu"))
                
                if text.strip():
                    print(f"🗣️ Heard: {text}")
                    state_queue.put({
                        "transcript": text,
                        "timestamp": time.time()
                    })
                
            except sr.WaitTimeoutError:
                continue
            except sr.UnknownValueError:
                continue
            except Exception as e:
                print(f"Listener error: {e}")
                # Brief pause to prevent rapid error looping
                time.sleep(0.5)

# ==========================================
# PILOT DOCUMENT GENERATION
# ==========================================

def build_pilot_document_components(agent_name, client_key, transcript, agent_context=""):
    """
    Build the structured components that form the pilot document.
    Returns a dict with each section for transparency.
    """
    agent_data = AGENT_DATABASE.get(agent_name, AGENT_DATABASE["Demo Agent"])
    client_data = CLIENT_CONFIG.get(client_key, CLIENT_CONFIG["NeoBank"])
    
    components = {
        "agent_profile": {
            "name": agent_name,
            "role": agent_data['role'],
            "manager": agent_data['manager'],
            "focus_area": agent_data['focus_area'],
            "performance_note": agent_data['latest_review']
        },
        "client_profile": {
            "name": client_key,
            "industry": client_data['industry'],
            "tone": client_data['tone'],
            "rules": client_data['key_rules'],
            "directive": client_data['directive']
        },
        "live_context": {
            "transcript": transcript,
            "agent_question": agent_context,
            "timestamp": time.time()
        },
        "available_sops": client_data['sops']
    }
    
    return components

def generate_pilot_doc_with_components(components):
    """Generate AI guidance using structured components"""
    if not model:
        return "⚠️ Error: Google API Key missing. Set GOOGLE_API_KEY environment variable."
    
    agent = components['agent_profile']
    client = components['client_profile']
    context = components['live_context']
    sops = components['available_sops']
    
    # Build context-aware prompt
    prompt = f"""
# SYSTEM ROLE: AI Research Assistant & Real-Time Coach

You are an expert AI assistant supporting a live call center agent.

---
## THE AGENT YOU ARE ASSISTING
* **Name:** {agent['name']}
* **Role:** {agent['role']} (Reports to: {agent['manager']})
* **Performance Context:** {agent['performance_note']}
* **Coaching Focus:** Pay special attention to "{agent['focus_area']}"

---
## THE CLIENT (Current Campaign)
* **Client:** {client['name']}
* **Industry:** {client['industry']}
* **Voice & Tone:** {client['tone']}
* **Strategy:** {client['directive']}
* **Critical Compliance Rules:** {client['rules']}

---
## LIVE SITUATION
* **Customer Said:** "{context['transcript']}"
* **Agent's Question/Context:** "{context['agent_question']}"

---
## AVAILABLE PROCEDURES
{json.dumps(sops, indent=2)}

---
## YOUR TASK
Provide real-time guidance for this agent. Structure your response as:

### 📋 SCRIPT (What to Say Right Now)
[Exact phrasing the agent can use, matching the client's tone]

### ✅ VERIFY (Data Points to Confirm)
[Bullet list of information to collect/verify]

### 💡 NEXT STEPS (Guidance)
[What should happen next in this interaction]

### 🎯 UPSELL/OPPORTUNITY (If Applicable)
[Any relevant product/service to mention based on context]

Keep it concise. The agent is reading this LIVE during the call.
"""
    
    try:
        # Gemini 2.0 Flash is strict. We must disable safety filters for "Scripting" tasks
        # or it often returns empty responses which crashes the app.
        safe_config = [
            {"category": "HARM_CATEGORY_HARASSMENT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_HATE_SPEECH", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_SEXUALLY_EXPLICIT", "threshold": "BLOCK_NONE"},
            {"category": "HARM_CATEGORY_DANGEROUS_CONTENT", "threshold": "BLOCK_NONE"},
        ]

        response = model.generate_content(
            prompt,
            safety_settings=safe_config,
            generation_config=genai.types.GenerationConfig(
                max_output_tokens=350, 
                temperature=0.4
            )
        )
        return response.text
    except Exception as e:
        print(f"API Error: {e}") # Print to terminal so you can see it
        return "⚠️ I couldn't generate a response. Please try again."

# ==========================================
# MANUAL SEARCH
# ==========================================

def perform_manual_search(query):
    """Manual knowledge base search"""
    if not query:
        return
    
    hits = search_kb(st.session_state.current_client, query)
    
    # Add to accumulated links
    current_ids = [item['id'] for item in st.session_state.accumulated_links]
    for hit in hits:
        if hit['id'] not in current_ids:
            hit['count'] = 'Manual'
            st.session_state.accumulated_links.insert(0, hit)
        else:
            # Move to top
            for existing in st.session_state.accumulated_links:
                if existing['id'] == hit['id']:
                    st.session_state.accumulated_links.remove(existing)
                    existing['count'] = 'Manual'
                    st.session_state.accumulated_links.insert(0, existing)
                    break
    
    # Force UI refresh
    st.rerun()

# ==========================================
# UI LAYOUT
# ==========================================

# Start file server
start_file_server()

# Sidebar Controls
with st.sidebar:
    st.header("⚙️ Agent Console")
    
    # Agent Selection
    st.markdown("#### 👤 Logged In As")
    selected_agent = st.selectbox(
        "Agent Profile", 
        list(AGENT_DATABASE.keys()),
        index=list(AGENT_DATABASE.keys()).index(st.session_state.current_agent)
    )
    if selected_agent != st.session_state.current_agent:
        st.session_state.current_agent = selected_agent
        st.rerun()
    
    agent_info = AGENT_DATABASE[st.session_state.current_agent]
    st.caption(f"**Role:** {agent_info['role']} | **Focus:** {agent_info['focus_area']}")
    
    st.divider()
    
    # Client Selection
    st.markdown("#### 🏢 Active Campaign")
    new_client = st.selectbox(
        "Client", 
        list(CLIENT_CONFIG.keys()),
        index=list(CLIENT_CONFIG.keys()).index(st.session_state.current_client)
    )
    if new_client != st.session_state.current_client:
        st.session_state.current_client = new_client
        st.session_state.accumulated_links = []
        st.rerun()
    
    client_info = CLIENT_CONFIG[st.session_state.current_client]
    st.caption(f"**Industry:** {client_info['industry']}")
    
    st.divider()
    
# Speech Recognition Toggle
    st.markdown("#### 🎤 Live Transcription")
    
    # 1. Initialize the stop event control
    if 'stop_event' not in st.session_state:
        st.session_state.stop_event = threading.Event()

    if SPEECH_AVAILABLE:
        # 2. Toggle Button Logic
        if st.button("🔴 Start Listening" if not st.session_state.listening_active else "⏹️ Stop Listening"):
            st.session_state.listening_active = not st.session_state.listening_active
            
            if st.session_state.listening_active:
                # STARTING: Clear the stop signal (make it False)
                st.session_state.stop_event.clear()
                
                if 'listener_queue' not in st.session_state:
                    st.session_state.listener_queue = queue.Queue()
                
                # Start thread if it's not already running
                if 'listener_thread' not in st.session_state or not st.session_state.listener_thread.is_alive():
                    st.session_state.listener_thread = threading.Thread(
                        target=run_listener, 
                        # Pass the queue AND the stop_event
                        args=(st.session_state.listener_queue, st.session_state.stop_event),
                        daemon=True
                    )
                    st.session_state.listener_thread.start()
            else:
                # STOPPING: Set the stop signal (make it True)
                st.session_state.stop_event.set()
                st.rerun()
        
        status_text = "🟢 ACTIVE" if st.session_state.listening_active else "⚫ IDLE"
        st.caption(f"Status: {status_text}")
    else:
        st.warning("Speech recognition not installed")
    
    st.divider()
    
    # Manual Search
    st.markdown("#### 🔎 Manual KB Search")
    search_query = st.text_input("Search knowledge base...", key="search_box")
    if st.button("Search", type="secondary"):
        perform_manual_search(search_query)
    
    st.divider()
    
    # Utilities
    if st.button("🗑️ Clear Knowledge Stream"):
        st.session_state.accumulated_links = []
        st.rerun()
    
    if st.button("📄 Clear Chat History"):
        st.session_state.chat_history = []
        st.rerun()

# Main Header
c1, c2, c3 = st.columns([1, 4, 1])
with c1:
    st.image("https://placehold.co/80x80/4A90E2/white?text=UA", width=80)
with c2:
    st.title(f"🌐 Universal Agent | {st.session_state.current_client}")
    st.caption(f"Connected • Agent: {st.session_state.current_agent} • {client_info['tone']}")
with c3:
    st.metric("Session", "LIVE", delta="Active")

st.divider()

# Check for new transcripts from listener
if st.session_state.listening_active and 'listener_queue' in st.session_state:
    try:
        while not st.session_state.listener_queue.empty():
            data = st.session_state.listener_queue.get_nowait()
            transcript = data['transcript']
            
            # Search KB
            hits = search_kb(st.session_state.current_client, transcript)
            
            # Add hits to stream
            current_ids = [item['id'] for item in st.session_state.accumulated_links]
            for hit in hits:
                if hit['id'] not in current_ids:
                    hit['count'] = 1
                    st.session_state.accumulated_links.insert(0, hit)
                else:
                    # Increment count and move to top
                    for existing in st.session_state.accumulated_links:
                        if existing['id'] == hit['id']:
                            st.session_state.accumulated_links.remove(existing)
                            existing['count'] = existing.get('count', 1) + 1
                            st.session_state.accumulated_links.insert(0, existing)
                            break
            
            # Store last transcript
            if 'last_transcript' not in st.session_state:
                st.session_state.last_transcript = ""
            st.session_state.last_transcript = transcript
            
    except queue.Empty:
        pass

# Auto-refresh when listening
# LOGIC FIX: Only autorefresh if we aren't currently waiting for a chat response
# We check if the last message was from the user. If so, we are "thinking", so don't refresh!
is_thinking = False
if st.session_state.chat_history:
    if st.session_state.chat_history[-1]['role'] == "user":
        is_thinking = True

if st.session_state.listening_active and not is_thinking:
    st_autorefresh(interval=1000, key="live_refresh")

# Main Workspace
left, middle, right = st.columns([1, 1.5, 1.5])

# LEFT: Knowledge Stream
with left:
    st.subheader("📚 Knowledge Stream")
    st.caption("Live-triggered articles & search results")
    
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
                display:block; background:#f8f9fa; padding:12px; border-radius:6px; 
                text-decoration:none; color:#0066cc; border-left: 4px solid #0066cc; 
                margin-bottom:8px; transition: all 0.2s;">
                <b>{item['name']}</b> 
                <span style='float:right; font-size:0.9em;'>{freq_badge}</span>
                </a>
                """,
                unsafe_allow_html=True
            )
    else:
        st.info("🎯 Waiting for triggers or manual search...")

# MIDDLE: Agent Buddy Chat
with middle:
    st.subheader("💬 Agent Buddy")
    st.caption("Ask questions, get context, request guidance")
    
    # Display last transcript if listening
    if st.session_state.listening_active and 'last_transcript' in st.session_state:
        st.info(f"**🎧 Last Heard:** \"{st.session_state.last_transcript}\"")
    
    # Chat interface
    chat_container = st.container(height=300)
    with chat_container:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything..."):
        # 1. Append User Message immediately
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # 2. Force a rerun immediately to SHOW the user message and PAUSE the autorefresh (via is_thinking logic)
        st.rerun()

    # Process the response in the NEXT run (where is_thinking is True)
    if st.session_state.chat_history and st.session_state.chat_history[-1]['role'] == "user":
        # Get context
        transcript_context = st.session_state.get('last_transcript', '')
        last_prompt = st.session_state.chat_history[-1]['content']
        
        components = build_pilot_document_components(
            st.session_state.current_agent,
            st.session_state.current_client,
            transcript_context,
            last_prompt
        )
        st.session_state.pilot_doc_components = components
        
        with st.spinner("⚡ Generating Guidance..."):
            response_text = generate_pilot_doc_with_components(components)
        
        # Append Assistant Response
        st.session_state.chat_history.append({"role": "assistant", "content": response_text})
        
        # Rerun to restart the autorefresh and show the result
        st.rerun()

# RIGHT: Pilot Document X-Ray
with right:
    st.subheader("🔬 Pilot Document X-Ray")
    st.caption("See how the AI guidance is assembled")
    
    if st.session_state.pilot_doc_components:
        comp = st.session_state.pilot_doc_components
        
        with st.expander("🎯 Layer 1: Agent Profile", expanded=False):
            st.json(comp['agent_profile'])
        
        with st.expander("🏢 Layer 2: Client Context", expanded=False):
            st.json(comp['client_profile'])
        
        with st.expander("💬 Layer 3: Live Situation", expanded=True):
            st.json(comp['live_context'])
        
        with st.expander("📋 Layer 4: Available SOPs", expanded=False):
            st.json(comp['available_sops'])
        
        st.success("✓ All layers combined → AI generates pilot guidance")
    else:
        st.info("💡 Ask a question in Agent Buddy to see the assembly process")

# Footer
st.divider()

# Check KB status
kb_status = "✅" if os.path.exists(KB_DIR) else "❌"
try:
    client_path = os.path.join(KB_DIR, st.session_state.current_client)
    if os.path.exists(client_path):
        article_count = len([f for f in os.listdir(client_path) if f.endswith('.md')])
        kb_info = f"{kb_status} {article_count} articles"
    else:
        kb_info = "❌ Client folder missing"
except:
    kb_info = "❌ KB error"

server_status = '🟢 Connected' if st.session_state.server_started else '🔴 Starting...'
st.caption(f"🌐 Universal Agent System | KB: {kb_info} | Server: http://localhost:{HTTP_PORT} ({server_status})")
