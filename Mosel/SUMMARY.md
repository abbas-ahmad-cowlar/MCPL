# MCLP Optimization Project: Final Report

## 1. Executive Summary

We have successfully implemented and benchmarked a suite of algorithms for the Maximum Covering Location Problem (MCLP). The solution includes an Exact Solver (MIP) and five heuristic approaches. Testing across 9 datasets (ranging from 50 to 5000 customers) demonstrates that our **Local Search** and **Tabu Search** algorithms provide optimal or near-optimal solutions in seconds, significantly outperforming the Exact Solver on large-scale instances where the latter faces licensing and scalability limits.

## 2. Problem Statement

The goal was to select a set of facility locations to maximize the total demand covered within a specified radius, subject to a budget constraint. This is a classic NP-hard optimization problem.

## 3. Methodology

### Algorithms Implemented

1.  **Exact Solver**: Uses Xpress Optimizer. Provides guaranteed optimal solutions but is limited by problem size and license constraints.
2.  **Greedy Heuristic**: Fast constructive method. Good baseline but often sub-optimal.
3.  **Closest Neighbor**: Simple distance-based heuristic.
4.  **Local Search**: Improves upon Greedy by swapping facilities. Extremely fast and effective.
5.  **Multi-Start Local Search**: Runs Local Search from multiple random starting points.
6.  **Tabu Search**: Advanced metaheuristic to escape local optima.

### Datasets

We generated and tested on a diverse set of instances:

- **Small (S1, S2)**: 50 facilities, 200 customers.
- **Medium (M1, M2)**: 100 facilities, 500 customers.
- **Large (L1, L2)**: 200 facilities, 1000 customers.
- **Extra Large (XL1)**: 500 facilities, 2000 customers.
- **XXL (XXL1)**: 1000 facilities, 5000 customers.

## 4. Key Results

| Dataset  | Best Algorithm   | Objective      | Runtime | Notes                                       |
| :------- | :--------------- | :------------- | :------ | :------------------------------------------ |
| **S1**   | Exact / Tabu     | 7,646.00       | < 0.2s  | All algorithms found optimal solution.      |
| **M2**   | **Tabu Search**  | **22,497.00**  | 0.21s   | Outperformed Exact solver (0.8% MIP gap).   |
| **L1**   | **Local Search** | **47,783.00**  | 0.01s   | Outperformed Exact solver (0.9% MIP gap).   |
| **XL1**  | **Tabu Search**  | **96,479.00**  | 0.59s   | Best known solution (387 units > Exact).    |
| **XXL1** | **Local Search** | **250,788.00** | 0.10s   | **Best known**. Exact solver failed (license limit). |

## 5. Analysis & Recommendations

### Scalability

- **Exact Solver**: Excellent for small instances (S1, S2), achieving optimality within 0.01-0.04 seconds. For medium instances, the solver often terminates with small MIP gaps (0.5-1.0%). For very large instances (XXL1), the community license limitation prevents execution (>5000 rows).
- **Local Search**: The most efficient algorithm for large-scale problems. It solved the massive XXL1 instance (5000 customers) to the best known solution in **0.10 seconds**, demonstrating exceptional scalability.
- **Tabu Search**: Highly robust across medium-to-large instances. Found the best solutions for XL1 and M2, demonstrating superior solution quality compared to the Exact solver. However, implementation limitations prevent execution on XXL1 (index out of range error).

### Recommendation

For deployment, we recommend a **hybrid approach**:

1.  Run **Local Search** first (0.01-0.10 seconds, consistently high quality across all instance sizes).
2.  Run **Tabu Search** (0.2-0.6 seconds for instances up to XL) to potentially improve the solution further, particularly for medium-to-large instances.
3.  Use **Exact Solver** only for small instances (< 200 facilities) when optimality guarantees are required, or when the license permits and MIP gap tolerance is acceptable.

## 6. Deliverables

- Full source code in Mosel (`src/`).
- Data generation and conversion scripts (`scripts/`).
- Benchmark scripts (`run_benchmark.ps1`).
- Detailed results (`benchmark_results.md`).
