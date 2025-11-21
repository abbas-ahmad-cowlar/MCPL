"""
Integration tests for Phase 4: Full pipeline.
"""

import sys
import os
import subprocess
import pandas as pd

sys.path.insert(0, 'src')

def test_pipeline_determinism():
    """Test that same seed produces identical results."""
    output_file = "results/test_determinism.csv"
    
    # Clean previous results
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Run twice with same seed
    for run in range(2):
        result = subprocess.run([
            sys.executable, 'src/run_mclp.py',
            '--instance', 'data/test_tiny.json',
            '--algorithm', 'ts',
            '--seed', '42',
            '--output', output_file
        ], capture_output=True, text=True)
        
        if result.returncode != 0:
            print(f"[FAIL] Run {run+1} failed!")
            print(f"STDOUT: {result.stdout}")
            print(f"STDERR: {result.stderr}")
            raise Exception(f"Pipeline failed: {result.stderr}")
    
    # Load results
    df = pd.read_csv(output_file)
    
    assert len(df) == 2, "Should have exactly 2 runs"
    
    # Check objectives match
    obj1, obj2 = df['objective'].values
    assert abs(obj1 - obj2) < 0.01, f"Objectives don't match: {obj1} vs {obj2}"
    
    # Check facilities match
    fac1, fac2 = df['facilities'].values
    assert fac1 == fac2, f"Facilities don't match: {fac1} vs {fac2}"
    
    print(f"[OK] Determinism test passed (obj={obj1:.2f})")
    
    # Cleanup
    os.remove(output_file)



def test_all_algorithms_executable():
    """Test that all algorithms run without errors."""
    output_file = "results/test_all_algos.csv"
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    algorithms = ['greedy', 'cn', 'ls', 'ts']
    
    for algo in algorithms:
        print(f"Testing {algo}...")
        result = subprocess.run([
            sys.executable, 'src/run_mclp.py',
            '--instance', 'data/test_tiny.json',
            '--algorithm', algo,
            '--seed', '42',
            '--output', output_file
        ], capture_output=True, text=True)
        
        assert result.returncode == 0, f"{algo} failed: {result.stderr}"
    
    # Verify all results recorded
    df = pd.read_csv(output_file)
    assert len(df) == len(algorithms), f"Expected {len(algorithms)} results, got {len(df)}"
    
    print(f"[OK] All algorithms executable ({len(algorithms)} tested)")
    
    # Cleanup
    os.remove(output_file)


def test_csv_schema():
    """Test that output CSV has correct schema."""
    output_file = "results/test_schema.csv"
    
    if os.path.exists(output_file):
        os.remove(output_file)
    
    subprocess.run([
        sys.executable, 'src/run_mclp.py',
        '--instance', 'data/test_tiny.json',
        '--algorithm', 'greedy',
        '--seed', '42',
        '--output', output_file
    ], check=True, capture_output=True)
    
    # Load and check schema
    df = pd.read_csv(output_file)
    
    required_columns = [
        'instance', 'seed', 'algorithm', 'objective', 'coverage_pct',
        'runtime_sec', 'num_facilities', 'budget_used', 'facilities'
    ]
    
    for col in required_columns:
        assert col in df.columns, f"Missing column: {col}"
    
    # Check data types
    assert df['objective'].dtype in [float, int], "objective should be numeric"
    assert df['seed'].dtype == int, "seed should be integer"
    
    print("[OK] CSV schema test passed")
    
    # Cleanup
    os.remove(output_file)


if __name__ == "__main__":
    print("Running Phase 4 Integration Tests...\n")
    test_pipeline_determinism()
    test_all_algorithms_executable()
    test_csv_schema()
    print("\n[DONE] All integration tests passed!")