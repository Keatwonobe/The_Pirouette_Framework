#!/usr/bin/env python3
"""
Universal Agent Assistant - Setup Script
Prepares the environment and validates configuration
"""

import os
import sys
import subprocess

def check_python_version():
    """Ensure Python 3.8+"""
    if sys.version_info < (3, 8):
        print("❌ Python 3.8 or higher is required")
        print(f"   Current version: {sys.version}")
        return False
    print(f"✓ Python version: {sys.version.split()[0]}")
    return True

def install_requirements():
    """Install required packages"""
    print("\n📦 Installing requirements...")
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt", "-q"])
        print("✓ All packages installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("❌ Failed to install requirements")
        print("   Try manually: pip install -r requirements.txt")
        return False

def check_api_key():
    """Check for Gemini API key"""
    print("\n🔑 Checking API key...")
    api_key = os.environ.get("GOOGLE_API_KEY")
    if api_key:
        print(f"✓ API key found (length: {len(api_key)})")
        return True
    else:
        print("⚠️  No API key found")
        print("   Set it with:")
        print("   - Windows: $env:GOOGLE_API_KEY=\"your_key\"")
        print("   - Mac/Linux: export GOOGLE_API_KEY=\"your_key\"")
        print("   Get your key: https://aistudio.google.com/app/apikey")
        return False

def check_knowledge_base():
    """Verify knowledge base structure"""
    print("\n📚 Checking knowledge base...")
    kb_dir = "Knowledge_Base"
    
    if not os.path.exists(kb_dir):
        print(f"❌ {kb_dir} directory not found")
        return False
    
    clients = ["NeoBank", "GlowCosmetics"]
    for client in clients:
        client_path = os.path.join(kb_dir, client)
        if os.path.exists(client_path):
            files = [f for f in os.listdir(client_path) if f.endswith(('.md', '.html'))]
            print(f"✓ {client}: {len(files)} files")
        else:
            print(f"⚠️  {client} folder missing")
    
    return True

def check_optional_features():
    """Check optional components"""
    print("\n🎤 Checking optional features...")
    
    # Speech recognition
    try:
        import speech_recognition
        print("✓ Speech recognition available")
        try:
            import speech_recognition as sr
            mics = sr.Microphone.list_microphone_names()
            print(f"  Found {len(mics)} audio devices")
            for i, mic in enumerate(mics):
                if "CABLE" in mic or "Stereo Mix" in mic:
                    print(f"  ✓ Virtual audio cable detected: {mic}")
        except:
            print("  ⚠️  Could not enumerate audio devices")
    except ImportError:
        print("⚠️  Speech recognition not installed (optional)")
        print("   Install with: pip install SpeechRecognition PyAudio")
    
    # Markdown
    try:
        import markdown
        print("✓ Markdown processor available")
    except ImportError:
        print("⚠️  Markdown not installed (for HTML conversion)")

def create_desktop_shortcut():
    """Create a desktop shortcut (optional)"""
    print("\n🖥️  Desktop shortcut...")
    print("   (Skipped - create manually if needed)")

def main():
    print("=" * 50)
    print("🌐 Universal Agent Assistant - Setup")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", install_requirements),
        ("API Key", check_api_key),
        ("Knowledge Base", check_knowledge_base),
        ("Optional Features", check_optional_features),
    ]
    
    results = []
    for name, check in checks:
        try:
            result = check()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Error during {name}: {e}")
            results.append((name, False))
    
    print("\n" + "=" * 50)
    print("📊 Setup Summary")
    print("=" * 50)
    
    for name, result in results:
        status = "✓" if result else "⚠️ "
        print(f"{status} {name}")
    
    print("\n" + "=" * 50)
    
    if all(result for _, result in results[:3]):  # Core features
        print("✅ Core setup complete! Ready to run.")
        print("\n🚀 Start the application with:")
        print("   streamlit run universal_agent_app.py")
    else:
        print("⚠️  Some setup steps need attention.")
        print("   Review the messages above and fix any issues.")
    
    print("=" * 50)

if __name__ == "__main__":
    main()
