"""
DDE-Pirouette v7.3 — The Living Archive (Minified)
Distributed Database Ecosystem integrated with the Pirouette Framework

Philosophy: Data → Light → Memory → Truth → Coherence
License: CC-BY-SA-4.0 (Pirouette Framework)

This version adds minified manifest saving for extreme compression.
- `save_manifest_minified` creates an AI-readable, compact JSON.
- `load_manifest` is now "smart" and can read both minified and full JSONs.
"""
from __future__ import annotations
import numpy as np
import pandas as pd
from PIL import Image
import hashlib
import json
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Union, Any
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')


try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS not available. Install with: pip install faiss-cpu")


# ═══════════════════════════════════════════════════════════════════════════
#  MINIFICATION KEY MAP (The "Meta Dict")
# ═══════════════════════════════════════════════════════════════════════════
# This is the "atlas at the top" you described.
# It maps human-readable keys to tiny, compressed keys.

DDE_KEY_MAP = {
    # Top Level
    "version": "v",
    "created": "ct",
    "manifest": "m",
    "pirouette_registry": "pr", # This will be skipped in minified saves
    "coherence_history": "ch",
    "vocab": "vo",
    "reverse_vocab": "rv",
    
    # Manifest Entry
    "shape": "s",
    "columns": "c",
    "stats": "st",
    "checksum": "cs",
    "vocab_size": "vs",
    "image_size": "is",
    "pirouette": "pi",
    "dark_residue": "dr",
    
    # Stats
    "type": "t",
    "min": "mn",
    "max": "mx",
    "mean": "me",
    
    # Pirouette Metadata
    "module_id": "id",
    "parents": "p",
    "children": "ci",
    "engrams": "e",
    "domain": "d",
    "status": "ss",
    "gamma_profile": "gp",
    "temporal_adherence": "ta",
    "coherence_target": "ctt",
    "created_at": "cat",
    
    # Coherence History
    "timestamp": "ts",
    "avg_coherence": "ac",
    "avg_dark_residue": "adr",
    "coherence_dividend": "cd",
    "altruism_score": "as",
    "closure_reward": "cr",
    "tiles_healed": "th",
    
    # Glob Manifest (for stitch_atlas_v2.py)
    "atlas_file": "af",
    "tile_size": "tsize",
    "grid_dim": "gdim",
    "total_modules": "tm",
    "locations": "loc",
    "original_manifest": "om",
    "x": "x",
    "y": "y"
}

def _minify_keys_recursive(obj, key_map):
    """Recursively replaces keys in a dict/list with their minified versions."""
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            minified_key = key_map.get(k, k) # Get minified key, or keep original if not in map
            new_dict[minified_key] = _minify_keys_recursive(v, key_map)
        return new_dict
    elif isinstance(obj, list):
        return [_minify_keys_recursive(item, key_map) for item in obj]
    else:
        return obj # Return primitives (str, int, float, bool) as-is

def _rehydrate_keys_recursive(obj, reverse_key_map):
    """Recursively replaces minified keys with their original human-readable versions."""
    if isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            original_key = reverse_key_map.get(k, k) # Get original key, or keep if not in map
            new_dict[original_key] = _rehydrate_keys_recursive(v, reverse_key_map)
        return new_dict
    elif isinstance(obj, list):
        return [_rehydrate_keys_recursive(item, reverse_key_map) for item in obj]
    else:
        return obj # Primitives


# ═══════════════════════════════════════════════════════════════════════════
# PIROUETTE METADATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════

class PirouetteMetadata:
    """Pirouette-aware metadata for data ingestion."""
    def __init__(
        self,
        module_id: str = "DATA-UNKNOWN",
        parents: List[str] = None,
        children: List[str] = None,
        engrams: List[str] = None,
        domain: str = "DOMA",
        status: str = "draft",
        gamma_profile: str = "low",
        temporal_adherence: float = 0.8,
        coherence_target: float = 0.9,
        created_at: Optional[str] = None
    ):
        self.module_id = module_id
        self.parents = parents or []
        self.children = children or []
        self.engrams = engrams or []
        self.domain = domain
        self.status = status
        self.gamma_profile = gamma_profile
        self.temporal_adherence = temporal_adherence
        self.coherence_target = coherence_target
        self.created_at = created_at or datetime.now().isoformat()
        
    def to_dict(self) -> Dict:
        return {
            'module_id': self.module_id,
            'parents': self.parents,
            'children': self.children,
            'engrams': self.engrams,
            'domain': self.domain,
            'status': self.status,
            'gamma_profile': self.gamma_profile,
            'temporal_adherence': self.temporal_adherence,
            'coherence_target': self.coherence_target,
            'created_at': self.created_at
        }


# ═══════════════════════════════════════════════════════════════════════════
# UNIVERSAL CLOSURE ENGINE (INST-CLOSURE-001)
# ═══════════════════════════════════════════════════════════════════════════

class ClosureMetrics:
    """Metrics for monitoring convergence to geodesic"""
    def __init__(self, D: float, dD_dt: float, kappa: float, on_geodesic: bool):
        self.D = D
        self.dD_dt = dD_dt
        self.kappa = kappa
        self.on_geodesic = on_geodesic

class UniversalClosureEngine:
    """Domain-agnostic framework for learning dynamic equilibrium."""
    def __init__(
        self,
        gamma: float = 1.5,
        beta: float = 0.05,
        delta: float = 1.0,
        eta: float = 0.1,
        epsilon: float = 1e-3
    ):
        self.gamma = gamma
        self.beta = beta
        self.delta = delta
        self.eta = eta
        self.epsilon = epsilon
        
    def compute_curvature_scalar(self, residue_vector: np.ndarray) -> float:
        """Compute κ (curvature) from residue time series."""
        if len(residue_vector) < 2:
            return 0.0
        d2_D = np.diff(residue_vector, n=2)
        kappa = np.mean(np.abs(d2_D))
        return kappa
    
    def compute_closure_reward(
        self,
        D_current: float,
        D_previous: float,
        kappa: float
    ) -> float:
        """Universal reward structure for closure learning."""
        dD = D_current - D_previous
        coherence_gain = self.gamma * max(0, -dD)
        persistence = self.beta
        residue_penalty = self.delta * D_current
        curvature_penalty = self.eta * abs(kappa)
        reward = (
            coherence_gain 
            + persistence 
            - residue_penalty 
            - curvature_penalty
        )
        return reward

#----------------------------------------------------------------------
"""
Idea Manifold Surveyor for DDE-Pirouette
Adapts INST-AUTH-MAP-001 to the atlas format produced by the DDE run.
- scans the atlas
- detects conceptual voids
- emits Pirouette-ready module stubs
"""
#----------------------------------------------------------------------

class IdeaManifoldSurveyor:
    def __init__(
        self,
        atlas_json_path: str,
        min_residue: float = 0.0,
        max_residue: float = 1.0,
        neighbor_radius: int = 1,
    ):
        """
        atlas_json_path: path to your dde_glob_manifest_modules_outbox.json
        min_residue / max_residue: optional window if you want to focus on “hurting” zones
        neighbor_radius: how many tiles (von Neumann-ish) to check around each module
        """
        self.path = Path(atlas_json_path)
        self.min_residue = min_residue
        self.max_residue = max_residue
        self.neighbor_radius = neighbor_radius

        self.data = self._load_and_rehydrate()
        self.locations: Dict[str, Dict[str, int]] = self.data["locations"]
        self.tile_size: int = self.data["tile_size"]
        self.glb = self.data  # just a shorter alias

        # original manifest is where residue, vocab_size, etc. live
        self.original_manifest = self.data["original_manifest"]["manifest"]
        self.global_vocab = self.data["original_manifest"].get("vocab", [])

        # for convenience
        self.grid_dim = self.data["grid_dim"]

    def _load_and_rehydrate(self) -> dict:
        raw = json.loads(self.path.read_text())
        if "meta_map" in raw and "data" in raw:
            # same trick as your read_atlas.py
            meta_map = raw["meta_map"]
            reverse_key_map = {v: k for k, v in meta_map.items()}

            def rehydrate(obj):
                if isinstance(obj, dict):
                    return {reverse_key_map.get(k, k): rehydrate(v) for k, v in obj.items()}
                elif isinstance(obj, list):
                    return [rehydrate(x) for x in obj]
                else:
                    return obj

            return rehydrate(raw["data"])
        else:
            return raw

    # ------------------------------------------------------------------
    # 1) SURVEY
    # ------------------------------------------------------------------
    def survey(self) -> Dict[str, Any]:
        """
        Builds a simple view of: occupancy, residue field, and neighbor density.
        """
        grid_w = grid_h = self.grid_dim
        occupancy = np.zeros((grid_h, grid_w), dtype=int)
        residue_field = np.zeros((grid_h, grid_w), dtype=float)

        for module_id, loc in self.locations.items():
            x, y = loc["x"], loc["y"]
            occupancy[y, x] = 1
            mod = self.original_manifest.get(module_id, {})
            dr = float(mod.get("dr", 0.0))
            residue_field[y, x] = dr

        return {
            "occupancy": occupancy,
            "residue": residue_field,
        }

    # ------------------------------------------------------------------
    # 2) VOID DETECTION
    # ------------------------------------------------------------------
    def find_voids(
        self,
        min_neighbors: int = 2,
        shepherd_context: str | None = None,
        context_weight: float = 0.35,
    ) -> list[tuple[int, int, float]]:
        """
        A 'void' is:
          - an occupied module that has too few neighbors
          - or has high residue
        PLUS: if a shepherd_context is given, we bias toward modules whose
        ids/engrams/domains look closer to that context.

        returns list of (x, y, score)
        """
        survey = self.survey()
        occ = survey["occupancy"]
        resid = survey["residue"]
        H, W = occ.shape
        voids: list[tuple[int, int, float]] = []

        shepherd_context = (shepherd_context or "").lower().strip()

        for y in range(H):
            for x in range(W):
                if occ[y, x] == 0:
                    continue

                # base signals
                # -------------------------------------------------
                # neighbor count
                neigh = 0
                for dy in range(-self.neighbor_radius, self.neighbor_radius + 1):
                    for dx in range(-self.neighbor_radius, self.neighbor_radius + 1):
                        ny, nx = y + dy, x + dx
                        if ny < 0 or nx < 0 or ny >= H or nx >= W:
                            continue
                        if dy == 0 and dx == 0:
                            continue
                        if occ[ny, nx] == 1:
                            neigh += 1

                module_residue = float(resid[y, x])
                wants_help = module_residue > 0.42  # your old soft cutoff
                is_island = neigh < min_neighbors

                if not (wants_help or is_island):
                    # still could be context-relevant, so don't skip yet
                    pass

                # fetch module id/metadata for context sim
                module_id = None
                module_meta = {}
                for mid, loc in self.locations.items():
                    if loc["x"] == x and loc["y"] == y:
                        module_id = mid
                        module_meta = self.original_manifest.get(mid, {})
                        break

                # -------------------------------------------------
                # context match: cheap lexical similarity
                # -------------------------------------------------
                ctx_score = 0.0
                if shepherd_context and module_id:
                    mid_low = module_id.lower()
                    # 1) direct substring
                    if shepherd_context in mid_low:
                        ctx_score += 1.0
                    # 2) in domain
                    dom = str(module_meta.get("domain", "")).lower()
                    if shepherd_context in dom:
                        ctx_score += 0.6
                    # 3) in engrams
                    engrams = module_meta.get("engrams") or module_meta.get("engram") or []
                    for eg in engrams:
                        if shepherd_context in str(eg).lower():
                            ctx_score += 0.4
                            break

                # final score
                # base = residue + island penalty
                base_score = module_residue + (max(0, min_neighbors - neigh) * 0.05)
                # add context
                total_score = base_score + (ctx_score * context_weight)

                # don't emit totally irrelevant ones if context was given
                if shepherd_context and ctx_score == 0.0 and not (wants_help or is_island):
                    # skip: doesn't need help AND doesn't match context
                    continue

                voids.append((x, y, total_score))

        voids.sort(key=lambda t: t[2], reverse=True)
        return voids


    # ------------------------------------------------------------------
    # 3) EMIT MODULE STUBS
    # ------------------------------------------------------------------
    def make_stub_for_tile(self, x: int, y: int, rank: int = 0) -> Dict[str, Any]:
        """
        Emits a Pirouette-style module stub that DDE can ingest.
        It looks at whatever module is sitting at (x,y) and proposes a
        'BRIDGE' or 'CLOSURE' module near it.
        """
        # find the existing module at x,y
        existing_id = None
        for mid, loc in self.locations.items():
            if loc["x"] == x and loc["y"] == y:
                existing_id = mid
                break

        if existing_id is None:
            # pure void tile: we make a synthetic id
            base_id = f"AUTH-VOID-{x:02d}-{y:02d}"
            parent = None
        else:
            base_id = f"{existing_id}_AUTH-BRIDGE"
            parent = existing_id

        stub = {
            "id": base_id,
            "title": f"Idea Manifold Bridge near ({x},{y})",
            "version": "0.1-dde",
            "status": "draft",
            "parents": [parent] if parent else [],
            "children": [],
            "domain": "INST-AUTH-MAP",
            "engram": [
                "inst:auth-map-001",
                "inst:manifold-survey",
                f"origin:({x},{y})",
            ],
            "created_at": datetime.utcnow().isoformat(),
            "body": [
                "## Purpose",
                "Automatic bridge module emitted by DDE-Pirouette manifold survey.",
                "## Context",
                f"Located adjacent to atlas tile ({x},{y}); ranked {rank} by need.",
                "## Task",
                "Describe the missing connective tissue between this module and its neighbors.",
                "Define Γ/Ki deltas, expected temporal adherence, and closure style.",
            ],
        }
        return stub

    def run_survey_and_emit(self, top_k: int = 10) -> List[Dict[str, Any]]:
        voids = self.find_voids()
        stubs = []
        for i, (x, y, score) in enumerate(voids[:top_k]):
            stubs.append(self.make_stub_for_tile(x, y, rank=i))
        return stubs

# ═══════════════════════════════════════════════════════════════════════════
# MAIN DDE-PIROUETTE CLASS
# ═══════════════════════════════════════════════════════════════════════════

class DDEPirouette:
    """
    Distributed Database Ecosystem with full Pirouette integration.
    v7.3: Adds minified save/load and vocab priming.
    """
    
    def __init__(self, gamma: float = 2.2, patch_size: int = 8):
        self.gamma = gamma
        self.patch_size = patch_size
        self.manifest = {}
        self.vocab = {}
        self.reverse_vocab = {}
        
        self.index = None
        self.vector_manifest = {}
        self.dimension = None
        
        self.pirouette_registry = {}
        self.coherence_history = []
        
        self.closure_engine = UniversalClosureEngine()

    # ═══════════════════════════════════════════════════════════════════════
    # VOCABULARY PRIMING (v7.2)
    # ═══════════════════════════════════════════════════════════════════════

    def prime_vocabulary_from_file(self, file_path: str):
        """
        "Yoinks" words from a .txt file (one word per line)
        to build a master, pre-defined vocabulary.
        """
        print(f"🧬 Priming master vocabulary from: {file_path}")
        try:
            word_count = 0
            with open(file_path, 'r', encoding='utf-8') as f:
                for line in f:
                    word = line.strip()
                    if word and word not in self.vocab:
                        code = self._hash_token(word) 
                        self.vocab[word] = code
                        self.reverse_vocab[code] = word
                        word_count += 1
            
            print(f"   ✅ Primed with {word_count} master words.")
            print(f"   Total vocab size is now: {len(self.vocab)}")

        except FileNotFoundError:
            print(f"  ❌ WARNING: Master vocab file not found: {file_path}. Proceeding without it.")
        except Exception as e:
            print(f"  ❌ WARNING: Error loading master vocab: {e}. Proceeding without it.")

    # ═══════════════════════════════════════════════════════════════════════
    # CORE ENCODING/DECODING (ENG-DDE-001, 003, 005)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _hash_token(self, token: str) -> int:
        """Convert text to deterministic integer via SHA256."""
        h = int(hashlib.sha256(token.encode()).hexdigest()[:8], 16)
        return h % 16777216
    
    def _build_vocab(self, data: pd.DataFrame) -> None:
        """Learn the universe of unique tokens, adding to existing vocab."""
        tokens = set()
        for col in data.select_dtypes(include='object').columns:
            tokens.update(data[col].dropna().astype(str).unique())
        
        new_words = 0
        for token in sorted(tokens):
            if token not in self.vocab:
                code = self._hash_token(token)
                self.vocab[token] = code
                self.reverse_vocab[code] = token
                new_words += 1
        
        if new_words > 0:
            print(f"   Discovered {new_words} new words. Total vocab: {len(self.vocab)}")
    
    def _encode_value(self, val, col_stats: Dict) -> Tuple[int, int, int, int]:
        """Transform a single value into RGBA."""
        if pd.isna(val):
            return (0, 0, 0, 0)
        
        if isinstance(val, (int, float)):
            vmin, vmax = col_stats['min'], col_stats['max']
            if vmax == vmin:
                norm = 128
            else:
                log_val = np.log1p(abs(val - vmin))
                log_range = np.log1p(abs(vmax - vmin))
                norm = int(255 * (log_val / log_range if log_range > 0 else 0))
            
            sign = 255 if val >= 0 else 0
            return (norm, sign, 128, 255)
        else:
            # Use hash for all text, whether in vocab or not
            code = self.vocab.get(str(val), self._hash_token(str(val)))
            r = (code >> 16) & 0xFF
            g = (code >> 8) & 0xFF
            b = code & 0xFF
            return (r, g, b, 255)
    
    def _decode_pixel(self, rgba: Tuple[int, int, int, int], 
                      col_stats: Dict, is_numeric: bool) -> any:
        """Reverse RGBA → original value."""
        r, g, b, a = rgba
        
        if a == 0:
            return np.nan
        
        if is_numeric:
            vmin, vmax = col_stats['min'], col_stats['max']
            if vmax == vmin:
                return vmin
            
            log_range = np.log1p(abs(vmax - vmin))
            log_val = (r / 255) * log_range
            val = np.expm1(log_val) + vmin
            
            if g < 128:
                val = -abs(val)
            
            return val
        else:
            code = (r << 16) | (g << 8) | b
            # Use the reverse_vocab for full rehydration
            return self.reverse_vocab.get(code, f"<UNK:{code}>")
    
    def encode(
        self, 
        data: pd.DataFrame, 
        label: str = "dataset",
        pirouette_meta: Optional[PirouetteMetadata] = None
    ) -> Image.Image:
        """Encode DataFrame → RGBA Image with Pirouette governance."""
        print(f"🌱 Encoding {label}: {data.shape[0]} rows × {data.shape[1]} cols")
        
        if pirouette_meta is None:
            pirouette_meta = PirouetteMetadata(module_id=f"DATA-{label.upper()}")
        
        # This is redundant if ingest_pirouette_module is used, but safe
        self.pirouette_registry[label] = pirouette_meta
        
        self._build_vocab(data)
        
        stats = {}
        for col in data.columns:
            if pd.api.types.is_numeric_dtype(data[col]):
                stats[col] = {
                    'type': 'numeric',
                    'min': data[col].min(),
                    'max': data[col].max(),
                    'mean': data[col].mean()
                }
            else:
                stats[col] = {'type': 'text'}
        
        n_rows, n_cols = data.shape
        n_pixels = n_rows * n_cols
        side = int(np.ceil(np.sqrt(n_pixels)))
        
        img_array = np.zeros((side, side, 4), dtype=np.uint8)
        
        idx = 0
        for row_i in range(n_rows):
            for col_i in range(n_cols):
                if idx >= side * side:
                    break
                
                val = data.iloc[row_i, col_i]
                col_name = data.columns[col_i]
                rgba = self._encode_value(val, stats[col_name])
                
                y = idx // side
                x = idx % side
                img_array[y, x] = rgba
                idx += 1
        
        img_array_corrected = (img_array.astype(float) / 255) ** (1/self.gamma)
        img_array_corrected = (img_array_corrected * 255).astype(np.uint8)
        
        # Store manifest with Pirouette metadata
        checksum = hashlib.sha256(data.to_csv().encode()).hexdigest()
        self.manifest[label] = {
            'shape': data.shape,
            'columns': list(data.columns),
            'stats': stats,
            'checksum': checksum,
            'vocab_size': len(self.vocab),
            'image_size': side,
            'pirouette': pirouette_meta.to_dict()
        }
        
        img = Image.fromarray(img_array_corrected, mode='RGBA')
        
        print(f"✨ Compressed to {side}×{side} RGBA ({pirouette_meta.module_id})")
        print(f"📊 Γ Profile: {pirouette_meta.gamma_profile} | "
              f"T_a: {pirouette_meta.temporal_adherence:.2f}")
        
        return img
    
    def decode(self, img: Image.Image, label: str) -> pd.DataFrame:
        """Decode RGBA Image → DataFrame with provenance validation."""
        if label not in self.manifest:
            raise ValueError(f"No manifest found for '{label}'. Encode first.")
        
        manifest = self.manifest[label]
        print(f"🔍 Decoding {label}: {manifest['pirouette']['module_id']}")
        
        img_array = np.array(img, dtype=float)
        img_array = (img_array / 255) ** self.gamma
        img_array = (img_array * 255).astype(np.uint8)
        
        pixels = img_array.reshape(-1, 4)
        n_rows, n_cols = manifest['shape']
        columns = manifest['columns']
        stats = manifest['stats']
        
        data = []
        idx = 0
        for row_i in range(n_rows):
            row = []
            for col_i in range(n_cols):
                if idx >= len(pixels):
                    row.append(np.nan)
                else:
                    rgba = tuple(pixels[idx])
                    col_name = columns[col_i]
                    is_numeric = stats[col_name]['type'] == 'numeric'
                    val = self._decode_pixel(rgba, stats[col_name], is_numeric)
                    row.append(val)
                idx += 1
            data.append(row)
        
        df = pd.DataFrame(data, columns=columns)
        
        # Validate checksum
        reconstructed_hash = hashlib.sha256(df.to_csv().encode()).hexdigest()
        if reconstructed_hash == manifest['checksum']:
            print("✅ Perfect reconstruction: checksums match")
        else:
            print("⚠️  Warning: checksum mismatch (lossy compression)")
        
        return df
    
    def dark_residue(self, label: str, energy_kwh: float = 0.001) -> float:
        """Compute Dark Residue: ethical cost of encoding."""
        if label not in self.manifest:
            return float('inf')
        
        manifest = self.manifest[label]
        n_pixels = manifest['shape'][0] * manifest['shape'][1]
        img_pixels = manifest['image_size'] ** 2
        
        padding_loss = (img_pixels - n_pixels) / img_pixels
        
        energy_ref = 0.0001
        energy_cost = energy_kwh / energy_ref
        
        pirouette_meta = manifest['pirouette']
        gamma_penalty = {
            'low': 0.0,
            'medium': 0.1,
            'high': 0.3,
            'critical': 0.5
        }.get(pirouette_meta['gamma_profile'], 0.0)
        
        T_a = pirouette_meta['temporal_adherence']
        coherence_bonus = max(0, T_a - 0.5) * 0.2
        
        residue = (
            0.4 * energy_cost + 
            0.3 * padding_loss + 
            0.3 * gamma_penalty -
            coherence_bonus
        )
        
        print(f"🌑 Dark Residue ({label}): {residue:.6f}")
        print(f"   └─ Energy: {energy_cost:.4f}, Padding: {padding_loss:.4f}, "
              f"Γ: {gamma_penalty:.4f}, T_a bonus: -{coherence_bonus:.4f}")
        
        return max(0, residue)
    
    # ═══════════════════════════════════════════════════════════════════════
    # VECTORIZATION & RESONANCE (ENG-DDE-004)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _extract_patches(self, img: Image.Image) -> np.ndarray:
        """Extract patch features from image."""
        img_array = np.array(img)
        h, w, c = img_array.shape
        
        patches = []
        for y in range(0, h, self.patch_size):
            for x in range(0, w, self.patch_size):
                patch = img_array[y:y+self.patch_size, x:x+self.patch_size, :]
                
                if patch.shape[0] == 0 or patch.shape[1] == 0:
                    continue
                
                features = []
                for channel in range(c):
                    ch_data = patch[:, :, channel].flatten()
                    features.extend([
                        np.mean(ch_data),
                        np.var(ch_data),
                        np.percentile(ch_data, 25),
                        np.percentile(ch_data, 75)
                    ])
                
                patches.append(features)
        
        return np.array(patches, dtype=np.float32)
    
    def vectorize(self, img: Image.Image, label: str, 
                  metadata: Optional[Dict] = None) -> np.ndarray:
        """Transform RGBA → high-dimensional vectors with Pirouette context."""
        print(f"🔮 Vectorizing {label}...")
        
        vectors = self._extract_patches(img)
        
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vectors = vectors / norms
        
        if metadata is None:
            metadata = {}
        
        pirouette_meta = self.manifest.get(label, {}).get('pirouette', {})
        
        for i, vec in enumerate(vectors):
            vec_id = f"{label}_patch_{i}"
            self.vector_manifest[vec_id] = {
                'label': label,
                'patch_idx': i,
                'dark_residue': self.manifest.get(label, {}).get('dark_residue', 0.0),
                'module_id': pirouette_meta.get('module_id', 'UNKNOWN'),
                'domain': pirouette_meta.get('domain', 'DOMA'),
                'gamma_profile': pirouette_meta.get('gamma_profile', 'low'),
                **metadata
            }
        
        if self.dimension is None:
            self.dimension = vectors.shape[1]
        
        print(f"   └─ {len(vectors)} patches (d={self.dimension}) | "
              f"Domain: {pirouette_meta.get('domain', 'DOMA')}")
        
        return vectors
    
    def build_index(self, use_gpu: bool = False, n_clusters: int = 16):
        """Build FAISS index for resonance search."""
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not installed. Run: pip install faiss-cpu")
        
        if self.dimension is None:
            raise ValueError("No vectors to index. Run vectorize() first.")
        
        print(f"🏗️  Building FAISS index (d={self.dimension})...")
        
        quantizer = faiss.IndexFlatL2(self.dimension)
        
        if n_clusters > 1:
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, n_clusters)
            print(f"   └─ IVF with {n_clusters} clusters")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            print(f"   └─ Flat L2 index")
        
        if use_gpu and hasattr(faiss, 'StandardGpuResources'):
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)
            print("   └─ GPU acceleration enabled")
        
        print("✅ Index ready")
    
    def add_to_index(self, vectors: np.ndarray, train: bool = True):
        """Add vectors to index."""
        if self.index is None:
            raise ValueError("Build index first with build_index()")
        
        if train and hasattr(self.index, 'train'):
            if not self.index.is_trained:
                print("🎓 Training index...")
                self.index.train(vectors)
        
        self.index.add(vectors)
        print(f"➕ Added {len(vectors)} vectors (total: {self.index.ntotal})")
    
    def resonance_search(
        self, 
        query_img: Image.Image, 
        k: int = 10,
        dark_residue_threshold: Optional[float] = None,
        domain_filter: Optional[str] = None,
        alpha: float = 0.7, 
        beta: float = 0.2, 
        gamma: float = 0.1
    ) -> List[Dict]:
        """Resonance-weighted search with Pirouette governance."""
        if self.index is None or self.index.ntotal == 0:
            raise ValueError("Index is empty")
        
        print(f"🔍 Resonance search (k={k})")
        if domain_filter:
            print(f"   └─ Filtering domain: {domain_filter}")
        
        query_vectors = self._extract_patches(query_img)
        norms = np.linalg.norm(query_vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        query_vectors = query_vectors / norms
        
        query_vec = np.mean(query_vectors, axis=0, keepdims=True)
        
        distances, indices = self.index.search(query_vec, k * 3)
        
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:
                continue
            
            vec_ids = list(self.vector_manifest.keys())
            if idx >= len(vec_ids):
                continue
            
            vec_id = vec_ids[idx]
            meta = self.vector_manifest[vec_id]
            
            if dark_residue_threshold is not None:
                if meta.get('dark_residue', 0) > dark_residue_threshold:
                    continue
            
            if domain_filter is not None:
                if meta.get('domain', '') != domain_filter:
                    continue
            
            d_entropy = abs(meta.get('dark_residue', 0) - 0.5)
            d_provenance = 0.1
            d_eff = alpha * dist + beta * d_entropy + gamma * d_provenance
            resonance = 1.0 / (1.0 + d_eff)
            
            results.append({
                'vector_id': vec_id,
                'label': meta['label'],
                'module_id': meta.get('module_id', 'UNKNOWN'),
                'domain': meta.get('domain', 'DOMA'),
                'patch_idx': meta['patch_idx'],
                'resonance': float(resonance),
                'distance': float(dist),
                'dark_residue': meta.get('dark_residue', 0.0),
                'd_effective': float(d_eff)
            })
        
        results.sort(key=lambda x: x['resonance'], reverse=True)
        results = results[:k]
        
        if results:
            print(f"✨ Found {len(results)} matches")
            print(f"   └─ Best: {results[0]['module_id']} "
                  f"(resonance: {results[0]['resonance']:.4f})")
        
        return results
    
    def coherence_map(self) -> Dict[str, Dict]:
        """Compute coherence statistics with Pirouette domain awareness."""
        if self.index is None or self.index.ntotal == 0:
            return {}
        
        print("🌐 Computing coherence map...")
        
        label_groups = {}
        domain_groups = {}
        
        for vec_id, meta in self.vector_manifest.items():
            label = meta['label']
            domain = meta.get('domain', 'DOMA')
            
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(meta)
            
            if domain not in domain_groups:
                domain_groups[domain] = []
            domain_groups[domain].append(meta)
        
        coherence = {}
        
        for label, metas in label_groups.items():
            avg_residue = np.mean([m.get('dark_residue', 0) for m in metas])
            n_patches = len(metas)
            
            coherence[label] = {
                'n_patches': n_patches,
                'avg_dark_residue': float(avg_residue),
                'coherence_score': float(n_patches * (1.0 - avg_residue)),
                'domain': metas[0].get('domain', 'DOMA'),
                'module_id': metas[0].get('module_id', 'UNKNOWN')
            }
        
        coherence['_by_domain'] = {}
        for domain, metas in domain_groups.items():
            avg_residue = np.mean([m.get('dark_residue', 0) for m in metas])
            coherence['_by_domain'][domain] = {
                'n_vectors': len(metas),
                'avg_dark_residue': float(avg_residue),
                'coherence': float(1.0 - avg_residue)
            }
        
        print(f"   └─ Analyzed {len(label_groups)} datasets across "
              f"{len(domain_groups)} domains")
        
        return coherence
    
    # ═══════════════════════════════════════════════════════════════════════
    # AUTOPOIETIC LEARNING LOOP (ENG-DDE-007)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _compute_tile_health(self, vec_id: str) -> Dict[str, float]:
        """Assess tile health with Pirouette coherence metrics."""
        if vec_id not in self.vector_manifest:
            return {}
        
        meta = self.vector_manifest[vec_id]
        
        dark_res = meta.get('dark_residue', 0.5)
        resonance = 1.0 - dark_res
        
        gamma_profile = meta.get('gamma_profile', 'low')
        gamma_penalty = {
            'low': 0.0,
            'medium': 0.1,
            'high': 0.2,
            'critical': 0.4
        }.get(gamma_profile, 0.0)
        
        coherence = max(0, resonance - gamma_penalty)
        
        kappa = 0.0
        if hasattr(self, 'residue_history') and len(self.residue_history) > 2:
            kappa = self.closure_engine.compute_curvature_scalar(
                np.array(self.residue_history[-10:])
            )
        
        return {
            'resonance': resonance,
            'coherence': coherence,
            'dark_residue': dark_res,
            'kappa': kappa,
            'needs_healing': coherence < 0.7 or dark_res > 0.5
        }
    
    def sense(self) -> Dict[str, List[str]]:
        """Stage ①: Sense ecosystem state (Pirouette-aware)."""
        print("👁️  SENSE: Observing ecosystem with Pirouette lens...")
        
        healthy, degraded, critical = [], [], []
        
        for vec_id in self.vector_manifest:
            health = self._compute_tile_health(vec_id)
            
            if health.get('coherence', 0) > 0.8:
                healthy.append(vec_id)
            elif health.get('needs_healing', False):
                if health.get('dark_residue', 0) > 0.7:
                    critical.append(vec_id)
                else:
                    degraded.append(vec_id)
            else:
                healthy.append(vec_id)
        
        total = len(self.vector_manifest)
        print(f"   └─ {len(healthy)}/{total} healthy, "
              f"{len(degraded)} degraded, {len(critical)} critical")
        
        return {'healthy': healthy, 'degraded': degraded, 'critical': critical}
    
    def predict(self, state: Dict[str, List[str]]) -> List[Tuple[str, float]]:
        """Stage ②: Predict Coherence Dividend from healing."""
        print("🔮 PREDICT: Forecasting Coherence Dividend...")
        
        candidates = state['degraded'] + state['critical']
        predictions = []
        
        for vec_id in candidates:
            health = self._compute_tile_health(vec_id)
            
            current_coherence = health.get('coherence', 0)
            current_residue = health.get('dark_residue', 0)
            
            potential_coherence = 0.9
            potential_residue = current_residue * 0.4
            
            delta_coherence = potential_coherence - current_coherence
            delta_residue = current_residue - potential_residue
            
            coherence_dividend = delta_coherence + delta_residue
            predictions.append((vec_id, coherence_dividend))
        
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        if predictions:
            print(f"   └─ Top candidate: {predictions[0][0]} "
                  f"(Dividend: +{predictions[0][1]:.4f})")
        
        return predictions
    
    def select(self, predictions: List[Tuple[str, float]], 
               budget: float = 0.01) -> List[str]:
        """Stage ③: Select tiles within Dark Residue budget."""
        print(f"🎯 SELECT: Choosing tiles within budget ({budget:.4f})...")
        
        selected = []
        accumulated_cost = 0.0
        
        for vec_id, dividend in predictions:
            health = self._compute_tile_health(vec_id)
            cost = health.get('dark_residue', 0)
            
            if dividend > 0 and (accumulated_cost + cost) <= budget:
                selected.append(vec_id)
                accumulated_cost += cost
                if len(selected) >= 10: break
        
        print(f"   └─ Selected {len(selected)} tiles (Cost: {accumulated_cost:.6f} D)")
        return selected
    
    def reconstruct(self, vec_ids: List[str]) -> Dict[str, Dict]:
        """Stage ④: Heal selected tiles via coherence restoration."""
        print("🔧 RECONSTRUCT: Healing tiles with Pirouette guidance...")
        
        healed = {}
        for vec_id in vec_ids:
            if vec_id not in self.vector_manifest: continue
            
            meta = self.vector_manifest[vec_id]
            old_residue = meta.get('dark_residue', 0)
            
            gamma_profile = meta.get('gamma_profile', 'low')
            base_healing = {
                'low': 0.6, 'medium': 0.5, 'high': 0.4, 'critical': 0.3
            }.get(gamma_profile, 0.5)
            
            healing_factor = base_healing + np.random.uniform(-0.1, 0.1)
            new_residue = old_residue * (1 - healing_factor)
            
            meta['dark_residue'] = new_residue
            meta['healed'] = True
            meta['healing_factor'] = healing_factor
            
            new_coherence = 1.0 - new_residue
            old_coherence = 1.0 - old_residue
            
            healed[vec_id] = {
                'old_residue': old_residue,
                'new_residue': new_residue,
                'coherence_gain': new_coherence - old_coherence,
                'healing_factor': healing_factor
            }
            
            print(f"   ✨ {meta.get('module_id', vec_id)}: "
                  f"D {old_residue:.4f} → {new_residue:.4f} "
                  f"({healing_factor*100:.0f}% healing)")
        
        return healed
    
    def integrate(self, healed: Dict[str, Dict]) -> Dict[str, float]:
        """Stage ⑤: Integrate and compute Thermodynamic Altruism metrics."""
        print("🌊 INTEGRATE: Computing ecosystem effects...")
        
        all_residues = [m.get('dark_residue', 0) 
                       for m in self.vector_manifest.values()]
        
        avg_residue = np.mean(all_residues) if all_residues else 0
        avg_coherence = 1.0 - avg_residue
        
        total_dividend = sum(h['coherence_gain'] for h in healed.values())
        altruism_score = -np.sum([h['new_residue'] - h['old_residue'] 
                                  for h in healed.values()])
        
        closure_reward = 0.0
        if hasattr(self, 'last_avg_residue'):
            closure_reward = self.closure_engine.compute_closure_reward(
                avg_residue, self.last_avg_residue, kappa=0.0
            )
        self.last_avg_residue = avg_residue
        
        self.coherence_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'avg_coherence': avg_coherence,
            'avg_residue': avg_residue,
            'coherence_dividend': total_dividend,
            'altruism_score': altruism_score,
            'closure_reward': closure_reward,
            'tiles_healed': len(healed)
        })
        
        metrics = {
            'avg_coherence': avg_coherence,
            'avg_dark_residue': avg_residue,
            'coherence_dividend': total_dividend,
            'altruism_score': altruism_score,
            'closure_reward': closure_reward,
            'tiles_healed': len(healed)
        }
        
        print(f"   └─ Ecosystem Coherence: {avg_coherence:.4f} "
              f"| Dividend: +{total_dividend:.6f} "
              f"| Altruism: +{altruism_score:.6f}")
        
        return metrics
    
    def autopoietic_cycle(self, budget: float = 0.01, 
                          verbose: bool = True) -> Dict[str, float]:
        """Execute one complete autopoietic cycle."""
        if not verbose:
            import sys, io
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
        
        try:
            state = self.sense()
            predictions = self.predict(state)
            selected = self.select(predictions, budget=budget)
            healed = self.reconstruct(selected)
            metrics = self.integrate(healed)
            return metrics
        finally:
            if not verbose:
                sys.stdout = old_stdout
    
    def run_evolution(self, n_cycles: int = 5, 
                     budget_per_cycle: float = 0.01) -> pd.DataFrame:
        """Run autopoietic evolution with Pirouette governance."""
        print("=" * 70)
        print("🌱 AUTOPOIETIC EVOLUTION: Thermodynamic Altruism in Action")
        print("=" * 70)
        print()
        
        history = []
        for cycle in range(n_cycles):
            print(f"\n{'─' * 70}\nCYCLE {cycle + 1}/{n_cycles}\n{'─' * 70}")
            
            metrics = self.autopoietic_cycle(budget=budget_per_cycle)
            metrics['cycle'] = cycle + 1
            history.append(metrics)
            
            if metrics['coherence_dividend'] < 1e-6:
                print("\n✅ Dynamic equilibrium reached")
                break
        
        df = pd.DataFrame(history)
        
        print("\n" + "=" * 70 + "\nEVOLUTION COMPLETE\n" + "=" * 70)
        print("\n📊 Trajectory:")
        print(df[['cycle', 'avg_coherence', 'coherence_dividend', 
                  'altruism_score', 'closure_reward']].to_string(index=False))
        print()
        
        if len(history) > 0:
            final = history[-1]
            print(f"🎯 Final Coherence: {final['avg_coherence']:.4f}")
            print(f"🌑 Final Dark Residue: {final['avg_dark_residue']:.6f}")
            print(f"💎 Total Coherence Dividend: "
                  f"{sum(h['coherence_dividend'] for h in history):.6f}")
            print(f"❤️  Total Altruism Score: "
                  f"{sum(h['altruism_score'] for h in history):.6f}")
            print("\n✨ The ecosystem has learned to heal itself.")
        
        return df
    
    # ═══════════════════════════════════════════════════════════════════════
    # PIROUETTE MODULE INGESTION
    # ═══════════════════════════════════════════════════════════════════════
    
    def ingest_pirouette_module(
        self, 
        module_text: str,
        module_id: str,
        parents: List[str] = None,
        domain: str = "DOMA",
        gamma_profile: str = "medium"
    ) -> Image.Image:
        """Ingest a Pirouette module markdown → structured data → RGBA."""
        print(f"📥 INGESTING PIROUETTE MODULE: {module_id}")
        print(f"   Domain: {domain} | Γ Profile: {gamma_profile}")
        
        lines = module_text.split('\n')
        sections, current_section, section_name = [], [], "header"
        
        for line in lines:
            if line.startswith('##'):
                if current_section:
                    sections.append({
                        'section': section_name,
                        'content': '\n'.join(current_section)
                    })
                section_name = line.strip('#').strip()
                current_section = []
            else:
                current_section.append(line)
        
        if current_section:
            sections.append({
                'section': section_name,
                'content': '\n'.join(current_section)
            })
        
        df = pd.DataFrame(sections)
        
        meta = PirouetteMetadata(
            module_id=module_id,
            parents=parents or [],
            domain=domain,
            gamma_profile=gamma_profile,
            engrams=[f"module:{module_id.lower()}"]
        )
        
        # This will call _build_vocab, adding any new words
        img = self.encode(df, label=module_id, pirouette_meta=meta)
        
        print(f"✅ Module ingested and encoded")
        return img
    
    # ═══════════════════════════════════════════════════════════════════════
    # PERSISTENCE & GOVERNANCE (v7.3 - Minified)
    # ═══════════════════════════════════════════════════════════════════════
    
    def save_manifest(self, path: str = "dde_pirouette_manifest.json"):
        """Saves the full, human-readable manifest (bloated)."""
        manifest_data = {
            'version': '7.3-pirouette-full-vocab',
            'created': datetime.utcnow().isoformat(),
            'manifest': self.manifest,
            'pirouette_registry': {
                k: v.to_dict() if isinstance(v, PirouetteMetadata) else v
                for k, v in self.pirouette_registry.items()
            },
            'coherence_history': self.coherence_history[-100:],
            'vocab': self.vocab,
            'reverse_vocab': self.reverse_vocab
        }
        
        with open(path, 'w') as f:
            json.dump(manifest_data, f, indent=2, default=str)
        
        print(f"💾 FULL Pirouette manifest saved to {path}")

    def save_manifest_minified(self, path: str = "dde_pirouette_manifest.json"):
        """
        Saves a minified, AI-readable manifest.
        - Uses the DDE_KEY_MAP to compress keys.
        - Removes the redundant 'pirouette_registry'.
        - Saves in a compact, single-line format.
        """
        print(f"🗜️  Saving MINIFIED manifest to {path}...")
        
        # 1. Create the data blob *without* redundant registry
        data_to_save = {
            'version': '7.3-pirouette-minified',
            'created': datetime.utcnow().isoformat(),
            'manifest': self.manifest,
            'coherence_history': self.coherence_history[-100:],
            'vocab': self.vocab,
            'reverse_vocab': self.reverse_vocab
        }
        
        # 2. Recursively minify all keys
        minified_data = _minify_keys_recursive(data_to_save, DDE_KEY_MAP)
        
        # 3. Create the final "meta dict" structure
        output_json = {
            "meta_map": DDE_KEY_MAP,
            "data": minified_data
        }

        # 4. Save with compact separators for maximum smallness
        with open(path, 'w') as f:
            json.dump(output_json, f, separators=(',', ':'), default=str)
        
        print(f"   ✅ Minified manifest saved.")


    def load_manifest(self, path: str = "dde_pirouette_manifest.json"):
        """
        "Smart" loader: Can load both old (bloated) and new (minified)
        manifest formats.
        """
        with open(path, 'r') as f:
            raw_data = json.load(f)
        
        data = {}
        
        # Check if this is a new "minified" file
        if "meta_map" in raw_data and "data" in raw_data:
            print("🧬 Minified manifest detected. Rehydrating...")
            meta_map = raw_data['meta_map']
            # Create reverse map: {'m': 'manifest'} -> {'manifest': 'm'}
            reverse_key_map = {v: k for k, v in meta_map.items()}
            data = _rehydrate_keys_recursive(raw_data['data'], reverse_key_map)
            print("   ✅ Rehydration complete.")
        else:
            # Assume it's an old, bloated file
            print("🧬 Bloated (human-readable) manifest detected. Loading directly.")
            data = raw_data
        
        self.manifest = data.get('manifest', {})
        self.coherence_history = data.get('coherence_history', [])
        self.vocab = data.get('vocab', {})
        
        # CRITICAL: JSON saves int keys as strings. Must convert back.
        self.reverse_vocab = {
            int(k): v for k, v in data.get('reverse_vocab', {}).items()
        }
        
        # Load registry (if it exists) for backward compatibility
        self.pirouette_registry = {}
        for label, meta_dict in data.get('pirouette_registry', {}).items():
            meta = PirouetteMetadata(**meta_dict)
            self.pirouette_registry[label] = meta
            
        # Also ensure manifest 'pirouette' data is loaded into registry
        # This handles new minified files that omit the registry
        for label, man_data in self.manifest.items():
            if label not in self.pirouette_registry and 'pirouette' in man_data:
                meta = PirouetteMetadata(**man_data['pirouette'])
                self.pirouette_registry[label] = meta

        print(f"📂 Manifest loaded from {path}")
        print(f"   └─ {len(self.manifest)} datasets, "
              f"{len(self.coherence_history)} evolution cycles")
        print(f"   └─ Loaded {len(self.vocab)} vocab keys.")