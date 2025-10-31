#!/usr/bin/env python3
"""
ontology_to_code.py
Generate a minimal, typed Python library (pirouette_lib) from Pirouette dictionary .md entries.

Usage:
  python ontology_to_code.py --dict ./dictionary --out ./pirouette_lib
"""

import argparse, re, textwrap, keyword, string
from pathlib import Path
from datetime import datetime
import re
import yaml  # pip install pyyaml
from typing import List

# -------------------------------
# Helpers (now defined up-front)
# -------------------------------

HEADINGS = {
    "definition":   r"^#{1,6}\s+Definition\b",
    "operational":  r"^#{1,6}\s+(Operational\s+Definition|Operationalization|Operations)\b",
    "measurements": r"^#{1,6}\s+(Measurements?|Measures|Metrics|Quantification)\b",
    "constraints":  r"^#{1,6}\s+(Constraints?(?:\s+and\s+Falsifiers)?|Falsifiers|Tests?)\b",
    "mappings":     r"^#{1,6}\s+(Formal\s+Mappings?|Mappings?|Formalization)\b",
    "example":      r"^#{1,6}\s+(Example|Worked\s+Example|Example\s+Measurement|Usage)\b",
}

CID_OK = set(string.ascii_uppercase + string.digits + "_")

def parse_frontmatter_and_body(p: Path):
    raw = p.read_text(encoding="utf-8")
    if not raw.startswith("---"):
        return {}, raw
    try:
        _, rest = raw.split("\n", 1)
        fm_raw, body = rest.split("---", 1)
        fm = yaml.safe_load(fm_raw) or {}
        return fm, body.lstrip("\n")
    except Exception:
        return {}, raw

def parse_bullets(text: str) -> list[str]:
    items = []
    for line in (text or "").splitlines():
        m = re.match(r"\s*[-*+]\s+(.*)", line)
        if m:
            items.append(m.group(1).strip())
    return items

def extract_sections(md: str):
    sections = {}
    for key, pat in HEADINGS.items():
        m = re.search(pat, md, flags=re.I | re.M)
        if not m:
            continue
        start = m.end()
        nxt = re.search(r"^#{1,6}\s+", md[start:], flags=re.M)
        end = start + (nxt.start() if nxt else len(md[start:]))
        sections[key] = md[start:end].strip()
    return sections

def _clip(s: str, lim: int = 2000) -> str:
    if not s: return ""
    s = s.strip()
    return s[:lim] + ("\n... (trimmed)" if len(s) > lim else "")

def block(secs: dict, key: str) -> str:
    """Indent a section safely for embedding into a docstring."""
    return textwrap.indent(_clip(secs.get(key, "")), "        ")

def snake(name: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", (name or "").strip())
    s = re.sub(r"_+", "_", s).strip("_").lower()
    if not s or s[0].isdigit() or s in {".", "", "__init__"}:
        s = "_" + (s or "x")
    return s

def pascal(name: str) -> str:
    parts = [p for p in re.split(r"[^A-Za-z0-9]+", (name or "").strip()) if p]
    s = "".join(p.capitalize() for p in parts)
    if not s or s[0].isdigit() or keyword.iskeyword(s):
        s = "Term_" + (s or "X")
    return s

def is_valid_cid(cid: str) -> bool:
    if not cid or len(cid) < 3: return False
    return all(ch in CID_OK for ch in cid)

def sanitize_cid_from_term(term: str) -> str:
    cid = re.sub(r"[^A-Za-z0-9]+","_", (term or "").strip()).upper()
    cid = re.sub(r"_+","_", cid).strip("_")
    return cid or ("TERM_" + str(abs(hash(term)))[:6])

# Accept -, *, +, •, –, —, or numbered like 1. / 1)
BULLET_MARKER = re.compile(r"""
    ^\s*(                # leading space
        (?:[-*+•–—])     # bullet glyphs
        |                # or
        (?:\d+[.)])      # numbered bullets (1.  2) etc.)
    )\s+
""", re.VERBOSE)

CHECKBOX = re.compile(r"^\s*[-*+]\s*\[(?: |x|X)\]\s+")
CODE_FENCE = re.compile(r"^\s*```")

def parse_bullets_multiline(text: str) -> List[str]:
    """Parse bullets with many glyphs, checkboxes, and wrapped lines until the next bullet/blank/fence."""
    if not text:
        return []
    lines = text.splitlines()
    items, cur = [], []
    in_code = False

    for line in lines:
        if CODE_FENCE.match(line):
            in_code = not in_code
            if cur:  # flush current item before/after code blocks
                items.append(" ".join(cur).strip())
                cur = []
            continue

        if in_code:
            continue

        # normalize checkboxes as bullets
        if CHECKBOX.match(line):
            line = CHECKBOX.sub("- ", line)

        m = BULLET_MARKER.match(line)
        if m:
            # start a new item
            if cur:
                items.append(" ".join(cur).strip())
                cur = []
            cur.append(line[m.end():].strip())
        else:
            # continuation of current bullet if any, else ignore empty/spacing
            if cur:
                # stop accumulation on a blank line or new heading
                if not line.strip() or line.lstrip().startswith("#"):
                    items.append(" ".join(cur).strip())
                    cur = []
                else:
                    cur.append(line.strip())

    if cur:
        items.append(" ".join(cur).strip())

    # de-dup & drop empties
    items = [s for s in (x.strip() for x in items) if s]
    seen, out = set(), []
    for s in items:
        if s not in seen:
            out.append(s); seen.add(s)
    return out

# -------------------------------
# Templates (braces are escaped)
# -------------------------------

BASE_PY = """# Auto-generated base interfaces for pirouette_lib
from __future__ import annotations
from dataclasses import dataclass
from typing import Any, Callable, Dict, List, Optional, Protocol, TypedDict

class Context(TypedDict, total=False):
    data: Any
    params: Dict[str, Any]

@dataclass
class Measurement:
    name: str
    description: str
    compute: Callable[[Context], Any]

@dataclass
class Constraint:
    name: str
    description: str
    check: Callable[[Context], bool]

@dataclass
class Mapping:
    name: str
    description: str
    confidence: float
    transform: Optional[Callable[[Any], Any]] = None

class Term(Protocol):
    canonical_id: str
    symbol: str

    def measure(self, ctx: Context) -> List[Measurement]: ...
    def constraints(self) -> List[Constraint]: ...
    def mappings(self) -> List[Mapping]: ...
    def example(self) -> str: ...
"""

REGISTRY_PY = """# Auto-generated registry
from __future__ import annotations
from typing import Dict, Type, Any
from importlib import import_module

# Populated by generator:
_TERMS: Dict[str, str] = {{
{entries}
}}

_INST: Dict[str, Any] = {{}}

def get(cid: str):
    \"\"\"Return a class (not instance) for canonical id.\"\"\"
    modpath = _TERMS.get(cid.upper())
    if not modpath:
        raise KeyError("Unknown term: " + str(cid))
    mod_name, cls_name = modpath.rsplit(":", 1)
    mod = import_module(mod_name)
    return getattr(mod, cls_name)

def instantiate(cid: str, *args, **kwargs):
    cls = get(cid)
    inst = cls(*args, **kwargs)
    _INST[cid.upper()] = inst
    return inst

def known_terms() -> Dict[str, str]:
    return dict(_TERMS)
"""

EXPERIMENT_PY = """# Tiny runner to chain measures → mappings → constraints
from __future__ import annotations
from typing import List
from .base import Context
from . import registry

def run_chain(cids: List[str], ctx: Context) -> dict:
    out = {"chain": cids, "steps": []}
    for cid in cids:
        TermClass = registry.get(cid)
        term = TermClass()
        ms = term.measure(ctx)
        maps = term.mappings()
        cons = term.constraints()
        out["steps"].append({
            "cid": cid,
            "measurements": [m.name for m in ms],
            "mappings": [(m.name, m.confidence) for m in maps],
            "constraints": [c.name for c in cons],
        })
        # execute constraints (best-effort)
        checks = {c.name: bool(c.check(ctx)) for c in cons}
        out["steps"][-1]["checks"] = checks
    return out
"""

MODULE_TEMPLATE = '''"""
Auto-generated from dictionary entry: {cid}
Term: {term}
Symbol: {symbol}
Aliases: {aliases}

DEFINITION (summary)
{definition}

Auto-generated at {now}
"""
from __future__ import annotations
from typing import List
from .base import Term, Context, Measurement, Constraint, Mapping

def _strip(s: str) -> str:
    return "\\n".join(line.rstrip() for line in s.strip().splitlines()) if s else ""

class {class_name}(Term):
    canonical_id = "{cid}"
    symbol = {symbol_literal}

    def __init__(self):
        pass

    def measure(self, ctx: Context) -> List[Measurement]:
        """
        Derived from OPERATIONAL DEFINITION / MEASUREMENTS
        ---
{operational_block}
{measurements_block}
        """
        tasks: List[Measurement] = []
        # Baseline: ensure every term is exercised at least once.
        tasks.append(Measurement(
            name="{cid}:noop",
            description="No-op baseline measurement (replace with real measurement).",
            compute=lambda c: c.get("data")
        ))
        # Bullet-derived measurements (generated)
        MEASURE_BULLETS = {measure_bullets_literal}
        for i, desc in enumerate(MEASURE_BULLETS, 1):
            tasks.append(Measurement(
                name=f"{cid}:m{{i}}",
                description=desc,
                compute=lambda c: c.get("data")
            ))
        return tasks


    def constraints(self) -> List[Constraint]:
        """
        Derived from CONSTRAINTS / FALSIFIERS
        ---
{constraints_block}
        """
        checks: List[Constraint] = []

        def _always_true(ctx: Context) -> bool:
            # TODO: replace with falsifiable condition from constraints
            return True

        # Baseline: ensure every term contributes a check.
        checks.append(Constraint(
            name="{cid}:exists",
            description="Default truthy constraint (replace with domain falsifier).",
            check=_always_true
        ))
        # Bullet-derived constraints (generated)
        CONSTRAINT_BULLETS = {constraint_bullets_literal}
        for i, desc in enumerate(CONSTRAINT_BULLETS, 1):
            checks.append(Constraint(
                name=f"{cid}:c{{i}}",
                description=desc,
                check=_always_true
            ))
        return checks

    def mappings(self) -> List[Mapping]:
        """
        Derived from FORMAL MAPPINGS (candidates with confidence)
        ---
{mappings_block}
        """
        maps: List[Mapping] = []
        # You can populate confidence via parsed bullets later if desired.
        return maps


    def example(self) -> str:
        """
        Example usage (doctest-friendly).
        ---
{example_block}
        """
        return ">>> from pirouette_lib.{mod_name} import {class_name}\\n>>> # TODO: fill example"
'''



# -------------------------------
# Main
# -------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dict", required=True)
    ap.add_argument("--out", default="./pirouette_lib")
    args = ap.parse_args()

    src = Path(args.dict)
    out = Path(args.out)
    out.mkdir(parents=True, exist_ok=True)

    # base + experiment
    (out / "base.py").write_text(BASE_PY, encoding="utf-8")
    (out / "experiment.py").write_text(EXPERIMENT_PY, encoding="utf-8")

    bad_entries = []
    registry_entries = []
    seen_modules = set()
    seen_classes = set()
    seen_cids = set()

    for fp in sorted(src.glob("*.md")):
        fm, body = parse_frontmatter_and_body(fp)
        term = (fm.get("term") or fp.stem).strip()
        cid  = (fm.get("canonical_id") or "").strip()

        # Validate/repair CID
        if not is_valid_cid(cid):
            cid = sanitize_cid_from_term(term)
        if not is_valid_cid(cid):
            bad_entries.append((fp.name, "invalid_cid_after_sanitize", cid))
            continue

        if cid in seen_cids:
            bad_entries.append((fp.name, "duplicate_cid", cid))
            continue
        seen_cids.add(cid)

        symbol = (fm.get("symbol") or "").strip()
        aliases = fm.get("aliases") or []
        if isinstance(aliases, str):
            aliases = [a.strip() for a in aliases.split(",") if a.strip()]

        secs = extract_sections(body)
        mod_name = snake(cid)
        cls_name = pascal(cid)

        # Avoid collisions / weird names
        if mod_name in seen_modules:
            mod_name = f"{mod_name}_{len(seen_modules)}"
        seen_modules.add(mod_name)

        if cls_name in seen_classes:
            cls_name = f"{cls_name}_{len(seen_classes)}"
        seen_classes.add(cls_name)

        # ---------- BULLET EXTRACTION (always define literals) ----------
        # raw sections (unclipped)
        oper_text = secs.get("operational") or ""
        meas_text = secs.get("measurements") or ""
        cons_text = secs.get("constraints") or ""

        # parse multi-line bullets from sections
        meas_bullets = parse_bullets_multiline(oper_text + "\n" + meas_text)
        cons_bullets = parse_bullets_multiline(cons_text)

        # also include front-matter arrays, if any
        def fm_list(key):
            val = fm.get(key)
            if isinstance(val, list):
                return [str(x).strip() for x in val if str(x).strip()]
            return []

        meas_bullets.extend(fm_list("measurements"))
        cons_bullets.extend(fm_list("constraints"))

        # fallback: synthesize one item from first sentence if section has text but no bullets
        def first_sentence(s: str) -> str:
            s = (s or "").strip()
            if not s:
                return ""
            parts = re.split(r"(?<=[.?!])\s+|\n+", s, maxsplit=1)
            return parts[0].strip()

        if not meas_bullets and (oper_text or meas_text):
            fs = first_sentence(oper_text or meas_text)
            if fs:
                meas_bullets = [fs]

        if not cons_bullets and cons_text:
            fs = first_sentence(cons_text)
            if fs:
                cons_bullets = [fs]

        # ALWAYS define these literals (even if lists are empty)
        meas_bullets_lit = repr(meas_bullets)   # e.g., "['foo', 'bar']" or "[]"
        cons_bullets_lit = repr(cons_bullets)
        # ---------- /BULLET EXTRACTION ----------



        rendered = MODULE_TEMPLATE.format(
            cid=cid,
            term=term,
            symbol=symbol or "",
            symbol_literal=("''" if not symbol else repr(symbol)),
            aliases=", ".join(aliases),
            definition=_clip(secs.get("definition","(no definition)")),
            operational_block=block(secs, "operational"),
            measurements_block=block(secs, "measurements"),
            constraints_block=block(secs, "constraints"),
            mappings_block=block(secs, "mappings"),
            example_block=block(secs, "example"),
            has_operational=("True" if secs.get("operational") or secs.get("measurements") else "False"),
            has_constraints=("True" if secs.get("constraints") else "False"),
            has_mappings=("True" if secs.get("mappings") else "False"),
            class_name=cls_name,
            mod_name=mod_name,
            now=datetime.now().isoformat()+"Z",
            measure_bullets_literal=meas_bullets_lit,
            constraint_bullets_literal=cons_bullets_lit,
        )

        (out / f"{mod_name}.py").write_text(rendered, encoding="utf-8")
        registry_entries.append(f'    "{cid}": "pirouette_lib.{mod_name}:{cls_name}",')

    # registry + __init__
    registry_entries = sorted(set(registry_entries))
    reg_body = REGISTRY_PY.format(entries="\n".join(registry_entries))
    (out / "registry.py").write_text(reg_body, encoding="utf-8")
    (out / "__init__.py").write_text("from . import registry\nfrom .base import *\n", encoding="utf-8")

    if bad_entries:
        (out / "_GEN_WARNINGS.txt").write_text(
            "\n".join(f"{fn}\t{reason}\t{cid}" for fn,reason,cid in bad_entries),
            encoding="utf-8"
        )

    print(f"Generated pirouette_lib in {out.resolve()}")

if __name__ == "__main__":
    main()
