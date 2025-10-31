#!/usr/bin/env python3
"""
dir_csv_masher.py — stream-safe directory "masher" for CSV/TSV files.

Features
- Recurse a root directory to find files by glob (e.g., *.csv, *.tsv, *.gz).
- Combine "many-to-one" (all into one file) or "per-directory" outputs.
- Union columns across heterogeneous files; missing values become NA.
- Stream in chunks to avoid OOM; optional row limit per file.
- Auto-detect delimiter (.csv -> ',', .tsv -> '\t') unless --sep provided.
- Infer compression from extension (.gz, .bz2, .xz) unless --compression provided.
- Add provenance columns: source_file, source_dir, source_basename.
- Optional regex capture groups to create additional columns from filenames/paths.
- Windows-friendly (uses pathlib + argparse).

Usage examples
--------------
# 1) Mash everything under Magnetics/ into one CSV
python dir_csv_masher.py -i "D:\Data\Magnetics" -o "D:\out\magnetics_all.csv" -p "*.csv" --recurse

# 2) Mash per-leaf directory (one output per directory)
python dir_csv_masher.py -i "D:\Data\Magnetics" --per-dir -p "*.csv" --recurse -O "D:\out"

# 3) Explicit separator and compression
python dir_csv_masher.py -i ./runs -o ./all.tsv --sep "\t"

# 4) Add run/shot columns from filename using regex
python dir_csv_masher.py -i ./Magnetics_E-935646-1 --recurse -p "*.csv" -o ./magnetics_E935646_all.csv \
  --extract "run:(?i)run[_\-]?(\d+)" --extract "shot:(?i)shot[_\-]?(\d+)"

"""
from __future__ import annotations
import argparse, sys, re
from pathlib import Path
from typing import Iterable, List, Dict, Optional
import pandas as pd

def infer_sep(path: Path, user_sep: Optional[str]) -> str:
    if user_sep is not None:
        return user_sep
    ext = path.suffix.lower()
    if ext == ".tsv":
        return "\t"
    # Default CSV
    return ","

def infer_compression(path: Path, user_comp: Optional[str]) -> Optional[str]:
    if user_comp is not None:
        return user_comp
    ext = path.suffix.lower()
    # pathlib only returns the last suffix, so also check full name
    name = path.name.lower()
    if name.endswith(".csv.gz") or name.endswith(".tsv.gz") or ext == ".gz":
        return "gzip"
    if name.endswith(".csv.bz2") or name.endswith(".tsv.bz2") or ext == ".bz2":
        return "bz2"
    if name.endswith(".csv.xz") or name.endswith(".tsv.xz") or ext == ".xz":
        return "xz"
    return None

def find_files(root: Path, pattern: str, recurse: bool) -> List[Path]:
    if recurse:
        return sorted([p for p in root.rglob(pattern) if p.is_file()])
    else:
        return sorted([p for p in root.glob(pattern) if p.is_file()])

def compile_extractors(specs: List[str]) -> List[re.Pattern]:
    # each spec form: "colname:regex"
    extractors = []
    for spec in specs:
        if ":" not in spec:
            raise ValueError(f"--extract spec must be 'colname:regex', got: {spec}")
        col, rgx = spec.split(":", 1)
        try:
            pat = re.compile(rgx)
        except re.error as e:
            raise ValueError(f"Bad regex for column '{col}': {e}")
        # store pattern object with a custom attribute
        pat._colname = col
        extractors.append(pat)
    return extractors

def extract_from_path(path: Path, extractors: List[re.Pattern]) -> Dict[str, str]:
    s = str(path.as_posix())
    out = {}
    for pat in extractors:
        m = pat.search(s)
        out[pat._colname] = m.group(1) if m else None
    return out

def read_chunked(path: Path, sep: str, compression: Optional[str], header: bool, encoding: str, 
                 nrows_per_chunk: int, provenance: Dict[str, str]) -> Iterable[pd.DataFrame]:
    # Try to read with pandas and stream chunks
    try:
        for chunk in pd.read_csv(
            path,
            sep=sep,
            compression=compression,
            encoding=encoding,
            chunksize=nrows_per_chunk,
            dtype=str,  # keep everything as string to unify schema easily
            on_bad_lines="skip"
        ):
            # add provenance cols
            for k, v in provenance.items():
                chunk[k] = v
            yield chunk
    except Exception as e:
        raise RuntimeError(f"Failed to read {path} — {e}")

def union_columns(order_ref: List[str], df: pd.DataFrame) -> List[str]:
    # Make a stable union (existing order_ref first, then new columns lexicographically)
    new_cols = [c for c in df.columns if c not in order_ref]
    return order_ref + sorted(new_cols)

def write_stream(out_path: Path, frames: Iterable[pd.DataFrame], header_written: bool, out_sep: str, out_encoding: str, mode: str = "a") -> bool:
    wrote_header = header_written
    for df in frames:
        # reorder columns stably across chunks
        if not wrote_header:
            col_order = list(df.columns)
            df.to_csv(out_path, sep=out_sep, index=False, encoding=out_encoding, mode="w")
            wrote_header = True
            col_order_ref = col_order
        else:
            # merge columns
            # df might have more columns; ensure union order
            # compute union
            col_order_ref = union_columns(list(col_order_ref), df)
            # align df to union (missing columns will be created by reindex)
            df = df.reindex(columns=col_order_ref)
            df.to_csv(out_path, sep=out_sep, index=False, encoding=out_encoding, mode=mode, header=False)
    return wrote_header

def mash_all_to_one(
    files: List[Path],
    out_path: Path,
    user_sep: Optional[str],
    compression: Optional[str],
    encoding: str,
    chunk_rows: int,
    extractors: List[re.Pattern]
):
    out_sep = user_sep if user_sep is not None else ","
    header_written = False
    col_order_ref = None  # captured via closure in write_stream

    # Local writer that keeps column order union across chunks and files
    def append_df(df: pd.DataFrame):
        nonlocal header_written, col_order_ref
        if not header_written:
            col_order_ref = list(df.columns)
            df.to_csv(out_path, sep=out_sep, index=False, encoding=encoding, mode="w")
            header_written = True
        else:
            # union-align
            col_order_ref = union_columns(list(col_order_ref), df)
            df = df.reindex(columns=col_order_ref)
            df.to_csv(out_path, sep=out_sep, index=False, encoding=encoding, mode="a", header=False)

    for f in files:
        sep = infer_sep(f, user_sep)
        comp = infer_compression(f, compression)
        prov = {
            "source_file": f.as_posix(),
            "source_dir": f.parent.as_posix(),
            "source_basename": f.name,
        }
        prov.update(extract_from_path(f, extractors) if extractors else {})
        try:
            for chunk in pd.read_csv(
                f,
                sep=sep,
                compression=comp,
                encoding=encoding,
                chunksize=chunk_rows,
                dtype=str,
                on_bad_lines="skip",
            ):
                for k, v in prov.items():
                    chunk[k] = v
                append_df(chunk)
        except Exception as e:
            print(f"[WARN] Skipping {f} due to read error: {e}", file=sys.stderr)

    print(f"[OK] Wrote combined file: {out_path}")

def mash_per_dir(
    files: List[Path],
    out_dir: Path,
    user_sep: Optional[str],
    compression: Optional[str],
    encoding: str,
    chunk_rows: int,
    extractors: List[re.Pattern]
):
    # Group by parent directory
    by_parent: Dict[Path, List[Path]] = {}
    for f in files:
        by_parent.setdefault(f.parent, []).append(f)

    for parent, flist in sorted(by_parent.items(), key=lambda kv: str(kv[0])):
        # derive output path
        safe_name = parent.name.replace(" ", "_")
        out_path = out_dir / f"{safe_name}_combined.csv" if user_sep is None or user_sep == "," else out_dir / f"{safe_name}_combined.tsv"
        out_path.parent.mkdir(parents=True, exist_ok=True)

        header_written = False
        col_order_ref = None

        def append_df(df: pd.DataFrame):
            nonlocal header_written, col_order_ref
            out_sep = "," if user_sep is None else user_sep
            if not header_written:
                col_order_ref = list(df.columns)
                df.to_csv(out_path, sep=out_sep, index=False, encoding=encoding, mode="w")
                header_written = True
            else:
                col_order_ref = union_columns(list(col_order_ref), df)
                df = df.reindex(columns=col_order_ref)
                df.to_csv(out_path, sep=out_sep, index=False, encoding=encoding, mode="a", header=False)

        for f in flist:
            sep = infer_sep(f, user_sep)
            comp = infer_compression(f, compression)
            prov = {
                "source_file": f.as_posix(),
                "source_dir": f.parent.as_posix(),
                "source_basename": f.name,
            }
            prov.update(extract_from_path(f, extractors) if extractors else {})
            try:
                for chunk in pd.read_csv(
                    f,
                    sep=sep,
                    compression=comp,
                    encoding=encoding,
                    chunksize=chunk_rows,
                    dtype=str,
                    on_bad_lines="skip",
                ):
                    for k, v in prov.items():
                        chunk[k] = v
                    append_df(chunk)
            except Exception as e:
                print(f"[WARN] Skipping {f} due to read error: {e}", file=sys.stderr)

        print(f"[OK] Wrote per-dir file: {out_path}")

def main():
    ap = argparse.ArgumentParser(description="Recurse a directory and mash many CSV/TSV files together safely.")
    ap.add_argument("-i", "--input", required=True, help="Input root directory")
    ap.add_argument("-p", "--pattern", default="*.csv", help="Glob pattern (e.g., *.csv, *.tsv, *.csv.gz). Default: *.csv")
    ap.add_argument("--recurse", action="store_true", help="Recurse under input")
    group = ap.add_mutually_exclusive_group(required=True)
    group.add_argument("-o", "--output", help="Single output file path (combine all into one)")
    group.add_argument("-O", "--output-dir", help="Output directory (one output per leaf directory)")
    ap.add_argument("--per-dir", action="store_true", help="Alias for using --output-dir with per-directory grouping")
    ap.add_argument("--sep", default=None, help="Output separator (default auto: ',' for .csv, '\\t' for .tsv).")
    ap.add_argument("--compression", default=None, help="Force input compression (gzip, bz2, xz). Default: infer from extension")
    ap.add_argument("--encoding", default="utf-8", help="Input and output text encoding. Default: utf-8")
    ap.add_argument("--chunksize", type=int, default=100_000, help="Rows per chunk when streaming. Default: 100k")
    ap.add_argument("--extract", action="append", default=[], help="Add a column from regex on full path, form 'colname:regex_with_group1'. Can repeat.")
    ap.add_argument("--dry-run", action="store_true", help="List files that would be processed and exit")
    args = ap.parse_args()

    root = Path(args.input).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        print(f"[ERROR] Input directory not found: {root}", file=sys.stderr)
        sys.exit(2)

    files = find_files(root, args.pattern, args.recurse)
    if len(files) == 0:
        print(f"[WARN] No files match pattern '{args.pattern}' under {root}", file=sys.stderr)
        sys.exit(1)

    # Extractors
    try:
        extractors = compile_extractors(args.extract) if args.extract else []
    except ValueError as e:
        print(f"[ERROR] {e}", file=sys.stderr)
        sys.exit(2)

    # Dry run
    if args.dry_run:
        print("[DRY-RUN] The following files would be processed:")
        for f in files:
            print(f" - {f.as_posix()}")
        print(f"[DRY-RUN] Count: {len(files)}")
        sys.exit(0)

    # Determine output mode
    if args.output_dir or args.per_dir:
        out_dir = Path(args.output_dir or ".").expanduser().resolve()
        out_dir.mkdir(parents=True, exist_ok=True)
        mash_per_dir(files, out_dir, args.sep, args.compression, args.encoding, args.chunksize, extractors)
    else:
        out_path = Path(args.output).expanduser().resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        mash_all_to_one(files, out_path, args.sep, args.compression, args.encoding, args.chunksize, extractors)

if __name__ == "__main__":
    main()
