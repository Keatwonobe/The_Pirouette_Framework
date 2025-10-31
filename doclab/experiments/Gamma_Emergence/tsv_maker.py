import scipy.io
import pandas as pd
import numpy as np

# 1. Load your .MAT file
# Replace with the actual path to your behavioral file
mat_file_path = 'C:/Users/keatw/Downloads/sub-01/sub-01/ses-S1/behavioral/MATB_Diff.mat' 
mat_data = scipy.io.loadmat(mat_file_path, squeeze_me=True) # squeeze_me helps simplify structures

# 2. Navigate to the parent structure that contains all the tasks
# This should now correctly point to the object with .TRACK, .SYSMON, etc.
data_struct = mat_data['MATB_diff']['output']

# 3. --- Access the CORRECT data based on the documentation ---
# The documentation says SYSMON contains the onsets.
sysmon_data = data_struct['SYSMON']

# 4. Extract the columns
# Column 1 (index 0) is the onset time in seconds.
onsets = sysmon_data[:, 0]
# Reaction time is in column 2 (index 1), if you ever need it.
# reaction_times = sysmon_data[:, 1]

# The documentation does not specify different event types or loads.
# We will create a placeholder 'load' column where every event is type 1.
loads = np.ones_like(onsets, dtype=int)

# 5. Create the final BIDS-compliant DataFrame
events_df = pd.DataFrame({
    'onset': onsets,
    'duration': np.zeros_like(onsets),  # Assuming events are instantaneous
    'load': loads
})

print("--- Successfully extracted SYSMON events ---")
print(events_df.head())
print("------------------------------------------\n")

# 6. Save to the .tsv file
# Note the task name is now 'matb' or similar, not 'track'
# It MUST match your EEG file's name perfectly.
bids_tsv_path = 'C:/Users/keatw/Downloads/sub-01/sub-01/ses-S1/eeg/sub-01_ses-S1_task-MATBdiff.tsv'
events_df.to_csv(bids_tsv_path, sep='\t', index=False)

print(f"Successfully created {bids_tsv_path}")