# INSTRUMENT PART 1: The Forager
# id: INST-DATA-FETCHER-001
# version: 1.0
#
# ABSTRACT: This script is responsible for the first stage of the analysis:
# data acquisition. It patiently fetches time-series data from a public API
# and saves it to a local file. This decouples the analysis from the
# potential failures and rate limits of network requests, ensuring the
# analyzer script has a stable, local dataset to work with.

import yfinance as yf
import pandas as pd
import sys

def fetch_and_save_data(ticker, start_date, end_date, filename):
    """
    Fetches historical market data and saves the normalized 'Close' price
    to a local CSV file.
    """
    print(f"Attempting to fetch data for '{ticker}' from {start_date} to {end_date}...")
    
    # Download the data from Yahoo Finance
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    # --- Robustness Check ---
    # Exit gracefully if the download fails for any reason.
    if data.empty:
        print("\n--- DATA FETCH FAILED ---")
        print("Could not download market data. This may be due to:")
        print("  1. API Rate Limiting: Please wait a while before trying again.")
        print("  2. An invalid ticker symbol or date range.")
        print("  3. A network connection issue.")
        sys.exit(1)
        
    print("Data fetched successfully.")
    
    # Isolate the 'Close' price and ensure it's a numeric type
    price = pd.to_numeric(data['Close'])
    
    # Normalize the data to oscillate between -1 and 1
    price_min = price.min()
    price_max = price.max()
    normalized_price = 2 * ((price - price_min) / (price_max - price_min)) - 1
    
    # Save the normalized data to a CSV file
    normalized_price.to_csv(filename, header=['normalized_price'], index=False)
    print(f"Normalized data saved to '{filename}'")

if __name__ == '__main__':
    # --- PARAMETERS ---
    # Define the data to be fetched.
    TICKER = '^GSPC'
    START_DATE = '2007-01-01'
    END_DATE = '2010-01-01'
    OUTPUT_FILENAME = 'sp500_data_2007_2010.csv'
    
    # --- EXECUTION ---
    fetch_and_save_data(TICKER, START_DATE, END_DATE, OUTPUT_FILENAME)
