import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("daily_avalanche_slopes.csv")
df["t"] = range(len(df))

plt.figure(figsize=(8,5))
plt.plot(df["t"], df["alpha"], marker="o", linewidth=2)
plt.axhline(-1.0, color="red", linestyle="--", label="α = -1 (critical)")
plt.xlabel("Time window (hours)")
plt.ylabel("Avalanche exponent α")
plt.title("Temporal Γ-sweep in Higgs Twitter cascade")
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()
plt.savefig("gamma_sweep_combined.png", dpi=150)