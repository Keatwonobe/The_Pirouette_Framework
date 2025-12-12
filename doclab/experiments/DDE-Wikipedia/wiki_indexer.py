"""
DDE-Pirouette: Wikipedia SQL Indexer v4.2 (The Brain Builder - Fixed)
---------------------------------------------------------------------
Scans the SQL database for unindexed articles (Dark Matter) 
and computes their semantic signatures.
- Fixed: Removed all 'getprevious' calls (Standard Lib Safe).
- Fixed: Root clearing memory management.
- Direct SQL streaming.
- ThreadPool execution.

Usage:
    python wiki_indexer_sql.py --workers 6
"""

import sqlite3
import argparse
import sys
import os
import time
import re
import xml.etree.ElementTree as ET
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
import threading
import gc

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DB_FILE = "dde_knowledge_base.db"

def get_db():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

# ---------------------------------------------------------------------------
# LOGIC
# ---------------------------------------------------------------------------
def clean_wiki_text_fast(text):
    if not text: return ""
    # Fast regex cleanup
    try:
        text = re.sub(r'\[\[File:.*?\]\]', '', text)
        text = re.sub(r'<ref.*?>.*?</ref>', '', text, flags=re.DOTALL)
        text = re.sub(r'\{\{.*?\}\}', '', text, flags=re.DOTALL)
        text = re.sub(r'[^a-zA-Z\s]', ' ', text) 
        return text.lower()
    except:
        return ""

def compute_signature(text, top_k=50):
    if not text: return []
    words = text.split()
    # Heuristic: longer words carry more meaning
    meaningful_words = [w for w in words if len(w) > 4]
    counts = Counter(meaningful_words)
    # Rank by (Length * Frequency) -> "Heavy" words
    ranked = sorted(counts.items(), key=lambda x: (len(x[0]) * x[1]), reverse=True)
    return [w for w, count in ranked[:top_k]]

def get_target_ids():
    conn = get_db()
    cur = conn.cursor()
    print("   🔍 Identifying unindexed targets...")
    
    # We want articles that exist in 'articles' but NOT in 'signatures'
    cur.execute("""
        SELECT id FROM articles 
        EXCEPT 
        SELECT article_id FROM signatures
    """)
    
    rows = cur.fetchall()
    target_ids = set(row[0] for row in rows)
    conn.close()
    print(f"   🎯 Found {len(target_ids)} unindexed articles.")
    return target_ids

# ---------------------------------------------------------------------------
# MAIN PROCESS
# ---------------------------------------------------------------------------
class SQLStreamingIndexer:
    def __init__(self, xml_path, workers=4):
        self.xml_path = xml_path
        self.workers = workers
        self.conn = get_db()
        self.cur = self.conn.cursor()
        self.processed = 0
        self.signatures_added = 0
        
    def process_article(self, data):
        """Thread worker to compute signatures."""
        mid, raw_text = data
        
        clean = clean_wiki_text_fast(raw_text)
        keywords = compute_signature(clean)
        
        # Prepare batch rows: (article_id, keyword, weight)
        rows = []
        for i, kw in enumerate(keywords):
            weight = 1.0 / (i + 1)
            rows.append((mid, kw, weight))
            
        return rows

    def run(self):
        # Load Targets
        self.targets = get_target_ids()
        
        if not self.targets:
            print("   ✨ All articles are already indexed! Nothing to do.")
            return

        print(f"🚀 STARTING INDEXER (Workers: {self.workers})")
        print("   Streaming XML to find targets...")
        
        executor = ThreadPoolExecutor(max_workers=self.workers)
        futures = []
        batch_buffer = []
        
        # Standard Library Iterparse Setup
        # We need 'start' to get the root, and 'end' to process elements
        context = ET.iterparse(self.xml_path, events=('start', 'end'))
        context = iter(context)
        event, root = next(context) # Capture the root element
        
        start_time = time.time()
        
        try:
            for event, elem in context:
                if event == 'end':
                    # Manual Tag Strip (Namespace removal)
                    tag = elem.tag.split('}')[-1]
                    
                    if tag == "page":
                        try:
                            title = "Unknown"
                            raw_text = ""
                            
                            # Fast manual traversal
                            for child in elem:
                                ctag = child.tag.split('}')[-1]
                                if ctag == "title": title = child.text
                                elif ctag == "revision":
                                    for rev in child:
                                        if rev.tag.split('}')[-1] == "text": 
                                            raw_text = rev.text
                            
                            if title:
                                # Re-derive ID
                                safe_title = "".join([c if c.isalnum() else "_" for c in title])
                                mid = f"WIKI-{safe_title[:50]}"
                                
                                # IS THIS A TARGET?
                                if mid in self.targets:
                                    if raw_text:
                                        future = executor.submit(self.process_article, (mid, raw_text))
                                        futures.append(future)
                                        
                                        # Optimization: Remove found target from set to speed up lookups?
                                        # No, let's keep it simple. Set lookup is fast.
                        
                        except Exception as e:
                            pass # Don't crash on XML weirdness
                        
                        # --- MEMORY MANAGEMENT (The Fix) ---
                        # Clear the element we just finished
                        elem.clear()
                        # Clear the root's children reference
                        root.clear()

                        # Flush Futures Buffer
                        if len(futures) >= 500:
                            for f in futures:
                                try:
                                    rows = f.result()
                                    if rows:
                                        batch_buffer.extend(rows)
                                        self.processed += 1
                                        self.signatures_added += len(rows)
                                except: pass
                            
                            # Write to DB
                            if batch_buffer:
                                try:
                                    self.cur.executemany("INSERT OR IGNORE INTO signatures VALUES (?, ?, ?)", batch_buffer)
                                    self.conn.commit()
                                    
                                    elapsed = time.time() - start_time
                                    rate = self.processed / elapsed if elapsed > 0 else 0
                                    sys.stdout.write(f"\r   ⚡ Indexed: {self.processed} articles | {self.signatures_added} sigs | {rate:.1f}/s")
                                except Exception as e:
                                    print(f"\n   ❌ DB Write Error: {e}")
                                
                                batch_buffer = []
                                gc.collect() # Keep RAM tidy
                            
                            futures = []

        except Exception as e:
            print(f"\n❌ ERROR: {e}")
        finally:
            print("\n   (Flushing remaining...)")
            for f in futures:
                try:
                    rows = f.result()
                    if rows: batch_buffer.extend(rows)
                except: pass
            
            if batch_buffer:
                self.cur.executemany("INSERT OR IGNORE INTO signatures VALUES (?, ?, ?)", batch_buffer)
                self.conn.commit()
                
            executor.shutdown()
            self.conn.close()
            print("\n🏁 INDEXING COMPLETE.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_file", type=str)
    parser.add_argument("--workers", type=int, default=6)
    args = parser.parse_args()
    
    if not os.path.exists(args.xml_file):
        print("❌ XML not found.")
        sys.exit(1)
        
    indexer = SQLStreamingIndexer(args.xml_file, workers=args.workers)
    indexer.run()