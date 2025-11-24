# Run benchmark on LARGE datasets
$datasets = @("XL1", "XXL1")
$algorithms = @(
    @{Name = "Exact"; File = "src\mclp_exact.mos" },
    @{Name = "Greedy"; File = "src\mclp_greedy.mos" },
    @{Name = "ClosestNeighbor"; File = "src\mclp_closest_neighbor.mos" },
    @{Name = "LocalSearch"; File = "src\mclp_local_search.mos" },
    @{Name = "MultiStart"; File = "src\mclp_multistart.mos" },
    @{Name = "TabuSearch"; File = "src\mclp_tabu_search.mos" }
)

$resultsDir = "results_large"
New-Item -ItemType Directory -Force -Path $resultsDir | Out-Null

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MCLP LARGE SCALE BENCHMARK" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($dataset in $datasets) {
    Write-Host "----------------------------------------" -ForegroundColor Magenta
    Write-Host "Dataset: $dataset" -ForegroundColor Magenta
    Write-Host "----------------------------------------" -ForegroundColor Magenta
    
    foreach ($alg in $algorithms) {
        $outputFile = "$resultsDir\${dataset}_$($alg.Name).txt"
        Write-Host "  Running $($alg.Name)..." -NoNewline
        
        $dataFile = "data/${dataset}.dat"
        $cmd = "mosel"
        # Pass parameters: DATA_FILE and TIME_LIMIT (for Exact)
        $moselArgs = @($alg.File, "DATA_FILE='$dataFile'", "TIME_LIMIT=600")
        
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
