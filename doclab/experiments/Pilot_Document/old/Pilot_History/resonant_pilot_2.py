# Save as app.py
import streamlit as st
import os
import time

# --- PAGE SETUP ---
st.set_page_config(page_title="Universal Agent", layout="wide", page_icon="🌐")

# --- HOSTING THE FILES LOCALLY ---
# In a real deployment, this points to the internal server.
# For the demo, we assume files are in 'Universal_Drive' relative to this script.
DRIVE_PATH = os.path.abspath("Universal_Drive")

# --- STYLING FOR CLARITY (International Friendly) ---
st.markdown("""
<style>
    .main { background-color: #f0f2f6; }
    .big-font { font-size: 1.2rem !important; }
    .status-ok { color: green; font-weight: bold; }
    .status-alert { color: red; font-weight: bold; }
    
    /* Disguised Framework Styles */
    .protocol-box { border-left: 5px solid #d32f2f; background: white; padding: 15px; border-radius: 5px; }
    .guide-box { border-left: 5px solid #2e7d32; background: white; padding: 15px; border-radius: 5px; }
    
    /* Tab Button Style */
    .tab-link {
        display: inline-block;
        padding: 10px 20px;
        background-color: #005cc5;
        color: white !important;
        text-decoration: none;
        border-radius: 5px;
        margin-right: 10px;
        font-weight: bold;
    }
    .tab-link:hover { background-color: #004494; }
</style>
""", unsafe_allow_html=True)

# --- SESSION STATE ---
if 'client' not in st.session_state: st.session_state.client = "NeoBank" # Default
if 'topic' not in st.session_state: st.session_state.topic = "greeting"

# --- HELPER FUNCTIONS ---
def get_file_content(client, topic, ext=".md"):
    try:
        path = os.path.join("Universal_Drive", client, f"{topic}{ext}")
        with open(path, "r") as f:
            return f.read()
    except:
        return "Content loading..."

def get_file_link(client, topic):
    # In a real server this would be http://server/files/...
    # For local demo, we use the file:// protocol or a relative path if hosted
    path = os.path.join(DRIVE_PATH, client, f"{topic}.html")
    return f"file:///{path}"

# --- SIDEBAR: SIMULATED CTI (The 'Ireland' Connection) ---
with st.sidebar:
    st.header("📞 CTI Bridge")
    st.caption("Status: CONNECTED (Voice Link Active)")
    
    # 1. Client Selector (Simulates the Phone Number recognition)
    st.session_state.client = st.selectbox("Active Line:", ["NeoBank", "GlowCosmetics"])
    
    st.divider()
    
    # 2. The 'Live Listener' (Wizard of Oz Triggers)
    st.subheader("🎧 Live Transcript")
    st.caption("System listening...")
    
    # This simulates the Speech-to-Text picking up keywords
    if st.button("Detected: 'Hello / Greeting'"):
        st.session_state.topic = "greeting"
    
    if st.button("Detected: 'Price / Cost'"):
        st.session_state.topic = "pricing"
        
    if st.button("Detected: 'Identity / Rules'"):
        st.session_state.topic = "identity"

# --- MAIN UI ---

# 1. TOP BAR: INSTANT CONTEXT
col1, col2 = st.columns([3, 1])
with col1:
    st.title(f"Serving: {st.session_state.client}")
with col2:
    st.metric("Session Health", "Stable", delta="No Errors")

st.markdown("---")

# 2. THE WORKSPACE
left_col, right_col = st.columns(2)

with left_col:
    st.subheader("🛑 The Rules (Protocol)")
    st.markdown(f"**Client:** {st.session_state.client}")
    
    # Load the Identity/Rules markdown
    identity_content = get_file_content(st.session_state.client, "identity")
    st.markdown(f"""<div class="protocol-box">{identity_content}</div>""", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Quick Reference Tabs (The Bulletproof Bookmarks)
    st.markdown("**📚 Reference Docs (Opens in New Tab):**")
    
    # Generate Links
    # NOTE: 'file:///' links often blocked by modern browsers for security if not configured. 
    # For the presentation, you can simply show these as buttons that expand content below, 
    # OR run a simple python http.server in the background. 
    # For this specific demo code, I will use streamlits 'link_button' to simulate.
    
    c1, c2 = st.columns(2)
    with c1:
        st.link_button("📑 Open Full Policy", "https://www.example.com") # Replace with local host if running server
    with c2:
        st.link_button("💲 Pricing Sheet", "https://www.example.com")

with right_col:
    st.subheader("✅ Suggested Action (Live Guide)")
    
    # Dynamic Topic Loading
    topic_content = get_file_content(st.session_state.client, st.session_state.topic)
    
    # Visual Feedback for Context Switching
    st.info(f"Context Trigger: **{st.session_state.topic.upper()}** detected.")
    
    st.markdown(f"""<div class="guide-box">{topic_content}</div>""", unsafe_allow_html=True)
    
    st.text_area("Agent Notes", placeholder="Type here...", height=100)

# --- FOOTER ---
st.markdown("---")
st.caption("Universal Agent System v1.0 | Connected to Global Knowledge Base")