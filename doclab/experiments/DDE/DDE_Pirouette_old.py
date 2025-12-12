"""
DDE-Pirouette v7.0 — The Living Archive
Distributed Database Ecosystem integrated with the Pirouette Framework

Philosophy: Data → Light → Memory → Truth → Coherence
License: CC-BY-SA-4.0 (Pirouette Framework)

This implementation unifies:
- RGBA encoding (ENG-DDE-001/003)
- Vectorization & resonance (ENG-DDE-004)
- Autopoietic learning (ENG-DDE-007)
- Dark Residue ethics (ENG-DDE-008)
- Pirouette module governance (LAW-AUTOPOI-001)
"""

import numpy as np
import pandas as pd
from PIL import Image
import hashlib
import json
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Union
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
# PIROUETTE METADATA STRUCTURES
# ═══════════════════════════════════════════════════════════════════════════

class PirouetteMetadata:
    """
    Pirouette-aware metadata for data ingestion.
    Embeds framework governance into every data tile.
    """
    def __init__(
        self,
        module_id: str = "DATA-UNKNOWN",
        parents: List[str] = None,
        children: List[str] = None,
        engrams: List[str] = None,
        domain: str = "DOMA",
        status: str = "draft",
        gamma_profile: str = "low",  # low, medium, high, critical
        temporal_adherence: float = 0.8,
        coherence_target: float = 0.9
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
        self.created_at = datetime.utcnow().isoformat()
        
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
# Integrated for dynamic equilibrium detection
# ═══════════════════════════════════════════════════════════════════════════

class ClosureMetrics:
    """Metrics for monitoring convergence to geodesic"""
    def __init__(self, D: float, dD_dt: float, kappa: float, on_geodesic: bool):
        self.D = D
        self.dD_dt = dD_dt
        self.kappa = kappa
        self.on_geodesic = on_geodesic


class UniversalClosureEngine:
    """
    Domain-agnostic framework for learning dynamic equilibrium.
    Integrated from INST-CLOSURE-001 for DDE coherence monitoring.
    """
    
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
        """
        Compute κ (curvature) from residue time series.
        High κ = hard to maintain coherence.
        """
        if len(residue_vector) < 2:
            return 0.0
        
        # Second derivative approximation
        d2_D = np.diff(residue_vector, n=2)
        kappa = np.mean(np.abs(d2_D))
        
        return kappa
    
    def compute_closure_reward(
        self,
        D_current: float,
        D_previous: float,
        kappa: float
    ) -> float:
        """
        Universal reward structure for closure learning.
        Used to evaluate autopoietic healing quality.
        """
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


# ═══════════════════════════════════════════════════════════════════════════
# MAIN DDE-PIROUETTE CLASS
# ═══════════════════════════════════════════════════════════════════════════

class DDEPirouette:
    """
    Distributed Database Ecosystem with full Pirouette integration.
    
    This is time observing itself through data, governed by thermodynamic altruism.
    """
    
    def __init__(self, gamma: float = 2.2, patch_size: int = 8):
        self.gamma = gamma
        self.patch_size = patch_size
        self.manifest = {}
        self.vocab = {}
        self.reverse_vocab = {}
        
        # FAISS components
        self.index = None
        self.vector_manifest = {}
        self.dimension = None
        self.faiss_ids: List[str] = []  # row i in FAISS → this vec_id
        
        # Pirouette governance
        self.pirouette_registry = {}  # module_id → PirouetteMetadata
        self.coherence_history = []   # Tracks system-wide coherence over time
        self.residue_history = []   # track avg/system residue over time

        # Universal closure engine
        self.closure_engine = UniversalClosureEngine()
        
    # ═══════════════════════════════════════════════════════════════════════
    # CORE ENCODING/DECODING (ENG-DDE-001, 003, 005)
    # ═══════════════════════════════════════════════════════════════════════
    
    def _hash_token(self, token: str) -> int:
        """Convert text to deterministic integer via SHA256."""
        h = int(hashlib.sha256(token.encode()).hexdigest()[:8], 16)
        return h % 16777216
    
    def _build_vocab(self, data: pd.DataFrame) -> None:
        """Learn the universe of unique tokens."""
        tokens = set()
        for col in data.select_dtypes(include='object').columns:
            tokens.update(data[col].dropna().astype(str).unique())
        
        for i, token in enumerate(sorted(tokens)):
            code = self._hash_token(token)
            self.vocab[token] = code
            self.reverse_vocab[code] = token
    
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
            return self.reverse_vocab.get(code, f"<UNK:{code}>")
    
    def encode(
        self, 
        data: pd.DataFrame, 
        label: str = "dataset",
        pirouette_meta: Optional[PirouetteMetadata] = None
    ) -> Image.Image:
        """
        Encode DataFrame → RGBA Image with Pirouette governance.
        """
        print(f"🌱 Encoding {label}: {data.shape[0]} rows × {data.shape[1]} cols")
        
        # Register Pirouette metadata
        if pirouette_meta is None:
            pirouette_meta = PirouetteMetadata(module_id=f"DATA-{label.upper()}")
        
        self.pirouette_registry[label] = pirouette_meta
        
        # Build vocabulary
        self._build_vocab(data)
        
        # Compute statistics
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
        
        # Create RGBA array
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
        
        # Gamma correction (entropy balance)
        img_array = (img_array.astype(float) / 255) ** (1/self.gamma)
        img_array = (img_array * 255).astype(np.uint8)
        
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
        
        # immediately compute and store dark residue so vectorizer can read it
        residue = self.dark_residue(label)
        self.manifest[label]["dark_residue"] = residue

        img = Image.fromarray(img_array, mode='RGBA')
        
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
        
        # Reverse gamma correction
        img_array = np.array(img, dtype=float)
        img_array = (img_array / 255) ** self.gamma
        img_array = (img_array * 255).astype(np.uint8)
        
        # Decode pixels
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
        """
        Compute Dark Residue: ethical cost of encoding.
        Integrates with Pirouette's Γ and coherence metrics.
        """
        if label not in self.manifest:
            return float('inf')
        
        manifest = self.manifest[label]
        n_pixels = manifest['shape'][0] * manifest['shape'][1]
        img_pixels = manifest['image_size'] ** 2
        
        # Information loss from padding
        padding_loss = (img_pixels - n_pixels) / img_pixels
        
        # Energy cost normalized
        energy_ref = 0.0001
        energy_cost = energy_kwh / energy_ref
        
        # Γ penalty: higher gamma profiles increase residue
        pirouette_meta = manifest['pirouette']
        gamma_penalty = {
            'low': 0.0,
            'medium': 0.1,
            'high': 0.3,
            'critical': 0.5
        }.get(pirouette_meta['gamma_profile'], 0.0)
        
        # Temporal coherence bonus
        T_a = pirouette_meta['temporal_adherence']
        coherence_bonus = max(0, T_a - 0.5) * 0.2
        
        # Dark Residue formula (ENG-DDE-008)
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
        
        # Normalize
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        vectors = vectors / norms
        
        # Store with Pirouette metadata
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
        
        self.faiss_ids.append(vec_id)

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
        """
        Resonance-weighted search with Pirouette governance.
        Implements: d_eff = α·d_L2 + β·d_entropy + γ·d_provenance
        """
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
            
            if idx >= len(self.faiss_ids):
                continue
            vec_id = self.faiss_ids[idx]


            meta = self.vector_manifest[vec_id]
            
            # Apply filters
            if dark_residue_threshold is not None:
                if meta.get('dark_residue', 0) > dark_residue_threshold:
                    continue
            
            if domain_filter is not None:
                if meta.get('domain', '') != domain_filter:
                    continue
            
            # Resonance score
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
        
        # Per-dataset coherence
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
        
        # Per-domain aggregate
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
        
        # Base resonance
        dark_res = meta.get('dark_residue', 0.5)
        resonance = 1.0 - dark_res
        
        # Γ profile penalty
        gamma_profile = meta.get('gamma_profile', 'low')
        gamma_penalty = {
            'low': 0.0,
            'medium': 0.1,
            'high': 0.2,
            'critical': 0.4
        }.get(gamma_profile, 0.0)
        
        # Coherence with Γ adjustment
        coherence = max(0, resonance - gamma_penalty)
        
        # Universal closure curvature (if available)
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
        
        healthy = []
        degraded = []
        critical = []
        
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
        
        return {
            'healthy': healthy,
            'degraded': degraded,
            'critical': critical
        }
    
    def predict(self, state: Dict[str, List[str]]) -> List[Tuple[str, float]]:
        """Stage ②: Predict Coherence Dividend from healing."""
        print("🔮 PREDICT: Forecasting Coherence Dividend...")
        
        candidates = state['degraded'] + state['critical']
        predictions = []
        
        for vec_id in candidates:
            health = self._compute_tile_health(vec_id)
            
            current_coherence = health.get('coherence', 0)
            current_residue = health.get('dark_residue', 0)
            
            # Potential state after healing
            potential_coherence = 0.9
            potential_residue = current_residue * 0.4
            
            # Coherence Dividend (DOMA-042)
            delta_coherence = potential_coherence - current_coherence
            delta_residue = current_residue - potential_residue
            
            # Thermodynamic Altruism: ΔC_D = ΔC + ΔD_reduction
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
                
                if len(selected) >= 10:
                    break
        
        print(f"   └─ Selected {len(selected)} tiles")
        print(f"   └─ Total cost: {accumulated_cost:.6f} Dark Residue")
        
        return selected
    
    def reconstruct(self, vec_ids: List[str]) -> Dict[str, Dict]:
        """Stage ④: Heal selected tiles via coherence restoration."""
        print("🔧 RECONSTRUCT: Healing tiles with Pirouette guidance...")
        
        healed = {}
        
        for vec_id in vec_ids:
            if vec_id not in self.vector_manifest:
                continue
            
            meta = self.vector_manifest[vec_id]
            old_residue = meta.get('dark_residue', 0)
            
            # Healing factor depends on Γ profile
            gamma_profile = meta.get('gamma_profile', 'low')
            base_healing = {
                'low': 0.6,
                'medium': 0.5,
                'high': 0.4,
                'critical': 0.3
            }.get(gamma_profile, 0.5)
            
            healing_factor = base_healing + np.random.uniform(-0.1, 0.1)
            new_residue = old_residue * (1 - healing_factor)
            
            # Update metadata
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
        
        # Coherence Dividend (COHERENCE_DIVIDEND)
        total_dividend = sum(h['coherence_gain'] for h in healed.values())
        
        # Thermodynamic Altruism Score (ALTRUISM)
        altruism_score = -np.sum([h['new_residue'] - h['old_residue'] 
                                  for h in healed.values()])
        
        # Universal Closure reward

        # update residue history first
        self.residue_history.append(avg_residue)

        # compute curvature κ from last few residues
        if len(self.residue_history) > 2:
            kappa = self.closure_engine.compute_curvature_scalar(
                np.array(self.residue_history[-10:])  # last 10 steps is fine
            )
        else:
            kappa = 0.0

        if hasattr(self, 'last_avg_residue'):
            closure_reward = self.closure_engine.compute_closure_reward(
                avg_residue, 
                self.last_avg_residue,
                kappa=kappa  # Could track from history
            )
        else:
            closure_reward = 0.0
        
        self.last_avg_residue = avg_residue
        
        # Track history
        self.coherence_history.append({
            'timestamp': datetime.utcnow().isoformat(),
            'avg_coherence': avg_coherence,
            'avg_residue': avg_residue,
            'coherence_dividend': total_dividend,
            'altruism_score': altruism_score,
            'closure_reward': closure_reward
        })
        
        metrics = {
            'avg_coherence': avg_coherence,
            'avg_dark_residue': avg_residue,
            'coherence_dividend': total_dividend,
            'altruism_score': altruism_score,
            'closure_reward': closure_reward,
            'tiles_healed': len(healed)
        }
        
        print(f"   └─ Ecosystem Coherence: {avg_coherence:.4f}")
        print(f"   └─ Coherence Dividend: +{total_dividend:.6f}")
        print(f"   └─ Altruism Score: +{altruism_score:.6f}")
        print(f"   └─ Closure Reward: {closure_reward:.4f}")
        
        return metrics
    
    def autopoietic_cycle(self, budget: float = 0.01, 
                          verbose: bool = True) -> Dict[str, float]:
        """
        Execute one complete autopoietic cycle.
        Time observing itself through data.
        """
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
            print(f"\n{'─' * 70}")
            print(f"CYCLE {cycle + 1}/{n_cycles}")
            print(f"{'─' * 70}")
            
            metrics = self.autopoietic_cycle(budget=budget_per_cycle)
            metrics['cycle'] = cycle + 1
            history.append(metrics)
            
            # Check convergence (dynamic equilibrium)
            if metrics['coherence_dividend'] < 1e-6:
                print("\n✅ Dynamic equilibrium reached")
                break
        
        df = pd.DataFrame(history)
        
        print("\n" + "=" * 70)
        print("EVOLUTION COMPLETE")
        print("=" * 70)
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
            print()
            print("✨ The ecosystem has learned to heal itself.")
            print("   Time observed itself and chose coherence.")
        
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
        """
        Ingest a Pirouette module markdown → structured data → RGBA.
        
        This is the bridge between framework text and DDE substrate.
        """
        print(f"📥 INGESTING PIROUETTE MODULE: {module_id}")
        print(f"   Domain: {domain} | Γ Profile: {gamma_profile}")
        
        # try to read YAML-ish front matter
        front_meta = {}
        if module_text.lstrip().startswith("---"):
            parts = module_text.split("---", 2)
            if len(parts) >= 3:
                fm = parts[1]
                body = parts[2]
                for line in fm.splitlines():
                    if ":" in line:
                        k, v = line.split(":", 1)
                        front_meta[k.strip()] = v.strip()
                module_text = body  # continue with body only
        # allow front matter to override call-time args
        domain = front_meta.get("domain", domain)
        gamma_profile = front_meta.get("gamma_profile", gamma_profile)
        if "parents" in front_meta and isinstance(front_meta["parents"], str):
            parents = [p.strip() for p in front_meta["parents"].split(",")]

        # Parse module (simplified - real version would parse YAML frontmatter)
        lines = module_text.split('\n')
        
        # Extract key content
        sections = []
        current_section = []
        section_name = "header"
        
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
        
        # Convert to DataFrame
        df = pd.DataFrame(sections)
        
        # Create Pirouette metadata
        meta = PirouetteMetadata(
            module_id=module_id,
            parents=parents or [],
            domain=domain,
            gamma_profile=gamma_profile,
            engrams=[f"module:{module_id.lower()}"]
        )
        
        # Encode
        img = self.encode(df, label=module_id, pirouette_meta=meta)
        
        print(f"✅ Module ingested and encoded")
        
        return img
    
    # ═══════════════════════════════════════════════════════════════════════
    # PERSISTENCE & GOVERNANCE
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
                        # Use the same deterministic hash
                        code = self._hash_token(word) 
                        self.vocab[word] = code
                        self.reverse_vocab[code] = word
                        word_count += 1
            
            print(f"   ✅ Primed with {word_count} master words.")
            print(f"   Total vocab size is now: {len(self.vocab)}")
            
            # This flag tells the normal _build_vocab to
            # still add new words it finds, but to not
            # overwrite the ones we just primed.
            # (Our current logic already does this, but it's
            # good to be explicit)
            self.vocab_locked = False 

        except FileNotFoundError:
            print(f"  ❌ WARNING: Master vocab file not found: {file_path}. Proceeding without it.")
        except Exception as e:
            print(f"  ❌ WARNING: Error loading master vocab: {e}. Proceeding without it.")


    def save_manifest(self, path: str = "dde_pirouette_manifest.json"):
        """Save manifest with full Pirouette provenance AND full vocab."""
        manifest_data = {
            'version': '7.1-pirouette-full-vocab',
            'created': datetime.utcnow().isoformat(),
            'manifest': self.manifest,
            'pirouette_registry': {
                k: v.to_dict() if isinstance(v, PirouetteMetadata) else v
                for k, v in self.pirouette_registry.items()
            },
            'coherence_history': self.coherence_history[-100:],  # Last 100 cycles
            'vocab': self.vocab,  # <--- FULL VOCAB
            'reverse_vocab': self.reverse_vocab # <--- FULL REVERSE VOCAB
        }
        
        with open(path, 'w') as f:
            json.dump(manifest_data, f, indent=2, default=str)
        
        print(f"💾 Pirouette manifest (with FULL vocab) saved to {path}")

    def load_manifest(self, path: str = "dde_pirouette_manifest.json"):
        """Load manifest and restore Pirouette state."""
        with open(path, 'r') as f:
            data = json.load(f)
        
        self.manifest = data['manifest']
        self.coherence_history = data.get('coherence_history', [])
        self.vocab = data.get('vocab', {}) # <--- LOAD FULL VOCAB
        
        # CRITICAL: JSON saves int keys as strings. Must convert back.
        self.reverse_vocab = {
            int(k): v for k, v in data.get('reverse_vocab', {}).items()
        } # <--- LOAD & FIX REVERSE VOCAB
        
        # Restore Pirouette registry
        for label, meta_dict in data.get('pirouette_registry', {}).items():
            meta = PirouetteMetadata(**meta_dict)
            self.pirouette_registry[label] = meta
        
        print(f"📂 Manifest loaded from {path}")
        print(f"   └─ {len(self.manifest)} datasets, "
              f"{len(self.coherence_history)} evolution cycles")
        print(f"   └─ Loaded {len(self.vocab)} vocab keys.")


# ───────────────────────────────────────────────────────────
# Minimal API surface so AI / tools can talk to DDE-Pirouette
# ───────────────────────────────────────────────────────────
try:
    from fastapi import FastAPI
    from pydantic import BaseModel
    import uvicorn

    app = FastAPI(title="DDE-Pirouette")

    dde_instance = DDEPirouette()

    class IngestRequest(BaseModel):
        module_text: str
        module_id: str
        parents: list[str] | None = None
        domain: str = "DOMA"
        gamma_profile: str = "medium"

    @app.post("/ingest")
    def ingest_mod(req: IngestRequest):
        img = dde_instance.ingest_pirouette_module(
            req.module_text,
            req.module_id,
            parents=req.parents,
            domain=req.domain,
            gamma_profile=req.gamma_profile,
        )
        # immediately vectorize so it’s searchable
        vecs = dde_instance.vectorize(img, req.module_id)
        return {"status": "ok", "vectors": len(vecs)}

    class SearchRequest(BaseModel):
        module_id: str
        k: int = 10
        domain: str | None = None
        residue_max: float | None = None

    @app.post("/search")
    def search(req: SearchRequest):
        manifest = dde_instance.manifest.get(req.module_id)
        if manifest is None:
            return {"error": "module not found"}
        # rebuild img from disk or from encode step if you keep it around
        img_size = manifest["image_size"]
        # quick way: re-encode from decoded df
        df = dde_instance.decode(
            dde_instance.encode(
                pd.DataFrame([[0]]), "__tmp__"  # replace with your own storage
            ),
            "__tmp__",
        )

    # you can just run: uvicorn this_file:app --reload
except ImportError:
    # FastAPI not installed; ignore
    pass
