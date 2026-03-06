import pandas as pd
import time
import os

base_file = 'all_stocks_5yr.csv'
base_df = pd.read_csv(base_file)

print(f"Base CSV: {len(base_df):,} rows, {base_df.memory_usage(deep=True).sum() / 1e6:.1f} MB")

scales = [10, 100]

for scale in scales:
    print(f"\n=== Creating {scale}x scale ===")
    
    # 1. Create ballooned DataFrame (Pandas)
    start = time.time()
    balloon_df = pd.concat([base_df] * scale, ignore_index=True)
    balloon_time = time.time() - start
    
    # 2. Save CSV
    csv_file = f"all_stocks_{scale}x.csv"
    start = time.time()
    balloon_df.to_csv(csv_file, index=False)
    csv_time = time.time() - start
    csv_size = os.path.getsize(csv_file) / 1e6
    
    # 3. Save Parquet (optimized)
    parquet_file = f"all_stocks_{scale}x.parquet"
    start = time.time()
    balloon_df.to_parquet(parquet_file, index=False, engine='pyarrow')
    parquet_time = time.time() - start
    parquet_size = os.path.getsize(parquet_file) / 1e6
    
    # 4. Verify + Timing
    print(f"Created {len(balloon_df):,} rows: {balloon_time:.2f}s")
    print(f"  Memory: {balloon_df.memory_usage(deep=True).sum() / 1e6:.1f} MB")
    print(f"  CSV write: {csv_time:.2f}s ({csv_size:.1f} MB)")
    print(f"  Parquet write: {parquet_time:.2f}s ({parquet_size:.1f} MB)")
    print(f"  CSV/Parquet size ratio: {csv_size/parquet_size:.1f}x")
    
    # 5. Read timing comparison (Pandas vs Polars)
    print("\nRead benchmarks:")
    
    # Pandas CSV
    start = time.time()
    pd.read_csv(csv_file, nrows=10000)
    print(f"  Pandas CSV (10k rows): {time.time()-start:.3f}s")
    
    # Pandas Parquet
    start = time.time()
    pd.read_parquet(parquet_file).head(10000)
    print(f"  Pandas Parquet (10k): {time.time()-start:.3f}s")

input("Press any key to quit.")