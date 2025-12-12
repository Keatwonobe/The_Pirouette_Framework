import re
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as style

def parse_log_file(file_path):
    """Parses the provided log file to extract training data."""
    data = {
        'episode': [],
        'score': [],
        'run_type': [],
        'avg_top_scores': [],
        'dyn_threshold': []
    }
    
    with open(file_path, 'r') as f:
        for line in f:
            if line.strip().startswith('Episode'):
                # Extract main episode data
                ep_match = re.search(r'Episode (\d+): (.*?) run\.\s*Score: (\d+)', line)
                if ep_match:
                    data['episode'].append(int(ep_match.group(1)))
                    data['run_type'].append(ep_match.group(2).strip())
                    data['score'].append(int(ep_match.group(3)))

            elif 'avg=' in line:
                # Extract average score and dynamic threshold from the next lines
                avg_match = re.search(r'avg=([\d.]+)', line)
                dyn_match = re.search(r'dyn_threshold=(\d+)', line)
                
                if avg_match:
                    data['avg_top_scores'].append(float(avg_match.group(1)))
                else:
                    data['avg_top_scores'].append(None) # Handle missing data
                    
                if dyn_match:
                    data['dyn_threshold'].append(int(dyn_match.group(1)))
                else:
                    # If threshold isn't on the same line, check the next one or use previous
                    if data['dyn_threshold']:
                         data['dyn_threshold'].append(data['dyn_threshold'][-1])
                    else:
                         data['dyn_threshold'].append(None)

    # Ensure all lists are of the same length before creating the DataFrame
    min_len = min(len(v) for v in data.values())
    for k in data:
        data[k] = data[k][:min_len]
        
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

    # Line plot for the average of top scores
    ax.plot(df['episode'], df['avg_top_scores'], color='dodgerblue', linewidth=2.5, label='Top Scores Average')
    
    # Line plot for the dynamic threshold
    ax.plot(df['episode'], df['dyn_threshold'], color='gold', linestyle='--', linewidth=2, label='Dynamic Threshold')

    # --- Chart Customization ---
    ax.set_title('Agent Performance Over 500 Episodes', fontsize=18, fontweight='bold')
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
    peak_score_episode = df['score'].idxmax()
    peak_score = df['score'].max()
    ax.annotate(f'Peak Score: {peak_score}', 
                xy=(df['episode'][peak_score_episode], peak_score),
                xytext=(df['episode'][peak_score_episode], peak_score + 30),
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
    
    # Fill any missing threshold values by carrying forward the last known value
    training_df['dyn_threshold'].ffill(inplace=True)

    print("Successfully parsed data:")
    print(training_df.head())
    
    plot_training_run(training_df)