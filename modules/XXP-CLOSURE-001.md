---
id: EXP-OBS-CLOSURE-001
title: Observer-Induced Closure in Public “Random” Sequences
version: 1.0
parents: [DOMA-CLOSURE-KIT-001, MATH-GEODESIC-001]
status: draft
summary: Tests the hypothesis that publicly observed random processes (lotteries) exhibit weak geodesics and nonzero Dark Residue relative to quantum or software random sources, due to observation cadence and bounded state space.
---

# §1 · Hypothesis
Any **observed, rate-limited, bounded** random process acquires a nonzero Dark Residue:
\[
D_\text{observed} = D_\text{intrinsic} + D_\text{observer} > 0
\]
because the act of observation imposes a cycle (draw time) and a boundary (1..69), thus introducing **weak closure**.

# §2 · Data Sources
- Public Powerball/MegaMillions archives (draw-by-draw). :contentReference[oaicite:7]{index=7}
- ANU QRNG (quantum) as “least observed” baseline. :contentReference[oaicite:8]{index=8}
- random.org atmospheric source (observed, but different apparatus). :contentReference[oaicite:9]{index=9}
- Local PRNG (numpy) as control.

# §3 · Preprocessing
1. Map every source to an integer time series \( x_t \in \{1,\dots,69\} \).
2. Segment into windows \(W_k\) of fixed length (e.g. 64 draws).
3. For each window, compute:
   - lag-1 autocorr: \( \rho_1(W_k) \)
   - edge frequency: \( e(W_k) \)
   - flatness (std/mean of histogram): \( f(W_k) \)
   - power change: \( \Delta P_k = (P_k - P_0) / P_0 \)
   - curvature: \( |κ^\*|_k \) using the same formula as the MSEED analyzer

# §4 · Dark Residue Functional
For each window \(W_k\):
\[
D_k = α|\rho_1(W_k)| + β e(W_k) + γ f(W_k) + ζ |κ^\*|_k
\]
with \( α,β,γ,ζ > 0 \) chosen so that a perfectly flat i.i.d. stream gives \(D_k \approx 0\).

# §5 · Geodesic Detection
Define closure:
\[
\text{geodesic}(W_k) \iff \frac{dD_k}{dt} \approx 0 \quad \text{and} \quad D_k \le \epsilon
\]
Across the 4 sources, count the fraction of windows satisfying this. Expect:
\[
\text{QRNG} > \text{PRNG} \ge \text{random.org} > \text{lottery}
\]
if the lottery is the *most* observed.

# §6 · Analysis Targets
1. **Do lottery windows form arcs** on the (ΔP, |κ*|) plane, like your seismic data?  
2. **Does curvature stay nonzero** even when ΔP≈0?  
3. **Does high-attention period** (jackpot spike) show higher D than low-attention periods? (Use jackpot news windows.) :contentReference[oaicite:10]{index=10}

# §7 · Success Criteria
- We observe **persistent, non-vanishing** D_k on lottery data.
- We observe **lower** and **flatter** D_k on QRNG.
- We can feed all 4 sequences to the **same closure engine** without changing the engine — only the residue function.

# §8 · Notes
This experiment is falsifiable: if ANU QRNG and public lottery have indistinguishable D-distributions under the same windowing and same residue functional, the observer-induced closure hypothesis is *not* supported.
