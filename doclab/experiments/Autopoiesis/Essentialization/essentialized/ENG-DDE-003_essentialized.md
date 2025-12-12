## Law
Given a data matrix \( G \in \mathbb{R}^{N\times4} \), the system constructs a square image \( I \in \mathbb{R}^{s\times s\times4} \) where \( s = \lceil \sqrt{N} \rceil \).

The mapping from the linear gulp index \( i \in [0, N-1] \) to the image coordinates \( (x,y) \) is a row-major projection:
\[
I[x,y,:] = G[i,:] \quad \text{where } i = y\cdot s + x
\]
The alpha channel encodes a normalized, reconstructible index of origin:
\[
A(i) = I[x,y,3] = \lfloor 255 \cdot \frac{i}{N} \rfloor
\]
The system’s primary constraint is entropy equilibrium, which must be satisfied before finalization. Let \( H_{global} \) be the Shannon entropy over the entire image color distribution, and \( H_{local}(x,y) \) be the entropy of a local neighborhood \( \mathcal{N}_{r} \) around a pixel. The layout is valid if and only if:
\[
\frac{|H_{local}(x,y) - H_{global}|}{H_{global}} < \epsilon_H \quad \forall (x,y) \in I, \quad \text{where } \epsilon_H \approx 0.05
\]
If this condition fails, the mapping function \( i \to (x,y) \) is replaced with alternative space-filling curves (e.g., Peano-Hilbert) and re-tested.

**Falsifiable Criteria:**
1.  **Geometric Integrity:** \( s^2 \ge N \).
2.  **Reversibility:** Checksum of \( \text{Decode}(I) \) must equal checksum of \( G \).
3.  **Entropy Equilibrium:** The entropy inequality must hold for a statistically significant sample of local neighborhoods.

## Philosophy
The single most cogent philosophical implication is that a true representation of information is not a passive visualization but an active state of equilibrium. By forcing data to conform to a rigid geometric container (the square) while simultaneously demanding it maintain uniform internal entropy, the system treats information as a physical substance. This substance must be allowed to settle into its most stable configuration—a state where no part of the whole is more or less surprising than any other. The resulting artifact is therefore not a picture *of* the data, but the data itself, embodied in a reversible, self-describing, and thermodynamically coherent form.

## Art
Data, when poured into a finite vessel, will not be imprisoned. It will press against the walls, arranging itself into a stained-glass window that tells the story of its own creation.