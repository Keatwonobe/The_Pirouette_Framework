import streamlit as st
import json
import os
import time
import re
import datetime
import google.generativeai as genai
from glob import glob

# Optional dependencies
try:
    import pyperclip
    CLIPBOARD_AVAILABLE = True
except ImportError:
    CLIPBOARD_AVAILABLE = False
    print("⚠️ Pyperclip not found. 'Gimme That' will be disabled.")

# ==========================================
# CONFIGURATION
# ==========================================

st.set_page_config(page_title="Universal Agent v8", layout="wide", page_icon="🌀")

TRANSCRIPT_FILE = "live_log.txt"
KB_DIR = "Knowledge_Base"

# API Setup
api_key = os.environ.get("GOOGLE_API_KEY")
if api_key:
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash-exp')
else:
    model = None
    print("⚠️ GOOGLE_API_KEY not found. AI features disabled.")

# ==========================================
# 1. ASSET LOADING
# ==========================================

def load_json_assets(directory):
    """Load all JSON files from directory into dict"""
    assets = {}
    if not os.path.exists(directory): 
        return {}
    for filepath in glob(os.path.join(directory, "*.json")):
        key = os.path.splitext(os.path.basename(filepath))[0]
        try:
            with open(filepath, 'r', encoding='utf-8') as f: 
                assets[key] = json.load(f)
        except Exception as e:
            print(f"⚠️ Failed to load {filepath}: {e}")
    return assets

def load_prompt(filename):
    """Load markdown prompt template"""
    path = os.path.join("config/prompts", filename)
    if os.path.exists(path):
        try:
            with open(path, 'r', encoding='utf-8') as f: 
                return f.read()
        except Exception as e:
            print(f"⚠️ Failed to load {filename}: {e}")
    return ""

# Load all assets
CLIENTS = load_json_assets("config/clients")
AGENTS = load_json_assets("config/agents")
LIVE_PROMPT_TEMPLATE = load_prompt("live_guidance.md")
NOTE_PROMPT_TEMPLATE = load_prompt("note_generator.md")

# Fallback defaults if configs missing
if not CLIENTS:
    CLIENTS = {"default": {
        "name": "Default Client",
        "tone": "professional and helpful",
        "directive": "Provide excellent service",
        "context_parser": {},
        "compliance_checklist": [],
        "upsell_strategy": {},
        "tools": {},
        "sops": {}
    }}

if not AGENTS:
    AGENTS = {"default": {
        "name": "Default Agent",
        "experience": "General",
        "strengths": []
    }}

# ==========================================
# 2. STATE MANAGEMENT
# ==========================================

# Core State
if 'current_client_id' not in st.session_state: 
    st.session_state.current_client_id = list(CLIENTS.keys())[0]
if 'current_agent_id' not in st.session_state: 
    st.session_state.current_agent_id = list(AGENTS.keys())[0]

# Data Streams
if 'extracted_context' not in st.session_state: 
    st.session_state.extracted_context = {}
if 'accumulated_links' not in st.session_state: 
    st.session_state.accumulated_links = []
if 'chat_history' not in st.session_state: 
    st.session_state.chat_history = []
if 'last_processed_line' not in st.session_state: 
    st.session_state.last_processed_line = 0

# Three-Box Closer State
if 'agent_notes' not in st.session_state: 
    st.session_state.agent_notes = ""
if 'customer_summary' not in st.session_state: 
    st.session_state.customer_summary = ""
if 'generated_crm_note' not in st.session_state: 
    st.session_state.generated_crm_note = ""

# Compliance Tracking (per-client)
if 'compliance_state' not in st.session_state: 
    st.session_state.compliance_state = {}

# Demo Mode
if 'demo_mode' not in st.session_state: 
    st.session_state.demo_mode = False

# Sales Command Bar: per-session agent favorites
if 'sales_favorites' not in st.session_state:
    # list of {"label": str, "prompt": str}
    st.session_state.sales_favorites = []

# Live sentiment snapshot
if 'sentiment' not in st.session_state:
    # simple structure: label in {"Positive","Neutral","Negative"}, numeric score
    st.session_state.sentiment = {"label": "Neutral", "score": 0}


# ==========================================
# 3. CORE LOGIC - KB & SEARCH
# ==========================================

def search_kb(client_id, query_text):
    """Enhanced fuzzy KB search with phrase matching"""
    if not query_text or len(query_text) < 3:
        return []
    
    client_config = CLIENTS.get(client_id, {})
    
    # Find KB directory for this client
    target_dir = os.path.join(KB_DIR, client_id)
    if not os.path.exists(target_dir):
        target_dir = os.path.join(KB_DIR, client_config.get('name', '').replace(" ", ""))
    if not os.path.exists(target_dir):
        return []
    
    # Tokenize query
    query_lower = query_text.lower()
    words = re.findall(r'\b\w+\b', query_lower)
    keywords = [w for w in words if len(w) > 3]
    
    if not keywords:
        return []
    
    hits = []
    for filename in os.listdir(target_dir):
        if not filename.endswith(".md"):
            continue
            
        filepath = os.path.join(target_dir, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                content = f.read().lower()
            
            score = 0
            filename_lower = filename.lower()
            
            # Multi-word phrase matching (high priority)
            if len(keywords) > 1:
                phrase = " ".join(keywords)
                if phrase in content:
                    score += 10
                if phrase.replace(" ", "_") in filename_lower:
                    score += 15
            
            # Individual keyword matching
            for k in keywords:
                count = content.count(k)
                score += count
                
                if k in filename_lower:
                    score += 5
                if k in filename_lower.replace("_", " "):
                    score += 3
            
            if score > 0:
                hits.append({
                    "id": filename,
                    "name": filename.replace(".md", "").replace("_", " ").title(),
                    "score": score,
                    "count": 1,
                    "client": client_id,
                    "path": filepath
                })
        except Exception as e:
            print(f"⚠️ Error reading {filename}: {e}")
            continue
    
    hits.sort(key=lambda x: x['score'], reverse=True)
    return hits[:5]  # Top 5

def parse_clipboard_context(client_id):
    """'Gimme That' - Extract structured data from clipboard"""
    if not CLIPBOARD_AVAILABLE:
        return {"Error": "Pyperclip not installed"}
    
    try:
        content = pyperclip.paste()
    except Exception as e:
        return {"Error": f"Clipboard access failed: {e}"}
    
    if not content:
        return {"Info": "Clipboard is empty"}
    
    client = CLIENTS.get(client_id, {})
    parsers = client.get("context_parser", {})
    
    extracted = {}
    for field, pattern in parsers.items():
        match = re.search(pattern, content, re.IGNORECASE | re.MULTILINE)
        if match:
            extracted[field] = match.group(1).strip()
    
    return extracted if extracted else {"Info": "No patterns matched clipboard content"}

# ==========================================
# 4. AI GENERATION
# ==========================================

def generate_guidance(query, transcript_lines):
    """AI Co-Pilot - Context-aware guidance"""
    if not model:
        return "⚠️ AI unavailable (API key missing)"
    
    client = CLIENTS[st.session_state.current_client_id]
    agent = AGENTS[st.session_state.current_agent_id]
    
    context_str = json.dumps(st.session_state.extracted_context, indent=2)
    recent_transcript = "".join(transcript_lines[-15:])
    
    if not LIVE_PROMPT_TEMPLATE:
        # Fallback prompt if template missing
        prompt = f"""You are an AI assistant helping a call center agent.

Client: {client['name']}
Tone: {client['tone']}
Agent Experience: {agent.get('experience', 'General')}

Context Data:
{context_str}

Recent Transcript:
{recent_transcript}

Agent Question: {query}

Provide helpful, actionable guidance."""
    else:
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
    except Exception as e:
        return f"⚠️ AI generation failed: {e}"

def generate_crm_notes():
    """Three-Box Closer - Generate final CRM notes"""
    if not model:
        return "⚠️ AI unavailable (API key missing)"
    
    if not NOTE_PROMPT_TEMPLATE:
         # Hard-stop if mandatory template is missing
         return "⚠️ Error: NOTE_PROMPT_TEMPLATE file (config/prompts/note_generator.md) is missing or failed to load."

    client = CLIENTS[st.session_state.current_client_id]
    
    # Read full transcript
    lines = []
    if os.path.exists(TRANSCRIPT_FILE):
        try:
            with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
        except:
            pass
    
    transcript_text = "".join(lines[-30:])  # Last 30 lines
    context_str = json.dumps(st.session_state.extracted_context, indent=2)
    
    # *** DERIVE NECESSARY VARIABLES FOR THE MANDATORY TEMPLATE ***
    # The template (note_generator.md) mandates an emotional_state variable.
    # We derive this from the live sentiment tracking.
    current_sentiment_label = st.session_state.sentiment["label"]

    note_template = client.get("note_template", "Summary: {transcript}")
    
    # We now format the template directly, providing all required keys.
    try:
        prompt = NOTE_PROMPT_TEMPLATE.format(
            note_template=note_template,
            transcript=transcript_text,
            agent_notes=st.session_state.agent_notes,
            customer_summary=st.session_state.customer_summary,
            context_data=context_str,
            # Add the derived emotional state for the mandatory output structure
            emotional_state=current_sentiment_label 
        )
    except KeyError as e:
        # Catch case where template requires a key not provided above
        return f"⚠️ Note template requires missing key: {e}. Check note_generator.md structure."


    try:
        res = model.generate_content(prompt)
        return res.text
    except Exception as e:
        return f"⚠️ Note generation failed: {e}"

# ==========================================
# 4b. SALES COMMAND BAR HELPERS
# ==========================================

def get_sales_presets(client_id):
    """
    Return normalized sales presets for a client, plus agent favorites as a category.
    Expected client config structure (optional):

    "sales_presets": {
        "Discovery": [
            {"label": "Open the conversation", "prompt": "..."},
            "Ask what success looks like",  # also allowed; becomes label+prompt
        ],
        "Objections": [
            {"label": "Price pushback", "prompt": "..."}
        ]
    }
    """
    client = CLIENTS.get(client_id, {})
    raw = client.get("sales_presets", {})

    presets = {}

    if isinstance(raw, dict):
        for category, items in raw.items():
            normalized = []
            if isinstance(items, list):
                for item in items:
                    if isinstance(item, dict):
                        prompt_text = item.get("prompt") or item.get("text") or ""
                        if not prompt_text:
                            continue
                        label = (
                            item.get("label")
                            or item.get("name")
                            or item.get("title")
                            or prompt_text[:40] + ("..." if len(prompt_text) > 40 else "")
                        )
                    else:
                        prompt_text = str(item)
                        if not prompt_text:
                            continue
                        label = prompt_text[:40] + ("..." if len(prompt_text) > 40 else "")

                    normalized.append({"label": label, "prompt": prompt_text})
            if normalized:
                presets[category] = normalized

    # Fallback defaults if client didn't define any
    if not presets:
        presets = {
            "Discovery": [
                {
                    "label": "Find the real goal",
                    "prompt": "Help me ask an open question that uncovers the customer's true goal in this call.",
                },
                {
                    "label": "Budget + timeline",
                    "prompt": "Help me ask politely about budget and timeline based on this conversation.",
                },
            ],
            "Objections": [
                {
                    "label": "Handle price pushback",
                    "prompt": "Give me a short, empathetic way to respond to a price objection while protecting value.",
                },
                {
                    "label": "Handle 'need to think'",
                    "prompt": "Help me respond when the customer says they need to think about it, without being pushy.",
                },
            ],
            "Closing": [
                {
                    "label": "Soft close",
                    "prompt": "Suggest a low-pressure next step I can propose right now.",
                },
                {
                    "label": "Direct close",
                    "prompt": "Give me a direct close sentence tailored to this situation.",
                },
            ],
        }

    # Add agent's personal favorites as a separate category if any exist
    if st.session_state.sales_favorites:
        presets["⭐ My Favorites"] = list(st.session_state.sales_favorites)

    return presets

POSITIVE_WORDS = [
    "great", "good", "happy", "excellent", "love", "like", "thank", "thanks",
    "awesome", "perfect", "works", "resolved", "appreciate"
]

NEGATIVE_WORDS = [
    "bad", "angry", "upset", "frustrated", "hate", "terrible", "awful",
    "problem", "issue", "doesn't work", "doesnt work", "cancel", "refund"
]

def analyze_sentiment_from_lines(lines):
    """
    Lightweight keyword-based sentiment; good enough for a live 'mood light'.
    Looks at the last ~30 lines of transcript.
    """
    if not lines:
        return {"label": "Neutral", "score": 0}

    text = " ".join(lines[-30:]).lower()

    pos_score = 0
    for w in POSITIVE_WORDS:
        pos_score += text.count(w)

    neg_score = 0
    for w in NEGATIVE_WORDS:
        neg_score += text.count(w)

    score = pos_score - neg_score

    if score > 3:
        label = "Positive"
    elif score < -3:
        label = "Negative"
    else:
        label = "Neutral"

    return {"label": label, "score": score}


# ==========================================
# 5. UI FRAGMENTS (THE TWO HEARTBEATS)
# ==========================================

@st.fragment(run_every=1)
def render_knowledge_panel():
    """HEARTBEAT 1: Knowledge Stream Display"""
    if st.session_state.accumulated_links:
        for item in st.session_state.accumulated_links:
            badge = "📌" if item.get('count') == "Manual" else "🔥"
            
            # Read preview
            preview = ""
            try:
                with open(item['path'], 'r', encoding='utf-8') as f:
                    preview = f.read(200).strip()
            except:
                preview = "Preview unavailable"
            
            with st.expander(f"{badge} {item['name']}", expanded=False):
                st.caption(f"Relevance Score: {item['score']}")
                st.markdown(preview + "...")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("📋 Copy", key=f"copy_{item['id']}", use_container_width=True):
                        if CLIPBOARD_AVAILABLE:
                            try:
                                with open(item['path'], 'r', encoding='utf-8') as f:
                                    pyperclip.copy(f.read())
                                st.toast("✓ Copied to clipboard!")
                            except:
                                st.error("Copy failed")
                        else:
                            st.error("Pyperclip not available")
                
                with col2:
                    if st.button("🗑️", key=f"remove_{item['id']}", use_container_width=True):
                        st.session_state.accumulated_links.remove(item)
                        st.rerun()
    else:
        st.info("⏳ Waiting for triggers...")

@st.fragment(run_every=1)
def render_transcript_watcher():
    """HEARTBEAT 2: Transcript Monitor & Auto-KB Trigger"""
    
    # Read transcript file
    lines = []
    try:
        if os.path.exists(TRANSCRIPT_FILE):
            with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
        else:
            st.warning("⏳ Waiting for live transcription...")
            return
    except Exception as e:
        st.error(f"❌ Error reading transcript: {e}")
        return
    
    # Process new lines for KB search (Same logic as before)
    if len(lines) > st.session_state.last_processed_line:
        new_text_block = " ".join(lines[st.session_state.last_processed_line:])
        
        # Auto-trigger KB search
        hits = search_kb(st.session_state.current_client_id, new_text_block)
        
        # Update accumulated links 
        current_ids = [item['id'] for item in st.session_state.accumulated_links]
        for hit in hits:
            if hit['id'] not in current_ids:
                st.session_state.accumulated_links.insert(0, hit)
            else:
                for existing in st.session_state.accumulated_links:
                    if existing['id'] == hit['id']:
                        st.session_state.accumulated_links.remove(existing)
                        st.session_state.accumulated_links.insert(0, existing)
                        break
        
        # Update index
        st.session_state.last_processed_line = len(lines)

    # Update live sentiment snapshot
    st.session_state.sentiment = analyze_sentiment_from_lines(lines)

    # --- UPDATED DISPLAY LOGIC ---
    if lines:
        # We use a container with a defined height to mimic the text_area scroll box
        with st.container(height=200, border=True):
            # Formats it like code/log (monospaced) but allows it to refresh instantly
            st.text("".join(lines[-20:]))

        # Sentiment indicator under the log
        s = st.session_state.sentiment
        emoji = {"Positive": "🟢", "Neutral": "🟡", "Negative": "🔴"}.get(s["label"], "🟡")
        st.caption(f"{emoji} Live Sentiment: **{s['label']}** (score {s['score']})")
    else:
        st.caption("No transcript data yet...")

# ==========================================
# 6. DEMO MODE INJECTION
# ==========================================

def inject_demo_transcript():
    """Simulate a live call for demo purposes"""
    demo_lines = [
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Customer: Hi, I need help with my account.\n",
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Agent: Sure! What's your account number?\n",
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Customer: It's 12345. I want to upgrade my plan.\n",
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Agent: Great! Let me look that up for you.\n",
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Customer: Also, what's your refund policy?\n",
        f"[{datetime.datetime.now().strftime('%H:%M:%S')}] Agent: I can help with that too.\n",
    ]
    
    try:
        with open(TRANSCRIPT_FILE, "a", encoding="utf-8") as f:
            for line in demo_lines:
                f.write(line)
                f.flush()
                time.sleep(0.3)
        return True
    except Exception as e:
        st.error(f"Demo injection failed: {e}")
        return False



# ==========================================
# 7. MAIN LAYOUT
# ==========================================

# --- SIDEBAR: ADMIN PANEL ---
with st.sidebar:
    st.header("⚙️ Admin Panel")
    
    # Client Switcher
    c_names = {k: v['name'] for k, v in CLIENTS.items()}
    sel_c = st.selectbox("Active Client", options=list(c_names.keys()), 
                         format_func=lambda x: c_names[x])
    if sel_c != st.session_state.current_client_id:
        st.session_state.current_client_id = sel_c
        st.session_state.extracted_context = {}
        st.session_state.accumulated_links = []
        st.session_state.last_processed_line = 0
        st.rerun()
    
    # Agent Switcher
    a_names = {k: v['name'] for k, v in AGENTS.items()}
    sel_a = st.selectbox("Logged in Agent", options=list(a_names.keys()), 
                         format_func=lambda x: a_names[x])
    if sel_a != st.session_state.current_agent_id:
        st.session_state.current_agent_id = sel_a
        st.rerun()
    
    st.divider()
    
    # Tools Section
    st.markdown("#### 🔧 Tools")
    
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🧲 Gimme That", type="primary", use_container_width=True, 
                    disabled=not CLIPBOARD_AVAILABLE):
            data = parse_clipboard_context(st.session_state.current_client_id)
            st.session_state.extracted_context = data
            if "Error" not in data and "Info" not in data:
                st.toast("✓ Context Loaded!")
            else:
                st.toast(str(data.get("Error", data.get("Info"))))
    
    with col2:
        if st.button("🗑️ Clear", use_container_width=True):
            st.session_state.extracted_context = {}
            st.session_state.accumulated_links = []
            st.session_state.chat_history = []
            st.session_state.last_processed_line = 0
            st.session_state.agent_notes = ""
            st.session_state.customer_summary = ""
            st.session_state.generated_crm_note = ""
            st.toast("✓ Session cleared!")
            st.rerun()
    
    st.divider()
    
    # Manual KB Search
    st.markdown("#### 🔎 Manual Search")
    kb_q = st.text_input("Query", key="kb_manual_input", placeholder="Search knowledge base...")
    if st.button("Search", use_container_width=True):
        if kb_q:
            man_hits = search_kb(st.session_state.current_client_id, kb_q)
            for h in man_hits:
                h['count'] = 'Manual'
                st.session_state.accumulated_links.insert(0, h)
            st.rerun()
    
    st.divider()
    
    # Demo Mode
    st.markdown("#### 🎭 Demo Mode")
    if st.button("▶️ Simulate Call", use_container_width=True):
        with st.spinner("Injecting demo transcript..."):
            if inject_demo_transcript():
                st.session_state.demo_mode = True
                st.toast("✓ Demo transcript injected!")
                time.sleep(1)
                st.rerun()

# --- WORKSPACE ---
current_client = CLIENTS[st.session_state.current_client_id]
current_agent = AGENTS[st.session_state.current_agent_id]

st.title(f"🌀 {current_client['name']}")

# Show Extracted Context
if st.session_state.extracted_context:
    with st.expander("📌 Active Session Context", expanded=True):
        st.json(st.session_state.extracted_context)

# Main Columns
col_kb, col_chat, col_xray, col_pilot = st.columns([1.2, 1.8, 1.5, 1.5])

# ==========================================
# LEFT: KNOWLEDGE STREAM
# ==========================================
with col_kb:
    st.subheader("📚 Knowledge Stream")
    render_knowledge_panel()

# ==========================================
# MIDDLE: TRANSCRIPT & CHAT
# ==========================================
with col_chat:
    st.subheader("📝 Live Log")
    render_transcript_watcher()
    
    st.divider()
    
    st.subheader("💬 AI Co-Pilot")

    # ==========================
    # SALES COMMAND BAR
    # ==========================
    sales_presets = get_sales_presets(st.session_state.current_client_id)

    with st.expander("🎯 Sales Command Bar (one-click prompts)", expanded=True):
        st.caption("Pick a category, then click a button to get a ready-to-use response.")

        categories = list(sales_presets.keys())
        if categories:
            col_cat, col_dummy = st.columns([2, 1])
            with col_cat:
                selected_cat = st.selectbox(
                    "Category",
                    options=categories,
                    index=0,
                    key="sales_command_category"
                )

            # Render buttons for the selected category
            entries = sales_presets.get(selected_cat, [])
            if entries:
                # 3 columns of buttons, cycling
                button_cols = st.columns(3)
                for i, entry in enumerate(entries):
                    col = button_cols[i % 3]
                    with col:
                        if st.button(entry["label"], key=f"sales_btn_{selected_cat}_{i}", use_container_width=True):
                            # When clicked: push prompt into chat history and get guidance
                            prompt_text = entry["prompt"]
                            st.session_state.chat_history.append({"role": "user", "content": prompt_text})

                            # Read fresh transcript
                            lines = []
                            if os.path.exists(TRANSCRIPT_FILE):
                                try:
                                    with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
                                        lines = f.readlines()
                                except:
                                    pass

                            with st.spinner("Generating sales guidance..."):
                                resp = generate_guidance(prompt_text, lines)

                            st.session_state.chat_history.append({"role": "assistant", "content": resp})
                            st.rerun()
            else:
                st.caption("_No entries for this category_")

        # --- Agent Personal Favorites creator ---
        st.markdown("---")
        st.caption("⭐ Save a personal favorite prompt")

        fav_label = st.text_input("Favorite label", key="fav_label_input", placeholder="e.g. Handle polite price objection")
        fav_prompt = st.text_area("Favorite prompt behavior", key="fav_prompt_input",
                                  placeholder="Describe what you want the AI to do for you on this button.")
        col_save, col_clear = st.columns(2)
        with col_save:
            if st.button("💾 Save to My Favorites", use_container_width=True):
                if fav_label and fav_prompt:
                    st.session_state.sales_favorites.append({
                        "label": fav_label,
                        "prompt": fav_prompt
                    })
                    st.toast("⭐ Favorite saved into '⭐ My Favorites'")
                    st.rerun()
                else:
                    st.error("Please enter both a label and a prompt description.")
        with col_clear:
            if st.button("🗑️ Clear all My Favorites", use_container_width=True):
                st.session_state.sales_favorites = []
                st.toast("⭐ Favorites cleared.")
                st.rerun()

    # ==========================
    # Chat History (below the bar)
    # ==========================
    chat_box = st.container(height=280)
    with chat_box:
        for msg in st.session_state.chat_history:
            with st.chat_message(msg['role']):
                st.markdown(msg['content'])
    
    # Chat Input
    if prompt := st.chat_input("Ask for guidance..."):
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        
        # Read fresh transcript
        lines = []
        if os.path.exists(TRANSCRIPT_FILE):
            try:
                with open(TRANSCRIPT_FILE, "r", encoding="utf-8") as f:
                    lines = f.readlines()
            except:
                pass
        
        with st.spinner("Analyzing..."):
            resp = generate_guidance(prompt, lines)
        
        st.session_state.chat_history.append({"role": "assistant", "content": resp})
        st.rerun()

# ==========================================
# CENTER-RIGHT: X-RAY TRANSPARENCY PANEL
# ==========================================
with col_xray:
    st.subheader("🔬 X-Ray: AI Context")
    
    with st.expander("📊 Coherence Layers", expanded=True):
        st.caption("**Layer 1: Agent Profile**")
        st.json({
            "name": current_agent.get("name", "Unknown"),
            "experience": current_agent.get("experience", "General"),
            "strengths": current_agent.get("strengths", [])
        })
        
        st.caption("**Layer 2: Client Context**")
        st.json({
            "tone": current_client['tone'],
            "compliance_items": len(current_client.get('compliance_checklist', [])),
            "has_upsell": bool(current_client.get('upsell_strategy'))
        })
        
        st.caption("**Layer 3: Live Situation**")
        live_block = {
            "context": st.session_state.extracted_context if st.session_state.extracted_context else None,
            "sentiment": st.session_state.sentiment
        }
        st.json(live_block)

        st.caption("**Layer 4: Knowledge Base**")
        st.metric("Active Articles", len(st.session_state.accumulated_links))
    
    with st.expander("🧠 Pirouette Coherence", expanded=False):
        st.markdown("""
**K_τ (Temporal Coherence):** Agent maintains consistent brand voice across conversation

**V_Γ (Temporal Pressure):** Live call urgency + compliance requirements + customer needs

**Dark Residue Minimization:** AI surfaces exactly the right knowledge and guidance at the right time, eliminating wasted agent effort and cognitive load.

**Coherence Optimization:** The system maximizes (K_τ - V_Γ) by reducing friction in the agent's workflow.
        """)

# ==========================================
# RIGHT: PILOT DOCUMENT & CLOSER
# ==========================================
with col_pilot:
    st.subheader("📋 Pilot Document")
    
    # Quick Tools
    tools = current_client.get("tools", {})
    if tools:
        st.caption("**Quick Links**")
        cols = st.columns(len(tools))
        for i, (name, url) in enumerate(tools.items()):
            cols[i].markdown(f"[{name}]({url})", unsafe_allow_html=True)
    
    # Compliance Checklist
    with st.expander("✅ Compliance Checklist", expanded=True):
        checklist = current_client.get("compliance_checklist", [])
        if checklist:
            # Initialize compliance state for this client
            if st.session_state.current_client_id not in st.session_state.compliance_state:
                st.session_state.compliance_state[st.session_state.current_client_id] = {}
            
            for item in checklist:
                checked = st.session_state.compliance_state[st.session_state.current_client_id].get(item, False)
                new_val = st.checkbox(item, value=checked, key=f"comp_{item}")
                st.session_state.compliance_state[st.session_state.current_client_id][item] = new_val
        else:
            st.caption("_No compliance items_")
    
    # Upsell Strategy
    upsell = current_client.get("upsell_strategy", {})
    if upsell:
        with st.expander("💰 Upsell Opportunity", expanded=True):
            st.info(f"**Target:** {upsell.get('Target', 'N/A')}\n\n**Pitch:** \"{upsell.get('Pitch', 'N/A')}\"")
    
    # SOPs
    with st.expander("📜 Standard Procedures", expanded=False):
        sops = current_client.get("sops", {})
        if sops:
            st.json(sops)
        else:
            st.caption("_No SOPs defined_")
    
    st.divider()
    
    # THREE-BOX CLOSER
    st.subheader("📝 Call Closer")
    
    st.text_area("Agent Notes", value=st.session_state.agent_notes, height=100,
                key="agent_notes_input", placeholder="Quick notes during call...",
                on_change=lambda: setattr(st.session_state, 'agent_notes', 
                                         st.session_state.agent_notes_input))
    
    st.text_area("Customer Summary", value=st.session_state.customer_summary, height=100,
                key="customer_summary_input", placeholder="Key customer points...",
                on_change=lambda: setattr(st.session_state, 'customer_summary', 
                                         st.session_state.customer_summary_input))
    
    if st.button("🎯 Generate CRM Notes", type="primary", use_container_width=True):
        with st.spinner("Synthesizing final notes..."):
            note = generate_crm_notes()
            st.session_state.generated_crm_note = note
    
    if st.session_state.generated_crm_note:
        st.text_area("📋 Final CRM Entry", value=st.session_state.generated_crm_note, 
                    height=150, key="crm_output")
        if st.button("📋 Copy to Clipboard", use_container_width=True):
            if CLIPBOARD_AVAILABLE:
                try:
                    pyperclip.copy(st.session_state.generated_crm_note)
                    st.toast("✓ Copied to clipboard!")
                except:
                    st.error("Copy failed")
            else:
                st.error("Pyperclip not available")

# ==========================================
# FOOTER: METRICS DASHBOARD
# ==========================================
st.divider()
st.subheader("📈 Session Metrics")

metric_cols = st.columns(6)

with metric_cols[0]:
    st.metric("KB Articles", len(st.session_state.accumulated_links))

with metric_cols[1]:
    st.metric("AI Queries", len([m for m in st.session_state.chat_history if m['role'] == 'user']))

with metric_cols[2]:
    st.metric("Context Fields", len(st.session_state.extracted_context))

with metric_cols[3]:
    # Calculate compliance completion
    if st.session_state.current_client_id in st.session_state.compliance_state:
        total = len(current_client.get('compliance_checklist', []))
        checked = sum(st.session_state.compliance_state[st.session_state.current_client_id].values())
        pct = int((checked / total * 100)) if total > 0 else 0
        st.metric("Compliance", f"{pct}%")
    else:
        st.metric("Compliance", "0%")

with metric_cols[4]:
    # Coherence score (calculated)
    coherence = min(
        100,
        (len(st.session_state.accumulated_links) * 8)
        + (len(st.session_state.chat_history) * 4)
        + (len(st.session_state.extracted_context) * 6)
    )
    delta = "+12%" if coherence > 50 else None
    st.metric("Coherence", f"{coherence}%", delta=delta)

with metric_cols[5]:
    s = st.session_state.sentiment
    emoji = {"Positive": "🟢", "Neutral": "🟡", "Negative": "🔴"}.get(s["label"], "🟡")
    st.metric("Sentiment", f"{emoji} {s['label']}", s["score"])
