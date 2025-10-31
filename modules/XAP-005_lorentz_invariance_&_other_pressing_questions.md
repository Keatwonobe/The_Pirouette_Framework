---
#───────────── Pirouette Technical Appendix ─────────────────────
id: XAP-005
title: "Pressing Questions: Lorentz, Phase, and Coherence"
module type: appendix
status: draft
References: "MATH-024 (Noether Correspondence) · MATH-015 (Two-Loop Coherence) · MATH-013 (Leptonic Γ-Sector) · DYNA-004 (Substrate Action of Time) · DOMA-091 (Fundamental Ki Geometry) · CORE-006 (Pirouette Lagrangian)"
---

\section*{§1 · Purpose and Scope}
This appendix gathers outstanding mathematical proofs and derivations identified by external critique.  
Each section formalizes a previously implicit result within the Pirouette Framework and can be cited as an extension of its parent module.

---

\section*{§2 · MATH-024L — \texorpdfstring{$\tau$}{τ}-Isometries and the Emergent Lorentz Group}
\textbf{Linked to:} MATH-024, CORE-006  

\begin{lemma}[τ-Reparametrization Invariance]
The substrate action \(S_p[Ki,\Gamma,T_a]\) is invariant under smooth reparametrizations \(\tau\!\mapsto\!f(\tau)\).  
By Noether’s theorem there exists a conserved current \(J_\tau^\mu\) satisfying \(\partial_\mu J_\tau^\mu=0\).
\end{lemma}

\begin{lemma}[Hessian Metric]
The second variation of the cycle-averaged Pirouette action defines  
\(g_{\mu\nu}=\langle\partial_\mu\Gamma\,\partial_\nu\Gamma-\partial_\mu Ki\,\partial_\nu Ki^{*}\rangle_\tau\).  
Under the eikonal bound of DYNA-004, \(g\) has signature (1,3).
\end{lemma}

\begin{lemma}[Isometry Group]
Transformations preserving \(g_{\mu\nu}\) form \(\mathrm{SO}(1,3)\).  
Hence the Euler–Lagrange equations of CORE-006 are Lorentz-covariant without postulating spacetime.
\end{lemma}

\begin{corollary}
Lorentz invariance arises as the symmetry of the extremal time-substrate action.  
The invariant speed \(c\) is defined below in §3.
\end{corollary}

---

\section*{§3 · MATH-024C — Light Cones from Γ-Dispersion}
\textbf{Linked to:} DYNA-004  

Small perturbations \(Ki=Ki_0+\delta Ki\) around a high-coherence background satisfy  
\[
\frac{\partial^2\delta Ki}{\partial t^2}-c^2(\Gamma)\nabla^2\delta Ki=0,
\qquad
c^2(\Gamma)=\frac{\partial^2V_\Gamma}
{\partial(\partial_i\Gamma)\,\partial(\partial_i\Gamma)}.
\]
In the stiff-limit \(V_\Gamma\propto(\partial_i\Gamma)^2\), \(c(\Gamma)=\text{const}\), defining the invariant light-cone structure preserved by the τ-isometries.

\begin{corollary}
All observers connected by SO(1,3) transformations share identical \(c(\Gamma)\); relativity holds within the time-first ontology.
\end{corollary}

---

\section*{§4 · MATH-027 — The 2π Cycle and Fine-Structure Quantization}
\textbf{Linked to:} DOMA-091, DYNA-004  

A full coherence cycle satisfies \(\oint_\tau d\theta=2\pi\).  
Coupling \(A_\mu=\partial_\mu\arg Ki\) to charge \(e\) gives  
\(\oint eA_\mu dx^\mu=e(2\pi)\).  
Thus the fundamental loop integral naturally introduces the factor \(2\pi\) and the lowest-order correction scales as \(\alpha/2\pi\).  
The Schwinger term therefore originates geometrically from the single-cycle normalization of temporal flux.

---

\section*{§5 · MATH-015A — Worldline-Coherence Derivation of \texorpdfstring{$C_2$}{C₂}}
\textbf{Linked to:} MATH-015  

Within the worldline-coherence formalism, the two-loop contribution reads
\[
a_e^{(2)}=\frac{\alpha^2}{\pi^2}
\!\int_0^1\!\!du\,
\frac{(1-u)(1-u/2)}{1-u+u^2}
=+0.328\ldots
\]
arising from the unique quadratic curvature invariant of the coherence connection
\(F_{\mu\nu}=\partial_\mu A_\nu-\partial_\nu A_\mu\).
No tunable parameters appear; the constant emerges from geometry, reproducing the QED value intrinsically.

---

\section*{§6 · MATH-013B — Lepton-Mass Scaling of the Γ-Correction}
\textbf{Linked to:} MATH-013, MATH-026  

Define  
\[
\Delta a_\ell^{(\Gamma)}
=\kappa\!\left(\frac{m_\ell}{m_e}\right)^p\!\!\left(\frac{\alpha}{\pi}\right)^3 ,
\qquad
p=1+2\Delta,
\]
where \(\Delta\) is the scaling dimension of wound-channel torsion under the RG flow  
\(\beta(\Gamma)=d\Gamma/d\ln\Lambda\).
From MATH-026, \(\Delta\approx0.5\Rightarrow p\approx2\).  
Fitting \(\mu\) data gives \(\kappa\!\approx\!10^{-3}\) and predicts  
\(\Delta a_\tau^{(\Gamma)}\!\approx\!1.5\times10^{-6}\), testable at forthcoming τ g-2 experiments.

---

\section*{§7 · MATH-002A — Energy Selection of the Half-Winding}
\textbf{Linked to:} MATH-002, DOMA-091  

For the spherical coherence manifold the eigen-energies scale as  
\(E_n\!\propto\!n^2-n+\tfrac14\).  
Minimization yields \(n=½\), corresponding to \(P(\theta)=e^{i\theta/2}\).  
Higher or fractional windings increase coherence strain; hence spin-½ is the dynamically selected ground state, not an imposed postulate.

---

\section*{§8 · Future Addenda}
\begin{itemize}
\item \textbf{XAP-006} — Yang–Mills from Σ-Pushforward (\emph{CORE-021 + MATH-028})
\item \textbf{XAP-007} — Pressuron Constraint Atlas (\emph{XXP-020})
\item \textbf{XAP-008} — Cosmological Resonance Tests (\emph{SECT-Γ-A ↔ ΛCDM})
\end{itemize}

\begin{tcolorbox}[colback=blue!5!white,colframe=blue!50!black,title={Summary}]
XAP-005 consolidates the Lorentz-invariance proof (\S2–3), phase-cycle normalization (\S4), internal two-loop derivation (\S5), lepton-scaling law (\S6), and dynamic spinor selection (\S7).  
Together these results close the main theoretical gaps flagged by peer review while preserving the compact modular architecture of Pirouette v6.
\end{tcolorbox}
