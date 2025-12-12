
import os
import markdown

# Define the structure (Simplified for International Agents)
BASE_DIR = "Universal_Drive"

structure = {
    "NeoBank": {
        "identity.md": "# CLIENT: NeoBank\n**Tone:** Professional, Secure.\n**Key Rule:** Never ask for PINs.",
        "pricing.md": "# PRICING TIERS\n- **Basic:** Free\n- **Premium:** $15/mo\n- **Metal:** $25/mo",
        "greeting.md": "# GREETING\n1. Thank them for calling NeoBank.\n2. Ask for Full Name.\n3. Verify Account."
    },
    "GlowCosmetics": {
        "identity.md": "# CLIENT: GlowCosmetics\n**Tone:** Friendly, Excited.\n**Key Rule:** Use First Names.",
        "pricing.md": "# DISCOUNTS\n- **New Customer:** 10% Off\n- **Influencer:** 20% Off",
        "greeting.md": "# HELLO!\n1. Say: 'Thanks for glowing with us!'\n2. Ask for Order #."
    }
}

def generate_html(md_text, title):
    """Wraps markdown in a clean, readable HTML template"""
    html_content = markdown.markdown(md_text)
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>{title}</title>
        <style>
            body {{ font-family: sans-serif; padding: 40px; max-width: 800px; margin: 0 auto; line-height: 1.6; background: #f4f4f9; }}
            .card {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; border-bottom: 2px solid #eee; padding-bottom: 10px; }}
            strong {{ color: #e74c3c; }}
        </style>
    </head>
    <body><div class="card">{html_content}</div></body>
    </html>
    """

def build_drive():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
    
    for client, files in structure.items():
        client_dir = os.path.join(BASE_DIR, client)
        os.makedirs(client_dir, exist_ok=True)
        
        for filename, content in files.items():
            # Save HTML version for the Browser Tabs
            html_filename = filename.replace(".md", ".html")
            with open(os.path.join(client_dir, html_filename), "w") as f:
                f.write(generate_html(content, f"{client} - {filename}"))
            
            # Save MD version for the Snippet View
            with open(os.path.join(client_dir, filename), "w") as f:
                f.write(content)

    print("✅ Universal Drive Built. Ready for service.")

if __name__ == "__main__":
    build_drive()