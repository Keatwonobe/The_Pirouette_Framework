#!/usr/bin/env python3
"""
utils.py - Core utility functions for TLE combat runner
- Dice rolling
- Index parsing
- JSON directory loading
- Deep merge for overrides
"""

import os
import json
import random
import re

DICE_RE = re.compile(r"^(\d+)d(\d+)$")


def roll_amt(s):
    """
    Roll dice notation or return fixed value.
    '1d6' -> int, '2d4' -> int, '5' -> 5
    """
    if isinstance(s, (int, float)):
        return int(s)
    s = str(s)
    m = DICE_RE.match(s)
    if not m:
        return int(float(s))
    n, d = int(m.group(1)), int(m.group(2))
    return sum(random.randint(1, d) for _ in range(n))


def roll_dice(num_dice, num_sides):
    """Roll num_dice of num_sides each, return total"""
    return sum(random.randint(1, num_sides) for _ in range(num_dice))


def parse_index_tokens(tokens, max_len):
    """
    Parse index tokens like ['3', '5-8'] into 0-based indices.
    Returns sorted list of valid indices within [0, max_len).
    """
    indices = set()
    for tok in tokens:
        if "-" in tok:
            start_str, end_str = tok.split("-", 1)
            try:
                start = int(start_str) - 1
                end = int(end_str) - 1
            except ValueError:
                continue
            if start > end:
                start, end = end, start
            for i in range(start, end + 1):
                if 0 <= i < max_len:
                    indices.add(i)
        else:
            try:
                idx = int(tok) - 1
            except ValueError:
                continue
            if 0 <= idx < max_len:
                indices.add(idx)
    return sorted(indices)


def load_dir_as_map(path):
    """
    Load all .json files in a directory into a dict.
    Key is determined by id fields or filename.
    Warns on malformed files.
    """
    out = {}
    if not os.path.isdir(path):
        return out
    
    for fn in os.listdir(path):
        if not fn.endswith(".json"):
            continue
        full = os.path.join(path, fn)
        try:
            with open(full, "r") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[WARN] could not load JSON '{full}': {e}")
            continue

        key = (
            data.get("influence_id")
            or data.get("axis_id")
            or data.get("item_id")
            or data.get("spell_id")
            or fn
        )
        out[key] = data
    return out


def deep_merge(base: dict, override: dict):
    """
    Deep merge for item/spell overrides.
    Override values take precedence.
    """
    if not isinstance(override, dict):
        return override
    for k, v in override.items():
        if k in base and isinstance(base[k], dict) and isinstance(v, dict):
            base[k] = deep_merge(base[k], v)
        else:
            base[k] = v
    return base


def distance_2d(pos1, pos2):
    """Calculate 2D distance between two positions"""
    x1, y1 = pos1.get("x", 0), pos1.get("y", 0)
    x2, y2 = pos2.get("x", 0), pos2.get("y", 0)
    return ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5
