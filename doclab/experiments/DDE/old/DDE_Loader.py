"""
DDE-Pirouette Folder Synchronizer v1.0
"Slurp up" a folder of markdown files into a single, annealed DDE database.
"""

import sys
import numpy as np
from pathlib import Path
from DDE_Pirouette import DDEPirouette, PirouetteMetadata, FAISS_AVAILABLE

def sync_folder_to_dde(folder_path_str: str):
    """
    Ingests all .md files from a target folder into a new DDE instance.
    """
    
    folder_path = Path(folder_path_str)
    if not folder_path.is_dir():
        print(f"❌ Error: Path '{folder_path_str}' is not a valid directory.")
        return

    # Use the folder's name as the domain and the db label
    domain_name = folder_path.name.upper()
    db_label = folder_path.name
    
    print("=" * 70)
    print(f"🌱 INITIALIZING NEW DDE INSTANCE for: {db_label}")
    print(f"   Domain: {domain_name}")
    print("=" * 70)
    
    # 1. Initialize a fresh DDE instance
    dde = DDEPirouette(patch_size=8)
    
    md_files = list(folder_path.glob('*.md'))
    if not md_files:
        print(f"⚠️  No markdown files found in '{folder_path_str}'.")
        return

    print(f"Found {len(md_files)} modules to ingest...")
    
    all_vectors = []
    
    # --------------------------------------------------------------------
    # STAGE 1: INGESTION & VECTORIZATION
    # --------------------------------------------------------------------
    print("\n" + "─" * 70)
    print("STAGE 1: INGESTING MODULES")
    print("─" * 70)
    
    for md_path in md_files:
        try:
            # Use filename (without extension) as module_id
            module_id = md_path.stem.upper()
            
            with open(md_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 2. Ingest the module
            # We use the folder name for the domain
            meta = PirouetteMetadata(
                module_id=module_id,
                domain=domain_name,
                gamma_profile="medium",  # Default for text-based modules
                parents=[], # We can't infer this from a flat folder
                temporal_adherence=0.8 # Default adherence
            )
            
            img = dde.ingest_pirouette_module(
                content,
                module_id=module_id,
                domain=domain_name, # Pass domain to ingestor
                gamma_profile="medium",
                parents=[]
            )
            
            # 3. Calculate and store Dark Residue
            # Using a small, default energy cost for ingestion
            residue = dde.dark_residue(module_id, energy_kwh=0.0001)
            dde.manifest[module_id]["dark_residue"] = residue
            
            # 4. Vectorize (if FAISS is available)
            if FAISS_AVAILABLE:
                vectors = dde.vectorize(img, module_id)
                all_vectors.append(vectors)
            
            print(f"  ✅ Ingested: {md_path.name} (Module: {module_id})")
        
        except Exception as e:
            print(f"  ❌ FAILED to ingest {md_path.name}: {e}")
            
    # --------------------------------------------------------------------
    # STAGE 2: INDEXING & ANNEALING
    # --------------------------------------------------------------------
    if FAISS_AVAILABLE and all_vectors:
        print("\n" + "─" * 70)
        print(f"STAGE 2: BUILDING COHERENCE ({len(all_vectors)} modules)")
        print("─" * 70)
        
        # Concatenate all vectors from all files into one big matrix
        all_vectors_np = np.concatenate(all_vectors, axis=0)
        
        # Build a single index for the *entire* database
        # Use a small cluster count, good for a single folder's worth of data
        n_clusters = max(1, min(16, len(all_vectors) // 4)) 
        
        dde.build_index(use_gpu=False, n_clusters=n_clusters)
        dde.add_to_index(all_vectors_np)
        
        print("\n" + "─" * 70)
        print("STAGE 3: AUTOPOIETIC ANNEALING")
        print("─" * 70)
        print("Running evolution to heal the new database...")
        
        # Run a few cycles to "settle" the new database
        dde.run_evolution(n_cycles=3, budget_per_cycle=0.01)

    elif FAISS_AVAILABLE:
        print("\n⚠️  No vectors were generated. Skipping indexing.")
    else:
        print("\n⚠️  FAISS not available. Skipping indexing and evolution.")

    # --------------------------------------------------------------------
    # STAGE 4: SAVING THE DATABASE
    # --------------------------------------------------------------------
    print("\n" + "─" * 70)
    print("STAGE 4: SAVING DATABASE MANIFEST")
    print("─" * 70)
    
    # Save the final "balled up" database
    output_filename = f"dde_db_{db_label}.json"
    dde.save_manifest(output_filename)
    
    print(f"\n🎉 SUCCESS! 🎉")
    print(f"Successfully packed {len(md_files)} modules into:")
    print(f"{output_filename}")
    print("=" * 70)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("="*70)
        print("DDE Folder Synchronizer")
        print("="*70)
        print("Usage: python DDE_Loader.py <path_to_your_folder>")
        print("\nExample: python DDE_Loader.py ./my_pirouette_modules")
        print("="*70)
        sys.exit(1)
        
    target_folder = sys.argv[1]
    sync_folder_to_dde(target_folder)