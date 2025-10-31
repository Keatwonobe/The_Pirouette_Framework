#!/usr/bin/env python3
"""
gexf_cluster_frontier.py
(see earlier description in assistant message)
"""
import argparse, math, json
from pathlib import Path
import numpy as np
import pandas as pd
import networkx as nx

def _get_pos(n_attr):
    if 'x' in n_attr and 'y' in n_attr:
        try: return float(n_attr['x']), float(n_attr['y'])
        except: pass
    viz = n_attr.get('viz')
    if isinstance(viz, dict):
        pos = viz.get('position') or {}
        if 'x' in pos and 'y' in pos:
            return float(pos['x']), float(pos['y'])
        if 'x' in viz and 'y' in viz:
            return float(viz['x']), float(viz['y'])
    return None

def _cluster_attr(n_attr):
    for key in ['modularity_class', 'Modularity Class', 'community', 'cluster']:
        if key in n_attr:
            try:
                return int(n_attr[key])
            except Exception:
                try:
                    return int(float(n_attr[key]))
                except Exception:
                    return str(n_attr[key])
    return -1

def _edge_weight(G, u, v):
    data = G[u][v]
    w = 1.0
    if isinstance(data, dict):
        w = data.get('weight', 1.0)
    try:
        return float(w)
    except Exception:
        return 1.0

def analyze_graph(gexf_path: Path, out_dir: Path, theta_deg: float = 30.0, r_z: float = 2.0, ext_thresh: float = 0.4, min_tip_percent: float = 0.02):
    out_dir.mkdir(parents=True, exist_ok=True)
    G = nx.read_gexf(gexf_path)
    nodes = list(G.nodes())

    rows = []
    for n in nodes:
        a = G.nodes[n]
        pos = _get_pos(a)
        c = _cluster_attr(a)
        rows.append({'node': n, 'cluster': c, 'pos': pos})
    df = pd.DataFrame(rows)

    cluster_groups = {c: set(sub['node'].tolist()) for c, sub in df.groupby('cluster')}

    degrees = {}
    strengths = {}
    ext_ratio = {}

    for n in nodes:
        nbrs = G[n]
        total_w = 0.0
        ext_w = 0.0
        c = df.loc[df['node']==n, 'cluster'].values[0]
        inC = cluster_groups.get(c, set())
        for m in nbrs:
            w = _edge_weight(G, n, m)
            total_w += w
            if m not in inC:
                ext_w += w
        degrees[n] = len(nbrs)
        strengths[n] = total_w
        ext_ratio[n] = (ext_w / total_w) if total_w > 0 else 0.0

    df['degree'] = df['node'].map(degrees)
    df['strength'] = df['node'].map(strengths)
    df['ext_ratio'] = df['node'].map(ext_ratio)

    xs, ys = [], []
    for p in df['pos']:
        if p is None:
            xs.append(np.nan); ys.append(np.nan)
        else:
            xs.append(float(p[0])); ys.append(float(p[1]))
    df['x'] = xs; df['y'] = ys
    df['r'] = np.nan
    df['dx'] = np.nan
    df['dy'] = np.nan

    tips = []
    cone_rows = []
    cluster_rows = []
    theta = math.radians(theta_deg)

    for c, sub in df.groupby('cluster'):
        sub = sub.copy()
        if sub['x'].isna().all():
            cluster_rows.append({'cluster': c, 'size': len(sub), 'avg_strength': sub['strength'].mean(), 'centroid_x': np.nan, 'centroid_y': np.nan, 'num_tips': 0})
            continue

        cx = float(sub['x'].mean()); cy = float(sub['y'].mean())
        sub['dx'] = sub['x'] - cx; sub['dy'] = sub['y'] - cy
        sub['r'] = np.sqrt(sub['dx']**2 + sub['dy']**2)

        r_mu, r_sigma = sub['r'].mean(), sub['r'].std(ddof=0)
        r_cut = r_mu + r_z * (r_sigma if np.isfinite(r_sigma) else 0.0)
        r_floor = np.quantile(sub['r'], max(0.0, 1.0 - min_tip_percent))
        r_thr = max(r_cut, r_floor)

        cand = sub[(sub['r'] >= r_thr) & (sub['ext_ratio'] >= ext_thresh)].copy()

        for _, row in cand.iterrows():
            rv = np.array([row['dx'], row['dy']], dtype=float)
            norm = np.linalg.norm(rv) + 1e-12
            dirv = rv / norm
            tips.append({'node': row['node'], 'cluster': c, 'r': float(row['r']), 'ext_ratio': float(row['ext_ratio']), 'dir_x': float(dirv[0]), 'dir_y': float(dirv[1]), 'centroid_x': cx, 'centroid_y': cy})

        for _, t in cand.iterrows():
            tip_node = t['node']
            tip_r = float(t['r'])
            tip_dir = np.array([t['dx'], t['dy']], dtype=float)
            tip_dir = tip_dir / (np.linalg.norm(tip_dir) + 1e-12)

            for _, m in sub.iterrows():
                if m['node'] == tip_node: 
                    continue
                mv = np.array([m['dx'], m['dy']], dtype=float)
                m_r = np.linalg.norm(mv)
                if m_r == 0.0: 
                    continue
                cosang = float(np.dot(mv, tip_dir) / (m_r + 1e-12))
                aligned = (cosang / (np.linalg.norm(tip_dir) + 1e-12)) >= math.cos(theta)
                proj = float(np.dot(mv, tip_dir))
                if aligned and (proj <= tip_r):
                    angle = float(math.degrees(math.acos(max(-1.0, min(1.0, cosang/(np.linalg.norm(tip_dir)+1e-12))))))
                    cone_rows.append({'tip': tip_node, 'member': m['node'], 'cluster': c, 'angle_deg': angle, 'proj': proj, 'member_r': m_r})

        cluster_rows.append({'cluster': c, 'size': len(sub), 'avg_strength': sub['strength'].mean(), 'centroid_x': cx, 'centroid_y': cy, 'num_tips': int(len(cand))})

    out_dir.mkdir(parents=True, exist_ok=True)
    df_out = df.copy()
    tip_nodes = {t['node'] for t in tips}
    df_out['is_tip'] = df_out['node'].isin(tip_nodes).astype(int)
    df_out[['node','cluster','degree','strength','ext_ratio','x','y','r','is_tip']].to_csv(out_dir/'nodes_with_metrics.csv', index=False)
    pd.DataFrame(tips).to_csv(out_dir/'tips.csv', index=False)
    pd.DataFrame(cone_rows).to_csv(out_dir/'cones.csv', index=False)
    pd.DataFrame(cluster_rows).to_csv(out_dir/'clusters.csv', index=False)

    # annotate gexf
    G2 = G.copy()
    for _, r in df_out.iterrows():
        n = r['node']
        if n in G2.nodes:
            G2.nodes[n]['is_tip'] = int(r['is_tip'])
            try: G2.nodes[n]['ext_ratio'] = float(r['ext_ratio'])
            except: pass
            try: G2.nodes[n]['r'] = float(r['r']) if not np.isnan(r['r']) else 0.0
            except: pass
    nx.write_gexf(G2, out_dir/'annotated.gexf')

    summary = {"n_nodes": int(len(df_out)), "n_edges": int(G.number_of_edges()), "n_clusters": int(df_out['cluster'].nunique()), "n_tips": int(len(tips)), "theta_deg": float(theta_deg), "r_z": float(r_z), "ext_thresh": float(ext_thresh), "min_tip_percent": float(min_tip_percent)}
    with open(out_dir/'summary.json','w') as f:
        json.dump(summary, f, indent=2)
    print("Wrote outputs to", str(out_dir))

def main():
    import argparse
    ap = argparse.ArgumentParser()
    ap.add_argument("--gexf", required=True)
    ap.add_argument("--out", default="./cluster_out")
    ap.add_argument("--theta_deg", type=float, default=30.0)
    ap.add_argument("--r_z", type=float, default=2.0)
    ap.add_argument("--ext_thresh", type=float, default=0.4)
    ap.add_argument("--min_tip_percent", type=float, default=0.02)
    args = ap.parse_args()
    analyze_graph(Path(args.gexf), Path(args.out), args.theta_deg, args.r_z, args.ext_thresh, args.min_tip_percent)

if __name__ == "__main__":
    main()
