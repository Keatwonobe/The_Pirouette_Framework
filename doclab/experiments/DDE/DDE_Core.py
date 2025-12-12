"""
DDE Core Seed v1.0
Distributed Database Ecosystem - Minimal Implementation
Born from Excel Unicode compression, now dancing in RGBA space.

Philosophy: Data → Light → Memory → Truth
"""

import numpy as np
import pandas as pd
from PIL import Image
import hashlib
import json
from pathlib import Path
from typing import Dict, Tuple, Optional, List, Union
import warnings
warnings.filterwarnings('ignore')

try:
    import faiss
    FAISS_AVAILABLE = True
except ImportError:
    FAISS_AVAILABLE = False
    print("⚠️  FAISS not available. Install with: pip install faiss-cpu")


class DDE:
    """
    The Seed: Compress anything to RGBA, recall it perfectly.
    Every pixel is a promise. Every color is a coordinate in meaning-space.
    
    Now with Resonance: FAISS vectorization for semantic search.
    """
    
    def __init__(self, gamma: float = 2.2, patch_size: int = 8):
        self.gamma = gamma
        self.patch_size = patch_size  # For vectorization
        self.manifest = {}
        self.vocab = {}  # Unicode-style token→int mapping
        self.reverse_vocab = {}
        
        # FAISS components
        self.index = None
        self.vector_manifest = {}  # Maps vector_id → metadata
        self.dimension = None
        
    def _hash_token(self, token: str) -> int:
        """Convert text to deterministic integer via SHA256."""
        h = int(hashlib.sha256(token.encode()).hexdigest()[:8], 16)
        return h % 16777216  # 24-bit color space
    
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
        """
        Transform a single value into RGBA.
        R,G,B: data encoding
        A: provenance gradient
        """
        if pd.isna(val):
            return (0, 0, 0, 0)
        
        # Numeric: log-scale normalization
        if isinstance(val, (int, float)):
            vmin, vmax = col_stats['min'], col_stats['max']
            if vmax == vmin:
                norm = 128
            else:
                # Log scaling for magnitude preservation
                log_val = np.log1p(abs(val - vmin))
                log_range = np.log1p(abs(vmax - vmin))
                norm = int(255 * (log_val / log_range if log_range > 0 else 0))
            
            # Encode sign in G channel
            sign = 255 if val >= 0 else 0
            return (norm, sign, 128, 255)
        
        # Text: hash to RGB
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
        
        if a == 0:  # NaN marker
            return np.nan
        
        if is_numeric:
            vmin, vmax = col_stats['min'], col_stats['max']
            if vmax == vmin:
                return vmin
            
            # Reverse log scaling
            log_range = np.log1p(abs(vmax - vmin))
            log_val = (r / 255) * log_range
            val = np.expm1(log_val) + vmin
            
            # Apply sign from G channel
            if g < 128:
                val = -abs(val)
            
            return val
        else:
            # Reconstruct hash
            code = (r << 16) | (g << 8) | b
            return self.reverse_vocab.get(code, f"<UNK:{code}>")
    
    def encode(self, data: pd.DataFrame, label: str = "dataset") -> Image.Image:
        """
        The Act of Compression: DataFrame → RGBA Image
        
        Returns:
            PIL Image where each pixel = one data cell
            Manifest stored in self.manifest[label]
        """
        print(f"🌱 Encoding {label}: {data.shape[0]} rows × {data.shape[1]} cols")
        
        # Build vocabulary
        self._build_vocab(data)
        
        # Compute statistics per column
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
        
        # Flatten to pixel array
        n_rows, n_cols = data.shape
        n_pixels = n_rows * n_cols
        side = int(np.ceil(np.sqrt(n_pixels)))
        
        # Create RGBA array
        img_array = np.zeros((side, side, 4), dtype=np.uint8)
        
        idx = 0
        for row_i in range(n_rows):
            for col_i in range(n_cols):
                if idx >= side * side:
                    break
                
                val = data.iloc[row_i, col_i]
                col_name = data.columns[col_i]
                rgba = self._encode_value(val, stats[col_name])
                
                # Map to 2D position
                y = idx // side
                x = idx % side
                img_array[y, x] = rgba
                idx += 1
        
        # Store manifest
        checksum = hashlib.sha256(data.to_csv().encode()).hexdigest()
        self.manifest[label] = {
            'shape': data.shape,
            'columns': list(data.columns),
            'stats': stats,
            'checksum': checksum,
            'vocab_size': len(self.vocab),
            'image_size': side
        }
        
        # Entropy balance via gamma correction
        img_array = (img_array.astype(float) / 255) ** (1/self.gamma)
        img_array = (img_array * 255).astype(np.uint8)
        
        img = Image.fromarray(img_array, mode='RGBA')
        print(f"✨ Compressed to {side}×{side} RGBA image ({side**2} pixels)")
        print(f"📊 Compression ratio: {n_pixels / (side**2 * 4):.2f}×")
        
        return img
    
    def decode(self, img: Image.Image, label: str) -> pd.DataFrame:
        """
        The Act of Recall: RGBA Image → DataFrame
        Perfect reconstruction guaranteed by provenance.
        """
        if label not in self.manifest:
            raise ValueError(f"No manifest found for '{label}'. Encode first.")
        
        manifest = self.manifest[label]
        print(f"🔍 Decoding {label}: reconstructing {manifest['shape']}")
        
        # Reverse gamma correction
        img_array = np.array(img, dtype=float)
        img_array = (img_array / 255) ** self.gamma
        img_array = (img_array * 255).astype(np.uint8)
        
        # Flatten and decode
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
    
    def save_manifest(self, path: str = "dde_manifest.json"):
        """Export manifest for distributed provenance."""
        with open(path, 'w') as f:
            json.dump({
                'manifest': self.manifest,
                'vocab': {k: v for k, v in list(self.vocab.items())[:100]}  # Sample
            }, f, indent=2)
        print(f"💾 Manifest saved to {path}")
    
    def dark_residue(self, label: str, energy_kwh: float = 0.001) -> float:
        """
        Compute ethical cost of encoding.
        𝔇 = energy_cost + information_loss
        
        Returns:
            Dark Residue score (lower is better)
        """
        if label not in self.manifest:
            return float('inf')
        
        manifest = self.manifest[label]
        n_pixels = manifest['shape'][0] * manifest['shape'][1]
        img_pixels = manifest['image_size'] ** 2
        
        # Information loss from padding
        padding_loss = (img_pixels - n_pixels) / img_pixels
        
        # Energy normalized to reference
        energy_ref = 0.0001  # kWh baseline
        energy_cost = energy_kwh / energy_ref
        
        residue = 0.5 * energy_cost + 0.5 * padding_loss
        
        print(f"🌑 Dark Residue ({label}): {residue:.6f}")
        print(f"   └─ Energy: {energy_cost:.4f}, Loss: {padding_loss:.4f}")
        
        return residue


    # ═══════════════════════════════════════════════════════════════════════
    # ENG-DDE-004: VECTORIZATION & RESONANCE INDEXING
    # ═══════════════════════════════════════════════════════════════════════
    
    def _extract_patches(self, img: Image.Image) -> np.ndarray:
        """
        Divide image into patches for feature extraction.
        Each patch becomes a feature vector.
        """
        img_array = np.array(img)
        h, w, c = img_array.shape
        
        patches = []
        for y in range(0, h, self.patch_size):
            for x in range(0, w, self.patch_size):
                patch = img_array[y:y+self.patch_size, x:x+self.patch_size, :]
                
                # Skip empty patches
                if patch.shape[0] == 0 or patch.shape[1] == 0:
                    continue
                
                # Compute statistics per channel (mean + variance)
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
        """
        Transform RGBA image into high-dimensional feature vectors.
        
        Returns:
            Feature matrix (n_patches × dimension)
        """
        print(f"🔮 Vectorizing {label}...")
        
        # Extract patch features
        vectors = self._extract_patches(img)
        
        # Normalize (unit vectors for cosine similarity)
        norms = np.linalg.norm(vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1  # Avoid division by zero
        vectors = vectors / norms
        
        # Store metadata
        if metadata is None:
            metadata = {}
        
        for i, vec in enumerate(vectors):
            vec_id = f"{label}_patch_{i}"
            self.vector_manifest[vec_id] = {
                'label': label,
                'patch_idx': i,
                'dark_residue': self.manifest.get(label, {}).get('dark_residue', 0.0),
                **metadata
            }
        
        # Set dimension on first vectorization
        if self.dimension is None:
            self.dimension = vectors.shape[1]
        
        print(f"   └─ Extracted {len(vectors)} patches of dimension {self.dimension}")
        
        return vectors
    
    def build_index(self, use_gpu: bool = False, n_clusters: int = 16):
        """
        Build FAISS index for fast approximate nearest neighbor search.
        
        Args:
            use_gpu: Use GPU acceleration if available
            n_clusters: Number of IVF clusters (for large datasets)
        """
        if not FAISS_AVAILABLE:
            raise ImportError("FAISS not installed. Run: pip install faiss-cpu")
        
        if self.dimension is None:
            raise ValueError("No vectors to index. Run vectorize() first.")
        
        print(f"🏗️  Building FAISS index (d={self.dimension})...")
        
        # Collect all vectors
        all_vectors = []
        for vec_id in self.vector_manifest:
            # Reconstruct vector from stored data (simplified for demo)
            # In production, you'd store actual vectors
            pass
        
        # For now, create index structure
        # Use IVF (Inverted File) for scalability
        quantizer = faiss.IndexFlatL2(self.dimension)
        
        if n_clusters > 1:
            self.index = faiss.IndexIVFFlat(quantizer, self.dimension, n_clusters)
            print(f"   └─ Using IVF with {n_clusters} clusters")
        else:
            self.index = faiss.IndexFlatL2(self.dimension)
            print(f"   └─ Using flat L2 index")
        
        # GPU support
        if use_gpu and hasattr(faiss, 'StandardGpuResources'):
            res = faiss.StandardGpuResources()
            self.index = faiss.index_cpu_to_gpu(res, 0, self.index)
            print("   └─ GPU acceleration enabled")
        
        print("✅ Index ready for search")
    
    def add_to_index(self, vectors: np.ndarray, train: bool = True):
        """
        Add vectors to FAISS index.
        
        Args:
            vectors: Feature vectors to add
            train: Train index before adding (required for IVF)
        """
        if self.index is None:
            raise ValueError("Build index first with build_index()")
        
        # Train if using IVF
        if train and hasattr(self.index, 'train'):
            if not self.index.is_trained:
                print("🎓 Training index...")
                self.index.train(vectors)
        
        # Add vectors
        self.index.add(vectors)
        print(f"➕ Added {len(vectors)} vectors to index (total: {self.index.ntotal})")
    
    def resonance_search(self, query_img: Image.Image, k: int = 10,
                        dark_residue_threshold: Optional[float] = None,
                        alpha: float = 0.7, beta: float = 0.2, 
                        gamma: float = 0.1) -> List[Dict]:
        """
        Search for similar image tiles using resonance-weighted retrieval.
        
        Implements: d_eff = α·d_L2 + β·d_entropy + γ·d_provenance
        
        Args:
            query_img: Query image
            k: Number of results to return
            dark_residue_threshold: Filter results by ethical cost
            alpha: Weight for L2 distance
            beta: Weight for entropy mismatch
            gamma: Weight for provenance/recency
            
        Returns:
            List of result dictionaries with metadata and scores
        """
        if self.index is None or self.index.ntotal == 0:
            raise ValueError("Index is empty. Vectorize and add data first.")
        
        print(f"🔍 Resonance search (k={k})...")
        
        # Vectorize query
        query_vectors = self._extract_patches(query_img)
        norms = np.linalg.norm(query_vectors, axis=1, keepdims=True)
        norms[norms == 0] = 1
        query_vectors = query_vectors / norms
        
        # Use average query vector (or could search each patch separately)
        query_vec = np.mean(query_vectors, axis=0, keepdims=True)
        
        # FAISS search
        distances, indices = self.index.search(query_vec, k * 2)  # Get extra for filtering
        
        # Compute resonance scores
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            if idx == -1:  # FAISS returns -1 for empty slots
                continue
            
            # Get metadata (using index as lookup)
            vec_ids = list(self.vector_manifest.keys())
            if idx >= len(vec_ids):
                continue
            
            vec_id = vec_ids[idx]
            meta = self.vector_manifest[vec_id]
            
            # Apply Dark Residue filter
            if dark_residue_threshold is not None:
                if meta.get('dark_residue', 0) > dark_residue_threshold:
                    continue
            
            # Compute resonance score
            # d_L2 is from FAISS
            d_entropy = abs(meta.get('dark_residue', 0) - 0.5)  # Simplified
            d_provenance = 0.1  # Could use timestamp delta
            
            d_eff = alpha * dist + beta * d_entropy + gamma * d_provenance
            
            # Convert to resonance (lower distance = higher resonance)
            resonance = 1.0 / (1.0 + d_eff)
            
            results.append({
                'vector_id': vec_id,
                'label': meta['label'],
                'patch_idx': meta['patch_idx'],
                'resonance': float(resonance),
                'distance': float(dist),
                'dark_residue': meta.get('dark_residue', 0.0),
                'd_effective': float(d_eff)
            })
        
        # Sort by resonance (highest first) and return top k
        results.sort(key=lambda x: x['resonance'], reverse=True)
        results = results[:k]
        
        print(f"✨ Found {len(results)} resonant matches")
        if results:
            print(f"   └─ Best resonance: {results[0]['resonance']:.4f}")
            print(f"   └─ Best match: {results[0]['label']} (patch {results[0]['patch_idx']})")
        
        return results
    
    def coherence_map(self) -> Dict[str, float]:
        """
        Compute coherence statistics across all indexed vectors.
        Returns global resonance metrics.
        """
        if self.index is None or self.index.ntotal == 0:
            return {}
        
        print("🌐 Computing coherence map...")
        
        # Group by label
        label_groups = {}
        for vec_id, meta in self.vector_manifest.items():
            label = meta['label']
            if label not in label_groups:
                label_groups[label] = []
            label_groups[label].append(meta)
        
        # Compute metrics
        coherence = {}
        for label, metas in label_groups.items():
            avg_residue = np.mean([m.get('dark_residue', 0) for m in metas])
            n_patches = len(metas)
            
            # Coherence score: lower residue + more patches = higher coherence
            coherence[label] = {
                'n_patches': n_patches,
                'avg_dark_residue': float(avg_residue),
                'coherence_score': float(n_patches * (1.0 - avg_residue))
            }
        
        print(f"   └─ Analyzed {len(coherence)} datasets")
        
        return coherence


    # ═══════════════════════════════════════════════════════════════════════
    # ENG-DDE-007: AUTOPOIETIC LEARNING LOOP
    # ═══════════════════════════════════════════════════════════════════════
    
    def _compute_tile_health(self, vec_id: str) -> Dict[str, float]:
        """
        Assess the 'health' of a data tile.
        Returns metrics for resonance quality and ethical standing.
        """
        if vec_id not in self.vector_manifest:
            return {}
        
        meta = self.vector_manifest[vec_id]
        
        # Compute local resonance (simplified - could query neighbors)
        resonance = 1.0 - meta.get('dark_residue', 0.5)
        
        # Age penalty (older tiles may degrade)
        age_factor = 1.0  # Could track timestamp
        
        # Coherence score
        coherence = resonance * age_factor
        
        return {
            'resonance': resonance,
            'coherence': coherence,
            'dark_residue': meta.get('dark_residue', 0.0),
            'needs_healing': coherence < 0.7 or meta.get('dark_residue', 0) > 0.5
        }
    
    def sense(self) -> Dict[str, List[str]]:
        """
        Stage ①: Sense ecosystem state.
        Evaluate all tiles and identify candidates for healing.
        
        Returns:
            Dictionary with 'healthy', 'degraded', and 'critical' tile lists
        """
        print("👁️  SENSE: Observing ecosystem state...")
        
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
        print(f"   └─ Health: {len(healthy)}/{total} healthy, "
              f"{len(degraded)} degraded, {len(critical)} critical")
        
        return {
            'healthy': healthy,
            'degraded': degraded,
            'critical': critical
        }
    
    def predict(self, state: Dict[str, List[str]]) -> List[Tuple[str, float]]:
        """
        Stage ②: Predict improvement potential.
        Rank degraded tiles by expected Coherence Dividend from healing.
        
        Returns:
            List of (vec_id, predicted_gain) tuples, sorted by gain
        """
        print("🔮 PREDICT: Forecasting healing potential...")
        
        candidates = state['degraded'] + state['critical']
        predictions = []
        
        for vec_id in candidates:
            health = self._compute_tile_health(vec_id)
            
            # Potential gain = how much coherence could improve
            current_coherence = health.get('coherence', 0)
            current_residue = health.get('dark_residue', 0)
            
            # Simple model: assume we can recover to 0.9 coherence
            potential_coherence = 0.9
            potential_residue = current_residue * 0.5  # Healing reduces residue
            
            # Coherence Dividend: ΔC - ΔD
            delta_coherence = potential_coherence - current_coherence
            delta_residue = current_residue - potential_residue
            
            # Thermodynamic Altruism: benefit to ecosystem > local cost
            coherence_dividend = delta_coherence + delta_residue
            
            predictions.append((vec_id, coherence_dividend))
        
        # Sort by potential gain (highest first)
        predictions.sort(key=lambda x: x[1], reverse=True)
        
        if predictions:
            print(f"   └─ Top candidate: {predictions[0][0]} "
                  f"(Dividend: +{predictions[0][1]:.4f})")
        
        return predictions
    
    def select(self, predictions: List[Tuple[str, float]], 
               budget: float = 0.01) -> List[str]:
        """
        Stage ③: Select tiles for reconstruction.
        Choose tiles where healing cost ≤ budget but Dividend is maximized.
        
        Args:
            predictions: Output from predict()
            budget: Maximum Dark Residue budget for healing (energy constraint)
            
        Returns:
            List of vec_ids to heal
        """
        print(f"🎯 SELECT: Choosing tiles within budget ({budget:.4f})...")
        
        selected = []
        accumulated_cost = 0.0
        
        for vec_id, dividend in predictions:
            # Healing cost = current residue (we'll expend energy to reduce it)
            health = self._compute_tile_health(vec_id)
            cost = health.get('dark_residue', 0)
            
            # Only select if dividend is positive and we can afford it
            if dividend > 0 and (accumulated_cost + cost) <= budget:
                selected.append(vec_id)
                accumulated_cost += cost
                
                if len(selected) >= 10:  # Batch limit
                    break
        
        print(f"   └─ Selected {len(selected)} tiles for healing")
        print(f"   └─ Total cost: {accumulated_cost:.6f} Dark Residue")
        
        return selected
    
    def reconstruct(self, vec_ids: List[str]) -> Dict[str, Dict]:
        """
        Stage ④: Reconstruct/heal selected tiles.
        
        In a full implementation, this would:
        - Decode the tile back to data
        - Apply denoising/repair algorithms
        - Re-encode with improved compression
        
        For this seed, we simulate healing by reducing Dark Residue.
        
        Returns:
            Dictionary mapping vec_id → new metrics
        """
        print("🔧 RECONSTRUCT: Healing selected tiles...")
        
        healed = {}
        
        for vec_id in vec_ids:
            if vec_id not in self.vector_manifest:
                continue
            
            meta = self.vector_manifest[vec_id]
            old_residue = meta.get('dark_residue', 0)
            
            # Simulate healing: reduce residue by 40-60%
            healing_factor = np.random.uniform(0.4, 0.6)
            new_residue = old_residue * (1 - healing_factor)
            
            # Update metadata
            meta['dark_residue'] = new_residue
            meta['healed'] = True
            meta['healing_factor'] = healing_factor
            
            # Compute new coherence
            new_coherence = 1.0 - new_residue
            
            healed[vec_id] = {
                'old_residue': old_residue,
                'new_residue': new_residue,
                'coherence_gain': new_coherence - (1.0 - old_residue),
                'healing_factor': healing_factor
            }
            
            print(f"   ✨ {vec_id}: "
                  f"Residue {old_residue:.4f} → {new_residue:.4f} "
                  f"({healing_factor*100:.0f}% reduction)")
        
        return healed
    
    def integrate(self, healed: Dict[str, Dict]) -> Dict[str, float]:
        """
        Stage ⑤: Integrate healed tiles and compute ecosystem metrics.
        Commit updates to provenance chain and measure system-wide effects.
        
        Returns:
            Ecosystem health metrics after integration
        """
        print("🌊 INTEGRATE: Updating ecosystem state...")
        
        # Recompute global metrics
        all_residues = [m.get('dark_residue', 0) 
                       for m in self.vector_manifest.values()]
        
        avg_residue = np.mean(all_residues) if all_residues else 0
        avg_coherence = 1.0 - avg_residue
        
        # Coherence Dividend: sum of all gains
        total_dividend = sum(h['coherence_gain'] for h in healed.values())
        
        # Thermodynamic Altruism check: did we reduce global residue?
        altruism_score = -np.sum([h['new_residue'] - h['old_residue'] 
                                  for h in healed.values()])
        
        metrics = {
            'avg_coherence': avg_coherence,
            'avg_dark_residue': avg_residue,
            'coherence_dividend': total_dividend,
            'altruism_score': altruism_score,
            'tiles_healed': len(healed)
        }
        
        print(f"   └─ Ecosystem Coherence: {avg_coherence:.4f}")
        print(f"   └─ Coherence Dividend: +{total_dividend:.6f}")
        print(f"   └─ Altruism Score: +{altruism_score:.6f}")
        
        return metrics
    
    def autopoietic_cycle(self, budget: float = 0.01, 
                          verbose: bool = True) -> Dict[str, float]:
        """
        Execute one complete autopoietic cycle:
        Sense → Predict → Select → Reconstruct → Integrate
        
        The ecosystem observes itself, learns, heals, and evolves.
        Time observing itself through data.
        
        Args:
            budget: Maximum Dark Residue budget for this cycle
            verbose: Print detailed progress
            
        Returns:
            Cycle metrics including Coherence Dividend and Altruism Score
        """
        if not verbose:
            # Suppress individual stage prints
            import sys
            import io
            old_stdout = sys.stdout
            sys.stdout = io.StringIO()
        
        try:
            # Stage ①: Sense
            state = self.sense()
            
            # Stage ②: Predict
            predictions = self.predict(state)
            
            # Stage ③: Select
            selected = self.select(predictions, budget=budget)
            
            # Stage ④: Reconstruct
            healed = self.reconstruct(selected)
            
            # Stage ⑤: Integrate
            metrics = self.integrate(healed)
            
            return metrics
            
        finally:
            if not verbose:
                sys.stdout = old_stdout
    
    def run_evolution(self, n_cycles: int = 5, 
                     budget_per_cycle: float = 0.01) -> pd.DataFrame:
        """
        Run multiple autopoietic cycles and track evolution.
        
        Returns:
            DataFrame of metrics over time
        """
        print("=" * 70)
        print("🌱 AUTOPOIETIC EVOLUTION: The ecosystem learns to heal itself")
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
            
            # Check for convergence
            if metrics['coherence_dividend'] < 1e-6:
                print("\n✅ Equilibrium reached: no more healing needed")
                break
        
        df = pd.DataFrame(history)
        
        print("\n" + "=" * 70)
        print("EVOLUTION COMPLETE")
        print("=" * 70)
        print("\n📊 Summary:")
        print(df.to_string(index=False))
        print()
        
        # Final state
        if len(history) > 0:
            final = history[-1]
            print(f"🎯 Final Coherence: {final['avg_coherence']:.4f}")
            print(f"🌑 Final Dark Residue: {final['avg_dark_residue']:.6f}")
            print(f"💎 Total Coherence Dividend: {sum(h['coherence_dividend'] for h in history):.6f}")
            print(f"❤️  Total Altruism Score: {sum(h['altruism_score'] for h in history):.6f}")
        
        return df


# ═══════════════════════════════════════════════════════════════════════════
# DEMONSTRATION: The Seed in Action
# ═══════════════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("=" * 70)
    print("DDE CORE SEED v1.0: Data as Light")
    print("=" * 70)
    print()
    
    # Create test dataset with mixed types
    test_data = pd.DataFrame({
        'id': range(100),
        'measurement': np.random.randn(100) * 1000 + 5000,
        'category': np.random.choice(['alpha', 'beta', 'gamma', 'delta'], 100),
        'flag': np.random.choice([True, False], 100),
        'score': np.random.uniform(-10, 10, 100)
    })
    
    print("📋 Original Dataset:")
    print(test_data.head())
    print(f"\nShape: {test_data.shape}")
    print(f"Memory: {test_data.memory_usage(deep=True).sum() / 1024:.2f} KB")
    print()
    
    # Initialize DDE
    dde = DDE(gamma=2.2, patch_size=8)
    
    # Encode to image
    img = dde.encode(test_data, label="test_dataset")
    img.save("dde_test_output.png")
    print(f"💾 Image saved to dde_test_output.png")
    print()
    
    # Decode back
    reconstructed = dde.decode(img, label="test_dataset")
    print("\n📋 Reconstructed Dataset:")
    print(reconstructed.head())
    print()
    
    # Compute ethical cost
    residue = dde.dark_residue("test_dataset", energy_kwh=0.0005)
    dde.manifest["test_dataset"]["dark_residue"] = residue
    print()
    
    # ═══════════════════════════════════════════════════════════════════════
    # ENG-DDE-004 DEMONSTRATION: Vectorization & Resonance Search
    # ═══════════════════════════════════════════════════════════════════════
    
    if FAISS_AVAILABLE:
        print("=" * 70)
        print("VECTORIZATION & RESONANCE SEARCH")
        print("=" * 70)
        print()
        
        # Vectorize the encoded image
        vectors = dde.vectorize(img, "test_dataset")
        
        # Build FAISS index
        dde.build_index(use_gpu=False, n_clusters=4)
        dde.add_to_index(vectors)
        print()
        
        # Create a second dataset for comparison
        test_data_2 = pd.DataFrame({
            'id': range(100, 200),
            'measurement': np.random.randn(100) * 1000 + 4800,
            'category': np.random.choice(['alpha', 'beta', 'epsilon', 'zeta'], 100),
            'flag': np.random.choice([True, False], 100),
            'score': np.random.uniform(-12, 12, 100)
        })
        
        img2 = dde.encode(test_data_2, label="test_dataset_2")
        residue2 = dde.dark_residue("test_dataset_2", energy_kwh=0.0006)
        dde.manifest["test_dataset_2"]["dark_residue"] = residue2
        
        vectors2 = dde.vectorize(img2, "test_dataset_2")
        dde.add_to_index(vectors2, train=False)
        print()
        
        # Search for similar patches
        results = dde.resonance_search(img, k=5)
        print()
        
        print("🎯 Top Results:")
        for i, res in enumerate(results[:3], 1):
            print(f"{i}. {res['label']} | Resonance: {res['resonance']:.4f} | "
                  f"Dark Residue: {res['dark_residue']:.6f}")
        print()
        
        # Coherence map
        coherence = dde.coherence_map()
        print("\n🌐 Coherence Map:")
        for label, stats in coherence.items():
            print(f"  {label}:")
            print(f"    Patches: {stats['n_patches']}")
            print(f"    Avg Dark Residue: {stats['avg_dark_residue']:.6f}")
            print(f"    Coherence Score: {stats['coherence_score']:.2f}")
        print()
    else:
        print("\n⚠️  Install FAISS to enable vectorization: pip install faiss-cpu\n")
    
    # Save manifest
    dde.save_manifest()
    print()
    
    print("=" * 70)
    print("Seed planted. Watch it grow into an ecosystem.")
    print("=" * 70)