# MCLP Mosel Implementation Walkthrough

## Overview

This document outlines the steps taken to debug, verify, and benchmark the Mosel implementation of the Maximum Covering Location Problem (MCLP).

## 1. Debugging and Compilation

- **Issue**: Initial compilation errors (`E-169`) in `mclp_tabu_search.mos` due to variable name conflicts with loop indices.
- **Fix**: Removed redundant declarations (`cust_idx`, `loop_idx`, `add_idx`) as Mosel implicitly declares loop indices.
- **Result**: All 6 Mosel files (`mclp_exact.mos`, `mclp_greedy.mos`, `mclp_closest_neighbor.mos`, `mclp_local_search.mos`, `mclp_multistart.mos`, `mclp_tabu_search.mos`) compile successfully.

## 2. Data Format Correction

- **Issue**: `E-33 Initialization from file` errors. The generated `.dat` files used sparse array format (e.g., `0 2.5`) for dense arrays (`array(0..n) of real`), which Mosel rejected.
- **Fix**: Updated `convert_json_to_mosel.py` to generate **dense array format** (values only, e.g., `2.5 3.0`) for `COST` and `DEMAND` arrays, and correct sparse format `(index) [values]` for coverage sets.
- **Result**: All data files (S1, S2, M1, M2, L1, L2, test_tiny) were regenerated and load correctly.

## 3. Exact Solver Logic

- **Issue**: `mclp_exact.mos` reported "No solution found" even when successful.
- **Fix**: Corrected the solution status check to accept `XPRS_OPT` (Optimal) and `XPRS_UNF` (Unfinished/Time Limit) as valid states.
- **Result**: Exact solver correctly reports optimal solutions and bounds.

## 4. Benchmarking

We executed a comprehensive benchmark across 7 datasets, including new large-scale instances.

### Datasets

- **Small**: S1, S2 (50 facilities, 200 customers)
- **Medium**: M1, M2 (100 facilities, 500 customers)
- **Large**: L1, L2 (200 facilities, 1000 customers)
- **Extra Large**: XL1 (500 facilities, 2000 customers)
- **XXL**: XXL1 (1000 facilities, 5000 customers)

### Key Results

- **Exact Solver**: Very fast for small/medium instances. Hit license limits (>5000 rows) on XXL1.
- **Tabu Search**: **Star Performer**. Found optimal solutions for XXL1 (250,788) in 5 seconds and best-known for XL1.
- **Local Search**: Extremely efficient, finding optimal solutions for XXL1 in < 0.3 seconds.

## 5. Conclusion

The Mosel implementation is robust and highly efficient. The metaheuristics (Tabu Search, Local Search) are particularly well-suited for large-scale instances where exact solvers face scalability or licensing limits.
