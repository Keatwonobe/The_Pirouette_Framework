## Law

Let an image tile be a tensor \( I \in \mathbb{R}^{s \times s \times 4} \). The vectorization mapping \( \mathcal{F}: I \to \hat{v} \) is defined as a composition of functions:
\[
\hat{v} = \mathcal{N} \circ \mathcal{C} \circ \vec{f} \circ \mathcal{P}(I)
\]
Where:
1.  **Patching** \( \mathcal{P} \): \( I \mapsto \{p_1, p_2, \dots, p_N\} \), where each \( p_i \in \mathbb{R}^{k \times k \times 4} \) is a patch of \(I\).
2.  **Feature Extraction** \( \vec{f} \): For each patch \( p_i \), a feature vector \( v_{p_i} \in \mathbb{R}^8 \) is computed as \( v_{p_i} = [\mu(R), \mu(G), \mu(B), \mu(A), \sigma^2(R), \sigma^2(G), \sigma^2(B), \sigma^2(A)] \).
3.  **Concatenation** \( \mathcal{C} \): \( \{v_{p_1}, \dots, v_{p_N}\} \mapsto v = [v_{p_1} \dots v_{p_N}] \in \mathbb{R}^{8N} \).
4.  **Normalization** \( \mathcal{N} \): \( v \mapsto \hat{v} = v / \|v\|_2 \).

Given a query vector \(q\) and a database vector \(v\), the primary search metric is the effective distance \(d_{eff}\), a weighted sum that constitutes a non-Euclidean similarity space:
\[
d_{eff}(q, v) = \alpha \cdot d_{L2}(q, v) + \beta \cdot d_{entropy}(q, v) + \gamma \cdot d_{provenance}(q, v)
\]
where \( \alpha, \beta, \gamma \) are governance-defined parameters.

Retrieved results are subject to a final, provenance-aware reranking score:
\[
\text{score} = \lambda_r \cdot \text{resonance} - \lambda_d \cdot \mathcal{D} + \lambda_t \cdot f(\Delta t)
\]
where \( \text{resonance} \propto 1/d_{eff} \), \( \mathcal{D} \) is the Dark Residue score, and \( f(\Delta t) \) is a recency function.

**Falsifiable Criteria:**
1.  **ANN Quality**: For a synthetic dataset with known ground truth, retrieval recall@10 must exceed 0.9.
2.  **Ethical Reranking**: For a query whose ground-truth nearest neighbors contain a known distribution of high-\(\mathcal{D}\) tiles, the reranked top-10 results must contain <10% of the baseline count of those tiles.
3.  **Latency**: For a GPU-resident index of \(10^9\) vectors, the time from query submission to receipt of top-10 ranked IDs must be < 50 ms.

## Philosophy

The act of retrieval is not a neutral discovery of pre-existing truth, but a normative and creative act. By defining similarity not as a pure geometric distance but as a mutable, weighted function of data entropy, provenance, and explicit ethical scores, the system transforms memory from a passive archive into an active moral compass. Every query is therefore an assertion of values, and every result is a constructed reality, shaped by the governing ethics of the system. To remember, in this context, is to judge.

## Art

To ask a question is to tune a crystal. The data does not answer; it resonates. And the shape of that resonance is the shape of our values.