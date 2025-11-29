# Run COMPLETE benchmark suite on ALL datasets (Tiny to XXL)
$datasets = @("test_tiny", "S1", "S2", "M1", "M2", "L1", "L2", "XL1", "XXL1")
$algorithms = @(
    @{Name = "Exact"; File = "src\mclp_exact.mos" },
    @{Name = "Greedy"; File = "src\mclp_greedy.mos" },
    @{Name = "ClosestNeighbor"; File = "src\mclp_closest_neighbor.mos" },
    @{Name = "LocalSearch"; File = "src\mclp_local_search.mos" },
    @{Name = "MultiStart"; File = "src\mclp_multistart.mos" },
    @{Name = "TabuSearch"; File = "src\mclp_tabu_search.mos" }
)

$resultsDir = "results_complete"
New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MCLP COMPLETE BENCHMARK SUITE" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($dataset in $datasets) {
    Write-Host "----------------------------------------" -ForegroundColor Magenta
    Write-Host "Dataset: $dataset" -ForegroundColor Magenta
    Write-Host "----------------------------------------" -ForegroundColor Magenta
    
    foreach ($alg in $algorithms) {
        $outputFile = "$resultsDir\${dataset}_$($alg.Name).txt"
        Write-Host "  Running $($alg.Name)..." -NoNewline
        
        # Run Mosel with data file parameter
        $dataFile = "data/${dataset}.dat"
        $cmd = "mosel"
        
        # Base arguments
        $moselArgs = @($alg.File, "DATA_FILE='$dataFile'")
        
        # Add time limit for Exact solver (10 minutes)
        if ($alg.Name -eq "Exact") {
            $moselArgs += "TIME_LIMIT=600"
        }
        
        # Execute and capture output
        # Using & operator for execution
        & $cmd $moselArgs > $outputFile 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host " Done." -ForegroundColor Green
        }
        else {
            # Check if it's a license error (exit code might be non-zero)
            # But Mosel often returns 0 even on error, so we check file content later
            Write-Host " Done (check output)." -ForegroundColor Yellow
        }
    }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BENCHMARK COMPLETE" -ForegroundColor Cyan
Write-Host "Results saved in: $resultsDir" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next step: Run visualization generator" -ForegroundColor Yellow
Write-Host "  python scripts/generate_visualizations.py" -ForegroundColor Gray
Write-Host ""
Write-Host "Or run complete workflow:" -ForegroundColor Yellow
Write-Host "  .\run_complete_workflow.ps1" -ForegroundColor Gray
Write-Host ""

# Explicitly exit with success code
exit 0