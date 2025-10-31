import google.generativeai as genai
import os
import argparse
from pathlib import Path
import re

# --- Configuration ---
# It's recommended to set your API key as an environment variable
# for security, but you can also place it here if needed.
# genai.configure(api_key="YOUR_API_KEY")

def get_model(model_name="gemini-2.5-pro"):
    """Initializes and returns the generative model."""
    return genai.GenerativeModel(model_name)

def read_module(file_path):
    """Reads the content of a module file."""
    try:
        return file_path.read_text(encoding='utf-8')
    except Exception as e:
        print(f"Error reading {file_path.name}: {e}")
        return None

def save_module(directory, filename, content):
    """Saves the essentialized module content to a file in the specified directory."""
    # -FIXED- This now correctly joins the output directory and the new filename.
    output_path = Path(directory) / filename
    output_path.parent.mkdir(parents=True, exist_ok=True)
    try:
        output_path.write_text(content, encoding='utf-8')
    except Exception as e:
        print(f"Error saving {filename}: {e}")

def process_module(model, module_content, module_name):
    """Generates the essentialized content using the Gemini API."""
    prompt = f"""
You are a master synthesist and philosopher of science. Your task is to distill a complex technical document into its essential, potent core.
You must structure your output using three and only three specific Markdown headings: ## Law, ## Philosophy, and ## Art.

- ## Law: Extract the absolute core mathematical and formal principles. Include key equations, derivations, and falsifiable criteria. This section must be dense, precise, and unsparing in its formalism.
- ## Philosophy: Articulate the single most cogent and profound philosophical implication of the Law section.
- ## Art: Create a concise, powerful metaphor or poetic statement that bridges the abstract nature of the Law with the human implication of the Philosophy.

Do not include any preamble or extra conversational text. Begin your response immediately with the `## Law` heading.

SOURCE DOCUMENT: {module_name}
---
{module_content}
---
TASK: Distill the source content into its essential ## Law, ## Philosophy, and ## Art components.
"""
    response = model.generate_content(prompt)

    # -IMPROVED- This block safely extracts text and handles API blocks gracefully.
    try:
        # The safe way to get text from the response
        return ''.join(part.text for part in response.parts)
    except (ValueError, IndexError):
        # This runs if the response is empty (e.g., blocked by a safety filter)
        if response.prompt_feedback and response.prompt_feedback.block_reason:
            reason = response.prompt_feedback.block_reason.name
            print(f"  -> SKIPPING: Prompt blocked due to: {reason}")
        else:
            print("  -> SKIPPING: Received an empty response from the API.")
        return None

def main():
    p = argparse.ArgumentParser(description="Distill Pirouette modules into potent engrams (Law, Philosophy, Art).")
    p.add_argument("modules_dir", default="C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/modules", help="Path to directory with *.md modules")
    p.add_argument("--out", default="./essentialized", help="Output directory for essentialized modules")
    p.add_argument("--limit", type=int, default=0, help="Limit the number of files to process")
    args = p.parse_args()

    # Ensure GOOGLE_API_KEY is set
    if not os.getenv('GOOGLE_API_KEY'):
        print("Error: GOOGLE_API_KEY environment variable not set.")
        return

    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
    model = get_model()
    
    src_dir = Path(args.modules_dir)
    files = sorted([f for f in src_dir.glob("*.md") if not f.name.lower().startswith('readme')])

    if args.limit > 0:
        files = files[:args.limit]

    print(f"Found {len(files)} modules to process.")

    for file_path in files:
        module_content = read_module(file_path)
        if module_content:
            print(f"Essentializing {file_path.name}...")
            essentialized_content = process_module(model, module_content, file_path.name)
            
            if essentialized_content:
                # -FIXED- Implements the new, safe naming convention.
                new_filename = f"{file_path.stem}_essentialized.md"
                save_module(args.out, new_filename, essentialized_content)
                print(f"  -> Successfully saved: {new_filename}")

if __name__ == "__main__":
    main()