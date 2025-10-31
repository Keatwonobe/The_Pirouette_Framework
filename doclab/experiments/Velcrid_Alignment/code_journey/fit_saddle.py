import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from scipy.optimize import curve_fit
import os

def saddle_model(X, lambda_coeff):
    """
    Defines the provisional energy law E ≈ μ² – κ² + λσ.
    
    Args:
        X (tuple): A tuple containing the independent variables (μ, κ, σ).
        lambda_coeff (float): The coefficient λ to be fitted.
        
    Returns:
        The predicted energy E (approximated by Drift).
    """
    mu, kappa, sigma = X
    # Note: We scale the scores to prevent the μ² term from dominating
    # and to make the coefficients more interpretable.
    mu_scaled = mu * 1e3
    kappa_scaled = kappa
    sigma_scaled = sigma * 1e5
    
    # The core model equation
    energy = (mu_scaled**2) - (kappa_scaled**2) + (lambda_coeff * sigma_scaled)
    
    return energy

def fit_and_visualize_saddle(df: pd.DataFrame, output_filename='saddle_fit_validation.png'):
    """
    Performs non-linear regression to fit the saddle model and visualizes the result.
    """
    print("Performing non-linear regression to fit the saddle model...")
    
    # --- 1. Prepare the data from the DataFrame ---
    # Map the conceptual variables to the CSV columns
    mu = df['velcridance_score']
    kappa = df['kurtosis_score']
    sigma = df['radiance_score']
    energy = df['drift_score'] # E is represented by the Drift

    # The independent variables for curve_fit
    x_data = (mu, kappa, sigma)
    # The dependent variable we want to predict
    y_data = energy

    # --- 2. Run the curve-fit optimization ---
    # `popt` will contain the optimized value for lambda_coeff
    # `pcov` will contain the covariance matrix
    popt, pcov = curve_fit(saddle_model, x_data, y_data)
    
    # Extract the fitted coefficient
    fitted_lambda = popt[0]
    
    # --- 3. Calculate Goodness of Fit (R-squared) ---
    residuals = y_data - saddle_model(x_data, fitted_lambda)
    ss_res = np.sum(residuals**2)
    ss_tot = np.sum((y_data - np.mean(y_data))**2)
    r_squared = 1 - (ss_res / ss_tot)
    
    print("\n" + "="*50 + "\nSaddle-Fit Regression Results\n" + "="*50)
    print(f"Fitted Energy Law: E ≈ (1000μ)² – κ² + ({fitted_lambda:.4f}) ⋅ (100000σ)")
    print(f"Optimal λ (lambda) coefficient: {fitted_lambda:.4f}")
    print(f"R-squared (Goodness of Fit): {r_squared:.4f}")
    print("="*50 + "\n")

    # --- 4. Visualize the results ---
    print("Generating 3D visualization of the data and the fitted model...")
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')
    
    # Plot the original data points
    colors = {'radiant': 'gold', 'velcrid': 'darkblue'}
    for cat, group in df.groupby('category'):
        ax.scatter(group['velcridance_score'], group['kurtosis_score'], group['drift_score'], s=80,
                   c=colors.get(cat), label=cat.capitalize(), edgecolor='k', alpha=0.9)

    # Create a meshgrid to plot the fitted surface
    mu_surf = np.linspace(mu.min(), mu.max(), 20)
    kappa_surf = np.linspace(kappa.min(), kappa.max(), 20)
    mu_mesh, kappa_mesh = np.meshgrid(mu_surf, kappa_surf)
    
    # For the surface, we use the mean value of sigma as a representative value
    sigma_const = np.full_like(mu_mesh, sigma.mean())
    
    # Calculate the energy (Drift) for each point on the surface using the fitted model
    energy_fit = saddle_model((mu_mesh, kappa_mesh, sigma_const), fitted_lambda)
    
    # Plot the transparent fitted surface
    ax.plot_surface(mu_mesh, kappa_mesh, energy_fit, cmap='viridis', alpha=0.4, rstride=1, cstride=1)

    ax.set_xlabel('Velcridance (μ)')
    ax.set_ylabel('Kurtosis (κ)')
    ax.set_zlabel('Drift (E)')
    ax.set_title('Original Data vs. Fitted Saddle Model')
    ax.legend()
    
    plt.savefig(output_filename, dpi=300)
    print(f"✅ Validation plot saved as '{output_filename}'")
    plt.show()


if __name__ == '__main__':
    RESULTS_CSV = "vr_analysis_results_4d_2.csv"
    if not os.path.exists(RESULTS_CSV):
        print(f"Error: Results file '{RESULTS_CSV}' not found.")
    else:
        df = pd.read_csv(RESULTS_CSV)
        fit_and_visualize_saddle(df)