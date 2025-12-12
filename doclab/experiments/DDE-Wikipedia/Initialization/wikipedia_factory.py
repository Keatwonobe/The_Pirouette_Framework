"""
DDE-Pirouette: Wikipedia Factory (The Materializer)
---------------------------------------------------
Takes a DDE Checkpoint (Metadata/Vocab) and the Source XML,
and physically generates the RGBA Artifacts (Images) for the ingested articles.

Usage:
    python wiki_factory.py "path/to/wiki.xml" --checkpoint "dde_wiki_checkpoint_25000.json"
"""

import sys
import os
import argparse
import re
import xml.etree.ElementTree as ET
import json
import pandas as pd
import numpy as np
import glob
from pathlib import Path

# Import Core
try:
    from DDE_Pirouette import DDEPirouette, PirouetteMetadata
except ImportError:
    print("❌ CRITICAL: DDE_Pirouette.py not found.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# CONFIG & HELPERS
# ---------------------------------------------------------------------------
OUTPUT_DIR = "wiki_vault"

def clean_wiki_text(text):
    """Must match the ingestor logic exactly for consistency."""
    if not text: return ""
    if text.lower().startswith("#redirect"): return None
    try:
        text = re.sub(r'\[\[File:.*?\]\]', '', text)
        text = re.sub(r'\[\[Image:.*?\]\]', '', text)
        text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
        text = re.sub(r'<ref.*?>', '', text)
        text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
        text = re.sub(r'=+.*?=+', '', text)
        text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
        text = re.sub(r'<.*?>', '', text)
        return re.sub(r'\s+', ' ', text).strip()
    except:
        return None

def local_tag(tag):
    if not tag: return ""
    return tag.split('}', 1)[-1] if '}' in tag else tag

# ---------------------------------------------------------------------------
# CLASS: Factory DDE
# ---------------------------------------------------------------------------
class WikiFactory(DDEPirouette):
    def __init__(self, domain="WIKIPEDIA_OMNIBUS", **kwargs):
        super().__init__(**kwargs)
        self.domain_scope = domain
        # Silence the standard encode print spam for batch processing
        self.verbose = False 

    def generate_module_id(self, title):
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        return f"WIKI-{safe_title[:50]}"

    def text_to_dataframe(self, text):
        """
        Converts text into a DDE-compatible DataFrame.
        We split by lines to preserve some structural geography in the image.
        """
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if not lines:
            return pd.DataFrame(["<EMPTY>"], columns=["content"])
        return pd.DataFrame(lines, columns=["content"])

    def materialize_artifact(self, title, raw_text):
        """Generates and saves the PNG artifact."""
        clean_text = clean_wiki_text(raw_text)
        if not clean_text: return False
        
        module_id = self.generate_module_id(title)
        
        # Only process if it's in our target manifest
        if module_id not in self.manifest:
            return False
            
        # 1. Convert to DataFrame
        df = self.text_to_dataframe(clean_text)
        
        # 2. Retrieve Metadata from Checkpoint
        # We assume manifest is already loaded
        meta_dict = self.manifest[module_id].get('pirouette', {})
        if not isinstance(meta_dict, PirouetteMetadata):
            # Rehydrate if it's just a dict
            meta = PirouetteMetadata(
                module_id=module_id,
                domain=meta_dict.get('domain', 'WIKI'),
                status="materialized"
            )
        else:
            meta = meta_dict

        # 3. Encode (Quietly)
        # We temporarily redirect stdout to suppress "Encoding..." spam
        original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')
        try:
            img = self.encode(df, label=module_id, pirouette_meta=meta)
        except Exception:
            sys.stdout = original_stdout
            return False
        sys.stdout = original_stdout

        # 4. Save
        safe_name = "".join([c if c.isalnum() else "_" for c in title])[:100]
        filename = f"{OUTPUT_DIR}/{safe_name}.png"
        img.save(filename)
        
        return True

# ---------------------------------------------------------------------------
# MAIN PROCESS
# ---------------------------------------------------------------------------
def run_factory(xml_path, checkpoint_path, limit=None):
    print(f"🏭 DDE FACTORY ONLINE")
    print(f"   XML: {xml_path}")
    print(f"   Checkpoint: {checkpoint_path}")
    
    # 1. Setup Vault
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"   📁 Created vault: {OUTPUT_DIR}/")
    
    # 2. Initialize & Load
    factory = WikiFactory()
    print("   📖 Loading checkpoint/vocab (this may take a moment)...")
    try:
        factory.load_manifest(checkpoint_path)
        target_count = len(factory.manifest)
        vocab_size = len(factory.vocab)
        print(f"   ✅ Loaded {target_count} targets with {vocab_size} vocab words.")
    except Exception as e:
        print(f"   ❌ Failed to load checkpoint: {e}")
        return

    # 3. Stream & Materialize
    print("   ⚡ Streaming XML and materializing artifacts...")
    context = ET.iterparse(xml_path, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)

    processed = 0
    generated = 0
    
    for event, elem in context:
        if event == 'end':
            if local_tag(elem.tag) == "page":
                # Extract Title
                title = "Unknown"
                for child in elem:
                    if local_tag(child.tag) == "title":
                        title = child.text
                        break
                
                # Check if this is a target
                mid = factory.generate_module_id(title)
                if mid in factory.manifest:
                    
                    # Extract Text
                    raw_text = ""
                    try:
                        for child in elem:
                            if local_tag(child.tag) == "revision":
                                for rev in child:
                                    if local_tag(rev.tag) == "text": 
                                        raw_text = rev.text
                    except: pass

                    if raw_text:
                        success = factory.materialize_artifact(title, raw_text)
                        if success:
                            generated += 1
                            sys.stdout.write(f"\r   🖼️  Generated: {generated}/{target_count} | {title[:30]:<30}")
                            
                            if limit and generated >= limit:
                                print(f"\n   🛑 Test limit of {limit} reached.")
                                return

                # Cleanup
                elem.clear()
                root.clear()
                processed += 1
                if processed % 1000 == 0:
                    sys.stdout.write(f"\r   🔎 Scanned {processed} pages... (Generated: {generated})")

    print(f"\n\n✨ FACTORY RUN COMPLETE")
    print(f"   Generated {generated} images in '{OUTPUT_DIR}/'")

# ---------------------------------------------------------------------------
# ENTRY POINT
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_file", type=str)
    parser.add_argument("--checkpoint", type=str, required=True)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()

    if not os.path.exists(args.xml_file):
        print("❌ XML file not found.")
        sys.exit(1)

    run_factory(args.xml_file, args.checkpoint, args.limit)