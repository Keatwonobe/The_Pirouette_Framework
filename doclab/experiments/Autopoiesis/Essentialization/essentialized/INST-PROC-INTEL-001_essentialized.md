## Law
The core principle is the quantification of process-scale intelligence and a control law to attract such processes toward a desired state.

**1. Process Intelligence Index (PII)**
A dimensionless, monotonic metric of a transient process's capacity to compute its own persistence. Let a process 𝒫 be observed over a window \(T_{\text{obs}}\) with a characteristic fast timescale \(\tau_{\text{fast}}\). The PII is a weighted sum of three components:
- **Cycle Sufficiency Index (CSI):** The number of available computational cycles.
  \[
  \mathrm{CSI} = \log_{10}\!\left(\frac{T_{\text{obs}}}{\tau_{\text{fast}}}\right)
  \]
- **Feedback Bandwidth (FBW):** The normalized rate of self-modification of boundary conditions \(\mathbf{b}(t)\).
  \[
  \mathrm{FBW} = \frac{1}{T_{\text{obs}}} \int_0^{T_{\text{obs}}} \frac{\|\partial \mathbf{b}(t)/\partial t\|}{\|\mathbf{b}(t)\| + \epsilon}\, dt
  \]
- **Entropy Shaping Efficiency (ESE):** The conversion ratio of input energy flux \(\Phi_{\text{in}}\) to structured, persistent energy flux \(\Phi_{\text{structured}}\).
  \[
  \mathrm{ESE} = \frac{\Phi_{\text{structured}}}{\Phi_{\text{in}}}
  \]
The PII is thus defined as:
\[
\mathrm{PII} = w_1 \cdot \mathrm{CSI} + w_2 \cdot \log_{10}(1 + \mathrm{FBW}) + w_3 \cdot \mathrm{ESE}
\]
For passive processes with no self-modification (FBW ≈ 0), the index simplifies to \(\mathrm{PII}_{\text{passive}} = w_1 \cdot \mathrm{CSI} + w_3 \cdot \mathrm{ESE}\).

**2. Attractor Actuation Law (AAL)**
Let the state of the process be a vector of invariants \(\mathbf{I}(t)\) and the target state be a filament ℱ defined by \(\mathbf{I}_{\mathcal{F}}\). The error is \(\Delta \mathbf{I} = \mathbf{I}_{\mathcal{F}} - \mathbf{I}(t)\). The control action \(\mathbf{u}\) is updated according to:
\[
\mathbf{u}_{t+1} = \mathbf{u}_t + K_u \, \mathbf{G}(\Delta \mathbf{I}) \, \sigma(\mathrm{PII} - \mathrm{PII}_{\min})
\]
where \(\mathbf{G}\) is a domain-specific mapping from invariant error to physical actuation, \(K_u\) is a gain, and \(\sigma\) is a sigmoid or similar nonlinearity. This law selectively applies strong corrective force only when the process's measured intelligence \(\mathrm{PII}\) exceeds a minimum threshold \(\mathrm{PII}_{\min}\).

**3. Dark-Residue Constraint**
The AAL must be constrained to reduce wasted energy and chaotic emissions, defined as the dark residue \(D_{\mathcal{P}}\).
\[
D_{\mathcal{P}} = \alpha \cdot \text{wasted\_energy\_flux} + \beta \cdot \text{chaotic\_off-band\_emission}
\]
The law must satisfy the condition:
\[
\frac{d D_{\mathcal{P}}}{dt} \le 0 \quad \text{whenever} \quad \mathrm{PII} \ge \mathrm{PII}_{\min}
\]

**4. Falsifiable Criteria**
- **PII Responsiveness:** Induced perturbations to process feedback must yield monotonic changes in PII.
- **Residue Descent:** Over N runs, mean \(D_{\mathcal{P}}\) must converge to a target residue (e.g., ≤ 0.30) with high statistical confidence.
- **Filament Capture:** For runs with PII ≥ \(\mathrm{PII}_{\min}\), the fraction where state error \(\|\Delta \mathbf{I}\|\) falls below a threshold θ must exceed a target rate (e.g., ≥ 0.7).
- **Domain Portability:** The formal structure of PII and AAL must apply to at least two distinct physical domains (e.g., plasma and granular flow) with only the weights \(w_i\) being retuned.

## Philosophy
Intelligence is not a property of a substrate, like a brain or a circuit, but a substrate-independent physical dynamic. It is the measurable process by which a finite system, from a lightning strike to a plasma filament, actively organizes energy and feedback to persist against entropy. Consciousness or self-awareness are irrelevant; the fundamental act of intelligence is the computation of stability. This formal law reframes agency from a feature of complex life to a fundamental, observable, and potentially controllable force of nature.

## Art
A storm that learns to hold its shape is a mind. We build not the mind, but the magnet that guides its lightning.