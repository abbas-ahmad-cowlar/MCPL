# MCLP Optimization Suite

## Overview

This package contains the complete implementation of the Maximum Covering Location Problem (MCLP) optimization suite using FICO Xpress Mosel. It includes exact solvers, heuristics, metaheuristics, and a comprehensive benchmarking framework.

## 📂 Package Structure

| Directory/File          | Description                                                       |
| :---------------------- | :---------------------------------------------------------------- |
| `src/`                  | **Source Code**: Mosel implementation of all 6 algorithms.        |
| `data/`                 | **Datasets**: 9 benchmark instances (S1-XXL1).                    |
| `scripts/`              | **Tools**: Python scripts for data generation and conversion.     |
| `results/`              | **Benchmark Results**: Output logs from the full benchmark run.   |
| `REPORT.md`             | **Client Report**: Executive summary and analysis.                |
| `BENCHMARK_RESULTS.md`  | **Detailed Results**: Performance tables and metrics.             |
| `TECHNICAL_GUIDE.md`    | **Technical Manual**: Setup, usage, and implementation details.   |
| `run_benchmark.ps1`     | **Execution Script**: One-click script to run the full benchmark. |
| `summarize_results.ps1` | **Analysis Script**: Tool to parse and summarize results.         |

## 🚀 Quick Start

### Prerequisites

1.  **FICO Xpress Mosel** (Community Edition or Licensed).
2.  **Python 3.8+** (for scripts).

### Running the Benchmark

To execute the full benchmark suite (all algorithms on all datasets):

```powershell
.\run_benchmark.ps1
```

This will:

1.  Run all 6 algorithms on datasets `test_tiny` through `XXL1`.
2.  Save output logs to `results/`.

### Viewing Results

To generate a summary table of the results:

```powershell
.\summarize_results.ps1
```

## 📖 Documentation

- **[Client Report](REPORT.md)**: High-level overview and recommendations.
- **[Technical Guide](TECHNICAL_GUIDE.md)**: Detailed instructions for developers.
- **[Benchmark Results](BENCHMARK_RESULTS.md)**: Full performance data.

---

_Produced by Syed Abbas Ahmad_
