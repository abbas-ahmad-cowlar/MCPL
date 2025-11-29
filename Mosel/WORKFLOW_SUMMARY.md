# Complete Workflow Summary

## What `run_complete_workflow.ps1` Does

When you run `.\run_complete_workflow.ps1`, it automatically:

### ✅ Step 1: Runs All Benchmarks
- Executes all 6 algorithms on all 9 datasets
- Saves results to `results_complete/`
- Uses `run_benchmark.ps1`

### ✅ Step 2: Generates Visualizations & Tables
- Creates all figures (PDF and PNG):
  - `runtime_vs_size.pdf`
  - `solution_quality_vs_size.pdf`
  - `runtime_comparison.pdf`
- Generates LaTeX tables:
  - `performance_table.tex`
  - `instance_characteristics.tex`
- Uses `scripts/generate_visualizations.py`

### ✅ Step 3: Updates Report Tables (NEW!)
- **Automatically updates `SCIENTIFIC_REPORT.tex`** with latest values:
  - Performance comparison table (objectives and gaps)
  - Runtime comparison table
  - Creates backup: `SCIENTIFIC_REPORT.tex.backup`
- Uses `scripts/update_report_tables.py`

### ✅ Step 4: Compiles PDF (Optional)
- If you use `-CompileReport` flag:
  - Compiles `SCIENTIFIC_REPORT.tex` to PDF
  - Runs `pdflatex` twice (for references)
  - Generates `SCIENTIFIC_REPORT.pdf`

## Usage

### Basic (without PDF compilation):
```powershell
.\run_complete_workflow.ps1
```

### Complete (with PDF compilation):
```powershell
.\run_complete_workflow.ps1 -CompileReport
```

## What Gets Updated Automatically

### ✅ Automatically Updated:
- **Performance Table** (`tab:performance`): All objective values and gaps
- **Runtime Table** (`tab:runtime`): All runtime values

### ⚠️ Requires Manual Review:
- **Best Known Solutions Table** (`tab:best-known`): Requires interpretation to determine which algorithm found the best solution
- **Discussion sections**: May need updates if results change significantly
- **Algorithm rankings**: May need updates if relative performance changes

## Requirements

### Python Packages:
```bash
pip install -r requirements_viz.txt
```
Includes: `pandas`, `matplotlib`, `seaborn`, `numpy`

### LaTeX Distribution (for PDF compilation):
- **Windows**: MiKTeX (https://miktex.org/download)
- **Cross-platform**: TeX Live (https://www.tug.org/texlive/)
- See `LATEX_REQUIREMENTS.md` for details

## After Code Changes

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
   pdflatex SCIENTIFIC_REPORT.tex
   ```

## File Locations

- **Results**: `results_complete/*.txt`
- **Figures**: `figures/*.pdf`, `figures/*.png`
- **Tables**: `figures/*.tex`, `figures/*.csv`
- **Report**: `SCIENTIFIC_REPORT.tex` (updated automatically)
- **Backup**: `SCIENTIFIC_REPORT.tex.backup` (created before update)

## Troubleshooting

### Python not found:
- Install Python 3.8+ from https://www.python.org/
- Ensure Python is in PATH

### Missing Python packages:
```bash
pip install pandas matplotlib seaborn numpy
```

### pdflatex not found:
- Install MiKTeX or TeX Live
- See `LATEX_REQUIREMENTS.md` for details

### Report update fails:
- Check that `figures/performance_table.tex` exists
- Check that `results_complete/` has result files
- Review error messages in console

