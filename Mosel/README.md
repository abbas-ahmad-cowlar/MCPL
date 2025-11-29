# MCLP Optimization Suite

## 📋 Overview

This project provides a high-performance implementation of the **Maximum Covering Location Problem (MCLP)** using **FICO Xpress Mosel**. It is designed to solve large-scale facility location problems efficiently, featuring a suite of exact solvers, heuristics, and metaheuristics.

The suite is capable of handling instances ranging from small (50 facilities) to massive (1000 facilities, 5000 customers), providing optimal or near-optimal solutions in seconds.

## 📂 Project Structure

```
MCLP_Optimization_Suite/
├── src/                        # Mosel Source Code
│   ├── mclp_exact.mos          # Exact MIP solver (Xpress Optimizer)
│   ├── mclp_greedy.mos         # Greedy heuristic
│   ├── mclp_closest_neighbor.mos # Closest Neighbor heuristic
│   ├── mclp_local_search.mos   # Local Search improvement heuristic
│   ├── mclp_multistart.mos     # Multi-Start Local Search
│   └── mclp_tabu_search.mos    # Tabu Search Metaheuristic
├── data/                       # Benchmark Datasets (.dat)
│   ├── test_tiny.dat           # Test instance (small, for quick testing)
│   ├── S1.dat, S2.dat          # Small (50 facilities, 200 customers)
│   ├── M1.dat, M2.dat          # Medium (100 facilities, 500 customers)
│   ├── L1.dat, L2.dat          # Large (200 facilities, 1000 customers)
│   ├── XL1.dat                 # Extra Large (500 facilities, 2000 customers)
│   └── XXL1.dat                # Massive (1000 facilities, 5000 customers)
├── scripts/                    # Utility Scripts
│   ├── generate_instance.py    # Generate new random instances
│   ├── generate_visualizations.py  # Generate figures and performance tables
│   ├── update_report_tables.py # Auto-updates report with latest results
│   ├── convert_json_to_mosel.py # Convert JSON data to Mosel format
│   ├── run_benchmark.ps1        # Benchmark execution script
│   └── install_miktex.ps1      # MiKTeX installation helper
├── results_complete/           # Latest Benchmark Output Logs
├── figures/                    # Generated Figures and Tables
│   ├── runtime_vs_size.pdf
│   ├── solution_quality_vs_size.pdf
│   ├── runtime_comparison.pdf
│   └── performance_table.tex
├── SCIENTIFIC_REPORT.tex       # 📄 Comprehensive Report (LaTeX Source)
├── SCIENTIFIC_REPORT.pdf       # 📄 Compiled PDF Report
├── run_complete_workflow.ps1   # 🚀 Complete Workflow (Recommended)
├── requirements_viz.txt        # Python dependencies for visualization
└── archive/                    # Archived files
    ├── latex_aux/              # LaTeX auxiliary files (.aux, .log, .out, .toc)
    ├── report_backups/         # Report version backups
    └── ...                     # Other archived files
```

## 🚀 Quick Start

### Prerequisites

1. **FICO Xpress Mosel** (Version 5.0+)
   - Download from: https://www.fico.com/en/products/fico-xpress-optimization
   - Ensure `mosel` command is available in PATH

2. **Python 3.8+** (for data generation and visualization)
   - Download from: https://www.python.org/
   - Install required packages: `pip install -r requirements_viz.txt`

3. **PowerShell** (for execution scripts)
   - Pre-installed on Windows 10/11

4. **LaTeX Distribution** (optional, for PDF report compilation)
   - **Windows**: MiKTeX (recommended) - see installation below
   - **Cross-platform**: TeX Live
   - Installation is optional; you can compile the report later

### Installation Steps

#### 1. Install MiKTeX (for PDF Report Compilation)

**Option A: Automatic Installation (Recommended)**
```powershell
.\scripts\install_miktex.ps1
```
This script uses `winget` (Windows Package Manager) if available, or provides manual installation instructions.

**Option B: Manual Installation**
1. Download MiKTeX from: https://miktex.org/download
2. Run the installer
3. **Important**: Check "Add MiKTeX to PATH" during installation
4. Restart PowerShell after installation

**Verify Installation:**
```powershell
pdflatex --version
```

#### 2. Install Python Dependencies

```powershell
pip install -r requirements_viz.txt
```

This installs: `pandas`, `matplotlib`, `seaborn`, `numpy`

#### 3. Verify FICO Xpress Mosel

```powershell
mosel -v
```

## 🎯 Complete Workflow (Recommended)

To run benchmarks, generate visualizations, update the report, and compile PDF:

```powershell
.\run_complete_workflow.ps1 -CompileReport
```

This single command will:
1. ✅ Run all benchmarks (all 6 algorithms on all 9 datasets)
2. ✅ Generate all figures and performance tables
3. ✅ Automatically update `SCIENTIFIC_REPORT.tex` with latest results
4. ✅ Compile the PDF report (if LaTeX is installed)
5. ✅ Automatically move LaTeX auxiliary files to `archive/latex_aux/` (keeps root clean)

**Without PDF compilation:**
```powershell
.\run_complete_workflow.ps1
```

### What Gets Updated Automatically

- **Performance Table**: All objective values and gaps
- **Runtime Table**: All runtime values
- **Backup System**: Previous report versions are archived in `archive/report_backups/` with timestamps
- **LaTeX Files**: Auxiliary files (`.aux`, `.log`, `.out`, `.toc`) are automatically moved to `archive/latex_aux/` after compilation

### Manual Steps (After Workflow)

- **Best Known Solutions Table**: May require manual review to identify which algorithm found the best solution
- **Discussion Sections**: Review and update if results change significantly
- **Algorithm Rankings**: Update if relative performance changes

## 🔧 Individual Workflow Steps

### Running Benchmarks Only

To run only the benchmarks (without visualization/report updates):

```powershell
.\scripts\run_benchmark.ps1
```

This saves results to `results_complete/` directory.

### Generating Visualizations Only

To generate figures and tables from existing results:

```powershell
python scripts/generate_visualizations.py
```

This creates figures in `figures/` directory:
- `runtime_vs_size.pdf` / `.png`
- `solution_quality_vs_size.pdf` / `.png`
- `runtime_comparison.pdf` / `.png`
- `performance_table.tex` / `.csv`
- `instance_characteristics.tex` / `.csv`

### Updating Report Tables Only

To update the report with latest results:

```powershell
python scripts/update_report_tables.py
```

This updates `SCIENTIFIC_REPORT.tex` and creates a backup.

### Compiling PDF Report

**Automatic (via workflow):**
```powershell
.\run_complete_workflow.ps1 -CompileReport
```

**Manual:**
```powershell
pdflatex SCIENTIFIC_REPORT.tex
pdflatex SCIENTIFIC_REPORT.tex  # Run twice for references
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

## 📊 Output Files

### Results
- **Location**: `results_complete/`
- **Format**: Text files with detailed algorithm output
- **Naming**: `{DATASET}_{ALGORITHM}.txt`
- **Example**: `S1_Exact.txt`, `XL1_TabuSearch.txt`

### Figures
- **Location**: `figures/`
- **Formats**: PDF (for report) and PNG (for preview)
- **Files**:
  - `runtime_vs_size.pdf` - Runtime scaling analysis
  - `solution_quality_vs_size.pdf` - Solution quality analysis
  - `runtime_comparison.pdf` - Comparative runtime analysis

### Tables
- **Location**: `figures/`
- **Files**:
  - `performance_table.tex` / `.csv` - Performance comparison
  - `instance_characteristics.tex` / `.csv` - Instance details

### Report
- **Source**: `SCIENTIFIC_REPORT.tex`
- **Compiled**: `SCIENTIFIC_REPORT.pdf` (after compilation)
- **Backups**: `archive/report_backups/SCIENTIFIC_REPORT_YYYYMMDD_HHMMSS.tex` and `.tex.backup`
- **LaTeX Auxiliary Files**: `archive/latex_aux/` (`.aux`, `.log`, `.out`, `.toc` files)

## 🐛 Troubleshooting

### Python not found
- Install Python 3.8+ from https://www.python.org/
- Ensure Python is in PATH
- Restart PowerShell after installation

### Missing Python packages
```powershell
pip install pandas matplotlib seaborn numpy
```

### pdflatex not found
- Install MiKTeX: `.\scripts\install_miktex.ps1`
- Or download from: https://miktex.org/download
- Ensure "Add to PATH" is checked during installation
- Restart PowerShell after installation

### mosel not found
- Install FICO Xpress Mosel from: https://www.fico.com/en/products/fico-xpress-optimization
- Add Mosel bin directory to PATH
- Restart PowerShell

### Report update fails
- Check that `figures/performance_table.tex` exists
- Check that `results_complete/` has result files
- Review error messages in console

### Compilation errors
- Check LaTeX log file: `archive/latex_aux/SCIENTIFIC_REPORT.log`
- Ensure all figure files exist in `figures/` directory
- Verify all required LaTeX packages are installed (MiKTeX installs automatically)
- Note: LaTeX auxiliary files are automatically moved to `archive/latex_aux/` after compilation

## 📚 Documentation

- **Report**: `SCIENTIFIC_REPORT.tex` - Comprehensive academic-style report (LaTeX)
- **Pseudocode**: `pseudocode/` - Detailed algorithm logic for each heuristic
- **Archived Files**: `archive/` - Deprecated reports, old results, and outdated documentation

## 🔄 After Code Changes

If you modify any algorithm code:

1. **Run the complete workflow:**
   ```powershell
   .\run_complete_workflow.ps1 -CompileReport
   ```

2. **Review the updated report:**
   - Check that tables are correct
   - Review discussion sections
   - Update "Best Known Solutions" table if needed
   - Update algorithm rankings if performance changed

3. **Recompile if you made manual changes:**
   ```powershell
   pdflatex SCIENTIFIC_REPORT.tex
   pdflatex SCIENTIFIC_REPORT.tex  # Run twice for references
   ```
   Note: LaTeX auxiliary files will remain in root if compiled manually. Use the workflow script to automatically organize them.

## 📝 License

This project is provided for research and educational purposes.

---

_MCLP Optimization Suite - Production Ready_
