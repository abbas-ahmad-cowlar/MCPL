# Fresh MiKTeX Installation Script
# This script installs MiKTeX using winget (Windows 10/11) or provides manual instructions

param(
    [switch]$UseWinget = $true,
    [switch]$UseChocolatey = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Fresh MiKTeX Installation" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
$pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
if ($pdflatex) {
    Write-Host "[INFO] LaTeX (pdflatex) is already installed!" -ForegroundColor Green
    Write-Host "Location: $($pdflatex.Source)" -ForegroundColor Gray
    $version = & pdflatex --version 2>&1 | Select-Object -First 1
    Write-Host "Version: $version" -ForegroundColor Gray
    Write-Host ""
    $response = Read-Host "Reinstall anyway? (y/n)"
    if ($response -ne 'y') {
        Write-Host "Installation cancelled." -ForegroundColor Yellow
        exit 0
    }
}

Write-Host "Installation Method: " -NoNewline
if ($UseWinget) {
    Write-Host "winget (Windows Package Manager)" -ForegroundColor Cyan
} elseif ($UseChocolatey) {
    Write-Host "Chocolatey" -ForegroundColor Cyan
} else {
    Write-Host "Manual Download" -ForegroundColor Cyan
}
Write-Host ""

# Method 1: winget
if ($UseWinget) {
    Write-Host "Step 1: Checking for winget..." -ForegroundColor Yellow
    $winget = Get-Command winget -ErrorAction SilentlyContinue
    if ($winget) {
        Write-Host "  [OK] winget is available" -ForegroundColor Green
        Write-Host ""
        Write-Host "Step 2: Installing MiKTeX via winget..." -ForegroundColor Yellow
        Write-Host "  This may take several minutes..." -ForegroundColor Gray
        Write-Host ""
        
        try {
            & winget install --id MiKTeX.MiKTeX --accept-package-agreements --accept-source-agreements
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "[SUCCESS] MiKTeX installed successfully!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Step 3: Verifying installation..." -ForegroundColor Yellow
                Start-Sleep -Seconds 3
                
                # Refresh PATH
                $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")
                
                $pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
                if ($pdflatex) {
                    Write-Host "  [OK] pdflatex is now available!" -ForegroundColor Green
                    $version = & pdflatex --version 2>&1 | Select-Object -First 1
                    Write-Host "  Version: $version" -ForegroundColor Gray
                } else {
                    Write-Host "  [WARNING] pdflatex not found in PATH yet" -ForegroundColor Yellow
                    Write-Host "  Please restart PowerShell and run: pdflatex --version" -ForegroundColor Gray
                }
            } else {
                Write-Host ""
                Write-Host "[ERROR] Installation failed with exit code: $LASTEXITCODE" -ForegroundColor Red
                Write-Host "Trying alternative method..." -ForegroundColor Yellow
                $UseWinget = $false
            }
        } catch {
            Write-Host ""
            Write-Host "[ERROR] winget installation failed: $_" -ForegroundColor Red
            Write-Host "Trying alternative method..." -ForegroundColor Yellow
            $UseWinget = $false
        }
    } else {
        Write-Host "  [NOT FOUND] winget is not available" -ForegroundColor Yellow
        Write-Host "  Trying alternative method..." -ForegroundColor Yellow
        $UseWinget = $false
    }
}

# Method 2: Chocolatey
if (-not $UseWinget -and $UseChocolatey) {
    Write-Host ""
    Write-Host "Step 1: Checking for Chocolatey..." -ForegroundColor Yellow
    $choco = Get-Command choco -ErrorAction SilentlyContinue
    if ($choco) {
        Write-Host "  [OK] Chocolatey is available" -ForegroundColor Green
        Write-Host ""
        Write-Host "Step 2: Installing MiKTeX via Chocolatey..." -ForegroundColor Yellow
        Write-Host "  This may take several minutes..." -ForegroundColor Gray
        Write-Host ""
        
        try {
            & choco install miktex -y
            if ($LASTEXITCODE -eq 0) {
                Write-Host ""
                Write-Host "[SUCCESS] MiKTeX installed successfully!" -ForegroundColor Green
                Write-Host ""
                Write-Host "Please restart PowerShell and verify with: pdflatex --version" -ForegroundColor Yellow
            } else {
                Write-Host ""
                Write-Host "[ERROR] Chocolatey installation failed" -ForegroundColor Red
                Write-Host "Please install manually (see instructions below)" -ForegroundColor Yellow
            }
        } catch {
            Write-Host ""
            Write-Host "[ERROR] Chocolatey installation failed: $_" -ForegroundColor Red
            Write-Host "Please install manually (see instructions below)" -ForegroundColor Yellow
        }
    } else {
        Write-Host "  [NOT FOUND] Chocolatey is not available" -ForegroundColor Yellow
        Write-Host "  Please install manually (see instructions below)" -ForegroundColor Yellow
    }
}

# Method 3: Manual installation instructions
if (-not $UseWinget -and -not $UseChocolatey) {
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "Manual Installation Instructions" -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "1. Download MiKTeX installer:" -ForegroundColor Yellow
    Write-Host "   https://miktex.org/download" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "2. Run the installer and follow these steps:" -ForegroundColor Yellow
    Write-Host "   - Choose 'Install for all users' (requires admin) OR 'Install for current user'" -ForegroundColor Gray
    Write-Host "   - Select installation directory (default is fine)" -ForegroundColor Gray
    Write-Host "   - IMPORTANT: Check 'Add MiKTeX to PATH' option" -ForegroundColor Yellow
    Write-Host "   - Complete the installation" -ForegroundColor Gray
    Write-Host ""
    Write-Host "3. After installation:" -ForegroundColor Yellow
    Write-Host "   - Restart PowerShell" -ForegroundColor Gray
    Write-Host "   - Verify with: pdflatex --version" -ForegroundColor Gray
    Write-Host ""
    Write-Host "4. If pdflatex is still not found:" -ForegroundColor Yellow
    Write-Host "   - Add MiKTeX bin directory to PATH manually:" -ForegroundColor Gray
    Write-Host "     Usually: C:\Program Files\MiKTeX\miktex\bin\x64" -ForegroundColor Gray
    Write-Host "   - Or: C:\Users\$env:USERNAME\AppData\Local\Programs\MiKTeX\miktex\bin\x64" -ForegroundColor Gray
    Write-Host ""
}

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Installation Complete!" -ForegroundColor Green
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "  1. Restart PowerShell (if not already done)" -ForegroundColor Gray
Write-Host "  2. Verify installation: pdflatex --version" -ForegroundColor Gray
Write-Host "  3. Test PDF compilation: .\run_complete_workflow.ps1 -CompileReport" -ForegroundColor Gray
Write-Host ""
