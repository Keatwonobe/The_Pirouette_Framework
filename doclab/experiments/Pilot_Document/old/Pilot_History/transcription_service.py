# transcription_service.py
import json
import pyaudio
from vosk import Model, KaldiRecognizer
import requests
import threading

# CONFIG
PILOT_API_URL = "http://127.0.0.1:8000/ingest_audio"

def start_listening():
    # Load Model (Must be downloaded from https://alphacephei.com/vosk/models)
    print("Loading Voice Model...")
    model = Model("model") 
    rec = KaldiRecognizer(model, 16000)
    
    p = pyaudio.PyAudio()
    
    # LISTENING TO MICROPHONE (Input)
    # Note: Capturing "System Audio" (Caller) usually requires a Virtual Cable driver 
    # or a specific loopback setting in Windows (WASAPI). 
    # For this pilot, we focus on the Agent's voice (simpler to setup).
    stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=8000)
    
    print("👂 Listening for speech...")
    
    while True:
        data = stream.read(4000, exception_on_overflow=False)
        if rec.AcceptWaveform(data):
            result = json.loads(rec.Result())
            text = result.get("text", "")
            
            if text:
                # PUSH to the Brain
                try:
                    requests.post(PILOT_API_URL, json={"speaker": "Agent", "text": text})
                except:
                    pass # Keep listening even if UI is momentarily down

if __name__ == "__main__":
    start_listening()