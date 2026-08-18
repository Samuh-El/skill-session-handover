# Concrete Examples: Session Handover Artifacts

This file provides production-ready, concrete examples for every artifact defined in the `session-handover` architecture, covering both parametric and nonparametric tasks.

---

## 1. Exact Decisions Record: `active_prompt_v/exact_decisions.json` ($H_{\text{exact}}$)

```json
{
  "protocol_version": "1.1.0",
  "task_identifier": "autonomous-data-pipeline-v2",
  "primary_goal": "Refactor data extraction pipeline to stream Parquet chunks into S3 with sub-second latency.",
  "current_milestone": "Phase 2 - Parquet serialization and memory throttling",
  "binding_decisions": [
    {
      "decision_id": "dec_001",
      "summary": "Use Arrow streaming writer with snappy compression.",
      "rationale": "Gives 4x faster throughput than zstd in local benchmarks without exceeding 512MB RAM.",
      "source": "turn_14_user_confirmation"
    },
    {
      "decision_id": "dec_002",
      "summary": "Database connection pool capped at 8 workers.",
      "rationale": "Prevents RDS Postgres connection exhaustion under high load.",
      "source": "turn_22_tool_test"
    }
  ],
  "rejected_alternatives": [
    {
      "rejected_id": "rej_001",
      "approach": "In-memory Pandas DataFrame accumulation.",
      "rejection_reason": "Causes OOM errors on tables exceeding 5M rows.",
      "verdict": "PERMANENTLY_REJECTED"
    },
    {
      "rejected_id": "rej_002",
      "approach": "Synchronous HTTP upload to S3 bucket.",
      "rejection_reason": "Introduces 800ms bottleneck per chunk.",
      "verdict": "PERMANENTLY_REJECTED"
    }
  ],
  "active_constraints": [
    "Peak RAM consumption must stay below 512MB at all times.",
    "Do NOT introduce external non-standard C++ dependencies (pure Python / PyArrow only)."
  ],
  "unresolved_issues": [
    {
      "issue_id": "issue_001",
      "description": "Handle transient S3 SlowDown 503 errors during burst window.",
      "proposed_direction": "Implement exponential backoff with jitter in uploader worker."
    }
  ]
}
```

---

## 2. Sufficient Statistics Examples ($H_{\text{stat}}$)

### Example A: Parametric Bayesian Linear Regression (`active_prompt_v/sufficient_statistics.json`)
```json
{
  "statistic_type": "gaussian_linear_regression_gram",
  "dimension_d": 3,
  "sample_count_n": 10000,
  "gram_matrix_G_n": [
    [1250.45, 340.12, 89.20],
    [340.12, 980.60, 210.55],
    [89.20, 210.55, 450.30]
  ],
  "cross_vector_b_n": [
    450.80,
    312.40,
    188.90
  ],
  "noise_variance_sigma_sq": 0.25,
  "synthetic_demonstrations": {
    "num_rows_r": 3,
    "X_tilde": [
      [35.361, 9.618, 2.522],
      [0.0, 29.801, 6.251],
      [0.0, 0.0, 20.104]
    ],
    "y_tilde": [
      12.748,
      6.365,
      4.120
    ]
  }
}
```

### Example B: Nonparametric Cell Partition (`active_prompt_v/nonparametric_cells.json`)
```json
{
  "statistic_type": "nonparametric_cell_partition",
  "dimension_d": 2,
  "total_cells_M": 4,
  "quantization_step_q": 0.05,
  "cells": [
    { "cell_index": 1, "bounds": [[0.0, 0.5], [0.0, 0.5]], "count_N_j": 250, "quantized_mean_Y_j": 1.45 },
    { "cell_index": 2, "bounds": [[0.5, 1.0], [0.0, 0.5]], "count_N_j": 180, "quantized_mean_Y_j": 2.10 },
    { "cell_index": 3, "bounds": [[0.0, 0.5], [0.5, 1.0]], "count_N_j": 310, "quantized_mean_Y_j": -0.85 },
    { "cell_index": 4, "bounds": [[0.5, 1.0], [0.5, 1.0]], "count_N_j": 0,   "quantized_mean_Y_j": 0.00 }
  ]
}
```

---

## 3. Residual Metadata Pointers: `active_prompt_v/residual_metadata.json` ($J_{\text{res}}$)

```json
{
  "total_residuals": 2,
  "residual_pointers": [
    {
      "id": "failure_case_001",
      "relative_path": "external_storage_m/observations/failure_case_001.txt",
      "category": "TOOL_EXECUTION_FAILURE",
      "trigger_condition": "When parsing malformed UTF-8 byte sequences in customer feedback payloads.",
      "summary": "FastAPI JSON decode error on raw byte stream containing unescaped null bytes."
    },
    {
      "id": "rare_example_002",
      "relative_path": "external_storage_m/observations/rare_example_002.json",
      "category": "CORNER_CASE_INPUT",
      "trigger_condition": "When tenant account has zero active subscriptions but active trial credits.",
      "summary": "Billing calculator edge case resulting in DivisionByZero if trial rate is unconfigured."
    }
  ]
}
```

---

## 4. Residual Observation File: `external_storage_m/observations/failure_case_001.txt` ($M_{\text{res}}$)

```txt
=== HANDOVER RESIDUAL OBSERVATION: failure_case_001 ===
Timestamp: 2026-08-18T10:15:00Z
Origin: Tool execution in Session #1
Context: Ingestion worker attempting to deserialize incoming webhook payload.

[STACK TRACE]
Traceback (most recent call last):
  File "/app/workers/ingest.py", line 84, in parse_payload
    payload_obj = json.loads(raw_bytes.decode('utf-8'))
UnicodeDecodeError: 'utf-8' codec can't decode byte 0x89 in position 14: invalid start byte

[CRITICAL INVARIANT]
Do NOT use raw .decode('utf-8') directly on socket chunks.
Always use errors='replace' or pass raw bytes through sanitize_binary_stream() before JSON decoding.
```

---

## 5. Schema Definitions: `validation/schema_definitions.json`

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "ExactDecisionsSchema",
  "type": "object",
  "required": [
    "protocol_version",
    "primary_goal",
    "binding_decisions",
    "rejected_alternatives",
    "active_constraints",
    "unresolved_issues"
  ],
  "properties": {
    "protocol_version": { "type": "string" },
    "primary_goal": { "type": "string", "minLength": 5 },
    "binding_decisions": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["decision_id", "summary", "rationale", "source"]
      }
    },
    "rejected_alternatives": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["rejected_id", "approach", "rejection_reason", "verdict"]
      }
    },
    "active_constraints": {
      "type": "array",
      "items": { "type": "string" }
    },
    "unresolved_issues": {
      "type": "array",
      "items": {
        "type": "object",
        "required": ["issue_id", "description"]
      }
    }
  }
}
```

---

## 6. Numerical Checks Script: `validation/numerical_checks.py`

```python
#!/usr/bin/env python3
"""
Deterministic numerical and structural validator for ICL handover state.
Verifies file existence, JSON schemas, matrix dimensions, symmetry, and residual integrity.
"""
import os
import sys
import json

def validate_state(base_dir="docs/icl_state"):
    errors = []
    
    # 1. Path existence checks
    active_prompt_dir = os.path.join(base_dir, "handover_state", "active_prompt_v")
    external_dir = os.path.join(base_dir, "handover_state", "external_storage_m")
    
    exact_file = os.path.join(active_prompt_dir, "exact_decisions.json")
    res_meta_file = os.path.join(active_prompt_dir, "residual_metadata.json")
    stat_file = os.path.join(active_prompt_dir, "sufficient_statistics.json")
    
    if not os.path.isfile(exact_file):
        errors.append(f"Missing exact decisions file: {exact_file}")
    else:
        with open(exact_file, "r", encoding="utf-8") as f:
            try:
                data = json.load(f)
                for field in ["primary_goal", "binding_decisions", "rejected_alternatives", "active_constraints"]:
                    if field not in data:
                        errors.append(f"Field '{field}' missing from {exact_file}")
            except Exception as e:
                errors.append(f"Invalid JSON in {exact_file}: {e}")

    # 2. Residual pointer integrity
    if os.path.isfile(res_meta_file):
        with open(res_meta_file, "r", encoding="utf-8") as f:
            try:
                res_data = json.load(f)
                for ptr in res_data.get("residual_pointers", []):
                    rel_path = ptr.get("relative_path")
                    full_path = os.path.join(base_dir, "handover_state", rel_path) if not os.path.isabs(rel_path) else rel_path
                    if not os.path.exists(full_path):
                        errors.append(f"Broken residual pointer '{ptr.get('id')}': file not found at {full_path}")
            except Exception as e:
                errors.append(f"Invalid JSON in {res_meta_file}: {e}")

    # 3. Statistical Matrix Checks (if present)
    if os.path.isfile(stat_file):
        with open(stat_file, "r", encoding="utf-8") as f:
            try:
                sdata = json.load(f)
                if sdata.get("statistic_type") == "gaussian_linear_regression_gram":
                    G = sdata.get("gram_matrix_G_n", [])
                    d = sdata.get("dimension_d", len(G))
                    if len(G) != d or any(len(row) != d for row in G):
                        errors.append(f"Gram matrix dimensions do not match dimension_d={d}")
                    # Check symmetry
                    for i in range(d):
                        for j in range(i + 1, d):
                            if abs(G[i][j] - G[j][i]) > 1e-6:
                                errors.append(f"Gram matrix asymmetry detected at ({i},{j}) vs ({j},{i})")
            except Exception as e:
                errors.append(f"Error parsing statistics file {stat_file}: {e}")

    if errors:
        print("[FAIL] Handover validation failed with the following errors:")
        for err in errors:
            print(f"  - {err}")
        return False
    
    print("[PASS] Handover deterministic validation successful. All constraints verified.")
    return True

if __name__ == "__main__":
    success = validate_state()
    sys.exit(0 if success else 1)
```

---

## 7. Memory Accounting Ledger: `logs/memory_account.csv`

```csv
timestamp,session_id,prompt_tokens_v,external_bytes_m,total_residuals,handover_status,writer_model
2026-08-18T10:20:00Z,sess_001,480,4120,2,VALIDATED_SUCCESS,gemini-3.7-flash
```
