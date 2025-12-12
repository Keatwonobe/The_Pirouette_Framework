"""
LINGUISTIC ARCHAEOLOGY: Reverse Engineering Language Coordinates

Instead of generating language from coordinates, we FIND coordinates
from real language by solving the inverse problem.

Process:
1. Parse real text (Moby Dick, etc.)
2. Extract linguistic features (rhythm, complexity, structure)
3. Search fractal for coordinates that match those features
4. Map the "stable language region" in (m, λ) space
5. Compute geodesics between linguistic states

This reveals the SHADOWS that language casts on the fractal landscape.
"""

import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
import re


class LinguisticArchaeology:
    """
    Reverse-engineers fractal coordinates from real text.
    """
    def __init__(self):
        self.common_words = set([
            'the', 'be', 'to', 'of', 'and', 'a', 'in', 'that', 'have',
            'i', 'it', 'for', 'not', 'on', 'with', 'he', 'as', 'you',
            'do', 'at', 'this', 'but', 'his', 'by', 'from', 'they',
            'we', 'say', 'her', 'she', 'or', 'an', 'will', 'my', 'one',
            'all', 'would', 'there', 'their'
        ])
        
    def extract_linguistic_features(self, text):
        """
        Extract measurable features from text that we can map to (m, λ).
        
        Returns features that should correspond to fractal coordinates:
        - Temporal coherence (how words relate across distance)
        - Syntactic complexity (short vs long range dependencies)
        - Rhythmic structure (periodicity)
        - Semantic density (information per token)
        """
        # Clean and tokenize
        words = re.findall(r'\b[a-z]+\b', text.lower())
        
        if len(words) < 10:
            return None
        
        # 1. Word length variation (relates to coupling λ)
        word_lengths = [len(w) for w in words]
        avg_word_length = np.mean(word_lengths)
        word_length_var = np.std(word_lengths)
        
        # 2. Sentence length (temporal scale)
        sentences = re.split(r'[.!?]+', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        sentence_lengths = [len(s.split()) for s in sentences]
        avg_sentence_length = np.mean(sentence_lengths) if sentences else 0
        
        # 3. Rare word ratio (semantic density)
        rare_words = [w for w in words if w not in self.common_words]
        rare_ratio = len(rare_words) / len(words) if words else 0
        
        # 4. Bigram complexity (local coherence)
        bigrams = [(words[i], words[i+1]) for i in range(len(words)-1)]
        unique_bigrams = len(set(bigrams))
        bigram_diversity = unique_bigrams / len(bigrams) if bigrams else 0
        
        # 5. Long-range coherence (repeated words at distance)
        word_freq = Counter(words)
        repeated_words = [w for w, c in word_freq.items() if c > 2]
        coherence_score = len(repeated_words) / len(set(words)) if words else 0
        
        return {
            'avg_word_length': avg_word_length,
            'word_length_var': word_length_var,
            'avg_sentence_length': avg_sentence_length,
            'rare_ratio': rare_ratio,
            'bigram_diversity': bigram_diversity,
            'coherence_score': coherence_score,
            'num_words': len(words),
            'text_sample': ' '.join(words[:50])
        }
    
    def features_to_coordinate_estimate(self, features):
        """
        Map linguistic features to estimated (m, λ) coordinate.
        
        This is the INVERSE of what the generator does:
        - High coherence → negative m (opposing forces create stability)
        - High coupling (varied words) → high λ
        - Long sentences → medium λ (sustained coherence)
        - Dense semantics → Gold basin region
        """
        # Coherence → m (mass field)
        # High coherence across distance suggests negative m
        coherence = features['coherence_score']
        m_estimate = -0.5 * (1 - coherence)  # Range: [-0.5, 0]
        
        # Complexity → λ (coupling field)
        # High diversity and long sentences suggest high coupling
        diversity = features['bigram_diversity']
        length_factor = min(features['avg_sentence_length'] / 20.0, 1.0)
        lam_estimate = 0.5 + 0.5 * (diversity + length_factor) / 2
        
        return m_estimate, lam_estimate
    
    def compute_basin_from_coordinate(self, m, lam, steps=20):
        """
        Evolve coordinate to determine which basin it falls into.
        """
        p_m, p_l = 0.0, 0.0
        sigma = 1.0
        dt = 0.1
        
        for _ in range(steps):
            grad_m = m + 2 * sigma * m * lam
            grad_l = lam + sigma * (m**2 - lam**2)
            
            p_m_half = p_m - (dt / 2) * grad_m
            p_l_half = p_l - (dt / 2) * grad_l
            
            m = m + dt * p_m_half
            lam = lam + dt * p_l_half
            
            grad_m_new = m + 2 * sigma * m * lam
            grad_l_new = lam + sigma * (m**2 - lam**2)
            
            p_m = p_m_half - (dt / 2) * grad_m_new
            p_l = p_l_half - (dt / 2) * grad_l_new
            
            r2 = m**2 + lam**2
            if r2 > 20:
                break
        
        theta = np.arctan2(lam, m)
        
        if theta > 0.5 and theta < 2.5:
            return 'teal'
        elif np.abs(theta) > 2.5:
            return 'red'
        else:
            return 'gold'
    
    def analyze_text_file(self, text):
        """
        Analyze a text file and find its fractal coordinates.
        """
        # Break into passages (every ~100 words)
        words = re.findall(r'\b[a-z]+\b', text.lower())
        passage_size = 100
        
        passages = []
        for i in range(0, len(words) - passage_size, passage_size // 2):
            passage_words = words[i:i+passage_size]
            passage_text = ' '.join(passage_words)
            passages.append(passage_text)
        
        print(f"Analyzing {len(passages)} passages...")
        
        results = []
        for i, passage in enumerate(passages[:50]):  # Limit to first 50
            features = self.extract_linguistic_features(passage)
            if features:
                m, lam = self.features_to_coordinate_estimate(features)
                basin = self.compute_basin_from_coordinate(m, lam)
                
                results.append({
                    'passage_num': i,
                    'm': m,
                    'lam': lam,
                    'basin': basin,
                    'features': features
                })
        
        return results


class GeodesicComputer:
    """
    Computes geodesics (shortest paths) between points in the fractal.
    
    Uses triangular gradient descent: given current position and target,
    compute which direction minimizes action S = ∫ 𝓛 dt.
    """
    def __init__(self):
        self.sigma = 1.0
        
    def compute_potential(self, m, lam):
        """V_Γ = ½m² + ½λ² + σm²λ - σλ³/3"""
        return 0.5 * m**2 + 0.5 * lam**2 + \
               self.sigma * m**2 * lam - self.sigma * lam**3 / 3
    
    def compute_gradient(self, m, lam):
        """∇V = (∂V/∂m, ∂V/∂λ)"""
        grad_m = m + 2 * self.sigma * m * lam
        grad_l = lam + self.sigma * (m**2 - lam**2)
        return grad_m, grad_l
    
    def compute_geodesic(self, start_m, start_lam, end_m, end_lam, num_steps=20):
        """
        Compute geodesic path from start to end using gradient descent on action.
        
        The action S = ∫ (½v² + V) dt should be minimized.
        We use simple interpolation with potential energy penalty.
        """
        # Linear interpolation as baseline
        t_vals = np.linspace(0, 1, num_steps)
        
        # Initialize path
        m_path = start_m + t_vals * (end_m - start_m)
        lam_path = start_lam + t_vals * (end_lam - start_lam)
        
        # Refine using gradient descent on action
        learning_rate = 0.1
        iterations = 50
        
        for iteration in range(iterations):
            # Compute action along path
            action = 0
            
            for i in range(1, num_steps):
                # Kinetic energy (velocity squared)
                dm = m_path[i] - m_path[i-1]
                dlam = lam_path[i] - lam_path[i-1]
                kinetic = 0.5 * (dm**2 + dlam**2)
                
                # Potential energy
                potential = self.compute_potential(m_path[i], lam_path[i])
                
                action += kinetic + potential
            
            # Gradient of action with respect to path points
            # (simplified - full geodesic equation is more complex)
            for i in range(1, num_steps-1):
                grad_m, grad_lam = self.compute_gradient(m_path[i], lam_path[i])
                
                # Move against gradient to minimize action
                m_path[i] -= learning_rate * grad_m * 0.01
                lam_path[i] -= learning_rate * grad_lam * 0.01
        
        return m_path, lam_path
    
    def triangular_gradient(self, current_m, current_lam, target_m, target_lam):
        """
        Compute optimal direction using TRIANGULAR MATH.
        
        Given current position and target, compute the facet of the
        "triangle" (really the tangent space) that has the right slope
        to complete the gradient.
        
        This is faster than full geodesic computation.
        """
        # Direction vector
        dm = target_m - current_m
        dlam = target_lam - current_lam
        distance = np.sqrt(dm**2 + dlam**2)
        
        if distance < 1e-6:
            return current_m, current_lam
        
        # Unit direction
        dir_m = dm / distance
        dir_lam = dlam / distance
        
        # Current gradient (force field)
        grad_m, grad_lam = self.compute_gradient(current_m, current_lam)
        
        # Project gradient onto direction
        grad_along_dir = grad_m * dir_m + grad_lam * dir_lam
        
        # Correct for gradient (move along geodesic, not straight line)
        # This is the "triangular" correction
        correction_m = -grad_m * 0.1
        correction_lam = -grad_lam * 0.1
        
        # Step with correction
        step_size = 0.1
        next_m = current_m + step_size * dir_m + correction_m
        next_lam = current_lam + step_size * dir_lam + correction_lam
        
        return next_m, next_lam


def analyze_literature(text, title="Text"):
    """
    Main analysis function.
    """
    print("="*70)
    print(f"LINGUISTIC ARCHAEOLOGY: Reverse Engineering {title}")
    print("="*70)
    
    archaeologist = LinguisticArchaeology()
    
    # Analyze
    print(f"\nExtracting coordinates from {title}...")
    results = archaeologist.analyze_text_file(text)
    
    if not results:
        print("No valid passages found!")
        return None
    
    print(f"Found {len(results)} passage coordinates\n")
    
    # Statistics
    m_vals = [r['m'] for r in results]
    lam_vals = [r['lam'] for r in results]
    basins = [r['basin'] for r in results]
    
    basin_counts = Counter(basins)
    
    print("STATISTICS")
    print("-"*70)
    print(f"Mean m: {np.mean(m_vals):.3f} (coherence)")
    print(f"Mean λ: {np.mean(lam_vals):.3f} (coupling)")
    print(f"Std m: {np.std(m_vals):.3f}")
    print(f"Std λ: {np.std(lam_vals):.3f}")
    print(f"\nBasin distribution:")
    for basin, count in basin_counts.items():
        print(f"  {basin}: {count} ({count/len(results)*100:.1f}%)")
    
    # Show sample coordinates
    print(f"\nSample passage coordinates:")
    for i in range(min(3, len(results))):
        r = results[i]
        print(f"\nPassage {r['passage_num']}: m={r['m']:.3f}, λ={r['lam']:.3f} ({r['basin']})")
        print(f"  Sample: {r['features']['text_sample'][:80]}...")
    
    return results


def visualize_language_landscape(results_dict, save_path='/mnt/user-data/outputs/language_landscape.png'):
    """
    Visualize where different texts live in the fractal.
    """
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    
    colors_map = {'teal': '#00CED1', 'gold': '#DAA520', 'red': '#FF4500'}
    text_colors = ['blue', 'green', 'purple', 'orange', 'brown']
    
    # Plot 1: All texts overlaid
    ax1 = axes[0, 0]
    
    for i, (title, results) in enumerate(results_dict.items()):
        if results:
            m_vals = [r['m'] for r in results]
            lam_vals = [r['lam'] for r in results]
            ax1.scatter(m_vals, lam_vals, alpha=0.5, s=30, 
                       c=text_colors[i % len(text_colors)], label=title)
    
    ax1.set_xlabel('m (Coherence)')
    ax1.set_ylabel('λ (Coupling)')
    ax1.set_title('Language Landscape: All Texts')
    ax1.legend()
    ax1.grid(True, alpha=0.3)
    ax1.axvline(x=0, color='yellow', linestyle='--', alpha=0.5, label='m=0')
    
    # Plot 2: Basin distribution
    ax2 = axes[0, 1]
    
    basin_data = {}
    for title, results in results_dict.items():
        if results:
            basins = [r['basin'] for r in results]
            basin_counts = Counter(basins)
            basin_data[title] = basin_counts
    
    basins_list = ['teal', 'gold', 'red']
    x = np.arange(len(results_dict))
    width = 0.25
    
    for i, basin in enumerate(basins_list):
        counts = [basin_data.get(title, {}).get(basin, 0) 
                 for title in results_dict.keys()]
        ax2.bar(x + i*width, counts, width, label=basin, 
               color=colors_map[basin], alpha=0.7)
    
    ax2.set_xlabel('Text')
    ax2.set_ylabel('Passage Count')
    ax2.set_title('Basin Distribution by Text')
    ax2.set_xticks(x + width)
    ax2.set_xticklabels(list(results_dict.keys()), rotation=45, ha='right')
    ax2.legend()
    ax2.grid(True, alpha=0.3)
    
    # Plot 3: Geodesic example
    ax3 = axes[1, 0]
    
    # Compute geodesic between two text regions
    if len(results_dict) >= 2:
        texts = list(results_dict.items())
        text1_results = texts[0][1]
        text2_results = texts[1][1]
        
        if text1_results and text2_results:
            # Average coordinates
            m1 = np.mean([r['m'] for r in text1_results[:10]])
            lam1 = np.mean([r['lam'] for r in text1_results[:10]])
            m2 = np.mean([r['m'] for r in text2_results[:10]])
            lam2 = np.mean([r['lam'] for r in text2_results[:10]])
            
            # Compute geodesic
            computer = GeodesicComputer()
            m_path, lam_path = computer.compute_geodesic(m1, lam1, m2, lam2, num_steps=30)
            
            ax3.plot(m_path, lam_path, 'r-', linewidth=2, label='Geodesic')
            ax3.scatter([m1], [lam1], s=200, c='blue', marker='o', 
                       label=texts[0][0], zorder=3)
            ax3.scatter([m2], [lam2], s=200, c='green', marker='s', 
                       label=texts[1][0], zorder=3)
            
            ax3.set_xlabel('m (Coherence)')
            ax3.set_ylabel('λ (Coupling)')
            ax3.set_title(f'Geodesic Path Between Texts')
            ax3.legend()
            ax3.grid(True, alpha=0.3)
    
    # Plot 4: Density heatmap
    ax4 = axes[1, 1]
    
    # Combine all points
    all_m = []
    all_lam = []
    for results in results_dict.values():
        if results:
            all_m.extend([r['m'] for r in results])
            all_lam.extend([r['lam'] for r in results])
    
    if all_m:
        # Create 2D histogram
        h, xedges, yedges = np.histogram2d(all_m, all_lam, bins=20)
        
        extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]]
        im = ax4.imshow(h.T, origin='lower', extent=extent, cmap='hot', aspect='auto')
        
        ax4.set_xlabel('m (Coherence)')
        ax4.set_ylabel('λ (Coupling)')
        ax4.set_title('Language Density Heatmap')
        plt.colorbar(im, ax=ax4, label='Passage Count')
        ax4.axvline(x=0, color='cyan', linestyle='--', alpha=0.5)
    
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"\nVisualization saved to {save_path}")
    plt.show()


# Example texts for testing
SAMPLE_MOBY_DICK = """
Call me Ishmael. Some years ago never mind how long precisely having little 
or no money in my purse, and nothing particular to interest me on shore, 
I thought I would sail about a little and see the watery part of the world. 
It is a way I have of driving off the spleen and regulating the circulation. 
Whenever I find myself growing grim about the mouth; whenever it is a damp, 
drizzly November in my soul; whenever I find myself involuntarily pausing 
before coffin warehouses, and bringing up the rear of every funeral I meet; 
and especially whenever my hypos get such an upper hand of me, that it requires 
a strong moral principle to prevent me from deliberately stepping into the street, 
and methodically knocking people's hats off then, I account it high time to get 
to sea as soon as I can. This is my substitute for pistol and ball.
"""

SAMPLE_PRIDE = """
It is a truth universally acknowledged, that a single man in possession of a 
good fortune, must be in want of a wife. However little known the feelings or 
views of such a man may be on his first entering a neighbourhood, this truth 
is so well fixed in the minds of the surrounding families, that he is considered 
the rightful property of some one or other of their daughters. My dear Mr. Bennet, 
said his lady to him one day, have you heard that Netherfield Park is let at last?
"""

SAMPLE_TECHNICAL = """
The algorithm computes the gradient descent optimization by iterating through 
the parameter space. Each iteration updates the weight matrix according to the 
backpropagation formula. The learning rate determines the step size in the 
direction of the negative gradient. Convergence occurs when the loss function 
reaches a local minimum. The batch size affects both training speed and model 
generalization performance.
"""


if __name__ == "__main__":
    # Analyze sample texts
    results_dict = {}
    
    print("\n" + "="*70)
    print("ANALYZING SAMPLE TEXTS")
    print("="*70 + "\n")
    
    results_dict["Moby Dick"] = analyze_literature(SAMPLE_MOBY_DICK, "Moby Dick (Sample)")
    print("\n")
    results_dict["Pride & Prejudice"] = analyze_literature(SAMPLE_PRIDE, "Pride & Prejudice (Sample)")
    print("\n")
    results_dict["Technical"] = analyze_literature(SAMPLE_TECHNICAL, "Technical Writing")
    
    # Visualize
    print("\n" + "="*70)
    print("CREATING LANDSCAPE VISUALIZATION")
    print("="*70)
    visualize_language_landscape(results_dict)
    
    print("\n" + "="*70)
    print("NEXT STEPS")
    print("="*70)
    print("""
To analyze your own texts:
1. Load text file: with open('path/to/text.txt') as f: text = f.read()
2. Analyze: results = analyze_literature(text, "My Text")
3. Add to dict: results_dict["My Text"] = results
4. Visualize: visualize_language_landscape(results_dict)

The system will:
• Find fractal coordinates for each passage
• Map which basins contain different writing styles
• Compute geodesics between linguistic states
• Show the "shadow" language casts on geometry
    """)
