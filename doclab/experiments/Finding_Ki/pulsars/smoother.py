import os
import pint.models as models
import pint.toa as toa
from loguru import logger as log
from tqdm import tqdm

def smooth_files(base_dir):
    """
    Reads all .par and .tim files, loads them with pint, and saves them
    back out to a new 'smoothed' directory in a standardized format.
    """
    par_dir = os.path.join(base_dir, 'narrowband', 'par')
    tim_dir = os.path.join(base_dir, 'narrowband', 'tim')

    # Create directories for the cleaned files
    smoothed_par_dir = os.path.join(base_dir, 'narrowband', 'par_smoothed')
    smoothed_tim_dir = os.path.join(base_dir, 'narrowband', 'tim_smoothed')
    os.makedirs(smoothed_par_dir, exist_ok=True)
    os.makedirs(smoothed_tim_dir, exist_ok=True)

    pulsar_files = [f for f in os.listdir(par_dir) if f.endswith('.par')]
    
    log.info(f"Found {len(pulsar_files)} pulsar parameter files to smooth.")

    for par_filename in tqdm(pulsar_files, desc="Smoothing Files"):
        pulsar_name = par_filename.split('_')[0]
        tim_filename = f"{pulsar_name}_NANOGrav_15y_nb.tim" # Assuming standard naming for .tim files

        par_path = os.path.join(par_dir, par_filename)
        tim_path = os.path.join(tim_dir, tim_filename)

        if not os.path.exists(tim_path):
            log.warning(f"No corresponding .tim file found for {par_filename}. Skipping.")
            continue

        # Define output paths for the smoothed files
        smoothed_par_path = os.path.join(smoothed_par_dir, par_filename)
        smoothed_tim_path = os.path.join(smoothed_tim_dir, tim_filename)

        try:
            # 1. Read the data with PINT
            model = models.get_model(par_path)
            toas = toa.get_TOAs(tim_path, ephem="DE440", planets=True)

            # 2. Write the data back out in a standard format
            with open(smoothed_par_path, 'w') as f:
                f.write(model.as_parfile())
            
            toas.write_TOA_file(smoothed_tim_path, format='tempo2')
            
            log.success(f"Successfully smoothed {pulsar_name}")

        except Exception as e:
            log.error(f"Could not process {pulsar_name}. Error: {e}. Skipping this pulsar.")
            # Optionally, you can create a file to log the names of failed pulsars
            with open('failed_pulsars.log', 'a') as f:
                f.write(f"{pulsar_name}\n")

    log.info("Smoothing process complete.")

if __name__ == '__main__':
    NANOGRAV_BASE_DIR = r'C:/Users/keatw/Downloads/NANOGrav15yr_PulsarTiming_v2.1.0/NANOGrav15yr_PulsarTiming_v2.1.0'
    smooth_files(NANOGRAV_BASE_DIR)