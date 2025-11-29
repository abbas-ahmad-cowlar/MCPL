# LaTeX Compilation Requirements

To automatically compile `SCIENTIFIC_REPORT.tex` to PDF, you need a LaTeX distribution installed.

## Required LaTeX Distribution

Choose one of the following:

### Option 1: MiKTeX (Windows - Recommended)
- **Download**: https://miktex.org/download
- **Installation**: Run the installer, it will automatically install packages as needed
- **Verify**: Open PowerShell and run `pdflatex --version`

### Option 2: TeX Live (Cross-platform)
- **Download**: https://www.tug.org/texlive/
- **Installation**: Follow the installer instructions
- **Verify**: Open terminal and run `pdflatex --version`

### Option 3: Overleaf (Online - No Installation)
- **Website**: https://www.overleaf.com
- **Usage**: Upload `SCIENTIFIC_REPORT.tex` and compile online
- **Note**: Cannot be automated with the workflow script

## Required LaTeX Packages

The report uses the following packages (usually included in standard distributions):

- `amsmath`, `amssymb`, `amsthm` - Mathematical typesetting
- `graphicx` - Image inclusion
- `booktabs` - Professional tables
- `array` - Extended array and tabular environments
- `algorithm`, `algpseudocode` - Algorithm pseudocode
- `listings` - Code listings
- `xcolor` - Colors
- `hyperref` - Hyperlinks
- `cite` - Citations
- `caption`, `subcaption` - Captions
- `multirow` - Multi-row table cells
- `geometry` - Page layout

Most LaTeX distributions will automatically install missing packages when you compile.

## Compilation Command

Manual compilation:
```bash
pdflatex SCIENTIFIC_REPORT.tex
pdflatex SCIENTIFIC_REPORT.tex  # Run twice for references
```

Or use the workflow script:
```powershell
.\run_complete_workflow.ps1 -CompileReport
```

## Troubleshooting

### "pdflatex not found"
- Ensure LaTeX distribution is installed
- Add LaTeX bin directory to PATH
- Restart PowerShell/terminal after installation

### Missing packages
- MiKTeX: Packages install automatically on first use
- TeX Live: Use `tlmgr install <package>` to install manually

### Compilation errors
- Check LaTeX log file (`SCIENTIFIC_REPORT.log`)
- Ensure all figure files exist in `figures/` directory
- Verify all `.dat` files are referenced correctly

