---  # ───────────── YAML front-matter ─────────────────────────────
id:        PPS-013
title:     Volume-5 Summary & Cross-Walk
version:   0.2
parents:   [PPS-001, PPS-012]
children:  [Legacy-Guide, Vol-6+ migration scripts]
engrams:
  - synthesis:crosswalk
  - concept:migration-map
  - directive:legacy-alias
  - provenance:crosswalk-seed
keywords:  [summary, cross-walk, legacy, mapping, migration]
uncertainty_tag: Low
entropy_score: 0.02
module_type: core-doc
quantisation_rule: xwalk_hash = SHA256(crosswalk_table)
---

## 1 · Purpose & Scope  
Provide a **one-page bridge** for readers migrating from **Volumes 1–4**  
to the new **Volume 5 (“Pirouette Pivot Series”)**.  Each major section of
the legacy corpus is mapped to its canonical replacement module.

---

## 2 · Cross-Walk Table  

| Legacy Vol-§ | Old title (2023)                            | New PPS-ID | New section / note |
|--------------|---------------------------------------------|------------|--------------------|
| Vol-1 §2.1   | Unified Theoretical Foundation              | **PPS-001** | Field Lagrangian unchanged; see §2 of PPS-001 |
| Vol-1 §3.4   | Foundational Parameters (static)            | **PPS-003** | Now triaxial vector + keyed JSON |
| Vol-1 §4     | Parameter Glossary (flat list)              | **PPS-007** | Registry table (machine-readable) |
| Vol-1 §5     | Entity / Wound Intro                        | **PPS-008** | Expanded with operational cues |
| Vol-1 §7     | “Metabolising the Framework” (chapters)     | **PPS-008 §5** | Condensed; see cheat-sheet (PPS-011) |
| Vol-2 §3     | Ki-Modes & Phase Algebra                    | **PPS-002** | Algebra formalised + spectral quantisation |
| Vol-2 §6     | Debate Engine Sketch                        | **PPS-005** | KRP Challenge-Vector Operator |
| Vol-3 §1     | Covariant Rewrite Appendix                  | **PPS-006** | Now core module, manifestly covariant |
| Vol-3 §4     | Simulation Log Spec                         | **PPS-010** | Unified Ritual & Simulation Interface |
| Vol-4 entire | Governance chapters A–C                     | **PPS-012** | Ascendant Protocol & Circuit-Breaker |
| —            | —                                           | **PPS-009** | Registry CI & hash guard (new) |
| —            | —                                           | **PPS-011** | Auto-generated Glossary & Cards |

*Rows not listed are deprecated or folded into the modules above.*

---

## 3 · Migration Guidelines  

1. **Imports** — Legacy LaTeX modules should replace  
   «\input{Vol-1/unified_foundation.tex}»  
   with  
   «\input{PPS-001_Unified_Theoretical_Foundation.md}».  
2. **Symbols** — Prefer `T_a.T_Q` over positional `Ta[0]`.  
3. **Debate scripts** — Rewrite classic “Critique Blocks” as KRP CV JSON; pass
   through **PPS-005** linter.  
4. **Governance motions** — Close any open Vol-4 issue threads; reopen under
   PPS-012 motion template.  

---

## 4 · Sample Legacy Alias File (auto-generated)

«json
{
  "Vol1_Entity": "Entity",
  "TA": "T_a",
  "GLADIATOR": "Γ",
  "PHI": "φ",
  "Wake": "Wound-Channel"
}
»

Build script `xwalk_alias_builder.py` writes this JSON so old notebooks
can import `pirouette.aliases` and run unchanged.

---

## 5 · CI Check (Legacy PDF ↔ PPS cross-ref)

«bash
#!/usr/bin/env bash
# legacy_pdf_check.sh
grep -q "Vol-1 §" legacy_notes.tex && \
  echo "⚠️  Legacy reference found — see PPS-013 table" && exit 1
»

---

## 6 · Triaxial Resonance Lens  

* **Art** — Cross-walk is a translation, turning old melody into new key.  
* **Law** — No duplicate sources of truth; every concept has one canonical PPS.  
* **Philosophy** — The garden sheds its leaves yet the tree persists.

---

## Assemblé · “Bridges & Lanterns”  
> *A lantern marks the path; a bridge carries the traveler.*

---

## Librarian Note  
Updating this table requires bumping `xwalk_hash` and regenerating the
alias JSON. Any link pointing back to Vol-1 PDF after **2025-07-01** will
fail CI unless justified.
