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
│   ├── generate_visualizations.py  # Generate figures and performance tables
│   └── convert_json_to_mosel.py # Convert JSON data to Mosel format
├── pseudocode/                 # Algorithm Documentation
│   ├── greedy_pseudocode.txt
│   ├── closest_neighbor_pseudocode.txt
│   ├── local_search_pseudocode.txt
│   └── tabu_search_pseudocode.txt
├── results_complete/           # Latest Benchmark Output Logs
├── figures/                    # Generated Figures and Tables
│   ├── runtime_vs_size.pdf
│   ├── solution_quality_vs_size.pdf
│   ├── runtime_comparison.pdf
│   └── performance_table.tex
├── SCIENTIFIC_REPORT.tex       # 📄 COMPREHENSIVE REPORT (LaTeX Source)
├── run_complete_workflow.ps1   # 🚀 COMPLETE WORKFLOW (Recommended - runs everything)
├── run_benchmark.ps1           # Benchmark Execution Script (standalone)
├── scripts/
│   ├── generate_visualizations.py  # Result Analysis & Visualization Script
│   └── update_report_tables.py    # Auto-updates report with latest results
└── archive/                    # Archived deprecated files (see archive/README.md)
```

## 🚀 Quick Start

### Prerequisites

1.  **FICO Xpress Mosel** (Version 5.0+).
2.  **Python 3.8+** (for data generation scripts).
3.  **PowerShell** (for execution scripts).

### Complete Workflow (Recommended)

To run benchmarks, generate visualizations, update the report, and compile PDF:

```powershell
.\run_complete_workflow.ps1 -CompileReport
```

This single command will:
1. Run all benchmarks (all 6 algorithms on all 9 datasets)
2. Generate all figures and performance tables
3. Automatically update `SCIENTIFIC_REPORT.tex` with latest results
4. Compile the PDF report (if LaTeX is installed)

**Without PDF compilation:**
```powershell
.\run_complete_workflow.ps1
```

See `WORKFLOW_SUMMARY.md` for detailed documentation.

### Running Benchmarks Only

To run only the benchmarks (without visualization/report updates):

```powershell
.\run_benchmark.ps1
```

This saves results to `results_complete/` directory.

### Generating Visualizations Only

To generate figures and tables from existing results:

```powershell
python scripts/generate_visualizations.py
```

This creates figures in `figures/` directory.

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
- **[Final Report](REPORT.tex)**: Comprehensive academic-style report (LaTeX).
- **[Pseudocode](pseudocode/)**: Detailed logic for each heuristic.

---

_MCLP Optimization Suite_
