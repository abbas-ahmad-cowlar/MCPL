# Parse benchmark results for COMPLETE dataset suite
$resultsDir = "results_complete"

$results = @()

if (-not (Test-Path $resultsDir)) {
    Write-Error "Results directory not found: $resultsDir"
    exit 1
}

$files = Get-ChildItem "$resultsDir\*.txt"
foreach ($file in $files) {
    # Skip error files or ascii temp files
    if ($file.Name -match "_error" -or $file.Name -match "_ascii") { continue }

    # Parse filename for dataset and algorithm
    if ($file.Name -match "(.+)_(.+)\.txt") {
        $dataset = $matches[1]
        $algorithm = $matches[2]
        
        # Read content as single string
        $content = [System.IO.File]::ReadAllText($file.FullName)
        
        # Extract metrics using regex
        $objective = "N/A"
        $runtime = "N/A"
        
        # Try to find objective value
        if ($content -match "Covered demand:\s+([\d\.]+)") { $objective = $matches[1] }
        elseif ($content -match "Final objective:\s+([\d\.]+)") { $objective = $matches[1] }
        elseif ($content -match "Total demand covered:\s+([\d\.]+)") { $objective = $matches[1] }
        elseif ($content -match "Objective:\s+([\d\.]+)") { $objective = $matches[1] }
        
        # Try to find runtime
        if ($content -match "Solve time:\s+([\d\.]+)") { $runtime = $matches[1] }
        elseif ($content -match "Runtime:\s+([\d\.]+)") { $runtime = $matches[1] }
        
        $results += [PSCustomObject]@{
            Dataset   = $dataset
            Algorithm = $algorithm
            Objective = $objective
            Runtime   = $runtime
        }
    }
}

# Print CSV to console
$results | Sort-Object Dataset, Algorithm | ConvertTo-Csv -NoTypeInformation
