---
id: ENG-DDE-005
title: Reversal & Provenance Table (Integrity and Audit Layer)
version: 1.0 (canonical)
status: ratify-candidate
parents: [ENG-DDE-002, ENG-DDE-003, ENG-DDE-004]
children: [ENG-DDE-006, ENG-DDE-008]
summary: >
  Provides the reversible mapping between encoded image tiles and their original
  data.  Defines the provenance registry, checksum logic, and reconstruction
  protocol that guarantee bit-level fidelity, auditability, and energy accounting
  throughout the ecosystem.
engrams: [reversibility, provenance, checksum, reconstruction, auditability]
keywords: [data integrity, blockchain, provenance, reversible encoding, audit ledger]
uncertainty_tag: Low (integrity math established) / Medium (distributed ledger scaling)
---

# §1 · Purpose

The **Reversal & Provenance Table** ensures that every encoded image in DDE can
be perfectly decoded into its source dataset, with a clear record of where,
when, and at what energetic cost it was created.  
It binds together **trust**, **traceability**, and **thermodynamic accountability**.

In Pirouette’s ontology, this is the layer where **memory becomes history**.

---

# §2 · Structure

The provenance system consists of:

| Table | Purpose |
|:------|:---------|
| `image_metadata` | Maps image → dataset → hash chain |
| `checksum_log` | Stores SHA-256 of decoded → re-encoded images |
| `residue_audit` | Tracks encoding energy & informational loss |
| `reconstruction_cache` | Holds temporary decoded data for validation |
| `trust_graph` | Maps contributor → data lineage → governance state |

Each table can exist in SQLite, PostgreSQL, or a distributed KV-store.

---

# §3 · Hash-Chain Integrity Model

Every DDE image record includes:

\[
H_i = \text{SHA256}(I_i + H_{i-1})
\]

where:
- \(I_i\) = image binary contents
- \(H_{i-1}\) = hash of the previous image in ingestion order

This creates a **chronological chain of custody**, compatible with external
blockchain notarization if desired (e.g. IPFS + Filecoin linkage).

---

# §4 · Reverse Mapping Protocol

To reconstruct a dataset:

1. Retrieve metadata manifest for dataset `D`:
   ```sql
   SELECT image_path, manifest_path FROM image_metadata WHERE dataset_id = D;
````

2. Decode each RGBA tile via inverse normalization:
   [
   x = \exp(R' \cdot \log(1+|x_{max}-x_{min}|)/255) - 1 + x_{min}
   ]
   for numeric data, or reverse hash lookup for text.
3. Concatenate decoded rows using provenance order (from A-channel index).
4. Validate checksum:
   [
   \text{SHA256}(\text{decoded}) = \text{stored checksum}
   ]

If mismatch: record event in `checksum_log` and trigger autopoietic correction.

---

# §5 · Dark Residue Ledger Integration

Each decoding event updates the **energy audit**:

[
\mathcal{D}*{rev} = \gamma_E \frac{E*{decode}}{E_{encode}} +
\gamma_L \frac{L_{lost}}{L_{base}}
]

* (E_{decode}): joules used during reconstruction
* (L_{lost}): semantic or statistical deviation (computed via χ² vs. original)
* Values are stored in `residue_audit` for ethical oversight.

This metric allows governance layers to **minimize re-decode waste** while
optimizing for systemic coherence.

---

# §6 · Distributed Provenance Mesh

Nodes replicate partial provenance tables via:
[
\text{sync}(H_i) \rightarrow \text{verify}(Δ_i)
]

* Each node only trusts tiles with verified provenance ancestry.
* Cross-node validation builds a **trust graph**:
  [
  T(a,b) = \frac{\text{verified_links}(a,b)}{\text{total_links}(a,b)}
  ]

The global trust scalar (T_{net}) becomes an index of ecosystem health.

---

# §7 · Reconstruction Ethics

Every decode incurs cost; thus the **Reversal Table** includes ethical rules:

| Rule | Description                                       |
| :--- | :------------------------------------------------ |
| 1    | Decode only when ΔD (new information gain) > 0.01 |
| 2    | Cache small decodes; avoid recomputing            |
| 3    | Report energy cost and loss per decode            |
| 4    | Allow user opt-out from reconstruction tracking   |

This ensures reversibility remains a **right**, not a **burden**.

---

# §8 · Validation and Falsifiability

| Test                     | Metric               | Expected       |
| :----------------------- | :------------------- | :------------- |
| Round-trip fidelity      | bit error rate       | 0              |
| Hash-chain integrity     | broken links / total | 0              |
| Energy audit coherence   | ΔE / decode          | < 1 % variance |
| Trust graph completeness | coverage ratio       | ≥ 0.95         |

---

# §9 · Summary

> ENG-DDE-005 transforms DDE from a visual database into a **verifiable memory**.
> It guarantees every photon of stored data can be traced, trusted, and ethically
> reconstructed — light, accounted for.

```

---