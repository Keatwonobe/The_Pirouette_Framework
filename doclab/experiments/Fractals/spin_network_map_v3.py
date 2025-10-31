import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from scipy.spatial import ConvexHull
import matplotlib.patches as patches

class CausalSet:
    """Represents the discrete structure of spacetime as a growing graph."""
    def __init__(self, num_events):
        self.events = set(range(num_events))
        self.adj = {i: [] for i in self.events}
        self.graph = nx.DiGraph()
        self.graph.add_nodes_from(self.events)
        self.pos = None

    def add_causal_link(self, u, v):
        """Adds a causal link (directed edge) from event u to event v."""
        if u in self.events and v in self.events:
            self.adj[u].append(v)
            self.graph.add_edge(u, v)

    def get_past_cone_size(self, event):
        """Calculates Gamma(ε) as the size of the causal past."""
        return len(nx.ancestors(self.graph, event))

class PirouetteGrowthRule:
    """Implements the dynamic rule for adding new events to the Causal Set."""
    def __init__(self, causal_set):
        self.causal_set = causal_set

    def calculate_coherence_action(self, parent_event):
        """
        Calculates the 'Coherence Action' S_p for birthing a new event
        from a potential parent. This is the core of the 'law of becoming'.
        """
        # In a full model, this would be a complex function.
        # Here, we use the principle from MATH-017: high pressure (dense past)
        # makes new connections less likely, as it's an 'expensive' region.
        gamma = self.causal_set.get_past_cone_size(parent_event)
        # The action is inversely proportional to the pressure.
        # We add 1 to avoid division by zero for the first event.
        return 1.0 / (1.0 + gamma)

    def select_parent_and_birth_new_event(self, current_event_id, antichain):
        """
        Probabilistically selects parents from the antichain (the 'present')
        and adds the new event to the causal set.
        """
        if not antichain:
            return

        actions = np.array([self.calculate_coherence_action(p) for p in antichain])
        
        # Avoid division by zero if all actions are zero
        if np.sum(actions) == 0:
            probabilities = np.ones(len(antichain)) / len(antichain)
        else:
            probabilities = actions / np.sum(actions)

        # Choose one or more parents based on the calculated probabilities
        num_parents = np.random.randint(1, min(4, len(antichain) + 1))
        
        # Ensure antichain is not empty before choosing
        if len(antichain) > 0:
            parents = np.random.choice(antichain, size=num_parents, p=probabilities, replace=False)
            for parent in parents:
                self.causal_set.add_causal_link(parent, current_event_id)

class SpinNetworkLayout:
    """Handles the visualization of the Causal Set."""
    def __init__(self, causal_set):
        self.causal_set = causal_set

    def compute_layout(self):
        """Computes a layered, aesthetically informative layout."""
        # Use a topological sort to get a natural layering of events in time.
        # This is more robust than trying to infer ranks.
        pos = {}
        try:
            # This generates layers of nodes; nodes in a layer cannot reach each other.
            layers = list(nx.topological_generations(self.causal_set.graph))
            for i, layer in enumerate(layers):
                if not layer: continue
                # Spread nodes horizontally within each layer
                # Add a small random jitter to avoid perfect lines
                xs = np.linspace(-len(layer)/2, len(layer)/2, len(layer)) + np.random.rand(len(layer)) * 0.1
                for node, x_pos in zip(sorted(list(layer)), xs): # Sort layer for consistent plotting
                    pos[node] = (x_pos, -i) # Y-axis represents time flowing downwards
            self.causal_set.pos = pos
        except nx.NetworkXUnfeasible:
            # Fallback for graphs with cycles (shouldn't happen in a proper causal set)
            print("Warning: Graph is not a DAG, topological generations not possible. Using spring layout.")
            self.causal_set.pos = nx.spring_layout(self.causal_set.graph)
        return self.causal_set.pos

    def draw(self, output_path="spin_network_fractal_3.png"):
        """Draws the causal set graph."""
        if self.causal_set.pos is None:
            print("Layout not computed. Please run compute_layout first.")
            return

        plt.style.use('dark_background')
        fig, ax = plt.subplots(figsize=(20, 20))

        pos = self.causal_set.pos
        node_colors = [self.causal_set.get_past_cone_size(n) for n in sorted(self.causal_set.graph.nodes())]

        nx.draw_networkx_edges(self.causal_set.graph, pos, alpha=0.3, edge_color='gray', ax=ax, node_size=50)
        nodes = nx.draw_networkx_nodes(
            self.causal_set.graph, pos, node_color=node_colors, cmap=plt.cm.viridis,
            node_size=50, ax=ax
        )
        if nodes:
            cbar = plt.colorbar(nodes, ax=ax, label="Past Cone Size (Γ - Temporal Pressure)", shrink=0.8)
            cbar.ax.tick_params(labelsize=12)
            cbar.set_label("Past Cone Size (Γ - Temporal Pressure)", size=14)


        ax.set_title("The Fractal at the Heart of Time: A Causal Set Universe", fontsize=24, pad=20)
        plt.xlabel("Spacelike Dimension (Arbitrary)", fontsize=16)
        plt.ylabel("Timelike Dimension (Topological Rank)", fontsize=16)
        ax.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True, labelsize=12)
        plt.grid(True, linestyle='--', alpha=0.1)
        
        # Invert y-axis so time flows down
        ax.invert_yaxis()

        # Save the figure
        plt.savefig(output_path, dpi=150, bbox_inches='tight', facecolor='black')
        plt.close(fig)
        print(f"Fractal visualization saved to {output_path}")

# --- Main Execution Block ---
if __name__ == '__main__':
    NUM_EVENTS = 750  # A good number for a detailed but manageable plot

    # 1. Initialization
    causal_set = CausalSet(NUM_EVENTS)
    growth_rule = PirouetteGrowthRule(causal_set)

    # 2. The Growth Loop (Universe Simulation)
    # Start with a single event with no parents
    antichain = [0]
    for i in range(1, NUM_EVENTS):
        growth_rule.select_parent_and_birth_new_event(i, antichain)
        
        # Update the antichain (the "present moment") for the next step
        # The true antichain is all nodes with out_degree == 0
        current_nodes = causal_set.graph.nodes()
        antichain = [node for node in current_nodes if causal_set.graph.out_degree(node) == 0]
        
        # If the antichain ever empties (unlikely), restart from the last known node
        if not antichain:
            antichain = [i-1]


    # 3. Visualization
    layout_engine = SpinNetworkLayout(causal_set)
    layout_engine.compute_layout()
    layout_engine.draw()