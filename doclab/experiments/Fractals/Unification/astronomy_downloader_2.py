from astroquery.gaia import Gaia
import pandas as pd
import numpy as np

# --- Configuration ---
N_HEALPIX_LEVEL_4 = 3072 # Total number of HEALPix level 4 pixels in the sky
HEALPIX_CHUNKS_TO_PROCESS = 100 # Adjust this number to download over time. Use 3072 for full sky.
START_INDEX = 0 # Start from pixel 0
OUTPUT_FILENAME = 'gaia_chunked_subsample.parquet'
ALL_RESULTS = []

# --- ADQL Base Query ---
# Note: Do NOT use TOP N here; the WHERE clause does the filtering.
BASE_QUERY = """
SELECT
    source_id, ra, dec, parallax, parallax_error, pmra, pmdec, 
    phot_g_mean_mag, phot_bp_mean_mag, phot_rp_mean_mag
FROM
    gaiadr3.gaia_source
WHERE
    -- 1. Chunking filter (PLACEHOLDER: This will be replaced in the loop)
    healpix_index_4 = {index}
    
    -- 2. Uniform density filter (~1/1800 sources)
    AND MOD(source_id / 1000, 1800) = 9
    
    -- 3. Quality cuts for a 'publication-grade' sample
    AND parallax_over_error > 5
    AND visibility_periods_used > 8
"""

print(f"Starting chunked download for {HEALPIX_CHUNKS_TO_PROCESS} HEALPix level 4 pixels...")

# --- Iterative Download Loop ---
for i in range(START_INDEX, START_INDEX + HEALPIX_CHUNKS_TO_PROCESS):
    if i >= N_HEALPIX_LEVEL_4:
        break
        
    print(f"-> Querying HEALPix chunk {i+1} of {HEALPIX_CHUNKS_TO_PROCESS} (Index: {i})...")
    
    # Format the query with the current HEALPix index
    current_query = BASE_QUERY.format(index=i)
    
    try:
        # Execute the job synchronously, which is fast for small chunks
        job = Gaia.launch_job(current_query, dump_to_file=False)
        results_table = job.get_results()
        
        # Convert to DataFrame and append to list
        if len(results_table) > 0:
            results_df = results_table.to_pandas()
            ALL_RESULTS.append(results_df)
            print(f"   Success. Downloaded {len(results_df)} stars.")
        else:
            print("   Success. Chunk was empty.")

    except Exception as e:
        # Catch and report any potential network or server errors, then continue
        print(f"   !!! ERROR in chunk {i}: {e}. Skipping to next chunk.")
        
# --- Final Aggregation and Save ---
if ALL_RESULTS:
    final_df = pd.concat(ALL_RESULTS, ignore_index=True)
    final_df.to_parquet(OUTPUT_FILENAME, index=False)
    
    # Update the START_INDEX for the next run
    next_start_index = i + 1 
    
    print("\n-------------------------------------------")
    print(f"✅ Download complete! Total stars saved: {len(final_df)}")
    print(f"💾 Saved to {OUTPUT_FILENAME}")
    print(f"👉 Next time, set START_INDEX = {next_start_index} to continue from where you left off.")
else:
    print("\n❌ No data downloaded.")