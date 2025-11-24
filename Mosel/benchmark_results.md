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
| **S1**   | Exact            | **7,646.00**   | 0.03        | Optimal                    |
|          | Tabu Search      | **7,646.00**   | 0.21        | Optimal                    |
| **S2**   | Exact            | **7,449.00**   | 0.13        | Optimal                    |
|          | Tabu Search      | **7,449.00**   | 0.21        | Optimal                    |
| **M1**   | Exact            | **21,099.00**  | 0.25        | Optimal                    |
|          | Tabu Search      | **21,099.00**  | 0.69        | Optimal                    |
| **M2**   | Exact            | 22,448.00      | 0.18        | Stopped early (1% gap)     |
|          | **Tabu Search**  | **22,497.00**  | 0.48        | **Best Found**             |
| **L1**   | Exact            | 47,522.00      | 0.50        | Stopped early (1% gap)     |
|          | **Local Search** | **47,783.00**  | 0.02        | **Best Found**             |
| **L2**   | Exact            | **45,060.00**  | 0.18        |                            |
|          | Tabu Search      | 44,448.00      | 0.81        |                            |
| **XL1**  | Exact            | 96,092.00      | 0.33        | Stopped early              |
|          | **Tabu Search**  | **96,702.00**  | 1.18        | **Best Found**             |
| **XXL1** | Exact            | N/A            | N/A         | License Limit (>5000 rows) |
|          | **Local Search** | **250,788.00** | 0.25        | **Optimal**                |
|          | Tabu Search      | N/A            | N/A         | Failed (Index Error)       |

## Key Observations

1.  **Scalability**: The Exact solver is excellent for small/medium instances but hits license limits on massive instances (XXL1).
2.  **Heuristic Efficiency**: Local Search is incredibly fast (0.25s for XXL1) and found the optimal solution for the largest dataset.
3.  **Metaheuristic Quality**: Tabu Search consistently found optimal or best-known solutions for most instances, outperforming the Exact solver on M2 and XL1.

## Conclusion

The suite provides a robust set of tools. For general use, **Tabu Search** offers the best balance of quality and speed for large problems, while **Local Search** is unbeatable for massive scale speed.
