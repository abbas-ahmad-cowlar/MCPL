# Run all MCLP algorithms on tiny data and save results
$outputDir = "results_tiny"
New-Item -ItemType Directory -Force -Path $outputDir | Out-Null

$algorithms = @(
    @{Name = "Exact"; File = "src\mclp_exact.mos"; Output = "$outputDir\exact.txt" },
    @{Name = "Greedy"; File = "src\mclp_greedy.mos"; Output = "$outputDir\greedy.txt" },
    @{Name = "Closest Neighbor"; File = "src\mclp_closest_neighbor.mos"; Output = "$outputDir\closest_neighbor.txt" },
    @{Name = "Local Search"; File = "src\mclp_local_search.mos"; Output = "$outputDir\local_search.txt" },
    @{Name = "Multi-Start"; File = "src\mclp_multistart.mos"; Output = "$outputDir\multistart.txt" },
    @{Name = "Tabu Search"; File = "src\mclp_tabu_search.mos"; Output = "$outputDir\tabu_search.txt" }
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "MCLP ALGORITHMS - TINY DATA TEST" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

foreach ($alg in $algorithms) {
    Write-Host "Running: $($alg.Name)..." -ForegroundColor Yellow
    mosel $alg.File > $alg.Output 2>&1
    if ($LASTEXITCODE -eq 0) {
        Write-Host "  ✓ Complete - Results saved to $($alg.Output)" -ForegroundColor Green
    }
    else {
        Write-Host "  ✗ Failed - Check $($alg.Output) for errors" -ForegroundColor Red
    }
}

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "ALL TESTS COMPLETE" -ForegroundColor Cyan
Write-Host "Results saved in: $outputDir" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
