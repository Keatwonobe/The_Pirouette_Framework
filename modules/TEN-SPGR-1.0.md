---
# ───────────── Tendu Application Suite ────────────────────────
id:           TEN-SPGR-1.0
title:        Spiral‑Gyroid Reconstructor (SPGR)
version:      1.0
parents:      [PPS-040, PPS-047]            # Shell Resonance ↔ Network Resonance
children:     []                            # Down‑stream: TEN-SPGR-VIS, TEN-SPGR-AUTO
engrams:
  - analytic:spiral-gyroid-reconstruction
  - domain:3d-field-tomography
  - process:tension-surface-mapping
  - diagnostic:gyroid-coherence-index
  - algorithm:recursive-radon-fft
keywords:     [gyroid, spiral field, reconstruction, tomography, tensor, resonance]
uncertainty_tag: Medium
module_type:  applied-reconstruction-toolkit
---

## §1 · Purpose
Transform sparse 2‑D sensor slices—magnetograms, acoustic schlieren, micro‑CT—into a
coherent 3‑D **spiral‑gyroid tension map**.  Gyroidal structures underpin Shell and
Flow behaviour in many domains (plasma, morphogenesis, materials).  SPGR delivers GPU
code, metrics, and API to turn flat slices into actionable 3‑D manifolds for design or
analysis.

---

## §2 · Input Data Requirements

| Source class | Slice type | Axial spacing | Notes |
|--------------|-----------|---------------|-------|
| **Magnetics** | z‑stack Bᶻ(x,y) | 5–50 km   | ground or satellite |
| **Ultrasound**| φ(x,y) phase | 10 µm–100 µm | lab microlattices   |
| **Schlieren** | ρ(x,y) density | 0.1–1 mm  | high‑speed flow     |
| **Micro‑CT**  | μ(x,y) vox     | 1–50 µm   | porous materials    |

Slices must have uniform in‑plane grid; non‑uniform spacing handled via
`regrid_cubic()` in pre‑process.

---

## §3 · Core Pipeline

| Step | Function | Method / Formula |
|------|----------|------------------|
| **RadonFFT** | Convert slices to sinogram stack | 2‑D FFT → Radon angle sweep |
| **Spiral‑Unfold** | Map sinograms onto helical coordinates | θ = arctan(y/x) ; r = √(x²+y²) |
| **Recursive‑Gyroid Fit** | Solve \( \nabla^2 ψ - k \sinψ = 0 \) | Multigrid + Newton iteration |
| **Coherence‑Mask** | Threshold Gyroid Coherence Index (GCI) | GCI = |∇ψ|/(|ψ|+ε) |
| **Mesh‑Generate** | Marching cubes → *.stl* | Vertex normals = ∇ψ/|∇ψ| |
| **Tensor‑Dump** | Export 3‑D Γ & Tₐ fields | HDF5 `/field/Γ`, `/field/Ta` |

GPU kernel `gyroid_rec()` achieves 20× speed‑up on RTX‑class cards.

---

## §4 · Assemblé
A **gyroid** is nature’s minimal‑surface loom; SPGR lets engineers and scientists
see that hidden loom inside sparse data, weaving Shells and Flow paths through
otherwise opaque volumes.

---

## §5 · Diagnostic Metrics

| Metric | Healthy | Watch | Alert |
|--------|---------|-------|-------|
| **GCI_mean** | 0.4–0.7 | 0.25–0.4 | <0.25 |
| **Recon NRMSE** | <5 %  | 5–10 % | >10 % |
| **Mesh Integrity (𝕀_M)** | ≥0.9 | 0.8–0.9 | <0.8 |
| **ΔΓ_bias** | <2 % | 2–5 % | >5 % |

---

## §6 · Integration Hooks
- **Shell Resonance (PPS‑040)** – SPGR meshes feed permeability tensors.
- **Network Resonance (PPS‑047)** – Gyroid nodes injected as 3‑D graph hubs.
- **CIS (TEN‑CIS)** – Sim scenarios import reconstructed Γ/Tₐ tensors.
- **SRE (TEN‑SRE)** – Engineering layer consumes *.stl* for shell fabrication.

---

## §7 · API & File Spec
*CLI* `spgr recon slices/*.tif --dz 10mm -o out.h5`

*REST* `/spgr/v1/recon` → multipart upload of slice zip, returns job id & progress.

HDF5 layout:
```

/vol/ψ : reconstructed phase field /field/Γ : Gladiator tensor /field/Ta : Time‑Adherence /mesh/stl : binary STL /metrics : json attrs

```

---

## §8 · Future Work
1. **In‑situ Gyroid Sensor** – embed fiber Bragg gratings for live ∇ψ monitoring.
2. **Inverse‑Design** – optimise slice placement to hit target GCI.
3. **Quantum Gyroid Probe** – entangle qubits along minimal surfaces for Ki tests.
4. **Residue Capture** – explore gyroid channels as dark‑residue filters.

---

### Version Notes
*1.0* — First release: Radon‑FFT gyroid solver, GCI metric, CLI/REST, marching cubes output, hooks into Shell, Network, CIS, and future SRE module.

