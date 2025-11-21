# MCLP Mosel Implementation - User Guide

**Version**: 1.0
**Date**: November 21, 2025
**Status**: Complete

---

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Algorithm Selection Guide](#algorithm-selection-guide)
4. [Quick Reference](#quick-reference)
5. [Detailed Usage](#detailed-usage)
6. [Experimental Validation](#experimental-validation)
7. [Troubleshooting](#troubleshooting)
8. [Best Practices](#best-practices)
9. [FAQ](#faq)

---

## 1. Introduction

### 1.1 What is MCLP?

The Maximum Covering Location Problem (MCLP) is a facility location optimization problem where you select facilities to maximize covered customer demand within a budget constraint.

**Real-World Applications**:
- Emergency service location (ambulances, fire stations)
- Retail store placement
- Warehouse location planning
- Wireless network tower placement

### 1.2 This Implementation

This Mosel implementation provides **6 solution methods**:

1. **Exact MIP** - Optimal solutions (small instances)
2. **Greedy** - Fast constructive heuristic
3. **Closest Neighbor** - Alternative constructive heuristic
4. **Local Search** - Improvement method
5. **Multi-Start Local Search** - Robust quality
6. **Tabu Search** - Best heuristic quality

### 1.3 When to Use This Guide

- ✅ You have FICO Xpress Mosel installed
- ✅ You have MCLP instance data files
- ✅ You want to solve facility location problems
- ✅ You need guidance on algorithm selection

---

## 2. Getting Started

### 2.1 Prerequisites

**Required Software**:
- FICO Xpress Mosel (any recent version)
- Xpress Optimizer license
- Command line terminal

**Optional Software**:
- Python 3.6+ (for data conversion and analysis)
- Bash shell (for automated experiments)

### 2.2 Installation

1. **Clone or download** the Mosel directory

2. **Verify Mosel is installed**:
```bash
mosel --version
```

3. **Check instance files**:
```bash
ls Mosel/data/*.dat
```

You should see 7 files: `test_tiny.dat`, `S1.dat`, `S2.dat`, `M1.dat`, `M2.dat`, `L1.dat`, `L2.dat`

### 2.3 Your First Run

**Test the installation** with a tiny instance:

```bash
cd Mosel
mosel src/mclp_greedy.mos "DATA_FILE='data/test_tiny.dat'"
```

**Expected output**:
```
======================================================================
MCLP GREEDY HEURISTIC
======================================================================
Instance: data/test_tiny.dat
Facilities: 4, Customers: 8
Budget: 5.00
======================================================================

GREEDY SOLUTION:
  Open facilities: 3
  Covered customers: 7 / 8 (87.5%)
  Budget used: 4.90 / 5.00
  Final objective: 7.20 / 8.00 (90.0%)
  Runtime: 0.0015 seconds
```

If you see this, you're ready to go! ✅

---

## 3. Algorithm Selection Guide

### 3.1 Decision Tree

```
Do you NEED a provably optimal solution?
├─ YES → Is instance small (≤100 facilities)?
│         ├─ YES → Use EXACT MIP ✓
│         └─ NO  → Not feasible, use Tabu Search instead
│
└─ NO  → What's your time budget?
          ├─ < 1 second   → Use GREEDY ✓
          ├─ 1-10 seconds → Use LOCAL SEARCH ✓
          ├─ 10-60 seconds → Use MULTI-START LS ✓
          └─ 60+ seconds  → Use TABU SEARCH ✓
```

### 3.2 Algorithm Comparison

| Algorithm | Runtime | Quality | When to Use |
|-----------|---------|---------|-------------|
| **Exact MIP** | Minutes-Hours | 100% (optimal) | Small instances, optimality required |
| **Greedy** | < 1 second | 70-85% | Quick checks, warm starts |
| **Closest Neighbor** | < 1 second | 65-80% | Alternative heuristic |
| **Local Search** | 1-15 seconds | 80-92% | Improvement after greedy |
| **Multi-Start LS** | 10-100 seconds | 85-95% | Production systems |
| **Tabu Search** | 30-240 seconds | 90-98% | Best quality needed |

### 3.3 Recommendations by Scenario

**Scenario 1: Quick Feasibility Check**
- Algorithm: **Greedy**
- Runtime: < 1 second
- Command:
```bash
mosel src/mclp_greedy.mos "DATA_FILE='data/your_instance.dat'"
```

**Scenario 2: Daily Production Planning**
- Algorithm: **Multi-Start Local Search**
- Runtime: 10-30 seconds
- Command:
```bash
mosel src/mclp_multistart.mos "DATA_FILE='data/your_instance.dat'" "N_STARTS=10"
```

**Scenario 3: Strategic Planning (Best Quality)**
- Algorithm: **Tabu Search (2000 iterations)**
- Runtime: 30-240 seconds
- Command:
```bash
mosel src/mclp_tabu_search.mos \
  "DATA_FILE='data/your_instance.dat'" \
  "MAX_ITERATIONS=2000" \
  "VERBOSE=1"
```

**Scenario 4: Optimal Solution (Small Instance)**
- Algorithm: **Exact MIP**
- Runtime: Minutes
- Command:
```bash
mosel src/mclp_exact.mos \
  "DATA_FILE='data/S1.dat'" \
  "TIME_LIMIT=3600" \
  "VERBOSE=1"
```

---

## 4. Quick Reference

### 4.1 Command Cheat Sheet

**Run Greedy Heuristic**:
```bash
mosel src/mclp_greedy.mos "DATA_FILE='data/M1.dat'"
```

**Run Closest Neighbor**:
```bash
mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/M1.dat'"
```

**Run Local Search**:
```bash
mosel src/mclp_local_search.mos "DATA_FILE='data/M1.dat'" "MAX_MOVES=200"
```

**Run Multi-Start (10 starts)**:
```bash
mosel src/mclp_multistart.mos "DATA_FILE='data/M1.dat'" "N_STARTS=10"
```

**Run Tabu Search (500 iterations)**:
```bash
mosel src/mclp_tabu_search.mos \
  "DATA_FILE='data/M1.dat'" \
  "MAX_ITERATIONS=500" \
  "TABU_TENURE=15"
```

**Run Exact MIP**:
```bash
mosel src/mclp_exact.mos \
  "DATA_FILE='data/S1.dat'" \
  "TIME_LIMIT=1800"
```

### 4.2 Common Parameters

| Parameter | Default | Description | Range |
|-----------|---------|-------------|-------|
| `DATA_FILE` | (required) | Instance file path | Any .dat file |
| `VERBOSE` | 1 | Output level | 0, 1, 2 |
| `SEED` | 42 | Random seed | Any integer |
| `MAX_ITERATIONS` | 500 | TS iterations | 100-5000 |
| `MAX_MOVES` | 200 | LS max moves | 50-1000 |
| `N_STARTS` | 10 | Multi-start runs | 5-50 |
| `TABU_TENURE` | 10 | Tabu list tenure | 5-30 |
| `TIME_LIMIT` | 3600 | MIP time limit (sec) | 60-7200 |

---

## 5. Detailed Usage

### 5.1 Exact MIP Model

**Purpose**: Find provably optimal solutions

**When to use**: Small instances (≤100 facilities), optimality required

**Basic usage**:
```bash
mosel src/mclp_exact.mos \
  "DATA_FILE='data/S1.dat'" \
  "VERBOSE=1"
```

**Advanced usage**:
```bash
mosel src/mclp_exact.mos \
  "DATA_FILE='data/S2.dat'" \
  "TIME_LIMIT=1800" \
  "MIP_GAP=0.001" \
  "VERBOSE=2"
```

**Parameters**:
- `TIME_LIMIT`: Max runtime in seconds (default: 3600)
- `MIP_GAP`: Optimality tolerance (default: 0.001 = 0.1%)
- `VERBOSE`: 0 (quiet), 1 (normal), 2 (detailed)

**Output interpretation**:
```
EXACT MIP SOLUTION:
  Status: Optimal              ← Solution quality
  Objective: 165.34            ← Covered demand
  Open facilities: 9 / 50      ← Facilities selected
  Budget used: 9.95 / 10.00    ← Budget utilization
  MIP gap: 0.00%               ← Optimality gap
  Runtime: 245.67 seconds      ← Solve time
```

**See also**: [EXACT_MODEL_USAGE.md](EXACT_MODEL_USAGE.md)

### 5.2 Greedy Heuristic

**Purpose**: Fast constructive heuristic

**When to use**: Quick solutions, warm starts, baselines

**Basic usage**:
```bash
mosel src/mclp_greedy.mos "DATA_FILE='data/M1.dat'"
```

**Parameters**:
- `DATA_FILE`: Instance file (required)
- `VERBOSE`: Output level (default: 1)

**How it works**:
1. Start with empty solution
2. Repeat until budget exhausted:
   - Find facility with max coverage gain per cost
   - Add to solution
3. Return constructed solution

**Performance**:
- Runtime: < 1 second (all sizes)
- Quality: 70-85% of optimal
- Deterministic (same result every run)

**See also**: [HEURISTICS_USAGE.md](HEURISTICS_USAGE.md)

### 5.3 Closest Neighbor Heuristic

**Purpose**: Alternative constructive approach

**When to use**: Diversification, customer-centric planning

**Basic usage**:
```bash
mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/M1.dat'"
```

**Parameters**:
- `DATA_FILE`: Instance file (required)
- `VERBOSE`: Output level (default: 1)

**How it works**:
1. Sort customers by demand (high to low)
2. For each high-demand customer:
   - Find cheapest facility that covers it
   - Add facility if budget allows
3. Return constructed solution

**Performance**:
- Runtime: < 1 second (all sizes)
- Quality: 65-80% of optimal
- Deterministic

**See also**: [HEURISTICS_USAGE.md](HEURISTICS_USAGE.md)

### 5.4 Local Search

**Purpose**: Improve existing solution

**When to use**: After greedy, as component of multi-start

**Basic usage**:
```bash
mosel src/mclp_local_search.mos \
  "DATA_FILE='data/M1.dat'" \
  "MAX_MOVES=200"
```

**Advanced usage**:
```bash
mosel src/mclp_local_search.mos \
  "DATA_FILE='data/L1.dat'" \
  "INIT_METHOD='greedy'" \
  "MAX_MOVES=500" \
  "VERBOSE=2"
```

**Parameters**:
- `INIT_METHOD`: "greedy" or "random" (default: "greedy")
- `MAX_MOVES`: Maximum moves (default: 200)
- `SEED`: Random seed (default: 42)

**Neighborhoods**:
- **1-flip**: Open or close single facility
- **Swap**: Close one facility, open another

**Performance**:
- Runtime: 1-15 seconds
- Quality: 80-92% of optimal
- Improvement over greedy: 5-10%

**See also**: [HEURISTICS_USAGE.md](HEURISTICS_USAGE.md)

### 5.5 Multi-Start Local Search

**Purpose**: Robust high-quality solutions

**When to use**: Production systems, when time budget allows

**Basic usage**:
```bash
mosel src/mclp_multistart.mos \
  "DATA_FILE='data/M1.dat'" \
  "N_STARTS=10"
```

**Advanced usage**:
```bash
mosel src/mclp_multistart.mos \
  "DATA_FILE='data/L2.dat'" \
  "N_STARTS=20" \
  "MAX_MOVES=300" \
  "BASE_SEED=42" \
  "VERBOSE=1"
```

**Parameters**:
- `N_STARTS`: Number of starts (default: 10)
- `MAX_MOVES`: Max moves per start (default: 200)
- `BASE_SEED`: Base random seed (default: 42)

**Initialization strategies**:
- Start 1: Greedy
- Start 2: Closest Neighbor
- Starts 3-6: Perturbed Greedy
- Starts 7-10: Random

**Performance**:
- Runtime: 10-100 seconds (10 starts)
- Quality: 85-95% of optimal
- Very consistent across runs

**See also**: [HEURISTICS_USAGE.md](HEURISTICS_USAGE.md)

### 5.6 Tabu Search

**Purpose**: Best heuristic quality

**When to use**: Critical applications, best solution needed

**Basic usage**:
```bash
mosel src/mclp_tabu_search.mos \
  "DATA_FILE='data/M1.dat'" \
  "MAX_ITERATIONS=500"
```

**Advanced usage**:
```bash
mosel src/mclp_tabu_search.mos \
  "DATA_FILE='data/L1.dat'" \
  "MAX_ITERATIONS=2000" \
  "TABU_TENURE=20" \
  "CANDIDATE_SIZE=30" \
  "INTENSIFY_FREQ=50" \
  "STAGNATION_LIMIT=150" \
  "SEED=42" \
  "VERBOSE=1"
```

**Parameters**:
- `MAX_ITERATIONS`: Total iterations (default: 500)
- `TABU_TENURE`: Tabu list tenure (default: 10)
- `CANDIDATE_SIZE`: Candidate list size (default: 20)
- `INTENSIFY_FREQ`: Intensification frequency (default: 50)
- `STAGNATION_LIMIT`: Diversification trigger (default: 100)

**Mechanisms**:
1. **Tabu list**: Prevents cycling
2. **Aspiration**: Override tabu for best solutions
3. **Candidate list**: Efficient move evaluation
4. **Intensification**: Periodic local search
5. **Diversification**: Shake on stagnation

**Performance**:
- Runtime: 5-240 seconds (500-2000 iter)
- Quality: 90-98% of optimal
- Consistent high quality

**See also**: [TABU_SEARCH_USAGE.md](TABU_SEARCH_USAGE.md)

---

## 6. Experimental Validation

### 6.1 Running All Experiments

**Execute full validation suite**:
```bash
cd Mosel
bash scripts/run_experiments.sh
```

This runs **45 algorithm executions** across all 7 instances.

**Expected duration**: 30-60 minutes

**Outputs**:
- `results/experimental_results.csv`
- `results/summary_statistics.txt`
- `results/raw/*.log` (individual run logs)

### 6.2 Generating Analysis

**Create comparison tables**:
```bash
python3 scripts/generate_tables.py
```

**Outputs**:
- `results/comparison_tables.md`
- `results/statistical_analysis.md`

### 6.3 Interpreting Results

**CSV columns**:
- `Instance`: Instance name
- `Algorithm`: Algorithm name
- `Objective`: Covered demand
- `Runtime_sec`: Execution time
- `Gap_to_Best_Pct`: Gap to best solution (%)

**Good solution indicators**:
- Gap < 5% (excellent)
- Gap < 10% (good)
- Gap < 20% (acceptable)

**See also**: [EXPERIMENTAL_VALIDATION.md](EXPERIMENTAL_VALIDATION.md)

---

## 7. Troubleshooting

### 7.1 Common Issues

**Issue: "mosel: command not found"**

**Cause**: Mosel not installed or not in PATH

**Solution**:
```bash
# Add Mosel to PATH
export PATH=$PATH:/path/to/xpress/bin

# Verify
mosel --version
```

---

**Issue: "Cannot open file 'data/S1.dat'"**

**Cause**: Wrong working directory or missing data file

**Solution**:
```bash
# Check you're in Mosel directory
pwd  # Should end with /Mosel

# Verify data file exists
ls data/S1.dat

# Use correct path
mosel src/mclp_greedy.mos "DATA_FILE='data/S1.dat'"
```

---

**Issue: "No solution found" or very poor quality**

**Cause**: Instance may be infeasible or algorithm parameters need tuning

**Solution**:
1. Check budget is reasonable: `Budget ≥ cheapest facility cost`
2. Verify coverage: Ensure facilities can cover customers
3. Try different algorithm
4. Increase iterations/moves for iterative methods

---

**Issue: Runtime is too long**

**Cause**: Instance too large or too many iterations

**Solution**:
1. Reduce `MAX_ITERATIONS` or `MAX_MOVES`
2. Reduce `N_STARTS` for multi-start
3. Use faster algorithm (Greedy instead of Tabu Search)
4. Try smaller instance first

---

**Issue: Results not reproducible**

**Cause**: Different random seed

**Solution**:
```bash
# Always specify same seed
mosel src/mclp_tabu_search.mos \
  "DATA_FILE='data/M1.dat'" \
  "SEED=42"
```

---

### 7.2 Getting Help

**Documentation**:
- Read algorithm-specific usage guides in `docs/`
- Check pseudocode for algorithm details
- Review phase completion reports

**Debugging**:
- Use `VERBOSE=2` for detailed output
- Check `results/raw/*.log` for run logs
- Verify instance data format

**Contact**:
- Refer to project repository for issues
- Check FINAL_IMPLEMENTATION_REPORT.md for details

---

## 8. Best Practices

### 8.1 Workflow Recommendations

**Standard Workflow**:
1. **Start with Greedy** - Quick baseline in < 1 second
2. **Run Tabu Search** - Best quality in 30-120 seconds
3. **Compare results** - See improvement
4. **Use best solution** - Deploy or analyze

**Comparison Workflow**:
1. **Run all algorithms** - Use `run_experiments.sh`
2. **Generate tables** - Use `generate_tables.py`
3. **Analyze trade-offs** - Quality vs runtime
4. **Select best fit** - Based on requirements

**Production Workflow**:
1. **Greedy for feasibility** - Quick check
2. **Multi-Start for robustness** - Main solution
3. **Tabu Search for critical cases** - When quality paramount
4. **Log all runs** - Track performance over time

### 8.2 Parameter Tuning

**Tabu Search tenure** (instance-dependent):
- Small (50 facilities): tenure = 10
- Medium (100 facilities): tenure = 15
- Large (200 facilities): tenure = 20
- Formula: `tenure ≈ sqrt(nI)` to `2*sqrt(nI)`

**Iterations/Moves** (time budget):
- Quick run: 200-500
- Normal run: 500-2000
- Thorough run: 2000-5000

**Multi-Start runs**:
- Quick: 5 starts
- Normal: 10 starts
- Robust: 20+ starts

### 8.3 Performance Optimization

**For speed**:
- Use Greedy or Closest Neighbor
- Reduce iterations/moves
- Use smaller candidate list

**For quality**:
- Use Tabu Search with 2000 iterations
- Increase candidate list size
- More frequent intensification

**For robustness**:
- Use Multi-Start with 20+ starts
- Try multiple random seeds
- Compare across algorithms

---

## 9. FAQ

**Q: Which algorithm should I use?**

A: Depends on your needs:
- **Need optimal**: Exact MIP (small instances only)
- **Need fast**: Greedy (< 1 second)
- **Need quality**: Tabu Search (30-120 seconds)
- **Need robustness**: Multi-Start LS (10-60 seconds)

---

**Q: How do I know if my solution is good?**

A: Compare to benchmarks:
- Run Exact MIP on small instance to get optimal
- Run multiple algorithms and compare
- Check gap percentage: < 5% is excellent, < 10% is good
- Compare to literature results if available

---

**Q: Can I use my own instance data?**

A: Yes! Convert to Mosel .dat format:
```bash
python3 utilities/convert_json_to_mosel.py your_instance.json
```

See [DATA_FORMAT.md](DATA_FORMAT.md) for format specification.

---

**Q: How do I parallelize Multi-Start?**

A: Current implementation is sequential. For parallel execution:
1. Run individual starts separately with different seeds
2. Combine results manually
3. Or implement parallel version using Mosel's parallel features

---

**Q: Why is Exact MIP slow on large instances?**

A: MCLP is NP-hard. Exact MIP has exponential worst-case complexity.
- Small instances (50-100 facilities): Manageable
- Large instances (200+ facilities): Use heuristics instead

---

**Q: Can I change the objective function?**

A: Yes, but requires code modification:
- Edit .mos file objective definition
- Adjust delta-evaluation functions
- See [FINAL_IMPLEMENTATION_REPORT.md](FINAL_IMPLEMENTATION_REPORT.md) for details

---

**Q: How do I visualize solutions?**

A: Current implementation outputs facility IDs. To visualize:
1. Parse output to get facility list
2. Use your preferred visualization tool (Python matplotlib, etc.)
3. Plot facilities and customers with coverage arcs

---

**Q: What if I get "out of memory" errors?**

A: For very large instances:
1. Use heuristics (not Exact MIP)
2. Reduce candidate list size
3. Process in batches if possible
4. Increase system RAM or use larger machine

---

**Q: How accurate are the expected runtimes?**

A: Runtimes vary by hardware:
- Modern desktop/laptop: As documented
- Older systems: 2-3× slower
- High-performance server: 2-3× faster

Run `test_tiny` instance to calibrate.

---

**Q: Can I use this for other covering problems?**

A: Partially. The framework applies to:
- ✅ Maximal covering location problem (MCLP)
- ✅ Partial set covering (with modifications)
- ⚠️ Set covering problem (requires objective change)
- ⚠️ P-median (requires distance minimization objective)

---

## Summary

This user guide provides complete information for using the MCLP Mosel implementation:

✅ **Algorithm selection** - Decision tree and comparison
✅ **Quick reference** - Command cheat sheets
✅ **Detailed usage** - All 6 algorithms documented
✅ **Experimental validation** - How to run and analyze experiments
✅ **Troubleshooting** - Common issues and solutions
✅ **Best practices** - Workflows and parameter tuning
✅ **FAQ** - Answers to common questions

**For more details**, see:
- [FINAL_IMPLEMENTATION_REPORT.md](FINAL_IMPLEMENTATION_REPORT.md) - Complete project report
- [EXPERIMENTAL_VALIDATION.md](EXPERIMENTAL_VALIDATION.md) - Validation guide
- Algorithm-specific usage guides in `docs/`

**Ready to solve your MCLP instances!** 🚀

---

**Document Version**: 1.0
**Last Updated**: November 21, 2025
**Status**: Complete
