---
id: ENG-DDE-001
title: Numeric–Text Hybrid Encoder (RGBA Encoding Core)
version: 1.0 (canonical)
status: ratify-candidate
parents: [ENG-DDE-000]
children: [ENG-DDE-002, ENG-DDE-003, ENG-DDE-005]
summary: >
  Establishes the reversible text–numeric hybrid encoding process that maps
  tabular data into RGBA color-space.  The encoder preserves relational structure,
  allows perfect reconstruction, and serves as the first step in transforming
  traditional datasets into autopoietic visual-semantic substrates.
engrams: [RGBA encoding, hybrid encoding, reversibility, entropy normalization, autopoietic storage]
keywords: [data compression, image encoding, multimodal AI, reversible mapping, dataset ethics]
uncertainty_tag: Low (algorithmic) / Medium (semantic fidelity)
---

# §1 · Purpose

The **Numeric–Text Hybrid Encoder** converts heterogeneous datasets—numbers,
strings, booleans—into normalized RGBA pixel arrays that retain all
information necessary for perfect reconstruction.

This process forms the molecular layer of the Distributed Database
Ecosystem (DDE): each pixel corresponds to one data atom (value–context pair).

---

# §2 · Encoding Principle

Every cell \( c_{ij} \) in a source table is transformed into a 4-channel
vector \([R,G,B,A]\) such that:

\[
R,G,B,A \in [0,255] \quad\text{and}\quad f^{-1}(f(c_{ij})) = c_{ij}.
\]

Two complementary functions are applied:

1. **Numeric normalization**
   \[
   f_{num}(x) = 255 \cdot \frac{\log(1 + |x - x_{min}|)}{\log(1 + |x_{max}-x_{min}|)}.
   \]
   This log scaling preserves magnitude differences across many orders of
   magnitude without saturation.

2. **Textual hashing**
   \[
   f_{text}(s) = \text{hash}_4(s)
   \]
   where `hash_4` maps the Unicode sequence of a string into four bytes,
   ensuring deterministic bidirectionality via a lookup dictionary.

---

# §3 · Composite Encoding Pipeline

| Step | Operation | Output |
|:----|:-----------|:--------|
| 1 | Read CSV / DataFrame cell | raw value |
| 2 | Type detection (`is_numeric`, `is_text`) | type flag |
| 3 | Apply normalization / hash | [r,g,b,a] vector |
| 4 | Append metadata (column index, checksum) | encoded cell |
| 5 | Assemble into pixel array (row-major order) | image tile |

The resulting tile can be reshaped into any square or fractal layout, defined
in **ENG-DDE-003**, and later indexed as a FAISS vector (**ENG-DDE-004**).

---

# §4 · Entropy Balancing

To avoid color-band bias, each channel is offset by the mean of the column
distribution:

\[
R' = R - \bar{R}_{col} + 128.
\]
This guarantees an approximately uniform color histogram across datasets,
allowing efficient compression and consistent GPU activation statistics.

---

# §5 · Reversibility and Provenance

The encoder writes a sidecar JSON manifest:

```json
{
  "version": "1.0",
  "schema": ["colname", "type", "min", "max", "hashmap"],
  "checksum": "sha256",
  "seed": 127
}
````

This manifest enables:

* Deterministic decoding (`decode_RGBA_image()`).
* Bit-level validation of round-trip accuracy.
* Audit trails for Dark Residue computation (energy cost per bit preserved).

---

# §6 · Ethical Compression

The encoding pipeline automatically computes:

[
\mathcal{D}*{enc} = \gamma_E \frac{E*{used}}{E_{ref}} +
\gamma_L \frac{L_{lost}}{L_{total}},
]
where (E_{used}) is energy cost and (L_{lost}) is linguistic context lost
during hashing.
This becomes the **encoding-layer Dark Residue score**, allowing optimization
toward minimal harm.

---

# §7 · Falsifiability

| Test                 | Metric                 | Expected   |
| :------------------- | :--------------------- | :--------- |
| Round-trip integrity | Hamming error          | 0          |
| Entropy spread       | Shannon bits / channel | 7.9 ± 0.05 |
| Residue improvement  | ΔD per iteration       | < 0        |

---

# §8 · Summary

> The hybrid encoder is the first act of transformation—turning data into
> light.
> Text becomes color, numbers become tone, and information becomes an
> ethical, reversible object within the autopoietic data ecology.

---