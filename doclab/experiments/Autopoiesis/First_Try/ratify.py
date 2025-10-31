import os
import yaml
import re
import google.generativeai as genai
import time

# --- 1. CONFIGURATION ---
# Define the three source directories for the competing weaves
WEAVE_PATHS = [
    "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/refactored_weaves/weave_balanced/DOMA",
    "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/autopoietic_weaves/weave_autopoietic/DOMA",
    "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/grounded_cello_weaves/weave_grounded_cello/DOMA"
]
RATIFIED_CANON_PATH = "C:/Users/keatw/OneDrive/Documents/Doclab/Big_Datasets/target/paper/Pirouette_Volume_6/doclab/experiments/Autopoiesis/debated_rework_3"
MODERN_PREFIXES = ("CORE", "INST", "DOMA", "DYN")


try:
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])
except KeyError:
    print("FATAL: GOOGLE_API_KEY environment variable not found.")
    exit()

# --- 2. UTILITY FUNCTIONS ---
def parse_module_robust(filepath):
    """Robustly parses a markdown file, now with better error handling."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            full_content = f.read()
        parts = full_content.split('---')
        if len(parts) < 3: return None
        metadata = yaml.safe_load(parts[1])
        if not isinstance(metadata, dict): return None
        metadata['full_content'] = full_content
        return metadata
    except Exception as e:
        print(f"Warning: Low-level parsing error for {os.path.basename(filepath)}: {e}")
        return None

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

# --- 3. THE RATIFICATION ENGINE ---

def find_competing_modules(*weave_paths):
    """Scans all weave directories, now with more robust 'replaces' parsing."""
    competitors = {}
    print("\nScanning for refactored modules...")
    for path in weave_paths:
        if not os.path.exists(path): continue
        for root, _, files in os.walk(path):
            for file in files:
                if file.endswith(".md"):
                    module = parse_module_robust(os.path.join(root, file))
                    if module and 'replaces' in module and module['replaces']:
                        # Handle both list and string 'replaces' fields
                        original_ids = module['replaces']
                        if isinstance(original_ids, str):
                            original_ids = [original_ids] # Convert to list
                        
                        for original_id in original_ids:
                            if original_id not in competitors:
                                competitors[original_id] = []
                            competitors[original_id].append(module)
    print(f"Found {len(competitors)} unique original modules to process.")
    return competitors


def synthesize_and_ratify(original_id, competing_modules):
    """Constructs the final, hyper-specific synthesis prompt."""
    
    base_prompt = f"""
You are the Steward of the Pirouette Framework, a hyper-vigilant AI moderator.
Your task is to synthesize competing versions of a refactored module into a single, definitive, 'ratified' version.

The original module is: **{original_id}**

Analyze the following competing versions:
"""
    
    version_labels = ["Version A: The 'Balanced' Weave", "Version B: The 'Autopoietic' Weave", "Version C: The 'Grounded Cello' Weave"]
    for i, version in enumerate(competing_modules):
        base_prompt += f"\n---\n**{version_labels[i]}**\n{version['full_content']}\n---"

    final_mandate = """
**YOUR MANDATE (Follow these rules without deviation):**

1.  **Synthesize:** Create a *new* module that integrates the best qualities of all provided versions.
2.  **The Disratification Clause:** If all versions are flawed, you may **disratify** them. If you do so, the *very first line* of the markdown body (immediately after the `---`) MUST be the `§X · Justification for Disratification` section.
3.  **CRITICAL FORMATTING RULES:**
    * **START WITH DELIMITER:** Your entire response MUST begin with `---` on the very first line. No preamble.
    * **YAML TITLES:** If a `title` value contains a colon (`:`), the entire title MUST be enclosed in double quotes (`"`). Example: `title: "My Title: A Subtitle"`
    * **CLEAN KEYS:** Do not add extra characters to YAML keys. Correct: `id:`. Incorrect: `:id:`.
    * **PLACEHOLDER ID:** Use the placeholder `id: XXX-000` and suggest a `module_type`.
4.  **Final Output:** Your output must be a single, complete, perfectly formatted markdown file.

Proceed.
"""
    
    prompt = base_prompt + final_mandate
    
    print(f"--- Convening {len(competing_modules)}-way debate for {original_id} ---")
    model = genai.GenerativeModel('gemini-2.5-pro')
    try:
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"--- ERROR: API call failed for {original_id}. Reason: {e} ---"

def sanitize_and_save_ratified_module(module_text, original_id, counters):
    """Saves the final module, with the ultimate pre-parsing sanitizer."""
    try:
        # --- THE ULTIMATE SANITIZER ---
        
        # 1. Ensure the text starts with a YAML delimiter.
        clean_text = module_text.strip()
        if not clean_text.startswith('---'):
            # Attempt to fix by finding the first likely YAML key
            first_key_match = re.search(r'\w+:', clean_text)
            if first_key_match:
                clean_text = '---\n' + clean_text[first_key_match.start():]
        
        # 2. Split front-matter from content
        parts = re.split(r'---', clean_text, maxsplit=2)
        if len(parts) < 3:
            print(f"❌ FATAL ERROR for {original_id}: Sanitizer failed. LLM output was severely malformed. Skipping.")
            return

        front_matter_str, content = parts[1], parts[2]

        # 3. Fix unquoted colons in titles
        front_matter_str = re.sub(r'^(title:\s*)([^"\n]+:[^"\n]+)$', r'\1"\2"', front_matter_str, flags=re.MULTILINE)
        
        # 4. Attempt to parse the sanitized YAML
        front_matter = yaml.safe_load(front_matter_str)
        if not isinstance(front_matter, dict):
            print(f"❌ FATAL ERROR for {original_id}: Could not parse sanitized YAML. Skipping.")
            return

        # --- SAVE LOGIC ---
        ai_suggestion = front_matter.get('module_type', 'domain-application')
        category_map = { 'core': 'CORE', 'instrument': 'INST', 'domain': 'DOMA', 'dynamics': 'DYN' }
        category_prefix = 'DOMA'
        for key, prefix in category_map.items():
            if key in ai_suggestion:
                category_prefix = prefix
                break

        counters[category_prefix] += 1
        new_id = f"{category_prefix}-{counters[category_prefix]:03d}"
        
        front_matter['id'] = new_id
        front_matter['replaces'] = [original_id]
        front_matter['status'] = 'ratified'
        
        updated_front_matter_str = yaml.dump(front_matter, sort_keys=False)
        updated_module_text = f"---\n{updated_front_matter_str}---\n{content.strip()}"
        
        canon_path = os.path.join(RATIFIED_CANON_PATH, category_prefix)
        os.makedirs(canon_path, exist_ok=True)
        file_path = os.path.join(canon_path, f"{new_id}.md")
        
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(updated_module_text)
        print(f"✅ Ratified and saved: {file_path} (from {original_id})")
        
    except Exception as e:
        print(f"❌ CRITICAL SAVE ERROR for {original_id}: {e}. The AI output was likely malformed.")


# --- 4. THE RATIFICATION WORKFLOW ---
def main():
    print("### COMMENCING THE FINAL, PRODUCTION-READY SYNTHESIS ###")
    
    id_counters = get_id_counters(RATIFIED_CANON_PATH)
    all_refactored_modules = find_competing_modules(*WEAVE_PATHS)
    
    for original_id, versions in all_refactored_modules.items():
        if len(versions) > 1:
            ratified_text = synthesize_and_ratify(original_id, versions)
        else:
            print(f"--- Promoting single version for {original_id} ---")
            ratified_text = versions[0]['full_content']

        sanitize_and_save_ratified_module(ratified_text, original_id, id_counters)
        time.sleep(1.5)

if __name__ == "__main__":
    main()