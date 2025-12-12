import numpy as np
import igraph as ig
import matplotlib.pyplot as plt
import collections

# --- SCRIPT CONFIGURATION ---
FNAME = "higgs_hodge_out.npz"
# A tunable parameter from your framework. k_Gamma=1.0 means a direct comparison.
# You can increase this to find only stronger cascades.
K_GAMMA = 1.0

# 1. Load the pre-computed Hodge decomposition data
print(f"Loading data from {FNAME}...")
data = np.load(FNAME, allow_pickle=True)
edges = data['edges']
grad_part = data['grad']
curl_part = data['curl']

# 2. Define and identify local cascade events
# An edge is in a "cascade state" if its local curl energy exceeds its local gradient energy.
# This is the microscopic version of your framework's core Θ > Θ_c test.
curl_energy = curl_part**2
grad_energy = grad_part**2

cascade_mask = curl_energy > (K_GAMMA * grad_energy)
cascade_edges = edges[cascade_mask]

print(f"\nFound {len(cascade_edges)} edges participating in local cascades.")

# If no cascades are found, exit gracefully.
if len(cascade_edges) == 0:
    print("This network is purely gradient-dominated. No avalanche dimension to measure.")
else:
    # 3. Build a graph of only the cascade clusters
    print("Building cascade-only subgraph...")
    G_cascade = ig.Graph.TupleList(cascade_edges, directed=False)

    # 4. Measure the size of each "avalanche"
    # The size is the number of edges in each connected component of the cascade graph.
    # We call .subgraphs() to get actual graph objects for each component.
    component_subgraphs = G_cascade.components(mode='strong').subgraphs()
    avalanche_sizes = [comp.ecount() for comp in component_subgraphs if comp.ecount() > 0]

    print(f"Identified {len(avalanche_sizes)} distinct avalanche clusters.")
    print(f"Largest avalanche involves {max(avalanche_sizes) if avalanche_sizes else 0} edges.")

    # 5. Analyze and plot the distribution of avalanche sizes
    size_counts = collections.Counter(avalanche_sizes)
    sizes = np.array(list(size_counts.keys()))
    counts = np.array(list(size_counts.values()))

    # Sort for plotting
    sort_indices = np.argsort(sizes)
    sizes = sizes[sort_indices]
    counts = counts[sort_indices]

    # --- PLOTTING ---
    plt.figure(figsize=(12, 6))

    # Linear plot
    plt.subplot(1, 2, 1)
    plt.bar(sizes, counts, width=0.8, align='center')
    plt.xlabel("Avalanche Size (number of edges)")
    plt.ylabel("Frequency (count)")
    plt.title("Avalanche Size Distribution")
    plt.xscale('log')
    plt.yscale('log')
    
    # Log-log plot to test for power law
    plt.subplot(1, 2, 2)
    plt.scatter(sizes, counts)
    plt.xlabel("Avalanche Size (log scale)")
    plt.ylabel("Frequency (log scale)")
    plt.title("Log-Log Plot")
    plt.xscale('log')
    plt.yscale('log')
    # Fit a line to check for power-law behavior
    if len(sizes) > 1:
        log_sizes = np.log10(sizes)
        log_counts = np.log10(counts)
        # Fit a line (ignoring potential zeros)
        m, c = np.polyfit(log_sizes[np.isfinite(log_counts)], log_counts[np.isfinite(log_counts)], 1)
        plt.plot(sizes, 10**(m*np.log10(sizes) + c), color='red', linestyle='--', label=f'Power Law Fit (slope α={m:.2f})')
        plt.legend()

    plt.tight_layout()
    plt.savefig("higgs_avalanche_distribution.png")
    print("\nAnalysis complete. Plot saved to 'higgs_avalanche_distribution.png'")