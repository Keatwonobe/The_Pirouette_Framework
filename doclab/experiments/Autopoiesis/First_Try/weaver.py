import os
import yaml
import re
import google.generativeai as genai
import time

# --- 1. CONFIGURATION & API SETUP ---
MODULES_PATH = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/modules"
OUTPUT_PATH = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/essentialization_pass"
MODERN_PREFIXES = ("CORE", "INST", "DOMA", "DYN")
TARGET_PREFIXES = ("PPS", "PNS", "TEN")

try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("FATAL: GOOGLE_API_KEY environment variable not found.")
    exit()

# --- 2. CORE FUNCTIONS (No changes to API calls or parsing) ---

def call_language_model(prompt, weaving_style="grounded_cello"):
    """Calls the Google Generative AI model to rewrite a module."""
    print(f"--- Calling Google API with style: {weaving_style} ---")
    model = genai.GenerativeModel('gemini-2.5-pro')
    try:
        response = model.generate_content(prompt)
        if hasattr(response, 'text'):
            return response.text
        else:
            if hasattr(response, 'prompt_feedback') and response.prompt_feedback.block_reason:
                 return f"--- ERROR: Generation blocked for reason: {response.prompt_feedback.block_reason} ---"
            return f"--- ERROR: Could not generate module. Received an unexpected response format. ---"
    except Exception as e:
        print(f"An error occurred with the API call: {e}")
        return f"--- ERROR: Could not generate module. Reason: {e} ---"

def get_modern_context(all_modules):
    """Gathers the content of all modern modules to provide as context."""
    context_str = "--- CONTEXT: MODERN CORE PRINCIPLES ---\n\n"
    for mod in all_modules.values():
        if mod.get('id', '').startswith(MODERN_PREFIXES):
            context_str += f"## Module: {mod['id']}\n{mod.get('full_content', '')}\n\n"
    return context_str

def rewrite_module(module_content, context, style="grounded_cello"):
    """Constructs the prompt and calls the LLM to rewrite a single module."""
    # Modified prompt: Ask for a CATEGORY, not a full ID.
    prompt = f"""
You are an AI assistant specialized in the Pirouette Framework, tasked with "The Great Refactoring."
Your goal is to take an old module and rewrite it into a new, modernized "time-first" version.

**CRITICAL INSTRUCTIONS:**
1.  **Grounding:** The new module MUST be grounded in the principles of the new framework.
2.  **Suggest a Category:** In the YAML front-matter, you must suggest a module_type that maps to one of the four official categories: Core Principle, Instrumentation, Domain Application, or Dynamics Model. Do not invent new categories. The script will assign the final ID number.
3.  **Clarity and Preservation:** Preserve the core insight of the original module but re-express its mechanics in the new terminology. Consider making an INST or instrument module for the technology if it is covered already.
4.  **Format:** The output must be a single, complete markdown file with valid YAML front-matter. Do not name the file with a colon [:] in the filename.
5.  **Weaving Style:** Apply the following style: '{style}'.
6.  **Lagrangian Connection** The new module should show how it connects to the core Lagrangian (CORE-006).
7.  **The Assemblé** The Assemblé section at the end of the module is the most important part. It should be a short, poetic, and profound summary of the module's core philosophical implication. Answer the question: 'Why does this concept matter to a Weaver?' Use the '>' markdown for a blockquote.

---
**MODERN CONTEXT INFORMATION:**
{context}
---
**OLD MODULE TO REWRITE:**
{module_content}
---
**YOUR REWRITTEN MODULE:**
"""
    return call_language_model(prompt, weaving_style=style)

def parse_module_robust(filepath):
    """Robustly parses a markdown file, tolerating YAML errors."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()
        parts = full_content.split('---')
        if len(parts) < 3:
            base_name = os.path.basename(filepath).replace('.md', '')
            return {'id': f"UNKNOWN_{base_name}", 'title': base_name, 'full_content': full_content}
        front_matter_str = parts[1]
        content = "---".join(parts[2:]).strip()
        metadata = {}
        try:
            metadata = yaml.safe_load(front_matter_str)
            if not isinstance(metadata, dict): metadata = {}
        except yaml.YAMLError:
            metadata = {}
        if 'id' not in metadata:
            id_match = re.search(r'id:\s*(\S+)', front_matter_str)
            metadata['id'] = id_match.group(1) if id_match else f"UNKNOWN_{os.path.basename(filepath).replace('.md', '')}"
        if 'title' not in metadata:
            title_match = re.search(r'title:\s*(.+)', front_matter_str)
            metadata['title'] = title_match.group(1).strip() if title_match else metadata['id']
        return {**metadata, 'full_content': full_content, 'content_body': content}
    except Exception as e:
        print(f"❌ Error processing file {filepath}: {e}")
        return None

# --- 3. STATE-AWARE FUNCTIONS (NEW and MODIFIED) ---

def get_id_counters(output_dir):
    """Scans the output directory to find the highest number for each prefix."""
    counters = {prefix: 0 for prefix in MODERN_PREFIXES}
    if not os.path.exists(output_dir):
        return counters
    
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".md"):
                match = re.match(r'([A-Z]+)-(\d+)', file)
                if match:
                    prefix, num = match.groups()
                    if prefix in counters:
                        counters[prefix] = max(counters[prefix], int(num))
    print(f"Initialized ID counters: {counters}")
    return counters

def get_completed_modules(output_dir):
    """Scans output for modules that have a 'replaces' tag to avoid re-work."""
    completed = set()
    if not os.path.exists(output_dir):
        return completed
        
    for root, _, files in os.walk(output_dir):
        for file in files:
            if file.endswith(".md"):
                module_path = os.path.join(root, file)
                parsed = parse_module_robust(module_path)
                if parsed and 'replaces' in parsed and parsed['replaces']:
                    # The 'replaces' tag can be a list or a single item
                    original_ids = parsed['replaces']
                    if isinstance(original_ids, list):
                        for old_id in original_ids:
                            completed.add(old_id)
                    elif isinstance(original_ids, str):
                        completed.add(original_ids)
    print(f"Found {len(completed)} already refactored modules. They will be skipped.")
    return completed

def save_new_module(module_text, original_id, weave_name, counters):
    """Saves the module with a new, unique, incremented ID."""
    try:
        parts = re.split(r'---', module_text, maxsplit=2)
        if len(parts) < 3:
            print(f"Warning: LLM output was malformed. Could not save.")
            return

        front_matter = yaml.safe_load(parts[1])
        if not isinstance(front_matter, dict):
             print(f"Warning: LLM output had invalid YAML. Could not save.")
             return

        # Determine category based on AI's suggestion
        ai_suggestion = front_matter.get('module_type', 'domain-application')
        category_map = {
            'core-principle': 'CORE',
            'instrumentation': 'INST',
            'analytics-core': 'INST',
            'domain-application': 'DOMA',
            'dynamics-model': 'DYN'
        }
        category_prefix = 'DOMA' # Default
        for key, prefix in category_map.items():
            if key in ai_suggestion:
                category_prefix = prefix
                break

        # Generate the new unique ID
        counters[category_prefix] += 1
        new_id = f"{category_prefix}-{counters[category_prefix]:03d}"
        
        # Update the module text with the correct ID and 'replaces' tag
        front_matter['id'] = new_id
        front_matter['replaces'] = [original_id] # Track provenance
        
        updated_front_matter_str = yaml.dump(front_matter, sort_keys=False)
        updated_module_text = f"---\n{updated_front_matter_str}---\n{parts[2].strip()}"
        
        # Save the file
        weave_path = os.path.join(OUTPUT_PATH, weave_name, category_prefix)
        os.makedirs(weave_path, exist_ok=True)
        file_path = os.path.join(weave_path, f"{new_id}.md")
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_module_text)
        print(f"✅ Successfully saved: {file_path} (Replaced {original_id})")

    except Exception as e:
        print(f"❌ Error saving module: {e}")


# --- 4. THE STATE-AWARE WORKFLOW ---
def main(weave_name="weave_1", style="grounded_cello"):
    # Initial setup
    weave_dir = os.path.join(OUTPUT_PATH, weave_name)
    id_counters = get_id_counters(weave_dir)
    completed_modules = get_completed_modules(weave_dir)
    
    # Load all source modules
    all_modules = {}
    if not os.path.exists(MODULES_PATH):
        print(f"FATAL: Modules directory not found at '{MODULES_PATH}'")
        return
    for filename in os.listdir(MODULES_PATH):
        if filename.endswith(".md"):
            path = os.path.join(MODULES_PATH, filename)
            parsed = parse_module_robust(path)
            if parsed and 'id' in parsed:
                all_modules[parsed['id']] = parsed

    modern_context = get_modern_context(all_modules)
    
    modules_to_refactor = {k: v for k, v in all_modules.items() if k.startswith(TARGET_PREFIXES)}
    print(f"Found {len(modules_to_refactor)} modules to refactor.")

    for module_id, module_data in modules_to_refactor.items():
        # Skip modules that have already been refactored in this weave
        if module_id in completed_modules:
            print(f"\nSkipping module (already refactored): {module_id}")
            continue

        print(f"\nRefactoring module: {module_id}...")
        original_content = module_data['full_content']
        new_module_text = rewrite_module(original_content, modern_context, style=style)
        
        save_new_module(new_module_text, module_id, weave_name, id_counters)
        
        time.sleep(1.5)

if __name__ == "__main__":
    print("### STARTING WEAVE 2: grounded_cello REFACTORING ###")
    main(weave_name="weave_grounded_cello", style="grounded_cello")