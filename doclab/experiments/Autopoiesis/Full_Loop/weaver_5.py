#!/usr/bin/env python3
"""
author_v7_unified.py

Generalized Pirouette v7 authoring call.
Can talk to Gemini or OpenAI, and always feeds:
  - STUB
  - CONTEXT
into the same v7 module pattern.

Usage:
  python author_v7_unified.py --stub stub.md --context ctx.txt --out out.md --provider gemini
  python author_v7_unified.py --stub stub.md --context ctx.txt --out out.md --provider openai
"""

import os
import argparse
from pathlib import Path
from datetime import datetime
import time
import json
import traceback
import openai

# ---------- shared v7 instructions (from your weaver_4 lineage) ----------
INSTRUCTIONS = """
Your task is to act as the Pirouette Framework's core authoring intelligence.
You will expand a given STUB file into a full, canonical Pirouette v7 module.
You will be provided with the STUB and a CONTEXT blob containing essentialized definitions and dictionary terms.

You MUST generate a single, complete, valid markdown file.
You MUST NOT include any commentary outside the markdown file.
The file MUST follow this exact structure:

---
(Full YAML Header from STUB, fill in fields with relevant information)
---

## Law
- math-centric
- reference the Pirouette Lagrangian (𝓛_p) and its core components (Γ, Ki, Tₐ)
- address the 'Task' in the stub
- define Γ/Ki deltas if this is a bridge

## Philosophy
- explain the 'so what'
- keep the Pirouette voice

## Falsifiability Matrix
- at least two testable, quantitative criteria
- in list or table form

## Assemblé
- single, short, poetic line
"""

# ---------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------
def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def write_text(path: Path, text: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def build_prompt(stub: str, ctx: str) -> str:
    return f"""{INSTRUCTIONS}

---
## STUB
{stub}
---

---
## CONTEXT
{ctx}
---
"""


# ---------------------------------------------------------------------
# Gemini client
# ---------------------------------------------------------------------
def call_gemini(prompt: str, model_name: str = "gemini-2.5-pro"):
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))
    model = genai.GenerativeModel(model_name)
    gen_config = genai.GenerationConfig(
        temperature=0.35,
        top_p=0.9,
        top_k=40,
        max_output_tokens=4096,
    )
    try:
        resp = model.generate_content(prompt, generation_config=gen_config)
        return getattr(resp, "text", "").strip()
    except Exception as e:
        _dump_error("gemini_25pro_error", e)
        raise



# ---------------------------------------------------------------------
# OpenAI client
# ---------------------------------------------------------------------
def _dump_error(prefix: str, err: Exception):
    ts = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    fname = f"{prefix}_{ts}.log"
    with open(fname, "w", encoding="utf-8") as f:
        f.write("TYPE: " + prefix + "\n")
        f.write("TRACEBACK:\n")
        f.write("".join(traceback.format_exception(type(err), err, err.__traceback__)))
    print(f"[weaver_5] wrote error log to {fname}")

def _dump_response(prefix: str, resp_obj):
    ts = datetime.now().strftime("%Y%m%dT%H%M%SZ")
    fname = f"{prefix}_{ts}.json"
    try:
        with open(fname, "w", encoding="utf-8") as f:
            f.write(json.dumps(resp_obj.model_dump(), indent=2))
        print(f"[weaver_5] wrote response dump to {fname}")
    except Exception:
        # if model_dump isn't there, try plain json
        try:
            with open(fname, "w", encoding="utf-8") as f:
                f.write(json.dumps(resp_obj, indent=2))
            print(f"[weaver_5] wrote response dump to {fname}")
        except Exception:
            pass

def _extract_text_from_response(resp):
    # 1) newest SDKs often expose this:
    if hasattr(resp, "output_text") and resp.output_text:
        return resp.output_text.strip()

    collected = []

    # 2) walk the output list safely
    output = getattr(resp, "output", None)
    if output:
        for item in output:
            # item.content might be None, so guard it
            contents = getattr(item, "content", None)
            if not contents:
                continue
            for c in contents:
                # some SDKs use c.text, some use c["text"], some use type
                text = getattr(c, "text", None)
                if text:
                    collected.append(text)

    if collected:
        return "\n".join(t.strip() for t in collected if t.strip())

    # 3) nothing? return empty string; caller will have a dumped json beside it
    return ""

def call_openai(prompt: str, model: str = "gpt-5") -> str:
    client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    messages = [
        {
            "role": "system",
            "content": (
                "You are a Pirouette v7 author. Output ONLY markdown. "
                "Do NOT spend all tokens on internal reasoning. "
                "Follow the provided YAML header and section order."
                "Write the final module in under 1,000 tokens."
            ),
        },
        {"role": "user", "content": prompt},
    ]

    max_retries, delay = 4, 2
    for attempt in range(max_retries):
        try:
            resp = client.responses.create(
                model=model,
                input=messages,
                reasoning={"effort": "medium"},
                max_output_tokens=4000,
            )

            text = _extract_text_from_response(resp)
            if not text:
                # dump full response so we can inspect the exact shape
                _dump_response("openai_empty_output", resp)
                return "ERROR: OpenAI returned no text. See openai_empty_output_*.json"
            return text

        except Exception as e:
            _dump_error("openai_unknown", e)
            if attempt == max_retries - 1:
                raise
            time.sleep(delay)
            delay *= 2


# ---------------------------------------------------------------------
# main
# ---------------------------------------------------------------------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--stub", required=True, help="path to stub .md")
    ap.add_argument("--context", required=True, help="path to context .txt")
    ap.add_argument("--out", required=True, help="where to save authored module")
    ap.add_argument("--provider", choices=["gemini", "openai"], default="gemini")
    ap.add_argument("--openai-model", default="gpt-5")
    ap.add_argument("--gemini-model", default="gemini-2.5-pro")
    args = ap.parse_args()

    stub = read_text(Path(args.stub))
    ctx = read_text(Path(args.context))
    prompt = build_prompt(stub, ctx)

    if args.provider == "gemini":
        text = call_gemini(prompt, model_name=args.gemini_model)  # noqa
    else:
        text = call_openai(prompt, model=args.openai_model)

    write_text(Path(args.out), text)
    print(f"[author_v7] wrote {args.out}")


if __name__ == "__main__":
    main()
