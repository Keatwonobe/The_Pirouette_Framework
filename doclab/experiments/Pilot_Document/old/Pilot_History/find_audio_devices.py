import speech_recognition as sr

def list_microphones():
    mics = sr.Microphone.list_microphone_names()
    print("AVAILABLE AUDIO DEVICES:")
    print("-----------------------")
    for i, mic_name in enumerate(mics):
        print(f"Index {i}: {mic_name}")

if __name__ == "__main__":
    list_microphones()