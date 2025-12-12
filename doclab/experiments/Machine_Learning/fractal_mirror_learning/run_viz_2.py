import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style

def parse_log_file(file_path):
    """Parses the provided log file to extract training data."""
    data = {
        'episode': [],
        'score': [],
        'run_type': []
    }
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip().startswith('Episode'):
                # UPDATED REGEX: Correctly handles floats with a trailing period.
                ep_match = re.search(r'Episode (\d+): (.*?) run\.\s*\(task=.*\)\s*Score: (-?[\d]+\.?[\d]*)', line)
                if ep_match:
                    data['episode'].append(int(ep_match.group(1)))
                    data['run_type'].append(ep_match.group(2).strip())
                    data['score'].append(float(ep_match.group(3)))

    return pd.DataFrame(data)

def plot_training_run(df):
    """Creates and displays a plot of the training run from a DataFrame."""
    style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)

    # Define colors for run types
    colors = {'Coherent': 'limegreen', 'Dissonant': 'tomato'}
    
    # Scatter plot for individual episode scores, colored by run type
    for run_type, color in colors.items():
        subset = df[df['run_type'] == run_type]
        ax.scatter(subset['episode'], subset['score'], c=color, label=f'{run_type} Run', alpha=0.7, s=40)

    # REMOVED: The log file no longer contains data for 'Top Scores Average' or 'Dynamic Threshold'
    # ax.plot(df['episode'], df['avg_top_scores'], color='dodgerblue', linewidth=2.5, label='Top Scores Average')
    # ax.plot(df['episode'], df['dyn_threshold'], color='gold', linestyle='--', linewidth=2, label='Dynamic Threshold')

    # --- Chart Customization ---
    ax.set_title('Agent Performance Over 500+ Episodes', fontsize=18, fontweight='bold')
    ax.set_xlabel('Episode', fontsize=14)
    ax.set_ylabel('Score', fontsize=14)
    
    # Add a legend
    legend = ax.legend()
    for text in legend.get_texts():
        text.set_fontsize('large')
        
    # Set grid and ticks
    ax.grid(True, which='both', linestyle='--', linewidth=0.5)
    ax.tick_params(axis='both', which='major', labelsize=12)
    
    # Highlight the peak score
    if not df.empty:
        peak_score_episode_idx = df['score'].idxmax()
        peak_episode = df.loc[peak_score_episode_idx, 'episode']
        peak_score = df.loc[peak_score_episode_idx, 'score']
        
        ax.annotate(f'Peak Score: {peak_score}', 
                    xy=(peak_episode, peak_score),
                    xytext=(peak_episode, peak_score + 30),
                    arrowprops=dict(facecolor='black', shrink=0.05),
                    fontsize=12,
                    fontweight='bold',
                    ha='center')

    plt.tight_layout()
    plt.show()

# --- Main execution ---
if __name__ == '__main__':
    file_path = 'wendigo_7_run.txt'  # Your log file name
    training_df = parse_log_file(file_path)
    
    if not training_df.empty:
        print("Successfully parsed data:")
        print(training_df.head())
        plot_training_run(training_df)
    else:
        print("Could not parse any data from the log file. Please check the file format and regex.")