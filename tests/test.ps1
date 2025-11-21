Write-Host "`n======================================================================"
Write-Host "FINAL PRE-FLIGHT CHECKLIST" -ForegroundColor Yellow
Write-Host "======================================================================"

$checks = @(
    @{Name="Virtual environment active"; Test={$env:VIRTUAL_ENV}},
    @{Name="test_tiny.json exists"; Test={Test-Path "data/test_tiny.json"}},
    @{Name="All 6 instances exist"; Test={(Get-ChildItem data/*.json | Where-Object {$_.Name -match '^[SML][12]\.json$'}).Count -eq 6}},
    @{Name="results/ directory exists"; Test={Test-Path "results"}},
    @{Name="src/__init__.py exists"; Test={Test-Path "src/__init__.py"}},
    @{Name="run_mclp.py works"; Test={
        python src/run_mclp.py --instance data/test_tiny.json --algorithm greedy --seed 42 --output results/preflight_test.csv 2>&1 | Out-Null
        $LASTEXITCODE -eq 0
    }}
)

$allPass = $true
foreach ($check in $checks) {
    $result = & $check.Test
    if ($result) {
        Write-Host "[OK] $($check.Name)" -ForegroundColor Green
    } else {
        Write-Host "[FAIL] $($check.Name)" -ForegroundColor Red
        $allPass = $false
    }
}

Write-Host "======================================================================"
if ($allPass) {
    Write-Host "ALL CHECKS PASSED - READY FOR FULL EXPERIMENTS" -ForegroundColor Green
} else {
    Write-Host "SOME CHECKS FAILED - FIX ISSUES BEFORE PROCEEDING" -ForegroundColor Red
    exit 1
}