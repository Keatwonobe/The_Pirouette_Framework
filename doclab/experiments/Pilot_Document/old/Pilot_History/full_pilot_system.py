# full_pilot_system.py
import streamlit as st
from fastapi import FastAPI
import uvicorn
import threading
import requests
import time
from collections import deque

# --- SHARED MEMORY (Simulating a Database) ---
# In a real app, use SQLite or a proper state manager
if 'transcript_log' not in st.session_state:
    st.session_state['transcript_log'] = deque(maxlen=20) # Keep last 20 lines
if 'crm_context' not in st.session_state:
    st.session_state['crm_context'] = {"status": "Waiting for CRM..."}

# --- PART A: THE API SERVER (Background Process) ---
api = FastAPI()
TRANSCRIPT_STORE = [] # Global list for the thread-safe exchange
CONTEXT_STORE = {}

@api.post("/ingest_audio")
def ingest_audio(data: dict):
    """Receives text from the Transcription Service"""
    line = f"**{data['speaker']}:** {data['text']}"
    TRANSCRIPT_STORE.append(line)
    return {"status": "ok"}

@api.post("/ingest_context")
def ingest_context(data: dict):
    """Receives screen data from Chrome Extension"""
    global CONTEXT_STORE
    CONTEXT_STORE = data
    return {"status": "updated"}

def run_api_server():
    uvicorn.run(api, host="127.0.0.1", port=8000, log_level="error")

# --- PART B: THE UI (Streamlit) ---
def main():
    st.set_page_config(page_title="AgentPilot Zero", layout="wide")
    
    # Start API Server on first run only
    if "api_started" not in st.session_state:
        t = threading.Thread(target=run_api_server, daemon=True)
        t.start()
        st.session_state["api_started"] = True

    # --- HEADER ---
    st.title("🛡️ AgentPilot Co-Pilot")
    
    # --- LIVE DASHBOARD ---
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("📡 Live Context")
        # Poll the global store for updates
        if CONTEXT_STORE:
            st.success(f"Connected: {CONTEXT_STORE.get('page_title', 'Unknown Page')}")
            st.json(CONTEXT_STORE)
            
            # MAGIC: Auto-suggest based on scraped ID
            if "Refund" in str(CONTEXT_STORE):
                 st.info("💡 **Recommendation:** Open Refund Flow (SOP-404)")
        else:
            st.warning("Waiting for CRM activity...")

    with col2:
        st.subheader("💬 Live Transcription")
        st.caption("Real-time feed from call audio")
        
        # Poll transcript store
        # In production, you'd use Streamlit's `st.empty()` for smoother updates
        container = st.container(height=400)
        
        # Add new lines from API to Session State
        while TRANSCRIPT_STORE:
            line = TRANSCRIPT_STORE.pop(0)
            st.session_state['transcript_log'].append(line)
            
        with container:
            for line in st.session_state['transcript_log']:
                st.markdown(line)
                
        # Auto-Refresh Logic (The "Heartbeat")
        time.sleep(1) 
        st.rerun()

if __name__ == "__main__":
    main()