import os
import glob
import subprocess
import yaml

# --- Configuration ---
SOURCE_DIR = 'paper_sections'   # The folder where your .md files are
OUTPUT_PDF = 'pirouette_framework_paper.pdf'
TEMPLATE_FILE = 'template.tex'
TEMP_COMBINED_MD = 'temp_combined.md'

def parse_md_file(filepath):
    """Reads an MD file, separates YAML frontmatter and content."""
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    parts = content.split('---', 2)
    if len(parts) < 3:
        print(f"Warning: Could not find YAML frontmatter in {filepath}")
        return None, None

    metadata = yaml.safe_load(parts[1])
    markdown_body = parts[2]
    return metadata, markdown_body

def main():
    """Main function to compile the paper."""
    print("--- Starting Paper Compilation ---")

    # 1. Find all markdown files in the source directory
    md_files = glob.glob(os.path.join(SOURCE_DIR, '*.md'))
    if not md_files:
        print(f"Error: No .md files found in '{SOURCE_DIR}'. Please check the path.")
        return

    print(f"Found {len(md_files)} section files.")

    # 2. Parse each file and store its metadata and content
    sections = []
    for f in md_files:
        metadata, body = parse_md_file(f)
        if metadata and 'section_no' in metadata:
            sections.append({'meta': metadata, 'body': body})
        else:
            print(f"Skipping file {f} due to missing 'section_no'.")

    # 3. Sort sections based on the 'section_no' key
    sections.sort(key=lambda s: s['meta']['section_no'])
    print("Sections sorted successfully.")

    # 4. Combine all markdown bodies into a single string
    full_markdown_content = "\n\n---\n\n".join([s['body'] for s in sections])
    
    # Write to a temporary file
    with open(TEMP_COMBINED_MD, 'w', encoding='utf-8') as f:
        f.write(full_markdown_content)
    print(f"Combined content written to '{TEMP_COMBINED_MD}'.")

    # 5. Use Pandoc to convert the combined file to PDF
    pandoc_command = [
        'pandoc',
        TEMP_COMBINED_MD,
        '-o', OUTPUT_PDF,
        '--from', 'markdown',
        '--template', TEMPLATE_FILE,
        '--pdf-engine', 'xelatex',  # Better for unicode and custom fonts
        '--highlight-style', 'pygments' # For any code blocks
    ]

    print(f"\nRunning Pandoc command:\n{' '.join(pandoc_command)}\n")
    
    try:
        subprocess.run(pandoc_command, check=True, capture_output=True, text=True)
        print(f"✅ Success! PDF saved as '{OUTPUT_PDF}'")
    except subprocess.CalledProcessError as e:
        print(f"❌ Error during Pandoc conversion.")
        print("Pandoc stdout:", e.stdout)
        print("Pandoc stderr:", e.stderr)
    except FileNotFoundError:
        print("❌ Error: 'pandoc' command not found.")
        print("Please ensure Pandoc is installed and in your system's PATH.")
    finally:
        # 6. Clean up the temporary file
        if os.path.exists(TEMP_COMBINED_MD):
            os.remove(TEMP_COMBINED_MD)
            print(f"Cleaned up temporary file '{TEMP_COMBINED_MD}'.")
            
    print("--- Compilation Finished ---")


if __name__ == '__main__':
    main()