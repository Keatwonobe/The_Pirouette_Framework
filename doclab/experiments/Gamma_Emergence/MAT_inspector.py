import scipy.io

# Load your .MAT file
mat_data = scipy.io.loadmat('C:/Users/keatw/Downloads/sub-01/sub-01/ses-S1/behavioral/MATB_Diff.mat')

# Get the data variable
event_data = mat_data['MATB_diff']

# 1. Check the shape (rows, columns)
print(f"Shape of the data: {event_data.shape}")

# 2. Check the data type
print(f"Data type: {event_data.dtype}")

# 3. Print the first 5 rows to see its structure
print("First 5 rows:")
print(event_data[0:5, :])