#!/usr/bin/env python3
"""
fix_yaml_frontmatter.py
Scans a directory of Markdown files and permanently fixes common YAML
frontmatter parsing errors, primarily by converting double-quoted strings
with backslashes (like LaTeX) to single-quoted strings.

Usage:
  python fix_yaml_frontmatter.py --dict ./dictionary
"""
import argparse
import re
from pathlib import Path

# Regex to find lines like `key: "value with \ backslash"`
# It captures the key and the opening quote to preserve indentation and spacing.
# It specifically looks for a backslash inside the double quotes.
PROBLEM_PATTERN = re.compile(r"""
    ^
    (?P<key_part>\s*[\w\s-]+:\s*) # Capture 'key: ' part
    "                               # Match opening double quote
    (?P<content>[^"]*\\_?[^"]*)     # Capture content with at least one backslash
    "                               # Match closing double quote
    (?P<rest>\s*)$                   # Capture any trailing whitespace/comment
    """, re.VERBOSE)

# Regex for other common YAML issues found in your traceback
MANUAL_FIX_PATTERNS = {
    # 'term: ""Good tired""' -> 'term: "Good tired"'
    r'(""Good tired"")': '"Good tired"',
    # 'expected_signals: [>70% ...]' -> 'expected_signals: [">70% ..."]'
    r'(>\d+%)': r"'>\1'",
}


def fix_file_content(content: str) -> tuple[str, bool]:
    """
    Fixes the frontmatter within the given file content.

    Returns a tuple of (new_content, has_changed_flag).
    """
    lines = content.splitlines(True)
    new_lines = []
    in_frontmatter = False
    has_changed = False

    for i, line in enumerate(lines):
        if line.strip() == '---':
            in_frontmatter = not in_frontmatter
            if not in_frontmatter and i > 0: # Closing '---'
                in_frontmatter = False # Explicitly turn off
        
        if in_frontmatter and i > 0:
            original_line = line
            # Fix 1: LaTeX backslash issue
            match = PROBLEM_PATTERN.match(line)
            if match:
                key_part = match.group("key_part")
                content_part = match.group("content")
                rest = match.group("rest")
                # Replace double quotes with single quotes
                line = f"{key_part}'{content_part}'{rest}\n"
                
            # Fix 2: Other specific, known issues
            for pattern, replacement in MANUAL_FIX_PATTERNS.items():
                line = re.sub(pattern, replacement, line)

            if line != original_line:
                has_changed = True

        new_lines.append(line)

    return "".join(new_lines), has_changed


def main():
    parser = argparse.ArgumentParser(description="Permanently fix YAML frontmatter in Pirouette dictionary files.")
    parser.add_argument("--dict", required=True, help="Path to the dictionary directory.")
    args = parser.parse_args()

    dict_path = Path(args.dict)
    if not dict_path.is_dir():
        print(f"Error: Directory not found at '{dict_path}'")
        return

    print(f"Scanning for YAML issues in '{dict_path}'...")
    fixed_files_count = 0
    
    md_files = sorted(list(dict_path.glob("*.md")))

    for filepath in md_files:
        try:
            content = filepath.read_text(encoding='utf-8')
            new_content, changed = fix_file_content(content)
            
            if changed:
                filepath.write_text(new_content, encoding='utf-8')
                print(f"  Fixed -> {filepath.name}")
                fixed_files_count += 1
        except Exception as e:
            print(f"  ERROR processing {filepath.name}: {e}")
            
    print(f"\nDone. Fixed {fixed_files_count} files.")


if __name__ == "__main__":
    main()