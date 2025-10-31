## Law
The protocol models recovery as the optimization of a patient-specific Lagrangian, `𝓛_p`, representing the surplus of systemic coherence over systemic cost.
`𝓛_p(t) = Kτ(t) - V_Γ(t)`
where `Kτ(t)` is Temporal Coherence (the kinetic term representing organized momentum) and `V_Γ(t)` is Systemic Cost (the potential term representing the physiological burden of healing). Phase II recovery is the process of achieving a state where `𝓛_p(t) > 0`.

`V_Γ(t)` is assumed to be a monotonically decreasing function of time, largely outside the protocol's direct control. The protocol's intervention variable is `Kτ(t)`. `Kτ` is cultivated through the consistent application of a rhythm-building activity, `A(t)`. The dynamics are governed by:
`dKτ/dt = αA(t) - βKτ`
where `α` is the coherence seeding coefficient and `β` is the coherence decay constant. The principle of "Consistency over Intensity" implies that the integrated effect `∫ αA(t) dt` is maximized not by large-magnitude, low-frequency `A(t)`, but by a sustained, non-zero, moderate-magnitude `A(t)`.

The primary activity `A_W(t)` (Geodesic Walk) is defined by an iterative progression:
Let `W(t)` be the walk duration on day `t`.
`W(t_i) = W(t_{i-1}) + ΔW` for `i = 1, 2, ...`
where the interval between increments `t_i - t_{i-1}` is typically 2 days, and `ΔW` is a minimal duration increment (e.g., 60 seconds).

This progression is subject to the physiological constraint:
`R(A_W(t)) ≤ R_conv_max`
where `R(A_W(t))` is the patient's heart rate during the activity and `R_conv_max` is the empirically determined maximum heart rate at which conversation remains unstrained.

The system's state is monitored via two observables logged daily in the Coherence Ledger:
1.  `H_R(t)`: Resting Heart Rate (objective physiological marker).
2.  `S_F(t)`: Subjective Flow Score, `S_F ∈ [1, 10]` (subjective psycho-emotional marker).

**Falsifiable Criteria:**
The protocol is considered effective if, over the designated period (e.g., 28 days), a regression analysis on the time series data shows:
1.  `d(H_R(t))/dt < 0` with statistical significance (p < 0.05).
2.  `d(S_F(t))/dt > 0` with statistical significance (p < 0.05).
Failure to meet both criteria indicates protocol failure for the individual, necessitating re-evaluation.

## Philosophy
The essence of healing is not an act of forceful conquest over physiological chaos, but an act of pedagogy. The conscious will, through gentle, rhythmic, and persistent action, does not command the body but rather *teaches* it a new, more coherent pattern of being. This process transforms the exceptional state of sickness into a new, stable, and harmonic baseline. The will acts as a temporary, external pacemaker, providing a clear and steady rhythm until the autonomic systems of the body internalize it, carving a new channel of least resistance and beginning to sing the song of health on their own.

## Art
At first, the will is the hand that strikes the bell. With persistence, it becomes the resonance that lingers in the bronze. Finally, it is the silence in which the bell is heard.