import requests
import gzip
import re
import os

def create_download_list(output_file="gutenberg_urls.txt"):
    """
    Downloads the master file list from Project Gutenberg, finds all
    UTF-8 plain text ebooks, and saves their URLs to a file.
    """
    # URL for the master file list (ls-R.gz)
    master_list_url = "http://www.gutenberg.org/ls-R.gz"
    
    print(f"Downloading master file list from {master_list_url}...")
    
    try:
        # Download the compressed file list
        response = requests.get(master_list_url, stream=True)
        response.raise_for_status() # Raise an exception for bad status codes
        
        # Decompress the content on the fly
        # The content is decoded as UTF-8, ignoring errors for robustness
        content = gzip.decompress(response.content).decode('utf-8', errors='ignore')
        print("✓ Master file list downloaded and decompressed.")
        
    except requests.exceptions.RequestException as e:
        print(f"Error: Could not download the master file list. {e}")
        return

    # This regex finds lines ending in '-0.txt' or '-8.txt' (common text formats)
    # and captures the full path to the file.
    # Example path: ./files/1/10001/10001-0.txt
    text_file_regex = re.compile(r"\./(files/\d+/[\d\w]+/[\d\w]+-[08]\.txt)")
    
    # Find all matches in the decompressed content
    found_paths = text_file_regex.findall(content)
    
    if not found_paths:
        print("Error: Could not find any text file paths in the master list.")
        print("The format of the ls-R.gz file may have changed.")
        return
        
    print(f"Found {len(found_paths)} plain text ebooks.")
    
    # Base URL for constructing the full download links
    base_url = "http://www.gutenberg.org/"
    
    # Write the full URLs to the output file
    with open(output_file, 'w') as f:
        for path in found_paths:
            full_url = os.path.join(base_url, path).replace("\\", "/")
            f.write(full_url + "\n")
            
    print(f"✓ Successfully created '{output_file}' with all download URLs.")


if __name__ == "__main__":
    create_download_list()