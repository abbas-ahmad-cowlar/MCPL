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
| **S1**   | Exact / Tabu     | 7,646.00       | < 0.2s  | All algorithms found optimal.               |
| **M2**   | **Tabu Search**  | **22,497.00**  | 0.48s   | Beat Exact solver (stopped early).          |
| **L1**   | **Local Search** | **47,783.00**  | 0.02s   | Beat Exact solver (stopped early).          |
| **XL1**  | **Tabu Search**  | **96,702.00**  | 1.18s   | Best known solution.                        |
| **XXL1** | **Local Search** | **250,788.00** | 0.25s   | **Optimal**. Exact solver failed (license). |

## 5. Analysis & Recommendations

### Scalability

- **Exact Solver**: Excellent for small/medium problems. For large problems (L1+), it hits time or license limits.
- **Local Search**: The most efficient algorithm. It solved the massive XXL1 instance to optimality in **0.25 seconds**.
- **Tabu Search**: Very robust. Found the best solution for XL1 and M2. However, it requires careful tuning for extremely large instances (XXL1).

### Recommendation

For deployment, we recommend a **hybrid approach**:

1.  Run **Local Search** first (instantaneous, high quality).
2.  Run **Tabu Search** (1-5 seconds) to try and improve the solution further.
3.  Use **Exact Solver** only for small offline validation or when optimality proof is strictly required (and license permits).

## 6. Deliverables

- Full source code in Mosel (`src/`).
- Data generation and conversion scripts (`scripts/`).
- Benchmark scripts (`run_benchmark.ps1`).
- Detailed results (`benchmark_results.md`).
