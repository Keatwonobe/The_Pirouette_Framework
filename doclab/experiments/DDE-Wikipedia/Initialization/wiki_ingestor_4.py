"""
DDE-Pirouette: Wikipedia Stream Ingester (The Hawk-Eye Adapter) v3.1
- Fixed: Deep Sanitization (Converts Numpy/Sets to native types)
- Fixed: Buffered Write (Prevents partial file corruption)
- Fixed: Non-Blocking Save (Ingest continues even if save fails)
"""

import sys
import os
import argparse
import re
import xml.etree.ElementTree as ET
import time
import hashlib
import glob
import json
import numpy as np
from datetime import datetime
import builtins
from numbers import Integral, Real


# Import the Core Framework
try:
    from DDE_Pirouette import DDEPirouette, PirouetteMetadata
except ImportError:
    print("❌ CRITICAL: DDE_Pirouette.py not found. Cannot start.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# HELPER: Robust Wiki Cleaner
# ---------------------------------------------------------------------------
def clean_wiki_text(text):
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
    except (re.error, Exception):
        return None

def local_tag(tag):
    if not tag: return ""
    return tag.split('}', 1)[-1] if '}' in tag else tag

# ---------------------------------------------------------------------------
# LOCAL MINIFICATION & SANITIZATION
# ---------------------------------------------------------------------------
WIKI_KEY_MAP = {
    "version": "v", "created": "ct", "manifest": "m", "vocab": "vo", 
    "reverse_vocab": "rv", "shape": "s", "stats": "st", "checksum": "cs",
    "pirouette": "pi", "module_id": "id", "domain": "d", "status": "ss",
    "coherence_target": "ctt", "engrams": "e", "created_at": "cat",
    "text_length": "tl", "entropy": "en"
}

def safe_sanitize(obj):
    """
    Recursively converts Numpy/Sets/Tuples/Callables/etc to JSON-safe native types.
    This should *never* raise – on failure we fall back to str(obj).
    """
    try:
        # Dict: remap keys using WIKI_KEY_MAP (only if key is a string) + recurse values
        if isinstance(obj, dict):
            out = {}
            for k, v in obj.items():
                if isinstance(k, str):
                    mapped_k = WIKI_KEY_MAP.get(k, k)
                else:
                    mapped_k = k  # don't touch non-string keys
                out[mapped_k] = safe_sanitize(v)
            return out

        # Lists / tuples / sets: recurse each element
        if isinstance(obj, (list, tuple, set)):
            return [safe_sanitize(x) for x in obj]

        # Numpy scalar (int, float, bool, etc.)
        if isinstance(obj, np.generic):
            return obj.item()

        # Numpy arrays
        if isinstance(obj, np.ndarray):
            return [safe_sanitize(x) for x in obj.tolist()]

        # Bytes → utf-8 string (best effort)
        if isinstance(obj, (bytes, bytearray)):
            return obj.decode("utf-8", errors="replace")

        # Callables (functions/methods): turn into readable markers so JSON doesn't choke
        if callable(obj):
            name = getattr(obj, "__name__", type(obj).__name__)
            return f"<callable:{name}>"

        # Everything else: assume it's already JSON-safe or handled by json.dumps(default=str)
        return obj

    except Exception as e:
        # Absolute last resort: represent as string so we *never* crash during sanitization
        return f"<sanitize_error:{type(obj).__name__}:{e}>"



# ---------------------------------------------------------------------------
# CLASS: Virtual DDE (Bulletproof)
# ---------------------------------------------------------------------------
class WikiPirouette(DDEPirouette):
    def __init__(self, domain="WIKIPEDIA_OMNIBUS", **kwargs):
        super().__init__(**kwargs)
        self.domain_scope = domain

    def generate_module_id(self, title):
        safe_title = "".join([c if c.isalnum() else "_" for c in title])
        return f"WIKI-{safe_title[:50]}"

    def is_ingested(self, title):
        mid = self.generate_module_id(title)
        return mid in self.manifest

    def _calculate_entropy(self, text):
        if not text: return 0.0
        # Numpy returns float64, which we must handle in sanitization
        prob = [text.count(c) / len(text) for c in set(text)]
        return -sum(p * np.log2(p) for p in prob)

    def ingest_virtual_article(self, title, raw_text, source_id):
        clean_text = clean_wiki_text(raw_text)
        if not clean_text or len(clean_text) < 300:
            return False

        module_id = self.generate_module_id(title)
        entropy = self._calculate_entropy(clean_text)
        
        meta = PirouetteMetadata(
            module_id=module_id,
            domain=self.domain_scope,
            status="ingested",
            coherence_target=0.5 + (0.1 * float(entropy)), # Explicit cast just in case
            engrams=[f"wiki_id:{source_id}", f"entropy:{entropy:.2f}"],
            created_at=datetime.utcnow().isoformat()
        )

        self.pirouette_registry[module_id] = meta
        self.manifest[module_id] = {
            'shape': [len(clean_text), 1],
            'stats': {'text_length': len(clean_text), 'entropy': entropy},
            'pirouette': meta.to_dict(),
            'checksum': hashlib.sha256(clean_text.encode()).hexdigest()
        }

        # Vocab update
        tokens = set(word for word in clean_text.split() if len(word) > 3)
        for token in tokens:
            if token not in self.vocab:
                code = self._hash_token(token)
                self.vocab[token] = code
                self.reverse_vocab[code] = token
        
        return True

    # --- LOCAL OVERRIDE: BULLETPROOF SAVE ---
    def save_manifest_minified(self, path: str):
        """Atomic + Sanitized Save. Never crashes the stream."""
        temp_path = path + ".tmp"

        try:
            # 1. Prepare Data (keep this as-is semantically)
            data_to_save = {
                'version': '7.3-wiki-bulletproof',
                'created': datetime.utcnow().isoformat(),
                'manifest': self.manifest,
                'vocab': self.vocab,
                'reverse_vocab': self.reverse_vocab
            }

            # 2. Deep Sanitize (Fixes Numpy/Set issues)
            clean_data = safe_sanitize(data_to_save)
            output_json = {"meta_map": WIKI_KEY_MAP, "data": clean_data}

            # 3. Buffer to String (validate before touching disk)
            # NOTE: no default=str anymore – we *expect* everything to be primitive.
            json_str = json.dumps(output_json, separators=(',', ':'))

            # 4. Atomic write to temp file
            with open(temp_path, 'w', encoding='utf-8') as f:
                f.write(json_str)
                f.flush()
                os.fsync(f.fileno())

            # 5. Atomic Rename (Windows-friendly)
            if os.path.exists(path):
                os.remove(path)
            os.rename(temp_path, path)
            print(f"   ✅ Saved atomically to {path}")

        except Exception as e:
            # CRITICAL: Print error but DO NOT RAISE. Keep ingest running.
            print(f"   ❌ SAVE ERROR (Ignored): {type(e).__name__}: {e}")
            if os.path.exists(temp_path):
                try:
                    os.remove(temp_path)
                except:
                    pass


# ---------------------------------------------------------------------------
# CHECKPOINT FINDER
# ---------------------------------------------------------------------------
def find_latest_checkpoint():
    checkpoints = glob.glob("dde_wiki_checkpoint_*.json")
    if not checkpoints: return None
    
    def extract_num(fname):
        try:
            return int(re.search(r'checkpoint_(\d+)', fname).group(1))
        except: return 0
            
    return max(checkpoints, key=extract_num)

# ---------------------------------------------------------------------------
# STREAMER
# ---------------------------------------------------------------------------
def stream_wikipedia(xml_path, dde, limit=None, save_interval=5000):
    print(f"🦅 HAWK-EYE INGEST STARTING: {xml_path}")
    
    # Defensive read of manifest size – manifest might be a weird type after rehydrate
    try:
        manifest_obj = getattr(dde, "manifest", {})
        if isinstance(manifest_obj, (dict, list, tuple, set)):
            already_ingested_count = len(manifest_obj)
        else:
            # If it's some custom/container type, try len() but swallow errors
            try:
                already_ingested_count = len(manifest_obj)
            except Exception:
                already_ingested_count = 0
    except Exception:
        already_ingested_count = 0

    if already_ingested_count > 0:
        print(f"⏩ RESUMING: Manifest has {already_ingested_count} articles.")

    
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
                
                # Extract Title
                title = "Unknown"
                for child in elem:
                    if local_tag(child.tag) == "title":
                        title = child.text
                        break
                
                # Check Resume/Skip
                if dde.is_ingested(title):
                    skipped += 1
                    if skipped % 5000 == 0:
                        sys.stdout.write(f"\r⏩ Skipped {skipped} known articles...")
                    elem.clear()
                    root.clear()
                    continue

                # Parse Full
                page_id = "0"
                raw_text = ""
                try:
                    for child in elem:
                        c_tag = local_tag(child.tag)
                        if c_tag == "id": page_id = child.text
                        elif c_tag == "revision":
                            for rev in child:
                                if local_tag(rev.tag) == "text": raw_text = rev.text
                except: pass

                # Ingest
                if raw_text:
                    success = dde.ingest_virtual_article(title, raw_text, page_id)
                    if success:
                        ingested_new += 1
                        current_total = already_ingested_count + ingested_new
                        
                        if ingested_new % 10 == 0:
                            sys.stdout.write(f"\r✅ Ingested: {current_total} (+{ingested_new}) | {str(title)[:30]:<30}")
                        
                        # Checkpoint
                        if current_total % save_interval == 0:
                            chk_name = f"dde_wiki_checkpoint_{current_total}.json"
                            print(f"\n💾 Checkpoint reached! Saving...")
                            dde.save_manifest_minified(chk_name)
                            print("   ...Resuming.")

                        if limit and current_total >= limit:
                            print(f"\n🛑 Limit of {limit} reached.")
                            elem.clear()
                            break

                elem.clear()
                root.clear()

    total_time = time.time() - start_time
    print(f"\n\n--- STREAM COMPLETE ---")
    print(f"New Ingested: {ingested_new}")

    # Do NOT let this line ever crash the whole run
    try:
        manifest_obj = getattr(dde, "manifest", {})
        if isinstance(manifest_obj, (dict, list, tuple, set)):
            total_db = len(manifest_obj)
        else:
            try:
                total_db = len(manifest_obj)
            except Exception as e:
                total_db = f"unknown (len() failed: {e})"
    except Exception as e:
        total_db = f"unknown (manifest access failed: {e})"

    print(f"Total Database: {total_db}")
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
    
    # Resume
    latest_chk = find_latest_checkpoint()
    if latest_chk:
        print(f"📂 Loading checkpoint: {latest_chk}")
        try:
            wiki_dde.load_manifest(latest_chk)
        except Exception as e:
            print(f"⚠️  Load failed ({e}). Starting fresh.")
    
    try:
        stream_wikipedia(args.xml_file, wiki_dde, limit=args.limit)
    except KeyboardInterrupt:
        print("\n⚠️  User Interrupt! Saving...")
    except Exception as e:
        print(f"\n❌ CRITICAL CRASH: {e}")
    
    print("💾 Saving final manifest...")
    wiki_dde.save_manifest_minified("dde_wiki_manifest_final.json")
    print("✅ Done.")