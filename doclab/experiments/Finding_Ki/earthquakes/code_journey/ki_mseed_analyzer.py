from obspy import read
import numpy as np
import os
from pathlib import Path

def process_mseed_file(file_path, ki_freq=4.18879, band_width=0.05):
    st = read(file_path)
    results = []

    for tr in st:
        tr.detrend("demean")
        tr.detrend("linear")

        n = len(tr.data)
        dt = tr.stats.delta
        freqs = np.fft.rfftfreq(n, d=dt)
        fft_vals = np.abs(np.fft.rfft(tr.data))

        # Define frequency band around Ki
        band = (freqs > (ki_freq - band_width)) & (freqs < (ki_freq + band_width))
        band_energy = np.mean(fft_vals[band])
        baseline = np.mean(fft_vals) + 3 * np.std(fft_vals)

        if band_energy > baseline:
            results.append((tr.id, tr.stats.starttime, band_energy, baseline))

    return results

def scan_folder_for_ki(folder_path):
    folder = Path(folder_path)
    all_results = []

    for file in folder.glob("*.mseed"):
        file_results = process_mseed_file(file)
        if file_results:
            all_results.append((file.name, file_results))

    return all_results

if __name__ == "__main__":
    folder = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Ki/Gyroscope Data"
    ki_hits = scan_folder_for_ki(folder)
    for filename, entries in ki_hits:
        print(f"\n{filename}:")
        for trace_id, time, energy, baseline in entries:
            print(f"  ⚡ {trace_id} @ {time} → Energy: {energy:.2f}, Threshold: {baseline:.2f}")
