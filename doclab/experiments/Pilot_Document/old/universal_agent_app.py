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
    import nltk
    from nltk.corpus import stopwords
    SPEECH_AVAILABLE = True
    # Setup NLTK
    try:
        nltk.data.find('corpora/stopwords')
    except LookupError:
        nltk.download('stopwords', quiet=True)
    stop_words = set(stopwords.words('english'))
except ImportError:
    SPEECH_AVAILABLE = False
    print("⚠️ Speech recognition not available. Install: pip install SpeechRecognition nltk")

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
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# ==========================================
# CLIENT PROFILES
# ==========================================

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
        return []
    
    if not query_text:
        return []
    
    words = query_text.lower().split()
    keywords = [w for w in words if len(w) > 2]  # Basic filtering
    
    if not keywords:
        return []
    
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
                    
                    hits.append({
                        "id": filename,
                        "name": filename.replace(".md", "").replace("_", " ").title(),
                        "link": f"http://localhost:{HTTP_PORT}/{client}/{file_to_serve}",
                        "score": score,
                        "timestamp": time.time()
                    })
            except Exception as e:
                print(f"Error reading {filename}: {e}")
    
    hits.sort(key=lambda x: x['score'], reverse=True)
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

def run_listener(state_queue):
    """Background speech recognition thread"""
    if not SPEECH_AVAILABLE:
        print("⚠️ Speech recognition not available")
        return
    
    r = sr.Recognizer()
    mic_index = get_cable_index()
    
    if mic_index is None:
        print("⚠️ No virtual audio cable found. Using default microphone.")
    
    try:
        mic = sr.Microphone(device_index=mic_index)
    except:
        print("⚠️ Microphone error. Speech recognition disabled.")
        return
    
    print(f"🎧 Listener active on device index {mic_index}...")
    
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        
        while st.session_state.listening_active:
            try:
                audio = r.listen(source, timeout=2, phrase_time_limit=5)
                text = r.recognize_google(audio)
                print(f"🗣️ Heard: {text}")
                
                # Put transcript in queue for main thread
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
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI Generation Error: {e}"

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
    if SPEECH_AVAILABLE:
        if st.button("🔴 Start Listening" if not st.session_state.listening_active else "⏹️ Stop Listening"):
            st.session_state.listening_active = not st.session_state.listening_active
            if st.session_state.listening_active:
                # Start listener thread
                if 'listener_queue' not in st.session_state:
                    st.session_state.listener_queue = queue.Queue()
                if 'listener_thread' not in st.session_state or not st.session_state.listener_thread.is_alive():
                    st.session_state.listener_thread = threading.Thread(
                        target=run_listener, 
                        args=(st.session_state.listener_queue,),
                        daemon=True
                    )
                    st.session_state.listener_thread.start()
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
if st.session_state.listening_active:
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
    if prompt := st.chat_input("Ask me anything... (e.g., 'How do I process a return?')"):
        # Add user message
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Get last transcript context
        transcript_context = st.session_state.get('last_transcript', 'No recent transcript')
        
        # Build components for transparency
        components = build_pilot_document_components(
            st.session_state.current_agent,
            st.session_state.current_client,
            transcript_context,
            prompt
        )
        st.session_state.pilot_doc_components = components
        
        # Generate response
        with st.spinner("🤔 Thinking..."):
            response = generate_pilot_doc_with_components(components)
        
        # Add assistant message
        st.session_state.chat_history.append({"role": "assistant", "content": response})
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
st.caption(f"🌐 Universal Agent System | Knowledge Base Server: http://localhost:{HTTP_PORT} | Status: {'🟢 Connected' if st.session_state.server_started else '🔴 Starting...'}")
