# MCLP Heuristics Usage Guide

This guide explains how to use the Greedy and Closest Neighbor heuristics for solving MCLP instances.

## 📋 Overview

**Phase 3** implements two fast constructive heuristics:

1. **Greedy Heuristic** (`mclp_greedy.mos`) - Value-based selection
2. **Closest Neighbor** (`mclp_closest_neighbor.mos`) - Distance-based selection

Both heuristics provide fast, good-quality solutions suitable for:
- Large instances where exact solving is too slow
- Initial solutions for metaheuristics
- Baseline comparisons
- Real-time applications

---

## 🚀 Quick Start

### Greedy Heuristic

```bash
# Navigate to Mosel directory
cd Mosel

# Run with default settings (test_tiny.dat)
mosel src/mclp_greedy.mos

# Run on specific instance
mosel src/mclp_greedy.mos "DATA_FILE='data/S1.dat'"

# Run with detailed output
mosel src/mclp_greedy.mos "DATA_FILE='data/M1.dat'" "VERBOSE=2"
```

### Closest Neighbor Heuristic

```bash
# Run with default settings
mosel src/mclp_closest_neighbor.mos

# Run on specific instance
mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/S1.dat'"

# Run with detailed output
mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/M1.dat'" "VERBOSE=2"
```

---

## ⚙️ Parameters

Both heuristics accept the following parameters:

| Parameter | Default | Description |
|-----------|---------|-------------|
| `DATA_FILE` | `"data/test_tiny.dat"` | Path to instance file |
| `SEED` | `42` | Random seed (for tie-breaking) |
| `VERBOSE` | `1` | Output level (0=quiet, 1=normal, 2=detailed) |

### Examples

**Quiet mode** (minimal output):
```bash
mosel src/mclp_greedy.mos "DATA_FILE='data/L1.dat'" "VERBOSE=0"
```

**Detailed mode** (full trace):
```bash
mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/S1.dat'" "VERBOSE=2"
```

---

## 📊 Understanding the Output

### Normal Output (VERBOSE=1)

**Greedy Example**:
```
======================================================================
MCLP GREEDY HEURISTIC
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

Starting Greedy Construction...
----------------------------------------------------------------------

GREEDY SOLUTION:
  Iterations: 2
  Open facilities: 2 / 4
  Covered customers: 7 / 8 ( 87.5%)
  Budget used:       4.00 /       5.00 ( 80.0%)
  Total demand covered:     142.00 /     152.00 ( 93.4%)
  Runtime:     0.0012 seconds

OPEN FACILITIES:
  2 3

======================================================================
```

**Closest Neighbor Example**:
```
======================================================================
MCLP CLOSEST NEIGHBOR HEURISTIC
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

Starting Closest Neighbor Construction...
----------------------------------------------------------------------

CLOSEST NEIGHBOR SOLUTION:
  Customers processed: 8
  Facilities opened: 2
  Open facilities: 2 / 4
  Covered customers: 7 / 8 ( 87.5%)
  Budget used:       4.00 /       5.00 ( 80.0%)
  Total demand covered:     142.00 /     152.00 ( 93.4%)
  Runtime:     0.0008 seconds

OPEN FACILITIES:
  2 3

======================================================================
```

### Detailed Output (VERBOSE=2)

Additional information includes:
- **Greedy**: Iteration-by-iteration facility selection with gain/cost ratios
- **Closest Neighbor**: Customer processing order and facility selection details
- **Both**: Facility details, customer coverage, and solution validation

---

## 🔬 Algorithm Comparison

| Feature | Greedy | Closest Neighbor |
|---------|--------|------------------|
| **Selection Criterion** | Max coverage gain / cost | Nearest facility (by cost) |
| **Customer Priority** | Implicit (via gain) | Explicit (sorted by demand) |
| **Time Complexity** | O(nI² · nJ) | O(nJ · nI · log(nI)) |
| **Typical Runtime** | 1-5 seconds (large) | 0.5-3 seconds (large) |
| **Solution Quality** | Generally better | Good for high-demand focus |
| **Best For** | Balanced value/cost | Customer prioritization |

### When to Use Each

**Use Greedy when**:
- You want best average solution quality
- Budget allows opening multiple facilities
- Balanced coverage is important
- Value per cost is key metric

**Use Closest Neighbor when**:
- Speed is critical
- High-demand customers must be prioritized
- Distance/proximity matters
- Budget is very tight

---

## 📈 Expected Performance

### Solution Quality (% of Optimal)

| Instance Size | Greedy | Closest Neighbor |
|---------------|--------|------------------|
| Small (S1, S2) | 80-95% | 75-90% |
| Medium (M1, M2) | 75-90% | 70-85% |
| Large (L1, L2) | 70-85% | 65-80% |

### Runtime

| Instance | Facilities | Customers | Greedy | Closest Neighbor |
|----------|-----------|-----------|--------|------------------|
| test_tiny | 4 | 8 | < 0.01s | < 0.01s |
| S1, S2 | 50 | 200 | < 0.1s | < 0.05s |
| M1, M2 | 100 | 500 | < 1s | < 0.5s |
| L1, L2 | 200 | 1000 | 1-5s | 0.5-3s |

**Note**: Both heuristics are significantly faster than exact solving (100-1000x speedup on large instances)

---

## 🧪 Testing and Validation

### Test on test_tiny.dat

```bash
# Greedy
mosel src/mclp_greedy.mos

# Closest Neighbor
mosel src/mclp_closest_neighbor.mos
```

**Expected Results** (both should find similar solutions):
- Open facilities: 2-3
- Covered demand: 115-142
- Runtime: < 0.01 seconds

### Compare Both Heuristics

Run both and compare:

```bash
echo "=== GREEDY ===" > results/heuristics_comparison.txt
mosel src/mclp_greedy.mos "DATA_FILE='data/S1.dat'" >> results/heuristics_comparison.txt

echo "=== CLOSEST NEIGHBOR ===" >> results/heuristics_comparison.txt
mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/S1.dat'" >> results/heuristics_comparison.txt
```

### Validation Checks (VERBOSE=2)

Both heuristics include automatic validation:
1. Budget constraint satisfaction
2. Coverage relationship consistency
3. Objective value verification

---

## 💡 Best Practices

1. **Start with small instances**: Test on test_tiny.dat first
2. **Compare with exact**: Run exact model on small instances to gauge quality
3. **Use appropriate verbosity**:
   - VERBOSE=0 for batch runs
   - VERBOSE=1 for normal usage
   - VERBOSE=2 for debugging
4. **Save results**: Redirect output to files for analysis
5. **Test both heuristics**: Different instances favor different approaches

### Batch Processing Example

```bash
# Test both heuristics on all instances
for instance in test_tiny S1 S2 M1 M2 L1 L2; do
  echo "Processing $instance..."
  mosel src/mclp_greedy.mos "DATA_FILE='data/$instance.dat'" \
    > results/greedy_$instance.txt
  mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/$instance.dat'" \
    > results/cn_$instance.txt
done
```

---

## 🔄 Integration with Pipeline

These heuristics serve multiple purposes:

1. **Standalone Solutions**: Fast approximate solutions for large instances
2. **Initialization**: Starting points for local search (Phase 4) and tabu search (Phase 5)
3. **Baseline Comparison**: Benchmark for exact model and metaheuristics
4. **Performance Analysis**: Study algorithm behavior on different instance types

**Pipeline Flow**:
```
Phase 1: Data → Phase 2: Exact Model (optimal baseline)
                      ↓
Phase 3: Heuristics (fast baseline) → Phase 4: Local Search (improve)
                      ↓
Phase 5: Tabu Search (best heuristic quality)
                      ↓
Phase 6: Experimental Comparison
```

---

## 📚 Pseudocode Reference

Detailed algorithm pseudocode available in:
- `pseudocode/greedy_pseudocode.txt`
- `pseudocode/closest_neighbor_pseudocode.txt`

These files include:
- Complete algorithm specifications
- Example executions
- Complexity analysis
- Correctness properties
- Comparison with optimal solutions

---

## ❌ Troubleshooting

### Issue: "No facility provides positive gain"

**Cause**: All uncovered customers are outside coverage radius or budget insufficient

**Solution**: This is expected behavior when budget is very tight. Check:
```bash
mosel src/mclp_greedy.mos "VERBOSE=2"
```
Look for which customers remain uncovered.

### Issue: Very low coverage (< 50%)

**Causes**:
1. Budget too small for instance
2. Sparse coverage matrix
3. High facility costs relative to budget

**Solution**:
- Check budget ratio in output
- Try different instance
- Compare with exact model to verify instance difficulty

### Issue: Runtime longer than expected

**Cause**: Large instance with dense coverage matrix

**Solution**:
- Expected for large instances (L1, L2)
- Still much faster than exact model
- Use VERBOSE=0 to reduce output overhead

---

## 📊 Comparison with Python Implementation

To validate Mosel implementation against original Python:

**Python**:
```bash
cd ..  # Go to MCPL root
python src/run_mclp.py --instance data/S1.json --algorithm greedy --seed 42
python src/run_mclp.py --instance data/S1.json --algorithm cn --seed 42
```

**Mosel**:
```bash
cd Mosel
mosel src/mclp_greedy.mos "DATA_FILE='data/S1.dat'" "SEED=42"
mosel src/mclp_closest_neighbor.mos "DATA_FILE='data/S1.dat'" "SEED=42"
```

**Expected**: Objective values should match within 1-5% (small variations due to tie-breaking)

---

## 🎯 Next Steps

After running heuristics:

1. **Compare with Exact**: How close are heuristics to optimal?
2. **Proceed to Phase 4**: Use heuristic solutions as input to local search
3. **Proceed to Phase 5**: Initialize tabu search with heuristic solutions
4. **Experiment**: Test on all 7 instances and analyze patterns

---

**Updated**: November 21, 2025
**Author**: MCLP Migration Team
