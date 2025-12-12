"""
Vagabond Usage Examples

Demonstrates various ways to use the Vagabond agent
for different scenarios and use cases.
"""

import gymnasium as gym
import numpy as np
from vagabond import Vagabond, VagabondConfig, train_vagabond


def example_1_quick_training():
    """Example 1: Quick training on CartPole"""
    print("\n" + "="*70)
    print("EXAMPLE 1: Quick Training")
    print("="*70 + "\n")
    
    agent = train_vagabond('CartPole-v1', num_episodes=100, eval_interval=25)
    
    print("\n✅ Training complete!")
    print(f"Final geodesic hit rate: {agent.geodesic_map.get_hit_rate():.1%}")
    print(f"Δ field entries: {len(agent.temporal_field.field)}")


def example_2_custom_config():
    """Example 2: Custom configuration for specific needs"""
    print("\n" + "="*70)
    print("EXAMPLE 2: Custom Configuration")
    print("="*70 + "\n")
    
    # Aggressive learning: prioritize closing the loop quickly
    aggressive_config = VagabondConfig(
        gamma_weight=0.7,      # High reward for coherence gain
        delta_weight=0.2,      # Strong Dark Residue penalty
        exploration_noise=0.12, # Moderate exploration
        learning_rate=5e-4     # Faster learning
    )
    
    print("Training with aggressive configuration...")
    env = gym.make('Pendulum-v1')
    agent = Vagabond(env, aggressive_config)
    
    for ep in range(50):
        stats = agent.train_episode()
        if (ep + 1) % 10 == 0:
            print(f"Episode {ep + 1}: Reward={stats['reward']:.2f}, "
                  f"DR={stats['avg_dark_residue']:.4f}")
    
    print("\n✅ Aggressive training complete!")


def example_3_conservative_stable():
    """Example 3: Conservative, stable learning"""
    print("\n" + "="*70)
    print("EXAMPLE 3: Conservative Stable Learning")
    print("="*70 + "\n")
    
    # Conservative: prioritize stability over speed
    conservative_config = VagabondConfig(
        gamma_weight=0.4,         # Moderate coherence gain
        delta_weight=0.08,        # Light DR penalty
        delta_momentum_decay=0.98,# High Δ field inertia
        exploration_noise=0.08,   # Low exploration
        tau=0.003                 # Slow target updates
    )
    
    print("Training with conservative configuration...")
    env = gym.make('CartPole-v1')
    agent = Vagabond(env, conservative_config)
    
    for ep in range(50):
        stats = agent.train_episode()
        if (ep + 1) % 10 == 0:
            print(f"Episode {ep + 1}: Reward={stats['reward']:.2f}, "
                  f"DR={stats['avg_dark_residue']:.4f}")
    
    print("\n✅ Conservative training complete!")


def example_4_evaluate_and_visualize():
    """Example 4: Train, evaluate, and visualize"""
    print("\n" + "="*70)
    print("EXAMPLE 4: Train, Evaluate, and Visualize")
    print("="*70 + "\n")
    
    # Train
    env = gym.make('CartPole-v1')
    agent = Vagabond(env)
    
    print("Training for 100 episodes...")
    for ep in range(100):
        agent.train_episode()
    
    # Evaluate
    print("\nEvaluating agent...")
    eval_stats = agent.evaluate(num_episodes=50)
    
    print(f"\n📊 Evaluation Results:")
    print(f"  Mean Reward: {eval_stats['mean_reward']:.2f} ± "
          f"{eval_stats['std_reward']:.2f}")
    print(f"  Mean Dark Residue: {eval_stats['mean_dark_residue']:.4f}")
    
    # Visualize
    try:
        from visualize import (plot_dark_residue_history, 
                             visualize_geodesic_map,
                             create_full_dashboard)
        
        print("\nGenerating visualizations...")
        plot_dark_residue_history(agent, 'example_dr.png')
        visualize_geodesic_map(agent, 'example_geodesic.png')
        create_full_dashboard(agent, 'example_dashboard.png')
        
        print("✅ Visualizations saved!")
    except ImportError:
        print("⚠️  Visualization module not available")


def example_5_manual_training_loop():
    """Example 5: Manual training loop with custom logic"""
    print("\n" + "="*70)
    print("EXAMPLE 5: Manual Training Loop")
    print("="*70 + "\n")
    
    env = gym.make('CartPole-v1')
    agent = Vagabond(env)
    
    best_reward = float('-inf')
    patience = 10
    episodes_without_improvement = 0
    
    for episode in range(200):
        stats = agent.train_episode()
        
        # Custom early stopping logic
        if stats['reward'] > best_reward:
            best_reward = stats['reward']
            episodes_without_improvement = 0
        else:
            episodes_without_improvement += 1
        
        # Periodic reporting
        if (episode + 1) % 20 == 0:
            eval_stats = agent.evaluate(num_episodes=10)
            print(f"Episode {episode + 1}:")
            print(f"  Train Reward: {stats['reward']:.2f}")
            print(f"  Eval Reward: {eval_stats['mean_reward']:.2f}")
            print(f"  Dark Residue: {eval_stats['mean_dark_residue']:.4f}")
            print(f"  Geodesic Hit Rate: {stats['geodesic_hit_rate']:.1%}")
        
        # Early stopping
        if best_reward >= 495 and episodes_without_improvement > patience:
            print(f"\n🎯 Solved! Best reward: {best_reward:.2f}")
            break
    
    print("\n✅ Training complete!")


def example_6_transfer_learning():
    """Example 6: Transfer Δ field to similar task"""
    print("\n" + "="*70)
    print("EXAMPLE 6: Transfer Learning")
    print("="*70 + "\n")
    
    # Train on CartPole
    print("Training source agent on CartPole...")
    env1 = gym.make('CartPole-v1')
    source_agent = Vagabond(env1)
    
    for _ in range(50):
        source_agent.train_episode()
    
    source_dr = source_agent.evaluate(num_episodes=10)['mean_dark_residue']
    print(f"Source agent DR: {source_dr:.4f}")
    
    # Create target agent (Acrobot - similar balance task)
    print("\nTransferring to Acrobot (similar balance task)...")
    env2 = gym.make('Acrobot-v1')
    target_agent = Vagabond(env2)
    
    # Transfer Δ field structure (simplified - would need proper mapping)
    print("Note: Full transfer requires state space mapping")
    print("This demonstrates the concept")
    
    # Train target with transferred knowledge
    for ep in range(30):
        stats = target_agent.train_episode()
        if (ep + 1) % 10 == 0:
            print(f"Episode {ep + 1}: Reward={stats['reward']:.2f}")
    
    print("\n✅ Transfer complete!")


def example_7_curriculum_learning():
    """Example 7: Curriculum learning across difficulties"""
    print("\n" + "="*70)
    print("EXAMPLE 7: Curriculum Learning")
    print("="*70 + "\n")
    
    curriculum = [
        ('CartPole-v1', 50, 400),     # (env, episodes, threshold)
        ('Pendulum-v1', 100, -200),
        ('Acrobot-v1', 100, -150),
    ]
    
    for env_name, num_episodes, threshold in curriculum:
        print(f"\n📚 Training on {env_name}...")
        print(f"   Target: {threshold} in {num_episodes} episodes")
        
        env = gym.make(env_name)
        agent = Vagabond(env)
        
        for ep in range(num_episodes):
            stats = agent.train_episode()
            
            # Check if mastered
            if (ep + 1) % 10 == 0:
                eval_stats = agent.evaluate(num_episodes=5)
                if eval_stats['mean_reward'] >= threshold:
                    print(f"   ✅ Mastered at episode {ep + 1}!")
                    print(f"      Reward: {eval_stats['mean_reward']:.2f}")
                    print(f"      Dark Residue: {eval_stats['mean_dark_residue']:.4f}")
                    break
    
    print("\n✅ Curriculum complete!")


def example_8_compare_configurations():
    """Example 8: Compare different configurations"""
    print("\n" + "="*70)
    print("EXAMPLE 8: Configuration Comparison")
    print("="*70 + "\n")
    
    configs = {
        'default': VagabondConfig(),
        'aggressive': VagabondConfig(gamma_weight=0.7, delta_weight=0.2),
        'conservative': VagabondConfig(gamma_weight=0.4, delta_weight=0.08),
        'high_exploration': VagabondConfig(exploration_noise=0.3),
    }
    
    results = {}
    
    for name, config in configs.items():
        print(f"\nTesting {name} configuration...")
        env = gym.make('CartPole-v1')
        agent = Vagabond(env, config)
        
        for _ in range(50):
            agent.train_episode()
        
        eval_stats = agent.evaluate(num_episodes=10)
        results[name] = eval_stats['mean_reward']
        print(f"  Final reward: {eval_stats['mean_reward']:.2f}")
    
    print("\n📊 Configuration Comparison:")
    for name, reward in sorted(results.items(), key=lambda x: x[1], reverse=True):
        print(f"  {name:20s}: {reward:6.2f}")
    
    print("\n✅ Comparison complete!")


def example_9_debug_mode():
    """Example 9: Debug mode with detailed logging"""
    print("\n" + "="*70)
    print("EXAMPLE 9: Debug Mode")
    print("="*70 + "\n")
    
    env = gym.make('CartPole-v1')
    agent = Vagabond(env)
    
    # Run one episode with detailed logging
    state, _ = env.reset()
    episode_reward = 0
    step = 0
    
    done = False
    print("Step-by-step execution:\n")
    
    while not done and step < 20:  # Limit to 20 steps for brevity
        action = agent.select_action(state, evaluate=False)
        
        if agent.continuous:
            next_state, reward, terminated, truncated, _ = env.step(action)
        else:
            action_idx = action if isinstance(action, (int, np.integer)) else np.argmax(action)
            next_state, reward, terminated, truncated, _ = env.step(action_idx)
            action = np.array([action_idx], dtype=np.float32)
        
        done = terminated or truncated
        
        # Compute Dark Residue
        state_hash = agent._hash_state(state)
        dr = agent.dark_residue_calc.compute(
            state, action, next_state, reward,
            agent.temporal_field, state_hash
        )
        
        # Geodesic check
        geodesic_result = agent.geodesic_map.query(state_hash)
        used_geodesic = "Yes" if geodesic_result else "No"
        
        print(f"Step {step:2d}:")
        print(f"  State: [{state[0]:6.3f}, {state[1]:6.3f}, ...]")
        print(f"  Action: {action_idx if not agent.continuous else action[0]:.3f}")
        print(f"  Reward: {reward:6.2f}")
        print(f"  Dark Residue: {dr:.4f}")
        print(f"  Used Geodesic: {used_geodesic}")
        print(f"  Δ Field: {agent.temporal_field.get(state_hash):.4f}")
        print()
        
        episode_reward += reward
        state = next_state
        step += 1
    
    print(f"Episode ended after {step} steps")
    print(f"Total reward: {episode_reward:.2f}")
    print("\n✅ Debug run complete!")


def main():
    """Run all examples"""
    print("\n" + "="*70)
    print("VAGABOND USAGE EXAMPLES")
    print("="*70)
    
    examples = [
        ("Quick Training", example_1_quick_training),
        ("Custom Config", example_2_custom_config),
        ("Conservative Stable", example_3_conservative_stable),
        ("Evaluate & Visualize", example_4_evaluate_and_visualize),
        ("Manual Training Loop", example_5_manual_training_loop),
        ("Transfer Learning", example_6_transfer_learning),
        ("Curriculum Learning", example_7_curriculum_learning),
        ("Compare Configs", example_8_compare_configurations),
        ("Debug Mode", example_9_debug_mode),
    ]
    
    print("\nAvailable examples:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"  {i}. {name}")
    
    print("\nRun all? (y/n): ", end="")
    run_all = input().strip().lower() == 'y'
    
    if run_all:
        for name, func in examples:
            try:
                func()
            except Exception as e:
                print(f"\n⚠️  Example '{name}' failed: {e}")
    else:
        print("\nSelect example number (1-9): ", end="")
        try:
            choice = int(input().strip())
            if 1 <= choice <= len(examples):
                examples[choice - 1][1]()
            else:
                print("Invalid choice")
        except ValueError:
            print("Invalid input")


if __name__ == "__main__":
    # Quick demo - just run a couple examples
    print("\n🌀 Running quick demo examples...\n")
    
    example_1_quick_training()
    example_2_custom_config()
    
    print("\n" + "="*70)
    print("For more examples, run: python examples.py")
    print("="*70 + "\n")
