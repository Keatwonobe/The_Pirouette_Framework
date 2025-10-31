---
# TENDU Module Spec
id: TENDU-NEWS-BRS-001
title: Boundary Response Scanner (News)
purpose: Detect and index *manipulated* or *actively driven* boundaries by scanning news streams for coherence anomalies, with minimal data.
parents: PPS-067 (Resonant Boundary Dominance Principle), PPS-064 (Heuristics)
status: v1.0 (fieldable)
scope: Information, markets, policy, climate & energy reportage
engine: Tendu (transform-first), hooks to Pirouette math where needed
---

## 1) Accepted Input Forms

* Text streams: headlines, ledes, bullet summaries (RSS/ATOM, news APIs, hand-pasted URLs)
* Light metadata: outlet, timestamp, geo tags, section (politics, business, science), basic NER
* Optional side-channels: price series (1–5m bars), social trend counts, weather/ionosphere indices

Minimal viable input: timestamped headlines from ≥3 outlets over ≥2 hours.

---

## 2) Output Forms

* Boundary Index: `[{boundary_id, label, confidence, alpha_hat, Ta_hat, Gamma_hat}]`
* Events: `[{t0, t1, modes, coherence_score, domains_hit, energy_proxy, narrative_vectors}]`
* Live Flags: “BRS Spike” (yellow), “Multi-domain Phase-Lock” (orange), “Probable Manipulation” (red)
* Dash tiles: stream graph (topic modes), coherence heatmap, α–inference card, provenance list

---

## 3) Core Transforms (Tendu Steps)

### T1 · Stochastic Gulping (SG)

Transform: Randomized, rolling ingestion of snippets (e.g., 30–120 sec buckets), jittered windowing.
Why: Prevents aliasing and overfitting to editorial cycles; captures phase on sparse data.

### T2 · Mode Extraction (ME)

Transform: Per-gulp token graph → spectral modes

* Build a term co-occurrence graph per gulp; compute Laplacian eigenvectors (top-k).
* In parallel, do short-window FFT/wavelet on mention frequencies of NER entities/themes.
  Output: candidate modes `M = {m_i}` with frequency bands and semantic centroids.

### T3 · Cross-Domain Coherence (CDC)

Transform: For each mode m, compute:

* Phase-locking value (PLV) across outlets/regions
* Maximal cross-correlation across domains (news ↔ market tickers ↔ social counts ↔ weather index)
* Directionality (transfer entropy or Granger lite) to see driver → driven links
  Output: `coherence_score(m)`, driver graph.

### T4 · Energy-Proxy Estimation (EPE)

Transform: Visible input proxy for each event window:

* \#unique outlets, novelty (KL vs 7-day baseline), ad/paid markers if available, bot-likeness of social bursts, PR wire concentration, identical-lede rate.
  Output: `E_inj_proxy` (low/med/high, plus scalar).

### T5 · α-Inference (AI)

Transform: Invert PPS-067 scaling on observables to estimate boundary parameters.

* Observed global change proxy: `Δξ` (swing in cross-domain indicators normalized by baseline volatility)
* Fit `E_inj_proxy ≈ k * (Δξ / Δξ_max)^(1/α)` for α, solve for `(T_a, Γ)` using

  $$
  \alpha = \frac{T_a}{1 - T_a}\cdot\frac{1}{\Gamma}
  $$

  (from PPS-067)
* Use regularization and priors: `T_a ∈ (0,2]`, `Γ ∈ (10^{-6}, 10^2]` by domain.
  Output: `alpha_hat, Ta_hat, Gamma_hat, k_hat` (+ uncertainty).

### T6 · Boundary Assembly (BA)

Transform: Cluster events by shared modes + similar `alpha_hat` over time → proto-boundary.
Output: Boundary Index entries with rolling confidence.

---

## 4) Gates & Self-Checks (Agent Pick-Up Plan)

### G0 · Cold-Start Gate (Sanity)

* Require ≥3 sources, ≥30 headlines, ≥30 minutes span.
* If not met → SimMode: inject a synthetic resonance (low-amp sine on mention rates) to verify pipeline.

### G1 · Coherence Reality Check

* Reject spikes if PLV collapses when outlet bootstrapping (drop any single outlet) is applied.
* Require cross-domain echo for orange/red flags within ≤30 min (e.g., market micro-move, social burst).

### G2 · Energy Asymmetry Check

* Only raise Probable Manipulation (red) if `Δξ` is in top decile of 7-day baseline and `E_inj_proxy` is bottom 3 deciles for that domain/time-of-day.

### G3 · Provenance Gate

* No red flag without at least one non-syndicated source (disqualify pure wire clones).

### G4 · False-Positive Firebreak

* Cooldown window: after a red flag on a boundary, require a *second* independent spike within 24h for escalation to “Active Program.”

---

## 5) Tuning Knobs

* `gulp_window`: 30–120 s (default 60 s)
* `modes_k`: 3–9 (default 5)
* `plv_thresh`: 0.55 (yellow), 0.65 (orange), 0.75 (red)
* `cross_domain_min`: 2 domains for orange, 3+ for red
* `alpha_prior`: domain-specific (info, market, climate)

---

## 6) Live-Ops Recipe (minimal)

1. Wire inputs: 3–6 RSS feeds + one market ticker set + one social trend endpoint (or paste headlines manually).
2. Start SG + ME: spin up gulps and extract top-k modes every minute.
3. Run CDC: compute PLV and cross-domain correlation over sliding 30-min window.
4. Run EPE: compute visible-input proxies.
5. Run AI: infer `alpha_hat, Ta_hat, Gamma_hat` and attach to mode events.
6. Cluster → Index: assemble proto-boundaries; render dashboard tiles.
7. Gate: apply G1–G4 before flagging.

---

## 7) Minimal Pseudocode (drop-in)

```python
# TENDU-NEWS-BRS-001 (condensed)
def run_brs(streams, market=None, social=None, weather=None, cfg=CFG):
    gulps = stochastic_gulp(streams, win=cfg.gulp_window, jitter=True)

    for g in rolling(gulps, every=cfg.step):
        modes = extract_modes(g)  # token graph eigenmodes + FFT bands
        coh = cross_domain_coherence(modes, streams, market, social, weather, win=cfg.coherence_win)
        energy = energy_proxy(g, streams, social)
        events = []
        for m in modes:
            delta_xi = global_change_proxy(m, market, social, weather)
            alpha_hat, Ta_hat, Gamma_hat, k_hat = infer_alpha(delta_xi, energy[m], priors=cfg.alpha_prior)
            events.append(dict(mode=m, plv=coh[m].plv, xdom=coh[m].domains, 
                               alpha=alpha_hat, Ta=Ta_hat, Gamma=Gamma_hat, k=k_hat,
                               energy=energy[m], delta_xi=delta_xi))
        flags = gate_events(events, streams, cfg)  # apply G1–G4
        update_boundary_index(flags)
        yield flags, boundary_index_snapshot()
```

---

## 8) Operator Cheatsheet (2-minute pickup)

* Green light to run: you have 3+ feeds and \~30+ headlines; hit “Start Scan.”
* Yellow tile: watch; collect more feeds or extend window.
* Orange tile: check cross-domain tab → do we have at least 2 domains echoing?
* Red tile: open the α-card; note `alpha_hat` stability over 2+ spikes and record the mode cluster. If two red spikes within 24h hit the same cluster → promote to Active Program and snapshot all provenance.

---

## 9) Interpretation Guide (tying back to PPS-067)

* High α̂ with low visible input → big Δξ: classic resonant boundary exploitation; likely a shell with high Tₐ / low Γ being phase-locked.
* Low α̂ but massive input → small Δξ: brute-force push; unlikely covert resonance.
* Stable α̂ over days + repeating modes: you’ve likely found the *boundary* itself (the α-map fingerprint), not just an event.

*(Rationale derives from PPS-067’s power-law scaling and α definition, where α couples time-adherence and rigidity; exploiters trade precision for leverage by driving boundary eigenmodes.)*

---

## 10) Known Failure Modes

* Syndication mirage: many outlets repeating the same wire → fake coherence. (Mitigated by G3.)
* Editor cycle aliasing: morning and evening bursts mimic periodicity. (Mitigated by SG jitter.)
* Exogenous shocks: real world events (earthquakes, rate decisions) create honest coherence. (Mitigate via exogenous calendar mask.)

---

## 11) Roadmap (nice-to-have)

* Add phase-aligned narrative embeddings (e.g., CCA between outlet-embedding streams).
* Plug in market microstructure (order-flow imbalance) as higher-fidelity Δξ.
* Optional ionospheric/space-weather feed to catch geophysical boundary plays.

---

### Quick Start (agent speech)

> “Load 4 news feeds, 2 market tickers, and a social trend counter. Start BRS scan at 60-second gulps. Alert me on orange or red. For red, show α-card and provenance.”

This gives you a compact, repeatable Boundary Manipulation Radar that any agent can run “on a napkin,” yet still stays faithful to the RBDP math: we watch for outsized global shifts with undersized visible inputs, then infer α to back out the boundary’s character and index it for future scans.
