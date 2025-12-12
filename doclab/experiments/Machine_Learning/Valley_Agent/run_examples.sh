#!/bin/bash
# Sand RL Incremental - Quick Start Examples

echo "==============================================="
echo "Sand RL Incremental - Bomb-Proof RL Training"
echo "==============================================="
echo ""
echo "This script provides examples for training Ant and Humanoid."
echo "Features:"
echo "  - Incremental checkpointing (resume from any point)"
echo "  - Pirouette metrics tracked during execution"
echo "  - No memory accumulation (can run indefinitely)"
echo "  - Safe Ctrl+C (always resumes cleanly)"
echo ""

# Make the Python script executable
chmod +x sand_rl_incremental.py

echo "EXAMPLE 1: Train Humanoid-v5 (default)"
echo "---------------------------------------"
echo "python sand_rl_incremental.py \\"
echo "  --env Humanoid-v5 \\"
echo "  --episodes 10000 \\"
echo "  --output-dir ./humanoid_run1 \\"
echo "  --checkpoint-interval 50"
echo ""

echo "EXAMPLE 2: Train Ant-v5 (faster, good for testing)"
echo "---------------------------------------------------"
echo "python sand_rl_incremental.py \\"
echo "  --env Ant-v5 \\"
echo "  --episodes 5000 \\"
echo "  --output-dir ./ant_run1 \\"
echo "  --checkpoint-interval 25"
echo ""

echo "EXAMPLE 3: Resume interrupted training"
echo "---------------------------------------"
echo "Just rerun the same command! The script auto-detects checkpoints."
echo "python sand_rl_incremental.py --env Humanoid-v5 --output-dir ./humanoid_run1"
echo ""

echo "EXAMPLE 4: Disable sand metrics for pure RL"
echo "--------------------------------------------"
echo "python sand_rl_incremental.py \\"
echo "  --env Humanoid-v5 \\"
echo "  --no-sand-metrics"
echo ""

echo "EXAMPLE 5: Larger network for Humanoid"
echo "---------------------------------------"
echo "python sand_rl_incremental.py \\"
echo "  --env Humanoid-v5 \\"
echo "  --hidden-dim 512 \\"
echo "  --lr 1e-4"
echo ""

echo "OUTPUT STRUCTURE:"
echo "-----------------"
echo "./output_dir/"
echo "  ├── episode_metrics.csv          # Episode-by-episode metrics"
echo "  └── checkpoints/"
echo "      ├── training_state.json      # Resume info"
echo "      ├── checkpoint_ep50.pt       # Checkpoint at episode 50"
echo "      ├── checkpoint_ep100.pt      # Checkpoint at episode 100"
echo "      └── ..."
echo ""

echo "KEY METRICS IN episode_metrics.csv:"
echo "------------------------------------"
echo "  - total_reward: Episode return"
echo "  - steps: Episode length"
echo "  - avg_DR: Average Dark Residue (Pirouette)"
echo "  - avg_S: Average Surprise (Pirouette)"
echo "  - avg_Gamma: Average temporal pressure (Pirouette)"
echo "  - coherence_proxy: Estimated coherence (1 - avg_DR)"
echo "  - valley_count_estimate: Estimated valley crossings in episode"
echo ""

echo "TIPS:"
echo "-----"
echo "1. Start with Ant-v5 to test (simpler, faster)"
echo "2. Humanoid-v5 needs ~1000-2000 episodes to show progress"
echo "3. Watch avg_reward in the console output"
echo "4. Check episode_metrics.csv for detailed analysis"
echo "5. Press Ctrl+C anytime - it's safe!"
echo "6. Valley counts indicate potential coherence phase transitions"
echo ""

echo "QUICK TEST RUN:"
echo "---------------"
read -p "Run a quick test with Ant-v5 (100 episodes)? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "Starting test run..."
    python sand_rl_incremental.py \
        --env Ant-v5 \
        --episodes 100 \
        --output-dir ./test_run \
        --checkpoint-interval 25
fi
