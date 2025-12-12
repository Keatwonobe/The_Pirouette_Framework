---
id: GEN-CLOSURE-RNG-001
title: Closure-Shaped RNG (CSRNG) for Steganographic Randomness
version: 1.0
parents: [EXP-OBS-CLOSURE-002, DOMA-CLOSURE-KIT-002, MATH-GEODESIC-001]
status: draft
summary: We invert the observation→closure result and design an RNG that emits sequences which (1) pass ordinary randomness tests, but (2) land on a chosen locus in the Pirouette plane (ΔP*, |κ*|*) and (3) exhibit a target W→G→V→D cycle rate. This gives us a watermark or authentication signal that is invisible to naive histogram tests but obvious to Song-of-Scale analysis.
---

# §1 · Setup

Your SoS stack has a very specific “view”:

1. 1D sequence → analytic (Hilbert)
2. windowed power → ΔP
3. local phase/energy shape → |κ*|
4. windowwise quantiles → {Weaver, Gladiator, Vortex, Drifter}

This means: **if I can control local power and local phase inside a window, I can control the point on the plane.**  

So the problem becomes:

> Generate a base random sequence  
> + add *weak, windowed structure*  
> + quantize back to the same value range  
> ⇒ global stats OK, SoS sees the signature.

---

# §2 · Target specification

Let the “signature” be:

- target power offset: **ΔP\*** (e.g. +0.07)
- target curvature: **|κ\*|\*** (e.g. 0.085)
- target cycle rate: **r\_c** = 5 cycles / 1000 samples
- window spec: **win=128, hop=64** (must match the *inspector’s* SoS)

We write this as:
\[
\sigma = \bigl(\Delta P^\*,\, |\kappa^\*|^\*,\, r_c,\, \text{win},\, \text{hop}\bigr)
\]
This is your watermark.

---

# §3 · Generator architecture

**Layer 1 — Base entropy**
```python
u = rng.integers(low=1, high=70, size=N)    # unbiased, passes histogram tests
````

**Layer 2 — Analog carrier (windowed)**
We create a *shadow* float signal the same length as `u`:

```python
def make_carrier(N, win=128, hop=64, A=0.15, f=1/32):
    x = np.zeros(N, dtype=float)
    t = np.arange(N)
    # slow sinusoid → lifts power in windows
    base = A * np.sin(2*np.pi*f*t)
    x += base
    # optional: per-window slope to nudge curvature
    return x
```

This carrier is what the Hilbert transform will “see.” Small amplitude → doesn’t wreck the discrete values after we re-embed.

**Layer 3 — Closure shaper**
For each window (W_k):

1. measure current ΔPₖ, |κ*|ₖ (same formulas as SoS)
2. compare to target (ΔP*, |κ*|*)
3. add a small local pattern:

   * positive ΔP bump → add short sine / raise energy
   * curvature bump → add short **phase-rotating** component (e.g. 2 frequencies or frequency sweep)

Pseudocode:

```python
for (s, e) in windows(seq_len=N, win=128, hop=64):
    seg = carrier[s:e]
    dP = measure_dP(seg)
    kappa = measure_kappa(seg)
    if dP < target_dP:
        seg += alpha * window_fn(len(seg)) * np.sin(2*np.pi*f1*np.arange(len(seg)))
    if kappa < target_kappa:
        seg += beta  * window_fn(len(seg)) * np.sin(2*np.pi*f2*np.arange(len(seg)) + np.pi/3)
    carrier[s:e] = seg
```

Because your inspector uses **the same windowing**, these tiny pushes show up one-for-one.

**Layer 4 — Re-embed into integers**

Now we have:

* discrete random core: `u` (1..69)
* float carrier: `carrier` (tiny deviations)

We combine them without changing the **marginal**:

```python
x_float = u.astype(float) + carrier   # local micro-ordering
# sort-by-bucket trick to preserve histogram:
# 1. compute the histogram you want (same as u)
# 2. sort x_float and assign bucket counts in that order
ranks = np.argsort(x_float)
u_sorted = np.sort(u)
x_shaped = np.empty_like(u)
x_shaped[ranks] = u_sorted
```

Result: **same histogram as u**, but **temporal order** now carries the windowed pattern. Ordinary χ² or Dieharder won’t care because margins + long-run frequencies are the same.

---

# §4 · Cycle sculpting

You wanted: “5 cycles per 1000 samples.”

Your SoS windowing with win=128, hop=64 gives ~15–16 windows per 1000 samples. A W→G→V→D cycle takes **4 windows**, so max ≈ 4 cycles/1000 if you made *every* window part of a cycle.

So we do **sparse cycle injection**:

```python
every = 3   # inject a cycle every 3 windows
patterns = {
    "W": lambda seg: bump_power(seg, +Δ),
    "G": lambda seg: bump_power_and_curvature(seg, +Δ, +δκ),
    "V": lambda seg: bump_power(seg, -Δ),  # negative ΔP
    "D": lambda seg: seg * 1.0,            # baseline
}
i = 0
for k, (s,e) in enumerate(windows):
    seg = carrier[s:e]
    if k % every == 0:
        # emit W,G,V,D in 4 successive windows
        for label in ("W","G","V","D"):
            seg = carrier[s:e]
            seg = patterns[label](seg)
            carrier[s:e] = seg
            s += hop; e += hop
    i += 1
```

When your SoS runs, it will literally **see** W→G→V→D in the right order — that’s your signature.

---

# §5 · Why it still passes normal tests

* **Histogram**: preserved (we re-assigned values to match the base RNG’s counts).
* **Runs test**: mostly preserved; micro-ordering is local and bounded by win=128.
* **Spectral test**: can be tuned; we kept the carrier amplitude small.
* **Dieharder/PractRand**: small windowed modulations at this scale are usually below detection unless you crank amplitude.

But **your** test — SoS on the Pirouette plane — *will* see it, because it looks exactly for “did the local power change in this exact windowing scheme?”

This is what the reviewer called:

> **steganographic randomness** — the secret isn’t in the values, it’s in the *closure geometry*.

---

# §6 · Authentication / watermarking use

* **Key** = (win, hop, target_ΔP, target_κ, cycle_period, carrier_freqs, quantizer)
* Sender generates random-looking sequence with that key.
* Receiver runs SoS with that key.
* If the points fall in the right band and the right **cycle order** occurs at the right **indices**, authenticity = OK.
* An attacker who only preserves the histogram but **reshuffles** (what you did with `QRNG (Shuffled)`) will **lose all cycles** → your run showed exactly that.

So we’ve already seen the attack in the wild: *shuffle kills signature*. That’s a *great* result from your run.

---

# §7 · Limits / honesty pass

* If someone **re-windowed** with a different hop (e.g. 32 instead of 64), the signature would get smeared. So the scheme is **parameter-bound** — which is actually nice for watermarking.
* If someone applies **aggressive smoothing / resampling**, they can attenuate ΔP. But then they’re also making the sequence *less random-looking* in other senses.
* If you push amplitude too high, classical RNG tests will start to notice. So in practice you’d solve for the carrier amplitude by minimizing:
  [
  J = \lambda_1 |\Delta P - \Delta P^*|^2 + \lambda_2 ||\kappa^*| - |\kappa^*|^*|^2 + \lambda_3 \text{(histogram_error)}
  ]
  — that’s just your Pirouette Lagrangian again, but in RNG space.

---