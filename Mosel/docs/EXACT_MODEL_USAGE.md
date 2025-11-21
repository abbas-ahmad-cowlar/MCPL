# MCLP Exact Model Usage Guide

This guide explains how to use the exact MIP model for solving MCLP instances.

## 📋 Overview

**File**: `src/mclp_exact.mos`

The exact model implements the compact mathematical formulation from Cordeau, Furini & Ljubić (2016):

- **Variables**: Binary facility opening decisions (y) and customer coverage (z)
- **Objective**: Maximize total covered demand
- **Constraints**: Coverage linking, budget limit
- **Solver**: FICO Xpress Optimizer (MIP solver)

---

## 🚀 Quick Start

### Basic Usage

```bash
# Navigate to Mosel directory
cd Mosel

# Compile and run with default settings (test_tiny.dat)
mosel src/mclp_exact.mos

# Or compile and execute separately
mosel -c src/mclp_exact.mos
mosel exec mclp_exact.bim
```

### Run on Specific Instance

```bash
# Run on small instance S1
mosel src/mclp_exact.mos "DATA_FILE='data/S1.dat'"

# Run on medium instance M1
mosel src/mclp_exact.mos "DATA_FILE='data/M1.dat'"

# Run on large instance L1
mosel src/mclp_exact.mos "DATA_FILE='data/L1.dat'"
```

---

## ⚙️ Configuration Parameters

The model accepts several parameters that can be set at runtime:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DATA_FILE` | `"data/test_tiny.dat"` | Path to instance file |
| `TIME_LIMIT` | `3600` | Solver time limit (seconds) |
| `MIP_GAP` | `0.01` | Optimality gap tolerance (1%) |
| `VERBOSE` | `1` | Output level (0=quiet, 1=normal, 2=detailed) |
| `RELAX_Z` | `1` | Relax z variables to [0,1] (1=yes, 0=no) |

### Examples

**Run with custom time limit**:
```bash
mosel src/mclp_exact.mos "DATA_FILE='data/M1.dat'" "TIME_LIMIT=600"
```

**Run with detailed output**:
```bash
mosel src/mclp_exact.mos "DATA_FILE='data/S1.dat'" "VERBOSE=2"
```

**Run with strict binary formulation**:
```bash
mosel src/mclp_exact.mos "DATA_FILE='data/test_tiny.dat'" "RELAX_Z=0"
```

**Run quietly with tight optimality gap**:
```bash
mosel src/mclp_exact.mos "DATA_FILE='data/L1.dat'" "VERBOSE=0" "MIP_GAP=0.001"
```

---

## 📊 Understanding the Output

### Normal Output (VERBOSE=1)

```
======================================================================
MCLP EXACT MODEL - Compact Formulation
======================================================================
Instance: data/test_tiny.dat
Facilities: 4, Customers: 8
Budget: 5.0
======================================================================

Instance Statistics:
  Total facility cost:       9.00
  Total demand:            152.00
  Budget ratio:  55.56%
  Coverage density:  46.88%
  Coverage arcs: 15
✓ Data validation passed

Variable relaxation: z[j] ∈ [0,1] (continuous)

Model Statistics:
  Variables: 4 (y) + 8 (z) = 12
  Binary variables: 4 (y)
  Continuous variables: 8 (z)
  Coverage constraints: 8
  Budget constraint: 1
  Total constraints: 9

Starting optimization...
  Time limit: 3600 seconds
  MIP gap: 1.0%
======================================================================

[Solver output...]

======================================================================
SOLUTION STATUS
======================================================================
Status: OPTIMAL

OBJECTIVE:
  Covered demand:       117.00
  Best bound:           117.00

SOLUTION:
  Open facilities: 3 / 4
  Covered customers: 7 / 8 ( 87.5%)
  Budget used:       5.00 /       5.00 (100.0%)
  Total demand covered:     117.00 /     152.00 ( 77.0%)

COMPUTATIONAL:
  Solve time:     0.05 seconds
  Nodes explored: 3

OPEN FACILITIES:
  0 1 3

======================================================================
```

### Detailed Output (VERBOSE=2)

Additional sections include:
- Facility details (cost, customers covered)
- Customer details (demand, covering facilities)
- Solution validation checks

---

## 📐 Mathematical Model

### Decision Variables

**y[i]** ∈ {0,1} for i ∈ I (facilities)
- y[i] = 1 if facility i is opened
- y[i] = 0 otherwise

**z[j]** ∈ [0,1] for j ∈ J (customers)
- z[j] = 1 if customer j is covered
- z[j] = 0 otherwise
- Note: Can be relaxed to continuous without loss of optimality

### Objective Function

**Maximize**: Σ(j∈J) d[j] · z[j]

Maximize the total demand of covered customers.

### Constraints

**Coverage Constraints** (for each customer j):

Σ(i∈I_j) y[i] ≥ z[j]

At least one facility covering j must be open for j to be covered.

**Budget Constraint**:

Σ(i∈I) f[i] · y[i] ≤ B

Total cost of open facilities cannot exceed budget.

---

## 🎯 Expected Performance

### Small Instances (S1, S2)
- **Size**: 50 facilities, 200 customers
- **Expected solve time**: < 1 minute
- **Typical result**: Optimal solution

### Medium Instances (M1, M2)
- **Size**: 100 facilities, 500 customers
- **Expected solve time**: 1-10 minutes
- **Typical result**: Optimal solution or small gap

### Large Instances (L1, L2)
- **Size**: 200 facilities, 1000 customers
- **Expected solve time**: 10+ minutes (may hit time limit)
- **Typical result**: Near-optimal solution (small optimality gap)

**Note**: With community license, large instances may exceed variable limits (5000 variables/constraints).

---

## 🔍 Solution Validation

The model includes automatic validation checks:

1. **Budget Feasibility**: Verifies budget_used ≤ BUDGET
2. **Coverage Constraints**: Ensures no customer is marked covered without an open facility
3. **Variable Bounds**: Checks all variables within valid ranges

Enable with `VERBOSE=2` to see detailed validation output.

---

## ❌ Troubleshooting

### Error: "No valid license found"

**Solution**: Ensure Xpress Optimizer is licensed. See [SETUP.md](SETUP.md) for details.

```bash
# Check license
mosel -c "uses 'mmxprs'; exit"
```

### Error: "Variable limit exceeded"

**Cause**: Community license limits (5000 variables/constraints)

**Solution**:
- Use smaller instances (S1, S2, M1, M2)
- OR upgrade to academic/commercial license

### Error: "File not found"

**Cause**: Incorrect DATA_FILE path

**Solution**: Use relative path from Mosel directory:
```bash
mosel src/mclp_exact.mos "DATA_FILE='data/S1.dat'"
```

### Warning: "Time limit reached"

**Cause**: Large instance took too long to solve optimally

**Solution**:
- Increase TIME_LIMIT parameter
- Accept near-optimal solution with current gap
- Use heuristic methods (Phases 3-5) for faster solutions

### Issue: Model runs but no output

**Cause**: VERBOSE=0 or solver output suppressed

**Solution**: Set VERBOSE=1 or VERBOSE=2:
```bash
mosel src/mclp_exact.mos "VERBOSE=2"
```

---

## 🧪 Testing the Model

### Test on test_tiny.dat

This is the smallest instance, perfect for validating installation:

```bash
cd Mosel
mosel src/mclp_exact.mos
```

**Expected output**:
- Status: OPTIMAL
- Solve time: < 0.1 seconds
- Open facilities: 2-3 facilities
- Covered demand: ~115-120

### Test on S1.dat

Small instance to verify correctness:

```bash
mosel src/mclp_exact.mos "DATA_FILE='data/S1.dat'"
```

**Expected output**:
- Status: OPTIMAL
- Solve time: < 1 minute
- Coverage: ~30-40% of total demand

---

## 📈 Comparing with Python Implementation

To validate the Mosel implementation, compare results with Python:

**Python baseline** (from original implementation):
```bash
cd ..  # Go to MCPL root
python src/run_mclp.py --instance data/test_tiny.json --algorithm greedy
```

**Mosel exact model** (should achieve better or equal objective):
```bash
cd Mosel
mosel src/mclp_exact.mos
```

The exact model should find solutions equal to or better than Python heuristics.

---

## 💡 Best Practices

1. **Start small**: Test on test_tiny.dat before scaling up
2. **Set time limits**: Use TIME_LIMIT for large instances
3. **Monitor gaps**: Check optimality gap for solution quality
4. **Use relaxation**: Keep RELAX_Z=1 for better performance
5. **Save results**: Redirect output to file for analysis
   ```bash
   mosel src/mclp_exact.mos > results/S1_exact.txt
   ```

---

## 📚 References

**Cordeau, J.-F., Furini, F., & Ljubić, I. (2016)**
*Benders decomposition for very large scale partial set covering and maximal covering location problems.*
Computers & Operations Research, 66, 143–153.

**FICO Xpress Mosel Documentation**
- Language reference: $XPRESSDIR/docs/
- Optimizer guide: $XPRESSDIR/docs/optimizer/

---

## 🔄 Integration with Pipeline

This exact model serves as a **baseline** for comparing heuristics and metaheuristics:

1. **Phase 2 (Current)**: Exact model provides optimal/near-optimal solutions
2. **Phase 3**: Greedy and Closest Neighbor heuristics (fast, approximate)
3. **Phase 4**: Multi-start local search (improved quality)
4. **Phase 5**: Tabu search (best heuristic quality)
5. **Phase 6**: Compare all methods against exact solutions

---

**Updated**: November 21, 2025
**Author**: MCLP Migration Team
