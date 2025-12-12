import streamlit as st
import json
from datetime import datetime
import time

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Pilot Doc Builder", layout="wide")

# --- SESSION STATE INITIALIZATION (For Auto-Fill) ---
if 'call_context' not in st.session_state:
    st.session_state['call_context'] = None

# --- 1. MOCK DATABASES ---
def get_agent_database():
    return {
        "Alex Chen": {
            "role": "L1 Associate",
            "manager": "Sarah Connor",
            "tenure": "2 Weeks",
            "latest_review": "High enthusiasm, but struggles with system navigation.",
            "focus_area": "Confidence & Tool Usage",
            "kpis": {"AHT": "High", "CSAT": "Average"}
        },
        "Jordan Smith": {
            "role": "L3 Specialist",
            "manager": "Kyle Reese",
            "tenure": "3 Years",
            "latest_review": "Excellent product knowledge. Sometimes skips compliance.",
            "focus_area": "Compliance Adherence",
            "kpis": {"AHT": "Low", "CSAT": "High"}
        }
    }

def get_client_database():
    return {
        "NeoBank": {
            "industry": "Banking",
            "voice": "Secure, Trustworthy, Modern.",
            "key_rules": "NEVER read card numbers aloud. ALWAYS verify DOB.",
            "sops": {
                "Fraud Alert": "1. Freeze card immediately. 2. Verify last 3 transactions.",
                "Account Closure": "1. Check retention offers. 2. If declined, process close."
            }
        },
        "GlowCosmetics": {
            "industry": "E-Commerce",
            "voice": "Bubbly, Excited, Best Friend energy.",
            "key_rules": "Offer 10% discount if competitor mentioned.",
            "sops": {
                "Order Status": "1. Search Order ID. 2. Check shipping partner status.",
                "Product Recommendation": "1. Ask skin type. 2. Upsell 'Glow Kit'."
            }
        }
    }

# --- 2. THE BUILDER LOGIC ---
def generate_pilot_document(agent_name, agent_data, client_name, client_data, intent):
    prompt = f"""
# SYSTEM ROLE: AI COACH
# CONTEXT INJECTION SOURCE: {st.session_state.get('source', 'Manual Selection')}

### 1. AGENT PROFILE ({agent_name})
* **Focus Area:** {agent_data['focus_area']}
* **Manager Note:** {agent_data['latest_review']}

### 2. CLIENT PROFILE ({client_name})
* **Voice:** {client_data['voice']}
* **Compliance:** {client_data['key_rules']}

### 3. LIVE INTENT ({intent})
* **SOP:** {client_data['sops'].get(intent, "General Logic")}
"""
    return prompt

# --- 3. THE UI ---

st.title("✈️ Universal Agent: CTI/CRM Integration Demo")

# --- SIDEBAR: THE "PUSH" SIMULATION ---
st.sidebar.header("🔌 CTI/CRM Bridge (The Push)")
st.sidebar.markdown("Simulate an automated data push from Salesforce or Twilio.")

# Button to simulate a "Pop" (Screen Pop)
if st.sidebar.button("📞 SIMULATE INCOMING CALL (NeoBank)"):
    st.session_state['call_context'] = {
        "agent": "Alex Chen",
        "client": "NeoBank",
        "intent": "Fraud Alert",
        "source": "Twilio CTI + Salesforce Webhook"
    }
    st.toast("Incoming Call Detected! Context Auto-Loaded.", icon="📡")

if st.sidebar.button("📧 SIMULATE EMAIL TICKET (Glow)"):
    st.session_state['call_context'] = {
        "agent": "Jordan Smith",
        "client": "GlowCosmetics",
        "intent": "Order Status",
        "source": "Zendesk Webhook"
    }
    st.toast("New Ticket Opened! Context Auto-Loaded.", icon="📨")

if st.sidebar.button("❌ CLEAR CONTEXT"):
    st.session_state['call_context'] = None
    st.rerun()

st.sidebar.markdown("---")
st.sidebar.header("Manual Controls (Fallback)")

# --- LOGIC TO HANDLE AUTOMATION VS MANUAL ---
agent_db = get_agent_database()
client_db = get_client_database()

# Determine selections based on Session State (Auto) OR Sidebar (Manual)
if st.session_state['call_context']:
    # AUTOMATED PATH
    auto_data = st.session_state['call_context']
    sel_agent = auto_data['agent']
    sel_client = auto_data['client']
    sel_intent = auto_data['intent']
    st.session_state['source'] = auto_data['source']
    
    st.info(f"🔒 **SYSTEM LOCKED BY CTI EVENT:** Incoming interaction for **{sel_client}** (Intent: {sel_intent})")
else:
    # MANUAL PATH
    sel_agent = st.sidebar.selectbox("Agent", list(agent_db.keys()))
    sel_client = st.sidebar.selectbox("Client", list(client_db.keys()))
    sel_intent = st.sidebar.selectbox("Intent", list(client_db[sel_client]['sops'].keys()))
    st.session_state['source'] = "Manual Selection"

# Retrieve Data Objects
agent_info = agent_db[sel_agent]
client_info = client_db[sel_client]

# --- MAIN DISPLAY ---
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("Live Context Stream")
    
    # Visualizing the Data Source
    if st.session_state['call_context']:
        st.success(f"**Data Source:** {st.session_state['source']}")
    else:
        st.warning("**Data Source:** Manual Operator Input")

    with st.expander("Incoming Payload (JSON)", expanded=True):
        # Displaying what the JSON payload from Salesforce/Twilio would look like
        payload = {
            "event_type": "incoming_call" if st.session_state.get('call_context') else "manual_selection",
            "dnis_target": sel_client,
            "ani_customer": "+1-555-0199",
            "crm_match": "High Value Customer",
            "detected_intent": sel_intent
        }
        st.json(payload)

with col2:
    st.subheader("Generated Pilot Document")
    pilot_doc = generate_pilot_document(sel_agent, agent_info, sel_client, client_info, sel_intent)
    st.text_area("LLM System Prompt", pilot_doc, height=400)