---
id: MATH-027
title: Ki Propagator and Substrate Feynman Rules
module_type: theoretical-core
status: draft-1.0
parents: [DYNA-004 (Substrate Action of Time) · XAP-005 (τ-Isometries; Light Cones) · XAP-006 (Σ-Pushforward & Yang–Mills) · XAP-006C (Mass from Γ-Stiffness)]
children: []

summary: "Explicit Ki propagator and Feynman rules in substrate theory"

---

\section*{§1 · Field content and quadratic action (τ-substrate)}
We treat \(Ki(\tau,\mathbf{u})\) as a complex scalar over the time substrate \(\mathcal M_\tau\) with internal fiber \(\mathcal F\) (U(1) by default; SU(2)/SU(3) per XAP-006).
The minimal quadratic substrate Lagrangian (before Σ) is
\begin{equation}
\mathcal L^{(\tau)}_{Ki,\,\text{quad}}
= K_{Ki}\,|\partial_\tau Ki|^2
- \Lambda_{Ki}\,|\nabla_\tau Ki|^2
- m_{Ki,\tau}^2\,|Ki|^2 ,
\label{eq:Ki_quad_tau}
\end{equation}
with anisotropic “temporal” and “spatial” stiffnesses \(K_{Ki},\Lambda_{Ki}>0\).
The Γ–sector contributes an effective mass via XAP-006C:
\(m_{Ki,\tau}^2 \equiv m_0^2 + \xi_\Gamma\,\Gamma_0^2\).

\paragraph{Emergent Lorentz form.}
Using the light-cone result \(c^2=\Lambda_\Gamma/K_\Gamma\) (XAP-005), define rescaled time \(t = \sqrt{K_{Ki}}\,\tau\) and spatial metric \(\mathbf x = \sqrt{\Lambda_{Ki}}\,\mathbf u\).
Then \eqref{eq:Ki_quad_tau} becomes the Lorentz-covariant quadratic form
\begin{equation}
\mathcal L_{Ki,\text{quad}}^{(obs)}
= |\partial_t Ki|^2 - |\nabla Ki|^2 - m_{Ki}^2 |Ki|^2,
\qquad
m_{Ki}^2 \equiv \frac{m_{Ki,\tau}^2}{K_{Ki}}.
\label{eq:Ki_quad_obs}
\end{equation}

\section*{§2 · Free propagators (momentum space)}
\subsection*{2.1 Ki propagator}
Fourier transform \(Ki(x)=\!\int\!\frac{d^4p}{(2\pi)^4}e^{-ip\cdot x}\tilde Ki(p)\).
The observer-frame Feynman propagator is
\begin{equation}
\boxed{\; \Delta_{Ki}(p)=\frac{i}{p^2 - m_{Ki}^2 + i\varepsilon}\;}
\label{eq:Ki_prop}
\end{equation}
with \(p^2=p_0^2-\mathbf p^2\).
In substrate variables (no rescaling),
\(
\Delta^{(\tau)}_{Ki}(\omega,\mathbf k)
= i\big/(K_{Ki}\omega^2 - \Lambda_{Ki}\mathbf k^2 - m_{Ki,\tau}^2 + i\varepsilon).
\)

\subsection*{2.2 Gauge and Γ propagators (for completeness)}
U(1) gauge boson (R\(_\xi\) gauge):
\begin{equation}
D_{\mu\nu}(p)=\frac{-i}{p^2+i\varepsilon}\!\left(g_{\mu\nu}-(1-\xi)\frac{p_\mu p_\nu}{p^2}\right).
\label{eq:photon_prop}
\end{equation}
Γ (pressuron) small-fluctuation mode:
\begin{equation}
\Delta_\Gamma(p)=\frac{i}{p_0^2 - c_\Gamma^2 \mathbf p^2 - m_\Gamma^2 + i\varepsilon},
\quad
m_\Gamma^2=\frac{V''(\Gamma_0)}{K_\Gamma},
\quad
c_\Gamma^2=\frac{\Lambda_\Gamma}{K_\Gamma}.
\label{eq:gamma_prop}
\end{equation}

\section*{§3 · Interactions and vertex factors}
We collect the minimal interaction terms used in Pirouette EFT:
\begin{align}
\mathcal L_{\text{int}}
&=
|(\partial_\mu + i e A_\mu)Ki|^2
- \lambda_{Ki}\,|Ki|^4
- \lambda_\Gamma\big(|Ki|^2 - \xi\,\Gamma^2\big)^2
+ \bar\Psi(i\gamma^\mu D_\mu - y_\Gamma \Gamma)\Psi .
\label{eq:L_int}
\end{align}
Expanding \eqref{eq:L_int} yields the standard scalar QED vertices plus Γ-couplings:

\begin{center}
\begin{tabular}{|l|c|l|}
\hline
\textbf{Vertex} & \textbf{Factor} & \textbf{Comments} \\
\hline
\(Ki\,Ki^\dagger\,A_\mu\) & \(i e (p+p')_\mu\) &
Incoming \(p\) on \(Ki\), \(p'\) on \(Ki^\dagger\). \\
\hline
\(Ki\,Ki^\dagger\,A_\mu A_\nu\) & \(2 i e^2 g_{\mu\nu}\) & Contact term from \(|D_\mu Ki|^2\). \\
\hline
\(Ki\,Ki^\dagger\,Ki\,Ki^\dagger\) & \(-2 i \lambda_{Ki}\) & Symmetry factor included (complex scalar). \\
\hline
\(Ki\,Ki^\dagger\,\Gamma\) & \(-\,2 i \lambda_\Gamma \xi (2\Gamma_0)\) &
From expanding \(\lambda_\Gamma(|Ki|^2-\xi\Gamma^2)^2\) about \(\Gamma_0\). \\
\hline
\(Ki\,Ki^\dagger\,\Gamma\,\Gamma\) & \(-\,2 i \lambda_\Gamma \xi^2\) &
Quadratic Γ coupling (residual). \\
\hline
\(\bar\Psi \Psi \Gamma\) & \(-\,i y_\Gamma\) &
Torsion mass channel (XAP-006C). \\
\hline
\end{tabular}
\end{center}

\paragraph{Gauge choice.} Unless stated, use \(R_\xi\) with \(\xi=1\) (Feynman gauge) for internal lines; physical observables are \(\xi\)-independent.

\section*{§4 · Counterterms and on-shell scheme}
Define counterterm Lagrangian
\(
\delta\mathcal L
= \delta Z_{Ki}\,|\partial Ki|^2
- \delta m_{Ki}^2\,|Ki|^2
- \delta\lambda_{Ki}\,|Ki|^4
- \delta Z_e\, e\, A\!\cdot\!J_{Ki}
- \delta y_\Gamma\,\bar\Psi\Psi\Gamma
- \delta m_\Gamma^2\,\tfrac12 \Gamma^2 + \cdots
\)
with OS conditions
\[
\Sigma_{Ki}(p^2=m_{Ki}^2)=0,\qquad
\left.\frac{d\Sigma_{Ki}}{dp^2}\right|_{p^2=m_{Ki}^2}=0,
\qquad
\Pi_{\mu\nu}(0)=0,
\]
and analogous for \(\Gamma\) when

