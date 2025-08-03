# zz_compile_framework.py (v2 - Location-Aware)

import os
import glob
import yaml
import sys

def get_module_metadata(filepath):
    """
    Reads a markdown file and extracts metadata from the YAML front-matter.
    
    Args:
        filepath (str): The path to the markdown file.
        
    Returns:
        A dictionary with 'id', 'title', and the full 'content' of the file,
        or None if the file cannot be processed.
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()
            
        parts = full_content.split('---')
        
        if len(parts) < 3:
            print(f"⚠️  Warning: Skipping '{os.path.basename(filepath)}'. Could not find YAML front-matter.")
            return None

        front_matter = parts[1]
        metadata = yaml.safe_load(front_matter)
        
        if 'id' not in metadata or 'title' not in metadata:
            print(f"⚠️  Warning: Skipping '{os.path.basename(filepath)}'. Missing 'id' or 'title' in metadata.")
            return None
            
        return {
            'id': metadata['id'],
            'title': metadata['title'],
            'filepath': filepath,
            'content': full_content
        }
        
    except yaml.YAMLError as e:
        print(f"❌ Error parsing YAML in '{os.path.basename(filepath)}': {e}")
        return None
    except Exception as e:
        print(f"❌ An unexpected error occurred while processing '{os.path.basename(filepath)}': {e}")
        return None

def main():
    """
    Main function to discover, process, and combine markdown files from the script's own directory.
    """
    # --- SCRIPT LOCATION-AWARE LOGIC ---
    # Get the absolute directory path of the script itself
    script_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"Script location identified: {script_dir}")
    
    # Define the output file path relative to the script's directory
    output_filename = "prime_pirouette_series.md"
    output_filepath = os.path.join(script_dir, output_filename)
    
    # --- FILE DISCOVERY ---
    # Search for all .md files in the script's directory
    search_pattern = os.path.join(script_dir, '*.md')
    all_markdown_paths = glob.glob(search_pattern)
    
    # Exclude the output file itself to prevent it from being included in the next run
    markdown_files_to_process = [f for f in all_markdown_paths if f != output_filepath]
    
    if not markdown_files_to_process:
        print("\nNo markdown files (.md) found in the script's directory.")
        return
        
    print(f"Found {len(markdown_files_to_process)} markdown files to process.")
    
    # 1. Gather metadata from all files
    modules = []
    for md_filepath in markdown_files_to_process:
        metadata = get_module_metadata(md_filepath)
        if metadata:
            modules.append(metadata)
            
    # 2. Sort modules by their ID
    modules.sort(key=lambda x: x['id'])
    
    # 3. Write the combined file
    try:
        with open(output_filepath, 'w', encoding='utf-8') as f_out:
            f_out.write("# Pirouette Framework - Compiled Modules\n\n")
            f_out.write("## Table of Contents\n\n")
            for module in modules:
                anchor = str(module['id']).lower().replace(' ', '-')
                f_out.write(f"* [{module['id']}: {module['title']}](#{anchor})\n")
            
            f_out.write("\n")
            
            print("\nBuilding combined document...")
            for module in modules:
                print(f"  -> Appending {module['id']}: {module['title']}")
                anchor = str(module['id']).lower().replace(' ', '-')
                f_out.write("---\n\n")
                f_out.write(f'<a name="{anchor}"></a>\n\n')
                f_out.write(module['content'])
                f_out.write("\n\n")
        
        print(f"\n✅ Successfully combined {len(modules)} modules into '{output_filename}'")
        
    except IOError as e:
        print(f"❌ Error writing to output file '{output_filename}': {e}")

if __name__ == "__main__":
    main()