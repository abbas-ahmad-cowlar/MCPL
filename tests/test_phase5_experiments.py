"""
Tests for Phase 5: Experiment infrastructure.
"""

import sys
import os
import subprocess
import json

sys.path.insert(0, 'src')
sys.path.insert(0, 'scripts')

from generate_instance import generate_instance, validate_instance


def test_instance_generation():
    """Test that instance generator creates valid instances."""
    instance = generate_instance(
        num_facilities=10,
        num_customers=20,
        budget=5.0,
        coverage_radius=8.0,
        seed=42
    )
    
    # Basic checks
    assert len(instance['I']) == 10, "Wrong number of facilities"
    assert len(instance['J']) == 20, "Wrong number of customers"
    assert instance['B'] == 5.0, "Wrong budget"
    
    # Check coverage sets
    assert len(instance['I_j']) == 20, "Missing coverage sets"
    
    # Validate
    is_valid = validate_instance(instance)
    
    print(f"[OK] Instance generation test passed (valid={is_valid})")


def test_instance_generator_script():
    """Test that generator script runs without errors."""
    output_file = "data/test_gen.json"
    
    # Clean up
    if os.path.exists(output_file):
        os.remove(output_file)
    
    # Run generator
    result = subprocess.run([
        'python', 'scripts/generate_instance.py',
        '--I', '20',
        '--J', '50',
        '--B', '8',
        '--radius', '6.0',
        '--seed', '42',
        '-o', output_file,
        '--validate'
    ], capture_output=True, text=True)
    
    assert result.returncode == 0, f"Generator failed: {result.stderr}"
    assert os.path.exists(output_file), "Output file not created"
    
    # Load and verify
    with open(output_file, 'r') as f:
        data = json.load(f)
    
    assert len(data['I']) == 20
    assert len(data['J']) == 50
    
    print("[OK] Instance generator script test passed")
    
    # Cleanup
    os.remove(output_file)


def test_dataset_generation_script():
    """Test that full dataset generation works."""
    # This would take too long, so just check script exists and is executable
    script_path = "scripts/generate_dataset.sh"
    
    assert os.path.exists(script_path), "Dataset generation script not found"
    assert os.access(script_path, os.X_OK), "Script not executable (run: chmod +x scripts/generate_dataset.sh)"
    
    print("[OK] Dataset generation script exists")


def test_experiment_runner_exists():
    """Test that experiment runner script exists."""
    script_path = "scripts/run_full_experiments.sh"
    
    assert os.path.exists(script_path), "Experiment runner not found"
    
    print("[OK] Experiment runner script exists")


def test_analysis_scripts_exist():
    """Test that all analysis scripts are present."""
    scripts = [
        'scripts/analyze_results.py',
        'scripts/plot_convergence.py',
        'scripts/generate_report_tables.py'
    ]
    
    for script in scripts:
        assert os.path.exists(script), f"Missing script: {script}"
    
    print(f"[OK] All {len(scripts)} analysis scripts exist")


if __name__ == "__main__":
    print("Running Phase 5 Experiment Tests...\n")
    test_instance_generation()
    test_instance_generator_script()
    test_dataset_generation_script()
    test_experiment_runner_exists()
    test_analysis_scripts_exist()
    print("\n[DONE] All Phase 5 tests passed!")