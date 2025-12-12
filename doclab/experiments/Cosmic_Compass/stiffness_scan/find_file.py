import os

# Get the absolute path of the current script file
script_path = os.path.abspath(__file__)

# Get the directory containing the script
script_directory = os.path.dirname(script_path)

print(f"The script is located at: {script_path}")
print(f"The script's directory is: {script_directory}")