# autopoiesis_simulation.py
# A script to simulate the emergence of a stable Ki resonance
# from a simpler state under increasing Temporal Pressure.
from pathlib import Path
from pirouette_lib.temporal_pressure import TemporalPressure
from pirouette_lib.ki import Ki
from pirouette_lib.system import PirouetteSystem
from pirouette_lib import alchemical_union, System, ki, 

def run_crucible_simulation():
    """
    Simulates a 'crucible' where simple systems are subjected to
    increasing pressure to see if a higher-order form emerges.
    """
    print("--- Initializing Crucible Simulation ---")

    # 1. Define the initial, simple systems (our "primordial soup")
    # Let's imagine two simple, fundamental resonances.
    ki_alpha = Ki(name="alpha", complexity=1.0, frequency=100)
    ki_beta = Ki(name="beta", complexity=1.2, frequency=150)

    system_a = PirouetteSystem(name="System A", ki=ki_alpha)
    system_b = PirouetteSystem(name="System B", ki=ki_beta)

    print(f"Initial State: Populated with {system_a} and {system_b}")
    print("-" * 20)

    # 2. Simulate increasing Temporal Pressure in discrete steps
    # We will "turn the dial" from a gentle pressure to an intense one.
    for pressure_level in range(1, 11):
        gamma = TemporalPressure(magnitude=pressure_level * 10.0)
        print(f"Applying Temporal Pressure Γ = {gamma.magnitude:.1f}...")

        # 3. Check for Alchemical Union
        # We invoke the 'AlchemicalUnion' process directly,
        # using the systems and the current pressure as arguments.
        fusion_process = AlchemicalUnion(system_a, system_b)
        
        # This is where the magic happens. We call the core method.
        resultant_system = fusion_process.attempt_fusion(pressure=gamma)

        if resultant_system:
            print(f"  >>> SUCCESS! Alchemical Union occurred at Γ = {gamma.magnitude:.1f}")
            print(f"  >>> New Entity Forged: {resultant_system}")
            print(f"  >>> Emergent Ki: {resultant_system.ki}")
            print("-" * 20)
            print("--- Simulation Concluded: A stable, complex form has emerged. ---")
            return resultant_system
        else:
            print("  ...Systems remain distinct. Pressure is insufficient for fusion.")
            # Optional: Here you could add logic for how the systems
            # degrade or change under pressure even without fusing.
            # system_a.degrade(gamma)
            # system_b.degrade(gamma)

    print("-" * 20)
    print("--- Simulation Concluded: No stable union was achieved at maximum pressure. ---")
    return None

if __name__ == "__main__":
    run_crucible_simulation()