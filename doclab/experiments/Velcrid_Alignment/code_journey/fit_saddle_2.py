import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
import os

def refined_saddle_model(X, c0, c1, c2, c3):
    """
    Defines the more flexible energy law E ≈ c₀ + c₁μ² + c₂κ² + c₃σ.
    
    Args:
        X (tuple): A tuple containing the independent variables (μ, κ, σ).
        c0, c1, c2, c3 (float): The coefficients to be fitted.
        
    Returns:
        The predicted energy E (approximated by Drift).
    """
    mu, kappa, sigma = X
    
    # Scaling remains important for numerical stability during fitting
    mu_scaled = mu * 1e3
    kappa_scaled = kappa
    sigma_scaled = sigma * 1e5
    
    # The refined model equation
    energy = c0 + (c1 * mu_scaled**2) + (c2 * kappa_scaled**2) + (c3 * sigma_scaled)
    
    return energy

def fit_and_visualize_saddle(df: pd.DataFrame, output_filename='saddle_fit_refined.png'):
    """
    Performs non-linear regression with the refined model and visualizes the result.
    """
    print("Performing regression with the refined saddle model...")
    
    # --- 1. Prepare the data ---
    mu = df['velcridance_score']
    kappa = df['kurtosis_score']
    sigma = df['radiance_score']
    energy = df['drift_score']

    x_data = (mu, kappa, sigma)
    y_data = energy

    # --- 2. Run the optimization with the new model ---
    popt, pcov = curve_fit(refined_saddle_model, x_data, y_data)
    c0, c1, c2, c3 = popt

    # --- 3. Calculate and report the results ---
    residuals = y_data - refined_saddle_model(x_data, *popt)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_data - np.mean(y_data))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    print("\n" + "="*50 + "\nRefined Saddle-Fit Regression Results\n" + "="*50)
    print(f"Fitted Law: E ≈ {c0:.4f} + ({c1:.4f})μ² + ({c2:.4f})κ² + ({c3:.4f})σ")
    print(f"R-squared (Goodness of Fit): {r_squared:.4f}")
    print("="*50 + "\n")

    # --- 4. Visualize with a "zoomed-in" view ---
    print("Generating zoomed-in 3D visualization...")
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot original data points
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    for cat, group in df.groupby('category'):
        ax.scatter(group['velcridance_score'], group['kurtosis_score'], group['drift_score'], s=80,
                   c=colors.get(cat), label=cat.capitalize(), edgecolor='k', alpha=0.9)

    # Create a meshgrid for the fitted surface
    mu_surf = np.linspace(mu.min(), mu.max(), 20)
    kappa_surf = np.linspace(kappa.min(), kappa.max(), 20)
    mu_mesh, kappa_mesh = np.meshgrid(mu_surf, kappa_surf)
    sigma_const = np.full_like(mu_mesh, sigma.mean())
    
    energy_fit = refined_saddle_model((mu_mesh, kappa_mesh, sigma_const), *popt)
    
    # Plot the refined fitted surface
    ax.plot_surface(mu_mesh, kappa_mesh, energy_fit, cmap='viridis', alpha=0.3)

    # --- Set axis limits to "zoom in" on the data cluster ---
    ax.set_xlim(mu.min()*1.1, mu.max()*1.1)
    ax.set_ylim(kappa.min()*0.9, kappa.max()*1.1)
    ax.set_zlim(energy.min()*1.1, energy.max()*1.1)
    
    ax.set_xlabel('Velcridance (μ)')
    ax.set_ylabel('Kurtosis (κ)')
    ax.set_zlabel('Drift (E)')
    ax.set_title('Data vs. Refined Saddle Model (Zoomed)')
    ax.legend()
    
    plt.savefig(output_filename, dpi=300)
    print(f"✅ Refined validation plot saved as '{output_filename}'")
    plt.show()


if __name__ == '__main__':
    RESULTS_CSV = "vr_analysis_results_4d_2.csv"
    if not os.path.exists(RESULTS_CSV):
        print(f"Error: Results file '{RESULTS_CSV}' not found.")
    else:
        df = pd.read_csv(RESULTS_CSV)
        fit_and_visualize_saddle(df)