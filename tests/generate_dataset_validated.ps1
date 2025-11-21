# Validated Dataset Generation
$ErrorActionPreference = "Stop"

Write-Host "======================================================================"
Write-Host "Generating Validated MCLP Dataset"
Write-Host "======================================================================"

$instances = @(
    @{Name="S1"; I=50; J=200; B=10; R=7.0; Seed=44},
    @{Name="S2"; I=50; J=200; B=10; R=7.0; Seed=43},
    @{Name="M1"; I=100; J=500; B=15; R=6.5; Seed=42},
    @{Name="M2"; I=100; J=500; B=20; R=6.5; Seed=43},
    @{Name="L1"; I=200; J=1000; B=20; R=5.5; Seed=42},
    @{Name="L2"; I=200; J=1000; B=30; R=5.0; Seed=43}
)

$failed = @()

foreach ($inst in $instances) {
    Write-Host "`nGenerating $($inst.Name)..." -ForegroundColor Cyan
    
    $output = "data/$($inst.Name).json"
    
    python scripts/generate_instance.py `
        --I $inst.I `
        --J $inst.J `
        --B $inst.B `
        --radius $inst.R `
        --seed $inst.Seed `
        -o $output `
        --validate
    
    if ($LASTEXITCODE -ne 0) {
        Write-Host "[FAIL] $($inst.Name) generation failed" -ForegroundColor Red
        $failed += $inst.Name
        continue
    }
    
    # Verify no uncovered customers
    $content = Get-Content $output | ConvertFrom-Json
    $uncovered = 0
    foreach ($j in $content.J) {
        if (-not $content.I_j.$j -or $content.I_j.$j.Count -eq 0) {
            $uncovered++
        }
    }
    
    if ($uncovered -gt 0) {
        Write-Host "[FAIL] $($inst.Name) has $uncovered uncovered customers" -ForegroundColor Red
        $failed += $inst.Name
    } else {
        Write-Host "[OK] $($inst.Name) validated successfully" -ForegroundColor Green
    }
}

Write-Host "`n======================================================================"
if ($failed.Count -eq 0) {
    Write-Host "All instances generated successfully!" -ForegroundColor Green
} else {
    Write-Host "Failed instances: $($failed -join ', ')" -ForegroundColor Red
    exit 1
}