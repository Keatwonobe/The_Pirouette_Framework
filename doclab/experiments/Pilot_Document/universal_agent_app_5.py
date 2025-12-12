import streamlit as st
import json
import os
import time
import threading
import queue
import re
import datetime
import google.generativeai as genai
from glob import glob

# Optional dependencies
try:
    import speech_recognition as sr
    import whisper
    SPEECH_AVAILABLE = True
except ImportError:
    SPEECH_AVAILABLE = False

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False

# ==========================================
# 1. MODULAR LOADING SYSTEM (The Support Node)
# ==========================================

def load_json_assets(directory):
    """Loads all JSON files from a directory into a dict keyed by filename"""
    assets = {}
    if not os.path.exists(directory): return {}
    for filepath in glob(os.path.join(directory, "*.json")):
        key = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, 'r') as f:
            assets[key] = json.load(f)
    return assets

def load_prompt(filename):
    """Loads a markdown prompt template"""
    path = os.path.join("config/prompts", filename)
    if os.path.exists(path):
        with open(path, 'r') as f: return f.read()
    return ""

# Load Assets
CLIENTS = load_json_assets("config/clients")
AGENTS = load_json_assets("config/agents")
LIVE_PROMPT_TEMPLATE = load_prompt("live_guidance.md")
NOTE_PROMPT_TEMPLATE = load_prompt("note_generator.md")

# ==========================================
# 2. CONFIG & STATE
# ==========================================

st.set_page_config(page_title="Universal Agent v4", layout="wide", page_icon="🌐")

api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

# Session State Init
if 'accumulated_links' not in st.session_state: st.session_state.accumulated_links = []
if 'current_client_id' not in st.session_state: st.session_state.current_client_id = list(CLIENTS.keys())[0]
if 'current_agent_id' not in st.session_state: st.session_state.current_agent_id = list(AGENTS.keys())[0]
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'transcript_log' not in st.session_state: st.session_state.transcript_log = []
if 'extracted_context' not in st.session_state: st.session_state.extracted_context = {}
if 'generated_note' not in st.session_state: st.session_state.generated_note = ""
if 'listening_active' not in st.session_state: st.session_state.listening_active = False
if 'stop_event' not in st.session_state: st.session_state.stop_event = threading.Event()

# ==========================================
# 3. LOGIC CORES (The "Gimme That" & Note Gen)
# ==========================================

def parse_clipboard_context(client_id):
    """The 'Gimme That' Logic: Reads clipboard -> Apply Regex -> Return Data"""
    if not CLIPBOARD_AVAILABLE:
        return {"Error": "Pyperclip not installed"}
    
    try:
        content = pyperclip.paste()
    except:
        return {"Error": "Clipboard Access Failed"}

    if not content: return {"Info": "Clipboard Empty"}

    client_config = CLIENTS.get(client_id, {})
    parsers = client_config.get("context_parser", {})
    
    extracted = {}
    for field, pattern in parsers.items():
        match = re.search(pattern, content, re.IGNORECASE)
        if match:
            extracted[field] = match.group(1)
            
    return extracted if extracted else {"Info": "No patterns matched"}

def generate_notes(client_id, transcript):
    """The 'Auto-Note' Logic: Transcript + Template -> LLM -> Text"""
    if not model: return "Error: No API Key"
    
    client_config = CLIENTS.get(client_id, {})
    template = client_config.get("note_template", "Summary: {transcript}")
    
    # Fill the prompt
    final_prompt = NOTE_PROMPT_TEMPLATE.format(
        note_template=template,
        transcript="\n".join(transcript[-20:]) # Last 20 lines to save tokens
    )
    
    try:
        res = model.generate_content(final_prompt)
        return res.text
    except Exception as e:
        return f"Generation Error: {e}"

def generate_live_guidance(query):
    """The Chat Logic"""
    if not model: return "Error: No API Key"
    
    client = CLIENTS[st.session_state.current_client_id]
    
    # Inject extracted context (The "Gimme That" data)
    context_str = json.dumps(st.session_state.extracted_context)
    
    prompt = LIVE_PROMPT_TEMPLATE.format(
        client_name=client['name'],
        context_data=context_str,
        tone=client['tone'],
        transcript_history="\n".join(st.session_state.transcript_log[-5:]),
        user_query=query
    )
    
    try:
        res = model.generate_content(prompt)
        return res.text
    except: return "Generation Error"

# ==========================================
# 4. BACKGROUND LISTENERS (Simulated for v4)
# ==========================================
# (Keeping this concise to focus on the new features. 
# In prod, insert the threaded listener from v3 here.)

@st.fragment(run_every=1)
def render_transcript_log():
    if st.session_state.transcript_log:
        st.text_area("Live Transcript", value="\n".join(st.session_state.transcript_log[-10:]), height=150, disabled=True)
    else:
        st.info("Waiting for audio...")

# ==========================================
# 5. UI LAYOUT (One Screen)
# ==========================================

# --- SIDEBAR: SETTINGS ---
with st.sidebar:
    st.header("⚙️ Config")
    
    # Dynamic Selectors based on JSON files
    c_names = {k: v['name'] for k, v in CLIENTS.items()}
    sel_c = st.selectbox("Client", options=list(c_names.keys()), format_func=lambda x: c_names[x])
    if sel_c != st.session_state.current_client_id:
        st.session_state.current_client_id = sel_c
        st.session_state.extracted_context = {} # Clear context on switch
        st.rerun()
        
    st.divider()
    
    # "Gimme That" Button (Sidebar version)
    st.markdown("#### 📋 Context Injector")
    if st.button("🧲 Gimme That (Paste)", help="Reads Clipboard & Parses"):
        data = parse_clipboard_context(st.session_state.current_client_id)
        st.session_state.extracted_context = data
        if "Error" not in data:
            st.success("Data Extracted!")
        else:
            st.warning("No matches found")
            
    # Show Extracted Data
    if st.session_state.extracted_context:
        st.json(st.session_state.extracted_context)

# --- MAIN SCREEN ---
current_client = CLIENTS[st.session_state.current_client_id]

st.title(f"🌐 {current_client['name']} | Dashboard")

col_kb, col_work, col_tools = st.columns([1, 2, 1])

# LEFT: KNOWLEDGE
with col_kb:
    st.subheader("📚 Stream")
    st.caption("Auto-suggested articles")
    st.info("Start speaking to trigger KB...")
    # (KB Logic from v3 would go here)

# MIDDLE: WORKSPACE
with col_work:
    # 1. Transcript (Fragment)
    render_transcript_log()
    
    # 2. Chat Interface
    st.divider()
    chat_box = st.container(height=300)
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
                
    # Input
    if prompt := st.chat_input("Ask Coach..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        resp = generate_live_guidance(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        st.rerun()

    # 3. Note Generator (The Closer)
    st.divider()
    if st.button("📝 Generate CRM Notes"):
        with st.spinner("Summarizing..."):
            note = generate_notes(st.session_state.current_client_id, st.session_state.transcript_log)
            st.session_state.generated_note = note
    
    if st.session_state.generated_note:
        st.text_area("Copy to CRM", value=st.session_state.generated_note, height=150)

# RIGHT: TOOLS & PILOT DOC
with col_tools:
    st.subheader("🚀 Quick Tools")
    
    # Dynamic Tool Buttons from JSON
    tools = current_client.get("tools", {})
    for tool_name, url in tools.items():
        # Streamlit doesn't support 'open in new tab' natively in buttons easily without markdown hack
        # This markdown button simulates a native app feel
        st.markdown(f'''
            <a href="{url}" target="_blank" style="text-decoration: none;">
                <div style="background-color: #262730; border: 1px solid #4A90E2; 
                            padding: 10px; border-radius: 5px; text-align: center; margin-bottom: 10px;
                            color: #FAFAFA; font-weight: bold;">
                    🔗 {tool_name.replace("_", " ")}
                </div>
            </a>
        ''', unsafe_allow_html=True)
        
    st.divider()
    
    with st.expander("🏢 Client Rules", expanded=True):
        st.write(f"**Tone:** {current_client['tone']}")
        st.warning(f"**Directive:** {current_client['directive']}")
        
    with st.expander("📜 SOP Reference"):
        st.json(current_client.get("sops", {}))