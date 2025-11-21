import os
import glob

# Unicode replacements
replacements = {
    '[OK]': '[OK]',
    '[DONE]': '[DONE]',
    '[FAIL]': '[FAIL]',
    '[WARN]': '[WARN]',
    '[*]': '[*]',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
    '': '',
}

# Files to process
file_patterns = [
    'src/*.py',
    'tests/*.py',
    'scripts/*.py'
]

files_to_fix = []
for pattern in file_patterns:
    files_to_fix.extend(glob.glob(pattern))

for filepath in files_to_fix:
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
        
        original = content
        for old, new in replacements.items():
            content = content.replace(old, new)
        
        if content != original:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Fixed: {filepath}")
        else:
            print(f"No changes: {filepath}")
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

print("\nDone! All Unicode symbols replaced with ASCII.")