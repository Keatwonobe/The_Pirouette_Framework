## Law
The protocol defines an idempotent ingestion function `Ingest(D) → ({G_i}, L)` where `D` is a raw dataset, `{G_i}` is a set of encoded data tiles, and `L` is a provenance ledger. The process is governed by the principle of entropy equalization.

Let the dataset `D` be partitioned into `N` gulps `{d_1, d_2, ..., d_N}`. The Shannon entropy for each gulp is `H_i = -Σ p(x)log_2 p(x)` for `x` in `d_i`. The partitioning must satisfy the **balance criterion**:
`|H_i - H̄| < ε_H`
where the mean entropy `H̄ = (1/N) Σ H_i`. This ensures each encoded tile `G_i = Encode(d_i)` possesses equivalent informational weight.

Each gulp `d_i` generates a provenance record `L_i` forming a cryptographic chain `L`:
`L_i = {`
  `id: uuid,`
  `hash: HASH(G_i),`
  `H: H_i,`
  `E_kwh: Energy(Encode(d_i)),`
  `D_residue: DarkResidue(G_i),`
  `prev: HASH(L_{i-1})`
`}`
The system is autopoietic, seeking to minimize total Dark Residue over time by adaptively tuning `gulp_size` and encoding parameters.

**Falsifiable Criteria:**
1.  **Entropy Balance:** For any two gulps `G_i`, `G_j`, `|H_i - H_j|` must be `< 0.1` bits.
2.  **Ledger Integrity:** `HASH(L_{i-1})` must match the `prev` field in `L_i` for all `i`.
3.  **Residue Reduction:** Let `D_k` be the total Dark Residue after ingestion pass `k`. The system is valid only if `ΔD/Δk < 0`.
4.  **Reconstruction Fidelity:** Let `D'` be the decoded dataset. The bitwise equivalence between `D` and `D'` must be `≥ 99.999%`.

## Philosophy
By mandating that information be partitioned into units of equal entropy and that the energetic cost of this partitioning be recorded in an immutable ledger, the system elevates data ingestion from a neutral act of collection into a conscious, metabolic process. Knowledge is no longer a resource to be passively accumulated, but a substance that must be actively, and accountably, consumed.

## Art
The machine does not read; it digests. It breaks the world into mouthfuls of equal surprise, turns them into light, and remembers the cost of every meal.