# MCLP Mosel Implementation

This directory contains the complete FICO Xpress Mosel implementation of the Maximum Covering Location Problem (MCLP), migrated from Python as specified in the client requirements.

## 📋 Overview

This implementation follows the mathematical formulation from **Cordeau, Furini & Ljubić (2016)** and includes:

1. **Exact Mathematical Model** - Compact formulation with MIP solver
2. **Two Heuristics** - Greedy and Closest Neighbor
3. **Multi-Start Local Search** - 1-flip and swap neighborhoods
4. **Metaheuristic** - Tabu Search with intensification/diversification
5. **Comprehensive Pseudocode** - Detailed algorithm documentation
6. **Experimental Results** - Validation on 7 benchmark instances

## 📂 Directory Structure

```
Mosel/
├── README.md                    # This file
├── docs/
│   ├── SETUP.md                 # Installation and environment setup
│   ├── DATA_FORMAT.md           # Data format specification
│   └── PHASE1_COMPLETION.md     # Phase 1 completion report
├── data/                        # Mosel .dat instance files
│   ├── test_tiny.dat            # Tiny test (4 facilities, 8 customers)
│   ├── S1.dat, S2.dat           # Small instances (50 facilities, 200 customers)
│   ├── M1.dat, M2.dat           # Medium instances (100 facilities, 500 customers)
│   └── L1.dat, L2.dat           # Large instances (200 facilities, 1000 customers)
├── src/                         # Mosel source code (.mos files)
│   ├── mclp_exact.mos           # [Phase 2] Exact MIP model
│   ├── mclp_greedy.mos          # [Phase 3] Greedy heuristic
│   ├── mclp_closest_neighbor.mos # [Phase 3] Closest neighbor heuristic
│   ├── mclp_local_search.mos    # [Phase 4] Local search core
│   ├── mclp_multistart.mos      # [Phase 4] Multi-start wrapper
│   └── mclp_tabu_search.mos     # [Phase 5] Tabu search metaheuristic
├── pseudocode/                  # Algorithm pseudocode documentation
│   ├── greedy_pseudocode.txt
│   ├── closest_neighbor_pseudocode.txt
│   ├── local_search_pseudocode.txt
│   └── tabu_search_pseudocode.txt
├── results/                     # Experimental results
│   ├── experimental_results.csv
│   └── comparison_tables.md
└── utilities/                   # Helper scripts
    └── convert_json_to_mosel.py # JSON to .dat converter
```

## 🚀 Quick Start

### Prerequisites

- **FICO Xpress Mosel** compiler (version 5.0+)
- **FICO Xpress Optimizer** (valid license)
- **Python 3.8+** (for data conversion utilities)

### Installation

See [docs/SETUP.md](docs/SETUP.md) for detailed installation instructions.

### Running the Conversion Utility

Convert JSON instances to Mosel format:

```bash
# Convert all instances
python utilities/convert_json_to_mosel.py --input-dir ../data/ --output-dir data/

# Convert single instance
python utilities/convert_json_to_mosel.py --input ../data/S1.json --output data/
```

## 📊 Instance Characteristics

| Instance    | Facilities | Customers | Budget | Coverage Density |
|-------------|-----------|-----------|--------|------------------|
| test_tiny   | 4         | 8         | 5.00   | 46.88%          |
| S1          | 50        | 200       | 10.00  | 13.07%          |
| S2          | 50        | 200       | 10.00  | 13.31%          |
| M1          | 100       | 500       | 15.00  | 11.78%          |
| M2          | 100       | 500       | 20.00  | 11.63%          |
| L1          | 200       | 1000      | 20.00  | 8.72%           |
| L2          | 200       | 1000      | 30.00  | 7.40%           |

## 📖 Documentation

- **[SETUP.md](docs/SETUP.md)** - Environment setup and installation guide
- **[DATA_FORMAT.md](docs/DATA_FORMAT.md)** - Mosel data format specification
- **[EXACT_MODEL_USAGE.md](docs/EXACT_MODEL_USAGE.md)** - Exact model usage guide
- **[HEURISTICS_USAGE.md](docs/HEURISTICS_USAGE.md)** - Heuristics usage guide
- **[PHASE1_COMPLETION.md](docs/PHASE1_COMPLETION.md)** - Phase 1 completion report
- **[PHASE2_COMPLETION.md](docs/PHASE2_COMPLETION.md)** - Phase 2 completion report
- **[PHASE3_COMPLETION.md](docs/PHASE3_COMPLETION.md)** - Phase 3 completion report

## 🔬 Mathematical Model

The MCLP selects facilities to maximize covered demand within a budget constraint:

**Decision Variables:**
- `y[i]` = 1 if facility i is opened, 0 otherwise
- `z[j]` = 1 if customer j is covered, 0 otherwise (can be relaxed to [0,1])

**Formulation:**
```
Maximize   Σ(j∈J) d[j] * z[j]

Subject to:
  Σ(i∈I_j) y[i] ≥ z[j]        ∀ j ∈ J    (coverage constraints)
  Σ(i∈I) f[i] * y[i] ≤ B                 (budget constraint)
  y[i] ∈ {0,1}                 ∀ i ∈ I
  z[j] ∈ [0,1]                 ∀ j ∈ J
```

## 📈 Implementation Status

### ✅ Phase 1: Foundation & Data Infrastructure (COMPLETED)
- [x] Mosel environment setup documentation
- [x] Data conversion utility (JSON → .dat)
- [x] All 7 instances converted and validated
- [x] Data format specification documented

### ✅ Phase 2: Exact Mathematical Model (COMPLETED)
- [x] Compact MIP formulation implementation
- [x] Data input routines and validation
- [x] Solution extraction and output
- [x] Comprehensive usage documentation

### ✅ Phase 3: Heuristic Implementations (COMPLETED)
- [x] Greedy heuristic implementation
- [x] Closest Neighbor heuristic implementation
- [x] Pseudocode documentation (both algorithms)
- [x] Comprehensive usage guide

### 🚧 Phase 4: Multi-Start Local Search (PENDING)
- [ ] Local search with delta-evaluation
- [ ] Multi-start wrapper with diverse initialization
- [ ] Pseudocode documentation

### 🚧 Phase 5: Metaheuristic - Tabu Search (PENDING)
- [ ] Tabu list management
- [ ] Intensification/diversification strategies
- [ ] Pseudocode documentation

### 🚧 Phase 6: Experimental Validation (PENDING)
- [ ] Run all algorithms on all instances
- [ ] Statistical analysis
- [ ] Comparison tables

### 🚧 Phase 7: Final Documentation (PENDING)
- [ ] Complete implementation report
- [ ] User guide
- [ ] Experimental results discussion

## 📚 References

**Cordeau, J.-F., Furini, F., & Ljubić, I. (2016)**
*Benders decomposition for very large scale partial set covering and maximal covering location problems.*
Computers & Operations Research, 66, 143–153.
https://doi.org/10.1016/j.cor.2015.08.010

## 👤 Authors

MCLP Migration Team
Migration Date: November 2025

## 📄 License

This implementation is part of the MCPL project repository.

---

**Next Steps:** Proceed to Phase 2 (Exact Model Implementation) - see migration plan for details.
