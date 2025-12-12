import os
import markdown

# 1. DEFINE YOUR CLIENT KNOWLEDGE
# In production, this would come from the client web portal upload
raw_data = {
    "NeoBank": {
        "identity_verification.md": "# VERIFICATION\n**Strict Policy:** Never ask for PIN.\n\n1. Ask for Mother's Maiden Name.\n2. Verify Last Transaction.",
        "premium_pricing.md": "# METAL CARD PRICING\n- **Cost:** $25/mo\n- **Perks:** Travel Insurance, Airport Lounge.\n- **Keywords:** cost, price, expensive, metal, tier",
        "dispute_process.md": "# DISPUTES\n1. Check transaction date.\n2. Issue provisional credit if <$50.\n3. Keywords: fraud, stolen, charge, unrecognized"
    },
    "GlowCosmetics": {
        "return_policy.md": "# RETURNS\n**Window:** 30 Days.\n**Condition:** Lightly used is OK.\n**Keywords:** refund, return, hate it, broken",
        "influencer_tier.md": "# INFLUENCER PROMO\n- **Code:** GLOWUP20\n- **Discount:** 20% off.\n- **Keywords:** instagram, tiktok, code, promo"
    }
}

BASE_DIR = "Knowledge_Base"

def build():
    if not os.path.exists(BASE_DIR):
        os.makedirs(BASE_DIR)
        
    for client, docs in raw_data.items():
        client_dir = os.path.join(BASE_DIR, client)
        os.makedirs(client_dir, exist_ok=True)
        
        for filename, content in docs.items():
            # Create HTML version for the browser tab
            html_content = markdown.markdown(content)
            styled_html = f"""
            <html><head><style>
                body {{ font-family: sans-serif; padding: 40px; background: #f4f4f9; }}
                .card {{ background: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
                h1 {{ color: #005cc5; border-bottom: 2px solid #eee; }}
            </style></head><body><div class="card">{html_content}</div></body></html>
            """
            
            html_name = filename.replace(".md", ".html")
            with open(os.path.join(client_dir, html_name), "w") as f:
                f.write(styled_html)
                
            # Create MD version for AI Context reading
            with open(os.path.join(client_dir, filename), "w") as f:
                f.write(content)
                
    print("✅ Knowledge Base Built: HTML and MD files ready.")

if __name__ == "__main__":
    build()