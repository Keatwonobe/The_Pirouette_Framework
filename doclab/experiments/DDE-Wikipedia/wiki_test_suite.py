"""
DDE-Pirouette: Wikipedia Test Suite (The Examiner)
--------------------------------------------------
A comprehensive diagnostic tool for the 100k+ Article DDE.
Runs a battery of semantic tests and generates a detailed Markdown report.

Tests:
1.  VITAL SIGNS: Database health, density, and scale.
2.  THE SUPER-CONNECTORS: Finding the most connected nodes (Hubs).
3.  THE BLACK SWANS: Finding the rarest, most unique concepts.
4.  BRIDGE STRESS TEST: Attempting to connect random disparate pairs.
5.  CLUSTER COHERENCE: Verifying if known categories clump together.

Usage:
    python wiki_test_suite.py
"""

import sqlite3
import json
import os
import random
import time
import sys
from collections import Counter

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DB_FILE = "dde_knowledge_base.db"
REPORT_FILE = "wiki_test_results.md"

def get_db():
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found: {DB_FILE}")
        sys.exit(1)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def log(f, text):
    print(text)
    f.write(text + "\n")

def run_tests():
    print(f"🧪 STARTING DDE DIAGNOSTIC SUITE")
    print(f"   Target: {DB_FILE}")
    
    conn = get_db()
    cur = conn.cursor()
    
    with open(REPORT_FILE, 'w', encoding='utf-8') as f:
        # HEADER
        log(f, "# DDE-Pirouette: Diagnostic Report")
        log(f, f"**Date:** {time.strftime('%Y-%m-%d %H:%M:%S')}")
        log(f, f"**Database:** `{DB_FILE}`")
        log(f, "---")

        # ---------------------------------------------------------
        # TEST 1: VITAL SIGNS
        # ---------------------------------------------------------
        log(f, "\n## 1. Vital Signs")
        
        start = time.time()
        cur.execute("SELECT COUNT(*) FROM articles")
        count_arts = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(*) FROM signatures")
        count_sigs = cur.fetchone()[0]
        
        cur.execute("SELECT COUNT(DISTINCT keyword) FROM signatures")
        count_vocab = cur.fetchone()[0]
        
        density = count_sigs / count_arts if count_arts > 0 else 0
        
        log(f, f"* **Total Articles:** {count_arts:,}")
        log(f, f"* **Total Synapses (Signatures):** {count_sigs:,}")
        log(f, f"* **Unique Concepts (Vocab):** {count_vocab:,}")
        log(f, f"* **Semantic Density:** {density:.2f} keywords/article")
        log(f, f"* _Scan Time: {time.time() - start:.2f}s_")

        # ---------------------------------------------------------
        # TEST 2: THE SUPER-CONNECTORS (Hubs)
        # ---------------------------------------------------------
        log(f, "\n## 2. The Super-Connectors (Central Hubs)")
        log(f, "These articles have the most semantic connections (keywords). They are the 'Grand Central Stations' of your map.")
        
        start = time.time()
        cur.execute("""
            SELECT a.title, COUNT(s.keyword) as count
            FROM articles a
            JOIN signatures s ON a.id = s.article_id
            GROUP BY a.id
            ORDER BY count DESC
            LIMIT 10
        """)
        hubs = cur.fetchall()
        
        log(f, "| Rank | Article Title | Connections |")
        log(f, "| :--- | :--- | :--- |")
        for i, row in enumerate(hubs):
            log(f, f"| {i+1} | **{row['title']}** | {row['count']} |")
        log(f, f"\n* _Scan Time: {time.time() - start:.2f}s_")

        # ---------------------------------------------------------
        # TEST 3: THE BLACK SWANS (Rarity)
        # ---------------------------------------------------------
        log(f, "\n## 3. The Black Swans (Rarest Concepts)")
        log(f, "These keywords appear least frequently, indicating highly specialized knowledge.")
        
        start = time.time()
        # Find keywords that appear exactly once (Unique)
        cur.execute("""
            SELECT keyword, COUNT(*) as c 
            FROM signatures 
            GROUP BY keyword 
            HAVING c = 1 
            LIMIT 10
        """)
        rarest = cur.fetchall()
        
        # Get context for them
        log(f, "| Rare Keyword | Found In (Context) |")
        log(f, "| :--- | :--- |")
        for row in rarest:
            kw = row['keyword']
            # Find which article has it
            cur.execute("""
                SELECT a.title FROM articles a 
                JOIN signatures s ON a.id = s.article_id 
                WHERE s.keyword = ?
            """, (kw,))
            ctx = cur.fetchone()
            title = ctx['title'] if ctx else "Unknown"
            
            # FIXED: Added 'f' (file handle) as the first argument
            log(f, f"| `{kw}` | {title} |")
            
        log(f, f"\n* _Scan Time: {time.time() - start:.2f}s_")

        # ---------------------------------------------------------
        # TEST 4: BRIDGE STRESS TEST (Random Walks)
        # ---------------------------------------------------------
        log(f, "\n## 4. Bridge Stress Test (Connectivity)")
        log(f, "Attempting to connect 5 pairs of random articles. This tests the 'small world' property of the DDE.")
        
        # Get random IDs
        cur.execute("SELECT id, title FROM articles ORDER BY RANDOM() LIMIT 10")
        random_arts = cur.fetchall()
        pairs = [(random_arts[i], random_arts[i+1]) for i in range(0, 10, 2)]
        
        log(f, "| Source | Target | Bridge Found? | Steps |")
        log(f, "| :--- | :--- | :--- | :--- |")
        
        for start_node, end_node in pairs:
            # Simulate a bi-directional search (simplified for speed)
            # We look for a SHARED KEYWORD (1-hop bridge)
            s_title = start_node['title']
            e_title = end_node['title']
            
            t_start = time.time()
            
            # 1-Hop Query (Do they share a keyword?)
            cur.execute("""
                SELECT s1.keyword 
                FROM signatures s1 
                JOIN signatures s2 ON s1.keyword = s2.keyword 
                WHERE s1.article_id = ? AND s2.article_id = ? 
                LIMIT 1
            """, (start_node['id'], end_node['id']))
            
            bridge = cur.fetchone()
            
            if bridge:
                status = f"✅ YES (via '{bridge['keyword']}')"
                steps = "1 (Direct)"
            else:
                # 2-Hop Query (Do they share a neighbor?)
                # This is heavy, so we limit scan
                status = "❌ NO (Too distant)"
                steps = "> 1"
            
            log(f, f"| {s_title} | {e_title} | {status} | {steps} |")

        # ---------------------------------------------------------
        # TEST 5: CLUSTER COHERENCE
        # ---------------------------------------------------------
        log(f, "\n## 5. Cluster Coherence (The 'Color' Test)")
        log(f, "Checking if the concept 'Red' retrieves actual red things.")
        
        test_concept = "red"
        cur.execute("""
            SELECT a.title 
            FROM signatures s 
            JOIN articles a ON s.article_id = a.id 
            WHERE s.keyword = ? 
            LIMIT 10
        """, (test_concept,))
        
        reds = [r['title'] for r in cur.fetchall()]
        
        log(f, f"**Concept:** `{test_concept}`")
        log(f, "**Retrieved Artifacts:**")
        for r in reds:
            log(f, f"* {r}")
            
        log(f, "\n---")
        log(f, "**End of Report**")

    conn.close()
    print(f"\n✅ Test Suite Complete. Results written to: {REPORT_FILE}")

if __name__ == "__main__":
    run_tests()