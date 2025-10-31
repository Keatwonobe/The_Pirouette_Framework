
import os
import re
import time
from pathlib import Path
from typing import List, Tuple

# Optional: external validation of DOIs/URLs (only if internet available)
try:
    import requests  # type: ignore
    HAS_REQUESTS = True
except Exception:
    HAS_REQUESTS = False

# --- CONFIGURATION ---
MODEL_NAME = "gemini-2.5-pro"
OUTPUT_DIR = "./grand_manifesto_out"
GRAND_FILENAME = "grand_manifesto.md"
API_KEY_ENV = "GOOGLE_API_KEY"

# How many manifestos to combine. If None, use all in folder.
MAX_MANIFESTOS = None

# --- MODEL SETUP ---
def _init_model():
    """
    Lazily import and configure google.generativeai to avoid hard dependency for static analysis.
    """
    try:
        import google.generativeai as genai  # type: ignore
    except Exception as e:
        raise RuntimeError("google-generativeai is required: pip install google-generativeai") from e
    api_key = os.getenv(API_KEY_ENV)
    if not api_key:
        raise RuntimeError(f"{API_KEY_ENV} not set in environment.")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(MODEL_NAME)


# --- I/O HELPERS ---
def read_manifestos(input_dir: str) -> List[str]:
    """
    Read .md files from a directory, sorted by name. Returns file texts.
    """
    p = Path(input_dir)
    if not p.exists() or not p.is_dir():
        raise FileNotFoundError(f"Manifesto directory not found: {input_dir}")
    files = sorted([f for f in p.glob("*.md")])
    if MAX_MANIFESTOS is not None:
        files = files[:MAX_MANIFESTOS]
    texts = []
    for f in files:
        try:
            texts.append(f.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"Warning: could not read {f}: {e}")
    if not texts:
        raise RuntimeError("No manifesto .md files found.")
    return texts


# --- PROMPT CONSTRUCTION ---
def build_grand_prompt(manifestos: List[str], title_hint: str = "A Time-First Unification"):
    """
    Construct the grand-manifesto prompt with strict guardrails:
      • No internal (Pirouette) citations.
      • Use external, minimal, authoritative references only where necessary.
      • Follow the canonical structure & debate resonance.
    """
    joined = "\n\n--- MANIFESTO SPLIT ---\n\n".join(manifestos)

    # Canonical structure with the "Identify → Math → Predict → Apply → Test → Reflect" flow
    # merged into the six-section manifesto skeleton.
    constraints = r"""
# GRAND MANIFESTO — AUTHORING CONSTRAINTS (READ CAREFULLY)

GOAL:
Write a single, self-contained Grand Manifesto that *stands on its own*.
It MAY explain that it is "a resonance-first, time-substrate theory,"
but it MUST NOT cite or reference internal Pirouette module IDs, files, or prior papers.

LENGTH:
30–100 pages (Markdown). Err on the side of clarity and density over verbosity.

STRUCTURE (merge both frames):
1) Identify Problem → Do Math → Make Predictions → Cross-Domain Applications → Design Experiments → Examine Philosophy
2) Map these to the following sections:
   I.   The Foundational Crisis
   II.  The Substrate Action
   III. Physics Predictions
   IV.  Cross-Domain Instantiation
   V.   Experimental Roadmap
   VI.  Philosophical Implications
Conclude with a succinct "Synthesis & Outlook" and a single blockquote capturing the ethos.

STYLE:
- Formal, precise, testable. Allow restrained poetic gravitas.
- Use first principles; re-derive as though for the first time.
- Do NOT appeal to authority. Claims must be supported by math, logic, or evidence.
- Use equations where necessary in inline/plain Markdown notation.

CITATIONS (CRITICAL):
- DO NOT cite any internal Pirouette module IDs or repository artifacts.
- Use **external** sources only where necessary to anchor claims, with in-text (Author Year) and a full References section.
- Prefer primary literature, major reviews, data releases. Include DOIs or URLs.
- Keep citations minimal and load-bearing; avoid padding with unrelated references.
- If a claim is novel here, say so and justify it logically without citation.

DEBATE RESONANCE:
- Surface the strongest counter-arguments to each major claim (steelman them).
- Resolve through derivation, constraints, or clear falsification criteria.
- Include an explicit "Red Team Appendix" enumerating decisive failure modes and how experiments would reveal them.

PHILOSOPHY / ETHICS:
- Address ontology (time-as-substrate), epistemology (measurement as deformation), and ethics (coherence vs. dark-residue).
- No mysticism or vague appeals; keep it rigorous and grounded.

CHECKLIST TO SATISFY BEFORE OUTPUT:
- [ ] No internal IDs like [DOMA-], [MATH-], [XAP-], etc.
- [ ] References are external and minimally sufficient.
- [ ] Equations are self-contained (symbols defined on first use).
- [ ] Clear falsifiability statements exist for *each* major prediction.
- [ ] Experimental designs have concrete instrumentation, signals, and thresholds.
- [ ] Final blockquote present.
"""

    # Provide the model with source material but demand independence from it.
    prompt = f"""
You are an expert scientific author and editor.

You will be given a set of manifestos derived from an unpublished framework.
Your task is to produce a single **Grand Manifesto** that is independent and self-contained,
following the constraints below. You must NOT reference internal module IDs or repo artifacts.

TITLE HINT: {title_hint}

{constraints}

### SOURCE MATERIAL (for understanding only; do NOT cite internally)
{joined}

### YOUR TASK
Write the complete Grand Manifesto now, in Markdown, obeying all constraints.
Begin with a strong title and an abstract (150–250 words).
"""
    return prompt


# --- POST-PROCESSING GUARDS ---
_INTERNAL_PATTERNS = [
    r"\[(?:DOMA|CORE|MATH|DYNA|XAP|XXP|XRI|COSMO|SECT|INST|PDM|TLE|SOCIO)[^]]*\]",
    r"\b(DOMA|CORE|MATH|DYNA|XAP|XXP|XRI|COSMO|SECT|INST|PDM|TLE|SOCIO)[-\u2010\u2011\u2012\u2013\u2014]?\d+",
]

def strip_internal_citations(text: str) -> Tuple[str, List[str]]:
    """
    Remove internal Pirouette-style references. Returns (clean_text, removed_snippets).
    """
    removed = []
    clean = text
    for pat in _INTERNAL_PATTERNS:
        for m in re.finditer(pat, clean):
            removed.append(m.group(0))
        clean = re.sub(pat, "", clean)
    # Collapse double spaces created by removals
    clean = re.sub(r"[ \t]{2,}", " ", clean)
    return clean, removed


# Optional: very light DOI/URL validation (best-effort)
_DOI_RE = re.compile(r"\b10\.\d{4,9}/[-._;()/:A-Za-z0-9]+\b")
_URL_RE = re.compile(r"https?://\S+")

def validate_references(text: str) -> dict:
    """
    Extract DOIs/URLs and (optionally) check they return 200.
    """
    dois = set(m.group(0) for m in _DOI_RE.finditer(text))
    urls = set(m.group(0) for m in _URL_RE.finditer(text))
    results = {"dois": {}, "urls": {}}
    if HAS_REQUESTS:
        for d in list(dois)[:25]:  # cap to be polite
            ok = False
            try:
                r = requests.head("https://doi.org/" + d, timeout=8)
                ok = (200 <= r.status_code < 400)
            except Exception:
                ok = False
            results["dois"][d] = ok
        for u in list(urls)[:25]:
            ok = False
            try:
                r = requests.head(u, timeout=8)
                ok = (200 <= r.status_code < 400)
            except Exception:
                ok = False
            results["urls"][u] = ok
    else:
        results["dois"] = {d: None for d in dois}
        results["urls"] = {u: None for u in urls}
    return results


# --- MAIN ORCHESTRATION ---
def synthesize_grand_manifesto(manifesto_dir: str, title_hint: str = "A Time-First Unification") -> Path:
    """
    Read manifestos from `manifesto_dir`, call the model with strong constraints, post-process
    to remove internal references, and save the final markdown.
    """
    model = _init_model()
    texts = read_manifestos(manifesto_dir)
    prompt = build_grand_prompt(texts, title_hint=title_hint)

    print("Calling model for Grand Manifesto synthesis...")
    start = time.time()
    response = model.generate_content(prompt)
    elapsed = time.time() - start
    print(f"Model call complete in {elapsed:.1f}s.")

    raw = getattr(response, "text", "") or ""
    if not raw.strip():
        raise RuntimeError("Empty response from model.")

    cleaned, removed = strip_internal_citations(raw)

    out_dir = Path(OUTPUT_DIR)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / GRAND_FILENAME

    # Append an autogenerated provenance footer
    footer = "\n\n---\n*Provenance:* Drafted via structured synthesis from prior manifestos. " \
             "This document is intentionally self-contained and cites only external sources where necessary.\n"

    (out_path).write_text(cleaned + footer, encoding="utf-8")
    print(f"✅ Grand Manifesto saved to: {out_path.resolve()}")

    if removed:
        removed_path = out_dir / "removed_internal_refs.log"
        removed_path.write_text("\n".join(removed), encoding="utf-8")
        print(f"ℹ️ Removed {len(removed)} internal references. Logged at: {removed_path.resolve()}")

    # Optional: check references
    refs = validate_references(cleaned)
    if any(v for v in refs["dois"].values()) or any(v for v in refs["urls"].values()):
        print("Reference check (best-effort):")
        for d, ok in refs["dois"].items():
            print(f"  DOI {d}: {'OK' if ok else 'Unknown/Fail'}")
        for u, ok in refs["urls"].items():
            print(f"  URL {u}: {'OK' if ok else 'Unknown/Fail'}")

    return out_path


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Synthesize a stand-alone Grand Manifesto with external citations only.")
    parser.add_argument("manifesto_dir", help="Directory containing ~10 manifesto .md files.")
    parser.add_argument("--title", default="A Time-First Unification", help="Optional title hint for the manifesto.")
    args = parser.parse_args()
    synthesize_grand_manifesto(args.manifesto_dir, title_hint=args.title)
