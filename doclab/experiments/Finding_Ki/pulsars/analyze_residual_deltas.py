import pandas as pd
import numpy as np
from tqdm import tqdm
from loguru import logger as log

def analyze_residual_deltas(input_csv, output_csv):
    """
    Analyzes the deltas between consecutive residuals for each pulsar.
    """
    log.info(f"Reading aggregated residuals from {input_csv}...")
    try:
        df = pd.read_csv(input_csv)
    except FileNotFoundError:
        log.error(f"Input file not found: {input_csv}. Please run the extractor script first.")
        return

    pulsar_names = df['pulsar'].unique()
    analysis_results = []

    for pulsar in tqdm(pulsar_names, desc="Analyzing Pulsar Deltas"):
        pulsar_df = df[df['pulsar'] == pulsar].sort_values('mjd').copy()

        if len(pulsar_df) < 2:
            continue

        # Calculate deltas between consecutive points
        pulsar_df['delta_mjd'] = pulsar_df['mjd'].diff()
        pulsar_df['delta_residual'] = pulsar_df['residual_us'].diff()

        # Remove the first row with NaN deltas
        deltas = pulsar_df['delta_residual'].dropna()

        if len(deltas) > 1:
            # Calculate higher-order statistics of the deltas
            variance = deltas.var()
            skewness = deltas.skew()
            kurtosis = deltas.kurtosis() # Pandas calculates excess kurtosis (0 is normal)

            analysis_results.append({
                'pulsar': pulsar,
                'observation_count': len(pulsar_df),
                'mean_residual': pulsar_df['residual_us'].mean(),
                'variance_of_deltas': variance,
                'skewness_of_deltas': skewness,
                'kurtosis_of_deltas': kurtosis
            })

    if analysis_results:
        results_df = pd.DataFrame(analysis_results)
        results_df.to_csv(output_csv, index=False)
        log.success(f"Delta analysis complete. Results for {len(results_df)} pulsars saved to {output_csv}")
    else:
        log.warning("No pulsars were analyzed.")

if __name__ == '__main__':
    # This script assumes you have already run the batch_residual_extractor.py
    # and have the 'all_pulsar_residuals.csv' file.
    INPUT_CSV = 'all_pulsar_residuals.csv'
    OUTPUT_CSV = 'pulsar_delta_analysis.csv'
    
    analyze_residual_deltas(INPUT_CSV, OUTPUT_CSV)