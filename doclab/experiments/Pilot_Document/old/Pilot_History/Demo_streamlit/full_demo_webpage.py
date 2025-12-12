import streamlit as st
import json
import os
import time
import google.generativeai as genai
from streamlit_autorefresh import st_autorefresh

# --- CONFIG ---
st.set_page_config(page_title="Universal Agent", layout="wide", page_icon="🌐")
STATE_FILE = "live_state.json"
KB_DIR = "Knowledge_Base"

# --- GEMINI SETUP ---
# Get API Key: https://aistudio.google.com/app/apikey
# Run in terminal: $env:GOOG_API_KEY="your_key_here" (PowerShell) or export GOOG_API_KEY="..." (Bash)
api_key = os.environ.get("GOOG_API_KEY")

if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-1.5-flash')
else:
    model = None

# --- CLIENT PROFILES (The "Flavor") ---
CLIENT_CONFIG = {
    "NeoBank": {
        "tone": "Professional, Empathetic, Secure.",
        "directive": "Frame all solutions as protecting the customer's assets. Use terms like 'Security', 'Verification', 'Peace of Mind'.",
        "kb_folder": "NeoBank"
    },
    "GlowCosmetics": {
        "tone": "High Energy, 'Bestie' Vibe, Excited.",
        "directive": "Frame selling as 'Treating yourself'. Use emojis. Focus on discounts and exclusives. Terms: 'Glow', 'Fam', 'Love that for you'.",
        "kb_folder": "GlowCosmetics"
    }
}

# --- SESSION STATE ---
if 'accumulated_links' not in st.session_state: st.session_state.accumulated_links = []
if 'last_processed_time' not in st.session_state: st.session_state.last_processed_time = 0
if 'manual_search_trigger' not in st.session_state: st.session_state.manual_search_trigger = False
if 'current_client' not in st.session_state: st.session_state.current_client = "NeoBank"

# --- HELPER: LOCALHOST LINKS ---
def get_hosted_link(filepath):
    # Assumes python -m http.server 8000 is running in parent dir
    if "Knowledge_Base" in filepath:
        part = filepath.split("Knowledge_Base")[-1]
        clean = part.replace("\\", "/").strip("/")
        # We assume the server root is where Knowledge_Base folder sits
        return f"http://localhost:8000/Knowledge_Base/{clean}"
    return filepath

# --- LOGIC: DATA SYNC ---
st_autorefresh(interval=1000, key="data_refresh")

live_data = {"client": "NeoBank", "transcript": "Waiting...", "new_hits": [], "last_update": 0}

if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            live_data = json.load(f)
            
        # 1. Sync Client from UI to JSON (if changed manually)
        if live_data['client'] != st.session_state.current_client:
            live_data['client'] = st.session_state.current_client
            # Write back to file so Pipeline switches context
            with open(STATE_FILE, "w") as f:
                json.dump(live_data, f)
        
        # 2. Append New Hits (Only if timestamp is new)
        if live_data['last_update'] > st.session_state.last_processed_time:
            new_items = live_data.get('new_hits', [])
            
            # Deduplicate and Add
            current_ids = [item['id'] for item in st.session_state.accumulated_links]
            for item in new_items:
                if item['id'] not in current_ids:
                    # Add count = 1 for ranking
                    item['count'] = 1
                    st.session_state.accumulated_links.insert(0, item) # Add to top
                else:
                    # If exists, move to top and increment 'count' (Importance Ranking)
                    for existing in st.session_state.accumulated_links:
                        if existing['id'] == item['id']:
                            existing['count'] = existing.get('count', 1) + 1
                            # Move to top list trick
                            st.session_state.accumulated_links.remove(existing)
                            st.session_state.accumulated_links.insert(0, existing)
                            break
            
            st.session_state.last_processed_time = live_data['last_update']
            
    except Exception as e:
        pass # File busy

# --- AI GENERATION ---
def generate_pilot_doc(client_key, context_text):
    if not model:
        return "⚠️ Error: Google API Key missing. Set GOOG_API_KEY."
    
    profile = CLIENT_CONFIG.get(client_key, {})
    
    prompt = f"""
    ROLE: Universal Call Center Agent
    CLIENT: {client_key}
    TONE GUIDE: {profile.get('tone')}
    STRATEGY: {profile.get('directive')}
    
    LIVE CONTEXT: "{context_text}"
    
    TASK: Generate a 'Pilot Document' (XML format).
    1. <script>: Exact phrasing for the agent to say NOW.
    2. <verify>: Bullet list of data to confirm.
    3. <upsell>: A relevant product pitch based on the context.
    
    Keep it concise. The agent is reading this live.
    """
    
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"⚠️ AI Error: {e}"

# --- MANUAL SEARCH LOGIC ---
def perform_manual_search(query):
    if not query: return
    client_path = os.path.join(KB_DIR, st.session_state.current_client)
    if not os.path.exists(client_path): return

    hits = []
    for filename in os.listdir(client_path):
        if filename.endswith(".md") and query.lower() in filename.lower():
             html_link = os.path.abspath(os.path.join(client_path, filename.replace(".md", ".html")))
             hits.append({
                "id": filename, 
                "name": filename.replace(".md", "").replace("_", " ").title(), 
                "link": f"file:///{html_link}",
                "count": "Manual"
            })
    
    # Add to stream
    for hit in hits:
        # Check dupe logic simplified for manual
        st.session_state.accumulated_links.insert(0, hit)

# ==========================================
# UI LAYOUT
# ==========================================

# SIDEBAR
with st.sidebar:
    st.header("⚙️ Agent Controls")
    
    # Client Selector
    new_client = st.selectbox("Active Client", list(CLIENT_CONFIG.keys()))
    if new_client != st.session_state.current_client:
        st.session_state.current_client = new_client
        st.session_state.accumulated_links = [] # Clear stream on client switch
        st.rerun()
        
    st.divider()
    
    # Manual Search
    st.markdown("#### 🔎 Manual Lookup")
    search_query = st.text_input("Search Knowledge Base...", key="search_box")
    if st.button("Search"):
        perform_manual_search(search_query)
        
    st.divider()
    
    # Clear Stream
    if st.button("🗑️ Clear Knowledge Stream"):
        st.session_state.accumulated_links = []
        st.rerun()

# MAIN HEADER
c1, c2, c3 = st.columns([1, 4, 1])
with c1: st.image("https://placehold.co/60x60/png", width=60)
with c2:
    st.title(f"{st.session_state.current_client} | Connected")
    st.caption(f"Profile: {CLIENT_CONFIG[st.session_state.current_client]['tone']}")
with c3:
    st.metric("Session Time", "01:24")

st.divider()

# WORKSPACE
left, right = st.columns([1, 2])

with left:
    st.subheader("📚 Knowledge Stream")
    st.caption("Live Context & Search Results (Auto-Appending)")
    
    if st.session_state.accumulated_links:
        for item in st.session_state.accumulated_links:
            # Render Link
            hosted_url = get_hosted_link(item['link'].replace("file:///", ""))
            
            # Visual ranking: darker blue for high counts
            freq_badge = f"🔥 {item['count']}" if isinstance(item['count'], int) and item['count'] > 1 else ""
            
            st.markdown(
                f"""<a href="{hosted_url}" target="_blank" style="
                display:block; background:white; padding:12px; border-radius:6px; 
                text-decoration:none; color:#005cc5; border:1px solid #e0e0e0; 
                border-left: 5px solid #005cc5; margin-bottom:8px;">
                <b>{item['name']}</b> <span style='float:right'>{freq_badge}</span>
                </a>""", 
                unsafe_allow_html=True
            )
    else:
        st.markdown("*Waiting for triggers...*")

with right:
    st.subheader("⚡ Pilot Document (Gemini Flash)")
    
    # Transcript Preview
    st.info(f"**Listening:** \"{live_data['transcript']}\"")
    
    if st.button("Generate Pilot Guidance", type="primary"):
        with st.spinner("Gemini is thinking..."):
            doc = generate_pilot_doc(st.session_state.current_client, live_data['transcript'])
            st.session_state.current_pilot = doc
    
    if 'current_pilot' in st.session_state and st.session_state.current_pilot:
        st.markdown(st.session_state.current_pilot)