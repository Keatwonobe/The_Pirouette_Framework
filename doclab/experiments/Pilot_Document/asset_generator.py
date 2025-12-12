import os
import json

# 1. Setup Directory Structure
folders = ["config/clients", "config/agents", "config/prompts"]
for f in folders:
    os.makedirs(f, exist_ok=True)

print("📂 Directories created.")

# ==========================================
# 2. PROMPT TEMPLATES (The Brain)
# ==========================================

live_guidance_md = """
# SYSTEM ROLE
You are an expert Real-Time Support Coach for **{client_name}**.

# INPUT CONTEXT
- **Customer Data (Scraped):** {context_data}
- **Required Tone:** {tone}
- **Live Transcript:** "{transcript_history}"
- **Current Agent Query:** "{user_query}"

# STRATEGIC OBJECTIVES
- **Compliance Requirements:** {compliance_list}
- **Upsell Opportunity:** {upsell_targets}

# RESPONSE FORMAT
Provide a response in this exact structure:

### 🗣️ SCRIPT
(Write the exact response the agent should say, matching the {tone} tone. Keep it under 2 sentences.)

### ✅ VERIFY
(Bullet points of data to confirm immediately.)

### 🧭 GUIDANCE
(The step-by-step solution or tool usage.)

### ⚠️ ALERT
(If a compliance rule from the list above was missed or is at risk, flag it here. Otherwise, leave empty.)
"""

with open("config/prompts/live_guidance.md", "w", encoding="utf-8") as f:
    f.write(live_guidance_md)

print("📝 Prompts generated.")

# ==========================================
# 3. CLIENT CONFIGURATIONS (The Identity)
# ==========================================

# CLIENT A: Pixel Pals (The "Wiki/Gibberish" Parser)
pixel_pals = {
    "name": "Pixel Pals Support",
    "industry": "Gaming / Tech Support",
    "tone": "Geeky, knowledgeable, 'Gamer' lingo, Empathetic regarding save data",
    "directive": "Solve the glitch, but warn about save file corruption.",
    "tools": {
        "Wiki_Search": "https://pixelpals.wiki/search",
        "Server_Status": "https://pixelpals.status",
        "Save_Editor": "https://pixelpals.admin/tools"
    },
    # The Regex looks for "Wiki" style headers
    "context_parser": {
        "Game_Version": "Game:\\s*([A-Za-z0-9\\s]+)",
        "Glitch_Name": "Topic:\\s*([A-Za-z0-9\\s\\-]+)",
        "Risk_Level": "Risk:\\s*(Low|Medium|High|EXTREME)",
        "Player_Loc": "Loc:\\s*([A-Za-z\\s]+)"
    },
    "compliance_checklist": [
        "1. Disclaimer: 'Unofficial Advice'",
        "2. Verify user is over 13 (COPPA)",
        "3. Warn: 'May Corrupt Save File'"
    ],
    "upsell_strategy": {
        "Target": "Pro Gamer Subscription",
        "Pitch": "Never lose a save file again. Cloud Backups start at $2/mo."
    },
    "sops": {
        "Soft-Lock Fix": "1. Power cycle. 2. Hold Up+B. 3. Pray.",
        "Item Duplication": "1. Fly to Coast. 2. Surf edge. 3. Encounter MissingNo.",
        "Corrupted Save": "1. Do NOT save. 2. Load Backup. 3. Submit Bug Report."
    }
}

# CLIENT B: NeoBank (The High Security)
neobank = {
    "name": "NeoBank",
    "industry": "Banking",
    "tone": "Professional, Secure, Reassuring, Concise",
    "directive": "Protect assets. Verify identity before ANY info disclosure.",
    "tools": {
        "Fraud_Dash": "https://neobank.int/fraud",
        "Acct_Viewer": "https://neobank.int/view",
        "Wire_Auth": "https://neobank.int/wire"
    },
    "context_parser": {
        "Acct_Num": "Account\\s*#?:?\\s*(\\d{8,12})",
        "Name": "Name:\\s*([A-Za-z\\s]+)",
        "Balance": "Balance:\\s*\\$([\\d,]+\\.\\d{2})",
        "Status": "Status:\\s*(Active|Frozen|Closed)"
    },
    "compliance_checklist": [
        "1. Verify Name & DOB",
        "2. Send 2FA to Mobile",
        "3. Read 'Recorded Line' Disclosure",
        "4. NEVER read card numbers aloud"
    ],
    "upsell_strategy": {
        "Target": "High-Yield Savings",
        "Pitch": "I see a healthy checking balance. Our HYS offers 4.5% APY—would you like to activate that?"
    },
    "sops": {
        "Fraud Freeze": "1. Click 'Emergency Freeze'. 2. Verify last 3 transactions. 3. Reissue Card.",
        "Wire Transfer": "1. Authenticate Voice ID. 2. Confirm IBAN. 3. Read Warning Script."
    }
}

# CLIENT C: GlowCosmetics (The High Energy)
glow = {
    "name": "GlowCosmetics",
    "industry": "Retail / Beauty",
    "tone": "Bestie Vibe, High Energy, Emojis, Supportive",
    "directive": "Make them feel pretty! Upsell the bundle.",
    "tools": {
        "Shopify_Admin": "https://shopify.com", 
        "Insta_Feed": "https://instagram.com",
        "Return_Portal": "https://returns.glow.com"
    },
    "context_parser": {
        "Order_ID": "Order\\s*#?:?\\s*(GLOW-\\d{4})",
        "Name": "Customer:\\s*([A-Za-z\\s]+)",
        "Items": "Items:\\s*([A-Za-z0-9\\s,]+)"
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
    "sops": {
        "Return Request": "1. Check 30-day window. 2. Verify condition (swatched ok, empty no). 3. Issue Label.",
        "Lost Package": "1. Empathize! 2. Check Carrier. 3. Resend with Free Sample."
    }
}

# CLIENT D: OmniTravel (Complex Dates)
omni = {
    "name": "OmniTravel Concierge",
    "industry": "Travel & Hospitality",
    "tone": "Efficient, Premium, Calm",
    "directive": "Solve the disruption. Keep the traveler moving.",
    "tools": {
        "GDS_Terminal": "https://sabre.view", 
        "Hotel_Bedbank": "https://hotelbeds.com"
    },
    "context_parser": {
        "PNR": "PNR:\\s*([A-Z0-9]{6})",
        "Passenger": "PAX:\\s*([A-Za-z\\s]+)",
        "Destination": "Dest:\\s*([A-Z]{3})",
        "Flight_Date": "Date:\\s*(\\d{2}[A-Z]{3})"
    },
    "compliance_checklist": [
        "1. Verify Passport Expiry",
        "2. Read 'Non-Refundable' Clause",
        "3. Confirm Visa Requirements"
    ],
    "upsell_strategy": {
        "Target": "Travel Insurance",
        "Pitch": "Given the tight connection, I strongly recommend the Missed Connection protection for $20."
    },
    "sops": {
        "Flight Cancellation": "1. Check next available. 2. Protect PNR. 3. Reissue Ticket.",
        "Name Change": "1. Check Fare Rules. 2. Collect Fee. 3. Update Secure Flight Data."
    }
}

# Write Clients
clients = {
    "pixel_pals": pixel_pals,
    "neobank": neobank,
    "glow_cosmetics": glow,
    "omni_travel": omni
}

for filename, data in clients.items():
    with open(f"config/clients/{filename}.json", "w") as f:
        json.dump(data, f, indent=2)

print("🏢 Client Configs generated.")

# ==========================================
# 4. AGENT PROFILES (The Users)
# ==========================================

agent_1 = {
    "name": "Demo Agent",
    "role": "Universal Associate",
    "focus_area": "System Capabilities",
    "stats": {"CSAT": "5.0", "AHT": "N/A"}
}

agent_2 = {
    "name": "Sarah Connor",
    "role": "Crisis Specialist",
    "focus_area": "De-escalation",
    "stats": {"CSAT": "4.9", "AHT": "420s"}
}

agent_3 = {
    "name": "Alex Murphy",
    "role": "Compliance Officer",
    "focus_area": "Regulatory Adherence",
    "stats": {"CSAT": "4.2", "AHT": "180s"}
}

agents = {
    "demo_agent": agent_1,
    "sarah_connor": agent_2,
    "alex_murphy": agent_3
}

for filename, data in agents.items():
    with open(f"config/agents/{filename}.json", "w") as f:
        json.dump(data, f, indent=2)

print("busts Agent Profiles generated.")
print("✅ Full Asset Loop Complete. Run 'universal_agent_v7.py' now.")