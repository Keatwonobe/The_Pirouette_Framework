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
    print("⚠️ Speech/Whisper not found.")

try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("⚠️ Pyperclip not found.")

# ==========================================
# CONFIG & ASSETS
# ==========================================

st.set_page_config(page_title="Universal Agent v5", layout="wide", page_icon="🎧")

KB_DIR = "Knowledge_Base"
HTTP_PORT = 8765

# API
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

# Load Assets
def load_json_assets(directory):
    assets = {}
    if not os.path.exists(directory): return {}
    for filepath in glob(os.path.join(directory, "*.json")):
        key = os.path.splitext(os.path.basename(filepath))[0]
        with open(filepath, 'r') as f: assets[key] = json.load(f)
    return assets

def load_prompt(filename):
    path = os.path.join("config/prompts", filename)
    if os.path.exists(path):
        with open(path, 'r') as f: return f.read()
    return ""

CLIENTS = load_json_assets("config/clients")
LIVE_PROMPT_TEMPLATE = load_prompt("live_guidance.md")

# ==========================================
# STATE MANAGEMENT
# ==========================================

if 'current_client_id' not in st.session_state: st.session_state.current_client_id = list(CLIENTS.keys())[0]
if 'extracted_context' not in st.session_state: st.session_state.extracted_context = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'transcript_log' not in st.session_state: st.session_state.transcript_log = []
if 'accumulated_links' not in st.session_state: st.session_state.accumulated_links = []
if 'listening_active' not in st.session_state: st.session_state.listening_active = False
if 'stop_event' not in st.session_state: st.session_state.stop_event = threading.Event()

# ==========================================
# CORE LOGIC
# ==========================================

def parse_clipboard_context(client_id):
    """Refined 'Gimme That' Logic"""
    if not CLIPBOARD_AVAILABLE: return {"Error": "No Pyperclip"}
    try:
        content = pyperclip.paste()
    except: return {"Error": "Clipboard Error"}
    
    if not content: return {"Info": "Clipboard Empty"}
    
    client = CLIENTS.get(client_id, {})
    parsers = client.get("context_parser", {})
    
    extracted = {}
    for field, pattern in parsers.items():
        # Multiline regex matching for better wiki scraping
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            extracted[field] = match.group(1).strip()
            
    return extracted if extracted else {"Info": "No patterns matched. Check Client Config."}

def generate_guidance(query):
    """The Brain"""
    if not model: return "⚠️ API Key Missing"
    
    client = CLIENTS[st.session_state.current_client_id]
    context_str = json.dumps(st.session_state.extracted_context)
    
    # Format the prompt with all the new rich data
    prompt = LIVE_PROMPT_TEMPLATE.format(
        client_name=client['name'],
        context_data=context_str,
        tone=client['tone'],
        transcript_history="\n".join(st.session_state.transcript_log[-10:]),
        user_query=query,
        compliance_list=json.dumps(client.get('compliance_checklist', [])),
        upsell_targets=json.dumps(client.get('upsell_strategy', {}))
    )
    
    try:
        res = model.generate_content(prompt)
        return res.text
    except: return "⚠️ AI Generation Failed"

def search_kb_manual(client_name, query):
    """Retaining the manual KB search as requested"""
    # (Simplified for this snippet, assumes file existence logic from v3)
    return [{"name": f"Article: {query}", "link": "#", "count": "Manual"}]

# ==========================================
# UI LAYOUT
# ==========================================

# --- SIDEBAR: CONTROLS ---
with st.sidebar:
    st.header("⚙️ Agent Console")
    
    # 1. Client Selector
    c_names = {k: v['name'] for k, v in CLIENTS.items()}
    sel_c = st.selectbox("Active Client", options=list(c_names.keys()), format_func=lambda x: c_names[x])
    if sel_c != st.session_state.current_client_id:
        st.session_state.current_client_id = sel_c
        st.session_state.extracted_context = {} 
        st.rerun()
    
    st.divider()
    
    # 2. The "Gimme That" Button
    st.markdown("#### 📋 Context Loader")
    if st.button("🧲 Gimme That (Paste)", type="primary"):
        data = parse_clipboard_context(st.session_state.current_client_id)
        st.session_state.extracted_context = data
        if "Error" not in data: st.toast("Context Loaded!")
    
    if st.session_state.extracted_context:
        st.json(st.session_state.extracted_context)
        
    st.divider()
    
    # 3. Legacy KB Search
    st.markdown("#### 🔎 KB Search")
    kb_q = st.text_input("Manual Search", key="kb_manual")
    if st.button("Search KB"):
        # Just mock functionality for demo continuity
        st.session_state.accumulated_links.insert(0, {"name": f"Result: {kb_q}", "link": "#", "count": "Manual"})
        st.rerun()

# --- MAIN STAGE ---
current_client = CLIENTS[st.session_state.current_client_id]
st.title(f"🌐 {current_client['name']} | Workspace")

col_kb, col_chat, col_pilot = st.columns([1, 1.8, 1.2])

# LEFT: KNOWLEDGE STREAM
with col_kb:
    st.subheader("📚 Knowledge")
    st.caption("Auto-retrieved articles")
    
    if st.session_state.accumulated_links:
        for item in st.session_state.accumulated_links:
            badge = "🔍" if item.get('count') == "Manual" else "🔥"
            st.markdown(f"""
            <div style="background:#262730; padding:10px; border-radius:5px; margin-bottom:5px; border-left:3px solid #FF4B4B;">
                <b>{item['name']}</b> <span style='float:right'>{badge}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Waiting for triggers...")

# MIDDLE: CHAT & TRANSCRIPT
with col_chat:
    # Transcript Log
    st.markdown("#### 📝 Live Transcript")
    st.text_area("Log", value="\n".join(st.session_state.transcript_log[-5:]), height=100, disabled=True, label_visibility="collapsed")
    
    st.divider()
    
    # Chat
    st.subheader("💬 AI Co-Pilot")
    chat_box = st.container(height=350)
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
                
    if prompt := st.chat_input("Ask for help..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.spinner("Analyzing rules & context..."):
            resp = generate_guidance(prompt)
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        st.rerun()

# RIGHT: PILOT DOCUMENT (The "Director's View")
with col_pilot:
    st.subheader("📋 Pilot Document")
    
    # 1. Quick Tools
    tools = current_client.get("tools", {})
    cols = st.columns(len(tools)) if tools else []
    for i, (name, url) in enumerate(tools.items()):
        cols[i].markdown(f"[{name}]({url})")

    # 2. COMPLIANCE CHECKLIST (New Feature)
    st.markdown("---")
    st.markdown("##### ✅ Compliance Timeline")
    checklist = current_client.get("compliance_checklist", [])
    for item in checklist:
        # Checkbox visually tracks progress (not persistant in this simple demo but demonstrates intent)
        st.checkbox(item, key=f"comp_{item}")

    # 3. UPSELL OPPORTUNITY (New Feature)
    st.markdown("---")
    st.markdown("##### 💰 Opportunity")
    upsell = current_client.get("upsell_strategy", {})
    if upsell:
        st.info(f"**Target:** {upsell.get('Target')}\n\n**Pitch:** \"{upsell.get('Pitch')}\"")

    # 4. Context/Rules (Legacy Collapsibles)
    st.markdown("---")
    with st.expander("🏢 Client Rules", expanded=False):
        st.write(f"**Tone:** {current_client['tone']}")
        st.error(f"**Directive:** {current_client['directive']}")
        
    with st.expander("📜 Standard Procedures", expanded=False):
        st.json(current_client.get("sops", {}))