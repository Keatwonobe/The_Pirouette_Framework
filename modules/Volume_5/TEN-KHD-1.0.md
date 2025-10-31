---
id:           TEN-KHD-1.0
title:        Ki-Harmonic Decomposition
version:      1.0
parents:      []                            # Placeholder: To be filled manually
children:     []                            # Placeholder: To be filled manually
engrams:
  - concept:core-principle
keywords:     ['based', 'complex', 'components', 'constant', 'decompose', 'decomposition']
uncertainty_tag: Medium # Placeholder
module_type:  applied-analytics-toolkit
---

## §1 · Purpose
To decompose complex signals or patterns into their fundamental symmetry components based on the natural frequency ratios defined by the dual modes of the Ki constant ($K_i$).

---

## §2 · Conceptual Anchor
**Theoretical Insight**: The dual-mode Ki constant ($K_i^{rest} \approx 4.14159$ and $K_i^{motion} \approx 4.18879$) defines natural frequency ratios or phase evolution rates fundamental to resonant systems. [cite: 62, 256] Decomposing signals based on these Ki-harmonics can reveal underlying symmetries and separate components related to rest versus motion states.

**Key Pirouette Parameters**:
* **Ki Constant ($K_i$)**: This is the central parameter. Both $K_i^{rest}$ and $K_i^{motion}$ are used to define the basis functions (e.g., Ki-modulated wavelets) for decomposition and to identify resonant frequencies. [cite: 62, 65]
* **Phase (θ(t))**: The input signal is often converted to a form amenable to phase analysis, and Ki-modulated wavelets incorporate a phase term $\theta(t)$. [cite: 63, 64]
* **Symmetry (especially $4\pi/3$ related)**: The analysis specifically looks for symmetries related to Ki values, particularly $K_i^{motion} \approx 4\pi/3$. [cite: 63, 65]

---

## §3 · Input & Configuration
### 3·1 · Input Stream
* **Data Characteristics**: Signal data amenable to frequency and phase analysis (e.g., time series, spatial patterns that can be parameterized).
* **And Structure**: Numerical array or stream representing the signal.
* **Viable Data Set**: Sufficient signal length to resolve the lowest desired Ki-harmonic components. Must contain enough periods of the phenomena of interest.
* **Steps**: Convert the input signal to a form suitable for phase analysis (e.g., complex representation, analytic signal). [cite: 63] Denoising or detrending may be necessary.

### 3·2 · Operational Parameters
| Parameter | Description | Typical Range |
|-----------|-------------|---------------|
| `maxHarmonics (n)` | The maximum number of Ki-harmonics to consider in the decomposition. [cite: 65] | `Integer, e.g., 1 to 20, depending on signal complexity and desired resolution.` |
| `waveletBasis ($\psi_0(t)$)` | The base wavelet function to be modulated by the Ki-related phase terms. [cite: 64] | `Standard wavelets like Morlet, Mexican Hat, etc.` |
| `KiModesToUse` | Specify whether to use $K_i^{rest}$, $K_i^{motion}$, or both for decomposition. [cite: 65] | `['rest', 'motion', 'both']` |

---

## §4 · Procedure & Outputs
### 4·1 · Procedural Guide
1. Signal Preparation: Convert the input signal to a form amenable to phase analysis if not already in such a form. [cite: 63]
2. Define Ki Values: Set $K_i^{rest} = 4.14159$ and $K_i^{motion} = 4.18879$. [cite: 65]
3. Iterate Through Harmonics: For each integer harmonic 'n' up to `maxHarmonics`:
4.   a. Calculate Resonant Frequencies: $f_{n,rest} = K_i^{rest}/(2\pi n)$ and $f_{n,motion} = K_i^{motion}/(2\pi n)$. [cite: 63, 65]
5.   b. Generate Ki-Modulated Wavelets: Construct wavelets $\psi_{K_i}(t) = \psi_0(t) \cdot e^{iK_i\theta(t)}$ or use wavelets tuned to $f_{n,rest}$ and $f_{n,motion}$ (e.g., $\psi_{n,rest}(t)$ based on $f_{n,rest}$ and $K_i^{rest}$; $\psi_{n,motion}(t)$ based on $f_{n,motion}$ and $K_i^{motion}$). [cite: 64, 65]
6.   c. Apply Wavelet Transform: Compute the wavelet transform of the signal using the Ki-modulated wavelets for both rest and motion components to obtain coefficients (e.g., $c_{n,rest}$, $c_{n,motion}$). [cite: 65]
7.   d. Harmonic Separation/Energy Calculation: Store or sum the energy (e.g., squared magnitude of coefficients) for components resonant with $K_i^{rest}$ and $K_i^{motion}$ separately. This step effectively performs the harmonic separation $f_n(t)=\sum_{k}c_k e^{iK_i kt/n}$. [cite: 63, 65]
8. Resonance Detection: Identify dominant harmonics by finding peaks in the energy spectrum of the rest and motion components. [cite: 63, 65]
9. Rest-Motion Separation Analysis: Compare the energy or amplitude of components resonant with $K_i^{rest}$ versus $K_i^{motion}$ to distinguish between stationary and dynamic aspects of the signal. [cite: 63]
10. Symmetry Analysis: Quantify symmetry structures in the signal, particularly those related to $K_i^{motion} \approx 4\pi/3$ periodicities or phase relationships. [cite: 63, 65]

### 4·2 · Output Interpretation
* **Data Structure**: A set of components (e.g., energy or amplitude coefficients) for harmonics related to $K_i^{rest}$ and $K_i^{motion}$. Identification of dominant harmonics. A symmetry metric. [cite: 65] Optionally, a reconstructed signal based on selected Ki-harmonic components. [cite: 65]
* **Insights And Derivations**: Identification of hidden periodicities and symmetries that are specifically aligned with Ki constants. Separation of signal components associated with 'rest' states versus 'motion' states. Detection of phase transitions between these states. Understanding of rotational or phase-based symmetries within the data.
* **Guidelines**: Strong components at frequencies $f = K_i/(2\pi n)$ indicate Ki-harmonic resonance. [cite: 63] A higher energy in $K_i^{rest}$ components suggests system stability or stationary behavior, while dominant $K_i^{motion}$ components indicate dynamic activity or propagation. Symmetry metrics reveal the degree of Ki-related order.

---

## §5 · Core Equations
### Ki-Modulated Wavelet
$$ \psi_{K_i}(t) = \psi_0(t) \cdot e^{iK_i\theta(t)} $$
A base wavelet $\psi_0(t)$ is modulated by a Ki-dependent phase term. [cite: 64]

### Ki-Harmonic Frequencies
$$ f_n = \frac{K_i}{2\pi n} $$
Characteristic frequencies for Ki-harmonic components, where n is an integer. [cite: 63] (Note: AMP implementation example uses $K_i/(2\pi n)$ which implies $K_i$ is an angular frequency. If $K_i$ is a phase constant as in $d\theta/d\tau = K_i f(\phi)$, then $f_n = K_i f(\phi)/(2\pi n)$ for some base cycle $f(\phi)$ or $K_i$ itself sets the scale for angular frequency in $e^{i K_i \omega_0 t / n}$). The AMP implementation example code implies $K_i$ is used directly in the numerator for a frequency, suggesting $K_i$ might be treated as $2\pi \times$ a fundamental cycle count here.

### Harmonic Component Separation (Conceptual)
$$ f_n(t) = \sum_k c_k e^{iK_i kt/n} $$
Decomposition of the signal into components with periods related to $K_i$. [cite: 63] Operationally achieved via wavelet transforms tuned to Ki-related frequencies.

### Symmetry Quantification (Example: $4\pi/3$ related)
$$ \text{SymmetryMetric} = \text{QuantifySymmetry}(\text{signal}, 4\pi/3) $$
Measures the strength of symmetries related to $K_i^{motion} \approx 4\pi/3$. [cite: 63, 65] The specific quantification method is not detailed in AMP but would involve phase analysis.

---

## §6 · Assemblé
This module transforms data into insight by quantifying a core system property according to Pirouette Framework principles.

---

## §7 · Integration & Use Cases
### 7·1 · Integration Hooks
* **Dependencies**: Requires a signal suitable for frequency/phase analysis. May use outputs from Stochastic Gulping to analyze specific segments of a larger data stream.
* **Applications**: Results can be used to filter signals for Ki-resonant components, classify system states (rest vs. motion), or provide features for more complex pattern recognition models. Can feed into 'Stability Optimization Frameworks'.
* **With Combined Workflows**: A core component of 'Multi-Scale Coherence Analysis' (often combined with Stochastic Gulping and Temporal Coherence Spectrum Analysis) [cite: 91, 93] and 'Stability Optimization Framework'. [cite: 98]

### 7·2 · Use Cases
* Identifying hidden periodicities in complex data (e.g., financial time series, astrophysical signals). [cite: 66]
* Analyzing rotation and symmetry patterns in signals (e.g., image analysis, molecular vibrations). [cite: 66]
* Separating stationary and dynamic components in evolving systems. [cite: 66]
* Detecting phase transitions between rest and motion states (e.g., in physical systems, biological activity). [cite: 66]

---

### Version Notes
*1.0* — Initial conversion from JSON definition.
