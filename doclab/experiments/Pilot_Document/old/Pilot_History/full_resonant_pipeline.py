import speech_recognition as sr
import os
import json
import time
import nltk
from nltk.corpus import stopwords

# Ensure stopwords are downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

stop_words = set(stopwords.words('english'))

# SHARED STATE FILE
STATE_FILE = "live_state.json"
KB_DIR = "Knowledge_Base"

def search_kb(client, transcript_fragment):
    """
    1. Tokenize transcript
    2. Remove stopwords
    3. Search client files for matches
    """
    if not client or not os.path.exists(os.path.join(KB_DIR, client)):
        return []

    # Essentialize
    words = transcript_fragment.lower().split()
    keywords = [w for w in words if w not in stop_words and len(w) > 3]
    
    hits = []
    
    # Simple Search: Check if keywords exist in filenames or content
    client_path = os.path.join(KB_DIR, client)
    for filename in os.listdir(client_path):
        if filename.endswith(".md"): # Scan MD for content, return HTML link
            with open(os.path.join(client_path, filename), "r") as f:
                content = f.read().lower()
            
            score = 0
            for k in keywords:
                if k in content or k in filename:
                    score += 1
            
            if score > 0:
                html_link = os.path.abspath(os.path.join(client_path, filename.replace(".md", ".html")))
                hits.append({"name": filename.replace(".md", ""), "link": f"file:///{html_link}", "score": score})
    
    # Sort by relevance
    hits.sort(key=lambda x: x['score'], reverse=True)
    return hits[:3] # Top 3 results

def run_listener():
    r = sr.Recognizer()
    
    # --- FIX START: Explicitly find the Virtual Cable ---
    target_mic_index = None
    mics = sr.Microphone.list_microphone_names()
    
    # 1. Try to auto-detect "CABLE Output"
    for i, name in enumerate(mics):
        if "CABLE Output" in name:
            target_mic_index = i
            print(f"✅ Auto-detected Virtual Cable at Index {i}: {name}")
            break
            
    # 2. Fallback: Use default if CABLE not found (prevents crash)
    if target_mic_index is None:
        print("⚠️ CABLE Output not found. Using default microphone.")
        # If you want to force a specific index you found in Step 1, set it here:
        # target_mic_index = 1  <-- REPLACE WITH YOUR INDEX IF AUTO-DETECT FAILS
    
    # Initialize Microphone with the specific index (or None for default)
    mic = sr.Microphone(device_index=target_mic_index)
    # --- FIX END ---

    # Initialize State
    current_state = {
        "client": "NeoBank", 
        "transcript": "",
        "suggested_links": []
    }
    
    # Safe Print: Handle case where index might still be None (Default)
    mic_name = mics[target_mic_index] if target_mic_index is not None else "Default Microphone"
    print(f"🎧 Listening on {mic_name}...")
    
    with mic as source:
        # We increase the adjust time slightly for virtual cables as they can be silent
        print("Adjusting for ambient noise... (Please wait)")
        r.adjust_for_ambient_noise(source, duration=1) 
        
        while True:
            try:
                # Same loop as before...
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=5)
                text = r.recognize_google(audio)
                print(f"🗣️ Heard: {text}")
                
                # Update State
                current_state["transcript"] = text # Keep only latest burst for search
                
                # Run Logic
                links = search_kb(current_state["client"], text)
                current_state["suggested_links"] = links
                
                # Write to JSON for Frontend
                with open(STATE_FILE, "w") as f:
                    json.dump(current_state, f)
                
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    run_listener()