#!/usr/bin/env python3
"""
compile_dictionary.py
Build a compact, machine-readable package of Pirouette dictionary entries.

Outputs:
  1) <out_prefix>.dictpack   # binary: MAGIC + header_len + header_json + gzipped bodies
  2) <out_prefix>.index.json # compact JSON index for quick review / CI diffs

Header JSON (in pack and in index.json) includes:
  - version, generated_at, counts
  - problems (missing fields, duplicates), symbol/alias collisions
  - entries: [{cid, term, symbol, aliases, prov_n, first_line, off, len, sha256}, ...]

Use:
  python compile_dictionary.py --dict ./dictionary --out_prefix ./dist/pirouette_dict

Notes:
  - Requires PyYAML (for frontmatter). If missing, install: pip install pyyaml
  - No schema validation here (kept minimal). You can add your JSON-schema pass upstream.
"""

import argparse, os, re, json, gzip, hashlib, struct, math
from pathlib import Path
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, Any, Tuple, List

try:
    import yaml
except Exception as e:
    raise SystemExit("Please `pip install pyyaml` (frontmatter parsing is required).")

MAGIC = b"PIRDICT1"   # 8 bytes
U64 = ">Q"            # big-endian uint64 for header length

# ---------- basic io ----------
def read_text(p: Path) -> str:
    return p.read_text(encoding="utf-8")

def write_text(p: Path, s: str):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(s, encoding="utf-8")

def write_bytes(p: Path, b: bytes):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(b)

# ---------- md helpers ----------
def parse_frontmatter_and_body(md_path: Path) -> Tuple[Dict[str, Any], str]:
    raw = read_text(md_path)

    # No frontmatter → return whole text as body
    if not raw.startswith("---"):
        return {}, raw

    # Split only on the first two '---'
    try:
        _, rest = raw.split("\n", 1)
        fm_raw, body = rest.split("---", 1)
        body = body.lstrip("\n")
    except ValueError:
        # malformed frontmatter fence → treat as body
        return {}, raw

    # First, try normal YAML
    try:
        fm = yaml.safe_load(fm_raw) or {}
        return fm, body
    except yaml.YAMLError:
        pass  # fall through to lenient pass

    # LENIENT PASS:
    # Convert any double-quoted scalar that contains a backslash into single-quoted.
    # Example: symbol: "(\mathcal{A}_{Ki})"  ->  symbol: '(\mathcal{A}_{Ki})'
    import re

    def _fix_backslashed_double_quotes(match: re.Match) -> str:
        key = match.group(1)
        val = match.group(2)
        # Single-quote escaping in YAML: '' means a literal '
        val_single = val.replace("'", "''")
        return f"{key}: '{val_single}'"

    # Only rewrite lines that look like   key: "value-with-\-in-it"
    fixed = re.sub(
        r'^([A-Za-z0-9_\-]+)\s*:\s*"([^"\n]*\\[^"\n]*)"\s*$',
        _fix_backslashed_double_quotes,
        fm_raw,
        flags=re.MULTILINE
    )

    # Try YAML again after the fix
    try:
        fm = yaml.safe_load(fixed) or {}
        return fm, body
    except yaml.YAMLError:
        # FINAL MINIMAL PARSER: best-effort key: value for the few fields we need
        fm_min: Dict[str, Any] = {}
        for line in fm_raw.splitlines():
            line = line.strip()
            if not line or line.startswith("#"): 
                continue
            if ":" not in line:
                continue
            k, v = line.split(":", 1)
            k = k.strip()
            v = v.strip().strip('"').strip("'")
            # crude list support for aliases/provenance if someone wrote [a, b]
            if v.startswith("[") and v.endswith("]"):
                try:
                    fm_min[k] = yaml.safe_load(v)
                except Exception:
                    fm_min[k] = [s.strip() for s in v[1:-1].split(",") if s.strip()]
            else:
                fm_min[k] = v
        return fm_min, body


def md_first_sentence(md: str, maxlen=180) -> str:
    t = strip_md(md)
    t = re.sub(r"\s+", " ", t).strip()
    return (t[:maxlen] + "…") if len(t) > maxlen else t

def strip_md(md: str) -> str:
    t = re.sub(r"`{1,3}[^`]+`{1,3}", " ", md)           # code spans
    t = re.sub(r"\[(.*?)\]\([^)]+\)", r"\1", t)         # links
    t = re.sub(r"[#>*_~\-]+", " ", t)                   # markup
    return t

def canon_id(s: str) -> str:
    s = re.sub(r"[^A-Za-z0-9]+", "_", s.strip())
    s = re.sub(r"_+", "_", s).strip("_")
    return s.upper()

# ---------- similarity (for optional stats) ----------
def name_similarity(a: str, b: str) -> float:
    import difflib
    return difflib.SequenceMatcher(a=a.lower(), b=b.lower()).ratio()

# ---------- main build ----------
def build_pack(dict_dir: Path) -> Tuple[Dict[str, Any], bytes]:
    problems: List[str] = []
    symbol_map = defaultdict(set)
    alias_map = defaultdict(set)
    entries_meta = []

    # collect entries
    md_files = sorted(dict_dir.glob("*.md"))
    seen_cid_paths: Dict[str, str] = {}
    bodies_bytes: List[bytes] = []
    offset = 0  # relative to start of blobs region

    for fp in md_files:
        fm, body = parse_frontmatter_and_body(fp)
        term = fm.get("term") or fp.stem
        cid  = fm.get("canonical_id") or canon_id(term)
        symbol = (fm.get("symbol") or "").strip()
        aliases = [a.strip() for a in (fm.get("aliases") or []) if a.strip()]
        prov = fm.get("provenance")
        if isinstance(prov, list):
            prov_n = len(prov)
        elif isinstance(prov, dict) and "sources" in prov:
            prov_n = len(prov.get("sources") or [])
        else:
            prov_n = 0

        if not term:
            problems.append(f"[{fp.name}] missing 'term'")
        if not cid:
            problems.append(f"[{fp.name}] missing 'canonical_id'")

        # duplicate cid
        if cid in seen_cid_paths and seen_cid_paths[cid] != str(fp):
            problems.append(f"[{fp.name}] duplicate canonical_id with {seen_cid_paths[cid]}: {cid}")
        seen_cid_paths[cid] = str(fp)

        if symbol:
            symbol_map[symbol].add(cid)
        for a in aliases:
            alias_map[a.lower()].add(cid)

        # compress body
        body_bytes = body.encode("utf-8")
        gz = gzip.compress(body_bytes, compresslevel=9)
        sha = hashlib.sha256(body_bytes).hexdigest()

        firstline = md_first_sentence(body)
        entries_meta.append({
            "cid": cid,
            "term": term,
            "symbol": symbol,
            "aliases": aliases,
            "prov_n": prov_n,
            "first_line": firstline,
            "off": offset,
            "len": len(gz),
            "sha256_body": sha,
            "file": fp.name
        })
        bodies_bytes.append(gz)
        offset += len(gz)

    # collisions
    symbol_collisions = {s: sorted(list(v)) for s, v in symbol_map.items() if len(v) > 1}
    alias_collisions  = {a: sorted(list(v)) for a, v in alias_map.items() if len(v) > 1}

    header = {
        "format": "pirouette-dictionary-pack",
        "format_version": "1.0",
        "generated_at": datetime.utcnow().isoformat() + "Z",
        "counts": {
            "files": len(md_files),
            "entries": len(entries_meta),
            "problems": len(problems),
            "symbol_collisions": len(symbol_collisions),
            "alias_collisions": len(alias_collisions),
        },
        "problems": problems,
        "symbol_collisions": symbol_collisions,
        "alias_collisions": alias_collisions,
        "entries": entries_meta,
    }

    # assemble binary: MAGIC + u64(header_len) + header_json + blobs
    header_json = json.dumps(header, ensure_ascii=False, separators=(",", ":")).encode("utf-8")
    blob = b"".join(bodies_bytes)
    pack = bytearray()
    pack += MAGIC
    pack += struct.pack(U64, len(header_json))
    pack += header_json
    pack += blob
    return header, bytes(pack)

# ---------- optional tiny reader (for consumers / tests) ----------
def load_pack(pack_path: Path) -> Tuple[Dict[str, Any], bytes, int]:
    data = pack_path.read_bytes()
    if data[:8] != MAGIC:
        raise ValueError("Bad magic in dictpack")
    hdr_len = struct.unpack(U64, data[8:16])[0]
    hdr_start = 16
    hdr_end = hdr_start + hdr_len
    header = json.loads(data[hdr_start:hdr_end].decode("utf-8"))
    blobs = data[hdr_end:]
    return header, blobs, hdr_end

def extract_entry(header: Dict[str, Any], blobs: bytes, cid: str) -> str:
    idx = {e["cid"]: e for e in header["entries"]}
    e = idx[cid]
    chunk = blobs[e["off"]: e["off"] + e["len"]]
    raw = gzip.decompress(chunk)
    return raw.decode("utf-8")

# ---------- cli ----------
def main():
    ap = argparse.ArgumentParser(description="Compile Pirouette dictionary into a compact pack + index JSON.")
    ap.add_argument("--dict", required=True, help="Directory with term .md files (frontmatter + body)")
    ap.add_argument("--out_prefix", required=True, help="Output prefix (e.g., ./dist/pirouette_dict)")
    ap.add_argument("--dry", action="store_true", help="Compute but do not write files")
    args = ap.parse_args()

    dict_dir = Path(args.dict)
    out_prefix = Path(args.out_prefix)
    out_prefix.parent.mkdir(parents=True, exist_ok=True)

    header, pack = build_pack(dict_dir)

    # write lightweight JSON index for quick review
    index_path = out_prefix.with_suffix(".index.json")
    pack_path  = out_prefix.with_suffix(".dictpack")

    if args.dry:
        print(json.dumps(header["counts"], indent=2))
        print(f"(dry) would write: {pack_path} ({len(pack)} bytes) and {index_path}")
        return

    write_text(index_path, json.dumps(header, ensure_ascii=False, indent=2))
    write_bytes(pack_path, pack)

    # quick summary to stdout
    print(f"Wrote: {pack_path} ({len(pack)} bytes)")
    print(f"Wrote: {index_path}")
    if header["counts"]["problems"] or header["counts"]["symbol_collisions"] or header["counts"]["alias_collisions"]:
        print("Warnings present — check index.json for details.")
    else:
        print("No problems detected.")

if __name__ == "__main__":
    main()
