# 🚀 QUICK START GUIDE
## Universal Agent Assistant - Executive Demo

### ⚡ 5-Minute Setup

#### Step 1: Install Requirements
```bash
pip install -r requirements.txt
```

#### Step 2: Set API Key
Get your free Gemini API key: https://aistudio.google.com/app/apikey

**Windows PowerShell:**
```powershell
$env:GOOG_API_KEY="your_api_key_here"
```

**Mac/Linux Terminal:**
```bash
export GOOG_API_KEY="your_api_key_here"
```

#### Step 3: Run Demo
```bash
python demo.py
```

That's it! The app will open in your browser automatically.

---

## 🎭 Demo Scenarios for Your Presentation

### Scenario 1: Show the Link Fix (404 Issue Resolved)
1. Start the app
2. Click "Search" in sidebar
3. Type: "fraud"
4. **Click any article that appears**
5. ✅ Article opens in new tab (no more 404!)

**Why it works now:**
- Built-in file server on port 8765
- Proper file:// to http:// conversion
- Automatic HTML serving

---

### Scenario 2: Agent Buddy (Context-Aware Chat)
1. In the middle panel "Agent Buddy"
2. Type: "How do I handle a fraud alert for a customer?"
3. Watch the AI generate guidance
4. **Click "Pilot Document X-Ray" (right panel)**
5. See all 4 layers of context assembly

**What to highlight:**
- Agent profile influences tone (new hire vs senior)
- Client compliance rules integrated
- Live conversation context
- Available SOPs referenced

---

### Scenario 3: Compare Client Personalities

**Test A - NeoBank (Banking):**
- Select "NeoBank" client
- Ask: "Customer can't remember their password"
- Notice: Professional, security-focused tone

**Test B - GlowCosmetics (Retail):**
- Switch to "GlowCosmetics" client
- Ask: "Customer wants to return lipstick"
- Notice: Bubbly, emoji-rich, "bestie" vibe

**The Point:** Same agent, same AI, different brand voice - automatically adapted.

---

### Scenario 4: X-Ray Transparency

After any Agent Buddy question, show the right panel:

**Layer 1: Agent Profile**
```json
{
  "name": "Alex Chen",
  "role": "L1 Associate",
  "focus_area": "Confidence & Tool Usage"
}
```

**Layer 2: Client Context**
```json
{
  "name": "NeoBank",
  "tone": "Professional, Empathetic, Secure",
  "rules": "NEVER read card numbers aloud"
}
```

**Layer 3: Live Situation**
```json
{
  "transcript": "customer reporting fraud",
  "agent_question": "How do I handle this?"
}
```

**Layer 4: Available SOPs**
```json
{
  "Fraud Alert": "1. Freeze card immediately..."
}
```

**Then show:** How all 4 layers combine into the AI response.

---

## 🎤 Optional: Live Transcription Demo

### If You Have Virtual Audio Cable Installed:

1. Click "🔴 Start Listening" in sidebar
2. Status changes to "🟢 ACTIVE"
3. Speak or play audio: "password reset"
4. Watch articles automatically populate in Knowledge Stream
5. Articles get 🔥 indicators when mentioned multiple times

### If Not Installed (Still Impressive):
Just use Manual Search - executives will understand the concept.

---

## 💡 Key Talking Points

### Problem This Solves:
1. **Inconsistent Agent Performance**
   - New hires struggle with complex scenarios
   - Knowledge buried in PDFs and wikis
   - Agents forget compliance steps under pressure

2. **Rigid Training Systems**
   - One-size-fits-all scripts don't work
   - Can't adapt to different client brands
   - No real-time coaching during live calls

### This Solution:
1. **Dynamic Context Assembly**
   - Agent profile + Client rules + Live situation = Perfect guidance
   - Adapts to experience level automatically
   - Brand voice maintained consistently

2. **Transparent AI**
   - X-Ray shows exactly how decisions are made
   - No "black box" mystery
   - Auditable for compliance

3. **Knowledge Automation**
   - Relevant articles surface automatically
   - No manual searching during calls
   - Frequency tracking shows trending issues

---

## 🔐 Security & Scalability Discussion Points

### Current (Demo) State:
- Localhost only
- No auth required
- Single-machine deployment

### Production Path (Your Pitch):
1. **Microsoft Integration**
   - Knowledge Base = OneDrive/SharePoint folders
   - Permissions managed via M365
   - "Point at Microsoft if something goes wrong" 😉

2. **Enterprise Auth**
   - Azure AD SSO
   - Role-based access
   - Audit logging

3. **Scalability**
   - Deploy to agent PCs via Group Policy
   - Or central server with thin clients
   - Load balancer for high-volume centers

---

## 📊 ROI Metrics to Discuss

### Measurable Improvements:
- **Reduced Average Handle Time (AHT)** - Agents find answers faster
- **Improved CSAT Scores** - Consistent brand voice, accurate info
- **Faster Onboarding** - New hires productive in days, not weeks
- **Compliance Adherence** - Critical steps baked into AI guidance
- **Knowledge Gap Identification** - Track search patterns to find missing KB content

### Cost Savings:
- Fewer escalations to supervisors
- Reduced training time
- Lower turnover (agents feel supported)
- Fewer compliance violations

---

## ⚠️ Common Questions You'll Get

**Q: "Can it work with our existing CRM?"**
A: Yes - the system is modular. We can integrate with Salesforce, Zendesk, etc. The Knowledge Base just needs file access.

**Q: "What about call recording compliance?"**
A: The transcription is local-only, never stored by default. In production, you'd integrate with your existing compliant recording system.

**Q: "Can it handle multiple languages?"**
A: The AI (Gemini) supports 100+ languages. Knowledge base can be translated or maintained in multiple languages per client.

**Q: "How do we keep the knowledge base updated?"**
A: That's the beauty of the file-based system. Your knowledge managers just edit markdown files in OneDrive. Changes go live immediately.

**Q: "What if the AI gives wrong information?"**
A: The X-Ray transparency lets supervisors audit responses. Plus, the KB is the source of truth - AI assembles from verified content.

---

## 🎯 Closing Your Pitch

### The Vision:
"Imagine every agent having a senior expert sitting next to them, whispering perfect guidance for every scenario, adapting to their skill level and the client's brand voice - all in real-time."

### The Ask:
- Pilot program with 10-20 agents
- 90-day trial period
- Metrics: AHT, CSAT, escalation rates
- Budget: [Your cost estimate]

### Next Steps:
1. They approve concept → Schedule detailed technical review
2. Get access to sample KB content from one client
3. Customize agent profiles for their team
4. Set up secure pilot environment
5. Train supervisors on X-Ray monitoring
6. Launch with metrics dashboard

---

## 📞 Support During Demo

If something breaks during the presentation:

### Knowledge base articles not loading?
```bash
# Quick fix - restart the app
# The file server auto-restarts
```

### AI not responding?
```bash
# Check API key
echo $GOOG_API_KEY
```

### Articles showing but links 404?
- Wait 5 seconds for file server to fully start
- Check browser console for actual port
- Refresh the page

---

## 🌟 Best Practices for the Demo

1. **Pre-load a scenario** before opening the app (use demo.py)
2. **Have backup screenshots** in case of technical issues
3. **Practice the X-Ray explanation** - it's the most impressive part
4. **Show the knowledge base files** in a file explorer - prove it's just markdown
5. **Let them type questions** - interactive is more convincing

---

**Good luck with your pitch! 🚀**

*Remember: They're buying the vision of augmented intelligence, not just a chatbot. Focus on the transparency, adaptability, and real business outcomes.*
