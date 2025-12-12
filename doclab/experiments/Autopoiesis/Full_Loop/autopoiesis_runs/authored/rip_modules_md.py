import os

MARKDOWN_DIR = '.'  # Directory to search ('.' means current directory)
OUTPUT_FILE = 'module_markdown.md' # The final combined file

# Find all files ending with .md
try:
    md_files = [f for f in os.listdir(MARKDOWN_DIR) 
                if f.endswith('.md') and os.path.isfile(os.path.join(MARKDOWN_DIR, f))]
    md_files.sort() # Sort files alphabetically
    
    # Exclude the output file itself if it already exists
    if OUTPUT_FILE in md_files:
        md_files.remove(OUTPUT_FILE)
        
except FileNotFoundError:
    print(f"Error: Directory not found: {MARKDOWN_DIR}")
    exit(1)

print(f"Found {len(md_files)} markdown files. Combining...")

# Open the output file in write mode
with open(OUTPUT_FILE, 'w', encoding='utf-8') as outfile:
    for filename in md_files:
        filepath = os.path.join(MARKDOWN_DIR, filename)
        
        print(f"Appending {filename}...")
        
        # Write the filename as a header
        outfile.write(f"\n\n---\n")
        outfile.write(f"# File: {filename}\n")
        outfile.write(f"---\n\n")
        
        # Try to read and write the content of the markdown file
        try:
            with open(filepath, 'r', encoding='utf-8') as infile:
                outfile.write(infile.read())
        except Exception as e:
            print(f"Warning: Could not read file {filepath}. Error: {e}")

print(f"\nDone! Successfully combined files into {OUTPUT_FILE}")