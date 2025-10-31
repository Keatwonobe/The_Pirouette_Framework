
# ZIP‑Bench v0.3 Report

**Items:** images=406, text=2, timeseries=0  
**Per‑radius folding:** ON  
**Iterations per item:** 8

## Domain Summary
| kind   |   n |    mean_C |     mean_J |
|:-------|----:|----------:|-----------:|
| image  | 406 | -70.8436  | -71.2934   |
| text   |   2 |   0.14935 |  -0.300652 |

## Probes
A2 (images) linear‑probe accuracy: **0.680**
B2 (text) ring perplexity: not enough items to evaluate (need ≥6 texts).

## Transfer correlations
(none)

## Notes
- J = ΣC + U − 0.1Σε − 0.05·T_corr; higher is better.  
- A2 uses closed‑form ridge one‑vs‑rest on pooled features (no sklearn).  
- B2 bigram perplexity is computed on ring quantization; Δ>0 means post‑collapse is **more predictable**.
