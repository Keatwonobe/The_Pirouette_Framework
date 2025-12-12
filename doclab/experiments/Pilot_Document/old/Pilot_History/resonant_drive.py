import os
import json

# Define the directory structure
base_dir = "Resonant_Drive"
structure = {
    "01_Clients/NeoBank": {
        "context.md": "# IDENTITY: NeoBank\n**Voice:** Formal, Secure, Empathetic.\n**Keywords:** Security, Asset Protection, Verification.\n**Never:** Use slang or emojis.",
        "auth_protocol.md": "## AUTHENTICATION (LEVEL 4)\n1. Ask for Full Name.\n2. Send Push Notification to App.\n3. Verify 6-digit code."
    },
    "01_Clients/GlowCosmetics": {
        "context.md": "# IDENTITY: GlowCosmetics\n**Voice:** Bestie energy! High energy, supportive.\n**Keywords:** Glow, Routine, Self-care.\n**Always:** Compliment their choice.",
        "auth_protocol.md": "## AUTHENTICATION (LEVEL 1)\n1. Ask for Order Number.\n2. Confirm Email Address."
    },
    "02_Modules": {
        "refund_process.md": "### SOP: REFUND PROCESS\n1. Check if purchase was < 30 days ago.\n2. If YES: Process full refund to original payment.\n3. If NO: Offer store credit only.",
        "upsell_closing.md": "### SOP: CLOSING\n1. Ask: 'Is there anything else?'\n2. Suggest: 'Did you see our new [Product_Name]?'\n3. Thank them for being a loyal customer.",
        "shipping_inquiry.md": "### SOP: SHIPPING CHECK\n1. Open Logistics Dashboard.\n2. Check tracking number status.\n3. If 'Delayed', offer 10% discount on next order."
    },
    "03_Agents": {
        "frame_config.json": json.dumps({
            "interface": "Sarah (Manager)",
            "feedback": "Mike (QA)",
            "core": ["Agent_1", "Agent_2", "Agent_3"]
        }, indent=2)
    }
}

def create_demo_files():
    if not os.path.exists(base_dir):
        os.makedirs(base_dir)
    
    for path, contents in structure.items():
        # Create subdirectories if nested
        full_path = os.path.join(base_dir, path)
        
        # If it's a directory key (has sub-keys), make the dir
        if isinstance(contents, dict):
            os.makedirs(full_path, exist_ok=True)
            for filename, file_content in contents.items():
                with open(os.path.join(full_path, filename), "w") as f:
                    f.write(file_content)
        else:
            # It's a file in a folder
            directory = os.path.dirname(full_path)
            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(full_path, "w") as f:
                f.write(contents)

    print(f"✅ Bulletproof Demo Data generated in '{base_dir}'")
    print("You can now point your Streamlit App to read from this folder.")

if __name__ == "__main__":
    create_demo_files()