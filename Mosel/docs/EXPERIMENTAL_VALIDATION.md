# Experimental Validation Guide

**Phase**: 6 - Experimental Validation
**Purpose**: Run all algorithms on all instances and analyze results
**Status**: Framework Ready

---

## 📋 Overview

This guide provides complete instructions for running experimental validation of all MCLP algorithms on all benchmark instances.

**Validation Objectives**:
1. Verify algorithm correctness
2. Measure solution quality
3. Compare runtime performance
4. Analyze trade-offs between methods
5. Provide recommendations for practitioners

---

## 🚀 Quick Start

### Step 1: Run All Experiments

```bash
cd Mosel
bash scripts/run_experiments.sh
```

This will:
- Run Exact MIP on small instances (test_tiny, S1, S2)
- Run all heuristics on all 7 instances
- Collect comprehensive statistics
- Generate `results/experimental_results.csv`

**Expected Runtime**: 30-60 minutes (depending on hardware)

### Step 2: Generate Comparison Tables

```bash
python3 scripts/generate_tables.py
```

This will:
- Create `results/comparison_tables.md`
- Create `results/statistical_analysis.md`
- Generate rankings and recommendations

### Step 3: Review Results

Open the generated files:
- `results/experimental_results.csv` - Raw data
- `results/comparison_tables.md` - Formatted tables
- `results/statistical_analysis.md` - Analysis and insights

---

## 📊 Experiments Overview

### Experiment Suite

| Exp# | Algorithm | Instances | Runs | Purpose |
|------|-----------|-----------|------|---------|
| 1 | Exact MIP | test_tiny, S1, S2 | 1 | Optimal benchmarks |
| 2 | Greedy | All 7 | 1 | Fast construction |
| 3 | Closest Neighbor | All 7 | 1 | Alternative heuristic |
| 4 | Local Search | All 7 | 1 | Improvement method |
| 5 | Multi-Start LS | All 7 | 10 starts | Robust quality |
| 6 | Tabu Search (500) | All 7 | 1 | Metaheuristic |
| 7 | Tabu Search (2000) | M1, M2, L1, L2 | 1 | Thorough search |

**Total Runs**: ~45 algorithm executions

### Instance Characteristics

| Instance | Facilities | Customers | Budget | Expected Difficulty |
|----------|-----------|-----------|--------|---------------------|
| test_tiny | 4 | 8 | 5.00 | Trivial (testing) |
| S1 | 50 | 200 | 10.00 | Small |
| S2 | 50 | 200 | 10.00 | Small |
| M1 | 100 | 500 | 15.00 | Medium |
| M2 | 100 | 500 | 20.00 | Medium |
| L1 | 200 | 1000 | 20.00 | Large |
| L2 | 200 | 1000 | 30.00 | Large |

---

## ⚙️ Configuration Details

### Algorithm Parameters

**Exact MIP**:
- Time limit: 3600 seconds (1 hour)
- MIP gap tolerance: 0.1%
- Only run on small instances

**Greedy Heuristic**:
- Deterministic (no parameters)
- Selection: Max coverage gain per cost

**Closest Neighbor**:
- Deterministic (no parameters)
- Selection: Min cost facility per high-demand customer

**Local Search**:
- Initialization: Greedy
- Max moves: 200
- Strategy: First-improvement

**Multi-Start Local Search**:
- Number of starts: 10
- Max moves per start: 200
- Initialization: Greedy, CN, Perturbed (×4), Random (×4)
- Seed: 42

**Tabu Search (500 iterations)**:
- Max iterations: 500
- Tabu tenure: 10 (S), 15 (M), 20 (L)
- Candidate size: 20
- Intensification frequency: 50
- Stagnation limit: 100
- Initialization: Greedy
- Seed: 42

**Tabu Search (2000 iterations)**:
- Max iterations: 2000
- Tabu tenure: 15 (M), 20 (L)
- Candidate size: 25
- Intensification frequency: 50
- Stagnation limit: 150
- Initialization: Greedy
- Seed: 42

---

## 📈 Expected Results

### Solution Quality (% of Optimal)

| Algorithm | Small (S1-S2) | Medium (M1-M2) | Large (L1-L2) |
|-----------|---------------|----------------|---------------|
| Greedy | 75-85% | 70-80% | 68-78% |
| Closest Neighbor | 70-80% | 68-78% | 65-75% |
| Local Search | 80-92% | 78-90% | 75-88% |
| Multi-Start LS | 85-95% | 82-92% | 80-90% |
| Tabu Search (500) | 90-97% | 88-96% | 85-95% |
| Tabu Search (2000) | - | 90-97% | 88-97% |

### Runtime Expectations

| Algorithm | Small | Medium | Large |
|-----------|-------|--------|-------|
| Exact MIP | 10-300s | 300-3600s | Not feasible |
| Greedy | < 0.5s | < 1s | < 2s |
| Closest Neighbor | < 0.5s | < 1s | < 2s |
| Local Search | < 1s | < 5s | < 15s |
| Multi-Start LS | < 10s | < 30s | < 100s |
| Tabu Search (500) | ~5s | ~20s | ~60s |
| Tabu Search (2000) | - | ~80s | ~240s |

---

## 🔍 Validation Checklist

### Pre-Execution Checks

- [ ] FICO Xpress Mosel installed and in PATH
- [ ] All .dat files exist in `data/` directory
- [ ] All .mos files exist in `src/` directory
- [ ] Python 3.6+ available for post-processing
- [ ] Sufficient disk space for log files (~100 MB)
- [ ] Sufficient time for execution (~1 hour)

### Post-Execution Checks

- [ ] All log files generated in `results/raw/`
- [ ] `experimental_results.csv` created
- [ ] All CSV fields populated (no empty values)
- [ ] `summary_statistics.txt` generated
- [ ] Comparison tables generated
- [ ] No errors in log files

### Quality Checks

- [ ] Exact MIP solutions verified as optimal
- [ ] All algorithms satisfy budget constraint
- [ ] Objective values monotonic (Greedy ≤ LS ≤ MS-LS ≤ TS)
- [ ] Runtime increases with instance size
- [ ] Gap to best ≤ 30% for all algorithms
- [ ] Tabu Search achieves < 5% gap on most instances

---

## 📊 Results Analysis

### Key Metrics to Analyze

1. **Solution Quality**:
   - Objective value (covered demand)
   - Gap to best solution
   - Gap to optimal (small instances)

2. **Computational Efficiency**:
   - Runtime (seconds)
   - Quality per second ratio
   - Scalability with instance size

3. **Algorithm Robustness**:
   - Consistency across instances
   - Worst-case performance
   - Standard deviation (for stochastic methods)

4. **Trade-offs**:
   - Quality vs speed
   - Complexity vs performance
   - Deterministic vs stochastic

### Statistical Analysis

Compute for each algorithm:
- **Mean objective** across instances
- **Mean gap to best**
- **Mean runtime**
- **Standard deviation** (if multiple runs)
- **Best/worst case** performance

Compare algorithms:
- **Pairwise improvement**: TS vs MS-LS, MS-LS vs LS, etc.
- **Runtime ratio**: How much faster is Greedy vs TS?
- **Quality ratio**: How much better is TS vs Greedy?

### Visualization Recommendations

1. **Bar chart**: Objective values per instance
2. **Line chart**: Gap to best vs instance size
3. **Scatter plot**: Quality vs runtime
4. **Box plot**: Gap distribution across instances (per algorithm)
5. **Pareto frontier**: Quality vs runtime trade-off

---

## 🐛 Troubleshooting

### Issue: Mosel command not found

**Solution**: Ensure FICO Xpress is installed and `mosel` is in your PATH:
```bash
export PATH=$PATH:/path/to/xpress/bin
```

### Issue: Permission denied on scripts

**Solution**: Make scripts executable:
```bash
chmod +x scripts/run_experiments.sh
```

### Issue: Python import errors

**Solution**: Ensure Python 3.6+ is installed:
```bash
python3 --version
```

### Issue: Experiment takes too long

**Solution**: Run subset of experiments:
```bash
# Edit run_experiments.sh and comment out large instances or TS-2000
```

### Issue: Results CSV has missing values

**Solution**: Check log files in `results/raw/` for errors. Common issues:
- Algorithm failed to converge
- Timeout reached
- Parse error in log extraction

### Issue: Gaps are unexpectedly large

**Possible causes**:
- Algorithm parameters need tuning
- Bug in implementation
- Instance characteristics unusual

**Solution**:
1. Verify algorithm correctness on test_tiny
2. Review log files for warnings
3. Try different parameter settings

---

## 📝 Reporting Results

### Minimal Report Contents

1. **Instance characteristics table**
2. **Objective values table** (all algorithms, all instances)
3. **Runtime table** (all algorithms, all instances)
4. **Gap to best table**
5. **Summary statistics** (mean, std dev, min, max)
6. **Key findings** (3-5 bullet points)
7. **Recommendations** (which algorithm for which scenario)

### Extended Report Contents

Additionally include:
- Algorithm rankings
- Quality vs runtime trade-off analysis
- Scalability analysis
- Sensitivity analysis (parameter variations)
- Convergence plots (for iterative methods)
- Statistical significance tests

---

## 🎯 Recommendations Template

Based on experimental results, provide recommendations:

**For quick solutions (< 1 second)**:
- Use: Greedy heuristic
- Expected quality: 70-85% of optimal
- Use case: Initial feasibility check, warm start

**For good solutions (10-30 seconds)**:
- Use: Multi-Start Local Search
- Expected quality: 85-95% of optimal
- Use case: Production planning, daily optimization

**For best solutions (30-120 seconds)**:
- Use: Tabu Search (500-2000 iterations)
- Expected quality: 90-98% of optimal
- Use case: Strategic planning, critical applications

**For provably optimal solutions**:
- Use: Exact MIP
- Applicable: Small instances only (≤ 100 facilities)
- Runtime: Minutes to hours

---

## 📚 References

### Benchmark Instances

Instance generator: Cordeau, Furini & Ljubić (2016)
- Facilities: 50-200
- Customers: 200-1000
- Coverage: Euclidean distance-based

### Performance Metrics

- **Gap**: (Best_Obj - Alg_Obj) / Best_Obj × 100%
- **Speedup**: Runtime_Baseline / Runtime_Algorithm
- **Quality Ratio**: Alg_Obj / Best_Obj

### Statistical Tests

For comparing algorithms:
- Paired t-test (parametric)
- Wilcoxon signed-rank test (non-parametric)
- Friedman test (multiple algorithms)

---

## 🔄 Reproducibility

To ensure reproducibility:
1. Document all parameter settings
2. Use fixed random seeds (42)
3. Record software versions:
   - FICO Xpress version
   - Mosel compiler version
   - Operating system
   - Hardware specifications
4. Provide all instance files
5. Share complete result logs

---

## ✅ Phase 6 Completion Criteria

Phase 6 is complete when:
- [ ] All experiments executed successfully
- [ ] Results CSV generated and validated
- [ ] Comparison tables created
- [ ] Statistical analysis completed
- [ ] Key findings documented
- [ ] Recommendations provided
- [ ] All result files committed to repository

---

**Document Version**: 1.0
**Last Updated**: November 21, 2025
**Phase**: 6 - Experimental Validation
