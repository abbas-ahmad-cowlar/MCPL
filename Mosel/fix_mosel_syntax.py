#!/usr/bin/env python3
"""
Fix Mosel Syntax Errors

This script fixes Python-style string multiplication syntax in Mosel files.
Mosel doesn't support "="*70, so we replace it with actual repeated strings.

Usage:
    python fix_mosel_syntax.py
"""

import re
import os
from pathlib import Path

def fix_string_multiplication(content):
    """Replace Python-style string multiplication with actual repeated strings."""
    
    # Pattern to match: "X"*N where X is a character and N is a number
    pattern = r'"([^"]+)"\s*\*\s*(\d+)'
    
    def replace_func(match):
        char = match.group(1)
        count = int(match.group(2))
        # Create the repeated string
        repeated = char * count
        return f'"{repeated}"'
    
    # Replace all occurrences
    fixed_content = re.sub(pattern, replace_func, content)
    return fixed_content

def fix_mosel_file(filepath):
    """Fix syntax errors in a single Mosel file."""
    print(f"Processing: {filepath}")
    
    # Read the file
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Fix string multiplication
    fixed_content = fix_string_multiplication(content)
    
    # Check if any changes were made
    if content != fixed_content:
        # Write back the fixed content
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(fixed_content)
        print(f"  ✓ Fixed")
        return True
    else:
        print(f"  - No changes needed")
        return False

def main():
    """Fix all Mosel files in the src directory."""
    print("=" * 70)
    print("MOSEL SYNTAX FIXER")
    print("=" * 70)
    print()
    
    src_dir = Path("src")
    if not src_dir.exists():
        print("ERROR: src/ directory not found")
        print("Please run this script from the mosel/ directory")
        return 1
    
    # Find all .mos files
    mos_files = list(src_dir.glob("*.mos"))
    
    if not mos_files:
        print("No .mos files found in src/")
        return 1
    
    print(f"Found {len(mos_files)} Mosel files")
    print()
    
    # Fix each file
    fixed_count = 0
    for mos_file in sorted(mos_files):
        if fix_mosel_file(mos_file):
            fixed_count += 1
    
    print()
    print("=" * 70)
    print(f"SUMMARY: Fixed {fixed_count} / {len(mos_files)} files")
    print("=" * 70)
    print()
    print("All Mosel files are now ready to run!")
    print()
    
    return 0

if __name__ == "__main__":
    exit(main())
