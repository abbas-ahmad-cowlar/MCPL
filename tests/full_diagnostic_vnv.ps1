# ============================================================================
# MCLP Framework - Complete Verification & Validation Script
# ============================================================================
# This script tests EVERYTHING before running full experiments
# Estimated runtime: 5-10 minutes
# ============================================================================

$ErrorActionPreference = "Stop"

# Color coding functions
function Write-Pass { param($msg) Write-Host "[PASS] $msg" -ForegroundColor Green }
function Write-Fail { param($msg) Write-Host "[FAIL] $msg" -ForegroundColor Red }
function Write-Warn { param($msg) Write-Host "[WARN] $msg" -ForegroundColor Yellow }
function Write-Info { param($msg) Write-Host "[INFO] $msg" -ForegroundColor Cyan }
function Write-Section { param($msg) Write-Host "`n========================================" -ForegroundColor Magenta; Write-Host $msg -ForegroundColor Magenta; Write-Host "========================================" -ForegroundColor Magenta }

# Statistics tracking
$script:totalTests = 0
$script:passedTests = 0
$script:failedTests = 0
$script:warnings = 0
$script:criticalIssues = @()

function Test-Condition {
    param($Name, $Condition, $IsCritical = $false)
    $script:totalTests++
    if ($Condition) {
        Write-Pass $Name
        $script:passedTests++
        return $true
    } else {
        Write-Fail $Name
        $script:failedTests++
        if ($IsCritical) {
            $script:criticalIssues += $Name
        }
        return $false
    }
}

# Start diagnostic
$startTime = Get-Date
Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "  MCLP FRAMEWORK - COMPLETE DIAGNOSTIC & VALIDATION SUITE" -ForegroundColor Cyan
Write-Host "  Starting at: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

# ============================================================================
# STAGE 0: ENVIRONMENT VALIDATION
# ============================================================================
Write-Section "STAGE 0: Environment Validation"

# Test 0.1: Python version
Write-Info "Test 0.1: Checking Python version..."
try {
    $pythonVersion = python --version 2>&1
    $versionMatch = $pythonVersion -match "Python (\d+)\.(\d+)"
    $majorVersion = [int]$Matches[1]
    $minorVersion = [int]$Matches[2]
    Test-Condition "Python version ($pythonVersion)" (($majorVersion -eq 3) -and ($minorVersion -ge 8)) -IsCritical $true
} catch {
    Test-Condition "Python installed" $false -IsCritical $true
}

# Test 0.2: Virtual environment active
Write-Info "Test 0.2: Checking virtual environment..."
Test-Condition "Virtual environment active" ($env:VIRTUAL_ENV -ne $null) -IsCritical $true

# Test 0.3: Required packages
Write-Info "Test 0.3: Checking required packages..."
try {
    $packageCheck = python -c "import numpy, pandas, yaml, matplotlib, pytest; print('OK')" 2>&1
    Test-Condition "All required packages installed" ($packageCheck -match "OK") -IsCritical $true
} catch {
    Test-Condition "All required packages installed" $false -IsCritical $true
}

# Test 0.4: Project structure
Write-Info "Test 0.4: Checking project structure..."
$requiredDirs = @('data', 'src', 'scripts', 'tests', 'results')
$requiredFiles = @('src/__init__.py', 'requirements.txt', 'config.yaml')

foreach ($dir in $requiredDirs) {
    Test-Condition "Directory exists: $dir" (Test-Path $dir)
}

foreach ($file in $requiredFiles) {
    Test-Condition "File exists: $file" (Test-Path $file)
}

# Test 0.5: Python can import framework
Write-Info "Test 0.5: Testing framework imports..."
$importScript = @"
import sys
sys.path.insert(0, 'src')
from instance_loader import MCLPInstance
from greedy import greedy_heuristic
from tabu_search import run_tabu_search
print('OK')
"@

try {
    $importTest = python -c $importScript 2>&1
    Test-Condition "Framework imports work" ($importTest -match "OK") -IsCritical $true
} catch {
    Test-Condition "Framework imports work" $false -IsCritical $true
}

# ============================================================================
# STAGE 1: CORE DATA VALIDATION
# ============================================================================
Write-Section "STAGE 1: Core Data Validation"

# Test 1.1: test_tiny.json loads
Write-Info "Test 1.1: Loading test_tiny.json..."
$loadScript = @"
import sys
sys.path.insert(0, 'src')
from instance_loader import MCLPInstance
inst = MCLPInstance('data/test_tiny.json')
print(f'{len(inst.I)},{len(inst.J)}')
"@

try {
    $loadTest = python -c $loadScript 2>&1
    Test-Condition "test_tiny.json loads" ($loadTest -match "\d+,\d+") -IsCritical $true
} catch {
    Test-Condition "test_tiny.json loads" $false -IsCritical $true
}

# Test 1.2: Coverage matrix symmetry
Write-Info "Test 1.2: Validating coverage matrix..."
$symmetryScript = @"
import sys
sys.path.insert(0, 'src')
from instance_loader import MCLPInstance
inst = MCLPInstance('data/test_tiny.json')
total_ij = sum(len(v) for v in inst.I_j.values())
total_ji = sum(len(v) for v in inst.J_i.values())
print('PASS' if total_ij == total_ji else 'FAIL')
"@

try {
    $symmetryTest = python -c $symmetryScript 2>&1
    Test-Condition "Coverage matrix symmetric" ($symmetryTest -match "PASS")
} catch {
    Test-Condition "Coverage matrix symmetric" $false
}

# Test 1.3: No orphaned customers
Write-Info "Test 1.3: Checking for orphaned customers..."
$orphanScript = @"
import sys
sys.path.insert(0, 'src')
from instance_loader import MCLPInstance
inst = MCLPInstance('data/test_tiny.json')
orphaned = [j for j in inst.J if j not in inst.I_j or len(inst.I_j[j]) == 0]
print('PASS' if not orphaned else f'FAIL:{len(orphaned)}')
"@

try {
    $orphanTest = python -c $orphanScript 2>&1
    Test-Condition "No orphaned customers in test_tiny" ($orphanTest -match "PASS") -IsCritical $true
} catch {
    Test-Condition "No orphaned customers in test_tiny" $false -IsCritical $true
}

# ============================================================================
# STAGE 2: ALGORITHM UNIT TESTS
# ============================================================================
Write-Section "STAGE 2: Algorithm Unit Tests"

# Test 2.1: Greedy heuristic
Write-Info "Test 2.1: Testing Greedy heuristic..."
try {
    $greedyOutput = python src/greedy.py --instance data/test_tiny.json --seed 42 2>&1 | Out-String
    $greedyObj = if ($greedyOutput -match "Total demand covered: ([\d.]+)") { [double]$Matches[1] } else { 0 }
    Test-Condition "Greedy runs successfully" ($greedyObj -gt 100) -IsCritical $true
    Write-Info "  Greedy objective: $greedyObj"
} catch {
    Test-Condition "Greedy runs successfully" $false -IsCritical $true
    $greedyObj = 0
}

# Test 2.2: Closest-Neighbor heuristic
Write-Info "Test 2.2: Testing Closest-Neighbor heuristic..."
try {
    $cnOutput = python src/closest_neighbor.py --instance data/test_tiny.json --seed 42 2>&1 | Out-String
    $cnObj = if ($cnOutput -match "Total demand covered: ([\d.]+)") { [double]$Matches[1] } else { 0 }
    Test-Condition "Closest-Neighbor runs successfully" ($cnObj -gt 100)
    Write-Info "  CN objective: $cnObj"
} catch {
    Test-Condition "Closest-Neighbor runs successfully" $false
}

# Test 2.3: Local Search
Write-Info "Test 2.3: Testing Local Search..."
try {
    $lsOutput = python src/local_search.py --instance data/test_tiny.json --seed 42 --max-moves 200 2>&1 | Out-String
    $lsObjMatch = $lsOutput -match "Final objective: ([\d.]+)"
    $lsObj = if ($lsObjMatch) { [double]$Matches[1] } else { 0 }
    Test-Condition "Local Search runs successfully" ($lsObj -gt 0)
    
    # Check non-degradation
    if ($greedyObj -gt 0) {
        Test-Condition "LS non-degradation (LS >= Greedy)" ($lsObj -ge ($greedyObj - 0.01))
    }
    Write-Info "  LS objective: $lsObj"
} catch {
    Test-Condition "Local Search runs successfully" $false
}

# Test 2.4: Multi-Start Local Search
Write-Info "Test 2.4: Testing Multi-Start LS..."
try {
    $msOutput = python src/multistart.py --instance data/test_tiny.json --n-starts 5 --seed 42 2>&1 | Out-String
    $msObjMatch = $msOutput -match "Best obj found:\s+([\d.]+)"
    $msObj = if ($msObjMatch) { [double]$Matches[1] } else { 0 }
    Test-Condition "Multi-Start LS runs successfully" ($msObj -gt 0)
    Write-Info "  Multi-Start best: $msObj"
} catch {
    Test-Condition "Multi-Start LS runs successfully" $false
}

# Test 2.5: Tabu Search (CRITICAL - THE FIX)
Write-Info "Test 2.5: Testing Tabu Search (checking for degradation bug)..."
try {
    $tsOutput = python src/tabu_search.py --instance data/test_tiny.json --seed 42 --tenure 10 --max-iterations 500 2>&1 | Out-String
    
    # Extract initial and final objectives
    $initMatch = $tsOutput -match "Initial objective: ([\d.]+)"
    $initObj = if ($initMatch) { [double]$Matches[1] } else { 0 }
    
    $finalMatch = $tsOutput -match "Best objective: ([\d.]+)"
    $finalObj = if ($finalMatch) { [double]$Matches[1] } else { 0 }
    
    Test-Condition "Tabu Search runs successfully" ($finalObj -gt 0) -IsCritical $true
    
    # CRITICAL TEST: TS should NOT degrade
    $noDegradation = $finalObj -ge ($initObj - 0.01)
    Test-Condition "TS non-degradation (TS >= initial Greedy)" $noDegradation -IsCritical $true
    
    if (-not $noDegradation) {
        Write-Fail "  CRITICAL: TS degraded from $initObj to $finalObj"
        Write-Fail "  The intensify() bug fix may not be applied correctly!"
        $script:criticalIssues += "TS degradation detected"
    } else {
        Write-Pass "  TS maintained/improved solution: $initObj -> $finalObj"
    }
    
    Write-Info "  TS initial: $initObj, TS best: $finalObj"
} catch {
    Test-Condition "Tabu Search runs successfully" $false -IsCritical $true
}

# ============================================================================
# STAGE 3: PIPELINE INTEGRATION
# ============================================================================
Write-Section "STAGE 3: Pipeline Integration"

# Test 3.1: run_mclp.py with single algorithm
Write-Info "Test 3.1: Testing pipeline with Greedy..."
try {
    rm results/test_pipeline.csv -ErrorAction SilentlyContinue
    $pipelineOutput = python src/run_mclp.py --instance data/test_tiny.json --algorithm greedy --seed 42 --output results/test_pipeline.csv 2>&1 | Out-Null
    Test-Condition "Pipeline runs successfully" (Test-Path results/test_pipeline.csv) -IsCritical $true
} catch {
    Test-Condition "Pipeline runs successfully" $false -IsCritical $true
}

# Test 3.2: CSV schema validation
Write-Info "Test 3.2: Validating CSV schema..."
if (Test-Path results/test_pipeline.csv) {
    $schemaScript = @"
import pandas as pd
df = pd.read_csv('results/test_pipeline.csv')
required = ['instance', 'seed', 'algorithm', 'objective', 'coverage_pct', 'runtime_sec', 'num_facilities', 'budget_used', 'facilities']
missing = [col for col in required if col not in df.columns]
print('PASS' if not missing else f'FAIL:{missing}')
"@
    
    try {
        $schemaCheck = python -c $schemaScript 2>&1
        Test-Condition "CSV schema valid" ($schemaCheck -match "PASS")
    } catch {
        Test-Condition "CSV schema valid" $false
    }
}

# Test 3.3: All algorithms through pipeline
Write-Info "Test 3.3: Testing all algorithms through pipeline..."
try {
    rm results/test_all_algos.csv -ErrorAction SilentlyContinue
    
    $allAlgosSuccess = $true
    foreach ($algo in @('greedy', 'cn', 'ls', 'ts')) {
        Write-Info "  Running $algo..."
        $null = python src/run_mclp.py --instance data/test_tiny.json --algorithm $algo --seed 42 --output results/test_all_algos.csv 2>&1
        if ($LASTEXITCODE -ne 0) {
            $allAlgosSuccess = $false
            Write-Fail "  $algo failed"
        }
    }
    
    Test-Condition "All 4 algorithms run through pipeline" $allAlgosSuccess -IsCritical $true
    
    if (Test-Path results/test_all_algos.csv) {
        $df = Import-Csv results/test_all_algos.csv
        Test-Condition "Pipeline produced 4 results (one per algorithm)" ($df.Count -eq 4)
    }
} catch {
    Test-Condition "All 4 algorithms run through pipeline" $false -IsCritical $true
}

# ============================================================================
# STAGE 4: DATASET VALIDATION
# ============================================================================
Write-Section "STAGE 4: Dataset Validation"

# Test 4.1: Check all 6 instances exist
Write-Info "Test 4.1: Checking dataset files..."
$instances = @('S1', 'S2', 'M1', 'M2', 'L1', 'L2')
foreach ($inst in $instances) {
    Test-Condition "Instance $inst.json exists" (Test-Path "data/$inst.json") -IsCritical $true
}

# Test 4.2: Validate each instance (no orphaned customers)
Write-Info "Test 4.2: Validating instance integrity..."
foreach ($inst in $instances) {
    if (Test-Path "data/$inst.json") {
        $validateScript = @"
import sys
sys.path.insert(0, 'src')
from instance_loader import MCLPInstance
inst = MCLPInstance('data/$inst.json')
orphaned = [j for j in inst.J if j not in inst.I_j or len(inst.I_j[j]) == 0]
print('PASS' if not orphaned else f'FAIL:{len(orphaned)}')
"@
        
        try {
            $validateOutput = python -c $validateScript 2>&1
            Test-Condition "Instance $inst has no orphaned customers" ($validateOutput -match "PASS") -IsCritical $true
        } catch {
            Test-Condition "Instance $inst has no orphaned customers" $false -IsCritical $true
        }
    }
}

# Test 4.3: Quick algorithm test on each instance
Write-Info "Test 4.3: Testing Greedy on all instances..."
rm results/dataset_validation.csv -ErrorAction SilentlyContinue

foreach ($inst in $instances) {
    if (Test-Path "data/$inst.json") {
        Write-Info "  Testing $inst..."
        try {
            $null = python src/run_mclp.py --instance "data/$inst.json" --algorithm greedy --seed 42 --output results/dataset_validation.csv 2>&1
            Test-Condition "$inst runs with Greedy" ($LASTEXITCODE -eq 0) -IsCritical $true
        } catch {
            Test-Condition "$inst runs with Greedy" $false -IsCritical $true
        }
    }
}

# ============================================================================
# STAGE 5: ALGORITHM PERFORMANCE VALIDATION
# ============================================================================
Write-Section "STAGE 5: Algorithm Performance Validation (This takes 2-3 min)"

# Test 5.1: Small-scale experiment (S1, all algorithms, 3 seeds)
Write-Info "Test 5.1: Running small-scale experiment on S1..."
rm results/perf_test.csv -ErrorAction SilentlyContinue

foreach ($seed in @(42, 43, 44)) {
    foreach ($algo in @('greedy', 'cn', 'ls', 'ts')) {
        Write-Info "  Running $algo (seed=$seed)..."
        try {
            $null = python src/run_mclp.py --instance data/S1.json --algorithm $algo --seed $seed --output results/perf_test.csv 2>&1
        } catch {
            Write-Warn "  Failed: $algo seed=$seed"
        }
    }
}

# Check if experiments completed
$perfTestExists = Test-Path results/perf_test.csv
Test-Condition "Small-scale experiment completed" $perfTestExists

# Test 5.2: Analyze performance hierarchy
Write-Info "Test 5.2: Validating algorithm performance hierarchy..."
if ($perfTestExists) {
    try {
        $perfData = Import-Csv results/perf_test.csv
        
        $greedyAvg = ($perfData | Where-Object {$_.algorithm -eq 'greedy'} | Measure-Object -Property objective -Average).Average
        $cnAvg = ($perfData | Where-Object {$_.algorithm -eq 'cn'} | Measure-Object -Property objective -Average).Average
        $lsAvg = ($perfData | Where-Object {$_.algorithm -eq 'ls'} | Measure-Object -Property objective -Average).Average
        $tsAvg = ($perfData | Where-Object {$_.algorithm -eq 'ts'} | Measure-Object -Property objective -Average).Average
        
        Write-Info "  Average objectives:"
        Write-Info "    Greedy: $([math]::Round($greedyAvg, 1))"
        Write-Info "    CN: $([math]::Round($cnAvg, 1))"
        Write-Info "    LS: $([math]::Round($lsAvg, 1))"
        Write-Info "    TS: $([math]::Round($tsAvg, 1))"
        
        # Expected: TS >= LS >= Greedy (generally)
        Test-Condition "LS >= Greedy (avg)" ($lsAvg -ge ($greedyAvg - 0.01))
        
        # CRITICAL: TS should be at least as good as Greedy
        $tsGood = $tsAvg -ge ($greedyAvg - 0.01)
        Test-Condition "TS >= Greedy (avg) - NO DEGRADATION" $tsGood -IsCritical $true
        
        if (-not $tsGood) {
            Write-Fail "  CRITICAL: TS performing worse than Greedy on average!"
            Write-Fail "  Greedy avg: $greedyAvg, TS avg: $tsAvg"
            $script:criticalIssues += "TS worse than Greedy in performance test"
        }
    } catch {
        Write-Warn "Could not analyze performance data: $_"
    }
}

# ============================================================================
# STAGE 6: TIMING VALIDATION
# ============================================================================
Write-Section "STAGE 6: Runtime Estimation"

Write-Info "Test 6.1: Measuring TS runtime on each size (this takes 1-2 min)..."
$timings = @{}

foreach ($inst in @('S1', 'M1', 'L1')) {
    Write-Info "  Timing $inst..."
    try {
        $start = Get-Date
        $null = python src/run_mclp.py --instance "data/$inst.json" --algorithm ts --seed 42 --output results/timing_test.csv 2>&1
        $elapsed = ((Get-Date) - $start).TotalSeconds
        $timings[$inst] = $elapsed
        Write-Info "    $inst TS runtime: $([math]::Round($elapsed, 2))s"
    } catch {
        Write-Warn "  Could not time $inst"
    }
}

# Estimate full experiment time
if ($timings.Count -eq 3) {
    $tsTimeEstimate = (2 * $timings['S1'] * 10) + (2 * $timings['M1'] * 10) + (2 * $timings['L1'] * 10) + (1 * 0.5 * 10)
    $totalEstimate = $tsTimeEstimate * 1.15
    
    $hours = [math]::Floor($totalEstimate / 3600)
    $minutes = [math]::Floor(($totalEstimate % 3600) / 60)
    
    Write-Info "`n  Estimated full experiment runtime: ${hours}h ${minutes}m"
    
    if ($totalEstimate -lt 600) {
        Write-Warn "  WARNING: Estimate is very fast (< 10 min)."
        Write-Warn "    TS max_iterations may be too low"
        $script:warnings++
    } elseif ($totalEstimate -gt 14400) {
        Write-Warn "  WARNING: Estimate is very long (> 4 hours)."
        $script:warnings++
    } else {
        Write-Pass "  Runtime estimate is reasonable (10 min - 4 hours)"
    }
}

# ============================================================================
# STAGE 7: PRE-FLIGHT CHECKLIST
# ============================================================================
Write-Section "STAGE 7: Pre-Flight Checklist"

Write-Info "Running final pre-flight checks..."

# Check disk space
$drive = (Get-Location).Drive
$freeSpaceGB = [math]::Round(($drive.Free / 1GB), 2)
Test-Condition "Sufficient disk space (> 1 GB)" ($freeSpaceGB -gt 1)
Write-Info "  Available: ${freeSpaceGB} GB"

# Verify results directory writable
try {
    "test" | Out-File results/writetest.tmp
    rm results/writetest.tmp
    Test-Condition "Results directory writable" $true
} catch {
    Test-Condition "Results directory writable" $false -IsCritical $true
}

# ============================================================================
# FINAL REPORT
# ============================================================================
Write-Section "DIAGNOSTIC COMPLETE - FINAL REPORT"

$endTime = Get-Date
$duration = $endTime - $startTime

Write-Host "`n================================================================" -ForegroundColor Cyan
Write-Host "                  DIAGNOSTIC SUMMARY" -ForegroundColor Cyan
Write-Host "================================================================" -ForegroundColor Cyan

Write-Host "`nTotal Tests Run: $script:totalTests" -ForegroundColor White
Write-Host "Passed: $script:passedTests" -ForegroundColor Green
Write-Host "Failed: $script:failedTests" -ForegroundColor Red
Write-Host "Warnings: $script:warnings" -ForegroundColor Yellow
Write-Host "Duration: $($duration.ToString('mm\:ss'))" -ForegroundColor White

if ($script:criticalIssues.Count -gt 0) {
    Write-Host "`nCRITICAL ISSUES DETECTED:" -ForegroundColor Red
    foreach ($issue in $script:criticalIssues) {
        Write-Host "  - $issue" -ForegroundColor Red
    }
    Write-Host "`nDO NOT PROCEED WITH FULL EXPERIMENTS!" -ForegroundColor Red
    Write-Host "Fix critical issues first!" -ForegroundColor Red
    exit 1
} elseif ($script:failedTests -gt 0) {
    Write-Host "`nSome tests failed, but no critical issues." -ForegroundColor Yellow
    Write-Host "Review failed tests and proceed with caution." -ForegroundColor Yellow
    exit 1
} else {
    Write-Host "`nALL TESTS PASSED!" -ForegroundColor Green
    Write-Host "Framework is ready for full experiments!" -ForegroundColor Green
    Write-Host "`nNext Steps:" -ForegroundColor Cyan
    Write-Host "  1. Review any warnings above" -ForegroundColor White
    Write-Host "  2. Run: .\run_full_experiments_production.ps1 -DryRun" -ForegroundColor White
    Write-Host "  3. Run: .\run_full_experiments_production.ps1" -ForegroundColor White
    Write-Host "  4. Monitor progress and wait for completion" -ForegroundColor White
    exit 0
}