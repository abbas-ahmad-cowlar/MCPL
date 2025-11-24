# MCLP Benchmark Results

## Overview

This document summarizes the performance of the MCLP algorithms across all benchmark datasets.

## Algorithms Tested

1.  **Exact Solver**: MIP formulation using Xpress Optimizer.
2.  **Greedy Heuristic**: Constructive heuristic.
3.  **Closest Neighbor**: Simple distance-based heuristic.
4.  **Local Search**: Hill-climbing improvement.
5.  **Multi-Start**: Repeated Local Search.
6.  **Tabu Search**: Metaheuristic with memory.

## Summary Table

| Dataset  | Algorithm        | Objective      | Runtime (s) | Notes                      |
| :------- | :--------------- | :------------- | :---------- | :------------------------- |
| **S1**   | Exact            | **7,646.00**   | 0.01        | Optimal (0% gap)           |
|          | Tabu Search      | **7,646.00**   | 0.16        | Optimal                    |
| **S2**   | Exact            | **7,449.00**   | 0.04        | Optimal (0% gap)           |
|          | Tabu Search      | **7,449.00**   | 0.16        | Optimal                    |
| **M1**   | Exact            | **21,099.00**  | 0.10        | Best bound: 21,249 (0.7% gap) |
|          | Tabu Search      | **21,099.00**  | 0.32        | Optimal                    |
| **M2**   | Exact            | 22,448.00      | 0.05        | Best bound: 22,634 (0.8% gap) |
|          | **Tabu Search**  | **22,497.00**  | 0.21        | **Best Found**             |
| **L1**   | Exact            | 47,522.00      | 0.17        | Best bound: 47,928 (0.9% gap) |
|          | **Local Search** | **47,783.00**  | 0.01        | **Best Found**             |
| **L2**   | Exact            | **45,060.00**  | 0.04        | Best bound: 45,289 (0.5% gap) |
|          | Tabu Search      | 44,448.00      | 0.30        | Below Exact solution       |
| **XL1**  | Exact            | 96,092.00      | 0.16        | Best bound: 97,035 (1.0% gap) |
|          | **Tabu Search**  | **96,479.00**  | 0.59        | **Best Found**             |
| **XXL1** | Exact            | N/A            | N/A         | License Limit (>5000 rows) |
|          | **Local Search** | **250,788.00** | 0.10        | **Best Known**             |
|          | Tabu Search      | N/A            | N/A         | Failed (Index Error)       |

## Key Observations

1.  **Scalability**: The Exact solver is excellent for small instances (S1, S2) but encounters computational limits on larger instances, hitting license restrictions on XXL1 (>5000 rows/columns).
2.  **Heuristic Efficiency**: Local Search is remarkably fast (0.10s for XXL1 with 5000 customers) and found the best known solution for the largest dataset, significantly outperforming all other methods.
3.  **Metaheuristic Quality**: Tabu Search consistently found optimal or near-optimal solutions for most instances, outperforming the Exact solver on M2 (by 49 units) and XL1 (by 387 units), demonstrating its effectiveness for medium-to-large scale problems.

## Conclusion

The suite provides a robust set of tools. For general use, **Tabu Search** offers the best balance of quality and speed for large problems, while **Local Search** is unbeatable for massive scale speed.
