# wada_experiment_suite.py
#
# Drop this next to wada_lookup_race.py.
# The only thing you MUST edit is build_graphs_from_oracle()
# to call your existing oracle + network builders.

import numpy as np
import matplotlib.pyplot as plt
from dataclasses import dataclass
from typing import List, Tuple
import random
import time

import torch
import torch.nn as nn
import torch.optim as optim


# ------------------------------------------------------------
# 0. Graph + Ising boilerplate
# ------------------------------------------------------------

@dataclass
class GraphIsingSystem:
    points: np.ndarray          # (N, 2) coordinates
    adj_list: List[List[int]]   # neighbors for each node
    name: str = "graph"

    def num_nodes(self) -> int:
        return self.points.shape[0]


def _ising_sweep(spins: np.ndarray,
                 adj_list: List[List[int]],
                 T: float,
                 beta: float = 1.0) -> None:
    """
    Single Metropolis sweep over all spins. In-place update.
    """
    N = spins.shape[0]
    invT = beta / T
    for i in range(N):
        s = spins[i]
        # local field from neighbors
        h = 0.0
        for j in adj_list[i]:
            h += spins[j]
        dE = 2.0 * s * h
        if dE <= 0.0:
            spins[i] = -s
        else:
            if random.random() < np.exp(-invT * dE):
                spins[i] = -s


def run_ising(graph: GraphIsingSystem,
              temps: np.ndarray,
              n_equil: int = 200,
              n_samples: int = 200,
              sample_interval: int = 5,
              seed: int = 0) -> np.ndarray:
    """
    Runs an Ising model on a given graph for a set of temperatures.
    Returns <|M|> per temperature.
    """
    rng = np.random.default_rng(seed)
    N = graph.num_nodes()
    mags = []

    for T in temps:
        # random initial spins
        spins = rng.choice([-1, 1], size=N).astype(np.int8)

        # Equilibration
        for _ in range(n_equil):
            _ising_sweep(spins, graph.adj_list, T)

        # Sampling
        m_acc = 0.0
        m_count = 0
        for step in range(n_samples):
            for _ in range(sample_interval):
                _ising_sweep(spins, graph.adj_list, T)
            m = np.abs(spins.mean())
            m_acc += m
            m_count += 1

        mags.append(m_acc / m_count)

    return np.array(mags)


# ------------------------------------------------------------
# 1. Simple graph learner (tiny GNN-ish regressor)
# ------------------------------------------------------------

class SimpleGraphMagNet(nn.Module):
    """
    Very small 'GNN':
      - Input: spins (N,1)
      - Layer 1: linear + ReLU
      - Aggregation: neighbor-average using adjacency matrix
      - Layer 2: linear + ReLU
      - Readout: mean over nodes -> scalar magnetization prediction
    """
    def __init__(self, hidden_dim: int = 32):
        super().__init__()
        self.lin1 = nn.Linear(1, hidden_dim)
        self.lin2 = nn.Linear(hidden_dim, hidden_dim)
        self.out = nn.Linear(hidden_dim, 1)

    def forward(self, spins: torch.Tensor,
                agg_idx: torch.Tensor,
                agg_ptr: torch.Tensor) -> torch.Tensor:
        """
        spins: (N, 1)
        agg_idx, agg_ptr encode adjacency in CSR style:

        for node i:
           neighbors are agg_idx[agg_ptr[i]:agg_ptr[i+1]]
        """
        x = self.lin1(spins)
        x = torch.relu(x)

        N = spins.shape[0]
        # Aggregate neighbors: simple mean
        agg_x = torch.zeros_like(x)
        for i in range(N):
            start = agg_ptr[i].item()
            end = agg_ptr[i+1].item()
            if end > start:
                neigh = agg_idx[start:end]
                agg_x[i] = x[neigh].mean(dim=0)
            else:
                agg_x[i] = x[i]

        x = self.lin2(agg_x)
        x = torch.relu(x)

        # Global readout: mean over nodes
        g = x.mean(dim=0, keepdim=True)
        out = self.out(g)  # (1,1)
        return out.squeeze()


def adj_to_csr(adj_list: List[List[int]]) -> Tuple[torch.Tensor, torch.Tensor]:
    """
    Convert Python adjacency list to CSR-like (idx, ptr) tensors.
    """
    idx = []
    ptr = [0]
    for neigh in adj_list:
        idx.extend(neigh)
        ptr.append(len(idx))
    idx = torch.tensor(idx, dtype=torch.long)
    ptr = torch.tensor(ptr, dtype=torch.long)
    return idx, ptr


def make_ising_dataset(graph: GraphIsingSystem,
                       temps: np.ndarray,
                       n_configs_per_T: int = 100,
                       n_equil: int = 200,
                       sample_interval: int = 10,
                       seed: int = 0):
    """
    Returns:
      X_spins: list of np arrays (N,)   (spin configs)
      X_T:     list of float            (temperatures)
      y_M:     list of float            (true |M|)
    """
    rng = np.random.default_rng(seed)
    N = graph.num_nodes()
    X_spins, X_T, y_M = [], [], []

    for T in temps:
        spins = rng.choice([-1, 1], size=N).astype(np.int8)
        for _ in range(n_equil):
            _ising_sweep(spins, graph.adj_list, T)

        for _ in range(n_configs_per_T):
            for _ in range(sample_interval):
                _ising_sweep(spins, graph.adj_list, T)
            m = np.abs(spins.mean())
            X_spins.append(spins.copy())
            X_T.append(float(T))
            y_M.append(float(m))

    return X_spins, X_T, y_M


def train_mag_learner(graph: GraphIsingSystem,
                      temps: np.ndarray,
                      n_configs_per_T: int = 50,
                      n_epochs: int = 40,
                      lr: float = 1e-3,
                      seed: int = 0):
    """
    Train SimpleGraphMagNet on (spins -> magnetization).
    Returns training and validation loss curves.
    """
    X_spins, X_T, y_M = make_ising_dataset(
        graph, temps,
        n_configs_per_T=n_configs_per_T,
        seed=seed
    )
    N = graph.num_nodes()
    X_spins = np.stack(X_spins)           # (K, N)
    y_M = np.array(y_M)                   # (K,)

    # Train/val split
    K = X_spins.shape[0]
    perm = np.random.permutation(K)
    split = int(0.8 * K)
    train_idx = perm[:split]
    val_idx = perm[split:]

    spins_train = torch.tensor(X_spins[train_idx], dtype=torch.float32)
    spins_val   = torch.tensor(X_spins[val_idx],   dtype=torch.float32)
    y_train = torch.tensor(y_M[train_idx], dtype=torch.float32)
    y_val   = torch.tensor(y_M[val_idx],   dtype=torch.float32)

    # Reshape to (batch, N, 1)
    spins_train = spins_train.unsqueeze(-1)
    spins_val   = spins_val.unsqueeze(-1)

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    model = SimpleGraphMagNet(hidden_dim=32).to(device)
    optimizer = optim.Adam(model.parameters(), lr=lr)
    loss_fn = nn.MSELoss()

    agg_idx, agg_ptr = adj_to_csr(graph.adj_list)
    agg_idx = agg_idx.to(device)
    agg_ptr = agg_ptr.to(device)

    spins_train = spins_train.to(device)
    spins_val   = spins_val.to(device)
    y_train = y_train.to(device)
    y_val   = y_val.to(device)

    train_losses = []
    val_losses = []

    for epoch in range(n_epochs):
        model.train()
        optimizer.zero_grad()

        # We do full-batch training for simplicity
        preds = []
        for b in range(spins_train.shape[0]):
            pred = model(spins_train[b], agg_idx, agg_ptr)
            preds.append(pred)
        preds = torch.stack(preds)
        loss = loss_fn(preds, y_train)
        loss.backward()
        optimizer.step()

        model.eval()
        with torch.no_grad():
            preds_val = []
            for b in range(spins_val.shape[0]):
                pv = model(spins_val[b], agg_idx, agg_ptr)
                preds_val.append(pv)
            preds_val = torch.stack(preds_val)
            val_loss = loss_fn(preds_val, y_val)

        train_losses.append(loss.item())
        val_losses.append(val_loss.item())
        print(f"[{graph.name}] Epoch {epoch+1}/{n_epochs}  "
              f"train={loss.item():.4f}  val={val_loss.item():.4f}")

    return train_losses, val_losses


# ------------------------------------------------------------
# 2. Where you plug in your existing oracle + networks
# ------------------------------------------------------------

def build_graphs_from_oracle() -> Tuple[GraphIsingSystem, GraphIsingSystem]:
    """
    !!! EDIT THIS FUNCTION !!!

    This is the only part that needs to know about your existing
    wada_lookup_race.py code.

    Goal:
      - Construct a Wada graph and a regular grid graph
      - Return them as GraphIsingSystem objects

    Skeleton below assumes you’ll import helpers from your old script.
    Replace the dummy code with real calls.
    """
    # Example: import your builders
    # from wada_lookup_race import (
    #     build_oracle_map,
    #     sample_wada_network,
    #     build_regular_grid_network,
    # )

    # --- BEGIN: dummy placeholder (replace with your real stuff) ---
    # This creates two simple graphs just so the script runs.
    # You should remove everything in this block and use your true builders.

    N = 1000
    # "Regular" as a 2D grid
    L = int(np.sqrt(N))
    xs, ys = np.meshgrid(np.linspace(-1, 1, L), np.linspace(-1, 1, L))
    pts_reg = np.column_stack([xs.ravel(), ys.ravel()])
    adj_reg = [[] for _ in range(L*L)]
    def idx(i, j): return i*L + j
    for i in range(L):
        for j in range(L):
            u = idx(i, j)
            for di, dj in [(-1,0), (1,0), (0,-1), (0,1)]:
                ni, nj = i+di, j+dj
                if 0 <= ni < L and 0 <= nj < L:
                    v = idx(ni, nj)
                    adj_reg[u].append(v)

    # "Wada" as random geometric graph (stand-in for your fractal sampling)
    rng = np.random.default_rng(0)
    pts_wada = rng.uniform(-1, 1, size=(N, 2))
    from scipy.spatial import Delaunay
    tri = Delaunay(pts_wada)
    adj_wada = [set() for _ in range(N)]
    for simp in tri.simplices:
        for a in range(3):
            u = simp[a]
            v = simp[(a+1) % 3]
            adj_wada[u].add(v)
            adj_wada[v].add(u)
    adj_wada = [list(s) for s in adj_wada]
    # --- END: dummy placeholder ---

    g_wada = GraphIsingSystem(points=pts_wada, adj_list=adj_wada, name="Wada")
    g_reg  = GraphIsingSystem(points=pts_reg,  adj_list=adj_reg,  name="Regular")
    return g_wada, g_reg


# ------------------------------------------------------------
# 3. The “this is worth investigating” panel
# ------------------------------------------------------------

def run_experiment_suite():
    # 3.1 Build graphs
    g_wada, g_reg = build_graphs_from_oracle()

    # 3.2 Physics: magnetization curves
    TEMPS = np.linspace(1.0, 4.0, 11)

    print("[*] Running Ising on Wada graph...")
    t0 = time.time()
    mag_wada = run_ising(g_wada, TEMPS, seed=1)
    print(f"    done in {time.time()-t0:.2f}s")

    print("[*] Running Ising on regular grid...")
    t0 = time.time()
    mag_reg = run_ising(g_reg, TEMPS, seed=2)
    print(f"    done in {time.time()-t0:.2f}s")

    # 3.3 Learners
    print("[*] Training learner on Wada graph...")
    t0 = time.time()
    tr_w, vl_w = train_mag_learner(
        g_wada, TEMPS,
        n_configs_per_T=20,
        n_epochs=30,
        seed=0
    )
    print(f"    done in {time.time()-t0:.2f}s")

    print("[*] Training learner on regular grid...")
    t0 = time.time()
    tr_r, vl_r = train_mag_learner(
        g_reg, TEMPS,
        n_configs_per_T=20,
        n_epochs=30,
        seed=1
    )
    print(f"    done in {time.time()-t0:.2f}s")

    # 3.4 Degree distributions
    deg_wada = [len(n) for n in g_wada.adj_list]
    deg_reg  = [len(n) for n in g_reg.adj_list]

    # --------------------------------------------------------
    # Plot: 3 panels
    # --------------------------------------------------------
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))

    # Panel 1: magnetization curves
    ax = axes[0]
    ax.plot(TEMPS, mag_wada, 'o-', label='Wada network')
    ax.plot(TEMPS, mag_reg, 's--', label='Regular grid')
    ax.set_xlabel("Temperature T")
    ax.set_ylabel(r"Magnetization $\langle |M| \rangle$")
    ax.set_title("Phase transition: Wada vs Regular")
    ax.legend()
    ax.grid(True)

    # Panel 2: learner validation loss
    ax = axes[1]
    ax.plot(vl_w, 'o-', label='Wada val loss')
    ax.plot(vl_r, 's--', label='Regular val loss')
    ax.set_xlabel("Epoch")
    ax.set_ylabel("MSE (|M| prediction)")
    ax.set_title("Simple learner performance")
    ax.legend()
    ax.grid(True)

    # Panel 3: degree distribution
    ax = axes[2]
    ax.hist(deg_wada, bins=range(0, max(deg_wada+deg_reg)+2),
            alpha=0.6, label='Wada')
    ax.hist(deg_reg,  bins=range(0, max(deg_wada+deg_reg)+2),
            alpha=0.6, label='Regular')
    ax.set_xlabel("Node degree")
    ax.set_ylabel("Count")
    ax.set_title("Topology contrast")
    ax.legend()
    ax.grid(True)

    plt.tight_layout()
    plt.savefig("wada_experiment_panel.png", dpi=150)
    plt.show()


if __name__ == "__main__":
    run_experiment_suite()
