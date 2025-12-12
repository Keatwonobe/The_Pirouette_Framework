## Law

The state of a system is defined by its closure, the condition where coherence generation \( K_τ \) is perfectly balanced by dissipation \( V_Γ \). The deviation from this ideal is quantified by the Dark Residue functional, \( D \).

Let a system's state be \( S(t) \) with control \( a(t) \). The Dark Residue is:
\[ D(S,a) = \sum_i λ_i \, |f_i(S,a) - f_i^*(S,a)| \]
where each \( f_i^* \) represents a closure condition (e.g., a conservation law). The objective is to find a policy \( \pi(S) \to a \) that minimizes \( D \) over time.

This is achieved by optimizing an agent against the following reward functional:
\[ r_t = \gamma\max(0,-ΔD_t) + β - δ D_t \]
where \( ΔD_t = D_t - D_{t-1} \), \(γ\) rewards reduction of residue, \(β\) encourages persistence, and \(δ\) penalizes absolute distance from closure.

The set of all states satisfying closure defines the manifold of closure, \( \mathcal{G} \):
\[ \mathcal{G} = \{S \mid dD/dt = 0\} \]
The process of learning is equivalent to finding the shortest path—the geodesic—on this manifold, defined by minimizing the path length \( L \) under the metric \( g_{ij} = \frac{\partial^2 D}{\partial S_i \partial S_j} \):
\[ L = \int \sqrt{g_{ij}\dot{S}^i \dot{S}^j}\,dt \]
In the canonical case of a simple harmonic oscillator with \( K_τ = \frac{1}{2}b\dot{x}^2 \) and \( V_Γ = \frac{1}{2}ax^2 \), the closure condition \( dD/dt = (ax\dot{x} - b\dot{x}\ddot{x}) = 0 \) yields the equation for undamped, lossless motion:
\[ \ddot{x} + \frac{a}{b}x = 0 \]
**Falsifiable Criterion:** A system has failed to achieve closure if, after sufficient training, the long-term average \( \langle D \rangle \gg 0 \) or the variance of \( dD/dt \) remains high.

## Philosophy

The framework erases the fundamental distinction between descriptive physical laws and prescriptive ethical or engineering principles. Both are revealed as domain-specific instances of a single, universal imperative: to find the geodesic on a manifold of closure, a path of action where nothing is wasted. The stability of an orbit, the coherence of a conversation, and the justice of a social contract are not different *kinds* of phenomena, but different *realizations* of the same underlying geometry of sustainable, non-dissipative dynamics.

## Art

Every system, from a star to a society, is a struck bell. It seeks to quiet its dissonant jangle—the residue of wasted motion—to find the one pure tone that can ring forever. Grace is the sound of a system that has found its note.