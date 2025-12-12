"""
DDE-Pirouette: Wikipedia SQL Ingestor v4.1 (The Crusher - Fixed)
----------------------------------------------------------------
High-performance, multi-threaded XML -> SQL ingestion pipeline.
- Fixed: Removed lxml dependency (getprevious crash).
- Fixed: Standard Library Memory Safety (Root Clearing).
- Direct SQL streaming (No JSON intermediates).
- ThreadPool execution for parallel processing.

Usage:
    python wiki_ingestor_sql.py "wiki.xml" --workers 4
"""

import sys
import os
import argparse
import re
import xml.etree.ElementTree as ET
import time
import hashlib
import sqlite3
import threading
import queue
import signal
import gc
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime

# Import Core
try:
    from DDE_Pirouette import DDEPirouette, PirouetteMetadata
except ImportError:
    print("❌ CRITICAL: DDE_Pirouette.py not found.")
    sys.exit(1)

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DB_FILE = "dde_knowledge_base.db"
BATCH_SIZE = 1000 # Commit to DB every N articles

# Global flags for threading
SHUTDOWN_FLAG = False

def get_db():
    return sqlite3.connect(DB_FILE, check_same_thread=False)

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
    except:
        return None

def local_tag(tag):
    if not tag: return ""
    return tag.split('}', 1)[-1] if '}' in tag else tag

# ---------------------------------------------------------------------------
# WORKER: The Processing Unit
# ---------------------------------------------------------------------------
def process_article(data):
    """
    Worker function. Takes raw XML data, cleans it, and returns a DB row.
    """
    title, raw_text, page_id = data
    
    # 1. Clean
    clean_text = clean_wiki_text(raw_text)
    if not clean_text or len(clean_text) < 300:
        return None # Skip junk
        
    # 2. ID Generation
    safe_title = "".join([c if c.isalnum() else "_" for c in title])
    mid = f"WIKI-{safe_title[:50]}"
    
    # 3. Stats
    import math
    entropy = 0.0
    if clean_text:
        prob = [clean_text.count(c) / len(clean_text) for c in set(clean_text)]
        entropy = -sum(p * math.log2(p) for p in prob)
        
    checksum = hashlib.sha256(clean_text.encode()).hexdigest()
    
    return (mid, title, checksum, entropy, datetime.utcnow().isoformat())

# ---------------------------------------------------------------------------
# MAIN INGESTOR CLASS
# ---------------------------------------------------------------------------
class SQLIngestor:
    def __init__(self, xml_path, workers=4):
        self.xml_path = xml_path
        self.workers = workers
        self.conn = get_db()
        self.cur = self.conn.cursor()
        self.processed_count = 0
        self.skipped_count = 0
        
        # Prepare DB
        self.cur.execute("""
        CREATE TABLE IF NOT EXISTS articles (
            id TEXT PRIMARY KEY,
            title TEXT,
            checksum TEXT,
            entropy REAL,
            created_at TEXT
        )
        """)
        self.conn.commit()
        
        # Check existing
        self.cur.execute("SELECT COUNT(*) FROM articles")
        self.existing_count = self.cur.fetchone()[0]
        print(f"   📚 Database already contains {self.existing_count} articles.")

    def run(self):
        global SHUTDOWN_FLAG
        print(f"🚀 STARTING INGESTION (Workers: {self.workers})")
        
        start_time = time.time()
        batch_buffer = []
        
        # Thread Pool
        executor = ThreadPoolExecutor(max_workers=self.workers)
        futures = []
        
        # XML Streamer - Use 'start' event to catch root for clearing
        context = ET.iterparse(self.xml_path, events=('start', 'end'))
        context = iter(context)
        event, root = next(context) # Get root element
        
        try:
            for event, elem in context:
                if SHUTDOWN_FLAG: break
                
                if event == 'end':
                    if local_tag(elem.tag) == "page":
                        # Extract Data (Main Thread)
                        title = "Unknown"
                        page_id = "0"
                        raw_text = ""
                        try:
                            for child in elem:
                                tag = local_tag(child.tag)
                                if tag == "title": title = child.text
                                elif tag == "id": page_id = child.text
                                elif tag == "revision":
                                    for rev in child:
                                        if local_tag(rev.tag) == "text": raw_text = rev.text
                        except: pass

                        if raw_text:
                            # Submit to Worker
                            future = executor.submit(process_article, (title, raw_text, page_id))
                            futures.append(future)
                        
                        # Process Futures Buffer
                        if len(futures) >= BATCH_SIZE:
                            for f in futures:
                                try:
                                    result = f.result()
                                    if result:
                                        batch_buffer.append(result)
                                        self.processed_count += 1
                                    else:
                                        self.skipped_count += 1
                                except Exception as e:
                                    print(f"   ⚠️ Worker Error: {e}")
                            
                            # Write Batch
                            if batch_buffer:
                                try:
                                    self.cur.executemany(
                                        "INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)", 
                                        batch_buffer
                                    )
                                    self.conn.commit()
                                    
                                    elapsed = time.time() - start_time
                                    rate = self.processed_count / elapsed if elapsed > 0 else 0
                                    print(f"   ⚡ Ingested: {self.processed_count} (+{self.existing_count}) | Rate: {rate:.1f}/s | Skipped: {self.skipped_count}")
                                except Exception as e:
                                    print(f"   ❌ DB Write Error: {e}")

                                batch_buffer = []
                                gc.collect() # Keep RAM clean
                            
                            futures = []

                        # MEMORY CLEARING (Standard Lib Safe)
                        elem.clear()
                        root.clear()

        except Exception as e:
            print(f"\n❌ STREAM ERROR: {e}")
        finally:
            # Flush remaining
            print("   (Flushing remaining threads...)")
            for f in futures:
                try:
                    res = f.result()
                    if res: batch_buffer.append(res)
                except: pass
            
            if batch_buffer:
                try:
                    self.cur.executemany("INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)", batch_buffer)
                    self.conn.commit()
                except: pass
            
            executor.shutdown(wait=False)
            self.conn.close()
            print("\n🏁 INGESTION STOPPED.")
            print(f"   Total New: {self.processed_count}")

# ---------------------------------------------------------------------------
# SIGNAL HANDLER
# ---------------------------------------------------------------------------
def signal_handler(sig, frame):
    global SHUTDOWN_FLAG
    print("\n\n🛑 CTRL+C DETECTED! Stopping gracefully...")
    SHUTDOWN_FLAG = True

# ---------------------------------------------------------------------------
# MAIN
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    
    parser = argparse.ArgumentParser()
    parser.add_argument("xml_file", type=str)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    
    if not os.path.exists(args.xml_file):
        print("❌ File not found.")
        sys.exit(1)
        
    ingestor = SQLIngestor(args.xml_file, workers=args.workers)
    ingestor.run()