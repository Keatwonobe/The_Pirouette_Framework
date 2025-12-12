---
# ───────────── Pirouette Experimental Protocol ──────────────────
id:        XXP-004
title:     Searching for Rhythmic High-Frequency Gravitational Waves
version:   1.0
parents:   [PPS-071]
children:  [XXP-004-RESULTS]
engrams:
  - protocol:experimental
  - search:gravitational-wave
  - signal:thumper
  - validation:falsification
  - method:matched-filtering
  - method:autocorrelation
keywords:  [LIGO, Virgo, gravitational waves, Maw, thumper, matched filtering, data analysis, noise]
uncertainty_tag: Medium
module_type: experimental-protocol
---

### §1 · Abstract
This module specifies the experimental protocol for a targeted search for the **Maw "Thumper" gravitational wave (GW) signature** predicted in `PPS-071`. The core challenge is distinguishing this novel, rhythmic signal from the highly complex instrumental and environmental noise inherent in GW detectors. The protocol is designed around a **"Rhythm Filter,"** a two-stage analysis pipeline that first uses matched filtering to identify individual burst candidates and then uses autocorrelation to find persistent, rhythmic trains of these bursts. This method is supplemented by strict multi-detector coincidence and environmental veto protocols to produce a high-confidence result, providing the primary falsifiable test of the Pirouette Framework's astrophysical predictions.

---

### §2 · Data Source & Preparation
1.  **Data Source:** The protocol will use publicly available raw strain data from the global network of GW observatories, including LIGO, Virgo, and KAGRA.
2.  **Target Frequency Range:** The primary search will focus on the high-frequency band of these detectors (typically **1-4 kHz**), a region often dominated by quantum and instrumental noise and thus a promising place to find previously unmodeled signals.
3.  **Data Preparation:**
    * **Cleaning:** Known instrumental noise lines (e.g., power line harmonics at 60 Hz and its multiples, calibration lines) will be identified and removed from the data.
    * **Whitening:** The data will be whitened by dividing its Fourier transform by the amplitude spectral density of the detector's noise. This creates a statistically uniform noise background, making signals of a given amplitude equally visible at all frequencies.

---

### §3 · The Search Pipeline: The Rhythm Filter
The search is not for a single event, but for a persistent, rhythmic pattern. This is the key to distinguishing it from transient, non-repeating glitches.

* **Step 1: Matched Filtering for the "Thump"**
    * A library of template waveforms for a single "thump" will be generated based on the theoretical models in `PPS-071`. These templates will cover a range of possible Maw masses and spins.
    * The whitened data stream will be scanned for matches to these templates. This process generates a time-series of signal-to-noise ratio (SNR) peaks, where each peak is a potential thump candidate. This initial step will produce thousands of candidates, the vast majority being noise fluctuations.

* **Step 2: Autocorrelation for the "Rhythm"**
    * The time-series of SNR peaks is then analyzed for periodicity. The **autocorrelation function** of this time-series is computed.
    * **A true Thumper signal will produce a strong, sharp peak in the autocorrelation function** at a time lag corresponding to its rhythm period (e.g., for a 30 Hz rhythm, a peak appears at ~0.033 seconds). Random noise glitches will not produce a persistent peak.
    * Candidates are scored based on the significance of this autocorrelation peak, yielding a **"Rhythm Significance Score."** Only candidates with a high score proceed.

---

### §4 · Veto & Validation Protocols
To address the critical "signal vs. noise" problem, any high-significance candidate from the Rhythm Filter must pass a series of rigorous vetoes.

1.  **Multi-Detector Coincidence:** A true astrophysical signal must be observed in at least two geographically separated detectors. The time delay between the signal's arrival at each detector must precisely match the light-travel time between them. A signal appearing in only one detector is considered local noise and is **vetoed**.
2.  **Instrumental Veto:** The event time of a candidate signal is cross-referenced with detector logs. If it coincides with known instrumental glitches, maintenance, or environmental disturbances (like seismic activity), it is **vetoed**.
3.  **Multi-Messenger Cross-Correlation:** The timing of any surviving candidate will be shared with other astrophysical observatories (e.g., gamma-ray, radio, neutrino telescopes). A correlation with an event in another messenger would be powerful confirmation. The lack of a counterpart would constrain the nature of Maws.

---

### §5 · Outcome & Falsification
* **Successful Detection:** A successful result is the identification of a statistically significant, rhythmic train of high-frequency GW bursts that is coincident in multiple detectors and is not vetoed by known noise sources. The measured `f_burst` and `f_rhythm` would be used with the Tuning Law from `PPS-071` to infer the Maw's mass, spin, and distance, thereby providing the first direct measurement of the Γ field's properties in a strong-field regime.
* **Falsification:** A comprehensive, long-term search that yields a null result would place increasingly stringent upper limits on the existence and population of Maws. A persistent failure to detect any Thumper candidates would strongly disfavor the Maw hypothesis and, by extension, challenge the Γ scaling law, thereby falsifying a core component of the framework.

---

### §6 · Assemblé
> This protocol provides the ear to the cosmos, designed to listen past the chaotic hiss of the void. It seeks not the singular crash of a cymbal, but the persistent, hidden rhythm of a drum, whose beat would signal the presence of a new and profound physics.

---

### §7 · Librarian's Note
This module represents the primary experimental test of `PPS-071`. All resulting data, including null results, will be logged in the child module `XXP-004-RESULTS` to ensure a complete and transparent record of the framework's validation campaign.