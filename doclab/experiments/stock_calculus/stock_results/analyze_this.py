import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
market_df = pd.read_csv('market_archetypes.csv')
helical_df = pd.read_csv('helical_summary.csv')

# Set plot style
sns.set_style("whitegrid")
fig, axes = plt.subplots(1, 2, figsize=(16, 7))

# Plot Market Data
sns.scatterplot(
    data=market_df,
    x='intrinsic_kappa',
    y='performance_score',
    ax=axes[0],
    alpha=0.6,
    edgecolor='k'
)
axes[0].set_title('Market Phase Space', fontsize=16)
axes[0].set_xlabel('Intrinsic Kappa', fontsize=12)
axes[0].set_ylabel('Performance Score', fontsize=12)
axes[0].set_xscale('log') # Using log scale based on the provided image

# Plot Helical Data
sns.scatterplot(
    data=helical_df,
    x='kappa_abs_med',
    y='delta_power_med',
    hue='archetype',
    ax=axes[1],
    alpha=0.7,
    edgecolor='k',
    palette='viridis'
)
axes[1].set_title('Helical Phase Space', fontsize=16)
axes[1].set_xlabel('Median Absolute Kappa', fontsize=12)
axes[1].set_ylabel('Median Delta Power', fontsize=12)

plt.tight_layout()
plt.show()