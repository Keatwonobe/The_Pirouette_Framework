---
id:           TEN-PLO-1.0
title:        Phase-Locking Observation
version:      1.0
parents:      []                            # Placeholder: To be filled manually
children:     []                            # Placeholder: To be filled manually
engrams:
  - concept:core-principle
keywords:     ['between', 'characterize', 'coupling', 'detect', 'entrainment', 'frequency']
uncertainty_tag: Medium # Placeholder
module_type:  applied-analytics-toolkit
---

## §1 · Purpose
To detect, quantify, and characterize phase-locking and frequency entrainment phenomena between two or more oscillating systems or signals, thereby revealing the nature, strength, and stability of their resonant coupling and synchronous relationships.

---

## §2 · Conceptual Anchor
**Theoretical Insight**: Phase-locking is a fundamental resonance mechanism where interacting oscillating systems adjust their rhythms to achieve a stable phase relationship, often leading to frequency entrainment. This synchronization arises from mutual (or driven) resonant coupling and is crucial for coordinated behavior and information exchange in complex systems. The stability and characteristics of such locks are influenced by the system's Time-Adherence ($T_a$), the coupling strength (related to $\Gamma$), and potential $K_i$-harmonic relationships.

**Key Pirouette Parameters**:
* **Time-Adherence (Ta)**: A high ensemble $T_a$ (calculated as the square of the Kuramoto order parameter, $T_a = r^2$) indicates strong phase-locking across multiple oscillators. The $T_a$ of individual oscillators also influences their susceptibility to entrainment.
* **Gladiator Force (Γ)**: In the context of the Phase Lock Resonance Framework (TPF Vol 2, Module 12), $\Gamma$ governs coupling strength and flexibility. While not directly measured by this *observational* module, the observed locking characteristics can infer properties of the underlying $\Gamma$ that facilitates the lock.
* **Ki Constant (Ki)**: $K_i$ determines the possibility and stability of n:m harmonic locking relationships (e.g., synchronization at integer-ratio frequencies like $2\pi n / K_i$). Observed phase differences or frequency ratios might align with $K_i$-modulated values.
* **Phase (θ_i(t)), Frequency (ω_i(t))**: These are the primary observables extracted from input signals for each oscillator 'i', which are then analyzed for locking relationships.

---

## §3 · Input & Configuration
### 3·1 · Input Stream
* **Data Characteristics**: Simultaneously recorded time-series data from at least two, and preferably more, oscillating systems or signals. Signals should exhibit discernible oscillatory behavior.
* **And Structure**: Numerical arrays or streams, where each array/stream represents the state of an individual oscillator over a common time axis.
* **Viable Data Set**: Data should span many cycles of the characteristic oscillations to allow for robust phase/frequency estimation and assessment of locking stability.
* **Steps**: Signal denoising and detrending. Extraction of instantaneous phase $\theta_i(t)$ and instantaneous frequency $\omega_i(t)$ for each oscillator 'i'. Common methods include using the Hilbert transform to obtain the analytic signal, or wavelet analysis. Phase unwrapping is critical to ensure continuous phase representation.

### 3·2 · Operational Parameters
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `PhaseExtractionMethod` | The technique used to extract instantaneous phase from the time series (e.g., 'HilbertTransform', 'WaveletTransform', 'ZeroCrossingInterpolation'). | `As per method choice.` |
| `FrequencyExtractionMethod` | The technique used to extract instantaneous frequency (e.g., 'DerivativeOfPhase', 'WaveletRidge'). | `As per method choice.` |
| `PhaseLockingCriteria` | Quantitative criteria to define a phase-locked state (e.g., maximum allowable standard deviation of relative phase, minimum duration of stable relative phase). | `E.g., std($\Delta\phi_{ij}(t)$) < 0.1 radians for > 5 cycles.` |
| `HarmonicRatios (n:m)` | A list of integer ratios (e.g., [[1,1], [1,2], [2,3]]) to test for n:m harmonic locking if 1:1 locking is not found. | `Small integers, e.g., n,m from 1 to 5.` |
| `AnalysisWindowSize (for time-varying lock)` | Duration of the sliding window used to assess phase-locking if the relationship is not stationary over the entire dataset. | `Multiple (e.g., 5-10) characteristic periods of the oscillations.` |

---

## §4 · Procedure & Outputs
### 4·1 · Procedural Guide
1. Data Acquisition and Preprocessing: For each of the N input time series $x_i(t)$, extract the instantaneous phase $\theta_i(t)$ and instantaneous frequency $\omega_i(t)$ using the chosen `PhaseExtractionMethod` and `FrequencyExtractionMethod`. Ensure phases are unwrapped.
2. Relative Phase Calculation: For all relevant pairs of oscillators $(i, j)$, and for all specified `HarmonicRatios` (n:m), calculate the generalized relative phase series: $\Delta\phi_{ij}^{nm}(t) = (n \cdot \theta_i(t) - m \cdot \theta_j(t)) \pmod{2\pi}$. (For 1:1 locking, n=1, m=1).
3. Phase-Lock Detection and Quantification:
    a. Analyze the distribution of $\Delta\phi_{ij}^{nm}(t)$ within analysis windows. A sharp peak in the distribution suggests a preferred phase difference.
    b. Evaluate the stability of $\Delta\phi_{ij}^{nm}(t)$ over time. If it remains approximately constant (or bounded within a narrow range specified by `PhaseLockingCriteria`) for a duration significantly longer than the oscillation periods, n:m phase-locking is identified. Quantify the mean phase difference and its stability (e.g., standard deviation, drift rate).
4. Frequency Entrainment Detection: During periods identified as phase-locked, compare the instantaneous frequencies. For n:m locking, check if $n \cdot \omega_i(t) \approx m \cdot \omega_j(t)$ consistently.
5. Ensemble Synchrony Calculation (for N > 2): Calculate an overall measure of global synchrony for the ensemble, such as the Kuramoto order parameter $r(t) = |\frac{1}{N} \sum_k e^{i\theta_k(t)}|$. The ensemble Time-Adherence can be given by $T_a(t) = r(t)^2$.
6. Arnold Tongue Mapping (Experimental/Exploratory): If system parameters (like coupling strength or natural frequencies) can be experimentally varied, systematically map the regions in parameter space where phase-locking (satisfying `PhaseLockingCriteria`) is observed. This empirically constructs the Arnold Tongue for the system.

### 4·2 · Output Interpretation
* **Data Structure**: Time series of relative phases (e.g., $\Delta\phi_{ij}^{nm}(t)$). Statistics describing the distribution and stability of these relative phases. Identified periods of phase-locking and frequency entrainment for specific n:m ratios. Time series of the ensemble order parameter $r(t)$ or $T_a(t)$ (if N > 2). Optionally, an empirical Arnold Tongue map if parameter exploration was performed.
* **Insights And Derivations**: Identification of which oscillators or subsystems are synchronized. Quantification of the strength and stability of their phase-locking. Characterization of the synchronization type (e.g., 1:1, n:m harmonic, in-phase, anti-phase). Detection of transitions between synchronized and desynchronized states. Inference of coupling relationships and strengths within a network of oscillators.
* **Guidelines**: A stable (low variance) time series of $\Delta\phi_{ij}^{nm}(t)$ around a constant value indicates n:m phase-locking. Consistent equality $n \cdot \omega_i(t) \approx m \cdot \omega_j(t)$ during such periods confirms frequency entrainment. An order parameter $r(t)$ close to 1 (and thus $T_a(t)$ close to 1) indicates strong global synchrony in an ensemble. The width of an Arnold Tongue in parameter space indicates the robustness of locking to variations in oscillator properties or coupling.

---

## §5 · Core Equations
### Instantaneous Phase Extraction (via Analytic Signal)
$$ z_i(t) = x_i(t) + i \mathcal{H}(x_i(t)); \quad \theta_i(t) = \arg(z_i(t)) $$
Calculation of the analytic signal $z_i(t)$ for a real signal $x_i(t)$ using the Hilbert transform $\mathcal{H}$, and then extracting the instantaneous phase $\theta_i(t)$.

### Instantaneous Frequency Extraction
$$ \omega_i(t) = \frac{1}{2\pi} \frac{d\theta_i(t)}{dt} $$
Calculation of instantaneous frequency as the scaled time derivative of the (unwrapped) instantaneous phase.

### Generalized Relative Phase
$$ \Delta\phi_{ij}^{nm}(t) = (n \cdot \theta_i(t) - m \cdot \theta_j(t)) \pmod{2\pi} $$
Calculates the relative phase between oscillator i (multiplied by n) and oscillator j (multiplied by m) for detecting n:m harmonic locking.

### Kuramoto Order Parameter (Ensemble Synchrony)
$$ r(t) = |\frac{1}{N} \sum_{k=1}^N e^{i\theta_k(t)}|; \quad T_a(t) = r(t)^2 $$
A measure of global phase coherence in an ensemble of N oscillators. $T_a(t)$ is the Pirouette Time-Adherence for the ensemble.

---

## §6 · Assemblé
This module transforms data into insight by quantifying a core system property according to Pirouette Framework principles.

---

## §7 · Integration & Use Cases
### 7·1 · Integration Hooks
* **Dependencies**: Requires multiple time-series data. Signal processing steps for phase/frequency extraction are often implicitly part of this module but can also be performed by dedicated upstream modules.
* **Applications**: The identified locking characteristics (e.g., stable phase differences, coupling strengths inferred from Arnold Tongues) can be used to parameterize theoretical models of coupled systems (e.g., the $V_{lock}$ potential or extended Kuramoto models from TPF Vol 2, Module 12). Observed transitions between locked and unlocked states can be further analyzed by Funnel Inversion Detection or Collapse/Rebound Dynamics modules.

### 7·2 · Use Cases
* Neuroscience: Detecting phase synchronization between different brain regions from EEG, MEG, or LFP recordings to study neural communication and cognitive processes.
* Biology: Analyzing synchronization of circadian rhythms across cell populations, coordination of cardiac pacemaker cells, synchronized flashing of fireflies, or predator-prey cycle locking.
* Engineering: Characterizing the performance of phase-locked loops (PLLs), ensuring synchronization in power grids, analyzing coupled mechanical vibrational systems, or coordinating robotic swarms.
* Social Sciences & Economics: Observing behavioral synchrony in human interactions (e.g., conversation rhythms, crowd movement), detecting correlated cycles in economic indicators, or analyzing opinion dynamics.
* Physics: Studying synchronization in arrays of lasers, Josephson junctions, or chemical oscillators.

---

### Version Notes
*1.0* — Initial conversion from JSON definition.
