import json
import os
import glob

def combine_json_files(folder_path, output_file):
    """
    Combines all JSON files in a specified folder into a single JSON file.

    Args:
        folder_path (str): The path to the folder containing the JSON files.
        output_file (str): The path for the combined output JSON file.
    """
    all_data = []
    json_files = glob.glob(os.path.join(folder_path, '*.json'))

    if not json_files:
        print(f"No JSON files found in {folder_path}")
        return

    for file_path in json_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                # If the JSON file contains a list, extend the main list.
                # If it's a dictionary, append it.
                if isinstance(data, list):
                    all_data.extend(data)
                else:
                    all_data.append(data)
            print(f"Successfully processed: {file_path}")
        except json.JSONDecodeError:
            print(f"Error decoding JSON from file: {file_path}. Skipping this file.")
        except Exception as e:
            print(f"An unexpected error occurred with file {file_path}: {e}. Skipping this file.")

    try:
        with open(output_file, 'w', encoding='utf-8') as outfile:
            json.dump(all_data, outfile, indent=4)
        print(f"\nSuccessfully combined {len(json_files)} JSON files into: {output_file}")
    except Exception as e:
        print(f"An error occurred while writing the output file: {e}")

# --- Configuration ---
# IMPORTANT: Replace with your actual folder path and desired output file name.
# Make sure to use raw string (r"...") or escape backslashes (\\) for Windows paths.
input_folder = r"C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/pirouette_personas/Personas"
output_json_file = r"C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/pirouette_personas/Personas/combined_persona_modules.json"
# Or, to save it in the same directory as the script:
# output_json_file = "combined_output.json"

# --- Run the script ---
if __name__ == "__main__":
    if not os.path.isdir(input_folder):
        print(f"Error: The input folder '{input_folder}' does not exist.")
    else:
        combine_json_files(input_folder, output_json_file)