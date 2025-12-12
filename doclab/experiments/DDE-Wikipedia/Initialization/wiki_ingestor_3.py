"""
DDE-Pirouette: Wikipedia Stream Ingester (The Hawk-Eye Adapter) v2.2
- Added: Smart Resume (Loads latest checkpoint to avoid restarting)
- Added: Fast-Forwarding (Skips known IDs in the stream)
- Fixed: Removed lxml dependency
- Fixed: Standard Library Memory Safety
"""

import sys
import os
import argparse
import re
import xml.etree.ElementTree as ET
import time
import hashlib
import glob
import numpy as np
from datetime import datetime
from pathlib import Path

# Import the Core Framework
try:
    from DDE_Pirouette import DDEPirouette, PirouetteMetadata
except ImportError:
    print("❌ CRITICAL: DDE_Pirouette.py not found. Cannot start.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# HELPER: Fast Cleanup
# ---------------------------------------------------------------------------
def clean_wiki_text(text):
    if not text: return ""
    if text.lower().startswith("#redirect"): return None
    
    # Fast/Rough regex cleanup
    text = re.sub(r'\[\[File:.*?\]\]', '', text)
    text = re.sub(r'\[\[Image:.*?\]\]', '', text)
    text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
    text = re.sub(r'<ref.*?>', '', text)
    text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
    text = re.sub(r'=+.*?=+', '', text)
    text = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]+)\]\]', r'\1', text)
    text = re.sub(r'<.*?>', '', text)
    return re.sub(r'\s+', ' ', text).strip()

def local_tag(tag):
    """Strips the {http://...} namespace from XML tags."""
    if not tag: return ""
    return tag.split('}', 1)[-1] if '}' in tag else tag

# ---------------------------------------------------------------------------
# CLASS: Virtual DDE (v7.3 Compliant + Resume Logic)
# ---------------------------------------------------------------------------
class WikiPirouette(DDEPirouette):
    def __init__(self, domain="WIKIPEDIA_OMNIBUS", **kwargs):
        super().__init__(**kwargs)
        self.domain_scope = domain

    def generate_module_id(self, title):
        """Deterministic ID generation."""
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        return f"WIKI-{safe_title[:50]}"

    def is_ingested(self, title):
        """Fast check if we already have this article."""
        mid = self.generate_module_id(title)
        return mid in self.manifest

    def _calculate_entropy(self, text):
        if not text: return 0.0
        prob = [text.count(c) / len(text) for c in set(text)]
        return -sum(p * np.log2(p) for p in prob)

    def ingest_virtual_article(self, title, raw_text, source_id):
        # 1. Clean
        clean_text = clean_wiki_text(raw_text)
        if not clean_text or len(clean_text) < 300:
            return False

        # 2. Generate ID
        module_id = self.generate_module_id(title)

        # 3. Calculate Metrics
        entropy = self._calculate_entropy(clean_text)
        
        # 4. Create v7.3 Metadata
        meta = PirouetteMetadata(
            module_id=module_id,
            domain=self.domain_scope,
            status="ingested",
            coherence_target=0.5 + (0.1 * entropy),
            engrams=[f"wiki_id:{source_id}", f"entropy:{entropy:.2f}"],
            created_at=datetime.utcnow().isoformat()
        )

        # 5. Update Manifest
        self.pirouette_registry[module_id] = meta
        self.manifest[module_id] = {
            'shape': [len(clean_text), 1],
            'stats': {'text_length': len(clean_text), 'entropy': entropy},
            'pirouette': meta.to_dict(),
            'checksum': hashlib.sha256(clean_text.encode()).hexdigest()
        }

        # 6. Update Vocab (Simple Tokenizer)
        tokens = set(word for word in clean_text.split() if len(word) > 3)
        for token in tokens:
            if token not in self.vocab:
                code = self._hash_token(token)
                self.vocab[token] = code
                self.reverse_vocab[code] = token
        
        return True

# ---------------------------------------------------------------------------
# RESUME LOGIC
# ---------------------------------------------------------------------------
def find_latest_checkpoint():
    """Finds the latest checkpoint file based on the ingestion count in filename."""
    checkpoints = glob.glob("dde_wiki_checkpoint_*.json")
    if not checkpoints:
        return None
    
    # Extract numbers: "dde_wiki_checkpoint_1000.json" -> 1000
    def extract_num(fname):
        try:
            return int(re.search(r'checkpoint_(\d+)', fname).group(1))
        except:
            return 0
            
    latest = max(checkpoints, key=extract_num)
    return latest

# ---------------------------------------------------------------------------
# THE STREAMER
# ---------------------------------------------------------------------------
def stream_wikipedia(xml_path, dde, limit=None, save_interval=1000):
    print(f"🦅 HAWK-EYE INGEST STARTING: {xml_path}")
    
    # Load Resume Data
    already_ingested_count = len(dde.manifest)
    if already_ingested_count > 0:
        print(f"⏩ RESUMING: Manifest already contains {already_ingested_count} articles.")
        print(f"   (Stream will fast-forward until new content is found)")
    
    context = ET.iterparse(xml_path, events=('start', 'end'))
    context = iter(context)
    event, root = next(context)
    
    count = 0
    ingested_new = 0
    skipped = 0
    start_time = time.time()
    
    print("🔎 Stream open. Scanning...")

    for event, elem in context:
        if event == 'end':
            tag = local_tag(elem.tag)
            
            if tag == "page":
                count += 1
                
                # 1. Fast Title Extraction (Namespace Safe)
                title = "Unknown"
                title_node = None
                # Optimization: Try finding title directly first
                for child in elem:
                    if local_tag(child.tag) == "title":
                        title = child.text
                        break
                
                # 2. FAST-FORWARD CHECK
                # If we already have this title in the manifest, skip everything else
                if dde.is_ingested(title):
                    skipped += 1
                    if skipped % 1000 == 0:
                        sys.stdout.write(f"\r⏩ Fast-Forwarding... Skipped {skipped} (Known: {title[:20]})")
                    
                    elem.clear()
                    root.clear()
                    continue

                # 3. It's new! Extract the rest
                page_id = "0"
                raw_text = ""
                try:
                    for child in elem:
                        c_tag = local_tag(child.tag)
                        if c_tag == "id":
                            page_id = child.text
                        elif c_tag == "revision":
                            for rev_child in child:
                                if local_tag(rev_child.tag) == "text":
                                    raw_text = rev_child.text
                except:
                    pass

                # 4. Ingest
                if raw_text:
                    success = dde.ingest_virtual_article(title, raw_text, page_id)
                    if success:
                        ingested_new += 1
                        current_total = already_ingested_count + ingested_new
                        
                        if ingested_new % 10 == 0:
                            sys.stdout.write(f"\r✅ Ingested: {current_total} (+{ingested_new}) | {str(title)[:30]:<30}")
                        
                        # Checkpoints
                        if current_total % save_interval == 0:
                            chk_name = f"dde_wiki_checkpoint_{current_total}.json"
                            print(f"\n💾 Checkpoint reached! Saving to {chk_name}...")
                            dde.save_manifest_minified(chk_name)
                            print("   ...saved. Resuming.")

                        # Limit
                        if limit and current_total >= limit:
                            print(f"\n🛑 Limit of {limit} reached.")
                            elem.clear()
                            break

                # Memory Clear
                elem.clear()
                root.clear()

    total_time = time.time() - start_time
    print(f"\n\n--- STREAM COMPLETE ---")
    print(f"Scanned Total: {count} pages")
    print(f"Skipped (Known): {skipped}")
    print(f"Ingested New: {ingested_new}")
    print(f"Total Database: {len(dde.manifest)}")
    print(f"Time: {total_time:.2f}s")

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_file", type=str)
    parser.add_argument("--limit", type=int, default=None)
    args = parser.parse_args()
    
    if not os.path.exists(args.xml_file):
        print(f"❌ File not found: {args.xml_file}")
        sys.exit(1)
        
    wiki_dde = WikiPirouette(domain="WIKIPEDIA_OMNIBUS")
    
    # --- SMART LOAD ---
    latest_chk = find_latest_checkpoint()
    if latest_chk:
        print(f"📂 Found checkpoint: {latest_chk}")
        try:
            wiki_dde.load_manifest(latest_chk)
        except Exception as e:
            print(f"⚠️  Warning: Could not load checkpoint ({e}). Starting fresh.")
    # ------------------
    
    try:
        stream_wikipedia(args.xml_file, wiki_dde, limit=args.limit)
    except KeyboardInterrupt:
        print("\n⚠️  User Interrupt! Saving what we have so far...")
    except Exception as e:
        print(f"\n❌ CRITICAL CRASH: {e}")
    
    # Final Save
    print("💾 Saving final manifest...")
    wiki_dde.save_manifest_minified("dde_wiki_manifest_final.json")
    print("✅ Done.")