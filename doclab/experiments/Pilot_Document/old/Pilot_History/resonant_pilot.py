import streamlit as st
import os
import time
import random

# --- CONFIGURATION ---
st.set_page_config(
    page_title="Resonant Pilot: Universal Agent",
    page_icon="Δ",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- STYLING (Dark Mode / Sci-Fi Aesthetic) ---
st.markdown("""
<style>
    .main {
        background-color: #0e1117;
        color: #c9d1d9;
    }
    .stButton>button {
        width: 100%;
        border-radius: 4px;
        font-weight: bold;
    }
    .metric-card {
        background-color: #161b22;
        padding: 15px;
        border-radius: 8px;
        border-left: 4px solid #2ea043;
        margin-bottom: 10px;
    }
    .client-header {
        padding: 10px;
        border-radius: 5px;
        margin-bottom: 20px;
        text-align: center;
        font-weight: bold;
        font-size: 1.5em;
    }
    .resonance-high { border-left-color: #2ea043; } /* Green */
    .resonance-med { border-left-color: #dbab09; }  /* Yellow */
    .resonance-low { border-left-color: #f85149; }  /* Red */
</style>
""", unsafe_allow_html=True)

# --- DATA LOADER (The "OneDrive" Connection) ---
BASE_DIR = "Resonant_Drive"

def load_markdown(path):
    """Reads a markdown file from the local 'drive'."""
    try:
        full_path = os.path.join(BASE_DIR, path)
        with open(full_path, "r") as f:
            return f.read()
    except FileNotFoundError:
        return f"⚠️ Error: File not found at {path}. Please run the setup script."

# --- SESSION STATE ---
if 'call_active' not in st.session_state:
    st.session_state.call_active = False
if 'current_client' not in st.session_state:
    st.session_state.current_client = None
if 'dark_residue_score' not in st.session_state:
    st.session_state.dark_residue_score = 0.0

# --- SIDEBAR: DIRECTOR CONTROLS ---
with st.sidebar:
    st.title("Δ Resonant Control")
    st.markdown("---")
    
    mode = st.radio("Operating Mode", ["Director View (Dashboard)", "Agent View (Universal)"])
    
    if mode == "Agent View (Universal)":
        st.markdown("### 📡 Signal Simulator")
        st.info("Simulate incoming traffic to test Delta-Pilot adaptability.")
        
        if st.button("📞 Incoming: NeoBank (Secure)"):
            st.session_state.call_active = True
            st.session_state.current_client = "NeoBank"
            st.session_state.intent = "Fraud Alert"
        
        if st.button("📞 Incoming: GlowCosmetics (Retail)"):
            st.session_state.call_active = True
            st.session_state.current_client = "GlowCosmetics"
            st.session_state.intent = "Shipping Inquiry"

        if st.session_state.call_active:
            st.markdown("---")
            if st.button("⏹️ End Call & Calc Resonance"):
                st.session_state.call_active = False
                st.session_state.show_qa = True

# --- MAIN PAGE: DIRECTOR VIEW ---
if mode == "Director View (Dashboard)":
    st.title("🌐 Network Resonance Dashboard")
    st.markdown("*Monitoring Dark Residue (D) across active Frames.*")
    
    # Top Level Metrics
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Global Coherence (C)", "98.2%", "+1.4%")
    col2.metric("Dark Residue (D)", "12.4 J·s", "-45% vs Trad")
    col3.metric("Active Frames", "12", "Fully Resonant")
    col4.metric("Moral Efficiency (η)", "0.88", "Class A")

    st.markdown("### 🔭 Active Frame Status")
    
    # Simulate 7-Node Frame Visualization
    c1, c2, c3 = st.columns([1, 2, 1])
    
    with c2:
        st.markdown("""
        <div style="text-align:center; padding:20px; border:1px dashed #30363d; border-radius:10px;">
            <h4>Frame Alpha-7</h4>
            <p><i>Current State: High-Flow</i></p>
            <div style="display:flex; justify-content:center; gap:10px;">
                <div class="metric-card resonance-high">Core 1<br>NeoBank</div>
                <div class="metric-card resonance-high">Core 2<br>GlowCos</div>
                <div class="metric-card resonance-high">Core 3<br>TechSpt</div>
            </div>
            <div style="display:flex; justify-content:center; gap:10px; margin-top:10px;">
                <div class="metric-card resonance-med">Support A<br>Research</div>
                <div class="metric-card resonance-high">Interface<br>Leading</div>
                <div class="metric-card resonance-med">Support B<br>Docs</div>
            </div>
            <div style="margin-top:10px;">
                <span class="metric-card resonance-high">Feedback Node (QA)<br>Monitoring D-Field</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

# --- MAIN PAGE: AGENT VIEW ---
elif mode == "Agent View (Universal)":
    
    # EMPTY STATE
    if not st.session_state.call_active and not st.session_state.get('show_qa', False):
        st.markdown("""
        <div style="text-align:center; margin-top:100px; opacity:0.5;">
            <h1>Δ</h1>
            <h3>Universal Agent Standby</h3>
            <p>Waiting for signal injection...</p>
            <p><i>"Minimizing Dark Residue through Contextual Awareness"</i></p>
        </div>
        """, unsafe_allow_html=True)

    # CALL ACTIVE STATE
    elif st.session_state.call_active:
        client = st.session_state.current_client
        
        # Dynamic Header Styling based on Client
        header_color = "#005cc5" if client == "NeoBank" else "#d32f2f" if client == "TechCorp" else "#9e6a03"
        header_bg = "linear-gradient(90deg, #0d1117 0%, #1f6feb 100%)" if client == "NeoBank" else "linear-gradient(90deg, #0d1117 0%, #d2a8ff 100%)"
        
        st.markdown(f"""
        <div class="client-header" style="background: {header_bg}; color: white;">
            INCOMING: {client.upper()} | INTENT: {st.session_state.intent.upper()}
        </div>
        """, unsafe_allow_html=True)
        
        col_left, col_right = st.columns([1, 2])
        
        # LEFT: CONTEXT & RULES (The "Constraint Field")
        with col_left:
            st.subheader("🔒 Protocol (Γ-Field)")
            
            # Load Context
            context_md = load_markdown(f"01_Clients/{client}/context.md")
            st.info(context_md)
            
            # Load Auth Rules
            auth_md = load_markdown(f"01_Clients/{client}/auth_protocol.md")
            with st.expander("Authentication Rules", expanded=True):
                st.markdown(auth_md)

        # RIGHT: THE MODULE (The "Skill Field")
        with col_right:
            st.subheader("🚀 Pilot Module (C-Field)")
            
            # Determine which module to load based on intent
            if "Fraud" in st.session_state.intent:
                module_file = "technical_troubleshoot.md" # Placeholder matching your generated files
            elif "Shipping" in st.session_state.intent:
                module_file = "shipping_inquiry.md"
            else:
                module_file = "refund_process.md"
                
            # In a real app, we'd have specific files for every intent. 
            # For demo, we map to what we generated in step 1.
            try:
                sop_content = load_markdown(f"02_Modules/{module_file}")
                st.markdown(sop_content)
            except:
                st.warning("Module not found. Loading generic fallback.")
            
            st.markdown("---")
            st.text_area("📝 Live Note Capture (Auto-saving to OneDrive...)", height=150)

    # QA / FEEDBACK STATE
    elif st.session_state.get('show_qa', False):
        st.title("✨ Resonance Check")
        
        # Calculate fake score
        adherence = random.randint(94, 100)
        dark_residue_saved = random.uniform(0.8, 1.5)
        
        c1, c2, c3 = st.columns(3)
        c1.metric("Pilot Adherence", f"{adherence}%")
        c2.metric("Dark Residue Avoided", f"{dark_residue_saved:.2f} units")
        c3.metric("Customer Sentiment", "Positive")
        
        st.success(f"**System Note:** The 'Call Pop' mechanism successfully injected the correct Context (Γ) and Skill (C) modules. No manual search required. Friction minimized.")
        
        if st.button("Return to Standby"):
            st.session_state.show_qa = False
            st.rerun()