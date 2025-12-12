# 🔧 TROUBLESHOOTING GUIDE
## Universal Agent Assistant

---

## 🐛 Current Issues & Fixes

### Issue 1: "Search doesn't show results"

**Symptoms:**
- Type in search box, click Search
- Nothing appears in Knowledge Stream

**Diagnosis Steps:**

1. **Check console output for debug messages:**
```
🔍 Searching NeoBank for keywords: ['password', 'reset']
  ✓ Found: Password_Reset_Guide.md (score: 6)
  → Returning 1 results
```

2. **Check footer status:**
- Should show: `KB: ✅ X articles`
- If shows `❌ Client folder missing` → Knowledge_Base folder issue

**Fixes:**

**Fix A: Knowledge_Base in wrong location**
```bash
# The app looks for Knowledge_Base in the same directory as universal_agent_app.py
# Make sure structure is:
universal_agent_app.py
Knowledge_Base/
    NeoBank/
        Fraud_Alert_Protocol.md
        Fraud_Alert_Protocol.html
        ...
    GlowCosmetics/
        ...
```

**Fix B: Recreate Knowledge_Base**
```bash
cd [your app directory]
python kb_generator.py
# Select option 2 to convert existing files
```

**Fix C: Test search manually**
```python
# Run this in Python console to test:
from pathlib import Path
import os

KB_DIR = "Knowledge_Base"
client = "NeoBank"
print(f"KB exists: {os.path.exists(KB_DIR)}")
print(f"Client path exists: {os.path.exists(os.path.join(KB_DIR, client))}")
if os.path.exists(os.path.join(KB_DIR, client)):
    files = os.listdir(os.path.join(KB_DIR, client))
    print(f"Files: {files}")
```

---

### Issue 2: "AI Generation Error: 404 models/gemini-1.5-flash not found"

**Cause:** Gemini API changed model names

**✅ FIXED in latest version!**

The model name has been updated to: `gemini-1.5-flash-latest`

**If you still see this error:**

1. **Download updated file:**
   The fixed version is in `/mnt/user-data/outputs/universal_agent_app.py`

2. **Or manually fix** (line ~59):
```python
# OLD (broken):
model = genai.GenerativeModel('gemini-1.5-flash')

# NEW (working):
model = genai.GenerativeModel('gemini-1.5-flash-latest')
```

3. **Alternative models if flash-latest doesn't work:**
```python
# Try these in order:
model = genai.GenerativeModel('gemini-1.5-pro-latest')
model = genai.GenerativeModel('gemini-pro')
model = genai.GenerativeModel('gemini-1.0-pro')
```

4. **Check available models:**
```python
import google.generativeai as genai
genai.configure(api_key="your_key")
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        print(m.name)
```

---

### Issue 3: "Knowledge base links download markdown files instead of opening HTML"

**Cause:** File server serving .md files when .html exists

**✅ FIXED in latest version!**

The search function now prioritizes HTML files:

```python
# New logic in search_kb():
html_file = filename.replace(".md", ".html")
if os.path.exists(os.path.join(client_path, html_file)):
    file_to_serve = html_file  # Serve HTML
else:
    file_to_serve = filename    # Fall back to MD
```

**If still downloading:**

1. **Check HTML files exist:**
```bash
ls Knowledge_Base/NeoBank/
# Should see both .md AND .html files
```

2. **Regenerate HTML files:**
```bash
python kb_generator.py
# Choose option 2: Batch convert existing .md files to HTML
```

3. **Test direct access:**
```
http://localhost:8765/NeoBank/Fraud_Alert_Protocol.html
```
Should open in browser, not download.

---

### Issue 4: "File server not starting"

**Symptoms:**
- Footer shows: `Server: 🔴 Starting...`
- Links give connection errors

**Fixes:**

**Fix A: Port already in use**
```bash
# Find process using port 8765:
# Windows:
netstat -ano | findstr :8765
# Mac/Linux:
lsof -i :8765

# Kill the process or change port in app:
HTTP_PORT = 8766  # Change this line ~57 in universal_agent_app.py
```

**Fix B: Firewall blocking**
```bash
# Windows: Add firewall rule
netsh advfirewall firewall add rule name="Universal Agent KB Server" dir=in action=allow protocol=TCP localport=8765

# Mac: System Preferences > Security & Privacy > Firewall > Firewall Options
# Allow Python
```

**Fix C: Permission issues**
```bash
# Run as administrator/sudo temporarily to test
```

---

### Issue 5: "Live transcription not working"

**Symptoms:**
- Click "Start Listening"
- Status shows ACTIVE but nothing happens

**Diagnosis:**

1. **Check console for errors:**
```
⚠️ No virtual audio cable found. Using default microphone.
```

2. **Test microphone access:**
```python
import speech_recognition as sr
r = sr.Recognizer()
with sr.Microphone() as source:
    print("Say something!")
    audio = r.listen(source)
    print(r.recognize_google(audio))
```

**Fixes:**

**Fix A: Install virtual audio cable**
- Windows: [VB-Audio Virtual Cable](https://vb-audio.com/Cable/)
- Mac: [BlackHole](https://github.com/ExistentialAudio/BlackHole)

**Fix B: PyAudio not installed**
```bash
# Windows:
pip install pipwin
pipwin install pyaudio

# Mac:
brew install portaudio
pip install pyaudio

# Linux:
sudo apt-get install portaudio19-dev python3-pyaudio
pip install pyaudio
```

**Fix C: Microphone permissions**
- Windows: Settings > Privacy > Microphone > Allow apps
- Mac: System Preferences > Security & Privacy > Microphone

---

### Issue 6: "Agent Buddy not generating responses"

**Symptoms:**
- Type question, click send
- Nothing happens or spinner never ends

**Diagnosis:**

1. **Check console:**
```
⚠️ Error: Google API Key missing
```

2. **Check API key:**
```bash
# Windows PowerShell:
echo $env:GOOG_API_KEY

# Mac/Linux:
echo $GOOG_API_KEY

# Should output your key, not empty
```

**Fixes:**

**Fix A: Set API key**
```bash
# Windows PowerShell:
$env:GOOG_API_KEY="your_actual_key_here"

# Windows CMD:
set GOOG_API_KEY=your_actual_key_here

# Mac/Linux:
export GOOG_API_KEY="your_actual_key_here"

# Make permanent (add to ~/.bashrc or ~/.zshrc):
echo 'export GOOG_API_KEY="your_key"' >> ~/.bashrc
```

**Fix B: API key invalid**
- Get new key: https://aistudio.google.com/app/apikey
- Make sure no spaces before/after key

**Fix C: Rate limit hit**
- Free tier: 60 requests/minute
- Wait 1 minute and try again
- Or upgrade to paid tier

---

### Issue 7: "X-Ray panel not showing data"

**Symptoms:**
- Ask question in Agent Buddy
- X-Ray panel says "Ask a question to see assembly"
- But you just did!

**Fix:**

```python
# This is a session state issue
# The component data isn't being stored

# Check if this line exists in generate function:
st.session_state.pilot_doc_components = components

# If missing, add it after building components in the chat section
```

---

## 🔍 Debug Mode

Enable verbose logging:

```bash
# Add this to top of universal_agent_app.py after imports:
import logging
logging.basicConfig(level=logging.DEBUG)
st.set_option('client.showErrorDetails', True)

# Run with debug flag:
streamlit run universal_agent_app.py --logger.level debug
```

---

## 📊 Health Check

Create this script to test everything:

```python
# health_check.py
import os
import sys

print("🔍 Universal Agent Health Check\n")

# 1. Check Python version
print(f"✓ Python: {sys.version.split()[0]}")

# 2. Check imports
try:
    import streamlit
    print(f"✓ Streamlit: {streamlit.__version__}")
except:
    print("❌ Streamlit not installed")

try:
    import google.generativeai
    print("✓ Gemini API library installed")
except:
    print("❌ google-generativeai not installed")

# 3. Check API key
api_key = os.environ.get("GOOG_API_KEY")
if api_key:
    print(f"✓ API Key: {'*' * 20}{api_key[-4:]}")
else:
    print("❌ API Key not set")

# 4. Check Knowledge Base
if os.path.exists("Knowledge_Base"):
    print("✓ Knowledge_Base directory exists")
    for client in ["NeoBank", "GlowCosmetics"]:
        path = f"Knowledge_Base/{client}"
        if os.path.exists(path):
            files = [f for f in os.listdir(path) if f.endswith('.md')]
            print(f"  ✓ {client}: {len(files)} articles")
        else:
            print(f"  ❌ {client} folder missing")
else:
    print("❌ Knowledge_Base directory not found")

# 5. Check ports
import socket
for port in [8501, 8765]:
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    if result == 0:
        print(f"⚠️  Port {port} already in use")
    else:
        print(f"✓ Port {port} available")
    sock.close()

print("\n✅ Health check complete!")
```

Run it:
```bash
python health_check.py
```

---

## 🆘 Quick Fixes Summary

| Problem | Quick Fix |
|---------|-----------|
| Search not working | Check console for debug messages, verify KB folder location |
| 404 model error | Update to `gemini-1.5-flash-latest` |
| Downloads MD not HTML | Run `python kb_generator.py` option 2 |
| Server won't start | Change HTTP_PORT to 8766 or check firewall |
| No API responses | Check `echo $GOOG_API_KEY` is set |
| Transcription silent | Install PyAudio and virtual audio cable |

---

## 📞 Still Stuck?

1. **Check the console output** - 90% of issues show error messages there
2. **Run health_check.py** - Systematic diagnosis
3. **Try demo.py** - Pre-configured test environment
4. **Check file locations** - Most common issue is Knowledge_Base in wrong place

---

## 🎓 Common Gotchas

1. **Working directory matters:**
   ```bash
   # Don't do this:
   cd /some/other/folder
   streamlit run /path/to/universal_agent_app.py
   
   # Do this:
   cd /path/to/universal_agent_app.py's_folder
   streamlit run universal_agent_app.py
   ```

2. **Environment variables don't persist across terminal sessions:**
   ```bash
   # Add to your shell profile to make permanent
   ```

3. **Streamlit caches aggressively:**
   ```bash
   # Clear cache if behavior seems stuck:
   streamlit cache clear
   ```

4. **KB files must be UTF-8 encoded:**
   ```bash
   # If seeing encoding errors, convert files:
   iconv -f ISO-8859-1 -t UTF-8 file.md > file_utf8.md
   ```

---

**Most issues are environment setup - the code is solid! 🚀**
