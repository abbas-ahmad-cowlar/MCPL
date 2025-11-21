import pandas as pd
import sys

def verify(csv_path):
    print(f"🔎 Verifying: {csv_path}")
    try:
        df = pd.read_csv(csv_path)
    except Exception as e:
        print(f"❌ CRITICAL: Could not read CSV. {e}")
        sys.exit(1)

    # 1. Integrity Checks
    if df.isnull().values.any():
        print("⚠️ WARNING: Dataset contains NaN values.")
        print(df[df.isnull().any(axis=1)])
    else:
        print("✅ Data Integrity: No missing values found.")

    if (df['coverage_pct'] > 100).any() or (df['coverage_pct'] < 0).any():
        print("❌ CRITICAL: Coverage percentage out of bounds (0-100).")
    else:
        print("✅ Logic Check: Coverage % is valid.")

    if (df['objective'] < 0).any():
        print("❌ CRITICAL: Negative objective values found.")
    else:
        print("✅ Logic Check: Objectives are non-negative.")

    # 2. The "Metaheuristic Assumption" (TS should generally beat Greedy)
    # We compare average objective per instance
    print("\n📊 Dominance Check (TS vs Greedy):")
    pivot = df.pivot_table(index='instance', columns='algorithm', values='objective', aggfunc='mean')
    
    # Only check if we have both columns
    if 'ts' in pivot.columns and 'greedy' in pivot.columns:
        pivot['TS > Greedy'] = pivot['ts'] >= pivot['greedy']
        pivot['Improvement'] = pivot['ts'] - pivot['greedy']
        
        print(pivot[['greedy', 'ts', 'TS > Greedy', 'Improvement']])
        
        if pivot['TS > Greedy'].all():
            print("\n✅ SUCCESS: Tabu Search outperforms Greedy on ALL instances on average.")
        else:
            failed_instances = pivot[~pivot['TS > Greedy']].index.tolist()
            print(f"\n⚠️ WARNING: Tabu Search underperformed on: {failed_instances}")
            print("   (This might be acceptable for very small instances, but bad for large ones)")
    
    # 3. Reproducibility Check (Standard Deviation > 0 means randomness worked)
    print("\n🎲 Randomness Check:")
    std_devs = df[df['algorithm'] == 'ts'].groupby('instance')['objective'].std()
    if (std_devs > 0).any():
        print("✅ Stochasticity confirmed (TS produces different results across seeds).")
    else:
        print("⚠️ WARNING: TS standard deviation is 0.0 everywhere. Did seeds work?")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python scripts/verify_results.py <path_to_csv>")
    else:
        verify(sys.argv[1])