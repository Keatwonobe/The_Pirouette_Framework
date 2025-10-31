import os
import numpy as np
import re
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

# Download necessary NLTK data (only needs to be done once)
try:
    nltk.data.find('tokenizers/punkt')
    nltk.data.find('sentiment/vader_lexicon.zip')
except nltk.downloader.DownloadError:
    print("Downloading NLTK data...")
    nltk.download('punkt')
    nltk.download('vader_lexicon')

def read_and_clean_text(filepath):
    """Reads a .txt or .html file and returns clean text."""
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()
    if filepath.lower().endswith('.html'):
        soup = BeautifulSoup(content, 'html.parser')
        # Remove script and style elements
        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()
        text = soup.get_text(separator=' ', strip=True)
    else:
        text = content
    # Clean up whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def analyze_text_archetypes(filepath):
    """
    Analyzes a text file sentence by sentence and maps it to the Pirouette phase space.
    """
    print(f"Analyzing '{os.path.basename(filepath)}'...")
    
    # --- 1. Load and Prepare Data ---
    full_text = read_and_clean_text(filepath)
    sentences = nltk.sent_tokenize(full_text)
    sid = SentimentIntensityAnalyzer()
    
    if not sentences:
        print("No sentences found to analyze.")
        return

    # --- 2. Calculate Metrics for each "Epoch" (Sentence) ---
    results = []
    for sentence in sentences:
        if not sentence.strip():
            continue
            
        words = nltk.word_tokenize(sentence)
        if len(words) < 3: # Ignore very short sentences
            continue

        # Performance (Sentiment): The 'compound' score is a nice single metric from -1 to 1
        performance_score = sid.polarity_scores(sentence)['compound']
        
        # Kappa (Complexity): A simple proxy using average word length.
        # Longer words often correlate with higher conceptual complexity.
        avg_word_length = sum(len(word) for word in words) / len(words)
        kappa_score = avg_word_length
        
        results.append({
            "sentence": sentence,
            "performance_sentiment": performance_score,
            "kappa_complexity": kappa_score
        })
        
    df = pd.DataFrame(results)
    
    # --- 3. Classify into Archetypes ---
    median_perf = df['performance_sentiment'].median()
    # Use a baseline of 0 for sentiment if median is too close to it
    if abs(median_perf) < 0.05:
        median_perf = 0
    median_kappa = df['kappa_complexity'].median()
    
    conditions = [
        (df['kappa_complexity'] < median_kappa) & (df['performance_sentiment'] > median_perf),
        (df['kappa_complexity'] > median_kappa) & (df['performance_sentiment'] > median_perf),
        (df['kappa_complexity'] < median_kappa) & (df['performance_sentiment'] < median_perf),
        (df['kappa_complexity'] > median_kappa) & (df['performance_sentiment'] < median_perf)
    ]
    choices = ['Weaver', 'Gladiator', 'Drifter', 'Vortex']
    df['archetype'] = np.select(conditions, choices, default='Borderline')

    # --- 4. Visualize the Semantic Phase Space ---
    plt.style.use('seaborn-v0_8-whitegrid')
    fig, ax = plt.subplots(figsize=(14, 11))
    
    archetype_colors = {
        'Weaver': 'blue', 'Gladiator': 'purple',
        'Drifter': 'gray', 'Vortex': 'red', 'Borderline': 'yellow'
    }
    
    sns.scatterplot(
        data=df,
        x='kappa_complexity', y='performance_sentiment',
        hue='archetype', palette=archetype_colors,
        alpha=0.7, s=50, ax=ax
    )
    
    ax.axvline(median_kappa, color='black', linestyle='--', alpha=0.6)
    ax.axhline(median_perf, color='black', linestyle='--', alpha=0.6)
    
    ax.set_title(f'Semantic Phase Space of "{os.path.basename(filepath)}"', fontsize=18)
    ax.set_xlabel('κ (Linguistic Complexity)', fontsize=14)
    ax.set_ylabel('Performance (Sentiment)', fontsize=14)
    
    # Save results
    base_name = os.path.splitext(os.path.basename(filepath))[0]
    plot_filename = f'{base_name}_semantic_map.png'
    csv_filename = f'{base_name}_semantic_analysis.csv'
    
    plt.savefig(plot_filename)
    df.to_csv(csv_filename, index=False)
    
    print(f"\nAnalysis complete!")
    print(f"Plot saved to: {plot_filename}")
    print(f"Detailed CSV saved to: {csv_filename}")
    plt.show()

# Run the analysis on your file
# Replace "example_book.txt" with the path to your .txt or .html file
if __name__ == '__main__':
    # Make sure to put your book file in the same directory, or provide a full path.
    # For example: analyze_text_archetypes('my_book.html')
    target_file = 'The Project Gutenberg eBook of The Art of War.txt'
    if os.path.exists(target_file):
        analyze_text_archetypes(target_file)
    else:
        print(f"File not found: '{target_file}'. Please provide the correct path to your book file.")