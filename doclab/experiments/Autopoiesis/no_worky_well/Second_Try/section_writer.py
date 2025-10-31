
import os, json, uuid
from pathlib import Path

try:
    import google.generativeai as genai  # type: ignore
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

MODEL = "gemini-2.5-pro"
API_KEY_ENV = "GOOGLE_API_KEY"

OUT_DIR = "./sections_out"

SYSTEM_DIRECTIVE = """You are writing ONE SECTION of a longer technical manifesto.
You MUST write from the vantage of the assigned section ONLY.
Keep tone and vocabulary consistent across calls: formal, precise, restrained poetic gravitas.
Define symbols on first use. Use minimal, load-bearing external citations (Author Year) + References at end of this section.
No internal module IDs or repo references.
Debate resonance: include a short 'Objections & Resolution' subsection.
Return Markdown only, no preamble.
"""

def _init_model():
    if not HAS_GENAI: return None
    key = os.getenv(API_KEY_ENV)
    if not key: return None
    genai.configure(api_key=key)
    return genai.GenerativeModel(MODEL)

def write_section(vessel_map_path: str, section_id: str, brief: str, shared_style: str = "") -> str:
    vm = json.loads(Path(vessel_map_path).read_text(encoding="utf-8"))
    sec = next((s for s in vm["sections"] if s["id"] == section_id), None)
    if not sec:
        raise ValueError(f"Unknown section id: {section_id}")
    model = _init_model()

    prompt = f"""{SYSTEM_DIRECTIVE}

PAPER MAP TITLE: {vm.get('title','(untitled)')}
TARGET SECTION: {sec['id']} — {sec['name']}
STYLE NOTES: {shared_style or vm.get('style','')}

TASK:
- Write 800–1200 words focused strictly on this section.
- Ensure formalism is fully specified (not essentialized): state equations, variables, units, invariants.
- Include a brief 'Objections & Resolution' subsection.
- End this section with a tiny 'References' list of 1–3 external, load-bearing anchors (DOIs/URLs welcome).

AUTHOR BRIEF (context for this section):
{brief}

BEGIN SECTION NOW:"""

    if model:
        resp = model.generate_content(prompt)
        text = getattr(resp, "text", "") or ""
    else:
        text = f"# {sec['id']}. {sec['name']}\n\n[offline stub] {brief}\n\n## Objections & Resolution\n- [offline] objection/response\n\n## References\n- [offline]"
    Path(OUT_DIR).mkdir(parents=True, exist_ok=True)
    fname = f"{sec['id']}__{uuid.uuid4().hex[:8]}.md"
    out = Path(OUT_DIR) / fname
    out.write_text(text, encoding="utf-8")
    return str(out)

def main():
    import argparse
    p = argparse.ArgumentParser(description="Write one manifesto section (consistent tone, strict placement).")
    p.add_argument("vessel_map", help="Path to section_map.json")
    p.add_argument("section_id", help="I, II, III, IV, V, VI, SYN, APP")
    p.add_argument("--brief", default="State the core ideas and formalism relevant to this section.")
    p.add_argument("--style", default="")
    args = p.parse_args()
    path = write_section(args.vessel_map, args.section_id, args.brief, shared_style=args.style)
    print(f"✅ Wrote section: {path}")

if __name__ == "__main__":
    main()
