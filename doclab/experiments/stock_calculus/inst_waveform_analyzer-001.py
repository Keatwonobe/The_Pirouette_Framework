# INST-WAVEFORM-ANALYZER-001 :: Pirouette Coherence Analyzer
# id: INST-WAVEFORM-ANALYZER-001
# version: 1.1
# parents: [DOMA-206]
#
# ABSTRACT: This script operationalizes the Pirouette Waveform model (DOMA-206)
# as a diagnostic instrument. It takes a one-dimensional time-series dataset
# (representing the "shadow") and searches for its hidden, three-dimensional
# helical coherence (the "form"). The experiment posits that seemingly chaotic
# data, like financial markets, contains a latent "Chirality Factor" (kappa)
# that reveals a more ordered, geometric structure when projected into 3D.
# This kappa is a measure of the system's rotational momentum or memory.
#
# VERSION 1.1 UPDATE: Added error handling for data fetching failures to prevent
# crashes when the yfinance API is rate-limited or unavailable.

import yfinance as yf
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import sys

def fetch_market_data(ticker, start_date, end_date):
    """
    Fetches historical market data for a given ticker.
    This represents the "unintelligible," 1D time-series data.
    """
    print(f"Fetching S&P 500 data ('{ticker}') from {start_date} to {end_date}...")
    data = yf.download(ticker, start=start_date, end=end_date, progress=False)

    # --- ROBUSTNESS FIX ---
    # Check if the download failed and the dataframe is empty. This handles
    # rate limiting, invalid tickers, or connection issues gracefully.
    if data.empty:
        print("\n--- DATA FETCH FAILED ---")
        print("The script could not download market data from Yahoo Finance.")
        print("This may be due to:")
        print("  1. API Rate Limiting: Please wait a minute and try again.")
        print("  2. An invalid ticker symbol or date range.")
        print("  3. A network connection issue.")
        print("Exiting script.")
        sys.exit(1) # Exit gracefully instead of crashing.
    
    price = data['Close'].values
    # Normalize the data to oscillate around zero, fitting the waveform model.
    normalized_price = 2 * ((price - np.min(price)) / (np.max(price) - np.min(price))) - 1
    return normalized_price

def calculate_coherence(data_3d):
    """
    Calculates the coherence of a 3D path. A more coherent path is "smoother."
    We measure this by calculating the total "bending energy" or the mean squared
    curvature. A lower value indicates a more coherent, less jagged path.
    This metric quantifies how well the chosen kappa resolves the 2D noise
    into a smooth 3D helix.
    """
    # Calculate the first derivative (velocity vectors)
    velocities = np.diff(data_3d, axis=0)
    # Calculate the second derivative (acceleration vectors)
    accelerations = np.diff(velocities, axis=0)
    # Use the magnitude of acceleration as a proxy for curvature/jerkiness.
    # A smooth helix has constant velocity magnitude and low acceleration.
    coherence_metric = np.sum(np.linalg.norm(accelerations, axis=1)**2)
    return coherence_metric

def find_optimal_kappa(data_1d, kappa_range, num_steps):
    """
    Iterates through a range of Chirality Factors (kappa) to find the one
    that produces the most coherent 3D waveform.
    This is the core of the INST-WAVEFORM-ANALYZER.
    """
    print(f"Scanning for optimal kappa across {num_steps} steps...")
    kappas = np.linspace(kappa_range[0], kappa_range[1], num_steps)
    coherence_scores = []
    
    t = np.arange(len(data_1d))

    for kappa in kappas:
        # Project the 1D data into a 3D Pirouette Waveform
        # As per DOMA-206, the data's amplitude modulates the helix.
        x = data_1d * np.cos(kappa * t)
        y = data_1d * np.sin(kappa * t)
        z = t / len(t) # Normalize time axis for consistent plotting
        
        data_3d = np.vstack([x, y, z]).T
        
        score = calculate_coherence(data_3d)
        coherence_scores.append(score)

    # The optimal kappa is the one that MINIMIZES the coherence score (maximizes smoothness)
    min_score_index = np.argmin(coherence_scores)
    optimal_kappa = kappas[min_score_index]
    
    return optimal_kappa, kappas, coherence_scores

def plot_results(data_1d, optimal_kappa, kappas, coherence_scores):
    """
    Visualizes the results of the analysis to make the findings tangible.
    """
    print(f"Optimal Chirality Factor (κ) found: {optimal_kappa:.6f}")
    
    fig = plt.figure(figsize=(18, 12))
    fig.suptitle("Pirouette Waveform Analysis of S&P 500 Data", fontsize=20)
    
    # 1. Plot the original 2D "shadow" data
    ax1 = fig.add_subplot(2, 2, 1)
    ax1.plot(data_1d, color='gray')
    ax1.set_title("1. Original 1D Time Series (The 'Shadow')", fontsize=14)
    ax1.set_xlabel("Time (Days)")
    ax1.set_ylabel("Normalized Price")
    ax1.grid(True, linestyle='--', alpha=0.5)

    # 2. Plot the coherence scan
    ax2 = fig.add_subplot(2, 2, 2)
    ax2.plot(kappas, coherence_scores, color='purple')
    ax2.axvline(optimal_kappa, color='red', linestyle='--', label=f'Optimal κ = {optimal_kappa:.6f}')
    ax2.set_title("2. Coherence Scan (Finding the Hidden Geometry)", fontsize=14)
    ax2.set_xlabel("Chirality Factor (κ)")
    ax2.set_ylabel("Incoherence Score (Lower is Better)")
    ax2.legend()
    ax2.grid(True, linestyle='--', alpha=0.5)

    # 3. Plot the 3D waveform with kappa = 0 (the incoherent projection)
    ax3 = fig.add_subplot(2, 2, 3, projection='3d')
    t = np.arange(len(data_1d))
    x0 = data_1d
    y0 = np.zeros_like(data_1d) # With kappa=0, sin(0*t) is always 0
    z0 = t / len(t)
    ax3.plot(x0, y0, z0, color='black', alpha=0.7)
    ax3.set_title("3. Projection with κ = 0 (The Flat 'Noise')", fontsize=14)
    ax3.set_xlabel("X (cos)")
    ax3.set_ylabel("Y (sin)")
    ax3.set_zlabel("Time")

    # 4. Plot the 3D waveform with the optimal kappa (the resolved form)
    ax4 = fig.add_subplot(2, 2, 4, projection='3d')
    x_opt = data_1d * np.cos(optimal_kappa * t)
    y_opt = data_1d * np.sin(optimal_kappa * t)
    z_opt = t / len(t)
    ax4.plot(x_opt, y_opt, z_opt, color='red', alpha=0.9)
    ax4.set_title(f"4. Projection with Optimal κ = {optimal_kappa:.6f} (The 'Form')", fontsize=14)
    ax4.set_xlabel("X (cos)")
    ax4.set_ylabel("Y (sin)")
    ax4.set_zlabel("Time")
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.95])
    plt.show()

if __name__ == '__main__':
    # --- EXPERIMENT PARAMETERS ---
    # We will analyze the volatile period of the 2008 financial crisis.
    # This period of high "temporal pressure" (V_Gamma) should reveal a
    # strong, non-zero chiral signature.
    TICKER = '^GSPC'
    START_DATE = '2007-01-01'
    END_DATE = '2010-01-01'
    
    # The range of kappa to search. Small values often have large effects.
    KAPPA_RANGE = (0, 0.1)
    KAPPA_STEPS = 500 # The resolution of our "instrument"

    # --- EXECUTION ---
    # 1. Fetch the data (the known)
    market_data_1d = fetch_market_data(TICKER, START_DATE, END_DATE)
    
    # 2. Analyze for hidden geometry (bridge to the unknown)
    opt_kappa, kappas, scores = find_optimal_kappa(market_data_1d, KAPPA_RANGE, KAPPA_STEPS)
    
    # 3. Visualize the claim
    plot_results(market_data_1d, opt_kappa, kappas, scores)

