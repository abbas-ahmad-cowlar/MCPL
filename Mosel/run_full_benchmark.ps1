# Run full benchmark suite on all datasets
$datasets = @("test_tiny", "S1", "S2", "M1", "M2", "L1", "L2")
$algorithms = @(
    @{Name = "Exact"; File = "src\mclp_exact.mos" },
    @{Name = "Greedy"; File = "src\mclp_greedy.mos" },
    @{Name = "ClosestNeighbor"; File = "src\mclp_closest_neighbor.mos" },
    @{Name = "LocalSearch"; File = "src\mclp_local_search.mos" },
    @{Name = "MultiStart"; File = "src\mclp_multistart.mos" },
    @{Name = "TabuSearch"; File = "src\mclp_tabu_search.mos" }
)

$resultsDir = "results_full"
New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MCLP FULL BENCHMARK SUITE" -ForegroundColor Cyan
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
        # Use simple command format that works reliably in PowerShell
        $cmd = "mosel"
        $moselArgs = @($alg.File, "DATA_FILE='$dataFile'")
        
        # Write-Host "  Command: $cmd $moselArgs"
        
        & $cmd $moselArgs > $outputFile 2>&1
        
        if ($LASTEXITCODE -eq 0) {
            Write-Host " Done." -ForegroundColor Green
        }
        else {
            Write-Host " Failed!" -ForegroundColor Red
        }
    }
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "BENCHMARK COMPLETE" -ForegroundColor Cyan
Write-Host "Results saved in: $resultsDir" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
