# 🌐 Universal Agent Assistant

**An AI-powered real-time agent assistance system combining live transcription, dynamic knowledge retrieval, and context-aware pilot document generation.**

---

## 🎯 What This Does

The Universal Agent Assistant is designed for call center environments to provide agents with:

1. **Live Transcription** - Captures customer conversations in real-time
2. **Dynamic Knowledge Retrieval** - Automatically surfaces relevant KB articles based on conversation content
3. **Agent Buddy Chat** - Conversational AI assistant for quick questions and context
4. **Pilot Document Generation** - AI-generated guidance considering:
   - Agent profile & performance focus areas
   - Client-specific tone and compliance rules
   - Live conversation context
   - Available SOPs and procedures
5. **X-Ray Transparency** - Shows exactly how the AI assembles its guidance

---

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key ([Get one here](https://aistudio.google.com/app/apikey))
- (Optional) Virtual Audio Cable for live transcription

### Installation

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Set up your API key:**

**Windows (PowerShell):**
```powershell
$env:GOOG_API_KEY="your_api_key_here"
```

**Mac/Linux (Bash):**
```bash
export GOOG_API_KEY="your_api_key_here"
```

3. **Run the application:**
```bash
streamlit run universal_agent_app.py
```

The app will automatically:
- Start a knowledge base file server on port 8765
- Open in your default browser at http://localhost:8501

---

## 📁 Project Structure

```
universal-agent/
├── universal_agent_app.py      # Main unified application
├── requirements.txt            # Python dependencies
├── Knowledge_Base/            # Article storage
│   ├── NeoBank/              # Client-specific KB
│   │   ├── Fraud_Alert_Protocol.md
│   │   ├── Fraud_Alert_Protocol.html
│   │   ├── Password_Reset_Guide.md
│   │   └── Password_Reset_Guide.html
│   └── GlowCosmetics/
│       ├── Order_Status_Tracking.md
│       ├── Order_Status_Tracking.html
│       ├── Returns_Exchange_Policy.md
│       └── Returns_Exchange_Policy.html
└── live_state.json           # (Auto-generated) State file
```

---

## 🎤 Setting Up Live Transcription

For the system to capture audio from calls:

### Option 1: Virtual Audio Cable (Recommended for Testing)

1. **Install Virtual Audio Cable:**
   - Windows: [VB-Audio Virtual Cable](https://vb-audio.com/Cable/)
   - Mac: [BlackHole](https://github.com/ExistentialAudio/BlackHole)

2. **Configure your audio routing:**
   - Set your call system to output to "CABLE Input"
   - The app will automatically detect "CABLE Output"

3. **Enable in the app:**
   - Click "🔴 Start Listening" in the sidebar
   - Speak or play audio through the virtual cable
   - Watch as knowledge articles automatically appear!

### Option 2: Direct Microphone (For Testing)

- If no virtual cable is detected, the system falls back to your default microphone
- Useful for demo purposes or testing queries verbally

---

## 🧠 How It Works

### The Pilot Document Assembly Process

The system builds AI guidance using **4 contextual layers**:

```
┌─────────────────────────────────────┐
│  Layer 1: Agent Profile            │
│  - Name, role, tenure               │
│  - Performance focus areas          │
│  - Manager and KPIs                 │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  Layer 2: Client Context           │
│  - Industry and tone guidelines     │
│  - Compliance rules                 │
│  - Brand voice directives           │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  Layer 3: Live Situation           │
│  - Current transcript               │
│  - Agent's specific question        │
│  - Conversation context             │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│  Layer 4: Available SOPs           │
│  - Relevant procedures              │
│  - Step-by-step protocols           │
│  - Compliance checklists            │
└─────────────────────────────────────┘
           ↓
┌─────────────────────────────────────┐
│    🤖 Gemini AI Generation         │
│  → Script (exact phrasing)          │
│  → Verify (data to confirm)         │
│  → Next Steps (guidance)            │
│  → Upsell (opportunities)           │
└─────────────────────────────────────┘
```

### Knowledge Base Search Logic

1. **Trigger**: Live transcript or manual search
2. **Keyword Extraction**: Filters stop words, keeps substantive terms
3. **Scoring Algorithm**:
   - Content match: +1 point
   - Filename match: +3 points (higher relevance)
4. **Ranking**: Top 5 results displayed
5. **Frequency Tracking**: Articles triggered multiple times show 🔥 indicator

---

## 📚 Adding Your Own Knowledge Base

### Step 1: Create Client Folder
```bash
mkdir -p Knowledge_Base/YourClient
```

### Step 2: Add Markdown Files
Create articles in simple markdown format:

```markdown
# Article Title

## Overview
Describe the process or policy

## Key Steps
1. First step
2. Second step
3. Third step

## Important Notes
⚠️ Critical compliance information

---
*Last Updated: 2024-11-24*
```

### Step 3: Convert to HTML (Optional but Recommended)
```python
# Run this from your terminal:
python3 << 'EOF'
import markdown
import os

md_file = "Knowledge_Base/YourClient/Article.md"
html_file = md_file.replace('.md', '.html')

with open(md_file, 'r') as f:
    md_content = f.read()

html_content = markdown.markdown(md_content, extensions=['extra'])

# Add styling and save
with open(html_file, 'w') as f:
    f.write(f"<html><body>{html_content}</body></html>")
EOF
```

### Step 4: Register Client in Config

Edit `universal_agent_app.py` and add to `CLIENT_CONFIG`:

```python
"YourClient": {
    "industry": "Your Industry",
    "tone": "Your Brand Voice",
    "directive": "Your Strategy Guidance",
    "kb_folder": "YourClient",
    "key_rules": "Critical compliance points",
    "sops": {
        "Process Name": "Step-by-step procedure",
        # Add more SOPs
    }
}
```

---

## 🎨 Customization

### Adding Agent Profiles

Edit `AGENT_DATABASE` in `universal_agent_app.py`:

```python
"Agent Name": {
    "role": "L1 Associate",
    "manager": "Manager Name",
    "tenure": "6 Months",
    "latest_review": "Performance notes here",
    "focus_area": "What they're working on improving",
    "kpis": {"AHT": "Low", "CSAT": "High"}
}
```

### Modifying AI Behavior

The prompt template in `generate_pilot_doc_with_components()` can be adjusted to:
- Change output format
- Add/remove sections
- Adjust tone and formality
- Include additional context

---

## 🔒 Security Considerations

### Current Implementation (Demo/Internal Use)
- Knowledge base served via localhost only
- No authentication required
- Files accessible only on local network

### Production Recommendations

1. **Authentication Layer:**
   - Implement SSO integration
   - Role-based access control
   - Session management

2. **Secure File Serving:**
   - Use HTTPS with proper certificates
   - Implement access logging
   - Add rate limiting

3. **Data Protection:**
   - Encrypt sensitive KB content
   - Implement audit trails
   - Regular access reviews

4. **Integration with Microsoft/Cloud:**
   - Mount OneDrive/SharePoint as KB source
   - Use Azure AD for authentication
   - Leverage existing enterprise security

**Example OneDrive Integration:**
```python
# Point KB_DIR to a OneDrive sync folder
KB_DIR = "C:/Users/Agent/OneDrive/Knowledge_Base"
# Permissions managed through Microsoft 365
```

---

## 🐛 Troubleshooting

### "No module named 'streamlit'"
```bash
pip install -r requirements.txt
```

### "API Key missing" error
Make sure you've set the environment variable:
```bash
echo $GOOG_API_KEY  # Should show your key
```

### 404 errors when clicking knowledge links
- Check that the file server started (look for "📁 Knowledge Base server running" in console)
- Verify HTML files exist: `ls Knowledge_Base/*/*.html`
- Try restarting the application

### Speech recognition not working
- Install PyAudio: `pip install PyAudio`
- On Mac: `brew install portaudio && pip install PyAudio`
- On Linux: `sudo apt-get install portaudio19-dev python3-pyaudio`

### Knowledge articles not appearing
- Check file names match search terms
- Verify client folder exists in Knowledge_Base/
- Try manual search to test KB connectivity

---

## 🎯 Demo Scenarios for Executives

### Scenario 1: Fraud Alert (NeoBank)
1. Select "NeoBank" as client
2. Select agent with "Confidence" focus area
3. In Agent Buddy, type: "Customer is reporting fraud charges"
4. Observe:
   - Fraud Alert Protocol appears in Knowledge Stream
   - X-Ray shows how agent profile influences guidance
   - AI provides script matching agent's skill level

### Scenario 2: Return Request (GlowCosmetics)
1. Switch to "GlowCosmetics" client
2. Ask: "Customer wants to return opened lipstick"
3. Observe:
   - Returns policy automatically surfaces
   - AI matches the "bestie" brand voice
   - Provides upsell alternatives before processing return

### Scenario 3: Live Transcription (If Available)
1. Enable "Start Listening"
2. Say phrases like "password reset" or "order status"
3. Watch knowledge base articles appear in real-time
4. See frequency indicators (🔥) for repeated topics

---

## 📈 Future Enhancements

- [ ] Multi-language support for international clients
- [ ] Integration with CRM systems (Salesforce, Zendesk)
- [ ] Advanced analytics dashboard
- [ ] Agent performance correlation with pilot doc usage
- [ ] Voice synthesis for suggested scripts
- [ ] Automated SOP generation from call recordings
- [ ] Collaborative knowledge base editing

---

## 🤝 Contributing

This is a demonstration system built for executive review. For production deployment:

1. Conduct security audit
2. Implement enterprise authentication
3. Set up monitoring and logging
4. Establish backup procedures
5. Create incident response plan

---

## 📄 License

Proprietary - Internal Use Only

---

## 👤 Contact

**Keaton** - Independent Researcher & Strategic Analyst

*Built as part of the Pirouette Framework initiative demonstrating coherence-based agent assistance.*

---

## 🎉 Quick Demo Command

```bash
# One-command demo setup (after installing requirements)
export GOOG_API_KEY="your_key" && streamlit run universal_agent_app.py
```

**Expected result:** Application opens in browser, knowledge base server starts, ready for testing!

---

*Last Updated: 2024-11-24*
*Version: 1.0.0 - Executive Demo*
