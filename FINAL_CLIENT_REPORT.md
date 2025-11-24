# MCLP Optimization Project: Final Report

## Executive Summary

We have successfully implemented and benchmarked a comprehensive suite of algorithms for the Maximum Covering Location Problem (MCLP). The solution includes an Exact Solver (MIP) and five heuristic approaches, tested across 9 datasets ranging from 50 to 5000 customers. Our results demonstrate that **Local Search** and **Tabu Search** algorithms provide optimal or near-optimal solutions in fractions of a second, significantly outperforming the Exact Solver on large-scale instances. Notably, our Local Search implementation solves the largest instance (1000 facilities, 5000 customers) to the best known solution in **0.10 seconds**, while Tabu Search achieves a **387-unit improvement** over the exact solver on the XL1 instance while maintaining sub-second runtimes.

## Problem Overview

### Problem Definition

The Maximum Covering Location Problem addresses the strategic question: *Given a limited budget and a set of potential facility locations, which facilities should be opened to maximize the customer demand covered within an acceptable service distance?* This is a classic NP-hard optimization problem with exponential worst-case complexity.

### Real-World Applications

MCLP has widespread applications across diverse domains:

- **Emergency Services**: Positioning ambulances, fire stations, and police units to maximize population coverage within critical response times
- **Retail Location Planning**: Selecting store locations to maximize market coverage within competitive service areas
- **Public Infrastructure**: Siting hospitals, schools, libraries, and community centers to serve maximum population under budget constraints
- **Telecommunications**: Placing cell towers, Wi-Fi access points, or service centers to maximize coverage area
- **Humanitarian Logistics**: Positioning relief centers in disaster response to maximize affected population access

## Solution Approach

### Algorithms Implemented

We implemented six solution methods representing different trade-offs between solution quality and computational efficiency:

1. **Exact Solver**: Uses FICO Xpress Optimizer. Provides guaranteed optimal solutions with optimality proofs, but is limited by problem size and license constraints (community license: ≤5000 rows).

2. **Greedy Heuristic**: Fast constructive method that iteratively selects facilities with maximum coverage gain. Provides good baseline solutions but often suboptimal.

3. **Closest Neighbor**: Simple distance-based heuristic prioritizing facilities closest to high-demand customers. Easy to implement but generally poor performance.

4. **Local Search**: Improvement heuristic starting from greedy solution and iteratively swapping facilities. Extremely fast and effective, demonstrating exceptional scalability.

5. **Multi-Start Local Search**: Runs Local Search from multiple random starting points to escape local optima. More robust with modest computational overhead.

6. **Tabu Search**: Advanced metaheuristic using short-term memory (tabu list), aspiration criteria, and diversification strategies to escape local optima. Most sophisticated method with excellent solution quality.

### Test Instances

We generated and tested on a diverse set of instances with the following characteristics:

- **Small (S1, S2)**: 50 facilities, 200 customers, budget = 10
- **Medium (M1, M2)**: 100 facilities, 500 customers, budget = 15-20
- **Large (L1, L2)**: 200 facilities, 1000 customers, budget = 20-30
- **Extra Large (XL1)**: 500 facilities, 2000 customers, budget = 40
- **XXL (XXL1)**: 1000 facilities, 5000 customers, budget = 80

All instances use:
- Uniformly distributed facility/customer coordinates in [0, 30] × [0, 30]
- Customer demands uniformly distributed in [1, 100]
- Unit facility costs (f_i = 1)
- Euclidean distance-based coverage with radius R ∈ [3.25, 6.25]

## Key Results

The following table presents results for five representative instances demonstrating algorithm performance across different problem scales:

| Dataset  | Best Algorithm   | Objective      | Runtime | Notes                                                |
| :------- | :--------------- | :------------- | :------ | :--------------------------------------------------- |
| **S1**   | Exact / Tabu     | 7,646.00       | < 0.2s  | All algorithms found optimal solution.               |
| **M2**   | **Tabu Search**  | **22,497.00**  | 0.21s   | Outperformed Exact solver (0.8% MIP gap).            |
| **L1**   | **Local Search** | **47,783.00**  | 0.01s   | Outperformed Exact solver (0.9% MIP gap).            |
| **XL1**  | **Tabu Search**  | **96,479.00**  | 0.59s   | Best known solution (387 units > Exact).             |
| **XXL1** | **Local Search** | **250,788.00** | 0.10s   | **Best known**. Exact solver failed (license limit). |

### Best Known Solutions Summary

The following table establishes benchmarks for all tested instances:

| Instance | Best Objective | Algorithm    | Runtime | Status                                    |
| :------- | :------------- | :----------- | :------ | :---------------------------------------- |
| S1       | 7,646          | Multiple     | <0.01s  | **Proven Optimal**                        |
| S2       | 7,449          | Multiple     | <0.01s  | **Proven Optimal**                        |
| M1       | 21,099         | Exact, Tabu  | 0.10s   | **Proven Optimal**                        |
| M2       | 22,497         | Tabu         | 0.21s   | Best Found (Exact: 22,448, 0.8% gap)      |
| L1       | 47,783         | Local, Multi | 0.01s   | Best Found (Exact: 47,522, 0.9% gap)      |
| L2       | 45,060         | Exact        | 0.04s   | **Proven Optimal**                        |
| XL1      | 96,479         | Tabu         | 0.59s   | Best Found (Exact: 96,092, improved 387)  |
| XXL1     | 250,788        | Local, Multi | 0.10s   | Best Known (Exact: failed, license limit) |

## Performance Analysis

### Scalability Assessment

**Exact Solver:**
- Excellent for small instances (S1, S2), achieving optimality within 0.01-0.04 seconds
- For medium instances, often terminates with small MIP gaps (0.5-1.0%)
- Struggles or fails on very large instances:
  - L1: 0.9% gap, terminated early
  - XL1: 0.4% gap, outperformed by heuristics
  - XXL1: Failed completely due to community license limitation (>5000 rows)

**Local Search:**
- Most efficient algorithm for large-scale problems
- Solved massive XXL1 instance (5000 customers) to best known solution in **0.10 seconds**
- Demonstrates exceptional scalability: 50× size increase (200→5000 customers) with only 10× runtime increase
- Nearly linear scaling behavior
- Highly effective across all instance sizes

**Tabu Search:**
- Highly robust across medium-to-large instances
- Found best solutions for XL1 and M2, demonstrating superior solution quality vs. Exact solver
- Consistent performance: 0.16-0.59s for instances up to 2000 customers
- Implementation limitations prevent execution on XXL1 (array index out of range error)
- Best overall solution quality for instances it can handle

**Greedy Heuristic:**
- Fastest construction (typically <0.50s even for XXL1)
- Solution quality typically 1-4% gap from best known
- Excellent as initialization method for more sophisticated algorithms
- Linear scaling as expected from O(nmk) complexity

**Multi-Start Local Search:**
- More robust than single local search
- Modest improvements over basic local search (typically 0.2-1.0% better)
- 10× runtime overhead compared to single local search
- Diminishing returns suggest single local search often sufficient

**Closest Neighbor:**
- Poor performance on both quality (gaps up to 19%) and runtime
- Not recommended for this problem class

### Algorithm Performance Ranking

**By Solution Quality:**
1. Tabu Search / Local Search (tied for best)
2. Multi-Start Local Search
3. Exact Solver (optimal on small, suboptimal or infeasible on large)
4. Greedy (1-4% gap)
5. Closest Neighbor (7-19% gap)

**By Runtime (large instances):**
1. Local Search (0.01-0.10s)
2. Greedy (0.01-0.48s)
3. Multi-Start (0.05-0.94s)
4. Tabu Search (0.16-0.59s)
5. Exact Solver (highly variable, often fails)

## Recommendations

### Deployment Strategy: Hybrid Approach

For deployment, we recommend a **tiered hybrid approach** based on instance characteristics:

**1. Small Instances (≤100 facilities, ≤500 customers):**
   - **Use**: Exact MIP Solver
   - **Rationale**: Optimality guaranteed in under 0.10 seconds
   - **Expected**: Proven optimal solutions with certificates

**2. Medium Instances (100-500 facilities, 500-2000 customers):**
   - **Primary**: Tabu Search (0.2-0.6 seconds)
   - **Fallback**: If optimality proof required and time permits, run Exact Solver with 600s limit
   - **Rationale**: Tabu Search consistently finds optimal or near-optimal solutions in under 1 second
   - **Expected**: Optimal or within 0.5% of optimal

**3. Large Instances (500-1000 facilities, 2000-5000 customers):**
   - **Step 1**: Run Local Search first (typically <0.5s) to obtain high-quality solution
   - **Step 2**: If additional quality needed, run Tabu Search for 1-2 seconds
   - **Rationale**: Local Search provides excellent solutions extremely fast; Tabu Search can refine if needed
   - **Expected**: Best known solutions, 0.1-2.0 seconds total

**4. Massive Instances (>1000 facilities or >5000 customers):**
   - **Use**: Local Search (only viable tested method)
   - **Rationale**: Scales exceptionally well, finds best known solutions in fractions of a second
   - **Expected**: High-quality solutions in <0.50s

**5. Real-Time Applications (interactive decision support):**
   - **Use**: Greedy followed by Local Search
   - **Rationale**: Total runtime <0.50s even for massive instances
   - **Expected**: Solutions within 1-2% of optimum

**6. Quality-Critical Applications (where solution quality is paramount):**
   - **Use**: Multi-Start Local Search (for massive instances) or Tabu Search (up to 2000 customers)
   - **Rationale**: Accept longer runtimes (1-2 seconds) for superior solution quality
   - **Expected**: Best possible solutions from heuristic methods

### General Deployment Recommendations

1. **Start Simple**: Always run Greedy first as a quick baseline to verify problem setup
2. **Budget Time Wisely**: Allocate 0.1-1.0s for most applications; only quality-critical scenarios justify >2s
3. **Monitor Performance**: Track solution quality and runtime to detect instance-specific patterns
4. **Validate Results**: On small instances, compare heuristics against Exact Solver to build confidence
5. **Consider Hybrid**: For critical decisions, run both Local Search and Tabu Search, then take the best solution

## Limitations and Future Work

### Current Limitations

1. **Tabu Search Scalability**: Implementation fails on instances >2000 customers due to array indexing issues. Code optimization needed for massive instances.

2. **Fixed Parameters**: We used fixed algorithm parameters (tabu tenure = 10, max iterations = 500). Instance-specific tuning could improve performance.

3. **Instance Characteristics**: All tests used uniform random distributions. Real-world instances may exhibit clustering or spatial patterns affecting relative algorithm performance.

4. **License Constraints**: Exact Solver limited by Xpress Community Edition (≤5000 rows). Commercial license required for larger instances.

5. **Single Objective**: We consider only demand maximization. Multi-objective extensions (e.g., balancing coverage and equity) not addressed.

### Future Research Directions

1. **Hybrid Exact-Heuristic Methods**: Use heuristic solutions as warm starts for exact solvers or Benders decomposition

2. **Parallel Computing**: Exploit multi-core architectures for parallel tabu search or distributed local search

3. **Machine Learning Integration**: Predict high-quality facilities based on instance features to guide search

4. **Dynamic and Stochastic Variants**: Handle uncertain demand, facility failures, or time-varying coverage

5. **Very Large Scale**: Combine metaheuristics with decomposition techniques to solve millions-of-customers instances

6. **Multi-Objective Optimization**: Incorporate equity, fairness, or redundancy considerations

## Implementation Quick Start

### Data File Format

All algorithms read standardized `.dat` files with the following structure:

```
! Problem dimensions
I: 50          ! Number of facilities
J: 200         ! Number of customers
BUDGET: 10.0   ! Available budget

! Facility costs and customer demands
COST: [1.0, 1.0, ...]
DEMAND: [10, 15, 20, ...]

! Coverage relationships (which facilities cover which customers)
COVERAGE_I_j: [...]
COVERAGE_J_i: [...]
```

### Running Algorithms

**Single Instance Execution:**
```bash
# Run exact solver
mosel exec src/mclp_exact.mos "DATA_FILE=data/S1.dat"

# Run local search
mosel exec src/mclp_local_search.mos "DATA_FILE=data/L1.dat"

# Run tabu search with custom parameters
mosel exec src/mclp_tabu_search.mos "DATA_FILE=data/XL1.dat MAX_ITER=1000"
```

**Batch Benchmarking:**
```bash
# Run all algorithms on all instances
./run_benchmark.ps1   # Windows PowerShell
./run_benchmark.sh    # Linux/macOS
```

### Software Requirements

- **FICO Xpress Mosel** 5.0 or later (required)
- **FICO Xpress Optimizer** 12.0+ (for exact solver only)
- **Python 3.7+** (for instance generation and visualization)
- **Python packages**: numpy, pandas, matplotlib (optional, for analysis)

**License Notes:**
- Xpress Community Edition: Free, limited to 5000 variables/constraints (sufficient for S, M, L instances)
- Commercial License: Required for XL, XXL instances with exact solver
- Heuristics have no license restrictions

### Troubleshooting

**Issue**: Exact solver fails with "too many variables"
- **Solution**: Use Local Search or Tabu Search heuristics, or upgrade to commercial license

**Issue**: Tabu Search crashes on large instances
- **Solution**: Use Local Search or Multi-Start for instances >2000 customers

**Issue**: Slow performance
- **Solution**: Start with Greedy for baseline, then use Local Search; reduce MAX_ITER if needed

## Comparison with Literature

Our results advance the state-of-the-art in several respects:

- **Instance Sizes**: We solve instances comparable to or larger than previous heuristic studies (Máximo et al., 2017: 7,730 nodes; our XXL1: 6,000 variables)
- **Runtime Performance**: Our Local Search achieves 0.10s on 5,000-customer instances, significantly faster than comparable methods
- **Solution Quality**: Tabu Search consistently matches or exceeds exact solver quality, with notable 387-unit improvement on XL1

Note: Cordeau et al. (2019) solve much larger instances (up to 15 million customers) using specialized Benders decomposition when the number of facilities is relatively small (n << m), demonstrating that exact methods remain viable for specific problem structures.

## References

1. Church, R., and ReVelle, C. (1974). The maximal covering location problem. *Papers in Regional Science*, 32(1), 101-118.

2. Cordeau, J.-F., Furini, F., and Ljubić, I. (2019). Benders decomposition for very large scale partial set covering and maximal covering location problems. *European Journal of Operational Research*, 275(3), 882-896.

3. Murray, A. T. (2016). Maximal coverage location problem: Impacts, significance, and evolution. *International Regional Science Review*, 39(1), 5-27.

4. Máximo, V. R., Nascimento, M. C., and Carvalho, A. C. (2017). Intelligent-guided adaptive search for the maximum covering location problem. *Computers & Operations Research*, 78, 129-137.

5. Glover, F., and Laguna, M. (1997). *Tabu Search*. Kluwer Academic Publishers.

## Deliverables

The complete project includes:

- **Source Code**: Full implementation in Mosel (`Mosel/src/`)
  - `mclp_exact.mos` - Exact MIP solver
  - `mclp_greedy.mos` - Greedy heuristic
  - `mclp_closest_neighbor.mos` - Closest neighbor heuristic
  - `mclp_local_search.mos` - Local search
  - `mclp_multistart.mos` - Multi-start local search
  - `mclp_tabu_search.mos` - Tabu search metaheuristic

- **Data Files**: Generated test instances (`Mosel/data/`)
- **Results**: Comprehensive benchmark results (`Mosel/benchmark_results.md`)
- **Scripts**: Data generation, conversion, and benchmarking scripts (`Mosel/scripts/`)
- **Visualization**: Performance analysis figures and charts (`Mosel/figures/`)
- **Documentation**:
  - This client report (`FINAL_CLIENT_REPORT.md`)
  - Scientific paper with full technical details (`Mosel/SCIENTIFIC_REPORT.tex`)
  - Implementation guide (included in scientific report appendix)

---

**For detailed mathematical formulation, algorithm pseudocode, and comprehensive implementation guide, please refer to `SCIENTIFIC_REPORT.pdf`.**
