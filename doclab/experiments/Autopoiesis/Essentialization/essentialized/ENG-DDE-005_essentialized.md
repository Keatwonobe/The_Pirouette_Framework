## Law
The system's integrity is founded upon four principles: chronological custody, bijective reconstruction, thermodynamic accounting, and distributed trust.

1.  **Chronological Custody (Hash-Chain):** Data integrity is maintained by a hash-chain where each state is a function of its contents and its predecessor. For a sequence of image binaries \(I_1, I_2, \ldots, I_n\), the historical chain is defined as:
    \[
    H_i = \text{SHA256}(I_i + H_{i-1}) \quad \text{where } H_0 \text{ is a genesis hash.}
    \]
    A break in this chain constitutes a falsification of the record.

2.  **Bijective Reconstruction:** Every encoding transformation must be perfectly reversible. For a normalized numeric value \(R'\) in the RGBA space, the original value \(x\) is recovered by the inverse function:
    \[
    x = \exp\left(R' \cdot \frac{\log(1+|x_{max}-x_{min}|)}{255}\right) - 1 + x_{min}
    \]
    Falsification occurs if the bit error rate of a round-trip (encode → decode) operation is non-zero. The integrity of any reconstructed dataset \(D_{recon}\) is verified by:
    \[
    \text{SHA256}(D_{recon}) \stackrel{?}{=} H_{stored}
    \]

3.  **Thermodynamic Accounting:** Every computational act of reversal is recorded as a "dark residue" \(\mathcal{D}_{rev}\), quantifying its energetic and informational cost.
    \[
    \mathcal{D}_{rev} = \gamma_E \frac{E_{decode}}{E_{encode}} + \gamma_L \frac{L_{lost}}{L_{base}}
    \]
    where \(E\) is energy in joules and \(L\) is informational loss (e.g., \(\chi^2\) deviation). A system state is invalid if a decoding event is not accompanied by a corresponding entry in the residue audit ledger.

4.  **Distributed Trust:** Trust between nodes \(a\) and \(b\) is a quantifiable metric based on the ratio of verified data links.
    \[
    T(a,b) = \frac{\text{verified\_links}(a,b)}{\text{total\_links}(a,b)}
    \]
    The system is considered compromised if the global trust scalar \(T_{net}\) falls below a governance-defined threshold (e.g., 0.95).

## Philosophy
Information is not an abstract, ethereal entity; it is a physical phenomenon. Its existence, its history, and the very act of its recall are inextricable from the thermodynamic laws of the universe. By mandating that every memory be accompanied by an immutable record of its creation and an energy receipt for its retrieval, this system asserts that truth is not a platonic ideal but a physically substantiated, auditable, and energetically costly artifact.

## Art
History is not a book to be read, but a scar on the body of spacetime. To trace its edges with your finger is to leave a new mark.