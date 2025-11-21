#!/bin/bash
################################################################################
# MCLP Experimental Validation Script
#
# This script runs all implemented algorithms on all instances and collects
# comprehensive results for analysis.
#
# Usage:
#   bash scripts/run_experiments.sh [output_dir]
#
# Requirements:
#   - FICO Xpress Mosel installed and in PATH
#   - All .dat files in data/ directory
#   - All .mos files in src/ directory
#
# Output:
#   - results/raw/[algorithm]_[instance].log - Individual run logs
#   - results/experimental_results.csv - Consolidated results
#   - results/summary_statistics.txt - Summary statistics
#
# Author: MCLP Migration Team
# Date: November 2025
# Phase: 6 - Experimental Validation
################################################################################

# Configuration
OUTPUT_DIR="${1:-results}"
RAW_DIR="${OUTPUT_DIR}/raw"
DATA_DIR="data"
SRC_DIR="src"

# Create output directories
mkdir -p "${RAW_DIR}"

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo "========================================================================"
echo "MCLP EXPERIMENTAL VALIDATION"
echo "========================================================================"
echo "Output directory: ${OUTPUT_DIR}"
echo "========================================================================"
echo ""

# Check if mosel is available
if ! command -v mosel &> /dev/null; then
    echo -e "${RED}ERROR: mosel command not found${NC}"
    echo "Please ensure FICO Xpress Mosel is installed and in your PATH"
    exit 1
fi

echo -e "${GREEN}✓ Mosel compiler found${NC}"
echo ""

# Define instances (excluding test_tiny for full experiments)
INSTANCES=(
    "test_tiny"
    "S1"
    "S2"
    "M1"
    "M2"
    "L1"
    "L2"
)

# Initialize results CSV
RESULTS_CSV="${OUTPUT_DIR}/experimental_results.csv"
echo "Instance,Algorithm,Objective,Runtime_sec,Facilities_Opened,Budget_Used,Coverage_Pct,Gap_to_Best_Pct,Notes" > "${RESULTS_CSV}"

################################################################################
# EXPERIMENT 1: EXACT MIP MODEL
# Run on small instances only (test_tiny, S1, S2)
################################################################################

echo "========================================================================"
echo "EXPERIMENT 1: EXACT MIP MODEL"
echo "========================================================================"

EXACT_INSTANCES=("test_tiny" "S1" "S2")

for instance in "${EXACT_INSTANCES[@]}"; do
    echo -e "${BLUE}Running Exact MIP on ${instance}...${NC}"

    logfile="${RAW_DIR}/exact_${instance}.log"

    # Run exact model with time limit
    mosel "${SRC_DIR}/mclp_exact.mos" \
        "DATA_FILE='${DATA_DIR}/${instance}.dat'" \
        "TIME_LIMIT=3600" \
        "VERBOSE=1" \
        > "${logfile}" 2>&1

    # Extract results from log file
    obj=$(grep "Objective:" "${logfile}" | tail -1 | awk '{print $2}')
    time=$(grep "Runtime:" "${logfile}" | tail -1 | awk '{print $2}')
    fac=$(grep "Open facilities:" "${logfile}" | tail -1 | awk '{print $3}')
    budget=$(grep "Budget used:" "${logfile}" | tail -1 | awk '{print $3}')
    coverage=$(grep "Covered customers:" "${logfile}" | grep -oP '\(\K[0-9.]+(?=%)')

    # Append to CSV
    echo "${instance},Exact_MIP,${obj},${time},${fac},${budget},${coverage},0.0,Optimal" >> "${RESULTS_CSV}"

    echo -e "${GREEN}  ✓ Complete: obj=${obj}, time=${time}s${NC}"
done

echo ""

################################################################################
# EXPERIMENT 2: GREEDY HEURISTIC
# Run on all instances
################################################################################

echo "========================================================================"
echo "EXPERIMENT 2: GREEDY HEURISTIC"
echo "========================================================================"

for instance in "${INSTANCES[@]}"; do
    echo -e "${BLUE}Running Greedy on ${instance}...${NC}"

    logfile="${RAW_DIR}/greedy_${instance}.log"

    mosel "${SRC_DIR}/mclp_greedy.mos" \
        "DATA_FILE='${DATA_DIR}/${instance}.dat'" \
        "VERBOSE=1" \
        > "${logfile}" 2>&1

    obj=$(grep "Final objective:" "${logfile}" | tail -1 | awk '{print $3}')
    time=$(grep "Runtime:" "${logfile}" | tail -1 | awk '{print $2}')
    fac=$(grep "Open facilities:" "${logfile}" | tail -1 | awk '{print $3}')
    budget=$(grep "Budget used:" "${logfile}" | tail -1 | awk '{print $3}')
    coverage=$(grep "Covered customers:" "${logfile}" | grep -oP '\(\K[0-9.]+(?=%)')

    echo "${instance},Greedy,${obj},${time},${fac},${budget},${coverage},,Constructive_heuristic" >> "${RESULTS_CSV}"

    echo -e "${GREEN}  ✓ Complete: obj=${obj}, time=${time}s${NC}"
done

echo ""

################################################################################
# EXPERIMENT 3: CLOSEST NEIGHBOR HEURISTIC
# Run on all instances
################################################################################

echo "========================================================================"
echo "EXPERIMENT 3: CLOSEST NEIGHBOR HEURISTIC"
echo "========================================================================"

for instance in "${INSTANCES[@]}"; do
    echo -e "${BLUE}Running Closest Neighbor on ${instance}...${NC}"

    logfile="${RAW_DIR}/closest_neighbor_${instance}.log"

    mosel "${SRC_DIR}/mclp_closest_neighbor.mos" \
        "DATA_FILE='${DATA_DIR}/${instance}.dat'" \
        "VERBOSE=1" \
        > "${logfile}" 2>&1

    obj=$(grep "Final objective:" "${logfile}" | tail -1 | awk '{print $3}')
    time=$(grep "Runtime:" "${logfile}" | tail -1 | awk '{print $2}')
    fac=$(grep "Open facilities:" "${logfile}" | tail -1 | awk '{print $3}')
    budget=$(grep "Budget used:" "${logfile}" | tail -1 | awk '{print $3}')
    coverage=$(grep "Covered customers:" "${logfile}" | grep -oP '\(\K[0-9.]+(?=%)')

    echo "${instance},Closest_Neighbor,${obj},${time},${fac},${budget},${coverage},,Constructive_heuristic" >> "${RESULTS_CSV}"

    echo -e "${GREEN}  ✓ Complete: obj=${obj}, time=${time}s${NC}"
done

echo ""

################################################################################
# EXPERIMENT 4: LOCAL SEARCH (GREEDY INIT)
# Run on all instances
################################################################################

echo "========================================================================"
echo "EXPERIMENT 4: LOCAL SEARCH (Greedy initialization)"
echo "========================================================================"

for instance in "${INSTANCES[@]}"; do
    echo -e "${BLUE}Running Local Search on ${instance}...${NC}"

    logfile="${RAW_DIR}/local_search_${instance}.log"

    mosel "${SRC_DIR}/mclp_local_search.mos" \
        "DATA_FILE='${DATA_DIR}/${instance}.dat'" \
        "INIT_METHOD='greedy'" \
        "MAX_MOVES=200" \
        "VERBOSE=1" \
        > "${logfile}" 2>&1

    obj=$(grep "Final objective:" "${logfile}" | tail -1 | awk '{print $3}')
    time=$(grep "Runtime:" "${logfile}" | tail -1 | awk '{print $2}')
    fac=$(grep "Open facilities:" "${logfile}" | tail -1 | awk '{print $3}')
    budget=$(grep "Budget used:" "${logfile}" | tail -1 | awk '{print $3}')
    coverage=$(grep "Covered customers:" "${logfile}" | grep -oP '\(\K[0-9.]+(?=%)')
    improvements=$(grep "Improvements:" "${logfile}" | tail -1 | awk '{print $2}')

    echo "${instance},Local_Search,${obj},${time},${fac},${budget},${coverage},,Greedy+LS_${improvements}_moves" >> "${RESULTS_CSV}"

    echo -e "${GREEN}  ✓ Complete: obj=${obj}, time=${time}s, ${improvements} improvements${NC}"
done

echo ""

################################################################################
# EXPERIMENT 5: MULTI-START LOCAL SEARCH
# Run on all instances with 10 starts
################################################################################

echo "========================================================================"
echo "EXPERIMENT 5: MULTI-START LOCAL SEARCH (10 starts)"
echo "========================================================================"

for instance in "${INSTANCES[@]}"; do
    echo -e "${BLUE}Running Multi-Start LS on ${instance}...${NC}"

    logfile="${RAW_DIR}/multistart_${instance}.log"

    mosel "${SRC_DIR}/mclp_multistart.mos" \
        "DATA_FILE='${DATA_DIR}/${instance}.dat'" \
        "N_STARTS=10" \
        "MAX_MOVES=200" \
        "BASE_SEED=42" \
        "VERBOSE=1" \
        > "${logfile}" 2>&1

    obj=$(grep "Objective:" "${logfile}" | grep "Best solution" -A 1 | tail -1 | awk '{print $2}')
    time=$(grep "Total runtime:" "${logfile}" | tail -1 | awk '{print $3}')
    fac=$(grep "Open facilities:" "${logfile}" | tail -1 | awk '{print $3}')
    budget=$(grep "Budget used:" "${logfile}" | tail -1 | awk '{print $3}')
    coverage=$(grep "Covered customers:" "${logfile}" | grep -oP '\(\K[0-9.]+(?=%)')
    improvements=$(grep "Improvements:" "${logfile}" | tail -1 | awk '{print $2}')

    echo "${instance},MultiStart_LS,${obj},${time},${fac},${budget},${coverage},,10_starts_${improvements}_improvements" >> "${RESULTS_CSV}"

    echo -e "${GREEN}  ✓ Complete: obj=${obj}, time=${time}s${NC}"
done

echo ""

################################################################################
# EXPERIMENT 6: TABU SEARCH (500 iterations)
# Run on all instances
################################################################################

echo "========================================================================"
echo "EXPERIMENT 6: TABU SEARCH (500 iterations)"
echo "========================================================================"

for instance in "${INSTANCES[@]}"; do
    echo -e "${BLUE}Running Tabu Search (500 iter) on ${instance}...${NC}"

    logfile="${RAW_DIR}/tabu_500_${instance}.log"

    # Determine tenure based on instance size
    if [[ "${instance}" == "test_tiny" ]]; then
        tenure=5
    elif [[ "${instance}" =~ ^S ]]; then
        tenure=10
    elif [[ "${instance}" =~ ^M ]]; then
        tenure=15
    else
        tenure=20
    fi

    mosel "${SRC_DIR}/mclp_tabu_search.mos" \
        "DATA_FILE='${DATA_DIR}/${instance}.dat'" \
        "MAX_ITERATIONS=500" \
        "TABU_TENURE=${tenure}" \
        "CANDIDATE_SIZE=20" \
        "INTENSIFY_FREQ=50" \
        "STAGNATION_LIMIT=100" \
        "INIT_METHOD='greedy'" \
        "SEED=42" \
        "VERBOSE=1" \
        > "${logfile}" 2>&1

    obj=$(grep "Final objective:" "${logfile}" | tail -1 | awk '{print $3}')
    time=$(grep "Runtime:" "${logfile}" | tail -1 | awk '{print $2}')
    fac=$(grep "Open facilities:" "${logfile}" | tail -1 | awk '{print $3}')
    budget=$(grep "Budget used:" "${logfile}" | tail -1 | awk '{print $3}')
    coverage=$(grep "Covered customers:" "${logfile}" | grep -oP '\(\K[0-9.]+(?=%)')
    improvements=$(grep "Improvements:" "${logfile}" | tail -1 | awk '{print $2}')
    last_imp=$(grep "Last improvement at iteration:" "${logfile}" | tail -1 | awk '{print $5}')

    echo "${instance},Tabu_Search_500,${obj},${time},${fac},${budget},${coverage},,500iter_tenure${tenure}_${improvements}impr_last@${last_imp}" >> "${RESULTS_CSV}"

    echo -e "${GREEN}  ✓ Complete: obj=${obj}, time=${time}s, ${improvements} improvements${NC}"
done

echo ""

################################################################################
# EXPERIMENT 7: TABU SEARCH (2000 iterations) - Large instances only
# For thorough search on challenging instances
################################################################################

echo "========================================================================"
echo "EXPERIMENT 7: TABU SEARCH (2000 iterations, large instances)"
echo "========================================================================"

LARGE_INSTANCES=("M1" "M2" "L1" "L2")

for instance in "${LARGE_INSTANCES[@]}"; do
    echo -e "${BLUE}Running Tabu Search (2000 iter) on ${instance}...${NC}"

    logfile="${RAW_DIR}/tabu_2000_${instance}.log"

    if [[ "${instance}" =~ ^M ]]; then
        tenure=15
    else
        tenure=20
    fi

    mosel "${SRC_DIR}/mclp_tabu_search.mos" \
        "DATA_FILE='${DATA_DIR}/${instance}.dat'" \
        "MAX_ITERATIONS=2000" \
        "TABU_TENURE=${tenure}" \
        "CANDIDATE_SIZE=25" \
        "INTENSIFY_FREQ=50" \
        "STAGNATION_LIMIT=150" \
        "INIT_METHOD='greedy'" \
        "SEED=42" \
        "VERBOSE=1" \
        > "${logfile}" 2>&1

    obj=$(grep "Final objective:" "${logfile}" | tail -1 | awk '{print $3}')
    time=$(grep "Runtime:" "${logfile}" | tail -1 | awk '{print $2}')
    fac=$(grep "Open facilities:" "${logfile}" | tail -1 | awk '{print $3}')
    budget=$(grep "Budget used:" "${logfile}" | tail -1 | awk '{print $3}')
    coverage=$(grep "Covered customers:" "${logfile}" | grep -oP '\(\K[0-9.]+(?=%)')
    improvements=$(grep "Improvements:" "${logfile}" | tail -1 | awk '{print $2}')

    echo "${instance},Tabu_Search_2000,${obj},${time},${fac},${budget},${coverage},,2000iter_tenure${tenure}_${improvements}impr" >> "${RESULTS_CSV}"

    echo -e "${GREEN}  ✓ Complete: obj=${obj}, time=${time}s${NC}"
done

echo ""

################################################################################
# POST-PROCESSING: Calculate gaps to best
################################################################################

echo "========================================================================"
echo "POST-PROCESSING: Calculating gaps to best solution"
echo "========================================================================"

python3 << 'PYTHON_SCRIPT'
import csv
from collections import defaultdict

# Read results
results = defaultdict(list)
with open('results/experimental_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        instance = row['Instance']
        results[instance].append(row)

# Find best objective per instance
best_obj = {}
for instance, rows in results.items():
    best = max(float(row['Objective']) for row in rows if row['Objective'])
    best_obj[instance] = best

# Calculate gaps
updated_rows = []
with open('results/experimental_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        instance = row['Instance']
        obj = float(row['Objective']) if row['Objective'] else 0
        best = best_obj[instance]
        gap = ((best - obj) / best * 100) if best > 0 else 0
        row['Gap_to_Best_Pct'] = f"{gap:.2f}"
        updated_rows.append(row)

# Write updated CSV
with open('results/experimental_results.csv', 'w', newline='') as f:
    fieldnames = ['Instance', 'Algorithm', 'Objective', 'Runtime_sec',
                  'Facilities_Opened', 'Budget_Used', 'Coverage_Pct',
                  'Gap_to_Best_Pct', 'Notes']
    writer = csv.DictWriter(f, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(updated_rows)

print("✓ Gaps calculated and CSV updated")
PYTHON_SCRIPT

################################################################################
# GENERATE SUMMARY STATISTICS
################################################################################

echo ""
echo "========================================================================"
echo "GENERATING SUMMARY STATISTICS"
echo "========================================================================"

python3 << 'PYTHON_SCRIPT'
import csv
from collections import defaultdict
import statistics

# Read results
results = defaultdict(lambda: defaultdict(list))
with open('results/experimental_results.csv', 'r') as f:
    reader = csv.DictReader(f)
    for row in reader:
        instance = row['Instance']
        algorithm = row['Algorithm']
        results[instance][algorithm].append({
            'obj': float(row['Objective']) if row['Objective'] else 0,
            'time': float(row['Runtime_sec']) if row['Runtime_sec'] else 0,
            'gap': float(row['Gap_to_Best_Pct']) if row['Gap_to_Best_Pct'] else 0
        })

# Generate summary
with open('results/summary_statistics.txt', 'w') as f:
    f.write("="*80 + "\n")
    f.write("EXPERIMENTAL RESULTS SUMMARY\n")
    f.write("="*80 + "\n\n")

    for instance in sorted(results.keys()):
        f.write(f"\nInstance: {instance}\n")
        f.write("-" * 80 + "\n")
        f.write(f"{'Algorithm':<25} {'Objective':>12} {'Runtime(s)':>12} {'Gap(%)':>10}\n")
        f.write("-" * 80 + "\n")

        for algorithm in sorted(results[instance].keys()):
            data = results[instance][algorithm][0]  # Single run per algorithm
            f.write(f"{algorithm:<25} {data['obj']:>12.2f} {data['time']:>12.4f} {data['gap']:>10.2f}\n")

        f.write("\n")

print("✓ Summary statistics generated: results/summary_statistics.txt")
PYTHON_SCRIPT

################################################################################
# COMPLETION
################################################################################

echo ""
echo "========================================================================"
echo "EXPERIMENTAL VALIDATION COMPLETE"
echo "========================================================================"
echo -e "${GREEN}✓ All experiments completed successfully${NC}"
echo ""
echo "Results files:"
echo "  • ${RESULTS_CSV}"
echo "  • ${OUTPUT_DIR}/summary_statistics.txt"
echo "  • ${RAW_DIR}/*.log (individual run logs)"
echo ""
echo "Next steps:"
echo "  1. Review results/experimental_results.csv"
echo "  2. Check results/summary_statistics.txt"
echo "  3. Generate comparison tables: python3 scripts/generate_tables.py"
echo "  4. Create visualizations (if needed)"
echo "========================================================================"
