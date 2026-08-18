#!/usr/bin/env python3
"""
Template script for deterministic handover validation.
Verifies structure, schemas, matrix dimensions, symmetry, and residual integrity.
"""
import os
import sys
import json

def run_checks(base_dir="docs/icl_state"):
    errors = []
    
    exact_file = os.path.join(base_dir, "handover_state", "active_prompt_v", "exact_decisions.json")
    res_meta_file = os.path.join(base_dir, "handover_state", "active_prompt_v", "residual_metadata.json")
    stat_file = os.path.join(base_dir, "handover_state", "active_prompt_v", "sufficient_statistics.json")
    
    # Check exact decisions file
    if not os.path.exists(exact_file):
        errors.append(f"Missing file: {exact_file}")
    else:
        try:
            with open(exact_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                required = ["primary_goal", "binding_decisions", "rejected_alternatives", "active_constraints", "unresolved_issues"]
                for req in required:
                    if req not in data:
                        errors.append(f"Missing required field '{req}' in {exact_file}")
        except Exception as e:
            errors.append(f"Failed to parse JSON in {exact_file}: {e}")

    # Check residual pointers
    if os.path.exists(res_meta_file):
        try:
            with open(res_meta_file, "r", encoding="utf-8") as f:
                res_data = json.load(f)
                for ptr in res_data.get("residual_pointers", []):
                    rel = ptr.get("relative_path", "")
                    full = os.path.join(base_dir, "handover_state", rel) if not os.path.isabs(rel) else rel
                    if not os.path.exists(full):
                        errors.append(f"Broken pointer '{ptr.get('id')}': file not found at {full}")
        except Exception as e:
            errors.append(f"Failed to parse JSON in {res_meta_file}: {e}")

    # Check matrix symmetry if statistics are present
    if os.path.exists(stat_file):
        try:
            with open(stat_file, "r", encoding="utf-8") as f:
                sdata = json.load(f)
                if sdata.get("statistic_type") == "gaussian_linear_regression_gram":
                    G = sdata.get("gram_matrix_G_n", [])
                    d = sdata.get("dimension_d", len(G))
                    if len(G) != d or any(len(row) != d for row in G):
                        errors.append(f"Gram matrix dimensions do not match dimension_d={d}")
                    for i in range(d):
                        for j in range(i + 1, d):
                            if abs(G[i][j] - G[j][i]) > 1e-6:
                                errors.append(f"Gram matrix asymmetry detected at ({i},{j}) vs ({j},{i})")
        except Exception as e:
            errors.append(f"Failed to parse JSON in {stat_file}: {e}")

    if errors:
        print("[ERROR] Handover state failed validation:")
        for err in errors:
            print(f"  - {err}")
        return False

    print("[SUCCESS] All deterministic handover checks passed.")
    return True

if __name__ == "__main__":
    success = run_checks()
    sys.exit(0 if success else 1)
