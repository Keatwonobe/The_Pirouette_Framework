1. Preprocess signals (band-pass 0.5–80 Hz, artifact removal).
2. Compute instantaneous phase (Hilbert or Morlet method).
3. Track TPCI(t) to locate collapse and recovery events.
4. Estimate τ_P and ξ_P per event.
5. Aggregate across participants and fit scaling exponents (ν_P, z_P).
6. Compare empirical results to Pirouette-predicted exponents:

   * ν_P ≈ 0.5 ± 0.1
   * z_P ≈ 2.0 ± 0.3