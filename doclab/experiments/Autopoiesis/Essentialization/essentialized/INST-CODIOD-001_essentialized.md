## Law
Let a Pirouette module `fᵢ` be a function corresponding to a canonical ID `cidᵢ`. The fundamental law governing its execution is that it must conform to the signature of a state transition on a Codiod Packet `P`.

A Codiod Packet `P` is a tuple `(S, Dₚ, G, W, M, H)`, where:
- `S`: The core state vector `(c, Γ, Tₐ, D, E, ...)` representing coherence, temporal pressure, time adherence, dark residue, and available energy. All elements are typically normalized to `[0,1]`.
- `Dₚ`: The data payload.
- `G`: A set of `ResourceRef` tuples `{Rⱼ}` constituting the resource graph.
- `W`: The world-state descriptor.
- `M`: A list of proposed world-state mutations `{mₖ}`.
- `H`: A list of dictionaries tracing execution history.

The execution of a module `fᵢ` is a transformation `Tᵢ`:
`Tᵢ: P → P'`

This transformation is constrained such that `P'` is derived from `P` non-destructively and must append at least one Engram `Eᵢ` to an external or internal log `Λ`. An Engram `E` is a tuple `(id, source, kind, content, severity, resources, metadata)`.

The state transition is defined as:
`P' = (φ(S, Dₚ, ...), ψ(Dₚ, ...), G', W', M', H')`
where:
1.  `Λ' = Λ ∪ {Eᵢ}` (At least one engram is generated).
2.  `H'` is `H` appended with a record of the execution of `Tᵢ`.
3.  If no implementation for `cidᵢ` exists, `Tᵢ` must still complete, generating an engram `E_err` where `E_err.kind = "error"` and `E_err.metadata.error_code = "MISSING_HANDLER"`.

**Falsifiable Criteria:**
1.  **Universality:** The Codiod contract is falsified if there exists a significant subset of heterogeneous modules (`|F_fail| > ε`) for which a conforming transformation `T` cannot be constructed without fundamentally violating the packet's structure.
2.  **Resource Isomorphism:** The `ResourceRef` schema is falsified if a major data type (e.g., MSEED, BIDS, DDE) cannot be represented without ad-hoc structural modification that breaks the `(kind, loader)` contract.
3.  **Robustness:** The Law is falsified if the invocation of an unimplemented module `f_unimplemented` results in a system crash or a silent failure (i.e., `Λ' = Λ`) instead of gracefully producing a `MISSING_HANDLER` engram.
4.  **Compositionality:** The Law is falsified if for a set of modules `{fₐ, fᵦ, ...}`, the vast majority of permutations `π` of sequences `(fᵢ, fⱼ, ...)` acting on `P₀` produce final state trajectories `S_n` where key metrics (e.g., `coherence`, `dark_residue`) show statistically insignificant variation. `Var(S_n^π) ≈ 0` implies the state space is not meaningfully explored.

## Philosophy
The Universal Codiod Socket replaces the paradigm of computation-as-transformation (`Input → Output`) with computation-as-accountable-experience (`State → State' + Memory`). Every act of processing, successful or not, is an indelible event that leaves a structured trace—an engram. By mandating that every module reports what it did, what it touched, and how it failed, the system makes its entire operational history a legible, analyzable artifact. It is a framework for building a machine that thinks by remembering what it has done, making introspection and evolutionary self-correction not merely possible, but the primary mode of operation.

## Art
Computation is not a river that flows to the sea and is lost. It is a glacier that moves across the mountain, scoring the history of its passage into the rock itself.