import speech_recognition as sr
import os
import json
import time
import nltk
from nltk.corpus import stopwords

# Setup NLTK
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')
stop_words = set(stopwords.words('english'))

# CONFIG
STATE_FILE = "live_state.json"
KB_DIR = "Knowledge_Base"

# Explicitly find the Virtual Cable (The Fix from earlier)
def get_cable_index():
    mics = sr.Microphone.list_microphone_names()
    for i, name in enumerate(mics):
        if "CABLE Output" in name:
            return i
    return None # Fallback to default

def search_kb(client, transcript_fragment):
    if not client or not os.path.exists(os.path.join(KB_DIR, client)):
        return []

    words = transcript_fragment.lower().split()
    # Looser filtering: Allow words > 2 chars to catch more hits
    keywords = [w for w in words if w not in stop_words and len(w) > 2]
    
    hits = []
    client_path = os.path.join(KB_DIR, client)
    
    # Scan files
    for filename in os.listdir(client_path):
        if filename.endswith(".md"):
            with open(os.path.join(client_path, filename), "r") as f:
                content = f.read().lower()
            
            # Scoring: 1 point for content match, 3 points for filename match
            score = 0
            for k in keywords:
                if k in content: score += 1
                if k in filename.lower(): score += 3
            
            if score > 0:
                # We return the filename as the unique ID
                html_link = os.path.abspath(os.path.join(client_path, filename.replace(".md", ".html")))
                hits.append({
                    "id": filename, 
                    "name": filename.replace(".md", "").replace("_", " ").title(), 
                    "link": f"file:///{html_link}", 
                    "score": score,
                    "timestamp": time.time()
                })
    
    hits.sort(key=lambda x: x['score'], reverse=True)
    return hits[:3] # Return top 3 for this burst

def run_listener():
    r = sr.Recognizer()
    mic_index = get_cable_index()
    mic = sr.Microphone(device_index=mic_index)
    
    print(f"🎧 Pipeline Active on Index {mic_index}...")
    
    # Initialize State File if missing
    if not os.path.exists(STATE_FILE):
        with open(STATE_FILE, "w") as f:
            json.dump({"client": "NeoBank", "transcript": "", "new_hits": []}, f)
            
    with mic as source:
        r.adjust_for_ambient_noise(source, duration=1)
        
        while True:
            try:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=5)
                text = r.recognize_google(audio)
                print(f"🗣️ Heard: {text}")
                
                # Load current client from state file (allows App to change client)
                try:
                    with open(STATE_FILE, "r") as f:
                        current_data = json.load(f)
                        current_client = current_data.get("client", "NeoBank")
                except:
                    current_client = "NeoBank"

                # Search
                new_hits = search_kb(current_client, text)
                
                # Update State
                output = {
                    "client": current_client,
                    "transcript": text,
                    "new_hits": new_hits,
                    "last_update": time.time()
                }
                
                with open(STATE_FILE, "w") as f:
                    json.dump(output, f)
                    
            except sr.WaitTimeoutError:
                pass
            except sr.UnknownValueError:
                pass
            except Exception as e:
                print(f"Error: {e}")

if __name__ == "__main__":
    run_listener()