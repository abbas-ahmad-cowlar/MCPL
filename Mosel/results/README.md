# Experimental Results Directory

This directory contains experimental validation results for all MCLP algorithms.

## 📁 Directory Structure

```
results/
├── README.md                      # This file
├── experimental_results.csv       # Raw results (all algorithms, all instances)
├── comparison_tables.md           # Formatted comparison tables
├── statistical_analysis.md        # Statistical analysis and insights
├── summary_statistics.txt         # Summary statistics
└── raw/                           # Individual algorithm run logs
    ├── exact_test_tiny.log
    ├── exact_S1.log
    ├── greedy_*.log
    ├── closest_neighbor_*.log
    ├── local_search_*.log
    ├── multistart_*.log
    ├── tabu_500_*.log
    └── tabu_2000_*.log
```

## 🚀 Generating Results

### Step 1: Run Experiments

```bash
cd ..  # Go to Mosel/ directory
bash scripts/run_experiments.sh
```

This will:
- Execute all algorithms on all instances
- Generate log files in `raw/`
- Create `experimental_results.csv`
- Calculate gaps to best solution

**Expected runtime**: 30-60 minutes

### Step 2: Generate Analysis

```bash
python3 scripts/generate_tables.py
```

This will:
- Create comparison tables
- Generate statistical analysis
- Produce rankings and recommendations

## 📊 Results Format

### experimental_results.csv

Columns:
- `Instance`: Instance name (e.g., S1, M1, L1)
- `Algorithm`: Algorithm name
- `Objective`: Covered demand (objective value)
- `Runtime_sec`: Execution time in seconds
- `Facilities_Opened`: Number of facilities opened
- `Budget_Used`: Total budget consumed
- `Coverage_Pct`: Percentage of customers covered
- `Gap_to_Best_Pct`: Gap to best solution (%)
- `Notes`: Additional information

### comparison_tables.md

Contains:
- Table 1: Objective values
- Table 2: Runtime (seconds)
- Table 3: Gap to best (%)
- Summary statistics
- Quality vs time trade-off
- Best algorithm per instance
- Algorithm rankings

### statistical_analysis.md

Contains:
- Key findings
- Algorithm performance summary
- Recommendations by use case
- Trade-off analysis

## 📈 Expected Results

### Solution Quality

| Algorithm | Expected Gap to Best |
|-----------|---------------------|
| Greedy | 15-30% |
| Closest Neighbor | 20-35% |
| Local Search | 8-20% |
| Multi-Start LS | 5-15% |
| Tabu Search (500) | 2-10% |
| Tabu Search (2000) | 1-8% |

### Runtime

| Algorithm | Small (S) | Medium (M) | Large (L) |
|-----------|-----------|------------|-----------|
| Greedy | < 0.5s | < 1s | < 2s |
| Local Search | < 1s | < 5s | < 15s |
| Multi-Start LS | < 10s | < 30s | < 100s |
| Tabu Search (500) | ~5s | ~20s | ~60s |

## 🔍 Validation

### Quality Checks

Run validation script:
```bash
python3 ../scripts/validate_results.py
```

Checks:
- All CSV fields populated
- Objective values reasonable
- Budget constraints satisfied
- Runtime values positive
- Gaps within expected range

### Consistency Checks

- Exact MIP solutions should be best (small instances)
- Tabu Search should dominate other heuristics
- Multi-Start should beat single Local Search
- Runtime should increase with instance size

## 📝 Citing Results

If using these results in publications:

```bibtex
@misc{mclp_mosel_2025,
  title={MCLP Mosel Implementation - Experimental Results},
  author={MCLP Migration Team},
  year={2025},
  note={Migration from Python to FICO Xpress Mosel}
}
```

## 🔄 Reproducibility

To reproduce results:
1. Use provided instances in `../data/`
2. Use algorithm implementations in `../src/`
3. Run with fixed random seeds (seed=42)
4. Use same parameter settings (documented in scripts)
5. Record software versions

## 📧 Issues

If results are inconsistent or unexpected:
1. Check log files in `raw/` for errors
2. Verify instance data files
3. Ensure correct Mosel version
4. Review algorithm parameters
5. Contact: [Provide contact information]

---

**Directory Status**: Template (run experiments to populate)
**Last Updated**: November 21, 2025
**Phase**: 6 - Experimental Validation
