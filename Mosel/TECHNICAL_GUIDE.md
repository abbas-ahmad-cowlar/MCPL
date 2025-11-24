# MCLP Technical Guide

## 1. System Requirements

- **FICO Xpress Mosel**: Version 5.0 or higher.
- **Python**: Version 3.8 or higher (required for data scripts).
- **PowerShell**: For execution scripts (Windows).

## 2. Compilation

The Mosel source files are located in `src/`. They can be compiled individually or run directly.
Common compilation errors:

- `E-100`: Syntax error. Ensure you are using the correct Mosel version.
- `E-33`: Data file error. Ensure `.dat` files in `data/` are generated correctly using `scripts/convert_json_to_mosel.py`.

## 3. Data Management

### Generating New Instances

Use `scripts/generate_instance.py` to create random datasets:

```bash
python scripts/generate_instance.py --I 100 --J 500 --B 20 --radius 5.0 --seed 42 -o new_instance.json
```

### Converting to Mosel Format

Mosel requires a specific `.dat` format. Convert JSON files using:

```bash
python scripts/convert_json_to_mosel.py --input new_instance.json --output data/
```

## 4. Running Benchmarks

The `run_benchmark.ps1` script orchestrates the execution of all algorithms.
It:

1.  Iterates through all datasets defined in the script.
2.  Runs each algorithm (`Exact`, `Greedy`, `TabuSearch`, etc.).
3.  Sets a time limit (e.g., 600s) for the Exact solver on large instances.
4.  Captures output to `results/`.

## 5. Algorithm Details

- **Exact Solver (`mclp_exact.mos`)**: Uses Xpress Optimizer. Best for small instances.
- **Tabu Search (`mclp_tabu_search.mos`)**: Metaheuristic with memory structures. Best for large instances.
- **Local Search (`mclp_local_search.mos`)**: Fast improvement heuristic.
- **Multi-Start (`mclp_multistart.mos`)**: Runs Local Search from multiple points.

## 6. Troubleshooting

- **License Error**: If the Exact solver fails on large instances (e.g., XXL1), it is likely due to the Xpress Community License limit (5000 constraints/variables). Use heuristics instead.
- **Index Out of Range**: Ensure data files match the expected format (dense arrays for COST/DEMAND).
