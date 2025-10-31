import os
import shutil

# --- Configuration ---
# Define the paths to your directories.
# Make sure to replace these placeholder paths with your actual folder paths.
folder_a = 'C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/modules'      # Folder with original markdown files
folder_b = 'C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/Essentialization/essentialized' # Folder with processed files
folder_c = 'C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/Essentialization/to_do'  # Folder where new files will be copied

# --- Script Logic ---
def process_files():
    """
    Finds unprocessed markdown files in folder_a and copies them to folder_c.
    """
    # 1. Ensure the destination directory (folder_c) exists.
    #    If it doesn't, create it to avoid errors.
    if not os.path.exists(folder_c):
        print(f"Creating destination directory: {folder_c}")
        os.makedirs(folder_c)

    # 2. Get a list of all files in the source directory (folder_a).
    try:
        source_files = os.listdir(folder_a)
    except FileNotFoundError:
        print(f"Error: Source directory not found at '{folder_a}'")
        return

    print("Checking for files to process...")
    files_copied_count = 0

    # 3. Loop through each file in the source directory.
    for filename in source_files:
        # Check if the file is a markdown file.
        if filename.endswith('.md'):
            # Construct the base name (e.g., "document" from "document.md")
            base_name = os.path.splitext(filename)[0]
            
            # Construct the expected name of the essentialized file.
            essentialized_filename = f"{base_name}_essentialized.md"
            essentialized_filepath = os.path.join(folder_b, essentialized_filename)
            
            # 4. Check if the essentialized version does NOT exist in folder_b.
            if not os.path.exists(essentialized_filepath):
                # This file needs to be processed.
                source_filepath = os.path.join(folder_a, filename)
                destination_filepath = os.path.join(folder_c, filename)
                
                # 5. Copy the file from folder_a to folder_c.
                print(f"  -> Found new file: '{filename}'. Copying to processing folder.")
                shutil.copy2(source_filepath, destination_filepath)
                files_copied_count += 1

    if files_copied_count == 0:
        print("No new files to process. Everything is up to date.")
    else:
        print(f"\nDone! Copied {files_copied_count} file(s) to '{folder_c}'.")


# --- Run the script ---
if __name__ == "__main__":
    process_files()