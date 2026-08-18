---
name: session-handover
description: "Executes mathematically rigorous In-Context Learning (ICL) state handover across LLM session boundaries or model switches, preserving exact constraints, sufficient statistics, and critical residual observations based on arXiv:2608.14528."
author: "Samuel Esteban Gajardo Vergara (https://github.com/Samuh-El)"
disable-model-invocation: true
version: 1.1.0
triggers:
  - /session-handover
---

# Session Handover (ICL State Transfer)

This skill implements the formal **Session Handover of In-Context Learning (ICL) State** protocol defined in research paper [arXiv:2608.14528](https://arxiv.org/html/2608.14528v1). It enables an agent to package its accumulated working context into a mathematically sufficient state record before switching models, clearing context windows, or handing off execution to another agent.

---

## Architecture & Storage Channels

All handover files reside in `docs/icl_state/` under the project root. Handover memory is split into two primary channels:
1. **Active Prompt Record ($V$)**: Direct payload placed in the recipient model's initial context window ($b_{\text{act}}(V) \le B_{\text{act}}$).
2. **External Storage Archive ($M$)**: Secondary files, raw observations, and reference databases available on disk ($b_{\text{tot}}(V, M) = b_{\text{act}}(V) + b_{\text{ext}}(M) \le B_{\text{tot}}$).

```
docs/icl_state/
├── handover_state/
│   ├── active_prompt_v/
│   │   ├── exact_decisions.json        # H_exact: Rigid memory (goals, constraints, rejected options)
│   │   ├── sufficient_statistics.bin   # H_stat: Task-justified dense statistics or synthetic demos
│   │   └── residual_metadata.json      # J_res: Pointers/tags to external residual observations
│   └── external_storage_m/
│       ├── observations/               # M_res: Uncompressed rare cases, specific failure logs (o_j)
│       │   ├── failure_case_001.txt
│       │   └── rare_example_002.json
│       └── indexed_data/               # External databases or reference files
├── validation/
│   ├── schema_definitions.json         # JSON Schema for deterministic field validation
│   └── numerical_checks.py             # Script checking matrix dimensions and numerical consistency
└── logs/
    └── memory_account.csv              # Token & byte usage audit ledger
```

---

## The 3-Part State Record Definition

1. **Exact Part ($H_{\text{exact}}$)**:
   * **Inviolable Invariant**: Must NEVER be summarized, paraphrased, or made tentative.
   * **Contents**: Primary project goal, binding architectural decisions, explicitly rejected alternatives with rationale, active blocking constraints, and unresolved open questions with sources.
   * **Online Maintenance**: Can be updated incrementally as decisions occur during the session (Appendix B.2), avoiding rushed end-of-context reconstruction.
2. **Statistical Part ($H_{\text{stat}}$)**:
   * **Invariant**: Used ONLY when an explicit mathematical compression guarantee (e.g., sufficient statistic or bounded error approximation) exists for the task loss.
   * **Contents**: Compact representations of repeated tool runs, Gram matrices ($G_n = X_n^\top X_n, b_n = X_n^\top y_n$), synthetic demonstrations $(\widetilde{X}, \widetilde{y})$, or cell partition statistics. If no formal guarantee exists, leave this empty.
3. **Residual Part ($H_{\text{residual}}$ & $M_{\text{res}}$)**:
   * **Contents**: Critical singular observations, rare edge cases, or tool failure logs that cannot be reduced to statistics but dictate downstream execution.
   * **Storage**: Pointers ($J_{\text{res}}$) go to `active_prompt_v/residual_metadata.json`; raw payloads ($o_j$) are saved in `external_storage_m/observations/`.

---

## Step-by-Step Handover Workflow

When `/session-handover` is invoked, execute the following checklist sequentially:

```markdown
- [ ] Phase 1: Context Ingestion & Scope Freezing
- [ ] Phase 2: Exact Decisions Extraction (H_exact)
- [ ] Phase 3: Sufficient Statistics Computation (H_stat)
- [ ] Phase 4: Residual Observations Selection (H_residual & M_res)
- [ ] Phase 5: Memory Budgeting & Channel Partitioning (V vs M)
- [ ] Phase 6: Serialization & Artifact Writing
- [ ] Phase 7: Deterministic Validation & Numerical Checks
- [ ] Phase 8: Ledger Logging & Session Handoff Summary
```

### Detailed Phase Execution:

1. **Phase 1: Context Ingestion & Scope Freezing**:
   - Parse entire pre-handover conversation history, user prompts, tool executions, and project instructions $(C, T)$.
   - Freeze state: do not accept new task mutations during serialization.

2. **Phase 2: Exact Decisions Extraction ($H_{\text{exact}}$)**:
   - Identify all decisions that permanently constrain next steps.
   - Extract rejected paths to prevent the recipient model from re-exploring failed approaches.
   - Record open issues verbatim. Map each entry to its origin source.
   - Populate `active_prompt_v/exact_decisions.json`.

3. **Phase 3: Sufficient Statistics Computation ($H_{\text{stat}}$)**:
   - Evaluate repeated numerical or structured data.
   - If task provides a formal sufficient statistic (e.g., Gaussian regression Gram matrices or cell counts), compute $(G_n, b_n)$, synthetic demos $(\widetilde{X}, \widetilde{y})$, or quantized cell means.
   - Otherwise, leave $H_{\text{stat}}$ null/empty. Do NOT invent heuristic lossy summaries.

4. **Phase 4: Residual Observations Selection ($H_{\text{residual}}$)**:
   - Identify non-compressible exceptions, rare failures, and edge cases.
   - Assign unique IDs (`res_001`, `res_002`) and write raw files to `external_storage_m/observations/`.
   - Add metadata tags and retrieval triggers to `active_prompt_v/residual_metadata.json`.

5. **Phase 5: Memory Budgeting ($V$ vs $M$)**:
   - Measure active prompt token size $b_{\text{act}}(V)$ against target budget $B_{\text{act}}$.
   - If $V$ exceeds budget, offload full observation texts from $V$ into $M_{\text{res}}$, retaining only lightweight pointers ($J_{\text{res}}$) in $V$.
   - Ensure total retained size satisfies $b_{\text{tot}}(V, M) \le B_{\text{tot}}$.

6. **Phase 6: Serialization & Artifact Writing**:
   - Write all files to `docs/icl_state/` using standard templates from `templates/`.
   - Ensure UTF-8 encoding and schema compliance.

7. **Phase 7: Deterministic Validation**:
   - Run `python docs/icl_state/validation/numerical_checks.py` (or execute `scripts/validate_handover.py`).
   - Confirm all required JSON schema fields exist, matrix dimensions match $d \times d$, and all referenced observation IDs exist on disk.

8. **Phase 8: Ledger Logging & Handoff Summary**:
   - Append session metrics to `docs/icl_state/logs/memory_account.csv` (prompt tokens, external bytes, active residual count, writer model).
   - Output structured handoff report to user with explicit instructions on how to resume in the new session.

---

## Degree of Freedom Calibration

- **Low Freedom (Strict Determinism)**:
  - Structure of `docs/icl_state/`.
  - Invariance of $H_{\text{exact}}$ (zero paraphrasing, no lossy rewriting of commitments).
  - Validation execution (`schema_definitions.json`, `numerical_checks.py`).
- **Medium Freedom (Calculated Heuristics)**:
  - Selection of residual failure cases for $H_{\text{residual}}$ based on criticality to downstream success.
  - Allocation of token budget between $H_{\text{stat}}$ and $J_{\text{res}}$ pointers.

---

## Gotchas & Anti-Patterns

- **Gotcha 1: The Prose Summary Trap**: Summarizing previous conversation in narrative prose loses exact negative constraints and mathematical statistics. Always use structured JSON/binary separation ($H_{\text{exact}}, H_{\text{stat}}, H_{\text{residual}}$).
- **Gotcha 2: Re-exploring Rejected Options**: If an architectural option was rejected in session 1, omitting it from $H_{\text{exact}}$ will cause the new model in session 2 to propose it again, wasting tokens and time.
- **Gotcha 3: Pre-Query State Coding Requirement**: Remember that the writer prepares the record BEFORE the user's next query $X$ is known. Never optimize the handover only for the last prompt; it must preserve sufficiency for the whole task domain $T$.
- **Gotcha 4: Phantom Residuals**: Referencing an observation ID in `residual_metadata.json` without creating the corresponding file in `external_storage_m/observations/` breaks deterministic verification.
- **Gotcha 5: Unvalidated Matrix Dimensions**: Quantizing or serializing sufficient statistics without verifying positive semidefiniteness $\overline{G} \succeq 0$ or symmetry can destabilize downstream posterior estimation.
- **Gotcha 6: Online Incremental Advantage**: In long sessions, updating `exact_decisions.json` immediately when a decision is made prevents forgetting and avoids costly end-of-session reconstruction.

---

## Progressive Disclosure References

- For in-depth mathematical formulations, proofs, and risk decomposition: see [`reference.md`](reference.md).
- For concrete schema templates and file examples: see [`examples.md`](examples.md).
- For reusable file blueprints: inspect [`templates/`](templates/).
- For CLI validation script: inspect [`scripts/validate_handover.py`](scripts/validate_handover.py).