"""
DDE-Pirouette: SQL Manager (The Foundation)
-------------------------------------------
Migrates the file-based DDE architecture to a robust SQL Database.
This enables scaling to 100k+ articles without RAM bottlenecks.

Schema:
- articles: The core registry (ID, Title, Metadata)
- signatures: The semantic index (Keyword, Weight)
- atlas: The physical coordinates (X, Y)

Usage:
    python dde_sql_manager.py --init
    python dde_sql_manager.py --migrate
"""

import sqlite3
import json
import os
import argparse
import sys

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DB_FILE = "dde_knowledge_base.db"

# JSON Source Files (for migration)
CHK_FILE = "dde_wiki_checkpoint_25000.json" # Or your latest checkpoint
IDX_FILE = "wiki_resonance_index.json"
MAP_FILE = "wiki_atlas_map.json"

def get_db():
    return sqlite3.connect(DB_FILE)

def init_db():
    print(f"🏗️  Initializing Database: {DB_FILE}...")
    conn = get_db()
    cur = conn.cursor()
    
    # 1. Articles Table (The Manifest)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS articles (
        id TEXT PRIMARY KEY,
        title TEXT,
        checksum TEXT,
        entropy REAL,
        created_at TEXT
    )
    """)
    
    # 2. Signatures Table (The Resonance Index)
    # Normalized for fast joins
    cur.execute("""
    CREATE TABLE IF NOT EXISTS signatures (
        article_id TEXT,
        keyword TEXT,
        weight REAL,
        FOREIGN KEY(article_id) REFERENCES articles(id)
    )
    """)
    # Index for speed
    cur.execute("CREATE INDEX IF NOT EXISTS idx_keyword ON signatures (keyword)")
    cur.execute("CREATE INDEX IF NOT EXISTS idx_sig_article ON signatures (article_id)")

    # 3. Atlas Table (The Map)
    cur.execute("""
    CREATE TABLE IF NOT EXISTS atlas (
        article_id TEXT PRIMARY KEY,
        x INTEGER,
        y INTEGER,
        FOREIGN KEY(article_id) REFERENCES articles(id)
    )
    """)
    
    conn.commit()
    conn.close()
    print("   ✅ Database Schema Created.")

def migrate_data():
    if not os.path.exists(DB_FILE):
        init_db()
        
    conn = get_db()
    cur = conn.cursor()
    
    print("📦 MIGRATION STARTED")
    
    # 1. Migrate Manifest (Articles)
    if os.path.exists(CHK_FILE):
        print(f"   📖 Reading Manifest: {CHK_FILE}...")
        with open(CHK_FILE, 'r') as f:
            data = json.load(f)
            if "data" in data: 
                manifest = data["data"]["m"]
            else:
                manifest = data.get("manifest", {})
        
        print(f"      Inserting {len(manifest)} articles...")
        batch = []
        for mid, info in manifest.items():
            # Extract clean title
            title = mid.replace("WIKI-", "")
            checksum = info.get("cs", "")
            entropy = 0.0 # Placeholder if missing
            
            # Get stats safely
            stats = info.get("st", {})
            if isinstance(stats, dict):
                entropy = stats.get("en", 0.0)
            
            batch.append((mid, title, checksum, entropy, "migrated"))
            
        cur.executemany("INSERT OR IGNORE INTO articles VALUES (?, ?, ?, ?, ?)", batch)
        conn.commit()
        print("      ✅ Articles migrated.")

    # 2. Migrate Index (Signatures)
    if os.path.exists(IDX_FILE):
        print(f"   📖 Reading Index: {IDX_FILE}...")
        with open(IDX_FILE, 'r') as f:
            index_data = json.load(f)["index"]
            
        print(f"      Inserting signatures (this may take a while)...")
        batch = []
        for mid, keywords in index_data.items():
            # We assume equal weight for now, or could use rank
            for i, kw in enumerate(keywords):
                # Weight = importance (higher is better). 
                # List is sorted, so we can use rank.
                weight = 1.0 / (i + 1) 
                batch.append((mid, kw, weight))
        
        # Use chunks to avoid memory overload
        chunk_size = 10000
        for i in range(0, len(batch), chunk_size):
            cur.executemany("INSERT OR IGNORE INTO signatures VALUES (?, ?, ?)", batch[i:i+chunk_size])
            sys.stdout.write(f"\r      Processed {i}/{len(batch)} keywords...")
            
        conn.commit()
        print("\n      ✅ Signatures migrated.")

    # 3. Migrate Map (Atlas)
    if os.path.exists(MAP_FILE):
        print(f"   📖 Reading Map: {MAP_FILE}...")
        with open(MAP_FILE, 'r') as f:
            map_data = json.load(f)["tiles"]
            
        print(f"      Inserting coordinates...")
        batch = []
        for filename, info in map_data.items():
            # ID needs to match article_id (WIKI-Title)
            # Filename is "WIKI-Title.png" or just "Title.png"
            # Info has 'id' which is the clean title
            clean_id = info['id']
            mid = f"WIKI-{clean_id}"
            
            batch.append((mid, info['x'], info['y']))
            
        cur.executemany("INSERT OR IGNORE INTO atlas VALUES (?, ?, ?)", batch)
        conn.commit()
        print("      ✅ Atlas migrated.")

    conn.close()
    print("\n🎉 MIGRATION COMPLETE. Your DDE is now SQL-Powered.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--init", action="store_true", help="Create DB Schema")
    parser.add_argument("--migrate", action="store_true", help="Import JSON data")
    args = parser.parse_args()
    
    if args.init:
        init_db()
    elif args.migrate:
        migrate_data()
    else:
        print("Usage: python dde_sql_manager.py --init OR --migrate")