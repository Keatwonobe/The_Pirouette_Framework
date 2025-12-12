"""
DDE-Pirouette: Wikipedia Stream Ingester (The Hawk-Eye Adapter)
---------------------------------------------------------------
Ingests massive XML dumps (enwiki-latest-pages-articles.xml) into the DDE
without exploding RAM. Treats every article as a Virtual Shard.

Usage:
    python DDE_Wiki_Ingest.py enwiki-latest.xml --limit 10000
"""

import sys
import os
import argparse
import re
import xml.etree.ElementTree as ET
import time
from pathlib import Path
import hashlib
import numpy as np
import datetime

# Import the Core Framework
from DDE_Pirouette import DDEPirouette, PirouetteMetadata

# ---------------------------------------------------------------------------
# HELPER: fast wikimarkup cleaner (Adapted from your hawk-27.py)
# ---------------------------------------------------------------------------
def clean_wiki_text(text):
    if not text: return ""
    # Remove redirects
    if text.lower().startswith("#redirect"):
        return None
    
    # Basic stripping of heavy markup
    # Remove file attachments
    text = re.sub(r'\[\[File:.*?\]\]', '', text)
    text = re.sub(r'\[\[Image:.*?\]\]', '', text)
    # Remove references <ref>...</ref>
    text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref.*?>', '', text)
    # Remove templates {{...}} - nested is hard with regex, this is a rough pass
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
    # Remove headers ==...==
    text = re.sub(r'=+.*?=+', '', text)
    # Clean links [[Link|Text]] -> Text
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    # Remove residual tags
    text = re.sub(r'<.*?>', '', text)
    
    # Compress whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    return text

# ---------------------------------------------------------------------------
# CLASS: Virtual DDE (Updated for v7.3 Compliance)
# ---------------------------------------------------------------------------
class WikiPirouette(DDEPirouette):
    """
    Extension of DDEPirouette that handles 'Virtual Files' passed directly
    from the XML stream. Adapted for v7.3 Framework API.
    """
    def __init__(self, domain="WIKIPEDIA_OMNIBUS", **kwargs):
        # Initialize parent without the domain arg
        super().__init__(**kwargs) 
        self.domain_scope = domain

    def _calculate_entropy(self, text):
        """Simple Shannon entropy approximation for text."""
        if not text: return 0.0
        prob = [text.count(c) / len(text) for c in set(text)]
        return -sum(p * np.log2(p) for p in prob)

    def ingest_virtual_article(self, title, raw_text, source_id):
        """
        Ingest a single wikipedia article as a DDE entry.
        """
        # 1. Clean
        clean_text = clean_wiki_text(raw_text)
        if not clean_text or len(clean_text) < 200:
            return False 

        # 2. Generate ID
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        module_id = f"WIKI-{safe_title}"

        # 3. Calculate Metrics (v7.3 Compatible)
        entropy = self._calculate_entropy(clean_text)
        coherence_target = 0.5 + (0.1 * entropy)
        
        # v7.3 PirouetteMetadata uses specific fields (module_id, domain, engrams)
        # We map the Wiki data to these fields.
        meta = PirouetteMetadata(
            module_id=module_id,
            domain=self.domain_scope,
            status="ingested",
            coherence_target=coherence_target,
            engrams=[f"wiki_id:{source_id}", f"entropy:{entropy:.2f}"],
            created_at=datetime.utcnow().isoformat()
        )
        
        # 4. Register directly (skipping full image encoding to save time/RAM)
        # We create a "minified" manifest entry manually
        self.pirouette_registry[module_id] = meta
        self.manifest[module_id] = {
            'shape': (len(clean_text), 1), # Virtual shape
            'stats': {'text_length': len(clean_text)},
            'pirouette': meta.to_dict(),
            'checksum': hashlib.sha256(clean_text.encode()).hexdigest()
        }
        
        # 5. Vocabulary Integration (Manual update for v7.3)
        # We tokenize by simple splitting to avoid heavy NLP libs
        tokens = set(clean_text.split())
        for token in tokens:
            if token not in self.vocab:
                code = self._hash_token(token)
                self.vocab[token] = code
                self.reverse_vocab[code] = token
        
        return True

# ---------------------------------------------------------------------------
# THE STREAMER
# ---------------------------------------------------------------------------
def stream_wikipedia(xml_path, dde, limit=None, save_interval=1000):
    print(f"🦅 HAWK-EYE INGEST: Scanning {xml_path}...")
    
    context = ET.iterparse(xml_path, events=('end',))
    
    count = 0
    ingested = 0
    start_time = time.time()
    
    # Namespace map often needed for Wiki XML
    prefix = "{http://www.mediawiki.org/xml/export-0.10/}"

    for event, elem in context:
        if elem.tag == f"{prefix}page":
            try:
                # Extract Title
                title_node = elem.find(f"{prefix}title")
                title = title_node.text if title_node is not None else "Unknown"
                
                # Extract ID
                id_node = elem.find(f"{prefix}id")
                page_id = id_node.text if id_node is not None else "0"

                # Extract Text
                revision = elem.find(f"{prefix}revision")
                if revision:
                    text_node = revision.find(f"{prefix}text")
                    raw_text = text_node.text if text_node is not None else ""
                    
                    # --- THE INGESTION ---
                    success = dde.ingest_virtual_article(title, raw_text, page_id)
                    if success:
                        ingested += 1
                        sys.stdout.write(f"\r   [+] Ingested: {title[:40]:<40} (Total: {ingested})")
                        sys.stdout.flush()
                
                count += 1

                # Periodic Save
                if ingested % save_interval == 0 and ingested > 0:
                    dde.save_manifest_minified(f"dde_wiki_checkpoint_{ingested}.json")

                # Limit Check
                if limit and ingested >= limit:
                    print(f"\n🛑 Limit of {limit} articles reached.")
                    break
                    
            except Exception as e:
                # Wikipedia is messy, don't let one bad char crash the flight
                pass
            finally:
                # CRITICAL: Clear element to free RAM
                elem.clear()
                
    total_time = time.time() - start_time
    print(f"\n\n--- STREAM COMPLETE ---")
    print(f"Scanned: {count} pages")
    print(f"Ingested: {ingested} valid articles")
    print(f"Time: {total_time:.2f}s")



# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="DDE Wiki Ingester")
    parser.add_argument("xml_file", type=str, help="Path to unzipped .xml file")
    parser.add_argument("--limit", type=int, default=None, help="Max articles to ingest (for testing)")
    args = parser.parse_args()
    
    if not os.path.exists(args.xml_file):
        print("❌ XML file not found.")
        sys.exit(1)
        
    # Initialize our Virtual DDE
    wiki_dde = WikiPirouette(domain="WIKIPEDIA_OMNIBUS")
    
    # Run the stream
    try:
        stream_wikipedia(args.xml_file, wiki_dde, limit=args.limit)
    except KeyboardInterrupt:
        print("\n⚠️  Interrupted by user. Saving progress...")
    
    # Final Save
    wiki_dde.save_manifest_minified("dde_wiki_manifest_final.json")
    print("✅ Manifest Saved.")