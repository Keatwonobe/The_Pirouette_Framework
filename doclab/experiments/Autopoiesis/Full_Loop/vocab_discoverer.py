"""
DDE Vocabulary Discoverer v1.0

Rips through a folder of .md files and extracts every unique
word to create a master vocabulary .txt file. This file can
then be used to "prime" a DDE instance.
"""

import sys
import re
from pathlib import Path
from collections import Counter

def discover_vocabulary(folder_path_str: str, output_file_str: str):
    """
    Scans all .md files in a folder, finds all unique words,
    and saves them to a new .txt file.
    """
    
    folder_path = Path(folder_path_str)
    if not folder_path.is_dir():
        print(f"❌ Error: Path '{folder_path_str}' is not a valid directory.")
        return

    print("=" * 70)
    print(f"🧬 DISCOVERING Relational Language")
    print(f"   Source: ./{folder_path.name}/")
    print("=" * 70)
    
    md_files = list(folder_path.glob('*.md'))
    if not md_files:
        print(f"⚠️  No markdown files found in '{folder_path_str}'.")
        return

    master_vocab = set()
    word_count = 0
    
    # A simple regex to find "words".
    # This will find any sequence of letters, numbers,
    # apostrophes, or hyphens (e.g., "CORE-001", "Pirouette's", "self-aware")
    # It converts everything to lowercase for uniqueness.
    word_regex = re.compile(r"[\w'-]+")

    for md_path in md_files:
        try:
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read().lower() # Convert to lowercase
                
                words_found = word_regex.findall(content)
                master_vocab.update(words_found)
                word_count += len(words_found)
                
            print(f"  ✅ Scanned: {md_path.name} ({len(words_found)} words)")
        
        except Exception as e:
            print(f"  ❌ FAILED to scan {md_path.name}: {e}")

    # --------------------------------------------------------------------
    # STAGE 2: SAVING THE VOCABULARY
    # --------------------------------------------------------------------
    print("\n" + "─" * 70)
    print("STAGE 2: SAVING MASTER VOCABULARY")
    print("─" * 70)
    
    sorted_vocab = sorted(list(master_vocab))
    output_path = Path(output_file_str)
    
    try:
        with open(output_path, 'w', encoding='utf-8') as f:
            for word in sorted_vocab:
                f.write(f"{word}\n")
                
        print(f"\n🎉 SUCCESS! 🎉")
        print(f"   Total words scanned: {word_count}")
        print(f"   Unique words found:  {len(sorted_vocab)}")
        print(f"   Master vocab saved to: {output_path.name}")
        print("=" * 70)
        
    except Exception as e:
        print(f"❌ FAILED to write vocab file: {e}")


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("="*70)
        print("DDE Vocabulary Discoverer v1.0")
        print("="*70)
        print("Usage: python discover_vocab.py <path_to_scan_folder> <output_filename.txt>")
        print("\nExample:")
        print("  python discover_vocab.py ./modules_outbox master_vocab.txt")
        print("="*70)
        sys.exit(1)
        
    scan_folder = sys.argv[1]
    output_file = sys.argv[2]
    discover_vocabulary(scan_folder, output_file)