# LaTeX Installation Helper Script for Windows
# This script helps install MiKTeX (recommended for Windows)

param(
    [switch]$AutoInstall = $false
)

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "LaTeX Installation Helper" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Check if already installed
$pdflatex = Get-Command pdflatex -ErrorAction SilentlyContinue
if ($pdflatex) {
    Write-Host "[OK] LaTeX is already installed!" -ForegroundColor Green
    Write-Host "Location: $($pdflatex.Source)" -ForegroundColor Gray
    $version = & pdflatex --version 2>&1 | Select-Object -First 1
    Write-Host "Version: $version" -ForegroundColor Gray
    exit 0
}

Write-Host "[INFO] LaTeX (pdflatex) is not installed." -ForegroundColor Yellow
Write-Host ""

# Check for MiKTeX in common locations
$miktexPaths = @(
    "C:\Program Files\MiKTeX",
    "C:\Program Files (x86)\MiKTeX",
    "$env:ProgramFiles\MiKTeX",
    "$env:ProgramFiles(x86)\MiKTeX"
)

$miktexFound = $false
foreach ($path in $miktexPaths) {
    if (Test-Path $path) {
        Write-Host "[FOUND] MiKTeX installation at: $path" -ForegroundColor Green
        Write-Host "       But pdflatex is not in PATH." -ForegroundColor Yellow
        Write-Host "       You may need to add it to PATH or restart your terminal." -ForegroundColor Yellow
        $miktexFound = $true
        break
    }
}

if (-not $miktexFound) {
    Write-Host "Installation Options:" -ForegroundColor Cyan
    Write-Host ""
    Write-Host "Option 1: Download and Install MiKTeX (Recommended for Windows)" -ForegroundColor Yellow
    Write-Host "  1. Visit: https://miktex.org/download" -ForegroundColor Gray
    Write-Host "  2. Download the Windows installer" -ForegroundColor Gray
    Write-Host "  3. Run the installer and follow the prompts" -ForegroundColor Gray
    Write-Host "  4. Restart PowerShell after installation" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 2: Use Chocolatey (if installed)" -ForegroundColor Yellow
    Write-Host "  choco install miktex" -ForegroundColor Gray
    Write-Host ""
    Write-Host "Option 3: Use winget (Windows 10/11)" -ForegroundColor Yellow
    Write-Host "  winget install MiKTeX.MiKTeX" -ForegroundColor Gray
    Write-Host ""
    
    if ($AutoInstall) {
        Write-Host "Attempting automatic installation with winget..." -ForegroundColor Cyan
        $winget = Get-Command winget -ErrorAction SilentlyContinue
        if ($winget) {
            Write-Host "Installing MiKTeX via winget..." -ForegroundColor Yellow
            & winget install MiKTeX.MiKTeX --accept-package-agreements --accept-source-agreements
            if ($LASTEXITCODE -eq 0) {
                Write-Host "[SUCCESS] MiKTeX installed! Please restart PowerShell." -ForegroundColor Green
            } else {
                Write-Host "[FAILED] Automatic installation failed. Please install manually." -ForegroundColor Red
            }
        } else {
            Write-Host "[INFO] winget not available. Please install manually." -ForegroundColor Yellow
        }
    } else {
        Write-Host "To attempt automatic installation, run:" -ForegroundColor Cyan
        Write-Host "  .\install_latex.ps1 -AutoInstall" -ForegroundColor Gray
    }
}

Write-Host ""
Write-Host "After installation, verify with:" -ForegroundColor Cyan
Write-Host "  pdflatex --version" -ForegroundColor Gray
Write-Host ""

