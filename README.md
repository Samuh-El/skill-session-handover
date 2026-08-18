# Session Handover Protocol (In-Context Learning State Transfer)

[![Agent Skills Compatible](https://img.shields.io/badge/Agent%20Skills-Compatible-blue.svg)](https://skills.sh)
[![arXiv:2608.14528](https://img.shields.io/badge/arXiv-2608.14528-b31b1b.svg)](https://arxiv.org/html/2608.14528v1)

This repository provides an enterprise-grade Agent Skill specification and operational protocol for executing mathematically verifiable In-Context Learning (ICL) state transfers across Large Language Model (LLM) session boundaries, architectural migrations, and context window resets.

---

## Executive Summary and Purpose

In complex multi-stage agent workflows, transitioning execution across session boundaries or switching model instances routinely introduces context degradation, loss of architectural constraints, and redundant re-evaluation of previously rejected implementations.

The Session Handover Protocol addresses these operational inefficiencies by establishing a formal procedure for agents to serialize active working context into a structured, three-part state record prior to session termination or handoff. This mechanism ensures:

- **Constraint Preservation**: Inviolable operational constraints, project objectives, and rejected technical options are preserved without semantic alteration or paraphrasing.
- **Statistical Sufficiency**: Task domains equipped with formal mathematical compression criteria maintain compact representations, such as Gram matrices and synthetic demonstrations.
- **Residual Observation Archiving**: Non-compressible singular observations, rare execution failures, and edge cases are archived to external storage with referenced metadata pointers.

---

## Academic Foundation and Citation

The architectural design and theoretical guarantees of this specification derive directly from the peer-reviewed research formulation:

> **Handover of In-Context Learning State Across Session Boundaries**  
> Authors: Masahiro Kato & Taka Kato (2026)  
> Publication Reference: [arXiv:2608.14528](https://arxiv.org/html/2608.14528v1)

---

## Technical Architecture

State retention is managed across active context memory and secondary file storage under `docs/icl_state/`:

1. **Exact Component ($H_{\text{exact}}$)**  
   Contains immutable binding decisions, explicit operational boundaries, rejected technical alternatives with rationale, and unresolved items. Content within this partition must not undergo heuristic summarization.

2. **Statistical Component ($H_{\text{stat}}$)**  
   Contains mathematically verified sufficient statistics, synthetic demonstrations, or cell partition parameters applicable when formal error bounds are established.

3. **Residual Component ($H_{\text{residual}}$ and $M_{\text{res}}$)**  
   Archives critical individual observations and failure logs in external secondary storage (`external_storage_m/`), retaining lightweight indexed pointers ($J_{\text{res}}$) in active memory.

---

## Deployment and Execution

### Package Installation

This specification can be integrated into compatible agent environments via the Agent Skills CLI:

```bash
npx skills add Samuh-El/skill-session-handover
```

### Protocol Invocation

The handover sequence is initiated via the command line interface:

```text
/session-handover
```

Upon execution, the agent completes an eight-phase workflow covering context freezing, decision extraction, statistical computation, channel partitioning, schema validation, and ledger record logging.

---

## Repository Structure

- [`SKILL.md`](SKILL.md): Core operational specification, frontmatter metadata, and execution checklists.
- [`docs/USE_MANUAL_ENG.md`](docs/USE_MANUAL_ENG.md): Step-by-step user manual and trigger scenarios (English).
- [`docs/MANUAL DE USO_SPA.md`](docs/MANUAL%20DE%20USO_SPA.md): Step-by-step user manual and trigger scenarios (Spanish).
- [`reference.md`](reference.md): Mathematical formulations, proof structures, and analytical derivations.
- [`examples.md`](examples.md): Schema definitions, structural templates, and memory account ledgers.
- [`templates/`](templates/): Standardized JSON and CSV templates for state record generation.
- [`scripts/validate_handover.py`](scripts/validate_handover.py): Automated verification utility for schema compliance and disk reference integrity.

---

## License

This software is released under the terms of the MIT License.
