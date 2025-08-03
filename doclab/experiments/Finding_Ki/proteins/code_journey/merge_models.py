import argparse
import pickle
import os
from collections import defaultdict, Counter
from tqdm import tqdm
from loguru import logger as log

# Class definition must match the one used for training
class ProteinProphet:
    """Container for n-gram counts. Can be merged."""
    def __init__(self, n=3):
        self.n = n
        self.counts = defaultdict(Counter)
        self.context_totals = Counter()
        self.vocabulary = set()
        self.V = 0

def merge_prophets(main_prophet, other_prophet):
    """Merges 'other_prophet' into 'main_prophet'."""
    main_prophet.vocabulary.update(other_prophet.vocabulary)
    main_prophet.context_totals.update(other_prophet.context_totals)
    for ctx, counter in other_prophet.counts.items():
        main_prophet.counts[ctx].update(counter)

def main():
    p = argparse.ArgumentParser(description="Merges partial ProteinProphet models into a final one.")
    p.add_argument("temp_dir", help="Directory containing the partial model files.")
    p.add_argument("final_model", help="Path to save the final, merged model file (e.g., prophet.pkl).")
    args = p.parse_args()

    partial_model_files = [os.path.join(args.temp_dir, f) for f in os.listdir(args.temp_dir) if f.endswith('.pkl')]
    if not partial_model_files:
        log.error(f"No partial model files found in '{args.temp_dir}'.")
        return

    log.info(f"Found {len(partial_model_files)} partial models to merge.")
    
    # Assume ngram size from the first model
    try:
        with open(partial_model_files[0], 'rb') as f:
            first_model = pickle.load(f)
        ngram_size = first_model.n
    except Exception as e:
        log.error(f"Could not load the first model to determine n-gram size. Error: {e}")
        return

    final_prophet = ProteinProphet(n=ngram_size)
    log.info(f"Initialized final model with n={final_prophet.n}.")

    for model_path in tqdm(partial_model_files, desc="Merging Models"):
        with open(model_path, 'rb') as f:
            partial_prophet = pickle.load(f)
        merge_prophets(final_prophet, partial_prophet)

    # Finalize the vocabulary size after merging is complete
    final_prophet.V = len(final_prophet.vocabulary)
    log.info(f"Final merged vocabulary size (V): {final_prophet.V}")

    log.info(f"Saving final merged model to {args.final_model}...")
    with open(args.final_model, 'wb') as f:
        pickle.dump(final_prophet, f)
    
    log.success("Model merging complete!")

if __name__ == "__main__":
    main()