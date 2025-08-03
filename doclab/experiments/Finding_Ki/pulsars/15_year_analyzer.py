import os
import matplotlib.pyplot as plt
from astropy import units as u

# Imports for the pint-pulsar library
from pint import models, toa, logging
from pint.residuals import Residuals
from loguru import logger as log

# Setup logging
logging.setup(level="INFO")

def find_pulsar_file(directory, pulsar_name, extension):
    """Searches a directory for a file starting with the pulsar name and ending with the extension."""
    for f in os.listdir(directory):
        if f.startswith(pulsar_name) and f.endswith(extension):
            return os.path.join(directory, f)
    return None

def analyze_nanograv_pulsar(base_dir, pulsar_name):
    """
    Analyzes a specific pulsar from the NANOGrav 15-year dataset.
    """
    log.info(f"Starting analysis for pulsar: {pulsar_name}")

    # --- MODIFIED SECTION ---
    # Dynamically find the .par and .tim files instead of building a static name
    par_dir = os.path.join(base_dir, 'narrowband', 'par')
    tim_dir = os.path.join(base_dir, 'narrowband', 'tim')

    par_file_path = find_pulsar_file(par_dir, pulsar_name, '.par')
    tim_file_path = find_pulsar_file(tim_dir, pulsar_name, '.tim')
    # --- END MODIFIED SECTION ---

    if not par_file_path or not tim_file_path:
        log.error(f"Data files not found for {pulsar_name}. Check paths and filenames.")
        if not par_file_path: log.warning(f"Could not find .par file in {par_dir}")
        if not tim_file_path: log.warning(f"Could not find .tim file in {tim_dir}")
        return

    log.info(f"Found PAR file: {os.path.basename(par_file_path)}")
    log.info(f"Found TIM file: {os.path.basename(tim_file_path)}")

    # Load data using pint-pulsar
    try:
        log.info("Loading timing model and TOAs...")
        model = models.get_model(par_file_path)
        t = toa.get_TOAs(tim_file_path, ephem="DE440", planets=True)
    except Exception as e:
        log.error(f"Error loading data for {pulsar_name}: {e}")
        return

    # Calculate and plot residuals
    log.info("Calculating timing residuals and generating plot...")
    residuals = Residuals(t, model).time_resids.to(u.us)
    times = t.get_mjds()
    errors = t.get_errors().to(u.us)

    plt.figure(figsize=(12, 6))
    plt.errorbar(times.value, residuals.value, yerr=errors.value, fmt='x', alpha=0.5, ecolor='lightgray')
    plt.title(f'Timing Residuals for Pulsar {pulsar_name}\n(NANOGrav 15yr Dataset)')
    plt.xlabel('Time (MJD)')
    plt.ylabel('Residuals (µs)')
    plt.grid(True, linestyle='--', alpha=0.6)
    
    output_filename = f'{pulsar_name}_residuals_plot.png'
    plt.savefig(output_filename)
    log.success(f"Plot saved to {output_filename}")
    plt.close()

if __name__ == '__main__':
    # Set the base directory for the NANOGrav dataset
    NANOGRAV_BASE_DIR = r'C:/Users/keatw/Downloads/NANOGrav15yr_PulsarTiming_v2.1.0/NANOGrav15yr_PulsarTiming_v2.1.0'
    PULSAR_TO_ANALYZE = 'J1903+0327'
    
    analyze_nanograv_pulsar(NANOGRAV_BASE_DIR, PULSAR_TO_ANALYZE)