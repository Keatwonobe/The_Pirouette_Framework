# TASK
Transform the following transcript and contextual knowledge into a structured, code-rigid PIRouette Module.
This output is designed for:
- Auto-QA systems
- Sales enablement
- Coaching
- Machine parsing
- Post-call enrichment
- Lead scoring
- Database ingestion
- Compliance verification

Always follow the structure.  
Never vary labels or ordering.  
Treat the call as a “phase flow event” and produce a wound-channel summary.

# OUTPUT FORMAT (MANDATORY)
Return the output in the following structure exactly:

### [PCM-1] WOUND_CHANNEL_SUMMARY
- A 3–7 sentence forensic reconstruction of the “interaction trajectory.”
- Focus on force vectors: intent, resistance, momentum, conversion probability.
- Describe the laminar vs turbulent information flow.
- Identify the pivot moments where the agent could re-stabilize or destabilize the call.

### [PCM-2] CUSTOMER_STATE_VECTOR
Provide a JSON object with:
{{
  "emotional_state": "...",
  "sentiment_score": -10 to +10,
  "friction_points": ["...", "..."],
  "purchase_vector": {{
      "intent_strength": 0-100,
      "urgency": 0-100,
      "budget_signal": "low|medium|high|unknown",
      "risk_posture": "low|medium|high"
  }},
  "retention_risk": 0-100,
  "expansion_opportunity": 0-100
}}

### [PCM-3] SALES_DIAGNOSTIC_MODULE
A list of 5–12 razor-sharp diagnostics identifying:
- Missed opportunities
- Perfect moves
- Micro-moments of leverage
- Hidden objections
- Latent buying motives
- Social signals
- Pirouette-coded “entropy leaks” (places where agent wasted effort or allowed disorder)

### [PCM-4] AUTO_QA_MODULE
Return a machine-readable auto-QA set:

{{
  "compliance_flags": [
    {{"line": X, "issue": "Missing disclosure", "severity": 2}},
    {{"line": Y, "issue": "Incorrect verification", "severity": 3}}
  ],
  "sales_effectiveness": {{
    "score": 0-100,
    "justification": "..."
  }},
  "behavioral_alignment": {{
    "score": 0-100,
    "notes": "Alignment with client's tone and directive"
  }},
  "critical_events": [
    {{"line": N, "event": "Objection emergence"}},
    {{"line": M, "event": "Momentum collapse"}},
    {{"line": P, "event": "Closing window opened"}}
  ]
}}

### [PCM-5] FOLLOW_UP_GUIDANCE
Provide:
- A recommended follow-up email or call script
- The 3 highest-value CTAs
- A timing recommendation (hours/days)
- A confidence interval

### [PCM-6] LEAD_ENRICHMENT_SUMMARY
Return structured details for CRM enrichment:

{{
  "customer_profile": "...",
  "identified_needs": ["...", "..."],
  "product_fits": ["...", "..."],
  "upsell_paths": ["..."],
  "next_purchase_probability": 0-100,
  "churn_prediction": 0-100
}}

### [PCM-7] ACTION_ITEMS
A list of clean, atomic tasks the agent should perform next.

### [PCM-8] DATA_ATOMS (FOR DATABASE INGESTION)
Return the 10–20 most important extracted nouns/keywords from the interaction.
This forms a “semantic fingerprint” for downstream retrieval.

### [PCM-9] RAW_CONTEXT_BRIDGE
Summarize in <200 tokens the minimal information required to rehydrate this call later.

# TRANSCRIPT
{transcript}

# CONTEXT
{context_data}