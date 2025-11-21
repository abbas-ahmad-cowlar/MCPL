#!/usr/bin/env python3
"""
Data Conversion Utility: JSON to Mosel .dat format
Converts MCLP instances from JSON format to FICO Xpress Mosel data files.

Author: MCLP Migration Team
Date: 2025-11-21
"""

import json
import os
import sys
from pathlib import Path
from typing import Dict, List, Tuple


class JSONtoMoselConverter:
    """Converts MCLP JSON instances to Mosel .dat format."""

    def __init__(self, json_path: str, output_dir: str = None):
        """
        Initialize converter.

        Args:
            json_path: Path to JSON instance file
            output_dir: Output directory for .dat file (default: same as json)
        """
        self.json_path = json_path
        self.output_dir = output_dir or os.path.dirname(json_path)
        self.data = None
        self.stats = {}

    def load_json(self) -> Dict:
        """Load and validate JSON instance."""
        print(f"Loading: {self.json_path}")

        with open(self.json_path, 'r') as f:
            self.data = json.load(f)

        # Validate required fields
        required_fields = ['I', 'J', 'f', 'd', 'I_j', 'B']
        missing = [f for f in required_fields if f not in self.data]

        if missing:
            raise ValueError(f"Missing required fields: {missing}")

        print(f"  ✓ Loaded instance: {self.data.get('name', 'unnamed')}")
        return self.data

    def compute_statistics(self) -> Dict:
        """Compute instance statistics for validation."""
        nI = len(self.data['I'])
        nJ = len(self.data['J'])

        total_facility_cost = sum(float(v) for v in self.data['f'].values())
        total_demand = sum(float(v) for v in self.data['d'].values())

        # Coverage statistics
        total_coverage_arcs = sum(len(facilities) for facilities in self.data['I_j'].values())
        coverage_density = total_coverage_arcs / (nI * nJ) if nI * nJ > 0 else 0

        # Compute J_i (reverse mapping)
        J_i = {i: [] for i in self.data['I']}
        for j_str, facilities in self.data['I_j'].items():
            j = int(j_str)
            for i in facilities:
                J_i[i].append(j)

        avg_facilities_per_customer = total_coverage_arcs / nJ if nJ > 0 else 0
        avg_customers_per_facility = total_coverage_arcs / nI if nI > 0 else 0

        self.stats = {
            'nI': nI,
            'nJ': nJ,
            'total_facility_cost': total_facility_cost,
            'total_demand': total_demand,
            'budget': float(self.data['B']),
            'budget_ratio': float(self.data['B']) / total_facility_cost if total_facility_cost > 0 else 0,
            'coverage_arcs': total_coverage_arcs,
            'coverage_density': coverage_density,
            'avg_facilities_per_customer': avg_facilities_per_customer,
            'avg_customers_per_facility': avg_customers_per_facility,
            'min_facility_cost': min(float(v) for v in self.data['f'].values()),
            'max_facility_cost': max(float(v) for v in self.data['f'].values()),
            'min_demand': min(float(v) for v in self.data['d'].values()),
            'max_demand': max(float(v) for v in self.data['d'].values()),
        }

        return self.stats

    def generate_mosel_dat(self) -> str:
        """
        Generate Mosel .dat file content.

        Mosel data format:
        - Scalars: nI, nJ, BUDGET
        - Arrays: FACILITIES, CUSTOMERS, COST, DEMAND
        - Coverage sets: I_j (list of lists)
        """
        lines = []

        # Header comment
        lines.append(f"! MCLP Instance: {self.data.get('name', 'unnamed')}")
        lines.append(f"! Generated from: {os.path.basename(self.json_path)}")
        lines.append(f"! Facilities: {self.stats['nI']}, Customers: {self.stats['nJ']}")
        lines.append(f"! Budget: {self.stats['budget']:.2f}")
        lines.append("")

        # Scalars
        lines.append("! === SCALARS ===")
        lines.append(f"nI: {self.stats['nI']}")
        lines.append(f"nJ: {self.stats['nJ']}")
        lines.append(f"BUDGET: {self.stats['budget']}")
        lines.append("")

        # Facility indices (0-indexed in Mosel)
        lines.append("! === FACILITY INDICES ===")
        facilities_str = " ".join(str(i) for i in sorted(self.data['I']))
        lines.append(f"FACILITIES: [{facilities_str}]")
        lines.append("")

        # Customer indices
        lines.append("! === CUSTOMER INDICES ===")
        customers_str = " ".join(str(j) for j in sorted(self.data['J']))
        lines.append(f"CUSTOMERS: [{customers_str}]")
        lines.append("")

        # Facility costs (as array indexed by facility ID)
        lines.append("! === FACILITY COSTS ===")
        lines.append("COST: [")
        for i in sorted(self.data['I']):
            cost = float(self.data['f'][str(i)])
            lines.append(f"  {i} {cost:.6f}")
        lines.append("]")
        lines.append("")

        # Customer demands
        lines.append("! === CUSTOMER DEMANDS ===")
        lines.append("DEMAND: [")
        for j in sorted(self.data['J']):
            demand = float(self.data['d'][str(j)])
            lines.append(f"  {j} {demand:.6f}")
        lines.append("]")
        lines.append("")

        # Coverage sets I_j (facilities that can cover customer j)
        lines.append("! === COVERAGE SETS I_j ===")
        lines.append("! For each customer j: list of facilities that can cover j")
        lines.append("COVERAGE_I_j: [")
        for j in sorted(self.data['J']):
            facilities = sorted(self.data['I_j'][str(j)])
            facilities_str = " ".join(str(i) for i in facilities)
            lines.append(f"  {j} [{facilities_str}]")
        lines.append("]")
        lines.append("")

        # Reverse coverage sets J_i (customers covered by facility i)
        lines.append("! === REVERSE COVERAGE SETS J_i ===")
        lines.append("! For each facility i: list of customers covered by i")
        lines.append("COVERAGE_J_i: [")

        # Build J_i mapping
        J_i = {i: [] for i in self.data['I']}
        for j_str, facilities in self.data['I_j'].items():
            j = int(j_str)
            for i in facilities:
                J_i[i].append(j)

        for i in sorted(self.data['I']):
            customers = sorted(J_i[i])
            customers_str = " ".join(str(j) for j in customers)
            lines.append(f"  {i} [{customers_str}]")
        lines.append("]")
        lines.append("")

        # Statistics as comments
        lines.append("! === INSTANCE STATISTICS ===")
        lines.append(f"! Total facility cost: {self.stats['total_facility_cost']:.2f}")
        lines.append(f"! Total demand: {self.stats['total_demand']:.2f}")
        lines.append(f"! Budget ratio: {self.stats['budget_ratio']:.2%}")
        lines.append(f"! Coverage density: {self.stats['coverage_density']:.2%}")
        lines.append(f"! Avg facilities per customer: {self.stats['avg_facilities_per_customer']:.2f}")
        lines.append(f"! Avg customers per facility: {self.stats['avg_customers_per_facility']:.2f}")
        lines.append(f"! Facility cost range: [{self.stats['min_facility_cost']:.2f}, {self.stats['max_facility_cost']:.2f}]")
        lines.append(f"! Demand range: [{self.stats['min_demand']:.2f}, {self.stats['max_demand']:.2f}]")

        return "\n".join(lines)

    def save_dat_file(self, content: str) -> str:
        """Save .dat file to disk."""
        # Generate output filename
        base_name = os.path.splitext(os.path.basename(self.json_path))[0]
        output_path = os.path.join(self.output_dir, f"{base_name}.dat")

        with open(output_path, 'w') as f:
            f.write(content)

        print(f"  ✓ Saved: {output_path}")
        return output_path

    def convert(self) -> Tuple[str, Dict]:
        """
        Execute full conversion pipeline.

        Returns:
            (output_path, statistics)
        """
        self.load_json()
        self.compute_statistics()

        print(f"  Statistics:")
        print(f"    - Facilities: {self.stats['nI']}, Customers: {self.stats['nJ']}")
        print(f"    - Budget: {self.stats['budget']:.2f} / {self.stats['total_facility_cost']:.2f} ({self.stats['budget_ratio']:.1%})")
        print(f"    - Coverage density: {self.stats['coverage_density']:.2%}")

        content = self.generate_mosel_dat()
        output_path = self.save_dat_file(content)

        return output_path, self.stats


def convert_all_instances(input_dir: str, output_dir: str) -> Dict[str, Dict]:
    """
    Convert all JSON instances in a directory.

    Args:
        input_dir: Directory containing JSON files
        output_dir: Output directory for .dat files

    Returns:
        Dictionary mapping instance name to statistics
    """
    json_files = [f for f in os.listdir(input_dir) if f.endswith('.json')]

    if not json_files:
        print(f"No JSON files found in {input_dir}")
        return {}

    print(f"\nFound {len(json_files)} JSON instance(s)")
    print("=" * 70)

    results = {}

    for json_file in sorted(json_files):
        json_path = os.path.join(input_dir, json_file)
        instance_name = os.path.splitext(json_file)[0]

        try:
            converter = JSONtoMoselConverter(json_path, output_dir)
            output_path, stats = converter.convert()
            results[instance_name] = stats
            print()

        except Exception as e:
            print(f"  ✗ ERROR converting {json_file}: {e}")
            print()

    return results


def print_summary_table(results: Dict[str, Dict]):
    """Print summary table of all converted instances."""
    if not results:
        return

    print("=" * 70)
    print("CONVERSION SUMMARY")
    print("=" * 70)
    print(f"{'Instance':<15} {'Facilities':<12} {'Customers':<12} {'Budget':<12} {'Coverage':<12}")
    print("-" * 70)

    for name in sorted(results.keys()):
        stats = results[name]
        print(f"{name:<15} {stats['nI']:<12} {stats['nJ']:<12} "
              f"{stats['budget']:<12.2f} {stats['coverage_density']:<12.2%}")

    print("=" * 70)
    print(f"Total instances converted: {len(results)}")
    print()


def main():
    """Main entry point for command-line usage."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Convert MCLP JSON instances to Mosel .dat format",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Convert single file
  python convert_json_to_mosel.py --input data/S1.json --output Mosel/data/

  # Convert all files in directory
  python convert_json_to_mosel.py --input-dir data/ --output-dir Mosel/data/
        """
    )

    parser.add_argument('--input', type=str, help='Input JSON file')
    parser.add_argument('--output', type=str, help='Output directory for .dat file')
    parser.add_argument('--input-dir', type=str, help='Input directory containing JSON files')
    parser.add_argument('--output-dir', type=str, help='Output directory for .dat files')

    args = parser.parse_args()

    # Validate arguments
    if args.input and args.input_dir:
        print("ERROR: Specify either --input or --input-dir, not both")
        sys.exit(1)

    if not args.input and not args.input_dir:
        print("ERROR: Must specify either --input or --input-dir")
        parser.print_help()
        sys.exit(1)

    # Single file conversion
    if args.input:
        if not os.path.exists(args.input):
            print(f"ERROR: Input file not found: {args.input}")
            sys.exit(1)

        output_dir = args.output or os.path.dirname(args.input)
        os.makedirs(output_dir, exist_ok=True)

        converter = JSONtoMoselConverter(args.input, output_dir)
        output_path, stats = converter.convert()

        print(f"\n✓ Conversion complete!")
        print(f"  Input:  {args.input}")
        print(f"  Output: {output_path}")

    # Directory conversion
    elif args.input_dir:
        if not os.path.exists(args.input_dir):
            print(f"ERROR: Input directory not found: {args.input_dir}")
            sys.exit(1)

        output_dir = args.output_dir or args.input_dir
        os.makedirs(output_dir, exist_ok=True)

        results = convert_all_instances(args.input_dir, output_dir)
        print_summary_table(results)

        print(f"✓ All conversions complete!")
        print(f"  Input directory:  {args.input_dir}")
        print(f"  Output directory: {output_dir}")


if __name__ == "__main__":
    main()
