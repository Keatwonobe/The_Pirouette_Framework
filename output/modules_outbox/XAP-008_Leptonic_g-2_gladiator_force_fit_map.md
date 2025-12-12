---
#───────────── Pirouette Technical Appendix ─────────────────────
id: XAP-008
title: "Cosmological Extension: Λ as Residual Γ-Stiffness"
module type: appendix
status: draft
References: XAP-007 (Pressuron Constraint Atlas) · MATH-013 (Leptonic $\Gamma$-sector) · XAP-006C (Mass from $\Gamma$-stiffness) · MATH-029 (Substrate Feynman Rules)
---

\section*{§1 · Model \& Scenarios}
We scan the three-parameter space $(\kappa, p, m_\Gamma)$ for leptonic magnetic-moment shifts
\[
\Delta a_\ell^{(\Gamma)}=\kappa\Big(\frac{m_\ell}{m_e}\Big)^p\Big(\frac{\alpha}{\pi}\Big)^3
\,\underbrace{\frac{m_\ell^2}{m_\ell^2+m_\Gamma^2}}_{F_\ell(m_\Gamma)},
\]
with $\ell\in\{e,\mu\}$ and $\alpha^{-1}=137.035999046$.
Two benchmark constraint bands:
\[
\text{A (permissive): }|\Delta a_\mu|\le 2.5{\times}10^{-9},\quad |\Delta a_e|\le 5{\times}10^{-13},\qquad
\text{B (tight): }|\Delta a_\mu|\le 5.0{\times}10^{-10},\quad |\Delta a_e|\le 3{\times}10^{-13}.
\]

\section*{§2 · Fit Outputs (CSV Artifacts)}
We provide three machine-readable tables for the module→paper pipeline:
\begin{itemize}
\item \textbf{Viable points:} $(\kappa,p,m_\Gamma)$ satisfying both $e$ and $\mu$ bands.  
      File: \texttt{xap\_007\_fits/viable\_points.csv}
\item \textbf{Envelopes at fixed $m_\Gamma$:} min/max ranges of $(\kappa,p)$ near $m_\Gamma=\{1,3,10,30,100\}$ MeV.  
      File: \texttt{xap\_007\_fits/envelopes.csv}
\item \textbf{Best-fit line (tight):} minimal $\kappa$ saturating the tight $\mu$ bound while passing the $e$ bound, across a grid of $(p,m_\Gamma)$.  
      File: \texttt{xap\_007\_fits/bestfit\_kappa\_tight.csv}
\end{itemize}

\section*{§3 · Excerpt Tables (for human reading)}
\begin{table}[H]
\centering
\caption{Viable $(\kappa,p,m_\Gamma)$ points (excerpt). Full table in \texttt{viable\_points.csv}.}
\label{tab:viable_excerpt}
\begin{tabular}{llllll}
\toprule
scenario & $\kappa$ & $p$ & $m_\Gamma$ [MeV] & $\Delta a_e$ & $\Delta a_\mu$\\
\midrule
\multicolumn{6}{c}{(rows sampled from the CSV; pipeline will render full table)}\\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[H]
\centering
\caption{Envelope ranges near selected $m_\Gamma$ slices (excerpt). Full table in \texttt{envelopes.csv}.}
\label{tab:envelopes_excerpt}
\begin{tabular}{lllllll}
\toprule
scenario & $m_\Gamma$ [MeV] & $\kappa_{\min}$ & $\kappa_{\max}$ & $p_{\min}$ & $p_{\max}$ & count\\
\midrule
\multicolumn{7}{c}{(rows sampled from the CSV; pipeline will render full table)}\\
\bottomrule
\end{tabular}
\end{table}

\begin{table}[H]
\centering
\caption{Best-fit $\kappa$ (tight band), saturating $\mu$ bound with $e$-safe check (excerpt). Full table in \texttt{bestfit\_kappa\_tight.csv}.}
\label{tab:bestfit_excerpt}
\begin{tabular}{lllll}
\toprule
$p$ & $m_\Gamma$ [MeV] & $\kappa_{\text{best}}$ & $\Delta a_e$ & $\Delta a_\mu$\\
\midrule
\multicolumn{5}{c}{(rows sampled from the CSV; pipeline will render full table)}\\
\bottomrule
\end{tabular}
\end{table}

\section*{§4 · Reading the Map (qualitative)}
\begin{itemize}
\item The electron bound dominates the viable set; decoupling $F_e(m_\Gamma)$ pushes solutions toward $m_\Gamma\!\gtrsim\!10$–$30$ MeV \emph{or} larger $p$.
\item Tight band favors $p\!\gtrsim\!1.5$–$2.5$ with $\kappa\!\sim\!10^{-4}$–$10^{-3}$; permissive band admits smaller $p$ or lighter $m_\Gamma$ if $\kappa\!\lesssim\!10^{-4}$.
\end{itemize}

\section*{§5 · Reproducibility \& Hooks}
The CSV set is designed for your “Great Plotting” API: each paper job can import the CSVs, fit contours, and render parameter wedges without re-running the scan.  
To regenerate from source, call the analysis routine in MATH-013/XAP-007 with the same $(\alpha, m_e, m_\mu)$ constants and the decoupling kernel $F_\ell$ above.

\begin{tcolorbox}[colback=blue!5!white,colframe=blue!50!black,title={Summary}]
XAP-009 publishes the $(\kappa,p,m_\Gamma)$ regions consistent with both $e$ and $\mu$ magnetic moments, plus machine-readable artifacts for downstream visualization and paper assembly.
\end{tcolorbox}

