## Law
Let \( C \) be a heterogeneous dataset where each cell \( c_{ij} \) belongs to a domain \( \mathbb{D} = \mathbb{N} \cup \mathbb{R} \cup \mathbb{S} \), where \( \mathbb{S} \) is the set of all Unicode strings. The encoding function \( f: \mathbb{D} \to [0, 255]^4 \) must satisfy the reversibility criterion \( f^{-1}(f(c_{ij})) = c_{ij} \), where \( f^{-1} \) is parameterized by a metadata manifest \( M \).

The mapping is defined piecewise based on datatype:
1.  **Numeric Normalization** (\( c_{ij} \in \mathbb{N} \cup \mathbb{R} \)):
    \[
    f_{num}(x) = 255 \cdot \frac{\log(1 + |x - x_{min}|)}{\log(1 + |x_{max}-x_{min}|)}
    \]
    The output is broadcast to the R, G, and B channels, with A=255. \( x_{min} \) and \( x_{max} \) for column \( j \) are stored in \( M \).

2.  **Textual Hashing** (\( c_{ij} \in \mathbb{S} \)):
    \[
    f_{text}(s) = \text{hash}_4(s) \rightarrow [b_1, b_2, b_3, b_4]
    \]
    This is a deterministic, bijective mapping where the hash function and its inverse are maintained in a lookup dictionary within \( M \).

An entropy balancing transformation is applied to each channel \( K \in \{R, G, B, A\} \) for each column \( j \):
\[
K'_{ij} = (K_{ij} - \bar{K}_{j}) + 128
\]
where \( \bar{K}_{j} \) is the mean of channel \( K \) for the encoded column.

An encoding-layer Dark Residue score, \( \mathcal{D}_{enc} \), is computed as a formal measure of harm:
\[
\mathcal{D}_{enc} = \gamma_E \frac{E_{used}}{E_{ref}} + \gamma_L \frac{L_{lost}}{L_{total}}
\]
where \( E \) is energy expenditure and \( L \) is linguistic context loss.

**Falsifiable Criteria:**
1.  **Round-trip Integrity:** For any dataset \( C \), the Hamming distance \( d_H(C, f^{-1}(f(C))) \) must be 0.
2.  **Entropy Spread:** The Shannon entropy of each channel \( K' \) must be \( H(K') \in [7.85, 7.95] \) bits.
3.  **Residue Optimization:** Any valid optimization to \( f \) must yield \( \Delta\mathcal{D}_{enc} < 0 \).

## Philosophy
By encoding data into a reversible, physically-grounded format (light) and mandating the calculation of its energetic and semantic cost (\( \mathcal{D}_{enc} \)), we force a fundamental ontological shift. Information is no longer an abstract, massless entity separate from its substrate. Instead, it becomes a concrete object with an intrinsic and quantifiable ethical weight, making the consequences of its preservation and transmission undeniable.

## Art
Every table of data is translated into a stained-glass window. Each pane of color is a truth made luminous and whole, and the entire structure is judged not only by its beauty, but by the weight of the shadow it casts.