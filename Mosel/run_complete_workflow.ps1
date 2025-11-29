# Complete MCLP Benchmark Workflow
# This script runs all benchmarks, generates visualizations, and optionally compiles the report
# Usage: .\run_complete_workflow.ps1 [-CompileReport]

param(
    [switch]$CompileReport = $false
)

$ErrorActionPreference = "Continue"

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MCLP COMPLETE WORKFLOW" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Run benchmarks
Write-Host "STEP 1: Running benchmarks..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
& .\scripts\run_benchmark.ps1

if ($LASTEXITCODE -ne 0) {
    Write-Host "ERROR: Benchmark execution failed!" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "STEP 2: Generating visualizations and tables..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow

# Check if Python is available
$pythonCmd = $null
if (Get-Command python -ErrorAction SilentlyContinue) {
    $pythonCmd = "python"
} elseif (Get-Command python3 -ErrorAction SilentlyContinue) {
    $pythonCmd = "python3"
} else {
    Write-Host "ERROR: Python not found! Please install Python 3.8+ and required packages." -ForegroundColor Red
    Write-Host "Install requirements: pip install -r requirements_viz.txt" -ForegroundColor Yellow
    exit 1
}

# Check if required packages are installed
Write-Host "  Checking Python dependencies..." -NoNewline
try {
    $check = & $pythonCmd -c "import pandas, matplotlib, seaborn, numpy" 2>&1
    if ($LASTEXITCODE -ne 0) {
        Write-Host " FAILED" -ForegroundColor Red
        Write-Host "  ERROR: Required Python packages not installed!" -ForegroundColor Red
        Write-Host "  Run: pip install -r requirements_viz.txt" -ForegroundColor Yellow
        exit 1
    }
    Write-Host " OK" -ForegroundColor Green
} catch {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  ERROR: Could not check Python packages!" -ForegroundColor Red
    exit 1
}

# Run visualization script
Write-Host "  Running visualization generator..." -NoNewline
& $pythonCmd scripts/generate_visualizations.py
if ($LASTEXITCODE -ne 0) {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  ERROR: Visualization generation failed!" -ForegroundColor Red
    exit 1
}
Write-Host " Done" -ForegroundColor Green

Write-Host ""
Write-Host "STEP 3: Updating report with latest results..." -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host "  Updating tables in SCIENTIFIC_REPORT.tex..." -NoNewline
& $pythonCmd scripts/update_report_tables.py
if ($LASTEXITCODE -ne 0) {
    Write-Host " FAILED" -ForegroundColor Red
    Write-Host "  WARNING: Report update failed, but continuing..." -ForegroundColor Yellow
} else {
    Write-Host " Done" -ForegroundColor Green
}

Write-Host ""
Write-Host "STEP 4: Summary" -ForegroundColor Yellow
Write-Host "----------------------------------------" -ForegroundColor Yellow
Write-Host "  Results: results_complete/" -ForegroundColor Cyan
$resultCount = (Get-ChildItem "results_complete\*.txt" -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "    ($resultCount result files)" -ForegroundColor Gray
Write-Host "  Figures: figures/" -ForegroundColor Cyan
$figureCount = (Get-ChildItem "figures\*.pdf","figures\*.png","figures\*.tex" -ErrorAction SilentlyContinue | Measure-Object).Count
Write-Host "    ($figureCount generated files)" -ForegroundColor Gray

if ($CompileReport) {
    Write-Host ""
    Write-Host "STEP 5: Compiling LaTeX report..." -ForegroundColor Yellow
    Write-Host "----------------------------------------" -ForegroundColor Yellow
    
    # Check if pdflatex is available
    if (-not (Get-Command pdflatex -ErrorAction SilentlyContinue)) {
        Write-Host "  WARNING: pdflatex not found. Skipping report compilation." -ForegroundColor Yellow
        Write-Host "  To compile manually: pdflatex SCIENTIFIC_REPORT.tex" -ForegroundColor Gray
    } else {
        Write-Host "  Compiling SCIENTIFIC_REPORT.tex..." -NoNewline
        Push-Location $PSScriptRoot
        
        # Compile LaTeX (run twice for references)
        & pdflatex -interaction=nonstopmode SCIENTIFIC_REPORT.tex > $null 2>&1
        & pdflatex -interaction=nonstopmode SCIENTIFIC_REPORT.tex > $null 2>&1
        
        # Move LaTeX auxiliary files to archive/latex_aux/
        $latexAuxDir = "archive\latex_aux"
        New-Item -ItemType Directory -Force -Path $latexAuxDir | Out-Null
        
        $auxFiles = @("SCIENTIFIC_REPORT.aux", "SCIENTIFIC_REPORT.log", "SCIENTIFIC_REPORT.out", "SCIENTIFIC_REPORT.toc")
        foreach ($file in $auxFiles) {
            if (Test-Path $file) {
                Move-Item -Path $file -Destination "$latexAuxDir\$file" -Force -ErrorAction SilentlyContinue
            }
        }
        
        Pop-Location
        
        if (Test-Path "SCIENTIFIC_REPORT.pdf") {
            Write-Host " Done" -ForegroundColor Green
            Write-Host "  Report: SCIENTIFIC_REPORT.pdf" -ForegroundColor Cyan
            Write-Host "  LaTeX aux files moved to: archive/latex_aux/" -ForegroundColor Gray
        } else {
            Write-Host " FAILED" -ForegroundColor Red
            Write-Host "  Check LaTeX errors in: archive/latex_aux/SCIENTIFIC_REPORT.log" -ForegroundColor Yellow
        }
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "WORKFLOW COMPLETE" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Review results in: results_complete/" -ForegroundColor Gray
Write-Host "  2. Check figures in: figures/" -ForegroundColor Gray
if (-not $CompileReport) {
    Write-Host "  3. Compile report: pdflatex SCIENTIFIC_REPORT.tex" -ForegroundColor Gray
} else {
    Write-Host "  3. Review report: SCIENTIFIC_REPORT.pdf" -ForegroundColor Gray
}
Write-Host ""

