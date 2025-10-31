# Tiny runner to chain measures → mappings → constraints
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
