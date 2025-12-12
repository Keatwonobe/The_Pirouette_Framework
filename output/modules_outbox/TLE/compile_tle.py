import os

# --- Configuration ---
# The folder containing your markdown files.
input_folder = 'C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/modules/TLE' 

# The name of the final combined file that will be created.
output_filename = 'C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/TLE_pirouette.md'

# --- Script Logic ---
def combine_markdown_files():
    """
    Combines all .md files in a folder into a single markdown file.
    """
    # Get a list of all markdown files in the input folder.
    # We sort the list to ensure a consistent and predictable order.
    try:
        filenames = sorted([f for f in os.listdir(input_folder) if f.endswith('.md')])
    except FileNotFoundError:
        print(f"Error: Input directory not found at '{input_folder}'")
        return

    if not filenames:
        print(f"No markdown files found in '{input_folder}'.")
        return

    # Open the output file in write mode ('w'). 
    # This will create the file if it doesn't exist, or overwrite it if it does.
    output_filepath = os.path.join(input_folder, output_filename)
    with open(output_filepath, 'w', encoding='utf-8') as outfile:
        print(f"Creating combined file at: {output_filepath}")
        
        # Loop through each markdown file.
        for filename in filenames:
            filepath = os.path.join(input_folder, filename)
            
            # 1. Write the filename as a header.
            # Using a level 2 header (##) is good practice.
            outfile.write(f"## {filename}\n\n")
            
            # 2. Read the content of the source file.
            with open(filepath, 'r', encoding='utf-8') as infile:
                content = infile.read()
                outfile.write(content)
            
            # 3. Add a horizontal rule and newlines for clean separation.
            outfile.write("\n\n---\n\n")

    print(f"\n✅ Success! Combined {len(filenames)} files into '{output_filename}'.")


# --- Run the script ---
if __name__ == "__main__":
    combine_markdown_files()