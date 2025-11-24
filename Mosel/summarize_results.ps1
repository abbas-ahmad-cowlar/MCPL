# Parse benchmark results and generate summary CSV
$resultsDir = "results_full"
$outputCsv = "benchmark_summary.csv"

$results = @()

$files = Get-ChildItem "$resultsDir\*.txt"
foreach ($file in $files) {
    # Parse filename for dataset and algorithm
    if ($file.Name -match "(.+)_(.+)\.txt") {
        $dataset = $matches[1]
        $algorithm = $matches[2]
        
        # Read content as single string to handle multiline matching if needed
        # Force reading as text to avoid encoding issues
        $content = [System.IO.File]::ReadAllText($file.FullName)
        
        # Extract metrics using regex
        $objective = "N/A"
        $runtime = "N/A"
        $budget = "N/A"
        $covered = "N/A"
        
        # Try to find objective value (prioritize "Covered demand" or "Final objective")
        if ($content -match "Covered demand:\s+([\d\.]+)") { $objective = $matches[1] }
        elseif ($content -match "Final objective:\s+([\d\.]+)") { $objective = $matches[1] }
        elseif ($content -match "Total demand covered:\s+([\d\.]+)") { $objective = $matches[1] }
        elseif ($content -match "Objective:\s+([\d\.]+)") { $objective = $matches[1] }
        
        # Try to find runtime
        if ($content -match "Solve time:\s+([\d\.]+)") { $runtime = $matches[1] }
        elseif ($content -match "Runtime:\s+([\d\.]+)") { $runtime = $matches[1] }
        
        # Try to find budget used
        if ($content -match "Budget used:\s+([\d\.]+)") { $budget = $matches[1] }
        
        # Try to find covered customers
        if ($content -match "Covered customers:\s+(\d+)") { $covered = $matches[1] }
        
        $results += [PSCustomObject]@{
            Dataset          = $dataset
            Algorithm        = $algorithm
            Objective        = $objective
            Runtime          = $runtime
            BudgetUsed       = $budget
            CoveredCustomers = $covered
        }
    }
}

# Export to CSV
$results | Export-Csv -Path $outputCsv -NoTypeInformation
Write-Host "Summary saved to $outputCsv"

# Print table to console
$results | Sort-Object Dataset, Algorithm | Format-Table -AutoSize
