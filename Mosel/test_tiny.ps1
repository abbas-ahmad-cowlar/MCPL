# Test all MCLP algorithms on tiny data
Write-Host "==================================="
Write-Host "MCLP ALGORITHMS - TINY DATA TEST"
Write-Host "==================================="
Write-Host ""

$algorithms = @(
    @{Name = "Exact Solver"; File = "src\mclp_exact.mos" },
    @{Name = "Greedy Heuristic"; File = "src\mclp_greedy.mos" },
    @{Name = "Closest Neighbor"; File = "src\mclp_closest_neighbor.mos" },
    @{Name = "Local Search"; File = "src\mclp_local_search.mos" },
    @{Name = "Multi-Start"; File = "src\mclp_multistart.mos" },
    @{Name = "Tabu Search"; File = "src\mclp_tabu_search.mos" }
)

foreach ($alg in $algorithms) {
    Write-Host "-----------------------------------"
    Write-Host "Running: $($alg.Name)"
    Write-Host "-----------------------------------"
    mosel $alg.File
    Write-Host ""
}

Write-Host "==================================="
Write-Host "ALL TESTS COMPLETE"
Write-Host "==================================="
