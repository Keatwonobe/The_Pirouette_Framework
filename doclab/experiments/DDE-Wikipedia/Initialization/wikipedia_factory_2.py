"""
DDE-Pirouette: Wikipedia Factory v2.1 (Smart Resume)
----------------------------------------------------
Robust materialization engine with Checkpointing.
- Smart Resume: Skips existing PNGs in 'wiki_vault'.
- ID Debugger: prints ID mismatches to diagnose 0-generation issues.
- Aggressive GC: Keeps RAM flat during long fast-forward runs.

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
import gc
import contextlib
import io
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

    def generate_module_id(self, title):
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        return f"WIKI-{safe_title[:50]}"

    def text_to_dataframe(self, text):
        lines = [l.strip() for l in text.split('\n') if l.strip()]
        if not lines:
            return pd.DataFrame(["<EMPTY>"], columns=["content"])
        return pd.DataFrame(lines, columns=["content"])

    def artifact_exists(self, title):
        """Check if the PNG already exists in the vault."""
        safe_name = "".join([c if c.isalnum() else "_" for c in title])[:100]
        filename = f"{OUTPUT_DIR}/{safe_name}.png"
        return os.path.exists(filename)

    def materialize_artifact(self, title, raw_text):
        """Generates and saves the PNG artifact."""
        try:
            # 1. Checkpoint Check (Fast Resume)
            if self.artifact_exists(title):
                return "EXISTS"

            clean_text = clean_wiki_text(raw_text)
            if not clean_text: return False
            
            module_id = self.generate_module_id(title)
            
            # 2. Manifest Check
            if module_id not in self.manifest:
                return False
                
            # 3. Convert & Meta
            df = self.text_to_dataframe(clean_text)
            meta_dict = self.manifest[module_id].get('pirouette', {})
            if not isinstance(meta_dict, PirouetteMetadata):
                meta = PirouetteMetadata(
                    module_id=module_id,
                    domain=meta_dict.get('domain', 'WIKI'),
                    status="materialized"
                )
            else:
                meta = meta_dict

            # 4. Encode (Silenced)
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                img = self.encode(df, label=module_id, pirouette_meta=meta)

            # 5. Save
            safe_name = "".join([c if c.isalnum() else "_" for c in title])[:100]
            filename = f"{OUTPUT_DIR}/{safe_name}.png"
            img.save(filename)
            
            return True
            
        except Exception as e:
            sys.stderr.write(f"\n⚠️ Skipped corrupt artifact '{title}': {e}\n")
            return False

# ---------------------------------------------------------------------------
# MAIN PROCESS
# ---------------------------------------------------------------------------
def run_factory(xml_path, checkpoint_path, limit=None):
    print(f"🏭 DDE FACTORY v2.1 ONLINE")
    print(f"   XML: {xml_path}")
    print(f"   Checkpoint: {checkpoint_path}")
    
    if not os.path.exists(OUTPUT_DIR):
        os.makedirs(OUTPUT_DIR)
        print(f"   📁 Vault created: {OUTPUT_DIR}/")
    else:
        print(f"   📂 Vault found: {OUTPUT_DIR}/ (Smart Resume Enabled)")

    # 1. Load Manifest
    factory = WikiFactory()
    print("   🧹 Pre-load Garbage Collection...")
    gc.collect()
    
    print("   📖 Loading checkpoint...")
    try:
        factory.load_manifest(checkpoint_path)
        target_count = len(factory.manifest)
        print(f"   ✅ Targets Loaded: {target_count}")
    except Exception as e:
        print(f"   ❌ Failed to load checkpoint: {e}")
        return

    # 2. Stream
    print("   ⚡ Streaming XML...")
    try:
        context = ET.iterparse(xml_path, events=('start', 'end'))
        context = iter(context)
        event, root = next(context)

        processed = 0
        generated = 0
        skipped_existing = 0
        
        for event, elem in context:
            if event == 'end':
                if local_tag(elem.tag) == "page":
                    
                    # Extract Title
                    title = "Unknown"
                    try:
                        for child in elem:
                            if local_tag(child.tag) == "title":
                                title = child.text
                                break
                    except: pass
                    
                    if title:
                        # DEBUG PROBE: Check the first few IDs to ensure alignment
                        if processed < 5:
                            mid = factory.generate_module_id(title)
                            is_target = mid in factory.manifest
                            print(f"      [PROBE] '{title}' -> ID: {mid} | Target? {is_target}")

                        # Materialize
                        mid = factory.generate_module_id(title)
                        
                        if mid in factory.manifest:
                            # Extract Text only if it's a target
                            raw_text = ""
                            try:
                                for child in elem:
                                    if local_tag(child.tag) == "revision":
                                        for rev in child:
                                            if local_tag(rev.tag) == "text": 
                                                raw_text = rev.text
                            except: pass
                            
                            if raw_text:
                                result = factory.materialize_artifact(title, raw_text)
                                
                                if result == True:
                                    generated += 1
                                    sys.stdout.write(f"\r   🖼️  Generated: {generated} | {title[:30]:<30}")
                                elif result == "EXISTS":
                                    skipped_existing += 1
                                    if skipped_existing % 100 == 0:
                                        sys.stdout.write(f"\r   ⏩ Resuming... Skipped {skipped_existing} existing artifacts.")

                                if limit and generated >= limit:
                                    print(f"\n   🛑 Limit of {limit} reached.")
                                    return

                    # Cleanup
                    elem.clear()
                    root.clear()
                    processed += 1
                    
                    if processed % 1000 == 0:
                        gc.collect()
                        if generated == 0 and skipped_existing == 0:
                             sys.stdout.write(f"\r   🔎 Scanned {processed} pages... (No matches yet)")

    except Exception as e:
        print(f"\n❌ STREAM ERROR: {e}")
        
    print(f"\n\n✨ FACTORY RUN COMPLETE")
    print(f"   Generated: {generated}")
    print(f"   Skipped (Existing): {skipped_existing}")

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