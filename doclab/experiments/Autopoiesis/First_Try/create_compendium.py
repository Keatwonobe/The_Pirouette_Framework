import argparse
from pathlib import Path

def create_compendium(modules_dir: str, output_file: str):
    """
    Finds all .md files in a directory, concatenates them into a single
    file, using the source filename as a header for each section.
    """
    src_dir = Path(modules_dir)
    out_path = Path(output_file)
    
    # Find all Markdown files in the source directory, sorted for consistency
    files = sorted(src_dir.glob("*_essentialized.md"))
    
    if not files:
        print(f"Error: No '*_essentialized.md' files found in '{modules_dir}'.")
        return

    print(f"Found {len(files)} essentialized modules. Combining into '{out_path.name}'...")

    # Open the output file and write the contents of each module
    with out_path.open('w', encoding='utf-8') as outfile:
        outfile.write(f"# Pirouette Framework Micro-Compendium\n")
        outfile.write(f"# Generated from {len(files)} essentialized modules.\n\n")
        
        for i, md_file in enumerate(files):
            # Read the content of the module
            content = md_file.read_text(encoding='utf-8').strip()
            
            # Write a separator and the filename as a header
            separator = "---\n"
            header = f"## MODULE SOURCE: {md_file.name}\n\n"
            
            # Add a separator between entries, but not at the very beginning
            if i > 0:
                outfile.write("\n\n" + separator)
                
            outfile.write(header)
            outfile.write(content)
            
    print(f"✅ Success! Compendium created at: {out_path}")

def main():
    parser = argparse.ArgumentParser(
        description="Combine essentialized Pirouette modules into a single compendium file."
    )
    parser.add_argument(
        "modules_dir", 
        help="Path to the directory containing the '_essentialized.md' files (e.g., './essentialized')."
    )
    parser.add_argument(
        "--out", 
        default="./Pirouette_Micro_Framework.md", 
        help="Path for the final output file."
    )
    args = parser.parse_args()
    
    create_compendium(args.modules_dir, args.out)

if __name__ == "__main__":
    main()