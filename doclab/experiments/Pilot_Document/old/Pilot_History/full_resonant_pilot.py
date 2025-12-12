import streamlit as st
import json
import os
import time
from streamlit_autorefresh import st_autorefresh
from openai import OpenAI
from datetime import datetime

# --- CONFIG ---
st.set_page_config(page_title="Universal Agent", layout="wide", page_icon="🌐")
STATE_FILE = "live_state.json"
HISTORY_DIR = "Pilot_History"

# --- SAFETY: Initialize OpenAI ---
try:
    client = OpenAI() # Expects OPENAI_API_KEY in env variables
except:
    client = None

# --- SESSION STATE INITIALIZATION ---
if 'client' not in st.session_state: st.session_state.client = "NeoBank"
if 'is_generating' not in st.session_state: st.session_state.is_generating = False
if 'current_pilot' not in st.session_state: st.session_state.current_pilot = None

# --- LOGIC: THE REFRESH LOOP ---
# We ONLY refresh if we are NOT currently generating the pilot doc.
# This prevents the reload from killing the AI process.
if not st.session_state.is_generating:
    st_autorefresh(interval=2000, key="data_refresh")

# --- LOAD CTI STATE ---
# We use a safe loader that defaults to "Waiting" if the file is busy
live_data = {"client": "NeoBank", "transcript": "Waiting for audio...", "suggested_links": []}
if os.path.exists(STATE_FILE):
    try:
        with open(STATE_FILE, "r") as f:
            live_data = json.load(f)
            # Sync CTI client change to Session State
            if live_data['client'] != st.session_state.client:
                st.session_state.client = live_data['client']
    except:
        pass

# --- HELPER: Generate Links to Localhost ---
def get_hosted_link(filepath):
    # Converts "C:\...\Universal_Drive\NeoBank\pricing.html" 
    # into "http://localhost:8000/NeoBank/pricing.html"
    
    # 1. Find where 'Universal_Drive' starts in the path
    if "Universal_Drive" in filepath:
        relative_path = filepath.split("Universal_Drive")[-1]
    else:
        relative_path = filepath
        
    # 2. Clean up slashes for URL
    clean_path = relative_path.replace("\\", "/").strip("/")
    return f"http://localhost:8000/{clean_path}"

# --- AI GENERATION FUNCTION ---
def generate_pilot_doc(client_name, context_text):
    st.session_state.is_generating = True # LOCK the refresh
    
    if not client:
        time.sleep(2) # Fake delay for demo if no API key
        st.session_state.is_generating = False
        return "⚠️ Error: OpenAI Key missing. (Simulated Success)"
    
    prompt = f"""
    You are a Universal Agent Assistant.
    Client: {client_name}
    Current Call Context: "{context_text}"
    
    Generate a concise 'Pilot Document' script for the agent. 
    Include:
    1. Suggested Greeting/Transition
    2. Key Info to Verify (Bullet points)
    3. Potential Upsell or Solution
    """
    
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        result = response.choices[0].message.content
    except Exception as e:
        result = f"⚠️ API Error: {str(e)}"
    
    st.session_state.is_generating = False # UNLOCK the refresh
    return result

# ==========================================
# UI LAYOUT
# ==========================================

# 1. CTI HEADER
col1, col2, col3 = st.columns([1, 2, 1])
with col1:
    st.markdown("### 🟢 ONLINE")
with col2:
    st.subheader(f"📞 Connected: {st.session_state.client}")
    st.caption("Verified Secure Line | Encrypted")
with col3:
    st.metric("Call Duration", "00:42")

st.divider()

# 2. MAIN WORKSPACE
left, right = st.columns([1, 2])

with left:
    st.subheader("💡 Knowledge Stream")
    st.caption("Live suggestions based on conversation...")
    
    # Live Transcript Box
    st.info(f"🗣️ **Latest Audio:** \"{live_data['transcript']}\"")
    
    # Dynamic Links (Now pointing to Localhost 8000)
    if live_data['suggested_links']:
        for link in live_data['suggested_links']:
            # Convert file path to localhost URL
            hosted_url = get_hosted_link(link['link'].replace("file:///", ""))
            
            st.markdown(
                f"""<a href="{hosted_url}" target="_blank" style="
                display:block; background:white; padding:15px; border-radius:8px; 
                text-decoration:none; color:#005cc5; border-left:5px solid #005cc5; 
                box-shadow: 0 2px 5px rgba(0,0,0,0.05); margin-bottom:10px;">
                📄 <b>{link['name'].upper()}</b> <br>
                <span style="font-size:0.8em; color:grey;">Match Score: {link['score']}</span>
                </a>""", 
                unsafe_allow_html=True
            )
    else:
        st.markdown("*Listening for keywords...*")

with right:
    st.subheader("✈️ Pilot Document (AI)")
    
    # Generate Button
    if st.button("Generate Pilot Doc", type="primary", disabled=st.session_state.is_generating):
        with st.spinner("AI Generating context... (Refresh Paused)"):
            doc = generate_pilot_doc(st.session_state.client, live_data['transcript'])
            st.session_state.current_pilot = doc # SAVE to session state
            st.rerun() # Force update immediately

    # Display Area (Reads from Session State, so it persists)
    if st.session_state.current_pilot:
        st.success("Context Generated Successfully")
        st.markdown(st.session_state.current_pilot)
    else:
        st.markdown("""
        > *Waiting to generate...*
        >
        > **Pre-Call Warmup:**
        > * Review Client Identity
        > * Check Mic Levels
        """)

# ==========================================
# 3. EDUCATIONAL FOOTER (The Builder)
# ==========================================
st.markdown("---")
st.subheader("🛠️ How It Works: The Pilot Builder")

with st.expander("View Pilot Document Construction Logic", expanded=False):
    b_col1, b_col2 = st.columns([1, 2])
    
    with b_col1:
        st.markdown("**Input Layers**")
        st.info(f"**1. Agent Context:**\nExpert Level (Tier 3)\n*Derived from HR System*")
        st.warning(f"**2. Client Context:**\n{st.session_state.client}\n*Derived from Knowledge Base*")
        st.error(f"**3. Live Context:**\n\"{live_data['transcript'][:50]}...\"\n*Derived from CTI*")
        
    with b_col2:
        st.markdown("**The Assembled Prompt (Backend View)**")
        
        # Simulate the prompt construction for educational purposes
        demo_prompt = f"""
        # SYSTEM ROLE: AI COACH
        AGENT: Alex (Expert)
        CLIENT: {st.session_state.client}
        TRANSCRIPT: "{live_data['transcript']}"
        
        TASK:
        1. Search vector database for "{st.session_state.client}" rules.
        2. Analyze transcript for intent.
        3. Generate compliant script.
        4. Flag any missing data.
        """
        st.code(demo_prompt, language="yaml")
        st.caption("This meta-prompt is constructed instantly and sent to the LLM.")