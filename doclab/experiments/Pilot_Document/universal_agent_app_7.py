import streamlit as st
import json
import os
import time
import re
import google.generativeai as genai
import pyperclip
from glob import glob

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(page_title="Universal Agent v7", layout="wide", page_icon="🌐")

TRANSCRIPT_FILE = "live_log.txt"
KB_DIR = "Knowledge_Base"
HTTP_PORT = 8765

# API Setup
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

# ==========================================
# 1. ASSET LOADING & HELPERS
# ==========================================

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
AGENTS = load_json_assets("config/agents") # Added back for Admin Panel
LIVE_PROMPT_TEMPLATE = load_prompt("live_guidance.md")

# ==========================================
# 2. STATE MANAGEMENT
# ==========================================

if 'current_client_id' not in st.session_state: st.session_state.current_client_id = list(CLIENTS.keys())[0]
if 'current_agent_id' not in st.session_state: st.session_state.current_agent_id = list(AGENTS.keys())[0] if AGENTS else "Default"
if 'extracted_context' not in st.session_state: st.session_state.extracted_context = {}
if 'chat_history' not in st.session_state: st.session_state.chat_history = []
if 'accumulated_links' not in st.session_state: st.session_state.accumulated_links = []
if 'last_processed_line' not in st.session_state: st.session_state.last_processed_line = 0

# ==========================================
# 3. CORE LOGIC (KB & SEARCH)
# ==========================================

def search_kb(client_id, query_text):
    """The Logic that finds articles based on text"""
    client_config = CLIENTS.get(client_id, {})
    client_name = client_config.get('name', 'General')
    # Map friendly name to folder name if needed, or use ID. 
    # For this demo, we assume folder name matches client ID or Name.
    # We will search the Client's specific folder.
    
    target_dir = os.path.join(KB_DIR, client_id)
    # If folder doesn't exist, try the name
    if not os.path.exists(target_dir):
        target_dir = os.path.join(KB_DIR, client_config.get('name', '').replace(" ", ""))
    
    if not os.path.exists(target_dir):
        return []

    words = query_text.lower().split()
    keywords = [w for w in words if len(w) > 3] # Filter small words
    if not keywords: return []

    hits = []
    for filename in os.listdir(target_dir):
        if filename.endswith(".md"):
            try:
                with open(os.path.join(target_dir, filename), "r", encoding="utf-8") as f:
                    content = f.read().lower()
                
                score = 0
                for k in keywords:
                    if k in content: score += 1
                    if k in filename.lower(): score += 3 # Title match weighs heavily
                
                if score > 0:
                    hits.append({
                        "id": filename,
                        "name": filename.replace(".md", "").replace("_", " ").title(),
                        "score": score,
                        "count": 1,
                        "client": client_id
                    })
            except: pass
    
    hits.sort(key=lambda x: x['score'], reverse=True)
    return hits[:3] # Top 3 only to avoid clutter

def parse_clipboard_context(client_id):
    """Gimme That Logic"""
    try: content = pyperclip.paste()
    except: return {"Error": "Clipboard Error"}
    if not content: return {"Info": "Clipboard Empty"}
    
    client = CLIENTS.get(client_id, {})
    parsers = client.get("context_parser", {})
    extracted = {}
    for field, pattern in parsers.items():
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match: extracted[field] = match.group(1).strip()
    return extracted if extracted else {"Info": "No patterns matched."}

def generate_guidance(query, transcript_lines):
    """AI Brain"""
    if not model: return "⚠️ API Key Missing"
    client = CLIENTS[st.session_state.current_client_id]
    context_str = json.dumps(st.session_state.extracted_context)
    recent_transcript = "".join(transcript_lines[-15:])
    
    prompt = LIVE_PROMPT_TEMPLATE.format(
        client_name=client['name'],
        context_data=context_str,
        tone=client['tone'],
        transcript_history=recent_transcript,
        user_query=query,
        compliance_list=json.dumps(client.get('compliance_checklist', [])),
        upsell_targets=json.dumps(client.get('upsell_strategy', {}))
    )
    try:
        res = model.generate_content(prompt)
        return res.text
    except: return "⚠️ AI Generation Failed"

# ==========================================
# 4. UI FRAGMENTS (The Two Heartbeats)
# ==========================================

@st.fragment(run_every=1)
def render_knowledge_panel():
    """HEARTBEAT 1: The Display. Updates every 1s to show links found by the other fragment."""
    if st.session_state.accumulated_links:
        for item in st.session_state.accumulated_links:
            badge = "🔍" if item.get('count') == "Manual" else "🔥"
            # Simple Card UI
            st.markdown(f"""
            <div style="background:#262730; padding:10px; border-radius:5px; margin-bottom:8px; border-left:3px solid #FF4B4B;">
                <div style="font-weight:bold; color:#FAFAFA;">{item['name']}</div>
                <div style="font-size:0.8em; color:#AAA;">{badge} Relevance Score: {item['score']}</div>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Waiting for triggers...")

@st.fragment(run_every=1)
def render_transcript_watcher():
    """HEARTBEAT 2: The Processor. Reads log, updates transcript, runs KB search silently."""
    
    # 1. READ LOG
    lines = []
    if os.path.exists(TRANSCRIPT_FILE):
        with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
            
    # 2. PROCESS NEW LINES FOR KB
    if len(lines) > st.session_state.last_processed_line:
        # We have new text!
        new_text_block = " ".join(lines[st.session_state.last_processed_line:])
        
        # Run Search
        hits = search_kb(st.session_state.current_client_id, new_text_block)
        
        # Update Session State (This triggers the other fragment to render next cycle)
        current_ids = [item['id'] for item in st.session_state.accumulated_links]
        for hit in hits:
            if hit['id'] not in current_ids:
                st.session_state.accumulated_links.insert(0, hit)
            else:
                # Move to top
                for existing in st.session_state.accumulated_links:
                    if existing['id'] == hit['id']:
                        st.session_state.accumulated_links.remove(existing)
                        st.session_state.accumulated_links.insert(0, existing)
                        break
        
        # Update Index
        st.session_state.last_processed_line = len(lines)

    # 3. RENDER TRANSCRIPT UI
    if lines:
        log_text = "".join(lines[-20:])
        st.text_area("Live Transcript", value=log_text, height=200, disabled=True, label_visibility="collapsed")
    else:
        st.caption("Waiting for active_listener.py...")

# ==========================================
# MAIN LAYOUT
# ==========================================

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Admin Panel")
    
    # Client Switcher
    c_names = {k: v['name'] for k, v in CLIENTS.items()}
    sel_c = st.selectbox("Active Client", options=list(c_names.keys()), format_func=lambda x: c_names[x])
    if sel_c != st.session_state.current_client_id:
        st.session_state.current_client_id = sel_c
        st.session_state.extracted_context = {}
        st.session_state.accumulated_links = [] # Clear KB on switch
        st.session_state.last_processed_line = 0 # Reset transcript index
        st.rerun()

    # Agent Switcher
    a_names = {k: v['name'] for k, v in AGENTS.items()} if AGENTS else {"Default": "Default Agent"}
    sel_a = st.selectbox("Logged in Agent", options=list(a_names.keys()), format_func=lambda x: a_names.get(x, x))
    if sel_a != st.session_state.current_agent_id:
        st.session_state.current_agent_id = sel_a
        st.rerun()

    st.divider()
    
    # Gimme That
    st.markdown("#### 📋 Tools")
    if st.button("🧲 Gimme That (Paste)", type="primary"):
        data = parse_clipboard_context(st.session_state.current_client_id)
        st.session_state.extracted_context = data
        if "Error" not in data: st.toast("Context Loaded!")
    
    # Manual KB Search (Restored)
    st.divider()
    st.markdown("#### 🔎 Manual Search")
    kb_q = st.text_input("Query", key="kb_manual_input")
    if st.button("Search"):
        man_hits = search_kb(st.session_state.current_client_id, kb_q)
        for h in man_hits:
            h['count'] = 'Manual'
            # Insert at top
            st.session_state.accumulated_links.insert(0, h)
        st.rerun()

# --- WORKSPACE ---
current_client = CLIENTS[st.session_state.current_client_id]
st.title(f"🌐 {current_client['name']}")

# Show Extracted Context if available
if st.session_state.extracted_context:
    with st.expander("🔌 Active Session Context", expanded=True):
        st.json(st.session_state.extracted_context)

col_kb, col_chat, col_pilot = st.columns([1, 1.8, 1.2])

# LEFT: KNOWLEDGE STREAM (Heartbeat 1)
with col_kb:
    st.subheader("📚 Stream")
    render_knowledge_panel()

# MIDDLE: TRANSCRIPT & CHAT (Heartbeat 2)
with col_chat:
    st.subheader("📝 Live Log")
    render_transcript_watcher()
    
    st.divider()
    st.subheader("💬 AI Co-Pilot")
    
    # Chat History
    chat_box = st.container(height=300)
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])

    # Chat Input
    if prompt := st.chat_input("Ask for guidance..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Read log fresh
        lines = []
        if os.path.exists(TRANSCRIPT_FILE):
             with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f: lines = f.readlines()
        
        with st.spinner("Analyzing..."):
            resp = generate_guidance(prompt, lines)
        
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        st.rerun()

# RIGHT: PILOT DOC (Static)
with col_pilot:
    st.subheader("📋 Pilot Document")
    
    # Tools
    tools = current_client.get("tools", {})
    cols = st.columns(len(tools)) if tools else []
    for i, (name, url) in enumerate(tools.items()):
        cols[i].markdown(f"[{name}]({url})")
    
    st.markdown("---")
    
    # Compliance
    st.markdown("##### ✅ Compliance")
    for item in current_client.get("compliance_checklist", []):
        st.checkbox(item, key=f"comp_{item}")
        
    # Upsell
    upsell = current_client.get("upsell_strategy", {})
    if upsell:
        st.info(f"**Target:** {upsell.get('Target')}\n\n**Pitch:** \"{upsell.get('Pitch')}\"")
        
    # Rules
    with st.expander("Rules & SOPs"):
        st.write(f"**Tone:** {current_client['tone']}")
        st.json(current_client.get("sops", {}))