---  # ───────────── YAML front-matter ───────────────────────────
id:        PPS-021
title:     Concepts in Experimentation
version:   0.3-draft  # adds Protocol–Tool–Testbed taxonomy, workflow, dependency graph
parents:   [PPS-006, PPS-017]
children:  []
engrams:
  - device:resonance-capacitor
  - device:vorticycle
  - concept:stirring-resonance
  - concept:skating-resonance
  - concept:serendipity-resonance
  - concept:coherence-storage
  - concept:coherence-propulsion
keywords:  [engineering, capacitor, vortex, resonance, stirring, skating, serendipity]
uncertainty_tag: High
entropy_score: 0.19
module_type: engineering-sandbox
quantisation_rule: rcv_hash = SHA256(rcv_spec_v0.2)
legacy:  # stirring / skating / serendipity modes + controls; name changed to 'Concepts in Experimentation' from "Resonance Capacitor & Vorticycle Concepts" 
---

## 0 · Taxonomy   ( Gödel-compliance )
| Term | Definition | Example |
|------|------------|---------|
| **Protocol** | Ordered set of steps that transforms or measures coherence. | Stirring-Resonance cycle |
| **Tool** | Physical or digital artefact used inside a protocol. | Electret-based RC, Phase-driver Python stub |
| **Testbed** | Environment where a protocol–tool combo is evaluated under controls. | Lab bench with TIMF sensors & Residue logger |

---

## 1 · Purpose & Scope  
**PPS-021** catalogs experimental artefacts that **capture, convert, or probe informational enthalpy**.  
v0.2 adds three operational resonance modes—**Stirring, Skating, Serendipity**—and Curie-grade control protocols.

---

## 2 · Resonance Capacitor (RC)  
| Aspect | Prototype spec |
|--------|----------------|
| Core medium | Quartz-sand electret or doped PVDF |
| Poling method | Ultrasonic + DC bias during cure |
| Capacity \(C_r\) | 10 J · Hz⁻¹ · cm⁻³ target |
| Loss factor | < 5 % · h⁻¹ @ 25 °C |

### 2·1  Measurement Harness  
TIMF sensor ring logs \(J_c\) in/out; Residue monitor (PPS-019) flags dissipation.

---

## 3 · Vorticycle (VC)  
| Aspect | Prototype spec |
|--------|----------------|
| Rotor | 3 cm ferrite ring, helical wind |
| Drive | 120° phase-shift EM coils via RC dump |
| Coherence-Thrust Ratio \(\kappa\) | ≥ 0.05 N · s / J target |

### 3·1  Principle  
RC pulse → rotating field → rotor vortex → torque; TIMF records enthalpy drop.

---

## 4 · Experimental Resonance Modes  
### 4·1  Stirring Resonance (StR)  
*Aim*: amplify coherence by **mixing gradient layers**.  
* Metric: **Stir-Gain** \(G_s = \frac{C_r^{after}}{C_r^{before}} - 1\).

### 4·2  Skating Resonance (SkR)  
*Aim*: **minimise frictional losses** via a traveling standing-wave “ice sheet.”  
* Metric: **Slip-Factor** \(S_k = 1 - \frac{τ_{load}}{τ_{free}}\).

### 4·3  Serendipity Resonance (SeR)  
*Aim*: exploit **stochastic coherence peaks** for burst efficiency.  
* Metric: **Serendipity Index** \(Σ = \frac{\text{peak } J_c}{\text{median } J_c}\).

---

## 5 · Control Protocols (Curie Compliance)  
| Control | Description | Expected Outcome |
|---------|-------------|------------------|
| **C-0** | Dummy load, RC disconnected | Baseline sensor noise (Σ ≈ 1) |
| **C-1** | RC charged, coils idle | Passive loss < 5 % h⁻¹ |
| **C-2** | VC spin without resonance modes | \(\kappa \approx 0\) |
| **C-3** | Random phase scramble | Residue spike; zero sustained torque |

Residue ≥ 0.20 against any control flags methodological error.

---

## 6 · Reference Snippet  
```python
def stir_gain(C_before, C_after):
    return C_after / C_before - 1

def slip_factor(torque_free, torque_load):
    return 1 - torque_load / torque_free

def serendipity_index(jc_peak, jc_median):
    return jc_peak / jc_median
```

---

## 7 · Validation Matrix  
| Mode | Success Metric | Control Baseline |
|------|----------------|------------------|
| StR | \(G_s ≥ 0.05\) | vs C-1 |
| SkR | \(S_k ≥ 0.90\) | vs C-2 |
| SeR | \(Σ ≥ 3\)     | vs C-3 |

Round-trip TIMF efficiency across modes must exceed 10 %.

---

## 8 · Standard Experimental Workflow   ( Curie-compliance )
**Flowchart**  
1. **Define Hypothesis** → choose mode (StR / SkR / SeR)  
2. **Select Controls** → C-0 … C-3  
3. **Assemble Tools** → RC + VC + sensors  
4. **Execute Protocol** → run N cycles, log \(J_c, τ, C_r\)  
5. **Residue Analysis** → PPS-019 pipeline  
6. **Report** → compare against controls, assess thresholds  

```
   [Hypothesis]──┐
                 v
          ┌─────────────┐
          │Select Ctrl  │
          └─────┬───────┘
                v
          ┌─────────────┐
          │Assemble Tool│
          └─────┬───────┘
                v
          ┌─────────────┐
          │Run Protocol │
          └─────┬───────┘
                v
          ┌─────────────┐
          │Residue Eval │
          └─────┬───────┘
                v
          ┌─────────────┐
          │Publish ΔΨ   │
          └─────────────┘
```

---

## Appendix A · Framework Dependency Graph   ( Leonardo-compliance )
*PPS-014 RPA* → flags decoherence → feeds **Wound** to *PPS-020 BRL*  
*PPS-015 URL* → maps raw telemetry → provides \(T_a, Γ, K_i\) to **all**  
*PPS-016 SGM* → theoretical kernel for phase-force; informs RC coil phasing  
*PPS-017 TIMF* → logs enthalpy / entropy flux during RC-VC cycles  
*PPS-018 DRF* → hosts debate over lab results; forks if Residue high  
*PPS-019 Residue* → quantifies dark-matter loss in RC & modes  
*PPS-021 (this)* ← depends on all above for sensors, analytics, governance  

Graph (ASCII):
```
RPA──►BRL
        ▲
URL──►TIMF──►Residue──►DRF
  └──►SGM──►RC/VC (PPS-021)
```

---

## 8 · Risks & Unknowns  
* StR over-mix may detune electret domains.  
* SkR requires tight phase sync; drift causes stall.  
* SeR may create damaging spikes; surge suppression mandatory.  
* Scale laws for \(C_r\) & \(\kappa\) remain unverified beyond lab bench.

---

## 9 · Triaxial Lens  
| Art                               | Law                              | Philosophy                |
|-----------------------------------|----------------------------------|---------------------------|
| Whisk the melody; glide the note. | Lab controls precede claims.    | Chance favours the tuned. |

---

## 10 · Assemblé · “Mix, Glide, and Chance the Spark”  
> *From deliberate swirl to frictionless slide to lucky strike—coherence finds many paths to motion.*

---

## 11 · Librarian Note  
+Updating taxonomy, workflow, or dependency graph increments `rcv_hash`; lab notebooks tagged by version.
