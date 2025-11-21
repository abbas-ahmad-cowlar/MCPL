# Mosel Environment Setup Guide

This guide walks through setting up FICO Xpress Mosel for MCLP implementation.

## 📋 Table of Contents

1. [Prerequisites](#prerequisites)
2. [Installing FICO Xpress](#installing-fico-xpress)
3. [Verifying Installation](#verifying-installation)
4. [Python Environment Setup](#python-environment-setup)
5. [Directory Structure Setup](#directory-structure-setup)
6. [Troubleshooting](#troubleshooting)

---

## 1. Prerequisites

### System Requirements

- **Operating System**: Windows, Linux, or macOS
- **RAM**: Minimum 4GB (8GB+ recommended for large instances)
- **Disk Space**: ~2GB for FICO Xpress installation
- **Python**: 3.8 or higher (for utilities)

### Required Software

1. **FICO Xpress Mosel** compiler
2. **FICO Xpress Optimizer** (MIP solver)
3. **Valid FICO Xpress License** (community, academic, or commercial)

---

## 2. Installing FICO Xpress

### Option A: Community License (Free)

1. **Download FICO Xpress Community Edition**
   - Visit: https://content.fico.com/xpress-optimization-community-license
   - Register for free community license (limited to smaller problem sizes)
   - Download installer for your platform

2. **Install Xpress**
   ```bash
   # Linux/macOS
   chmod +x xpress_installer.sh
   ./xpress_installer.sh

   # Windows
   # Run the .exe installer as Administrator
   ```

3. **Activate License**
   ```bash
   # Set environment variable with license path
   export XPRESSDIR=/opt/xpressmp  # Linux/macOS
   # or
   set XPRESSDIR=C:\xpressmp       # Windows

   # Add to PATH
   export PATH=$XPRESSDIR/bin:$PATH
   ```

### Option B: Academic License

1. Contact FICO Academic Relations for full-featured academic license
2. Provides unlimited problem size for research/teaching
3. Follow installation instructions provided with academic license

### Option C: Commercial License

1. Purchase commercial license from FICO
2. Follow enterprise installation guide

---

## 3. Verifying Installation

### Test Mosel Compiler

```bash
# Check Mosel version
mosel --version

# Expected output:
# FICO Xpress Mosel v5.x.x
```

### Test Optimizer

```bash
# Check optimizer license
mosel -c "uses 'mmxprs'; exit"

# Should complete without license errors
```

### Run Hello World Example

Create `test.mos`:

```mosel
model "HelloWorld"
  writeln("Hello from Mosel!")
end-model
```

Compile and run:

```bash
mosel test.mos
mosel exec test.bim

# Expected output: Hello from Mosel!
```

### Test MIP Solver

Create `test_mip.mos`:

```mosel
model "TestMIP"
  uses "mmxprs"

  declarations
    x, y: mpvar
  end-declarations

  ! Simple LP: maximize x + y subject to x + y <= 10, x,y >= 0
  Objective := x + y
  x + y <= 10
  x >= 0
  y >= 0

  maximize(Objective)

  writeln("Objective value: ", getobjval)
  writeln("x = ", getsol(x), ", y = ", getsol(y))
end-model
```

Run:

```bash
mosel test_mip.mos
mosel exec test_mip.bim

# Expected output:
# Objective value: 10
# x = 5, y = 5 (or any optimal solution)
```

---

## 4. Python Environment Setup

The data conversion utility requires Python 3.8+.

### Install Python Dependencies

```bash
# Navigate to project root
cd /path/to/MCPL

# Install requirements (if not already done)
pip install -r requirements.txt

# For conversion utility specifically, only json and pathlib needed (built-in)
```

### Test Conversion Utility

```bash
# Navigate to Mosel directory
cd Mosel

# Test conversion
python utilities/convert_json_to_mosel.py --input ../data/test_tiny.json --output data/

# Expected output:
# Loading: ../data/test_tiny.json
# ✓ Loaded instance: test_tiny
# ...
# ✓ Saved: data/test_tiny.dat
```

---

## 5. Directory Structure Setup

Ensure the following directory structure exists:

```bash
# Navigate to project root
cd /path/to/MCPL

# Verify Mosel directory structure
ls -l Mosel/

# Should show:
# data/           - Converted .dat instance files
# docs/           - Documentation
# pseudocode/     - Algorithm pseudocode
# results/        - Experimental results
# src/            - Mosel source code (.mos files)
# utilities/      - Conversion scripts
# README.md       - Main documentation
```

If any directories are missing:

```bash
mkdir -p Mosel/{data,docs,pseudocode,results,src,utilities}
```

---

## 6. Troubleshooting

### Issue: "mosel: command not found"

**Solution**: Add Mosel to PATH

```bash
# Linux/macOS
export XPRESSDIR=/opt/xpressmp
export PATH=$XPRESSDIR/bin:$PATH

# Add to ~/.bashrc or ~/.zshrc for persistence
echo 'export XPRESSDIR=/opt/xpressmp' >> ~/.bashrc
echo 'export PATH=$XPRESSDIR/bin:$PATH' >> ~/.bashrc
source ~/.bashrc
```

```cmd
REM Windows (Command Prompt)
set XPRESSDIR=C:\xpressmp
set PATH=%XPRESSDIR%\bin;%PATH%

REM Add to system environment variables for persistence
```

### Issue: License errors when running models

**Symptoms**:
```
ERROR: No valid license found
ERROR: Cannot load optimizer library
```

**Solutions**:

1. **Check license file**:
   ```bash
   # Linux/macOS
   ls $XPRESSDIR/bin/xpauth.xpr

   # Windows
   dir %XPRESSDIR%\bin\xpauth.xpr
   ```

2. **Verify license environment variable**:
   ```bash
   echo $XPRSLICPATH  # Linux/macOS
   echo %XPRSLICPATH% # Windows
   ```

3. **Community license limitations**:
   - Maximum 5,000 variables and 5,000 constraints
   - If exceeded, upgrade to academic/commercial license

4. **Activate license**:
   ```bash
   # Use slactivate utility (if provided)
   slactivate -a <license_code>
   ```

### Issue: "mmxprs module not found"

**Solution**: Ensure Xpress Optimizer is installed (not just Mosel compiler)

```bash
# Verify optimizer installation
ls $XPRESSDIR/lib/libxprs*  # Linux/macOS
dir %XPRESSDIR%\lib\xprs*   # Windows
```

If missing, reinstall FICO Xpress with Optimizer component enabled.

### Issue: Python conversion script fails

**Common causes**:

1. **File not found**: Verify input file path
   ```bash
   ls ../data/test_tiny.json
   ```

2. **Invalid JSON**: Validate JSON syntax
   ```bash
   python -m json.tool ../data/test_tiny.json
   ```

3. **Permission denied**: Check write permissions on output directory
   ```bash
   chmod +w Mosel/data/
   ```

---

## ✅ Verification Checklist

Before proceeding to Phase 2 implementation, verify:

- [ ] Mosel compiler installed and accessible (`mosel --version` works)
- [ ] Xpress Optimizer licensed (`mosel -c "uses 'mmxprs'; exit"` succeeds)
- [ ] Test MIP model compiles and solves
- [ ] Python 3.8+ installed
- [ ] Data conversion utility successfully converts all 7 instances
- [ ] All `.dat` files present in `Mosel/data/` directory
- [ ] Directory structure complete

---

## 📚 Additional Resources

### Official Documentation

- **Mosel Language Reference**: https://www.fico.com/en/products/fico-xpress-mosel
- **Xpress Optimizer**: https://www.fico.com/en/products/fico-xpress-solver
- **Mosel Tutorial**: Included in Xpress installation (`$XPRESSDIR/docs/`)

### Community Support

- **FICO Community Forum**: https://community.fico.com/
- **Stack Overflow**: Tag `xpress` or `mosel`

### Example Code

- Xpress installation includes example models: `$XPRESSDIR/examples/`
- Facility location examples: Look for `facility*.mos` or `location*.mos`

---

## 🎯 Next Steps

Once environment is set up and verified:

1. **Read data format specification**: [DATA_FORMAT.md](DATA_FORMAT.md)
2. **Review Phase 1 completion report**: [PHASE1_COMPLETION.md](PHASE1_COMPLETION.md)
3. **Proceed to Phase 2**: Implement exact MIP model (`src/mclp_exact.mos`)

---

**Updated**: November 21, 2025
**Author**: MCLP Migration Team
