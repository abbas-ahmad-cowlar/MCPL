$ErrorActionPreference = "Stop"

$OUTPUT = "results/test_experiment_small.csv"
rm $OUTPUT -ErrorAction SilentlyContinue

Write-Host "Running small-scale experiment test..."
Write-Host "Instance: S1"
Write-Host "Algorithms: greedy, cn, ls, ts"
Write-Host "Seeds: 42, 43, 44"
Write-Host ""

$algorithms = @('greedy', 'cn', 'ls', 'ts')
$seeds = @(42, 43, 44)
$total = 0

foreach ($seed in $seeds) {
    foreach ($algo in $algorithms) {
        Write-Host "Running $algo (seed=$seed)..." -ForegroundColor Cyan
        python src/run_mclp.py --instance data/S1.json --algorithm $algo --seed $seed --output $OUTPUT
        
        if ($LASTEXITCODE -ne 0) {
            Write-Host "[FAIL] Experiment failed" -ForegroundColor Red
            exit 1
        }
        $total++
    }
}

Write-Host "`n[OK] All experiments completed" -ForegroundColor Green

# Analyze results
$df = Import-Csv $OUTPUT

Write-Host "`nResults Summary:"
Write-Host "Total experiments: $($df.Count) (expected: $total)"

# Group by algorithm
$df | Group-Object algorithm | ForEach-Object {
    $avgObj = ($_.Group.objective | Measure-Object -Average).Average
    $avgTime = ($_.Group.runtime_sec | Measure-Object -Average).Average
    Write-Host "  $($_.Name): avg_obj=$([math]::Round($avgObj,1)), avg_time=$([math]::Round($avgTime,4))s"
}

# Check for anomalies
$objectives = $df.objective | ForEach-Object { [double]$_ }
$minObj = ($objectives | Measure-Object -Minimum).Minimum
$maxObj = ($objectives | Measure-Object -Maximum).Maximum

if ($minObj -eq 0) {
    Write-Host "[FAIL] Some experiments returned objective=0" -ForegroundColor Red
    exit 1
}

Write-Host "`n[PASS] Small-scale experiment test successful" -ForegroundColor Green