import qrandom
import numpy as np
import datetime
import time

def fetch_anu_qrng_10k(filename):
    """
    Fetches 10,000 uint16 numbers from ANU QRNG using the quantumrandom library.
    The API provides a maximum of 1000 numbers per request.
    """
    print("Starting ANU QRNG fetch for 10,000 numbers...")
    all_data = []
    n_needed = 10000
    n_per_request = 1000  # Max allowed by API
    
    while len(all_data) < n_needed:
        remaining = n_needed - len(all_data)
        fetch_size = min(n_per_request, remaining)
        
        print(f"  Fetching batch of {fetch_size} numbers...")
        try:
            # Fetch one batch
            batch = qrandom.get_data(data_type='uint16', array_length=fetch_size)
            if batch is not None and len(batch) > 0:
                all_data.extend(batch)
                print(f"  Success. Total numbers fetched: {len(all_data)}")
            else:
                print("  API returned no data, retrying...")
            
            # Be polite to the API
            time.sleep(0.5) 
                
        except Exception as e:
            print(f"  Error fetching data: {e}. Retrying in 2 seconds...")
            time.sleep(2)
            
    # Convert final list to a numpy array
    final_data = np.array(all_data, dtype='uint16')
    
    # Save to file
    try:
        np.savetxt(filename, final_data, fmt='%d')
        print(f"\nSuccessfully saved 10,000 numbers to {filename}")
    except Exception as e:
        print(f"\nError saving data to {filename}: {e}")

if __name__ == "__main__":
    # Create a timestamped filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    N_VALUES = 10000
    output_filename = f"anu_qrng_{N_VALUES}_{timestamp}.txt"
    
    print(f"This script will fetch {N_VALUES} quantum random numbers")
    print("and save them to:")
    print(f"{output_filename}\n")
    print("This may take 10-15 seconds due to API limits.")
    
    fetch_anu_qrng_10k(output_filename)

