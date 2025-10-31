import os
import pandas as pd
import warnings

# --- Corrected PINT Imports ---
# Use the recommended high-level function and import other components directly.
from pint.models import get_model_and_toas
from pint.residuals import Residuals
from pint import logging
# --- End of Imports ---

from loguru import logger as log
from tqdm import tqdm

# Suppress warnings from PINT for cleaner output
warnings.filterwarnings("ignore", category=UserWarning)
logging.setup(level="ERROR") # Keep PINT's output quiet

def find_pulsar_file(directory, pulsar_name, extension):
    """Finds a file for a pulsar, handling different naming conventions."""
    for f in os.listdir(directory):
        if f.startswith(pulsar_name) and f.endswith(extension):
            return os.path.join(directory, f)
    log.warning(f"No '{extension}' file found for pulsar {pulsar_name} in {directory}")
    return None

def extract_residuals_for_pulsar(par_file, tim_file):
    """Core function to calculate residuals for one pulsar."""
    try:
        # Use the modern, combined function to load the model and TOAs.
        # This function handles all necessary initializations.
        model, t = get_model_and_toas(
            par_file,
            tim_file,
            ephem="DE440",
            planets=True,
            include_bipm='BIPM2021'
        )
        res = Residuals(t, model).time_resids.to_value('us')
        mjds = t.get_mjds().value
        return pd.DataFrame({'mjd': mjds, 'residual_us': res})
    except Exception as e:
        log.error(f"Failed to process {os.path.basename(par_file)} due to: {e}")
        return None

def get_processed_pulsars(checkpoint_file):
    """Load the set of already processed pulsars from a log file."""
    if not os.path.exists(checkpoint_file):
        return set()
    with open(checkpoint_file, 'r') as f:
        return set(line.strip() for line in f)

def log_processed_pulsar(checkpoint_file, pulsar_name):
    """Log a successfully processed pulsar to the checkpoint file."""
    with open(checkpoint_file, 'a') as f:
        f.write(f"{pulsar_name}\n")

def batch_process_directory(base_dir, output_csv, checkpoint_log):
    """
    Processes all pulsars in a directory with a robust checkpointing system.
    """
    par_dir = os.path.join(base_dir, 'narrowband', 'par')
    tim_dir = os.path.join(base_dir, 'narrowband', 'tim')

    pulsar_names = sorted(list(set([f.split('_')[0] for f in os.listdir(par_dir) if f.endswith('.par')])))
    log.info(f"Found {len(pulsar_names)} total pulsars to potentially process.")

    processed_pulsars = get_processed_pulsars(checkpoint_log)
    if processed_pulsars:
        log.info(f"Resuming... Found {len(processed_pulsars)} pulsars in the checkpoint log to skip.")

    if not os.path.exists(output_csv):
        pd.DataFrame(columns=['mjd', 'residual_us', 'pulsar']).to_csv(output_csv, index=False)
        log.info(f"Created new output file: {output_csv}")

    for pulsar in tqdm(pulsar_names, desc="Extracting Residuals"):
        if pulsar in processed_pulsars:
            continue

        par_file = find_pulsar_file(par_dir, pulsar, '.par')
        tim_file = find_pulsar_file(tim_dir, pulsar, '.tim')

        if par_file and tim_file:
            residuals_df = extract_residuals_for_pulsar(par_file, tim_file)
            
            if residuals_df is not None:
                residuals_df['pulsar'] = pulsar
                residuals_df.to_csv(output_csv, mode='a', header=False, index=False)
                log_processed_pulsar(checkpoint_log, pulsar)
                log.success(f"Processed and saved residuals for {pulsar}.")
    
    log.info("Batch processing complete.")

if __name__ == '__main__':
    # Make sure to update this path to your actual data directory
    NANOGRAV_BASE_DIR = r'C:/Users/keatw/Downloads/NANOGrav15yr_PulsarTiming_v2.1.0/NANOGrav15yr_PulsarTiming_v2.1.0'
    OUTPUT_CSV = 'all_pulsar_residuals.csv'
    CHECKPOINT_LOG = 'processed_pulsars.log'
    
    batch_process_directory(NANOGRAV_BASE_DIR, OUTPUT_CSV, CHECKPOINT_LOG)