"""
DDE-Pirouette: Wikipedia Network Tool (The Nexus)
-------------------------------------------------
A multi-point triangulation engine.
Given N concepts, it finds the 'Semantic Centroid' (The Nexus)
that connects them all, and traces the 'Key' keywords that bridge them.

Usage:
    python wiki_network_tool.py "Physics,Philosophy,Art"
"""

import sqlite3
import argparse
import sys
import os
import heapq

# ---------------------------------------------------------------------------
# CONFIG
# ---------------------------------------------------------------------------
DB_FILE = "dde_knowledge_base.db"

def get_db():
    if not os.path.exists(DB_FILE):
        print(f"❌ Database not found: {DB_FILE}")
        sys.exit(1)
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def get_signatures(conn, concept):
    """Finds articles matching the concept."""
    cursor = conn.cursor()
    cursor.execute("""
        SELECT article_id, weight 
        FROM signatures 
        WHERE keyword = ? 
        ORDER BY weight DESC 
        LIMIT 50
    """, (concept.lower(),))
    return cursor.fetchall()

def find_nexus(concepts):
    conn = get_db()
    print(f"🕸️  NETWORK TOOL ONLINE")
    print(f"   Triangulating: {concepts}")
    
    input_terms = [c.strip().lower() for c in concepts.split(',')]
    if len(input_terms) < 2:
        print("   ❌ Need at least 2 concepts to triangulate.")
        return

    # 1. Gather Candidate Nodes
    # We want nodes that resonate with ALL inputs, or the maximum subset.
    
    # Candidate Score Map: {article_id: {term: score}}
    candidates = {}
    
    print("   📡 Scanning signal fields...")
    for term in input_terms:
        hits = get_signatures(conn, term)
        if not hits:
            print(f"   ⚠️ Term '{term}' has no direct resonance.")
            # Try finding neighbors (1-hop) if direct fails? 
            # For now, we skip to keep it fast.
            continue
            
        for row in hits:
            mid = row['article_id']
            if mid not in candidates: candidates[mid] = {}
            candidates[mid][term] = row['weight']

    # 2. Score Candidates (The Centroid)
    # Score = (Count of Terms Matched) * (Sum of Weights)
    ranked_nexus = []
    
    for mid, matches in candidates.items():
        match_count = len(matches)
        total_weight = sum(matches.values())
        
        # Bonus for hitting multiple distinct inputs
        synergy_bonus = match_count ** 2 
        final_score = total_weight * synergy_bonus
        
        ranked_nexus.append((mid, final_score, matches))
        
    ranked_nexus.sort(key=lambda x: x[1], reverse=True)
    
    # 3. The Reveal
    top_nexus = ranked_nexus[:5]
    
    if not top_nexus:
        print("   🌑 No semantic intersection found.")
        return
        
    print(f"\n✨ FOUND {len(top_nexus)} NEXUS POINTS:")
    
    for i, (mid, score, matches) in enumerate(top_nexus):
        # Get Title
        cur = conn.cursor()
        cur.execute("SELECT title FROM articles WHERE id = ?", (mid,))
        res = cur.fetchone()
        title = res['title'] if res else mid
        
        print(f"\n🏆 RANK {i+1}: {title} (Score: {score:.2f})")
        print(f"   The Bridge is built on:")
        
        for term in input_terms:
            if term in matches:
                print(f"   ✅ {term.title():<15} -> (Direct Resonance)")
            else:
                # If not direct, find the "Key" (1-hop)
                # Find a keyword that connects [Term] -> [Nexus]
                key = find_indirect_key(conn, term, mid)
                if key:
                    print(f"   🔗 {term.title():<15} -> via '{key}'")
                else:
                    print(f"   ❌ {term.title():<15} -> (Disconnected)")

    conn.close()

def find_indirect_key(conn, term, target_mid):
    """Finds a shared keyword between 'Term' articles and 'Target' article."""
    # 1. Get keywords of Target
    cur = conn.cursor()
    cur.execute("SELECT keyword FROM signatures WHERE article_id = ?", (target_mid,))
    target_keywords = set(row['keyword'] for row in cur.fetchall())
    
    # 2. Get articles for Term
    cur.execute("SELECT article_id FROM signatures WHERE keyword = ? LIMIT 10", (term,))
    term_articles = [r['article_id'] for r in cur.fetchall()]
    
    # 3. Find Intersection
    for term_mid in term_articles:
        cur.execute("SELECT keyword FROM signatures WHERE article_id = ?", (term_mid,))
        term_keywords = set(row['keyword'] for row in cur.fetchall())
        
        overlap = target_keywords.intersection(term_keywords)
        if overlap:
            return list(overlap)[0] # Return the first bridge word
            
    return None

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("concepts", type=str, help="Comma separated concepts")
    args = parser.parse_args()
    
    find_nexus(args.concepts)