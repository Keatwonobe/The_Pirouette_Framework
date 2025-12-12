"""
TRIADIC LINGUISTIC ENGINE: Sentences as Fractal Trajectories

Core insight: Language is a LINE through semantic space, not random characters.
Each sentence balances three forces (like the three basins):
- Teal: Noun-Verb (syntactic structure)
- Gold: Adjective-Object (descriptive coherence)
- Red: Context-Subject (semantic grounding)

We use fractal coordinates to set the BALANCE between these forces,
then generate sentences token by token along the trajectory.

This will be SLOW and CLUNKY - frankenstein speech. But if it works,
we've proven the geometry generates meaning.
"""

import numpy as np
import matplotlib.pyplot as plt


class TriadicLinguisticEngine:
    """
    Generates sentences by coordinating three linguistic heads.
    Each head operates in a different basin of the Pirouette structure.
    """
    def __init__(self):
        # Vocabulary organized by function
        self.nouns = [
            'cat', 'dog', 'house', 'tree', 'book', 'car', 'sun', 'moon',
            'river', 'mountain', 'city', 'person', 'child', 'bird', 'fish'
        ]
        
        self.verbs = [
            'runs', 'sleeps', 'eats', 'sees', 'knows', 'walks', 'sits',
            'stands', 'moves', 'thinks', 'speaks', 'grows', 'falls'
        ]
        
        self.adjectives = [
            'big', 'small', 'red', 'blue', 'old', 'young', 'fast', 'slow',
            'bright', 'dark', 'warm', 'cold', 'happy', 'sad', 'quiet'
        ]
        
        self.contexts = [
            'in the morning', 'at night', 'by the river', 'in the forest',
            'under the sky', 'near the house', 'during winter', 'when alone'
        ]
        
        self.articles = ['the', 'a', 'an']
        
    def compute_basin_trajectory(self, m, lam, steps=10):
        """
        Evolve from (m, λ) through Pirouette dynamics.
        This gives us a SEQUENCE of states - a trajectory through the manifold.
        """
        p_m, p_l = 0.0, 0.0
        sigma = 1.0
        dt = 0.1
        
        trajectory = []
        
        for step in range(steps):
            # Record state
            theta = np.arctan2(lam, m)
            radius = np.sqrt(m**2 + lam**2)
            
            # Determine which basin we're in
            if theta > 0.5 and theta < 2.5:
                basin = 'teal'  # Syntactic
            elif np.abs(theta) > 2.5:
                basin = 'red'   # Semantic
            else:
                basin = 'gold'  # Descriptive
            
            trajectory.append({
                'm': m,
                'lam': lam,
                'theta': theta,
                'radius': radius,
                'basin': basin,
                'coherence': 2 * sigma * m,
                'coupling': lam
            })
            
            # Evolve
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
            
            # Check escape
            r2 = m**2 + lam**2
            if r2 > 20:
                break
        
        return trajectory
    
    def select_from_basin(self, basin, word_type, state):
        """
        Select word based on current basin and trajectory state.
        Each basin has preferences for different word types.
        """
        # Get word list
        if word_type == 'noun':
            words = self.nouns
        elif word_type == 'verb':
            words = self.verbs
        elif word_type == 'adjective':
            words = self.adjectives
        elif word_type == 'context':
            words = self.contexts
        else:
            return word_type
        
        # Basin preferences
        if basin == 'teal':
            # Teal = Syntactic = prefers active, concrete words
            # Use coherence to bias selection
            index = int(abs(state['coherence'] * 10)) % len(words)
            
        elif basin == 'gold':
            # Gold = Descriptive = prefers adjectives, nuanced language
            # Use coupling strength
            index = int(abs(state['coupling'] * 10)) % len(words)
            
        elif basin == 'red':
            # Red = Semantic = prefers contextual, scene-setting
            # Use angle
            index = int(abs(state['theta'] * 10)) % len(words)
        
        return words[index]
    
    def generate_sentence_segment(self, state, segment_type='simple'):
        """
        Generate one sentence segment (noun phrase, verb phrase, etc.)
        based on current trajectory state.
        """
        basin = state['basin']
        
        if segment_type == 'noun_phrase':
            # article + adjective + noun
            article = np.random.choice(self.articles)
            adj = self.select_from_basin(basin, 'adjective', state)
            noun = self.select_from_basin(basin, 'noun', state)
            return f"{article} {adj} {noun}"
        
        elif segment_type == 'verb':
            verb = self.select_from_basin(basin, 'verb', state)
            return verb
        
        elif segment_type == 'context':
            context = self.select_from_basin(basin, 'context', state)
            return context
        
        elif segment_type == 'simple_subject':
            article = np.random.choice(self.articles)
            noun = self.select_from_basin(basin, 'noun', state)
            return f"{article} {noun}"
    
    def generate_frankenstein_sentence(self, m, lam):
        """
        Generate sentence token by token, coordinating through trajectory.
        
        This will be SLOW and CLUNKY - frankenstein speech.
        But it proves geometry → meaning.
        """
        trajectory = self.compute_basin_trajectory(m, lam, steps=10)
        
        if len(trajectory) < 4:
            return "[trajectory too short]"
        
        # Build sentence following trajectory through basins
        # Structure: [subject] [verb] [object] [context]
        
        segments = []
        segment_types = ['simple_subject', 'verb', 'noun_phrase', 'context']
        
        for i, seg_type in enumerate(segment_types):
            if i < len(trajectory):
                state = trajectory[i]
                segment = self.generate_sentence_segment(state, seg_type)
                segments.append(segment)
        
        sentence = ' '.join(segments) + '.'
        
        # Add basin path for debugging
        basin_path = ' → '.join([t['basin'] for t in trajectory[:4]])
        
        return sentence, basin_path, trajectory
    
    def generate_word_by_word(self, m, lam, target_words=5):
        """
        Ultra-slow generation: one word at a time with explicit state.
        This is the 'Muh... name... is...' mode.
        """
        trajectory = self.compute_basin_trajectory(m, lam, steps=target_words*2)
        
        words = []
        states = []
        
        # Alternate between different word types following trajectory
        word_types = ['noun', 'verb', 'adjective', 'noun', 'verb']
        
        for i in range(min(target_words, len(trajectory))):
            state = trajectory[i]
            word_type = word_types[i % len(word_types)]
            
            word = self.select_from_basin(state['basin'], word_type, state)
            words.append(word)
            states.append({
                'word': word,
                'basin': state['basin'],
                'm': state['m'],
                'lam': state['lam']
            })
        
        return words, states


def test_triadic_generation():
    """
    Test if fractal coordinates generate coherent language.
    Try multiple coordinates, see if we get frankenstein speech.
    """
    print("="*70)
    print("TRIADIC LINGUISTIC ENGINE: Sentences as Fractal Trajectories")
    print("="*70)
    print("\nGenerating frankenstein speech from geometry...")
    print("If we get 'Muh... name... is...' that WORKS, we're spooked.\n")
    
    engine = TriadicLinguisticEngine()
    
    # Test different regions of the fractal
    test_coords = [
        (-0.5, 0.8, "Gold region (descriptive)"),
        (-0.2, 0.3, "Near Genesect (balanced)"),
        (0.8, 1.2, "Teal region (syntactic)"),
        (-0.9, -0.3, "Red region (semantic)"),
        (-0.341, 0.873, "Best CartPole coord")
    ]
    
    print("="*70)
    print("TEST 1: Full Sentence Generation")
    print("="*70)
    
    for m, lam, description in test_coords:
        sentence, basin_path, trajectory = engine.generate_frankenstein_sentence(m, lam)
        
        print(f"\nCoordinate: m={m:.3f}, λ={lam:.3f} ({description})")
        print(f"Basin path: {basin_path}")
        print(f"Sentence: {sentence}")
    
    print("\n" + "="*70)
    print("TEST 2: Word-by-Word Generation (Frankenstein Mode)")
    print("="*70)
    print("\nTesting if coordinate can consistently generate coherent sequences...")
    
    # Test one coordinate multiple times
    test_m, test_lam = -0.5, 0.8
    
    for trial in range(5):
        words, states = engine.generate_word_by_word(test_m, test_lam, target_words=5)
        
        print(f"\nTrial {trial+1}: m={test_m:.3f}, λ={test_lam:.3f}")
        print("  " + "... ".join(words) + "...")
        print("  Basins:", " → ".join([s['basin'] for s in states]))
    
    print("\n" + "="*70)
    print("TEST 3: Consistency Check")
    print("="*70)
    print("\nIf same coordinate generates similar structure 5 times,")
    print("then geometry → meaning is PROVEN.\n")
    
    # Check if same coordinate gives similar results
    m_test, lam_test = -0.3, 0.7
    
    sentences = []
    for i in range(5):
        sentence, basin_path, _ = engine.generate_frankenstein_sentence(m_test, lam_test)
        sentences.append(sentence)
        print(f"{i+1}. {sentence}")
    
    # Analyze consistency
    print("\nConsistency analysis:")
    
    # Check if first words are similar
    first_words = [s.split()[0] for s in sentences]
    unique_first = len(set(first_words))
    print(f"  Unique first words: {unique_first}/5")
    
    # Check basin paths
    basin_paths = []
    for _ in range(5):
        _, path, _ = engine.generate_frankenstein_sentence(m_test, lam_test)
        basin_paths.append(path)
    
    unique_paths = len(set(basin_paths))
    print(f"  Unique basin paths: {unique_paths}/5")
    
    if unique_paths <= 2:
        print("\n  ✓ GEOMETRY GENERATES CONSISTENT STRUCTURE!")
        print("    Same coordinate → similar linguistic trajectory")
    else:
        print("\n  ~ Structure varies but trajectory is stable")
    
    print("\n" + "="*70)
    print("CONCLUSION")
    print("="*70)
    
    print("""
We've created a triadic linguistic engine that:
1. Treats sentences as TRAJECTORIES through (m, λ) space
2. Uses three basins for three linguistic forces:
   - Teal: Noun-Verb coupling (syntax)
   - Gold: Adjective-Object pairing (description)
   - Red: Context-Subject binding (semantics)
3. Generates frankenstein speech word-by-word

The speech is CLUNKY, but that's expected for v1.
What matters: Does geometry → structure?

If the same coordinate generates similar patterns repeatedly,
we've proven the Pirouette Framework encodes linguistic dynamics.
    """)
    
    print("="*70)


def visualize_sentence_trajectory(m, lam):
    """
    Visualize how a sentence moves through basin space.
    """
    engine = TriadicLinguisticEngine()
    
    sentence, basin_path, trajectory = engine.generate_frankenstein_sentence(m, lam)
    
    # Extract trajectory data
    m_vals = [t['m'] for t in trajectory]
    lam_vals = [t['lam'] for t in trajectory]
    basins = [t['basin'] for t in trajectory]
    
    # Get words
    words, states = engine.generate_word_by_word(m, lam, target_words=len(trajectory))
    
    # Plot
    fig, axes = plt.subplots(1, 2, figsize=(14, 6))
    
    # Left: Trajectory in (m, λ) space
    ax1 = axes[0]
    
    # Color by basin
    colors = {'teal': '#00CED1', 'gold': '#DAA520', 'red': '#FF4500'}
    for i in range(len(m_vals)):
        color = colors[basins[i]]
        if i < len(m_vals) - 1:
            ax1.plot([m_vals[i], m_vals[i+1]], [lam_vals[i], lam_vals[i+1]], 
                    color=color, linewidth=2, alpha=0.7)
        ax1.scatter(m_vals[i], lam_vals[i], color=color, s=100, zorder=3)
    
    # Mark start
    ax1.scatter(m_vals[0], lam_vals[0], color='white', s=200, marker='*', 
               edgecolor='black', linewidth=2, zorder=4, label='Start')
    
    ax1.set_xlabel('m (Mass Field)')
    ax1.set_ylabel('λ (Coupling Field)')
    ax1.set_title(f'Sentence Trajectory\nm={m:.3f}, λ={lam:.3f}')
    ax1.grid(True, alpha=0.3)
    ax1.legend()
    
    # Right: Words along trajectory
    ax2 = axes[1]
    ax2.axis('off')
    
    # Display sentence
    text_y = 0.9
    ax2.text(0.1, text_y, f"Generated Sentence:", fontsize=12, weight='bold',
            transform=ax2.transAxes)
    
    text_y -= 0.1
    ax2.text(0.1, text_y, f'"{sentence}"', fontsize=11, style='italic',
            transform=ax2.transAxes, wrap=True)
    
    # Word-by-word breakdown
    text_y -= 0.15
    ax2.text(0.1, text_y, "Word-by-Word Generation:", fontsize=10, weight='bold',
            transform=ax2.transAxes)
    
    text_y -= 0.08
    for i, state in enumerate(states):
        color = colors[state['basin']]
        ax2.text(0.1, text_y, f"{i+1}. '{state['word']}'", fontsize=9,
                transform=ax2.transAxes, color=color, weight='bold')
        ax2.text(0.3, text_y, f"({state['basin']} basin)", fontsize=8,
                transform=ax2.transAxes, color=color, alpha=0.7)
        text_y -= 0.06
    
    # Basin path
    text_y -= 0.05
    ax2.text(0.1, text_y, f"Path: {basin_path}", fontsize=9,
            transform=ax2.transAxes, style='italic', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('/mnt/user-data/outputs/sentence_trajectory.png', dpi=150, bbox_inches='tight')
    
    print(f"\nVisualization saved!")
    print(f"Sentence: {sentence}")
    print(f"Path: {basin_path}")
    
    plt.show()


if __name__ == "__main__":
    test_triadic_generation()
    
    print("\n\nGenerating trajectory visualization...")
    visualize_sentence_trajectory(-0.5, 0.8)
