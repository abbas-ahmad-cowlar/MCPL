# MCLP Optimization Suite

## 📋 Overview

This project provides a high-performance implementation of the **Maximum Covering Location Problem (MCLP)** using **FICO Xpress Mosel**. It is designed to solve large-scale facility location problems efficiently, featuring a suite of exact solvers, heuristics, and metaheuristics.

The suite is capable of handling instances ranging from small (50 facilities) to massive (1000 facilities, 5000 customers), providing optimal or near-optimal solutions in seconds.

## 📂 Project Structure

The project is organized as follows:

```text
MCLP_Optimization_Suite/
├── src/                        # Mosel Source Code
│   ├── mclp_exact.mos          # Exact MIP solver (Xpress Optimizer)
│   ├── mclp_greedy.mos         # Greedy heuristic
│   ├── mclp_closest_neighbor.mos # Closest Neighbor heuristic
│   ├── mclp_local_search.mos   # Local Search improvement heuristic
│   ├── mclp_multistart.mos     # Multi-Start Local Search
│   └── mclp_tabu_search.mos    # Tabu Search Metaheuristic
├── data/                       # Benchmark Datasets (.dat)
│   ├── S1.dat, S2.dat          # Small (50 facilities, 200 customers)
│   ├── M1.dat, M2.dat          # Medium (100 facilities, 500 customers)
│   ├── L1.dat, L2.dat          # Large (200 facilities, 1000 customers)
│   ├── XL1.dat                 # Extra Large (500 facilities, 2000 customers)
│   └── XXL1.dat                # Massive (1000 facilities, 5000 customers)
├── scripts/                    # Utility Scripts
│   ├── generate_instance.py    # Generate new random instances
│   └── convert_json_to_mosel.py # Convert JSON data to Mosel format
├── pseudocode/                 # Algorithm Documentation
│   ├── greedy_pseudocode.txt
│   ├── closest_neighbor_pseudocode.txt
│   ├── local_search_pseudocode.txt
│   └── tabu_search_pseudocode.txt
├── results/                    # Benchmark Output Logs
├── REPORT.md                   # Executive Summary
├── client_report.tex           # 📄 FINAL REPORT (LaTeX Source)
├── REPORT_DELIVERY.md          # 📖 Delivery Guide
├── run_benchmark.ps1           # Main Execution Script
└── summarize_results.ps1       # Result Analysis Script
```

## 🚀 Quick Start

### Prerequisites

1.  **FICO Xpress Mosel** (Version 5.0+).
2.  **Python 3.8+** (for data generation scripts).
3.  **PowerShell** (for execution scripts).

### Running the Full Benchmark

To execute the complete benchmark suite across all algorithms and datasets:

```powershell
.\run_benchmark.ps1
```

This script will:

1.  Execute all 6 algorithms on all 9 datasets (S1 through XXL1).
2.  Apply a 600-second time limit for the Exact solver on large instances.
3.  Save detailed logs to the `results/` directory.

### Analyzing Results

To generate a summary table of the benchmark performance:

```powershell
.\summarize_results.ps1
```

## 🔬 Algorithms Implemented

| Algorithm            | Type          | Description                                 | Best For                     |
| :------------------- | :------------ | :------------------------------------------ | :--------------------------- |
| **Exact Solver**     | MIP           | Mathematical optimal solution using Xpress. | Small/Medium instances.      |
| **Greedy**           | Heuristic     | Fast constructive method.                   | Baseline comparison.         |
| **Closest Neighbor** | Heuristic     | Simple distance-based assignment.           | Very fast baseline.          |
| **Local Search**     | Heuristic     | Hill-climbing improvement.                  | **Massive instances (XXL)**. |
| **Multi-Start**      | Metaheuristic | Repeated Local Search from random points.   | Robustness.                  |
| **Tabu Search**      | Metaheuristic | Advanced search with memory.                | **Large instances (XL)**.    |

## 📚 Documentation

- **[Executive Summary](REPORT.md)**: High-level analysis and key findings.
- **[Final Report](client_report.tex)**: Comprehensive academic-style report (LaTeX).
- **[Delivery Guide](REPORT_DELIVERY.md)**: Instructions for compiling and using this package.
- **[Pseudocode](pseudocode/)**: Detailed logic for each heuristic.

---

_MCLP Optimization Suite_
