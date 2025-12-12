# active_listener.py
import os
import queue
import sys
import sounddevice as sd
import vosk
import json
import datetime

# CONFIGURATION
# =================
MODEL_PATH = "model" # Folder name where you unzipped the Vosk model
OUTPUT_FILE = "live_log.txt"
SAMPLE_RATE = 16000
# Set this to the ID of your Virtual Cable if default doesn't work.
# Run 'python -m sounddevice' to see list.
DEVICE_ID = None 
IGNORE_LIST = ["huh", "hmm", "ah", "oh"] # Words to strictly ignore if they appear alone

# INIT VOSK
# =================
if not os.path.exists(MODEL_PATH):
    print(f"❌ Model not found at '{MODEL_PATH}'. Please download from https://alphacephei.com/vosk/models")
    sys.exit(1)

print(f"🚀 Loading Vosk Model...")
model = vosk.Model(MODEL_PATH)
q = queue.Queue()

def callback(indata, frames, time, status):
    """This is called (from a separate thread) for each audio block."""
    if status:
        print(status, file=sys.stderr)
    q.put(bytes(indata))

# MAIN LOOP
# =================
print(f"🎤 Listening... Writing to {OUTPUT_FILE}")
print("Press Ctrl+C to stop.")

# Clear old log on start
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    f.write(f"--- Session Started: {datetime.datetime.now()} ---\n")

try:
    with sd.RawInputStream(samplerate=SAMPLE_RATE, blocksize=8000, device=DEVICE_ID,
                           dtype='int16', channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, SAMPLE_RATE)
        
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                # Final Result (Phrase Complete)
                result = json.loads(rec.Result())
                text = result['text'].strip() # Remove surrounding whitespace
                
                # LOGIC: Filter out "huh" and empty strings
                # 1. Check if text exists
                # 2. Check if the text is exactly one of the ignore words
                # 3. Optional: Check if text is too short (e.g. < 2 chars) to be a real sentence
                if text and (text not in IGNORE_LIST) and (len(text) > 1):
                    
                    timestamp = datetime.datetime.now().strftime("%H:%M:%S")
                    line = f"[{timestamp}] {text}\n"
                    print(line.strip()) 
                    
                    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
                        f.write(line)
                        f.flush()
            else:
                # Partial Result (In progress) - Optional: Use this if you want "streaming" text
                pass

except KeyboardInterrupt:
    print("\n🛑 Stopping...")
except Exception as e:
    print(f"\n❌ Error: {e}")