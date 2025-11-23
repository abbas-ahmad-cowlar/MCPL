#!/usr/bin/env python3
"""
Add missing variable declarations to Mosel files.

This script adds proper declarations for all undeclared variables
in the Mosel source files.
"""

import re
from pathlib import Path

def add_declarations_to_file(filepath, declarations_block, insert_after_pattern):
    """Add declarations block to a Mosel file after a specific pattern."""
    
    with open(filepath, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # Find the line to insert after
    insert_index = -1
    for i, line in enumerate(lines):
        if insert_after_pattern in line:
            insert_index = i + 1
            break
    
    if insert_index == -1:
        print(f"  ⚠ Pattern not found in {filepath}")
        return False
    
    # Insert the declarations block
    lines.insert(insert_index, "\n")
    lines.insert(insert_index + 1, declarations_block)
    lines.insert(insert_index + 2, "\n")
    
    # Write back
    with open(filepath, 'w', encoding='utf-8') as f:
        f.writelines(lines)
    
    return True

def main():
    print("=" * 70)
    print("Adding Variable Declarations to Mosel Files")
    print("=" * 70)
    print()
    
    mosel_dir = Path("src")
    
    # Define declarations for each file
    files_to_fix = {
        "mclp_greedy.mos": {
            "pattern": "end-initializations",
            "declarations": """  declarations
    ! Additional variables
    covered: set of integer
    best_fac: integer
    best_ratio: real
    new_cust: set of integer
    ratio: real
    temp: integer
    fac: integer
    fac_list: array(range) of integer
    idx: integer
  end-declarations"""
        },
        "mclp_closest_neighbor.mos": {
            "pattern": "end-initializations",
            "declarations": """  declarations
    ! Additional variables
    covered: set of integer
    best_fac: integer
    customer: integer
    cust_array: array(range) of integer
    demand_array: array(range) of real
    temp_d: real
    temp_c: integer
    best_cost: real
  end-declarations"""
        },
        "mclp_local_search.mos": {
            "pattern": "end-initializations",
            "declarations": """  declarations
    ! Additional variables
    covered: set of integer
    best_fac: integer
    best_ratio: real
    new_cust: set of integer
    ratio: real
    fac_list: array(range) of integer
    temp: integer
    fac: integer
    loss: real
    returned: real
  end-declarations"""
        },
        "mclp_multistart.mos": {
            "pattern": "end-initializations",
            "declarations": """  declarations
    ! Additional variables
    overall_start_time: real
    seed: integer
    init_method: string
    use_greedy: boolean
    use_cn: boolean
    use_random: boolean
    perturb: boolean
    covered: set of integer
    best_fac: integer
    best_ratio: real
    new_cust: set of integer
    ratio: real
    num_remove: integer
    fac_array: array(range) of integer
    idx: integer
    rem_fac: integer
    cand_array: array(range) of integer
    add_fac: integer
    cust_array: array(range) of integer
    demand_array: array(range) of real
    temp_d: real
    temp_c: integer
    customer: integer
    best_cost: real
  end-declarations"""
        },
        "mclp_tabu_search.mos": {
            "pattern": "end-initializations",
            "declarations": """  declarations
    ! Additional variables
    covered: set of integer
    best_fac: integer
    best_ratio: real
    new_cust: set of integer
    ratio: real
    fac_array: array(range) of integer
    temp: integer
    fac: integer
    initial_obj: real
    improvements: integer
    stagnation_counter: integer
    last_improvement_iter: integer
    num_candidates: integer
    loss: real
    delta: real
    gain: real
  end-declarations"""
        }
    }
    
    for filename, config in files_to_fix.items():
        filepath = mosel_dir / filename
        if not filepath.exists():
            print(f"⚠ File not found: {filepath}")
            continue
        
        print(f"Processing: {filename}")
        
        # Read file and check if declarations already added
        with open(filepath, 'r') as f:
            content = f.read()
        
        if "! Additional variables" in content:
            print(f"  - Already has additional declarations, skipping")
            continue
        
        # Add declarations
        if add_declarations_to_file(filepath, config["declarations"], config["pattern"]):
            print(f"  ✓ Added declarations")
        else:
            print(f"  ✗ Failed to add declarations")
    
    print()
    print("=" * 70)
    print("Done!")
    print("=" * 70)

if __name__ == "__main__":
    main()
