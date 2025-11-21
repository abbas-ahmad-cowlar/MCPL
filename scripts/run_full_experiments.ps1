# Complete experiment protocol - PowerShell version
# Runs 1-5 from implementation plan

$ErrorActionPreference = "Stop"

Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "MCLP Full Experiment Protocol (PowerShell)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

# Configuration
$SEEDS = 42, 43, 44, 45, 46, 47, 48, 49, 50, 51  # 10 seeds
$INSTANCES = @(
    "data/test_tiny.json",
    "data/S1.json",
    "data/S2.json",
    "data/M1.json",
    "data/M2.json",
    "data/L1.json",
    "data/L2.json"
)
$OUTPUT_DIR = "results"
$TIMESTAMP = Get-Date -Format "yyyyMMdd_HHmmss"
$OUTPUT_FILE = "$OUTPUT_DIR/full_experiments_$TIMESTAMP.csv"
$CONFIG_FILE = "config.yaml"

# Create output directory
New-Item -ItemType Directory -Force -Path $OUTPUT_DIR | Out-Null

Write-Host "Configuration:" -ForegroundColor Yellow
Write-Host "  Config file: $CONFIG_FILE"
Write-Host "  Instances: $($INSTANCES.Count)"
Write-Host "  Seeds per config: $($SEEDS.Count)"
Write-Host "  Output: $OUTPUT_FILE"
Write-Host ""

# Check if all instances exist
Write-Host "Checking instance files..." -ForegroundColor Yellow
foreach ($instance in $INSTANCES) {
    if (Test-Path $instance) {
        Write-Host "  [OK] $instance" -ForegroundColor Green
    } else {
        Write-Host "  [MISSING] $instance" -ForegroundColor Red
        Write-Host "ERROR: Instance file missing. Run: bash scripts/generate_dataset.sh" -ForegroundColor Red
        exit 1
    }
}
Write-Host ""

# =============================================================================
# Run 1: Greedy vs Closest-Neighbor (10 seeds each)
# =============================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "RUN 1: Greedy vs Closest-Neighbor Comparison" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$run1_count = 0
foreach ($instance in $INSTANCES) {
    Write-Host "Processing $instance..." -ForegroundColor Yellow
    foreach ($seed in $SEEDS) {
        Write-Host "  Greedy (seed=$seed)"
        python src/run_mclp.py --instance $instance --algorithm greedy `
               --seed $seed --output $OUTPUT_FILE --log-level WARNING `
               --config $CONFIG_FILE
        $run1_count++
        
        Write-Host "  Closest-Neighbor (seed=$seed)"
        python src/run_mclp.py --instance $instance --algorithm cn `
               --seed $seed --output $OUTPUT_FILE --log-level WARNING `
               --config $CONFIG_FILE
        $run1_count++
    }
}

Write-Host "[OK] Run 1 complete ($run1_count experiments)" -ForegroundColor Green
Write-Host ""

# =============================================================================
# Run 2: Multi-Start LS (10 seeds each)
# =============================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "RUN 2: Multi-Start Local Search (N=20)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$run2_count = 0
foreach ($instance in $INSTANCES) {
    Write-Host "Processing $instance..." -ForegroundColor Yellow
    foreach ($seed in $SEEDS) {
        Write-Host "  Multi-Start LS (seed=$seed)"
        python src/run_mclp.py --instance $instance --algorithm ls `
               --seed $seed --output $OUTPUT_FILE --log-level WARNING `
               --config $CONFIG_FILE
        $run2_count++
    }
}

Write-Host "[OK] Run 2 complete ($run2_count experiments)" -ForegroundColor Green
Write-Host ""

# =============================================================================
# Run 3: Tabu Search (10 seeds each)
# =============================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "RUN 3: Tabu Search (T=10, I_freq=50, 2000 iter)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$run3_count = 0
foreach ($instance in $INSTANCES) {
    Write-Host "Processing $instance..." -ForegroundColor Yellow
    foreach ($seed in $SEEDS) {
        Write-Host "  Tabu Search (seed=$seed)"
        python src/run_mclp.py --instance $instance --algorithm ts `
               --seed $seed --output $OUTPUT_FILE --log-level WARNING `
               --config $CONFIG_FILE
        $run3_count++
    }
}

Write-Host "[OK] Run 3 complete ($run3_count experiments)" -ForegroundColor Green
Write-Host ""

# =============================================================================
# Run 4: TS Parameter Sensitivity (M1 only, 3 seeds)
# =============================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "RUN 4: Tabu Search Parameter Sensitivity" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$TENURE_VALUES = 7, 10, 15
$INTENS_FREQ_VALUES = 25, 50, 100
$PARAM_SEEDS = 42, 43, 44
$PARAM_INSTANCES = @("data/M1.json")

$run4_count = 0
foreach ($instance in $PARAM_INSTANCES) {
    Write-Host "Processing $instance for parameter sweep..." -ForegroundColor Yellow
    
    foreach ($tenure in $TENURE_VALUES) {
        foreach ($i_freq in $INTENS_FREQ_VALUES) {
            foreach ($seed in $PARAM_SEEDS) {
                Write-Host "  TS (T=$tenure, I_freq=$i_freq, seed=$seed)"
                
                # FIX: Use .Trim() to ensure no indentation in the YAML file
                $tempConfigContent = @"
instance:
  path: "$instance"
  format: "json"

seed: $seed

algorithms:
  - ts

ts_params:
  tenure: $tenure
  intensification_freq: $i_freq
  candidate_list_size: 20
  max_iterations: 15000
  stagnation_limit: 1000

results:
  output_csv: "$OUTPUT_FILE"

logging:
  level: "WARNING"
  output_dir: "logs/"
"@
                $tempConfigPath = "temp_config_${seed}_${tenure}_${i_freq}.yaml"
                # FIX: Use Set-Content explicitly to avoid encoding issues
                $tempConfigContent | Set-Content -Path $tempConfigPath -Encoding UTF8
                
                # FIX: Pass --instance explicitly so Python doesn't rely solely on the YAML path
                try {
                    python src/run_mclp.py --config $tempConfigPath --instance $instance --log-level ERROR
                } catch {
                    Write-Host "    [!] Crash detected, continuing..." -ForegroundColor Red
                }
                
                if (Test-Path $tempConfigPath) {
                    Remove-Item $tempConfigPath
                }
                $run4_count++
            }
        }
    }
}

Write-Host "[OK] Run 4 complete ($run4_count experiments)" -ForegroundColor Green
Write-Host ""


# =============================================================================
# Run 5: Full Method Comparison (single seed)
# =============================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "RUN 5: Complete Algorithm Comparison (single seed)" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan

$BASELINE_INSTANCES = @("data/test_tiny.json", "data/M1.json", "data/M2.json")
$BASELINE_SEED = 42

$run5_count = 0
foreach ($instance in $BASELINE_INSTANCES) {
    Write-Host "Processing $instance..." -ForegroundColor Yellow
    
    foreach ($algo in @("greedy", "cn", "ls", "ts")) {
        Write-Host "  $algo"
        python src/run_mclp.py --instance $instance --algorithm $algo `
               --seed $BASELINE_SEED --output $OUTPUT_FILE --log-level WARNING `
               --config $CONFIG_FILE
        $run5_count++
    }
}

Write-Host "[OK] Run 5 complete ($run5_count experiments)" -ForegroundColor Green
Write-Host ""

# =============================================================================
# Summary
# =============================================================================
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Experiment Protocol Complete!" -ForegroundColor Cyan
Write-Host "======================================================================" -ForegroundColor Cyan
Write-Host "Results saved to: $OUTPUT_FILE" -ForegroundColor Green
Write-Host ""

# Count experiments
$totalRuns = $run1_count + $run2_count + $run3_count + $run4_count + $run5_count
Write-Host "Experiment counts:" -ForegroundColor Yellow
Write-Host "  Run 1 (Greedy/CN): $run1_count"
Write-Host "  Run 2 (LS): $run2_count"
Write-Host "  Run 3 (TS): $run3_count"
Write-Host "  Run 4 (Param sweep): $run4_count"
Write-Host "  Run 5 (Baseline): $run5_count"
Write-Host "  Total: $totalRuns"
Write-Host ""

# Try to show summary (requires pandas)
Write-Host "Checking results file..." -ForegroundColor Yellow
if (Test-Path $OUTPUT_FILE) {
    $lineCount = (Get-Content $OUTPUT_FILE | Measure-Object -Line).Lines
    Write-Host "  Rows in CSV: $lineCount (including header)" -ForegroundColor Green
    
    # Try pandas summary if available
    try {
        python -c @"
import pandas as pd
df = pd.read_csv('$OUTPUT_FILE')
print('\nBy algorithm:')
print(df['algorithm'].value_counts())
print('\nBy instance:')
print(df['instance'].value_counts())
"@
    } catch {
        Write-Host "  (Install pandas for detailed summary: pip install pandas)" -ForegroundColor Gray
    }
} else {
    Write-Host "  ERROR: Output file not found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Analyze results:"
Write-Host "     python scripts/analyze_results.py --input $OUTPUT_FILE"
Write-Host ""
Write-Host "  2. Generate plots:"
Write-Host "     python scripts/plot_convergence.py --input $OUTPUT_FILE"