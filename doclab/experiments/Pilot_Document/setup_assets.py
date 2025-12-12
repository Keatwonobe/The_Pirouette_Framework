# setup_assets_v5.py
import os
import json

# 1. Setup Folders
folders = ["config/clients", "config/agents", "config/prompts"]
for f in folders:
    os.makedirs(f, exist_ok=True)

# 2. PROMPTS (Updated to include Compliance/Upsell context)
live_guidance_prompt = """
# ROLE
You are an expert Support Coach for {client_name}.
# CONTEXT
- **Customer Data:** {context_data}
- **Tone:** {tone}
- **Transcript:** {transcript_history}
- **Query:** {user_query}

# STRATEGY
- **Compliance Requirements:** {compliance_list}
- **Upsell Targets:** {upsell_targets}

# INSTRUCTIONS
Provide a response in this format:
1. **SCRIPT:** Exact words to say (Match Tone).
2. **CHECK:** What to verify immediately.
3. **GUIDE:** The step-by-step solution.
4. **COMPLIANCE ALERT:** If they missed a required step, flag it.
"""

with open("config/prompts/live_guidance.md", "w") as f: f.write(live_guidance_prompt)

# 3. CLIENT CONFIGS
# ---------------------------------------

# A. The "Gibberish" Challenge (Game Wiki)
pixel_pals_config = {
    "name": "Pixel Pals Support",
    "industry": "Gaming / Tech Support",
    "tone": "Geeky, knowledgeable, 'Gamer' lingo",
    "directive": "Solve the glitch, but warn about save file corruption.",
    "tools": {
        "Wiki_Search": "https://pixelpals.wiki/search",
        "Server_Status": "https://pixelpals.status"
    },
    # The Regex looks for "Wiki" style headers
    "context_parser": {
        "Game_Version": "Game:\\s*([A-Za-z0-9\\s]+)",
        "Glitch_Name": "Topic:\\s*([A-Za-z0-9\\s\\-]+)",
        "Risk_Level": "Risk:\\s*(Low|Medium|High|EXTREME)",
        "Player_Loc": "Loc:\\s*([A-Za-z\\s]+)"
    },
    "compliance_checklist": [
        "1. Confirm 'Unofficial Advice' Disclaimer",
        "2. Verify user is over 13",
        "3. Warn about 'Save File Corruption'"
    ],
    "upsell_strategy": {
        "Target": "Pro Gamer Subscription",
        "Pitch": "Never lose a save file again with Cloud Backups."
    },
    "sops": {
        "Soft-Lock Fix": "1. Power cycle. 2. Hold Up+B. 3. Pray.",
        "Item Duplication": "1. Fly to Coast. 2. Surf edge. 3. Encounter MissingNo."
    }
}

# B. NeoBank (Updated)
neobank_config = {
    "name": "NeoBank",
    "industry": "Banking",
    "tone": "Professional, Secure",
    "directive": "Protect assets.",
    "tools": {
        "Fraud_Dash": "https://neobank.int/fraud",
        "Acct_Viewer": "https://neobank.int/view"
    },
    "context_parser": {
        "Acct_Num": "Account\\s*#?:?\\s*(\\d{8,12})",
        "Name": "Name:\\s*([A-Za-z\\s]+)",
        "Status": "Status:\\s*(Active|Frozen|Closed)"
    },
    "compliance_checklist": [
        "1. Verify Name & DOB",
        "2. Send 2FA to Mobile",
        "3. Read 'Recorded Line' Disclosure"
    ],
    "upsell_strategy": {
        "Target": "High-Yield Savings",
        "Pitch": "I see you have a high checking balance. Our HYS offers 4.5% APY."
    },
    "sops": {"Fraud": "Freeze -> Verify -> Reissue", "Wire": "Auth -> Confirm -> Send"}
}

# C. Glow (Updated)
glow_config = {
    "name": "GlowCosmetics",
    "industry": "Retail",
    "tone": "Bestie Vibe, High Energy",
    "directive": "Make them feel pretty!",
    "tools": {"Shopify": "https://shopify.com", "Insta": "https://instagram.com"},
    "context_parser": {
        "Order_ID": "Order\\s*#?:?\\s*(GLOW-\\d{4})",
        "Name": "Customer:\\s*([A-Za-z\\s]+)"
    },
    "compliance_checklist": [
        "1. Confirm Shipping Address",
        "2. Check 'Allergy' Field",
        "3. Mention 'Final Sale' items"
    ],
    "upsell_strategy": {
        "Target": "Glow Kit Bundle",
        "Pitch": "Since you love the lipstick, the whole kit is 20% off today!"
    },
    "sops": {"Return": "30 Days -> Condition Check -> Label", "Lost Pkg": "Wait 48h -> Resend"}
}

with open("config/clients/pixel_pals.json", "w") as f: json.dump(pixel_pals_config, f, indent=2)
with open("config/clients/neobank.json", "w") as f: json.dump(neobank_config, f, indent=2)
with open("config/clients/glow_cosmetics.json", "w") as f: json.dump(glow_config, f, indent=2)

print("✅ Assets Updated: Pixel Pals, NeoBank, Glow")