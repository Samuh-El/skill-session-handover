# User Manual

## When and on what occasions should /session-handover be invoked?

You should invoke the skill in any of these 4 key situations:

1. **Context Saturation (Token Window Almost Full)**: When the conversation has accumulated many turns or tool executions and you notice slowness, degradation in responses, or are approaching the model's token limit.
2. **Model or Agent Switch**: When you started with a high-reasoning model (for example, to plan and design the architecture) and wish to hand off execution to a faster or code-specialized model.
3. **Work Session Pause or End of Day**: When you are about to close the environment or finish your session for the day and want to ensure all technical decisions, rejected paths, and constraints are frozen to resume tomorrow without data loss.
4. **Noisy Context Cleanup**: When there was extensive trial-and-error debugging in the chat and you wish to "reset the conversation from scratch" without losing approved decisions or learned constraints.

## Step-by-Step Guide

- **Phase 1: In the Current Session (Before closing or switching models)**: 
    1. Type the command in the chat:
    ```
    /session-handover
    ```
    The agent will act as the "Writer":
    * Freeze the active working context.
    * Create the `docs/icl_state/` directory in your project if it does not exist.
    * Extract goals, binding decisions made, rejected alternatives (to prevent re-proposing them), and open issues into `exact_decisions.json`.
    * Save residual observations (rare errors, log payloads) in `external_storage_m/observations/`.
    * Run the deterministic validation script to confirm that no file is corrupted.
    * Deliver a closing handoff summary confirming that the state record is safely persisted.
- **Phase 2: In the New Session (Upon resuming or switching models)**:
    1. Open your new chat window or initiate a new session with your preferred model.
    2. Send the initial resumption prompt:
    "Resume project work by reading the handover state record in docs/icl_state/handover_state/active_prompt_v/exact_decisions.json. Strictly respect previously established decisions and rejected alternatives."

- In this way, the new model will:
    * Read the rigid memory using minimal prompt tokens.
    * Assimilate binding constraints without inventing or re-exploring failed paths.
    * Query pointers in `residual_metadata.json` on-demand if details of previous failures are required.
    * Continue the task exactly where it was left off.
