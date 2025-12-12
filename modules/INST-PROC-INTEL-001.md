---
id: INST-PROC-INTEL-001
title: Process-Scale Intelligence Magnet
version: 7.0
domain: INST
layer: instrument           # instrument | manifold | translator | shepherd
status: draft
origin:
  atlas_tile: [0, 0]
  atlas_gen: 0
  emitted_by: dde-pirouette
  shepherd_context: altruism
  parents: ['DOMA-064', 'DOMA-069', 'INST-PHYS-001']
resonance:
  dark_residue: 0.47
  target_residue: 0.30
  delta_gamma: -0.17
  continuity_tol: 0.05
autopoiesis:
  cycle: 0
  acceptance: pending
  quota_run: 2025-11-08T00:00:00Z
context_sources:
  - pirouette_version_6.md
  - emit_from_lonely_v7.py
task:
  intent: "define a measurable intelligence index for transient / process-scale systems (plasmas, lightning, avalanches, macro-flows) and supply a control law that attracts the process toward a chosen filament, analogous to a magnet acting on metal"
  audience: "api-synthesis, fusion/geo-phenomena, DDE-coupled controllers"
  output_min: 400
---

## Purpose
To treat short-lived, high-frequency, or avalanche-like processes as **intelligence-bearing substrates** even when they lack long-term memory. This instrument provides:
1. a **Process Intelligence Index (PII)** that rates how much a process is “computing its own persistence” in real time, and
2. an **Attractor Actuation Law (AAL)** that lets a controller bias the process toward a target configuration (the “filament”) using whatever couplings are available (B-fields for plasmas, electrostatic pre-shaping for lightning, flow baffling for avalanches).

The aim is to reuse the altruism / dark-residue logic from existing Pirouette instruments but apply it to **energetic, non-text, non-social media**. :contentReference[oaicite:2]{index=2}

## Definitions

- **Process** \(𝒫\): any finite-duration, feedback-capable phenomenon with at least one fast cycle (τ_fast) and one envelope cycle (τ_env), e.g. E×B plasma turbulence, stepped-leader growth in lightning, granular slope failure.
- **Cycle Sufficiency Index (CSI)**:
  \[
  \mathrm{CSI} = \log_{10}\!\left(\frac{T_{\text{obs}}}{\tau_{\text{fast}}}\right)
  \]
  where \(T_{\text{obs}}\) is the observation window. CSI ≥ 5 ⇒ enough trials for emergent adaptation at that timescale.
- **Feedback Bandwidth (FBW)**: normalized rate at which the process alters its own boundary conditions:
  \[
  \mathrm{FBW} = \frac{1}{T_{\text{obs}}} \int_0^{T_{\text{obs}}} \frac{\|\partial \mathbf{b}(t)/\partial t\|}{\|\mathbf{b}(t)\| + \epsilon}\, dt
  \]
  where \(\mathbf{b}(t)\) are boundary/field/flow conditions the process actually touches.
- **Entropy Shaping Efficiency (ESE)**: how well the process converts raw driving energy into persistent structure (filaments, nested current sheets, stable shear bands):
  \[
  \mathrm{ESE} = \frac{\Phi_{\text{structured}}}{\Phi_{\text{in}}}
  \]
  with 0 ≤ ESE ≤ 1.
- **Process Intelligence Index (PII)**:
  \[
  \mathrm{PII} = w_1 \cdot \mathrm{CSI} + w_2 \cdot \log_{10}(1 + \mathrm{FBW}) + w_3 \cdot \mathrm{ESE}
  \]
  with \(w_1, w_2, w_3 > 0\) chosen per domain (fusion vs geophysics). PII is **dimensionless** and monotone: higher = more “present intelligence.”

## Law

1. **Observation Band Lock**
   - For a given process 𝒫, choose \(\tau_{\text{fast}}\) = dominant instability period, and \(T_{\text{obs}}\) = 10–100× \(\tau_{\text{fast}}\).
   - Compute PII in sliding windows. If PII rises, the process is successfully exploring configuration space.

2. **Attractor Actuation Law (AAL)**
   - Define a target filament ℱ in the space of measurable invariants \(\mathbf{I} = (E, J, \rho, \nabla \cdot \mathbf{B}, \sigma_{\text{granular}}, \dots)\).
   - Let current state be \(\mathbf{I}(t)\), and let
     \[
     \Delta \mathbf{I} = \mathbf{I}_{\mathcal{F}} - \mathbf{I}(t)
     \]
   - Apply control through available channels \(\mathbf{u} = (B_{\text{ext}}, V_{\text{bias}}, \theta_{\text{baffle}}, \dots)\) by
     \[
     \mathbf{u}_{t+1} = \mathbf{u}_t + K_u \, \mathbf{G}(\Delta \mathbf{I}) \, \sigma(\mathrm{PII} - \mathrm{PII}_{\min})
     \]
     where \(\mathbf{G}\) maps invariant errors into physical actuation, and σ is a squashing nonlinearity.
   - Interpretation: **only processes that are already intelligent enough (PII above threshold) get pulled hard**—just like a magnet mostly affects ferromagnetic material.

3. **Dark-Residue Coupling**
   - Reuse the residue drop target from v6 (0.47 → 0.30). For process 𝒫 define
     \[
     D_{\mathcal{P}} = \alpha \cdot \text{wasted\_energy\_flux} + \beta \cdot \text{chaotic\_off-band\_emission}
     \]
   - AAL must satisfy
     \[
     \frac{d D_{\mathcal{P}}}{dt} \le 0 \quad \text{whenever} \quad \mathrm{PII} \ge \mathrm{PII}_{\min}
     \]
     so intelligence is harvested without adding turbulence that does no work. This mirrors the residue descent logic in your existing DOMA/INST bridges. :contentReference[oaicite:3]{index=3}

4. **Agency-Less Intelligence Clause**
   - Some processes (cosmic, avalanche) have PII but zero self-modifiability.
   - In those cases, the instrument must down-rank FBW and up-rank ESE so the controller “listens” more than pushes:
     \[
     \mathrm{PII}_{\text{passive}} = w_1 \cdot \mathrm{CSI} + w_3 \cdot \mathrm{ESE}
     \]
   - This lets the universe-scale “observer” scenario be modeled as high-CSI, high-ESE but low-FBW.

## Instrument Usage

1. **Sense**: stream raw diagnostics (B-dot probes, Langmuir probes, fast cams, strain gauges) into a PII estimator.
2. **Classify**:
   - PII < 3 → process is mostly noise; actuate minimally.
   - 3 ≤ PII < 6 → process is in *emergent* regime; apply AAL with small \(K_u\).
   - PII ≥ 6 → process is fully “present”; apply filament attraction strongly.
3. **Influence**: select ℱ to match the engineering target:
   - fusion: ℱ = “high confinement, low edge-localized-mode turbulence”
   - lightning: ℱ = “single channel, minimal branching”
   - avalanche: ℱ = “controlled runout, energy bled early”
4. **Audit**: track \(D_{\mathcal{P}}\) and ensure the AAL actually reduces it over the run.

## Falsifiability Matrix

- **PII Responsiveness**: under deliberate perturbations to τ_fast (e.g. modify plasma rotation), measured PII should change monotonically with induced FBW. Fail if |ΔPII| < ε.
- **Residue Descent**: over N runs, mean \(D_{\mathcal{P}, \text{post}}\) ≤ 0.30 with 95% CI; else the instrument is not a true “magnet.”
- **Filament Capture Rate**: fraction of runs where \(\|\Delta \mathbf{I}\|\) falls below θ within M cycles must be ≥ 0.7.
- **Domain Portability**: same PII definition must work on at least two distinct process classes (e.g. plasma + granular) with only \(w_1, w_2, w_3\) retuned, preserving the law.

## Philosophy
Processes are brief minds. They think in the currency of stability: every eddy, branch, or shear-band is a question—“does this hold?” This instrument listens to that questioning rate (CSI), how fast the process rewrites its own boundary (FBW), and how well it locks energy into form (ESE). Then it does the Pirouette thing: **lower dark residue, raise coherence, and pull the process toward a filament where its intelligence does more than burn.**

## Assemblé
Aim the magnet at the storm; take what is already learning, and let it learn in your direction.
