#!/usr/bin/env python3
"""
Falsifiability Ledger Extractor

This script scans a directory of Pirouette Framework markdown files,
finds all "Falsifiable Criteria" sections, and compiles them into
a single master markdown file for review and pipeline planning.
"""

import argparse
import re
from pathlib import Path
from typing import List

def extract_criteria_blocks(content: str) -> List[str]:
    """
    Finds all blocks of text that constitute falsifiability criteria.
    
    This regex finds a line starting with (optional bullet) **Falsifiable Criteria...**
    and captures everything from that line until the *next* heading
    (## Philosophy, ## Art) or a horizontal rule (---).
    """
    
    # Regex to find the start of a falsifiability section.
    # It looks for a bolded line that contains "Falsifiable Criteria" (or variations).
    # (?i) -> case-insensitive
    # (?-s) -> . does NOT match newline
    # (?s) -> . MATCHES newline
    # We are looking for the heading line, then capturing everything after it
    # until we hit a "stop" condition.
    
    # Find the heading line itself, e.g., "**Falsifiable Criteria:**"
    start_regex = re.compile(
        r"(^\s*(?:\*\s+)?\*\*Falsifiab(?:le|lity)\s+Crit(?:erion|eria)[^\*]*\*\*.*$)",
        re.IGNORECASE | re.MULTILINE
    )
    
    # Find the next thing that is *not* part of the criteria.
    # This is either the next H2 heading for Philosophy/Art, or a rule.
    end_regex = re.compile(
        r"(^\s*##\s+(?:Philosophy|Art)\b|^\s*---+)",
        re.IGNORECASE | re.MULTILINE
    )

    criteria_blocks = []
    
    for match in start_regex.finditer(content):
        start_index = match.start()
        
        # Find the end of this block
        end_match = end_regex.search(content, match.end())
        end_index = end_match.start() if end_match else len(content)
        
        block = content[start_index:end_index].strip()
        if block:
            criteria_blocks.append(block)
            
    return criteria_blocks

def main():
    """
    Main execution function.
    """
    parser = argparse.ArgumentParser(
        description="Compile a Falsifiability Ledger from Pirouette modules."
    )
    parser.add_argument(
        "--input-dir",
        type=str,
        required=True,
        help="Directory containing the .md module files."
    )
    parser.add_argument(
        "--output-file",
        type=str,
        default="FALSIFIABILITY_LEDGER.md",
        help="Path to the master output markdown file."
    )
    args = parser.parse_args()

    input_path = Path(args.input_dir)
    output_file = Path(args.output_file)
    
    if not input_path.is_dir():
        print(f"Error: Input directory not found: {input_path}")
        return

    ledger = ["# Pirouette Framework: Falsifiability Ledger\n"]
    ledger.append(f"Master compilation of all falsifiable criteria for pipeline optimization.\n")
    
    found_files = 0
    found_blocks = 0

    # Iterate through all .md files in the directory
    for file in sorted(input_path.glob("*.md")):
        print(f"Processing: {file.name}...")
        try:
            content = file.read_text(encoding="utf-8")
            blocks = extract_criteria_blocks(content)
            
            if blocks:
                found_files += 1
                ledger.append(f"\n---\n\n## {file.name}\n")
                for i, block in enumerate(blocks):
                    found_blocks += 1
                    if i > 0:
                        ledger.append("\n***\n") # Add separator for multiple blocks in one file
                    ledger.append(block)
                print(f"  -> Found {len(blocks)} criteria block(s).")
            else:
                print("  -> No criteria section found.")

        except Exception as e:
            print(f"  -> ERROR processing file: {e}")

    # Write the compiled ledger
    try:
        output_file.write_text("\n".join(ledger), encoding="utf-8")
        print("\n" + "="*30)
        print("Done.")
        print(f"Found {found_blocks} criteria blocks in {found_files} files.")
        print(f"Falsifiability Ledger written to: {output_file}")
    except Exception as e:
        print(f"Error writing output file: {e}")

if __name__ == "__main__":
    main()
