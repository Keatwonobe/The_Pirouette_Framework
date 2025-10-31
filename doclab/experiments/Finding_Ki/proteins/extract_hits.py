#!/usr/bin/env python3
import re
from tqdm import tqdm

def parse_match_headers(match_file_path):
    """
    Parses the analysis report to extract a unique set of protein headers.

    Args:
        match_file_path (str): Path to the analysis report file.

    Returns:
        set: A set of unique protein header IDs that are Ki matches.
    """
    print(f"Parsing match headers from '{match_file_path}'...")
    # Using a set for fast, O(1) average time complexity lookups.
    hit_headers = set()
    try:
        with open(match_file_path, 'r') as f:
            for line in f:
                # This regex is designed to be robust and capture header IDs
                # like '1h0h_A', '7sqc_F0', '9cpc_1P', etc. from the report.
                match = re.match(r'^\s*([a-zA-Z0-9_]+)\s+', line)
                if match:
                    header_id = match.group(1)
                    # Avoid capturing the table header "header"
                    if header_id.lower() != 'header':
                        hit_headers.add(header_id)
    except FileNotFoundError:
        print(f"ERROR: Match file not found at '{match_file_path}'")
        return None
        
    print(f"Found {len(hit_headers)} unique protein IDs to extract.")
    return hit_headers

def extract_fasta_hits(database_path, hit_headers, output_path):
    """
    Scans a large FASTA database and writes entries with matching headers to a new file.

    Args:
        database_path (str): Path to the large source FASTA file.
        hit_headers (set): A set of header IDs to extract.
        output_path (str): Path for the output FASTA file.
    """
    if not hit_headers:
        print("No hit headers provided. Exiting.")
        return

    print(f"Scanning '{database_path}' to extract hits...")
    
    # Using a with statement ensures files are properly closed.
    try:
        with open(database_path, 'r') as db_file, open(output_path, 'w') as out_file:
            current_sequence_parts = []
            current_header = None
            found_match = False
            
            # Using tqdm for a progress bar, as this can be a long process.
            for line in tqdm(db_file, desc="Scanning Database"):
                if line.startswith('>'):
                    # --- Process the previous entry before starting a new one ---
                    if current_header and found_match:
                        out_file.write(current_header)
                        out_file.write("".join(current_sequence_parts))
                        out_file.write("\n")

                    # --- Start the new entry ---
                    current_header = line
                    current_sequence_parts = []
                    
                    # Extract the ID from the full header line, e.g., '>102l_A ...' -> '102l_A'
                    header_id_match = re.match(r'>\s*([a-zA-Z0-9_]+)', line)
                    if header_id_match and header_id_match.group(1) in hit_headers:
                        found_match = True
                    else:
                        found_match = False
                else:
                    # Append sequence parts only if it's a potential match
                    if found_match:
                        current_sequence_parts.append(line.strip())
            
            # --- Don't forget to write the very last entry in the file if it was a match ---
            if current_header and found_match:
                out_file.write(current_header)
                out_file.write("".join(current_sequence_parts))
                out_file.write("\n")

    except FileNotFoundError:
        print(f"ERROR: Database file not found at '{database_path}'")
        return

    print(f"\n✅ Extraction complete. All matching sequences saved to '{output_path}'.")


if __name__ == '__main__':
    # --- Configuration ---
    # The original, complete FASTA database file.
    DATABASE_FILE = "pdb_seqres.txt" 
    
    # The text file containing the list of Ki matches.
    MATCH_FILE = "Analysis Complete.txt"
    
    # The new FASTA file that will be created with only the hits.
    OUTPUT_HITS_FILE = "ki_hits.txt"

    # --- Execution ---
    target_ids = parse_match_headers(MATCH_FILE)
    if target_ids:
        extract_fasta_hits(DATABASE_FILE, target_ids, OUTPUT_HITS_FILE)

