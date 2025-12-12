import re
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.style as style
import matplotlib.cm as cm

def parse_log_file(file_path):
    """Parses the provided log file to extract training data, including game names."""
    data = {
        'episode': [],
        'score': [],
        'run_type': [],
        'game': [] # New column to store the game for each episode
    }
    games = set()

    with open(file_path, 'r') as f:
        for line in f:
            if "[INFO] Registered task" in line:
                game_match = re.search(r"\('([^']*)'\)", line)
                if game_match:
                    games.add(game_match.group(1))

            if line.strip().startswith('Episode'):
                # UPDATED REGEX: Capture the task name from within the parentheses
                ep_match = re.search(r'Episode (\d+): (.*?) run\.\s*\(task=([^)]*)\)\s*Score: (-?[\d]+\.?[\d]*)', line)
                if ep_match:
                    data['episode'].append(int(ep_match.group(1)))
                    data['run_type'].append(ep_match.group(2).strip())
                    data['game'].append(ep_match.group(3)) # Add game name
                    data['score'].append(float(ep_match.group(4)))

    return pd.DataFrame(data), sorted(list(games)) # Return sorted games for consistent colors

def plot_training_run(df, games):
    """Creates and displays a plot of the training run from a DataFrame."""
    style.use('seaborn-v0_8-darkgrid')
    fig, ax = plt.subplots(figsize=(16, 8), dpi=100)

    # --- Plot 1: Scatter points for Coherent/Dissonant runs ---
    run_type_colors = {'Coherent': 'limegreen', 'Dissonant': 'tomato'}
    for run_type, color in run_type_colors.items():
        subset = df[df['run_type'] == run_type]
        ax.scatter(subset['episode'], subset['score'], c=color, label=f'{run_type} Run', alpha=0.5, s=30)

    # --- Plot 2: Thin lines for each game's performance ---
    # Create a color map for the games
    game_colors = cm.viridis(np.linspace(0, 1, len(games)))
    color_map = {game: color for game, color in zip(games, game_colors)}

    for game in games:
        game_df = df[df['game'] == game].sort_values(by='episode')
        ax.plot(game_df['episode'], game_df['score'], color=color_map[game], label=f'{game} Thread', alpha=0.7, linewidth=1.2)

    # --- Chart Customization ---
    game_names = ', '.join(games) if games else 'Tasks'
    ax.set_title(f'Agent Performance on {game_names}', fontsize=18, fontweight='bold')
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
    file_path = 'wendigo_7_run.txt'
    training_df, games_played = parse_log_file(file_path)
    
    if not training_df.empty:
        print("Successfully parsed data:")
        print(training_df.head())
        
        if games_played:
            print(f"\nDetected games: {', '.join(games_played)}")
        
        plot_training_run(training_df, games_played)
    else:
        print("Could not parse any data from the log file. Please check the file format and regex.")