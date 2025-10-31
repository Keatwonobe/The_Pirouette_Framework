---
id: XAP-eγ→eγ
title: "Appendix A: Klein--Nishina Cross Section from the $\Sigma$-pushed QED Rules"
version: 1.0
status: Release
parents: []
outputs: []
artifact_dir: ./qed_exp_v1
---

\appendix
\section*{Appendix A: Klein--Nishina Cross Section from the $\Sigma$-pushed QED Rules}

\subsection*{A.1 Kinematics and conventions}
We work in the observer chart after the spatialization map $\Sigma$. Incoming electron momentum $p^\mu=(E,\mathbf{p})$, mass $m$; incoming photon momentum $k^\mu=(\omega,\mathbf{k})$ with polarization $\varepsilon^\mu$; outgoing electron $p'$, outgoing photon $k'=(\omega',\mathbf{k}')$ with polarization $\varepsilon'^\mu$. On-shell:
\[
p^2=p'^2=m^2,\qquad k^2=k'^2=0,\qquad (2\pi)^4\delta^{(4)}(p+k-p'-k')\,.
\]
We define the scattering angle $\theta$ between $\mathbf{k}$ and $\mathbf{k}'$ in the electron rest frame (ERF), where $p=(m,\mathbf{0})$.

\subsection*{A.2 Tree-level amplitude}
From the $\Sigma$-pushed Lagrangian $\mathcal{L}=-\tfrac14 F^2+\bar\Psi(i\!\not\!D-m)\Psi$ with $D_\mu=\partial_\mu+iqA_\mu$, the two Compton diagrams give
\[
\mathcal{M} = (-iq)^2\, \varepsilon'_\mu \varepsilon_\nu\,
\bar u(p')\!\left[
\gamma^\mu\,\frac{\not p+\not k+m}{(p+k)^2-m^2+i0}\,\gamma^\nu
+\gamma^\nu\,\frac{\not p-\not k'+m}{(p-k')^2-m^2+i0}\,\gamma^\mu
\right]\!u(p).
\]
Gauge invariance (Ward identities) follows because $\Sigma$ is a functorial pushforward preserving Noether currents; algebraically
$\mathcal{M}\big|_{\varepsilon\to k}=0$ and $\mathcal{M}\big|_{\varepsilon'\to k'}=0$
using $\not p\,u(p)=mu(p)$ and $k^2=0$.

\subsection*{A.3 Spin and polarization sums}
Average over initial spins (factor $\tfrac12$) and initial photon polarizations (factor $\tfrac12$), sum over finals. Use
\[
\sum_s u^{(s)}(p)\bar u^{(s)}(p)=\not p+m,\qquad
\sum_{\lambda}\varepsilon^{(\lambda)}_\mu(k)\varepsilon^{(\lambda)}_\nu(k)=-g_{\mu\nu}
\quad(\text{covariant gauge}).
\]
Then $|\overline{\mathcal{M}}|^2 = \frac14\,(-q^2)^2\, \mathrm{Tr}$ of gamma chains with the two propagators. Standard trace technology gives the Lorentz invariants in terms of $s=(p+k)^2$, $u=(p-k')^2$, and $t=(k-k')^2$ with $s+u+t=2m^2$.

A useful intermediate result:
\[
\Big|\overline{\mathcal{M}}\Big|^2
= 2 q^4\!\left(\frac{m^2 s}{(p\!\cdot\! k)(p\!\cdot\! k')} 
+ \frac{m^2 u}{(p\!\cdot\! k)(p\!\cdot\! k')} 
- \frac{t}{2}\left[\frac{1}{p\!\cdot\! k} - \frac{1}{p\!\cdot\! k'}\right]^2 \right),
\]
which simplifies cleanly in the ERF.

\subsection*{A.4 ERF relations and Compton formula}
In the ERF, $p=(m,\mathbf{0})$, hence $p\!\cdot\! k=m\omega$ and $p\!\cdot\! k'=m\omega'$. Energy–momentum conservation yields the Compton relation
\[
\omega'=\frac{\omega}{1+\frac{\omega}{m}(1-\cos\theta)}\,,
\qquad
\frac{\omega'}{\omega}=\frac{1}{1+\frac{\omega}{m}(1-\cos\theta)}.
\]

\subsection*{A.5 Differential cross section}
The two-body phase space in the ERF gives
\[
\frac{d\sigma}{d\Omega}=\frac{1}{64\pi^2 m^2}\,\frac{\omega'}{\omega}\,|\overline{\mathcal{M}}|^2.
\]
After substituting the ERF invariants and simplifying,
\[
\boxed{
\frac{d\sigma}{d\Omega}
= \frac{r_e^2}{2}\left(\frac{\omega'}{\omega}\right)^2
\!\left(\frac{\omega}{\omega'}+\frac{\omega'}{\omega}-\sin^2\theta\right),
}
\qquad
r_e \equiv \frac{q^2}{4\pi m}.
\]
This is the Klein--Nishina formula. Low-energy (Thomson) limit $\omega\ll m$ gives
\[
\frac{d\sigma}{d\Omega}\xrightarrow{\omega\ll m}\frac{r_e^2}{2}\,(1+\cos^2\theta).
\]

\subsection*{A.6 Note on $\Sigma$-dependence}
All observer-side structures—propagators, vertex, and the Ward identities—are inherited from the substrate via $\Sigma$, which transports the gauge connection and the Dirac bundle while preserving the Noether current. Thus the derivation above is \emph{identical in form} to textbook QED once in the observer chart; the substrate enters through the existence and normalization of $q$ and $m$ (Berry holonomy and Ki/Γ balance) before pushforward.
