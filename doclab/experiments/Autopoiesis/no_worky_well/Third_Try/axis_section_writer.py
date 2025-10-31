import os, json, uuid, re, unicodedata
from pathlib import Path

try:
    import google.generativeai as genai  # type: ignore
    HAS_GENAI = True
except Exception:
    HAS_GENAI = False

MODEL = "gemini-2.5-pro"
API_KEY_ENV = "GOOGLE_API_KEY"

DEFAULT_OUT_DIR = "./concept_sections"

SYSTEM = """You are writing ONE focused micro-section for a larger manifesto.
Axis choices: Art, Law, Philosophy. Write ONLY from the assigned axis perspective.
- Art: metaphors, imagery, human salience; still precise and disciplined.
- Law: formalism, equations, definitions, falsifiable tests, external anchors.
- Philosophy: ontology/epistemology/ethics; tight, argument-driven; governance and Dark Residue awareness.
Tone: consistent across calls (formal, restrained poetic gravitas). Define symbols on first use.
Minimal, load-bearing external citations only; end with 1–3 references.
Include a short 'Objections & Resolution' at the end.
Markdown only.
"""

SYM_MAP = {
    "Γ":"Gamma","γ":"gamma","α":"alpha","Α":"Alpha","β":"beta","Β":"Beta","τ":"tau","Τ":"Tau",
    "μ":"mu","Μ":"Mu","κ":"kappa","Κ":"Kappa","λ":"lambda","Λ":"Lambda","ω":"omega","Ω":"Omega",
    "θ":"theta","Θ":"Theta","π":"pi","Π":"Pi",
}

def ascii_slug(s: str) -> str:
    for k,v in SYM_MAP.items():
        s = s.replace(k, v)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode("ascii")
    s = re.sub(r"[^A-Za-z0-9]+", "_", s).strip("_")
    return s or "concept"

def _init_model():
    if not HAS_GENAI: return None
    key = os.getenv(API_KEY_ENV)
    if not key: return None
    genai.configure(api_key=key)
    return genai.GenerativeModel(MODEL)

def write_axis_piece(concept_label: str, axis: str, context_snippets: str, section_hint: str, style: str, out_dir: str) -> str:
    model = _init_model()
    prompt = f"""{SYSTEM}

SECTION HINT: {section_hint}
AXIS: {axis}
CONCEPT: {concept_label}

LOCAL CONTEXT (snippets, do not cite internally):
{context_snippets}

TASK:
- 400–700 words.
- If AXIS=Law, include at least one equation and one falsifiable criterion.
- If AXIS=Philosophy, include an explicit governance implication (Dark Residue minimization).
- If AXIS=Art, maintain rigor; no mysticism; evoke with restraint.

Begin.
"""
    if model:
        resp = model.generate_content(prompt)
        text = getattr(resp,"text","") or ""
    else:
        text = f"### {axis}: {concept_label}\n\n[offline stub]\n\n**Objections & Resolution**\n- [offline]\n\n**References**\n- [offline]"
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    label_slug = ascii_slug(concept_label)
    axis_slug  = ascii_slug(axis)
    fname = f"{axis_slug}__{uuid.uuid4().hex[:8]}__{label_slug}.md"
    out = Path(out_dir)/fname
    out.write_text(text, encoding="utf-8")
    return str(out)

def main():
    import argparse, re
    p = argparse.ArgumentParser(description="Write Art/Law/Philosophy micro-sections for target concepts.")
    p.add_argument("graph_json", help="concept_graph.json")  # kept for symmetry (not required at runtime)
    p.add_argument("target_seed", help="target_seed.json (editable)")
    p.add_argument("--section_hint", default="Map this concept into the vessel section structure (I–VI, SYN, APP) as appropriate and write accordingly.")
    p.add_argument("--out", default=DEFAULT_OUT_DIR, help="Output directory for micro-sections")
    args = p.parse_args()

    seed  = json.loads(Path(args.target_seed).read_text(encoding="utf-8"))

    # optional: build context from local md files (best-effort)
    from glob import glob
    corpus = []
    for pat in ["*.md","paper_*.md","manifesto_*.md","grand_manifesto.md"]:
        for pth in glob(pat):
            try:
                corpus.append(Path(pth).read_text(encoding="utf-8"))
            except Exception:
                pass
    full_text = "\n\n".join(corpus)

    for sel in seed["selected_nodes"]:
        pat   = sel["pattern"]
        label = sel.get("label", pat)
        import re as _re
        snippets = _re.findall(rf"(.{{0,240}}{pat}.{{0,240}})", full_text, flags=_re.I|_re.S)
        ctx = "\n---\n".join(snippets[:5]) if snippets else "(no local context found)"
        for ax in sel["axis"]:
            path = write_axis_piece(label, ax, ctx, args.section_hint, seed.get("style",""), args.out)
            print(f"✅ Wrote: {path}")

if __name__=="__main__":
    main()
