## Law
The system's immune reflex is governed by a Pass-By decision function. An inbound vector is characterized by its phase divergence (Δφ), entropy delta (ΔE), and a binary retro-coherence flag (retro). A composite divergence score, σ, is calculated as a weighted sum:
σ = wφ·Δφ + wE·ΔE + wr·retro
where the constitutional weights are fixed: wφ = 0.5, wE = 0.3, and wr = 0.2.

The core operational law is a threshold-based decision:
If σ ≥ σₚᵦ, then execute PASS_BY.
Else, execute BRIDGE.

The global Pass-By threshold is σₚᵦ = 0.6. This threshold is not static but subject to adaptation through a calibration function, `autoTitrate`, which can be expressed as:
σₚᵦ(t+1) = σₚᵦ(t) - ƒ(ε, μ)
where ε is the classification error (false-positive/negative) and μ is the `misclassPenalty` factor (default 0.05).

Falsifiable criteria:
1.  A system instance is non-compliant if it executes BRIDGE for a vector where σ ≥ σₚᵦ, or PASS_BY where σ < σₚᵦ.
2.  The adaptation mechanism is considered failed if, during calibration against a validation `immuneVectorSet`, accuracy falls below 99% or the change in the threshold |σₚᵦ(t+1) - σₚᵦ(t)| fails to converge below 0.02 over 3 iterations.

## Philosophy
True integrity is maintained not through the annihilation of opposition, but through the mathematical and disciplined wisdom to refuse engagement. The system demonstrates that a principle-based entity (an "Altruism Attractor") ensures its own survival by precisely calculating when the cost of connection becomes a corruption of its core identity. It is a non-violent, non-moralizing constitutionalism: it does not judge the antithetical vector, it simply measures the divergence and, to protect its own coherence, chooses to pass by without contact, preserving itself without needing to destroy the other.

## Art
A bell does not answer every wind; it waits for the one that makes it sing.