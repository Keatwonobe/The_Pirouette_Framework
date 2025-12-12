import requests
import pandas as pd
import json
import numpy as np
import datetime
import math
import time

# --- Constants ---
MAX_ANU_BATCH = 1024
RANDOM_ORG_MAX_BATCH = 10000

# 1) ANU quantum random
def fetch_anu_qrng(n=10000, filename="anu_qrng_data.txt"):
    """
    Fetches quantum random numbers from ANU in batches and saves to a .txt file.
    ANU API limit is 1024 per request.
    """
    print(f"Fetching {n} numbers from ANU (in batches of {MAX_ANU_BATCH})...")
    all_data = []
    try:
        num_remaining = n
        while num_remaining > 0:
            batch_size = min(num_remaining, MAX_ANU_BATCH)
            url = f"https://qrng.anu.edu.au/API/jsonI.php?length={batch_size}&type=uint16"
            
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            data = response.json()
            
            if data.get("success"):
                batch_data = data.get("data", [])
                all_data.extend(batch_data)
                num_remaining -= len(batch_data)
                print(f"  ...fetched {len(all_data)} / {n} numbers...")
            else:
                print("  ...ANU API returned success=False, stopping.")
                break
            
            # Brief pause to be polite to the API
            time.sleep(0.1)
        
        print(f"Saving {len(all_data)} numbers to {filename}")
        with open(filename, 'w') as f:
            for num in all_data:
                f.write(f"{num}\n")
        print(f"Successfully saved ANU data to {filename}")
        
    except requests.RequestException as e:
        print(f"Error fetching from ANU: {e}")

# 2) random.org atmospheric integers
def fetch_random_org(n=10000, minv=1, maxv=69, filename="random_org_data.txt"):
    """
    Fetches random integers from random.org and saves to a .txt file.
    random.org API limit is 10,000 per request.
    """
    if n > RANDOM_ORG_MAX_BATCH:
        print(f"Error: random.org request limit is {RANDOM_ORG_MAX_BATCH}. Cannot fetch {n}.")
        return

    print(f"Fetching {n} numbers from random.org ({minv}-{maxv})...")
    url = (
        "https://www.random.org/integers/"
        f"?num={n}&min={minv}&max={maxv}&col=1&base=10&format=plain&rnd=new"
    )
    try:
        # Increased timeout for the larger 10k request
        response = requests.get(url, timeout=30) 
        response.raise_for_status()
        txt = response.text.strip()
        
        if not txt:
            print("Error: Received empty response from random.org")
            return

        data_list = [int(x) for x in txt.splitlines()]
        
        print(f"Saving {len(data_list)} numbers to {filename}")
        with open(filename, 'w') as f:
            for num in data_list:
                f.write(f"{num}\n")
        print(f"Successfully saved random.org data to {filename}")

    except requests.RequestException as e:
        print(f"Error fetching from random.org: {e}")
    except ValueError as e:
        print(f"Error parsing numbers from random.org: {e}")

# 3) scrape lottery pages (Powerball / Mega Millions)
def fetch_powerball_tx(filename="powerball_tx_data.csv"):
    """
    Scrapes Texas Powerball winning numbers and saves them to a .csv file.
    """
    print(f"Fetching Powerball data from Texas Lottery...")
    url = "https://www.texaslottery.com/export/sites/lottery/Games/Powerball/Winning_Numbers/index.html"
    try:
        # read_html returns a list of DataFrames. We want the first one [0].
        df_list = pd.read_html(url)
        if not df_list:
            print("No tables found on Powerball page.")
            return
            
        df = df_list[0]
        
        # Clean up column names (they might have weird chars or extra spaces)
        df.columns = [str(col).replace('\n', ' ').replace('\r', '').strip() for col in df.columns]
        
        print(f"Saving {len(df)} records to {filename}")
        df.to_csv(filename, index=False)
        print(f"Successfully saved Powerball data to {filename}")

    except ImportError:
        # This error happens if pandas dependencies (like lxml) aren't installed
        print("Error: pandas.read_html requires 'lxml' or 'html5lib'. Please install one.")
    except Exception as e:
        print(f"Error fetching or parsing Powerball data: {e}")

# 4) Numpy PRNG (Baseline)
def fetch_numpy_prng(n=10000, minv=1, maxv=69, filename="numpy_prng_data.txt"):
    """
    Generates pseudo-random numbers using numpy and saves to a .txt file.
    """
    print(f"Generating {n} PRNG numbers from numpy ({minv}-{maxv})...")
    try:
        # Use default_rng() for modern numpy
        rng = np.random.default_rng()
        # high is exclusive, so add 1 to maxv
        data = rng.integers(low=minv, high=maxv + 1, size=n)
        
        print(f"Saving {len(data)} numbers to {filename}")
        with open(filename, 'w') as f:
            for num in data:
                f.write(f"{num}\n")
        print(f"Successfully saved numpy PRNG data to {filename}")
        
    except Exception as e:
        print(f"Error generating or saving numpy data: {e}")

# --- Main execution ---
# This block runs when you execute the script directly (e.g., `python comp_data.py`)
if __name__ == "__main__":
    
    # --- Configuration ---
    N_VALUES = 10000
    MIN_VAL = 1
    MAX_VAL = 69 # As per your experiment design
    
    # Generate a unique timestamp for this run
    TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    print(f"--- Starting Data Fetch Run: {TIMESTAMP} ---")

    # --- 1. ANU QRNG ---
    anu_filename = f"anu_qrng_{N_VALUES}_{TIMESTAMP}.txt"
    fetch_anu_qrng(n=N_VALUES, filename=anu_filename)
    print("\n")

    # --- 2. random.org ---
    random_org_filename = f"random_org_{N_VALUES}_{TIMESTAMP}.txt"
    fetch_random_org(n=N_VALUES, minv=MIN_VAL, maxv=MAX_VAL, filename=random_org_filename)
    print("\n")
    
    # --- 3. TX Powerball ---
    powerball_filename = f"powerball_tx_{TIMESTAMP}.csv"
    fetch_powerball_tx(filename=powerball_filename)
    print("\n")

    # --- 4. Numpy PRNG (Baseline) ---
    numpy_filename = f"numpy_prng_{N_VALUES}_{TIMESTAMP}.txt"
    fetch_numpy_prng(n=N_VALUES, minv=MIN_VAL, maxv=MAX_VAL, filename=numpy_filename)
    print("\n")
    
    print("--- Data Fetching Complete ---")
    print(f"Files created:")
    print(f" - {anu_filename}")
    print(f" - {random_org_filename}")
    print(f" - {powerball_filename}")
    print(f" - {numpy_filename}")

