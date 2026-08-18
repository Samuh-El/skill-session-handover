# Theoretical Reference: Session Handover & Predictive Sufficiency

This document provides the exhaustive mathematical foundation, theoretical guarantees, and analytical proofs established in the research paper *Handover of In-Context Learning State Across Session Boundaries* (Masahiro Kato & Taka Kato, 2026, [arXiv:2608.14528](https://arxiv.org/html/2608.14528v1)).

---

## 1. General Mathematical Formulation of Session Handover

### 1.1 Episode Definition & Information Order
An evaluation instance (episode) is defined as:
$$\omega = (C, T, X, Y) \sim \mathsf{P}_{\text{ep}}$$
where:
* $C$: Full pre-handover context (dialogue turns, tool outputs, dataset samples, error traces).
* $T$: Task specification, target structure, and scoring rule known at the boundary.
* $X$: Post-handover input (subsequent query, next user instruction, or environment state).
* $Y$: Ground-truth target outcome (prediction, code generation, or trajectory score).

### 1.2 The Handover Writer ($E$)
The writer program or agent $E$ produces the handover record $H$ observing only $(C, T)$ **strictly before** the realized downstream input $X$ is revealed:
$$H = (V, M), \qquad H \sim P_E(\cdot \mid C, T)$$
* $V$: Active record injected into the initial context window of the new session.
* $M$: External storage archive (persistent disk files, databases, vector stores) accessible on demand.

### 1.3 Memory Budget Constraints
Memory limits are imposed on active prompt tokens ($B_{\text{act}}$) and total retained storage ($B_{\text{tot}}$):
$$b_{\text{act}}(V) \le B_{\text{act}}, \qquad b_{\text{tot}}(V, M) = b_{\text{act}}(V) + b_{\text{ext}}(M) \le B_{\text{tot}}$$

---

## 2. Predictive Sufficiency vs. Exact Recovery

### Definition 2.1 (Exact Recovery of Selected Material)
An item $O = \phi(C, T)$ is exactly recoverable from $H$ if there exists a measurable decoding map $r$ such that:
$$O = r(H, T) \quad \text{almost surely}$$
*(Exact recovery of the entire context corresponds to $O = C$.)*

### Definition 2.2 (Predictive Sufficiency)
A handover record $H$ is **predictively sufficient** for $C$ relative to $(X, Y, T)$ if:
$$P(Y \mid C, X, T) = P(Y \mid H, X, T) \quad \text{almost surely}$$
Equivalently, the conditional mutual information between earlier context $C$ and target $Y$ vanishes given $(H, X, T)$:
$$I(Y; C \mid H, X, T) = 0$$

### Proposition 2.3 (Hierarchical Invariance & Non-Reversibility)
$$\text{Exact Context Recovery } (O = C) \implies \text{Predictive Sufficiency } (H) \implies R_\ell^\star(H) = R_\ell^\star(C)$$
* **Core Insight**: Exact textual reconstruction is unnecessarily bloated and restrictive. A handover needs only to distinguish earlier contexts that alter the conditional law of $Y$, discarding superficial dialogue variations.

---

## 3. Coarsest Deterministic State & Minimum Bit Requirements

### Proposition 3.1 (Coarsest Sufficient State under Exogeneity)
Assuming the downstream query distribution $X \mid (C=c, T=t) \sim \mu_t$ is exogenous and context-invariant, two contexts $c \sim_t c'$ belong to the same ICL equivalence class if:
$$P(Y \mid C=c, X=x, T=t) = P(Y \mid C=c', X=x, T=t) \quad \text{for } \mu_t\text{-almost every } x$$
The canonical quotient map $q_t(c) = [c]_{\sim_t}$ is the coarsest deterministic sufficient handover. Any other deterministic sufficient handover can decode $q_t(c)$.

### Corollary 3.2 (Minimum Bit Budget)
If the state space $q_t(C)$ takes $N_t < \infty$ distinct values with positive probability, any fixed-length deterministic sufficient handover requires at least:
$$B_{\text{min}} = \lceil \log_2 N_t \rceil \quad \text{bits}$$

---

## 4. 3-Term Excess Risk Decomposition

For any post-handover model and decoder $D_\theta$, the excess risk over the theoretical full-context optimum decomposes into three distinct, additive penalties:
$$R(E, D_\theta) - R_{\text{full}}^\star = \underbrace{(R_B^\star - R_{\text{full}}^\star)}_{\text{Capacity Loss (Forced by Budget } B\text{)}} + \underbrace{(R_E^\star - R_B^\star)}_{\text{Writer Inefficiency}} + \underbrace{(R(E, D_\theta) - R_E^\star)}_{\text{Decoder / Model Utilization Gap}}$$

Where:
* $R_{\text{full}}^\star = \inf_D \mathbb{E}[\ell(D(C, X, T), Y)]$ (Optimum with uncompressed history)
* $R_E^\star = \inf_D \mathbb{E}[\ell(D(E(C, T), X, T), Y)]$ (Optimum achievable with record $H = E(C, T)$)
* $R_B^\star = \inf_{E \in \mathcal{E}_B} R_E^\star$ (Best possible risk under budget $B$)

---

## 5. Information Loss Identities & Decision Bounds

### Proposition 5.1 (Log-Loss Mutual Information Identity)
Under logarithmic loss $\ell_{\log}(p, y) = -\log p(y)$, the excess Bayes risk of a handover is exactly the discarded task information:
$$R_{\log}^\star(H) - R_{\log}^\star(C) = I(Y; C \mid H, X, T)$$

### Theorem 5.2 (General Decision Loss Bound)
For any bounded loss function $\ell(a, Y) \in [0, L_{\text{max}}]$ across a finite action space $\mathcal{A}$:
$$0 \le R_E^\star - R_{\text{full}}^\star \le L_{\text{max}} \sqrt{\frac{I(Y; C \mid H, X, T)}{2}} \quad \text{(measured in nats)}$$

### Proposition 5.3 (Cost of Pre-Query State Coding)
Let $C = (C_1, \dots, C_m) \in \{0, 1\}^m$ with i.i.d. $\text{Bernoulli}(1/2)$ coordinates and $X \sim \text{Uniform}(\{1, \dots, m\})$. If an encoder writes $H$ with budget $I(C; H) \le B$ bits before observing $X$, the Bayes log loss is bounded by:
$$\mathsf{H}_2(Y \mid H, X) \ge \max\left\{0, 1 - \frac{B}{m}\right\}$$
*(In contrast, an encoder observing $X$ before compressing requires only 1 bit to achieve 0 error).*

---

## 6. Information-Equivalent Records & The Representation Gap

### Proposition 6.1 (Ideal-Risk Ordering)
If $H_2 = s(H_1, T)$ deterministically, then $R^\star(H_1) \le R^\star(H_2)$. If there also exists a deterministic inverse $H_1 = r(H_2, T)$, both records share the exact same ideal risk:
$$R^\star(H_1) = R^\star(H_2)$$

### Corollary 6.2 (Representation-Gap Identity)
For any two mathematically equivalent representations $H_1$ and $H_2$ evaluated under a fixed recipient model $D$:
$$R(D; H_1) - R(D; H_2) = \left(R(D; H_1) - R^\star(H_1)\right) - \left(R(D; H_2) - R^\star(H_2)\right)$$
* **Key Implication**: Any observed performance gap between two information-equivalent formats (e.g., matrices vs. synthetic demonstrations) is entirely attributable to the recipient model's parsing/prompting efficiency, not to missing task information.

---

## 7. Statistical Case Studies

### 7.1 Parametric Bayesian Linear Regression
Consider $Y = x^\top \beta + \epsilon, \epsilon \sim \mathcal{N}(0, \sigma^2)$ with prior $\beta \sim \mathcal{N}(m_0, V_0)$ and $n$ demonstrations $(X_n, y_n)$.

1. **Exact Finite-Dimensional State**:
   $$H_n = (G_n, b_n), \qquad G_n = X_n^\top X_n \in \mathbb{R}^{d \times d}, \quad b_n = X_n^\top y_n \in \mathbb{R}^d$$
   Stores only $d(d+1)/2 + d$ real numbers regardless of sample size $n$, with $I(Y; X_n, y_n \mid H_n, x, T) = 0$.
2. **Equivalent Synthetic Demonstrations**:
   For $r = \text{rank}(G_n)$ and spectral decomposition $G_n = U_r \Lambda_r U_r^\top$:
   $$\widetilde{X} = \Lambda_r^{1/2} U_r^\top \in \mathbb{R}^{r \times d}, \qquad \widetilde{y} = \Lambda_r^{-1/2} U_r^\top b_n \in \mathbb{R}^r$$
   Satisfies $\widetilde{X}^\top \widetilde{X} = G_n$ and $\widetilde{X}^\top \widetilde{y} = b_n$, replicating identical posterior distributions and Ridge estimates.
3. **Quantization Stability (Theorem 5.3 & Corollary 5.4)**:
   If $\|\overline{G} - G_n\|_{\text{op}} \le \delta_G$ and $\|\overline{b} - b_n\|_2 \le \delta_b$, and $\alpha = \lambda_{\text{min}}(V_0^{-1}) > 0$:
   $$\|\overline{V} - V_n\|_{\text{op}} \le \frac{\delta_G}{\sigma^2 \alpha^2}, \qquad \|\overline{m} - m_n\|_2 \le \frac{\delta_b}{\sigma^2 \alpha} + \frac{\delta_G \|h_n\|_2}{\sigma^2 \alpha^2}$$
   $$D_{\text{KL}}(\mathcal{N}(\mu_x, v_x) \,\|\, \mathcal{N}(\overline{\mu}_x, \overline{v}_x)) \le \frac{\varepsilon_\mu^2}{2\sigma^2} + \frac{\varepsilon_v^2}{\sigma^4}$$

### 7.2 Nonparametric Regression over Hölder Spaces ($\mathcal{H}^\beta$)
Consider $Y_i = f(X_i) + \varepsilon_i, X_i \in [0, 1]^d, f \in \mathcal{H}^\beta(L, B_f)$.

1. **Cell-Partition Handover ($H_M$)**:
   Partition $[0, 1]^d$ into $M = m^d$ cubes $A_1, \dots, A_M$. Store cell counts $N_j = \sum \mathbf{1}(X_i \in A_j)$ and quantized cell means $Q_q(\overline{Y}_j)$.
2. **Achievable Risk Bound (Theorem 5.7)**:
   $$\sup_{f \in \mathcal{H}^\beta} \mathbb{E}_f[\|\widehat{f}_{H_M} - f\|_{P_X}^2] \le C_1 M^{-2\beta/d} + C_2 \frac{M}{n} + C_3 \exp\left(-\frac{n p_{\text{min}}}{M}\right) + C_4 q^2$$
3. **Optimal Bit Budget (Corollary 5.8)**:
   Matching the full-data minimax rate $O(n^{-2\beta/(2\beta+d)})$ requires a bit budget of:
   $$B_n = O\left(n^{d/(2\beta+d)} \log n\right) \quad \text{bits}$$
4. **Memory Minimax Lower Bound (Theorem 5.10)**:
   $$R_{n, B} \ge c \max\left\{n^{-2\beta/(2\beta+d)}, (B+1)^{-2\beta/d}\right\}$$
   Showing that unlike parametric regression, nonparametric memory MUST grow with desired precision.
