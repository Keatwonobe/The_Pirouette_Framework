import random
import time

# --- CONFIGURATION (D&D 5e Standard) ---
# Total points allowed to spend
TOTAL_BUDGET = 28

# The lowest score a stat can start at
BASE_SCORE = 8

# The highest score allowed (before racial bonuses)
MAX_SCORE = 15

# Cost table: Maps a score to its cumulative point cost
# 8 costs 0, 9 costs 1, ... 14 costs 7, 15 costs 9
COST_TABLE = {
    8: 0,
    9: 1,
    10: 2,
    11: 3,
    12: 4,
    13: 5,
    14: 7,
    15: 9
}

ATTRIBUTES = [
    "Strength", "Dexterity", "Constitution", 
    "Intelligence", "Wisdom"
]

def get_upgrade_cost(current_score):
    """
    Calculates the cost to increase a score by 1 point.
    Returns None if the score is already at MAX_SCORE.
    """
    if current_score >= MAX_SCORE:
        return None
    
    next_score = current_score + 1
    
    if next_score not in COST_TABLE:
        return None # Should not happen with standard config
        
    current_cost = COST_TABLE[current_score]
    next_cost = COST_TABLE[next_score]
    
    return next_cost - current_cost

def generate_random_point_buy():
    """
    Randomly distributes points to attributes until the budget is spent.
    Uses a trial-and-error approach to ensure we land exactly on 0 remaining points.
    """
    
    while True:
        # 1. Start everyone at the base score (8)
        stats = [BASE_SCORE] * len(ATTRIBUTES)
        remaining_budget = TOTAL_BUDGET
        
        # 2. Distribute points loop
        while remaining_budget > 0:
            # Find which stats are valid candidates to be increased
            # A stat is valid if:
            # a) It isn't at the max score yet
            # b) We have enough points left in the budget to pay for the upgrade
            candidates = []
            for i in range(len(stats)):
                cost = get_upgrade_cost(stats[i])
                if cost is not None and cost <= remaining_budget:
                    candidates.append(i)
            
            # If we have budget left but no affordable upgrades (e.g., 1 point left 
            # but only 2-point upgrades available), this run is a "failure".
            if not candidates:
                break 
            
            # Pick a random candidate and upgrade them
            choice_index = random.choice(candidates)
            upgrade_cost = get_upgrade_cost(stats[choice_index])
            
            stats[choice_index] += 1
            remaining_budget -= upgrade_cost
            
        # 3. Validation
        # If we successfully spent exactly all points, return the result.
        # If we broke out early (stuck with remainder), the outer 'while True' 
        # will just restart the process instantly.
        if remaining_budget == 0:
            return stats

def format_output(stats):
    """Helps print the stats nicely."""
    
    # Shuffle the attribute names so Strength isn't always the highest/lowest
    # (The stats list itself is random, but assigning them randomly adds variety)
    shuffled_attrs = ATTRIBUTES.copy()
    random.shuffle(shuffled_attrs)
    
    print("-" * 40)
    print(f"{'Attribute':<15} | {'Score':<5} | {'Cost':<5}")
    print("-" * 40)
    
    total_cost_check = 0
    
    for i in range(len(ATTRIBUTES)):
        score = stats[i]
        cost = COST_TABLE[score]
        attr = shuffled_attrs[i]
        
        print(f"{attr:<15} | {score:<5} | {cost:<5}")
        total_cost_check += cost
        
    print("-" * 40)
    print(f"{'TOTAL POINTS':<15} | {'':<5} | {total_cost_check:<5} / {TOTAL_BUDGET}")
    print("-" * 40)

def main():
    print(f"Welcome to the D&D 5e Point Buy Randomizer!")
    print(f"Budget: {TOTAL_BUDGET} points. Range: {BASE_SCORE}-{MAX_SCORE}.\n")
    
    while True:
        stats = generate_random_point_buy()
        format_output(stats)
        
        user_input = input("\nPress [Enter] to generate again, or type 'q' to quit: ")
        if user_input.lower() == 'q':
            print("Happy adventuring!")
            break

if __name__ == "__main__":
    main()