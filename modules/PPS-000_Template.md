---
id: PPS-000
title: Template
version: 1.4
parents: [AKEP-004]
children: [All Volume 5+ Modules]
engrams:
  - "provenance:Librarian/engram/synthesis-omega"
  - "debate:unification-of-tendu-and-latex"
  - "synthesis:rigor+freedom"
  - "directive:ai-output-to-yaml"
keywords: [template, authoring-system, pmd, json, latex, pandoc, tendu-unification]
uncertainty_tag: Very Low
entropy_score: 0.05 # Foundational artifact, highly ordered.
module_type: core-template

---

### Purpose and Scope

This document is the foundational module for Volume 5 of the Pirouette Framework. It establishes the official **Pirouette Module Definition (`.pmd`)** file format, a hybrid authoring system designed to provide a single source of truth for generating both human-readable PDFs and machine-readable JSON manifests.

### Instructions for AI Agents

When tasked with generating or modifying a Pirouette Framework module, you **must** output the entire module as a single, complete `.pmd` file formatted within a YAML code frame. The file must begin with the `id:` key and end with the final line of the Markdown body. This ensures the output is directly parsable by the framework's compilation pipeline.

---
### The `.pmd` Authoring System

The system is built on a "single source, multiple outputs" philosophy.

1.  **Authoring (`.pmd`)**: All modules are written as plain text `.pmd` files. These files contain a **YAML Frontmatter** block for structured metadata and a **Markdown Body** for the main content, which supports embedded LaTeX mathematics.

2.  **Compilation (`compiler.py`)**: A central Python script orchestrates the conversion process:
    * **--> PDF Output**: The script uses **Pandoc** and a **LaTeX** distribution to convert the `.pmd` into a beautifully formatted PDF. It does this by using a minimal `.tex` template which loads a comprehensive `.sty` style package.
    * **--> JSON Output**: The script parses the YAML frontmatter to generate a clean JSON object for each module, ready for integration with Tendu, the Librarian, and other automated systems.

---
### The Core LaTeX Files

To enable this system, your `templates/` directory should contain two files: a comprehensive style package (`pirouette.sty`) and a minimal Pandoc template (`template.tex`).

#### `templates/pirouette.sty`
This file contains all your custom commands, packages, and styling logic.

```latex
% pirouette.sty - Pirouette Framework Style Package (v1.2)
\ProvidesPackage{pirouette}[2025/06/28 v1.2 Pirouette Framework Macros]

% --- Core Package Dependencies ---
\RequirePackage[margin=1in]{geometry}
\RequirePackage{amsmath,amssymb,amsfonts}
\RequirePackage{graphicx}
\RequirePackage{xcolor}
\RequirePackage{booktabs}
\RequirePackage{hyperref}
\RequirePackage{tcolorbox}
\tcbuselibrary{skins,breakable}
\RequirePackage{environ}
\RequirePackage{xparse}
\RequirePackage{etoolbox}
\RequirePackage{lipsum}

% --- Key–Value \moduleKV ---
\ExplSyntaxOn
\keys_define:nn { pirouette/module }
 {
   id          .tl_set:N = \l_pir_id_tl,
   title       .tl_set:N = \l_pir_title_tl,
   version     .tl_set:N = \l_pir_ver_tl,
   parents     .tl_set:N = \l_pir_parents_tl,
   children    .tl_set:N = \l_pir_children_tl,
   engrams     .tl_set:N = \l_pir_engrams_tl,
   uncertainty .tl_set:N = \l_pir_unc_tl,
   keywords    .tl_set:N = \l_pir_keys_tl,
   module_type .tl_set:N = \l_pir_type_tl,
   module_type .initial:n = core,
 }
\NewDocumentCommand{\moduleKV}{ m }{ \group_begin: \keys_set:nn { pirouette/module } { #1 } \begin{tcolorbox}[enhanced,breakable,colframe=black!70,colback=gray!5,title={\bfseries \l_pir_title_tl\ — ID: \l_pir_id_tl\ (v\l_pir_ver_tl)}] \textbf{Type}: \l_pir_type_tl\\ \textbf{Parents}: \l_pir_parents_tl\\ \textbf{Children}: \l_pir_children_tl\\[2pt] \textbf{Uncertainty}: \l_pir_unc_tl\\[2pt] \textbf{Keywords}: \l_pir_keys_tl\\[2pt] \textbf{Engrams}: \parbox[t]{0.85\linewidth}{\l_pir_engrams_tl} \end{tcolorbox} \group_end: }
\ExplSyntaxOff

% --- Other custom environments like `librariannote`, `debateHistory`, etc. go here ---

\endinput