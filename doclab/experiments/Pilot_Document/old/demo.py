#!/usr/bin/env python3
"""
Universal Agent Assistant - Demo Mode
Launches with pre-populated sample data for executive presentations
"""

import json
import time
import os
import subprocess
import sys

def create_demo_state():
    """Create a demo state file with sample conversation"""
    demo_state = {
        "client": "NeoBank",
        "transcript": "I think someone stole my credit card information and made fraudulent charges",
        "new_hits": [
            {
                "id": "Fraud_Alert_Protocol.md",
                "name": "Fraud Alert Protocol",
                "link": "http://localhost:8765/NeoBank/Fraud_Alert_Protocol.html",
                "score": 10,
                "timestamp": time.time()
            }
        ],
        "last_update": time.time()
    }
    
    with open("live_state.json", "w") as f:
        json.dump(demo_state, f, indent=2)
    
    print("✓ Created demo state file")

def check_api_key():
    """Check if API key is set"""
    if not os.environ.get("GOOGLE_API_KEY"):
        print("\n⚠️  WARNING: No API key found!")
        print("   The Agent Buddy AI features will not work.")
        print("\n   To enable AI features:")
        print("   1. Get key: https://aistudio.google.com/app/apikey")
        print("   2. Set it:")
        print("      Windows: $env:GOOGLE_API_KEY=\"your_key\"")
        print("      Mac/Linux: export GOOGLE_API_KEY=\"your_key\"")
        print("\n   Press Enter to continue anyway, or Ctrl+C to exit...")
        input()

def print_demo_instructions():
    """Print helpful demo instructions"""
    print("\n" + "=" * 60)
    print("🎭 DEMO MODE - Universal Agent Assistant")
    print("=" * 60)
    print("\n📋 Demo Scenarios for Executives:\n")
    
    print("1️⃣  FRAUD ALERT (NeoBank)")
    print("   • Client: NeoBank")
    print("   • Agent: Select 'Alex Chen' (new hire)")
    print("   • In Agent Buddy: 'Customer reporting fraud charges'")
    print("   • Watch: X-Ray shows agent coaching focus\n")
    
    print("2️⃣  RETURNS (GlowCosmetics)")
    print("   • Client: GlowCosmetics")
    print("   • Agent: Select 'Jordan Smith' (senior)")
    print("   • In Agent Buddy: 'Customer wants to return opened lipstick'")
    print("   • Watch: Brand voice matching, upsell opportunities\n")
    
    print("3️⃣  MANUAL SEARCH")
    print("   • Use sidebar search: Try 'password' or 'order status'")
    print("   • Click articles to view full content")
    print("   • Watch: Frequency indicators on repeated searches\n")
    
    print("4️⃣  X-RAY TRANSPARENCY")
    print("   • After any Agent Buddy question")
    print("   • Right panel shows 4 layers of context")
    print("   • Demonstrates how AI assembles guidance\n")
    
    print("🎤 Optional: Live Transcription")
    print("   • If virtual audio cable is installed")
    print("   • Click 'Start Listening' in sidebar")
    print("   • Speak keywords like 'fraud' or 'return'")
    print("   • Watch articles auto-populate\n")
    
    print("=" * 60)
    print("\n🚀 Starting application...")
    print("   Browser will open automatically at: http://localhost:8501")
    print("=" * 60 + "\n")

def main():
    # Check environment
    check_api_key()
    
    # Create demo data
    create_demo_state()
    
    # Print instructions
    print_demo_instructions()
    
    # Wait a moment for user to read
    time.sleep(2)
    
    # Launch Streamlit
    try:
        subprocess.run([sys.executable, "-m", "streamlit", "run", "universal_agent_app.py"])
    except KeyboardInterrupt:
        print("\n\n👋 Demo ended. Thank you!")
    except Exception as e:
        print(f"\n❌ Error launching app: {e}")
        print("\nTry manually: streamlit run universal_agent_app.py")

if __name__ == "__main__":
    main()
