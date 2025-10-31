import pandas as pd
import numpy as np

def classify_archetype(row, kappa_median):
    if row['delta_power'] > 0 and row['kappa_abs'] > kappa_median:
        return 'Gladiator'
    elif row['delta_power'] > 0 and row['kappa_abs'] <= kappa_median:
        return 'Weaver'
    elif row['delta_power'] <= 0 and row['kappa_abs'] > kappa_median:
        return 'Vortex'
    else:
        return 'Drifter'

# Load the datasets
try:
    plasma_df = pd.read_csv("Magnetics_E-935646-1-1_archetypes.csv")
    eeg_df = pd.read_csv("helical_epochs.csv")
    market_df = pd.read_csv("market_archetypes.csv")
except FileNotFoundError as e:
    print(f"Error loading data: {e}. Make sure all CSV files are in the same folder as this script.")
    exit()

# Add source columns
plasma_df['source'] = 'plasma'
eeg_df['source'] = 'eeg'
market_df['source'] = 'market'

# Standardize column names
plasma_df = plasma_df[['kappa_abs', 'delta_power', 'archetype', 'source']]
eeg_df = eeg_df[['kappa_abs', 'delta_power', 'archetype', 'source']]

market_df = market_df.rename(columns={'intrinsic_kappa': 'kappa_abs', 'performance_score': 'delta_power'})
kappa_median_market = market_df['kappa_abs'].median()
market_df['archetype'] = market_df.apply(classify_archetype, args=(kappa_median_market,), axis=1)
market_df = market_df[['kappa_abs', 'delta_power', 'archetype', 'source']]


# Combine the dataframes
combined_df = pd.concat([plasma_df, eeg_df, market_df], ignore_index=True)

# Save the combined dataframe
combined_df.to_csv('combined_archetypes.csv', index=False)

print("Successfully combined the CSV files into 'combined_archetypes.csv'")