#!/usr/bin/env python3
"""
dice_buy.py - NEW: Entropy dice-buy mechanic for attack gambling
Implements entropy -> dice conversion with fizzle chance
"""

import random
from utils import roll_dice


# Dice buy costs (EP cost -> dice notation)
DICE_BUY_TABLE = {
    1: {"dice": "1d3-1", "num": 1, "sides": 3, "bonus": -1},
    2: {"dice": "1d4-1", "num": 1, "sides": 4, "bonus": -1},
    3: {"dice": "1d6-1", "num": 1, "sides": 6, "bonus": -1},
    4: {"dice": "2d3-1", "num": 2, "sides": 3, "bonus": -1},
    5: {"dice": "2d4-1", "num": 2, "sides": 4, "bonus": -1},
    6: {"dice": "1d8-1", "num": 1, "sides": 8, "bonus": -1},
    8: {"dice": "2d6-1", "num": 2, "sides": 6, "bonus": -1},
    10: {"dice": "2d8-1", "num": 2, "sides": 8, "bonus": -1},
}


def get_available_dice_buys(ep_available):
    """
    Return list of dice buy options within EP budget.
    Returns list of (ep_cost, dice_string) tuples.
    """
    options = []
    for cost, info in sorted(DICE_BUY_TABLE.items()):
        if cost <= ep_available:
            options.append((cost, info["dice"]))
    return options


def apply_dice_buy(ep_spent, fizzle_threshold=1):
    """
    Convert EP into dice roll with fizzle chance.
    
    Args:
        ep_spent: Amount of EP to convert to dice
        fizzle_threshold: If any die rolls <= this value, entire roll fizzles
    
    Returns:
        dict with 'damage', 'fizzled', 'roll_detail'
    """
    if ep_spent not in DICE_BUY_TABLE:
        # If exact match not found, use largest affordable
        valid_costs = [c for c in DICE_BUY_TABLE.keys() if c <= ep_spent]
        if not valid_costs:
            return {
                "damage": 0,
                "fizzled": True,
                "roll_detail": "No valid dice buy for this EP amount"
            }
        ep_spent = max(valid_costs)
    
    dice_info = DICE_BUY_TABLE[ep_spent]
    num = dice_info["num"]
    sides = dice_info["sides"]
    bonus = dice_info["bonus"]
    
    # Roll the dice
    rolls = [random.randint(1, sides) for _ in range(num)]
    total = sum(rolls) + bonus
    
    # Check for fizzle
    fizzled = any(r <= fizzle_threshold for r in rolls)
    
    if fizzled:
        damage = 0
        status = "FIZZLED"
    else:
        damage = max(0, total)  # Can't go below 0
        status = "HIT"
    
    roll_detail = f"{num}d{sides}{bonus:+d} = [{', '.join(map(str, rolls))}]{bonus:+d} = {total} [{status}]"
    
    return {
        "damage": damage,
        "fizzled": fizzled,
        "roll_detail": roll_detail,
        "ep_spent": ep_spent
    }


def calculate_attack_with_dice_buy(base_ep, buy_ep=0, raw_efficiency=0.5):
    """
    Calculate total attack damage using base EP and optional dice buy.
    
    Args:
        base_ep: EP applied directly as damage (at raw_efficiency)
        buy_ep: EP spent on dice buy gambling
        raw_efficiency: Efficiency of direct EP application (default 0.5)
    
    Returns:
        dict with 'total_damage', 'base_damage', 'dice_damage', 'details'
    """
    # Calculate base damage from direct EP
    base_damage = int(base_ep * raw_efficiency)
    
    # Calculate dice buy damage if any
    dice_result = None
    dice_damage = 0
    
    if buy_ep > 0:
        dice_result = apply_dice_buy(buy_ep)
        dice_damage = dice_result["damage"]
    
    total_damage = base_damage + dice_damage
    
    return {
        "total_damage": total_damage,
        "base_damage": base_damage,
        "dice_damage": dice_damage,
        "dice_result": dice_result,
        "ep_spent": base_ep + buy_ep
    }


def explain_dice_buy_options():
    """Print explanation of dice buy system"""
    print("\n=== DICE BUY SYSTEM ===")
    print("Gamble entropy for variable damage!")
    print("\nAvailable conversions:")
    for cost, info in sorted(DICE_BUY_TABLE.items()):
        print(f"  {cost} EP → {info['dice']}")
    print("\nFIZZLE RULE: If any die rolls 1, the entire dice buy deals 0 damage!")
    print("This adds risk/reward to entropy spending.\n")


def handle_dice_buy_attack(attacker, target, base_ep, buy_ep, libs):
    """
    Execute an attack using dice buy mechanics.
    
    Args:
        attacker: Attacking character
        target: Target character
        base_ep: EP for base damage
        buy_ep: EP for dice gambling
        libs: Library dict with axes, influences, etc.
    
    Returns:
        dict with attack results
    """
    # Calculate damage
    result = calculate_attack_with_dice_buy(base_ep, buy_ep)
    
    print(f"\n[ATTACK] {attacker['name']} → {target['name']}")
    print(f"  Base EP: {base_ep} → {result['base_damage']} damage")
    
    if buy_ep > 0 and result['dice_result']:
        print(f"  Dice Buy: {buy_ep} EP → {result['dice_result']['roll_detail']}")
    
    print(f"  TOTAL DAMAGE: {result['total_damage']}")
    
    # Apply damage through wound channels
    # (This would call into damage_system.py in full implementation)
    
    return result


def parse_dice_buy_command(parts):
    """
    Parse dice buy command from CLI.
    
    Format: attack <target> spend <base_ep> buy <buy_ep>
    
    Returns: (target_idx, base_ep, buy_ep) or None
    """
    if "spend" not in parts:
        return None
    
    try:
        # Get target
        target_idx = int(parts[1]) - 1
        
        # Find 'spend' keyword
        spend_idx = parts.index("spend")
        base_ep = int(parts[spend_idx + 1])
        
        # Check for 'buy' keyword
        buy_ep = 0
        if "buy" in parts:
            buy_idx = parts.index("buy")
            buy_ep = int(parts[buy_idx + 1])
        
        return (target_idx, base_ep, buy_ep)
    
    except (ValueError, IndexError):
        return None
