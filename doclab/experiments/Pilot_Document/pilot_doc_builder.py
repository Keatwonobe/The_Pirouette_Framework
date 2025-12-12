import streamlit as st
import json
from datetime import datetime

# --- PAGE CONFIGURATION ---
st.set_page_config(page_title="AI Pilot Doc Builder", layout="wide")

# --- 1. MOCK DATABASE (Simulating your Backend) ---

def get_agent_database():
    """Simulates the HR/Performance System"""
    return {
        "Alex Chen (New Hire)": {
            "role": "L1 Associate",
            "manager": "Sarah Connor",
            "tenure": "2 Weeks",
            "latest_review": "High enthusiasm, but struggles with system navigation. Fumbles when customers ask distinct technical questions.",
            "focus_area": "Confidence & Tool Usage",
            "kpis": {"AHT": "High", "CSAT": "Average"}
        },
        "Jordan Smith (Senior)": {
            "role": "L3 Specialist",
            "manager": "Kyle Reese",
            "tenure": "3 Years",
            "latest_review": "Excellent product knowledge. Sometimes skips compliance disclosures in favor of speed.",
            "focus_area": "Compliance Adherence",
            "kpis": {"AHT": "Low", "CSAT": "High"}
        }
    }

def get_client_database():
    """Simulates the Client SOP/Knowledge Base"""
    return {
        "NeoBank (FinTech)": {
            "industry": "Banking",
            "voice": "Secure, Trustworthy, yet Modern and Casual.",
            "key_rules": "NEVER read card numbers aloud. ALWAYS verify DOB.",
            "sops": {
                "Fraud Alert": "1. Freeze card immediately. 2. Verify last 3 transactions. 3. Issue provisional credit.",
                "Account Closure": "1. Check retention offers. 2. If declined, process close. 3. Send confirmation email."
            }
        },
        "GlowCosmetics (Retail)": {
            "industry": "E-Commerce",
            "voice": "Bubbly, Excited, Best Friend energy.",
            "key_rules": "Offer 10% discount if they mention a competitor. No returns on open lipstick.",
            "sops": {
                "Order Status": "1. Search Order ID. 2. Check shipping partner status. 3. Empathize with delays.",
                "Product Recommendation": "1. Ask skin type. 2. Upsell the 'Glow Kit'. 3. Mention vegan ingredients."
            }
        }
    }

# --- 2. THE BUILDER LOGIC ---

def generate_pilot_document(agent_name, agent_data, client_name, client_data, task_type, specific_intent):
    """
    This function assembles the 'Pilot Document' (The Meta-Prompt)
    This is the text that would be sent to the LLM (GPT-4/Claude) invisibly.
    """
    
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # Constructing the Prompt
    prompt = f"""
# SYSTEM ROLE: AI RESEARCH ASSISTANT & COACH
You are an expert AI assistant sitting next to a human agent. 
Your goal is to help them complete the task of [{task_type}] successfully.

---
### 1. THE AGENT YOU ARE ASSISTING
* **Name:** {agent_name}
* **Role:** {agent_data['role']} (Report to: {agent_data['manager']})
* **Performance Context:** {agent_data['latest_review']}
* ** COACHING INSTRUCTION:** Please pay special attention to their focus area: "{agent_data['focus_area']}". 
*(If the user struggles with compliance, double-check their work. If they struggle with confidence, suggest authoritative phrasing.)*

---
### 2. THE MISSION (CLIENT CONTEXT)
* **Client:** {client_name}
* **Tone of Voice:** {client_data['voice']}
* **Critical Compliance:** {client_data['key_rules']}

---
### 3. CURRENT PROCEDURE (SOP)
* **Intent:** {specific_intent}
* **Standard Operating Procedure:** {client_data['sops'].get(specific_intent, "General Support Logic")}

---
### 4. YOUR INSTRUCTIONS
The agent is currently live. Monitor their inputs. 
Provide real-time guidance, suggested scripts, and data lookups.
Adjust your tone to be helpful and invisible to the customer.
"""
    return prompt

# --- 3. THE UI (The Presentation Layer) ---

st.title("✈️ Universal Agent: Pilot Document Builder")
st.markdown("### Dynamic Context Generation System")
st.markdown("---")

# Sidebar Controls
st.sidebar.header("Simulation Controls")

# Select Agent
agent_db = get_agent_database()
selected_agent = st.sidebar.selectbox("Select Agent (Login)", list(agent_db.keys()))
agent_info = agent_db[selected_agent]

# Select Client
client_db = get_client_database()
selected_client = st.sidebar.selectbox("Select Client Campaign", list(client_db.keys()))
client_info = client_db[selected_client]

# Select Task
task_type = st.sidebar.selectbox("Task Type", ["Inbound Call Handling", "Outbound Sales", "Lead Research", "Chat Support"])
specific_intent = st.sidebar.selectbox("Current Scenario", list(client_info['sops'].keys()))

# Main Display
col1, col2 = st.columns([1, 1.5])

with col1:
    st.subheader("1. Input Context Layers")
    
    with st.expander("Layer A: Agent Profile (HR Data)", expanded=True):
        st.info(f"**Agent:** {selected_agent}\n\n**Manager:** {agent_info['manager']}\n\n**Review Note:** _{agent_info['latest_review']}_")
        
    with st.expander("Layer B: Client Profile (Knowledge Base)", expanded=True):
        st.success(f"**Client:** {selected_client}\n\n**Voice:** {client_info['voice']}\n\n**Rules:** {client_info['key_rules']}")

    with st.expander("Layer C: Live Situation", expanded=True):
        st.warning(f"**Task:** {task_type}\n\n**Intent:** {specific_intent}")

with col2:
    st.subheader("2. Generated 'Pilot Document'")
    st.caption("This is the invisible 'Brain' generated instantly for the AI Model.")
    
    # Generate the prompt
    pilot_doc = generate_pilot_document(selected_agent, agent_info, selected_client, client_info, task_type, specific_intent)
    
    st.text_area("System Prompt (JSON/Text)", pilot_doc, height=500)
    
    st.markdown("### 3. Simulated AI Output")
    if st.button("Simulate AI Assistance"):
        st.markdown(f"""
        > **AI Assistant says:** > "Hi {selected_agent.split()[0]}! I see you're handling a **{specific_intent}** for **{selected_client}**. 
        >
        > Since your manager wants you to focus on **{agent_info['focus_area']}**, I have prepared the script below.
        >
        > **Suggested Opening:** *'{client_info['voice'].split(',')[0]}... thank you for calling {selected_client}!'*
        > 
        > **Step 1 Reminder:** {client_info['sops'][specific_intent].split('.')[0]}."
        """)