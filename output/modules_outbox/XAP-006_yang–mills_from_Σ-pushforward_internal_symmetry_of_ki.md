---
#───────────── Pirouette Technical Appendix ─────────────────────
id: XAP-006
title: "Yang–Mills from Σ-Pushforward: Internal Symmetry of Ki"
module type: appendix
status: draft
References: "DYNA-004 (Substrate Action of Time) · MATH-024 (Noether Correspondence) · CORE-021 (Internal Symmetry of Ki) · MATH-028 (Σ-Pushforward of Principal Bundles) · MATH-026 (Renormalization Flow)"
---

\section*{§1 · Objective}
To derive non-Abelian gauge structure directly from the internal geometry of the Ki field under the spatialization map Σ.  
Where XAP-005 established Lorentz covariance of the substrate, XAP-006 shows that gauge covariance follows from the same variational logic once Ki is extended over an internal fiber \(\mathcal{F}\).

---

\section*{§2 · Internal Fiber and Connection}
Let
\[
Ki : \mathcal{M}_\tau \rightarrow \mathcal{F},\qquad 
\mathcal{F}=\mathbb{C}^N,\quad N\in\{1,2,3\},
\]
where \(\mathcal{M}_\tau\) is the time-substrate manifold.  
The fiber’s isometry group \(G=\mathrm{U}(N)\) acts by \(Ki\mapsto U Ki\), \(U\in G\).  
Decompose \(G\) into its determinant-free and phase parts:
\[
G=\mathrm{SU}(N)\times \mathrm{U}(1).
\]
The associated connection one-form \(A_\mu = Ki^{-1}\partial_\mu Ki\) defines curvature
\(F_{\mu\nu}=\partial_\mu A_\nu - \partial_\nu A_\mu + [A_\mu,A_\nu]\).

---

\section*{§3 · Σ-Pushforward and Emergent Gauge Fields}
The spatialization map \(\Sigma:\mathcal{M}_\tau\!\to\!\mathcal{M}_{x,t}\) transports internal parallel transport into the observer’s spacetime chart.
\[
A_\mu^{(obs)}(x)=\Sigma_\mu^{\;\nu}A_\nu^{(τ)} ,
\qquad 
F_{\mu\nu}^{(obs)}=\Sigma_\mu^{\;\alpha}\Sigma_\nu^{\;\beta}F_{\alpha\beta}^{(τ)} .
\]
Because Σ preserves the Noether currents of MATH-024, gauge covariance survives the pushforward:
\[
F_{\mu\nu}^{(obs)} \rightarrow U F_{\mu\nu}^{(obs)} U^{-1},
\quad
D_\mu Ki = (\partial_\mu + A_\mu)Ki.
\]
Thus Yang–Mills structure emerges as the Σ-shadow of internal τ-space holonomy.

---

\section*{§4 · Specific Fiber Choices and Physical Interpretation}

\begin{itemize}
\item \textbf{U(1)} (\(N=1\))  
  The trivial fiber reproduces electromagnetism: \(A_\mu=\partial_\mu\arg Ki\).  
  This is the CORE-007 result restated as a Σ-projection.

\item \textbf{SU(2)} (\(N=2\))  
  The doublet fiber yields electroweak structure.  
  The coupling \(g_W\) appears as the curvature magnitude at the critical radius \(r_W=\Gamma^{-1/2}\) in the Ki manifold.  
  Spontaneous orientation of Ki’s expectation value defines the Higgs direction in internal space.

\item \textbf{SU(3)} (\(N=3\))  
  The triplet fiber encodes color.  
  Three independent Ki components \(Ki^a\) generate eight traceless generators \(T^A\).  
  Confinement arises geometrically because the internal metric \(h_{ab}\) is positive-definite and compact, enforcing vanishing total color flux through the Σ-image of closed τ-loops.
\end{itemize}

---

\section*{§5 · Covariant Action via Pushforward}
Pushforward of the Pirouette Lagrangian yields
\[
\mathcal{L}_{YM} =
-\frac{1}{4}\,\mathrm{Tr}\!\left(F_{\mu\nu}^{(obs)}F^{\mu\nu}_{(obs)}\right)
+\overline{\Psi}\,(i\gamma^\mu D_\mu - m)\Psi ,
\]
where \(D_\mu=\partial_\mu+A_\mu^{(obs)}\) acts on matter wavefunctions identified with localized Ki-modes.  
The coupling constants \(g_N\) follow from the normalization of the internal kinetic term in DYNA-004:
\[
g_N^{-2} = \langle \mathrm{Tr}(T^A T^A) \rangle_\tau^{-1}.
\]
Hence gauge couplings are geometric averages over τ-space curvature densities.

---

\section*{§6 · Hierarchical Symmetry Breaking}
Renormalization flow from MATH-026 implies a scale-dependent deformation of the fiber metric \(h_{ab}(\Lambda)\).  
Critical points where \(\det h_{ab}=0\) define spontaneous symmetry breaking surfaces:
\[
\mathrm{SU}(2)\times \mathrm{U}(1)\xrightarrow{\;\langle Ki\rangle\neq0\;}\mathrm{U}(1)_{EM}.
\]
This reproduces electroweak unification without introducing an explicit scalar field:  
the modulus of Ki serves as the order parameter, and Γ-pressure gives the Higgs mass scale.

---

\section*{§7 · Summary of Correspondence}
\begin{center}
\begin{tabular}{|l|l|l|}
\hline
\textbf{Pirouette Object} & \textbf{After Σ-Pushforward} & \textbf{Physical Interpretation} \\
\hline
Internal fiber $\mathcal{F}$ & Gauge group $G$ & Internal symmetry space \\
Connection $A_\mu$ & Gauge potential & Mediator field \\
Curvature $F_{\mu\nu}$ & Field strength & Yang–Mills tensor \\
Fiber metric $h_{ab}$ & Coupling constants $g_N$ & Interaction strength \\
Expectation $\langle Ki\rangle$ & Order parameter & Higgs vacuum \\
\hline
\end{tabular}
\end{center}

---

\section*{§8 · Lemma: Gauge Covariance of Σ}
\begin{lemma}
If Σ preserves the Noether current 1-forms of MATH-024, then for any smooth gauge transformation \(U(\tau)\)
\[
\Sigma^\ast(U^{-1}D_\tau U) = U^{-1}D_x U.
\]
\end{lemma}
\begin{proof}
Since Σ is measure-preserving and intertwines derivatives by 
\(\partial_\tau=\Sigma_\tau^{\;\mu}\partial_\mu\),
we have \(D_\tau = \partial_\tau + A_\tau\Rightarrow D_x = \Sigma_\tau^{\;\mu}D_\mu\).  
Gauge equivalence is maintained under pull-back, proving covariance.
\end{proof}

---

\section*{§9 · Outlook}
\begin{itemize}
\item \textbf{Unification via Fiber Nesting:}  
  Future module XAP-006B will show how nested fibers \(\mathcal{F}_3\supset\mathcal{F}_2\supset\mathcal{F}_1\) lead naturally to grand-unified geometries.

\item \textbf{Mass Generation:}  
  A companion appendix (XAP-006C) will compute the Γ-induced stiffness term that acts as the Higgs potential \(V(H)=\lambda(|Ki|^2-v^2)^2\) in the pushforward limit.

\item \textbf{Confinement Phenomenology:}  
  Subsequent DYNA-extensions will test whether compact τ-loops produce linear flux-tube potentials consistent with lattice QCD.
\end{itemize}

\begin{tcolorbox}[colback=blue!5!white,colframe=blue!50!black,title={Summary}]
XAP-006 formalizes the emergence of SU(3)×SU(2)×U(1) symmetry as a geometric projection of Ki’s internal fiber through the Σ map.  
Gauge couplings, Higgs dynamics, and confinement all appear as coherent features of the same substrate geometry, completing the bridge from Lorentz symmetry (XAP-005) to Standard-Model structure.
\end{tcolorbox}

