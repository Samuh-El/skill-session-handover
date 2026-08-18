#!/usr/bin/env python3
"""
CLI Validation Script for Session Handover State
Compliant with arXiv:2608.14528 ICL State Protocol.

Usage:
  python validate_handover.py [--dir docs/icl_state]
"""

import os
import sys
import json
import argparse

def validate_handover(base_dir):
    print(f"[*] Validating Handover State in directory: {base_dir}")
    errors = []
    warnings = []

    handover_state = os.path.join(base_dir, "handover_state")
    active_prompt_v = os.path.join(handover_state, "active_prompt_v")
    external_storage_m = os.path.join(handover_state, "external_storage_m")
    validation_dir = os.path.join(base_dir, "validation")
    logs_dir = os.path.join(base_dir, "logs")

    # 1. Directory Structure Checks
    for d in [handover_state, active_prompt_v, external_storage_m, validation_dir, logs_dir]:
        if not os.path.isdir(d):
            errors.append(f"Directory missing: {d}")

    # 2. Exact Decisions Check
    exact_file = os.path.join(active_prompt_v, "exact_decisions.json")
    if not os.path.isfile(exact_file):
        errors.append(f"Missing mandatory file: {exact_file}")
    else:
        try:
            with open(exact_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                required_keys = ["protocol_version", "primary_goal", "binding_decisions", "rejected_alternatives", "active_constraints", "unresolved_issues"]
                for k in required_keys:
                    if k not in data:
                        errors.append(f"Field '{k}' missing from {exact_file}")
                
                # Check binding decisions
                for idx, dec in enumerate(data.get("binding_decisions", [])):
                    for field in ["decision_id", "summary", "rationale", "source"]:
                        if field not in dec:
                            errors.append(f"Decision #{idx} missing field '{field}' in {exact_file}")
        except Exception as e:
            errors.append(f"JSON error in {exact_file}: {e}")

    # 3. Residual Metadata & Pointers Check
    res_file = os.path.join(active_prompt_v, "residual_metadata.json")
    if os.path.isfile(res_file):
        try:
            with open(res_file, "r", encoding="utf-8") as f:
                res_data = json.load(f)
                pointers = res_data.get("residual_pointers", [])
                for ptr in pointers:
                    ptr_id = ptr.get("id", "unknown")
                    rel_path = ptr.get("relative_path", "")
                    target_path = os.path.join(handover_state, rel_path) if not os.path.isabs(rel_path) else rel_path
                    if not os.path.exists(target_path):
                        errors.append(f"Residual pointer '{ptr_id}' references non-existent file: {target_path}")
        except Exception as e:
            errors.append(f"JSON error in {res_file}: {e}")
    else:
        warnings.append("No residual_metadata.json found (empty residual state).")

    # 4. Sufficient Statistics Checks (if present)
    stat_file = os.path.join(active_prompt_v, "sufficient_statistics.json")
    stat_bin = os.path.join(active_prompt_v, "sufficient_statistics.bin")
    if os.path.isfile(stat_file):
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
            errors.append(f"Error validating statistics in {stat_file}: {e}")
    elif not os.path.exists(stat_bin):
        warnings.append("No sufficient_statistics found in active_prompt_v (H_stat is empty).")

    # Summary
    print("\n" + "="*50)
    if warnings:
        print("[!] Warnings:")
        for w in warnings:
            print(f"    - {w}")
            
    if errors:
        print("[X] Validation FAILED with errors:")
        for e in errors:
            print(f"    - {e}")
        print("="*50)
        return False
    else:
        print("[V] Handover state is VALID and fully compliant with ICL protocol.")
        print("="*50)
        return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Validate ICL Handover State Directory")
    parser.add_argument("--dir", default="docs/icl_state", help="Path to docs/icl_state directory")
    args = parser.parse_args()
    
    success = validate_handover(args.dir)
    sys.exit(0 if success else 1)
