import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import pandas as pd
from collections import defaultdict
import math

class ResonantSalesSimulator:
    """
    A simulator for modeling sales team performance using the Resonant Organization 
    framework with proper Pirouette mathematics.
    
    This simulator models a 7-person Resonant Frame sales team, demonstrating how
    Time-Adherence (Ta), Gladiator Force (Γ), and Ki-constant affect sales outcomes.
    """
    
    def __init__(self, 
                 simulation_days=90,
                 ki_rest=4.14159,
                 ki_motion=4.18879,
                 initial_ta=0.7,
                 initial_gladiator=0.4,
                 market_volatility=0.2,
                 implementation_phase="unwinding",
                 seed=None):
        """
        Initialize the Resonant Sales Simulator.
        
        Args:
            simulation_days: Number of days to simulate
            ki_rest: The Ki constant for stationary mode (~4.14159)
            ki_motion: The Ki constant for motion mode (~4.18879)
            initial_ta: Starting Time-Adherence value (0-1)
            initial_gladiator: Starting Gladiator Force value (0-1)
            market_volatility: Volatility of the market (0-1)
            implementation_phase: Current phase in implementation ("unwinding", "winding", "consolidation")
            seed: Random seed for reproducibility
        """
        # Set random seed if provided
        if seed is not None:
            np.random.seed(seed)
        
        # Pirouette constants
        self.ki_rest = ki_rest
        self.ki_motion = ki_motion
        
        # Simulation parameters
        self.simulation_days = simulation_days
        self.current_day = 0
        self.market_volatility = market_volatility
        self.implementation_phase = implementation_phase
        
        # Team structure - based on the 7-person Resonant Frame
        self.team = {
            "interface": {"productivity": 0.8, "focus": "management"},      # Team lead/manager
            "feedback": {"productivity": 0.7, "focus": "analytics"},       # Analyst/AI integrator
            "support1": {"productivity": 0.9, "focus": "research"},        # Support role 1
            "support2": {"productivity": 0.9, "focus": "admin"},           # Support role 2
            "core1": {"productivity": 1.0, "focus": "sales"},              # Core sales rep 1
            "core2": {"productivity": 1.0, "focus": "sales"},              # Core sales rep 2
            "core3": {"productivity": 1.0, "focus": "sales"},              # Core sales rep 3
        }
        
        # Resonance parameters
        self.ta = initial_ta  # Time-Adherence
        self.gladiator = initial_gladiator  # Gladiator Force
        
        # Control parameters for feedback equations
        self.lambda_decay = 0.1   # Natural decay rate of performance
        self.mu_feedback = 0.2    # Feedback strength coefficient
        
        # Performance metrics
        self.daily_sales = []
        self.daily_ta = []
        self.daily_gladiator = []
        self.daily_calls = []
        self.daily_conversion = []
        self.daily_average_deal = []
        self.cumulative_sales = []
        
        # Reference metrics (for comparison)
        self.reference_sales = []
        self.reference_cumulative = []
        
        # Phase transition tracking
        self.phase_transitions = []
        if implementation_phase != "unwinding":
            self.phase_transitions.append({"day": 0, "phase": implementation_phase})
        
        # Generate synthetic market conditions for the simulation period
        self.market_conditions = self._generate_market_conditions()
        
        # Initialize model state and history
        self.history = []
        self.initialize_state()
    
    def initialize_state(self):
        """Initialize the starting state of the simulation."""
        # Set initial state
        state = {
            "day": 0,
            "ta": self.ta,
            "gladiator": self.gladiator,
            "sales": 0,
            "cumulative_sales": 0,
            "calls": self._calculate_total_calls(),
            "conversion_rate": self._calculate_conversion_rate(),
            "average_deal_size": self._calculate_average_deal_size(),
            "team_health": self._calculate_team_health(),
            "market_condition": self.market_conditions[0],
            "phase": self.implementation_phase
        }
        
        self.history.append(state)
        self.daily_sales.append(0)
        self.daily_ta.append(self.ta)
        self.daily_gladiator.append(self.gladiator)
        self.daily_calls.append(state["calls"])
        self.daily_conversion.append(state["conversion_rate"])
        self.daily_average_deal.append(state["average_deal_size"])
        self.cumulative_sales.append(0)
        
        # Calculate reference (non-resonant) sales
        ref_sales = self._calculate_reference_sales(0)
        self.reference_sales.append(ref_sales)
        self.reference_cumulative.append(ref_sales)
    
    def _generate_market_conditions(self):
        """Generate synthetic market conditions for the simulation period."""
        # Start with baseline market
        base = 1.0
        
        # Generate random daily fluctuations with some autocorrelation
        conditions = [base]
        for _ in range(1, self.simulation_days):
            # Market has some memory of previous day (autocorrelation)
            previous = conditions[-1]
            change = np.random.normal(0, self.market_volatility)
            # Ensure market doesn't go below 0.5 or above 1.5 (reasonable bounds)
            new_condition = max(0.5, min(1.5, previous + change))
            conditions.append(new_condition)
        
        return conditions
    
    def _calculate_reference_sales(self, day):
        """Calculate sales for a reference (non-resonant) team for comparison."""
        # Basic sales model without resonance benefits
        base_calls = 15  # Each sales rep makes 15 calls per day
        base_conversion = 0.05  # 5% conversion rate
        base_deal_size = 1000  # $1000 average deal
        
        # Team size is same (3 core sales reps)
        total_calls = 3 * base_calls
        
        # Apply market condition
        market = self.market_conditions[day]
        
        # Calculate reference sales
        ref_sales = total_calls * base_conversion * base_deal_size * market
        
        return ref_sales
    
    def _calculate_total_calls(self):
        """Calculate the total number of sales calls based on team structure and resonance."""
        # Base call capacity for core sales reps
        base_calls_per_rep = 15
        
        # Calculate total core capacity
        core_reps = [member for member, data in self.team.items() if data["focus"] == "sales"]
        core_capacity = sum(self.team[rep]["productivity"] for rep in core_reps) * base_calls_per_rep
        
        # Time-Adherence affects call efficiency
        # High Ta means team sticks to optimal call schedule, reduces dead time
        ta_multiplier = 0.7 + (0.6 * self.ta)  # ranges from 0.7 to 1.3
        
        # Gladiator force affects how well information flows between team members
        # Moderate Γ is optimal (too high = chaotic, too low = rigid)
        gladiator_optimal = 0.4  # The sweet spot for Gladiator force
        gladiator_distance = abs(self.gladiator - gladiator_optimal)
        gladiator_multiplier = 1.0 - (0.3 * gladiator_distance)  # Penalty for being away from optimal
        
        # Calculate phase-dependent bonuses based on implementation phase
        phase_bonus = self._calculate_phase_bonus()
        
        # Apply all multipliers
        total_calls = core_capacity * ta_multiplier * gladiator_multiplier * phase_bonus
        
        # Add slight randomness to simulate daily variation
        randomness = np.random.normal(1.0, 0.05)  # 5% standard deviation
        
        return total_calls * randomness
    
    def _calculate_conversion_rate(self):
        """Calculate the conversion rate based on team performance and resonance."""
        # Base conversion rate
        base_conversion = 0.05  # 5% baseline
        
        # Support roles enhance conversion by providing good leads and materials
        support_members = [member for member, data in self.team.items() if "support" in member]
        support_effectiveness = sum(self.team[member]["productivity"] for member in support_members) / len(support_members)
        
        # Time-Adherence affects conversion via preparation and timing of follow-ups
        # Higher Ta means better follow-through on leads
        ta_multiplier = 0.8 + (0.4 * self.ta)  # ranges from 0.8 to 1.2
        
        # Gladiator force affects how well the team adapts to different customer needs
        # Moderate Γ is optimal (too high = inconsistent, too low = rigid script)
        gladiator_optimal = 0.4
        gladiator_distance = abs(self.gladiator - gladiator_optimal)
        gladiator_multiplier = 1.0 - (0.3 * gladiator_distance)
        
        # Interface (manager) quality affects overall conversion through coaching
        interface_effect = self.team["interface"]["productivity"] * 0.15
        
        # Feedback role improves conversion by providing data-driven insights
        feedback_effect = self.team["feedback"]["productivity"] * 0.15
        
        # Phase-dependent bonuses
        phase_bonus = self._calculate_phase_bonus()
        
        # Apply Pirouette resonance function: conversion improves with phase alignment
        # Use the core Pirouette resonance equation: cos(Ki * Δϕ)
        # where Δϕ is the phase difference between our operations and market
        # For simplicity, we use the day number modulo Ki as a proxy for phase
        day_phase = (self.current_day % self.ki_rest) / self.ki_rest * 2 * np.pi
        market_phase = np.random.uniform(0, 2 * np.pi)  # Market has its own phase
        phase_diff = day_phase - market_phase
        resonance_factor = 0.9 + (0.2 * np.cos(self.ki_rest * phase_diff))  # 0.7-1.1 range
        
        # Calculate final conversion rate with all factors
        conversion = (base_conversion * 
                      support_effectiveness * 
                      ta_multiplier * 
                      gladiator_multiplier * 
                      (1 + interface_effect) * 
                      (1 + feedback_effect) * 
                      phase_bonus * 
                      resonance_factor)
        
        # Add slight randomness
        randomness = np.random.normal(1.0, 0.08)  # 8% standard deviation
        conversion = conversion * randomness
        
        # Ensure conversion rate stays in reasonable bounds
        return max(0.01, min(0.25, conversion))
    
    def _calculate_average_deal_size(self):
        """Calculate the average deal size based on team performance and market conditions."""
        # Base deal size
        base_deal = 1000  # $1000 baseline
        
        # Market condition affects deal size
        market = self.market_conditions[self.current_day]
        
        # Time-Adherence affects deal size via preparation quality
        ta_multiplier = 0.85 + (0.3 * self.ta)  # ranges from 0.85 to 1.15
        
        # Gladiator force affects how well team can customize and upsell
        # Moderate Γ is optimal for customization
        gladiator_optimal = 0.35  # Slightly different optimal point for deal size
        gladiator_distance = abs(self.gladiator - gladiator_optimal) 
        gladiator_multiplier = 1.0 - (0.25 * gladiator_distance)
        
        # Interface role affects deal size through negotiation strategy
        interface_effect = self.team["interface"]["productivity"] * 0.2
        
        # Phase-dependent bonuses
        phase_bonus = self._calculate_phase_bonus()
        
        # Apply resonance effects based on the Ki constant
        # Deal size improves when team operations cycle aligns with Ki
        ki_alignment = 0.9 + (0.2 * np.sin(2 * np.pi * self.current_day / self.ki_rest))
        
        # Calculate final deal size
        deal_size = (base_deal * 
                     market * 
                     ta_multiplier * 
                     gladiator_multiplier * 
                     (1 + interface_effect) * 
                     phase_bonus *
                     ki_alignment)
        
        # Add randomness
        randomness = np.random.normal(1.0, 0.1)  # 10% standard deviation
        
        return deal_size * randomness
    
    def _calculate_team_health(self):
        """Calculate overall team health based on resonance parameters."""
        # Team health is optimal when parameters are in balance
        
        # Time-Adherence: Too high = burnout, Too low = confusion
        ta_optimal = 0.8
        ta_health = 1.0 - abs(self.ta - ta_optimal) * 2
        
        # Gladiator Force: Too high = chaos, Too low = rigidity
        gladiator_optimal = 0.4
        gladiator_health = 1.0 - abs(self.gladiator - gladiator_optimal) * 2.5
        
        # Combine metrics
        overall_health = (ta_health + gladiator_health) / 2
        
        # Bound between 0 and 1
        return max(0.0, min(1.0, overall_health))
    
    def _calculate_phase_bonus(self):
        """Calculate performance bonus based on implementation phase."""
        if self.implementation_phase == "unwinding":
            # Unwinding phase: Modest improvements as basic inefficiencies are removed
            return 1.05  # 5% improvement
        elif self.implementation_phase == "winding":
            # Winding phase: Substantial improvements as team hits its stride
            return 1.15  # 15% improvement
        elif self.implementation_phase == "consolidation":
            # Consolidation phase: Strong, stable performance
            return 1.25  # 25% improvement
        else:
            return 1.0  # Default
    
    def _update_resonance_parameters(self):
        """Update Ta and Gladiator based on performance and feedback."""
        # Get previous state
        prev_state = self.history[-1]
        
        # Implement the dynamic feedback control law from the paper:
        # dAFrame/dt = -λ(1 - AFrame(t)) + μ ΔP(t)
        
        # For Time-Adherence:
        # Natural decay: Ta tends to decay without active maintenance
        ta_decay = -self.lambda_decay * (1 - self.ta)
        
        # Feedback correction: Team adjusts based on performance feedback
        performance_delta = (prev_state["sales"] / self.reference_sales[-1]) - 1.0 if self.reference_sales[-1] > 0 else 0
        ta_correction = self.mu_feedback * performance_delta
        
        # Combined update
        ta_change = ta_decay + ta_correction
        
        # For Gladiator Force:
        # It should evolve based on team dynamics and implementation phase
        if self.implementation_phase == "unwinding":
            # Unwinding phase: Gradually increase structure (reduce Γ)
            target_gladiator = 0.35
        elif self.implementation_phase == "winding":
            # Winding phase: Find optimal flexibility
            target_gladiator = 0.4
        else:  # consolidation
            # Consolidation: Maintain optimal flexibility
            target_gladiator = 0.4
            
        # Gradual adjustment toward target
        gladiator_change = (target_gladiator - self.gladiator) * 0.05
        
        # Apply changes with bounds
        self.ta = max(0.1, min(0.95, self.ta + ta_change))
        self.gladiator = max(0.1, min(0.9, self.gladiator + gladiator_change))
    
    def _check_phase_transition(self):
        """Check if we should transition to a new implementation phase."""
        # Simulate phase transitions based on days and performance
        if self.implementation_phase == "unwinding" and self.current_day >= 30:
            self.implementation_phase = "winding"
            self.phase_transitions.append({"day": self.current_day, "phase": "winding"})
            return True
            
        elif self.implementation_phase == "winding" and self.current_day >= 60:
            self.implementation_phase = "consolidation"
            self.phase_transitions.append({"day": self.current_day, "phase": "consolidation"})
            return True
            
        return False
    
    def simulate_day(self):
        """Simulate a single day of sales operations."""
        if self.current_day >= self.simulation_days:
            return False
            
        # Calculate key metrics for the day
        total_calls = self._calculate_total_calls()
        conversion_rate = self._calculate_conversion_rate()
        average_deal = self._calculate_average_deal_size()
        
        # Calculate daily sales
        daily_sales = total_calls * conversion_rate * average_deal
        
        # Get cumulative sales
        prev_cumulative = self.history[-1]["cumulative_sales"]
        cumulative_sales = prev_cumulative + daily_sales
        
        # Update resonance parameters based on feedback
        self._update_resonance_parameters()
        
        # Check for phase transitions
        phase_transition = self._check_phase_transition()
        
        # Calculate team health
        team_health = self._calculate_team_health()
        
        # Store the day's results
        state = {
            "day": self.current_day + 1,
            "ta": self.ta,
            "gladiator": self.gladiator,
            "sales": daily_sales,
            "cumulative_sales": cumulative_sales,
            "calls": total_calls,
            "conversion_rate": conversion_rate,
            "average_deal_size": average_deal,
            "team_health": team_health,
            "market_condition": self.market_conditions[self.current_day],
            "phase": self.implementation_phase
        }
        
        self.history.append(state)
        self.daily_sales.append(daily_sales)
        self.daily_ta.append(self.ta)
        self.daily_gladiator.append(self.gladiator)
        self.daily_calls.append(total_calls)
        self.daily_conversion.append(conversion_rate)
        self.daily_average_deal.append(average_deal)
        self.cumulative_sales.append(cumulative_sales)
        
        # Calculate reference sales for comparison
        ref_sales = self._calculate_reference_sales(self.current_day)
        ref_cumulative = self.reference_cumulative[-1] + ref_sales
        
        self.reference_sales.append(ref_sales)
        self.reference_cumulative.append(ref_cumulative)
        
        # Increment day counter
        self.current_day += 1
        
        return True
    
    def run_simulation(self):
        """Run the full simulation for the specified number of days."""
        for _ in range(self.simulation_days):
            if not self.simulate_day():
                break
                
        return self.get_results()
    
    def get_results(self):
        """Get simulation results in a structured format."""
        return {
            "daily_data": self.history,
            "summary": self._generate_summary(),
            "phase_transitions": self.phase_transitions
        }
    
    def _generate_summary(self):
        """Generate summary statistics from the simulation."""
        # Calculate key performance indicators
        final_state = self.history[-1]
        
        # Overall sales improvement
        initial_reference = self.reference_sales[0] if self.reference_sales[0] > 0 else 1
        final_reference = self.reference_sales[-1] if self.reference_sales[-1] > 0 else 1
        
        initial_actual = self.daily_sales[0] if self.daily_sales[0] > 0 else 1
        final_actual = self.daily_sales[-1] if self.daily_sales[-1] > 0 else 1
        
        reference_improvement = (final_reference / initial_reference) - 1
        actual_improvement = (final_actual / initial_actual) - 1
        
        # Advantage over reference
        total_sales_advantage = (self.cumulative_sales[-1] / self.reference_cumulative[-1]) - 1
        
        # Phase-specific metrics
        phase_metrics = {}
        for phase in ["unwinding", "winding", "consolidation"]:
            phase_days = [day for day, state in enumerate(self.history) if state["phase"] == phase]
            if phase_days:
                phase_metrics[phase] = {
                    "days": len(phase_days),
                    "avg_sales": np.mean([self.daily_sales[day] for day in phase_days]),
                    "avg_ta": np.mean([self.daily_ta[day] for day in phase_days]),
                    "avg_gladiator": np.mean([self.daily_gladiator[day] for day in phase_days]),
                }
        
        return {
            "total_days": self.current_day,
            "final_ta": final_state["ta"],
            "final_gladiator": final_state["gladiator"],
            "final_sales_per_day": final_state["sales"],
            "total_sales": final_state["cumulative_sales"],
            "reference_total_sales": self.reference_cumulative[-1],
            "sales_improvement": actual_improvement,
            "reference_improvement": reference_improvement,
            "advantage_over_reference": total_sales_advantage,
            "phase_metrics": phase_metrics
        }
    
    def visualize_results(self, filename=None):
        """Create visualizations of the simulation results."""
        # Setup plots
        fig, axs = plt.subplots(3, 2, figsize=(15, 14))
        fig.suptitle('Resonant Organization Sales Simulation Results', fontsize=16)
        
        # Extract data for plotting
        days = list(range(self.current_day + 1))
        
        # Plot 1: Daily Sales Comparison
        axs[0, 0].plot(days, self.daily_sales, 'b-', label='Resonant Team')
        axs[0, 0].plot(days, self.reference_sales, 'r--', label='Reference Team')
        
        # Add vertical lines for phase transitions
        for transition in self.phase_transitions:
            axs[0, 0].axvline(x=transition["day"], color='g', linestyle='-', alpha=0.7)
            axs[0, 0].text(transition["day"], max(self.daily_sales) * 0.9, 
                          f"→ {transition['phase'].capitalize()}", 
                          rotation=90, fontsize=9, color='green')
        
        axs[0, 0].set_title('Daily Sales Performance')
        axs[0, 0].set_xlabel('Day')
        axs[0, 0].set_ylabel('Sales Revenue ($)')
        axs[0, 0].legend()
        axs[0, 0].grid(True, alpha=0.3)
        
        # Plot 2: Cumulative Sales
        axs[0, 1].plot(days, self.cumulative_sales, 'b-', label='Resonant Team')
        axs[0, 1].plot(days, self.reference_cumulative, 'r--', label='Reference Team')
        
        # Shade the area between curves to show cumulative advantage
        axs[0, 1].fill_between(days, self.cumulative_sales, self.reference_cumulative, 
                              where=(np.array(self.cumulative_sales) > np.array(self.reference_cumulative)),
                              alpha=0.3, color='blue', interpolate=True)
        
        # Add annotation for total advantage
        advantage = self.cumulative_sales[-1] - self.reference_cumulative[-1]
        advantage_percent = (self.cumulative_sales[-1] / self.reference_cumulative[-1] - 1) * 100
        axs[0, 1].annotate(f'+${advantage:.2f} (+{advantage_percent:.1f}%)',
                          xy=(days[-1], self.cumulative_sales[-1]),
                          xytext=(days[-1]*0.8, self.cumulative_sales[-1]*0.9),
                          arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                          fontsize=10)
        
        axs[0, 1].set_title('Cumulative Sales')
        axs[0, 1].set_xlabel('Day')
        axs[0, 1].set_ylabel('Cumulative Revenue ($)')
        axs[0, 1].legend()
        axs[0, 1].grid(True, alpha=0.3)
        
        # Plot 3: Time-Adherence and Gladiator Force Evolution
        axs[1, 0].plot(days, self.daily_ta, 'g-', label='Time-Adherence (Ta)')
        axs[1, 0].plot(days, self.daily_gladiator, 'm-', label='Gladiator Force (Γ)')
        
        # Add optimal ranges as shaded areas
        axs[1, 0].axhspan(0.75, 0.85, alpha=0.2, color='green', label='Optimal Ta Range')
        axs[1, 0].axhspan(0.35, 0.45, alpha=0.2, color='magenta', label='Optimal Γ Range')
        
        # Add phase transitions
        for transition in self.phase_transitions:
            axs[1, 0].axvline(x=transition["day"], color='gray', linestyle='--', alpha=0.7)
        
        axs[1, 0].set_title('Resonance Parameters Evolution')
        axs[1, 0].set_xlabel('Day')
        axs[1, 0].set_ylabel('Parameter Value')
        axs[1, 0].set_ylim(0, 1)
        axs[1, 0].legend()
        axs[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Sales Metrics
        axs[1, 1].plot(days, self.daily_calls, 'b-', label='Daily Calls')
        axs[1, 1].set_ylabel('Number of Calls', color='b')
        axs[1, 1].tick_params(axis='y', labelcolor='b')
        
        # Create twin axis for conversion rate
        ax2 = axs[1, 1].twinx()
        ax2.plot(days, [rate * 100 for rate in self.daily_conversion], 'r-', label='Conversion Rate')
        ax2.set_ylabel('Conversion Rate (%)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        # Combine legends
        lines1, labels1 = axs[1, 1].get_legend_handles_labels()
        lines2, labels2 = ax2.get_legend_handles_labels()
        ax2.legend(lines1 + lines2, labels1 + labels2, loc='upper left')
        
        axs[1, 1].set_title('Sales Activity Metrics')
        axs[1, 1].set_xlabel('Day')
        axs[1, 1].grid(True, alpha=0.3)
        
        # Plot 5: Average Deal Size
        axs[2, 0].plot(days, self.daily_average_deal, 'g-')
        
        # Add phase transitions
        for transition in self.phase_transitions:
            axs[2, 0].axvline(x=transition["day"], color='gray', linestyle='--', alpha=0.7)
        
        axs[2, 0].set_title('Average Deal Size')
        axs[2, 0].set_xlabel('Day')
        axs[2, 0].set_ylabel('Average Deal ($)')
        axs[2, 0].grid(True, alpha=0.3)
        
        # Plot 6: Phase Comparison
        # Prepare data for bar chart
        summary = self._generate_summary()
        phase_metrics = summary["phase_metrics"]
        
        phases = list(phase_metrics.keys())
        avg_sales = [phase_metrics[phase]["avg_sales"] for phase in phases]
        
        # Convert phase names to title case
        phase_labels = [phase.capitalize() for phase in phases]
        
        # Create the bar chart
        axs[2, 1].bar(phase_labels, avg_sales, color=['#E6B0AA', '#5DADE2', '#7DCEA0'])
        
        # Add text labels above bars
        for i, v in enumerate(avg_sales):
            axs[2, 1].text(i, v + 100, f"${v:.2f}", ha='center')
        
        axs[2, 1].set_title('Average Daily Sales by Implementation Phase')
        axs[2, 1].set_ylabel('Average Daily Sales ($)')
        axs[2, 1].grid(True, alpha=0.3, axis='y')
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # Save or show the visualization
        if filename:
            plt.savefig(filename)
            plt.close()
        else:
            plt.show()

class ResonantSalesExperiment:
    """
    Run multiple simulations to test different parameters and configurations
    of the Resonant Organization framework.
    """
    
    def __init__(self):
        """Initialize the experiment runner."""
        self.experiment_results = []
        
    def run_parameter_sweep(self, 
                            initial_ta_values=[0.5, 0.7, 0.9],
                            initial_gladiator_values=[0.2, 0.4, 0.6],
                            market_volatility_values=[0.1, 0.2, 0.3],
                            simulation_days=90,
                            runs_per_config=3):
        """Run a parameter sweep to test different configurations.
        
        Args:
            initial_ta_values: List of Time-Adherence values to test
            initial_gladiator_values: List of Gladiator Force values to test
            market_volatility_values: List of market volatility values to test
            simulation_days: Number of days to simulate for each configuration
            runs_per_config: Number of runs per configuration (for statistical significance)
        
        Returns:
            Dictionary of experiment results
        """
        results = []
        
        # Create all combinations of parameters
        total_configs = len(initial_ta_values) * len(initial_gladiator_values) * len(market_volatility_values)
        total_runs = total_configs * runs_per_config
        run_count = 0
        
        print(f"Running parameter sweep with {total_configs} configurations, {runs_per_config} runs each ({total_runs} total runs)")
        
        for ta in initial_ta_values:
            for gladiator in initial_gladiator_values:
                for volatility in market_volatility_values:
                    config_results = []
                    
                    for run in range(runs_per_config):
                        run_count += 1
                        print(f"Running configuration {run_count}/{total_runs}: Ta={ta}, Γ={gladiator}, volatility={volatility}, run {run+1}/{runs_per_config}")
                        
                        # Create simulator with this configuration
                        simulator = ResonantSalesSimulator(
                            simulation_days=simulation_days,
                            initial_ta=ta,
                            initial_gladiator=gladiator,
                            market_volatility=volatility,
                            implementation_phase="unwinding",
                            seed=run  # Different seed for each run
                        )
                        
                        # Run simulation
                        sim_results = simulator.run_simulation()
                        
                        # Extract key metrics
                        summary = sim_results["summary"]
                        config_results.append({
                            "run": run,
                            "total_sales": summary["total_sales"],
                            "reference_total_sales": summary["reference_total_sales"],
                            "advantage_percent": summary["advantage_over_reference"] * 100,
                            "final_ta": summary["final_ta"],
                            "final_gladiator": summary["final_gladiator"]
                        })
                    
                    # Calculate average results for this configuration
                    avg_sales = np.mean([r["total_sales"] for r in config_results])
                    avg_reference = np.mean([r["reference_total_sales"] for r in config_results])
                    avg_advantage = np.mean([r["advantage_percent"] for r in config_results])
                    avg_final_ta = np.mean([r["final_ta"] for r in config_results])
                    avg_final_gladiator = np.mean([r["final_gladiator"] for r in config_results])
                    
                    # Store configuration results
                    results.append({
                        "config": {
                            "initial_ta": ta,
                            "initial_gladiator": gladiator,
                            "market_volatility": volatility
                        },
                        "runs": config_results,
                        "avg_sales": avg_sales,
                        "avg_reference_sales": avg_reference,
                        "avg_advantage_percent": avg_advantage,
                        "avg_final_ta": avg_final_ta,
                        "avg_final_gladiator": avg_final_gladiator
                    })
        
        # Store overall results
        self.experiment_results = results
        return {"results": results}
    
    def run_phase_comparison(self, simulation_days=90, runs_per_phase=5):
        """Run an experiment to compare different implementation phases.
        
        Args:
            simulation_days: Number of days to simulate
            runs_per_phase: Number of runs per phase (for statistical significance)
            
        Returns:
            Dictionary of experiment results
        """
        results = []
        phases = ["unwinding", "winding", "consolidation"]
        
        print(f"Running phase comparison experiment ({len(phases)} phases, {runs_per_phase} runs each)")
        
        for phase in phases:
            phase_results = []
            
            for run in range(runs_per_phase):
                print(f"Running {phase} phase, run {run+1}/{runs_per_phase}")
                
                # Create simulator starting at this phase
                simulator = ResonantSalesSimulator(
                    simulation_days=simulation_days,
                    implementation_phase=phase,
                    seed=run
                )
                
                # Run simulation
                sim_results = simulator.run_simulation()
                
                # Extract key metrics
                summary = sim_results["summary"]
                phase_results.append({
                    "run": run,
                    "total_sales": summary["total_sales"],
                    "reference_total_sales": summary["reference_total_sales"],
                    "advantage_percent": summary["advantage_over_reference"] * 100,
                    "final_ta": summary["final_ta"],
                    "final_gladiator": summary["final_gladiator"]
                })
            
            # Calculate average results for this phase
            avg_sales = np.mean([r["total_sales"] for r in phase_results])
            avg_reference = np.mean([r["reference_total_sales"] for r in phase_results])
            avg_advantage = np.mean([r["advantage_percent"] for r in phase_results])
            
            # Store phase results
            results.append({
                "phase": phase,
                "runs": phase_results,
                "avg_sales": avg_sales,
                "avg_reference_sales": avg_reference,
                "avg_advantage_percent": avg_advantage
            })
        
        # Add to experiment results
        self.experiment_results.extend(results)
        return {"results": results}
    
    def visualize_parameter_sweep(self, filename=None):
        """Visualize the results of a parameter sweep experiment."""
        if not self.experiment_results:
            print("No experiment results to visualize.")
            return
            
        # Filter results to only include parameter sweep experiments
        sweep_results = [r for r in self.experiment_results if "config" in r]
        
        if not sweep_results:
            print("No parameter sweep results found.")
            return
        
        # Setup plots
        fig, axs = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle('Resonant Organization Parameter Sweep Results', fontsize=16)
        
        # Extract unique parameter values
        ta_values = sorted(list(set([r["config"]["initial_ta"] for r in sweep_results])))
        gladiator_values = sorted(list(set([r["config"]["initial_gladiator"] for r in sweep_results])))
        volatility_values = sorted(list(set([r["config"]["market_volatility"] for r in sweep_results])))
        
        # Plot 1: Advantage % by Initial Ta and Gladiator Force (averaged across volatility)
        ta_gladiator_data = {}
        for ta in ta_values:
            for gladiator in gladiator_values:
                key = (ta, gladiator)
                matching_results = [r for r in sweep_results 
                                   if r["config"]["initial_ta"] == ta and 
                                   r["config"]["initial_gladiator"] == gladiator]
                
                if matching_results:
                    avg_advantage = np.mean([r["avg_advantage_percent"] for r in matching_results])
                    ta_gladiator_data[key] = avg_advantage
        
        # Create heatmap data
        heatmap_data = np.zeros((len(ta_values), len(gladiator_values)))
        for i, ta in enumerate(ta_values):
            for j, gladiator in enumerate(gladiator_values):
                key = (ta, gladiator)
                if key in ta_gladiator_data:
                    heatmap_data[i, j] = ta_gladiator_data[key]
        
        # Plot heatmap
        im = axs[0, 0].imshow(heatmap_data, cmap='viridis', origin='lower')
        axs[0, 0].set_xticks(np.arange(len(gladiator_values)))
        axs[0, 0].set_yticks(np.arange(len(ta_values)))
        axs[0, 0].set_xticklabels(gladiator_values)
        axs[0, 0].set_yticklabels(ta_values)
        axs[0, 0].set_xlabel('Initial Gladiator Force (Γ)')
        axs[0, 0].set_ylabel('Initial Time-Adherence (Ta)')
        axs[0, 0].set_title('Advantage % by Initial Ta and Γ')
        
        # Add colorbar
        cbar = fig.colorbar(im, ax=axs[0, 0])
        cbar.set_label('Advantage % Over Reference')
        
        # Add text annotations to the heatmap
        for i in range(len(ta_values)):
            for j in range(len(gladiator_values)):
                text = axs[0, 0].text(j, i, f"{heatmap_data[i, j]:.1f}%",
                                    ha="center", va="center", color="w" if heatmap_data[i, j] < 15 else "black")
        
        # Plot 2: Advantage % by Market Volatility
        volatility_data = {}
        for vol in volatility_values:
            matching_results = [r for r in sweep_results if r["config"]["market_volatility"] == vol]
            if matching_results:
                avg_advantage = np.mean([r["avg_advantage_percent"] for r in matching_results])
                volatility_data[vol] = avg_advantage
        
        vols = list(volatility_data.keys())
        advantages = list(volatility_data.values())
        
        axs[0, 1].bar(vols, advantages, color='skyblue')
        axs[0, 1].set_xlabel('Market Volatility')
        axs[0, 1].set_ylabel('Average Advantage %')
        axs[0, 1].set_title('Resonant Team Advantage by Market Volatility')
        
        # Add text labels above bars
        for i, v in enumerate(advantages):
            axs[0, 1].text(i, v + 0.5, f"{v:.1f}%", ha='center')
        
        axs[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Plot 3: Final Ta vs Initial Ta
        initial_ta_values = [r["config"]["initial_ta"] for r in sweep_results]
        final_ta_values = [r["avg_final_ta"] for r in sweep_results]
        
        axs[1, 0].scatter(initial_ta_values, final_ta_values, alpha=0.7)
        
        # Add diagonal line (y=x) for reference
        min_ta = min(min(initial_ta_values), min(final_ta_values))
        max_ta = max(max(initial_ta_values), max(final_ta_values))
        axs[1, 0].plot([min_ta, max_ta], [min_ta, max_ta], 'k--', alpha=0.5)
        
        # Add arrow annotations showing the direction of change
        for init, final in zip(initial_ta_values, final_ta_values):
            if abs(final - init) > 0.05:  # Only show significant changes
                axs[1, 0].annotate("", 
                                  xy=(init, final), 
                                  xytext=(init, init),
                                  arrowprops=dict(arrowstyle="->", lw=1, alpha=0.5,
                                                color='green' if final > init else 'red'))
        
        axs[1, 0].set_xlabel('Initial Time-Adherence (Ta)')
        axs[1, 0].set_ylabel('Final Time-Adherence (Ta)')
        axs[1, 0].set_title('Time-Adherence Evolution')
        axs[1, 0].grid(True, alpha=0.3)
        
        # Plot 4: Final Gladiator vs Initial Gladiator
        initial_g_values = [r["config"]["initial_gladiator"] for r in sweep_results]
        final_g_values = [r["avg_final_gladiator"] for r in sweep_results]
        
        axs[1, 1].scatter(initial_g_values, final_g_values, alpha=0.7)
        
        # Add diagonal line (y=x) for reference
        min_g = min(min(initial_g_values), min(final_g_values))
        max_g = max(max(initial_g_values), max(final_g_values))
        axs[1, 1].plot([min_g, max_g], [min_g, max_g], 'k--', alpha=0.5)
        
        # Add arrow annotations showing the direction of change
        for init, final in zip(initial_g_values, final_g_values):
            if abs(final - init) > 0.05:  # Only show significant changes
                axs[1, 1].annotate("", 
                                  xy=(init, final), 
                                  xytext=(init, init),
                                  arrowprops=dict(arrowstyle="->", lw=1, alpha=0.5,
                                                color='green' if final > init else 'red'))
        
        axs[1, 1].set_xlabel('Initial Gladiator Force (Γ)')
        axs[1, 1].set_ylabel('Final Gladiator Force (Γ)')
        axs[1, 1].set_title('Gladiator Force Evolution')
        axs[1, 1].grid(True, alpha=0.3)
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # Save or show the visualization
        if filename:
            plt.savefig(filename)
            plt.close()
        else:
            plt.show()
    
    def visualize_phase_comparison(self, filename=None):
        """Visualize the results of a phase comparison experiment."""
        # Filter results to only include phase comparison experiments
        phase_results = [r for r in self.experiment_results if "phase" in r]
        
        if not phase_results:
            print("No phase comparison results found.")
            return
            
        # Setup plot
        fig, ax = plt.subplots(figsize=(10, 6))
        fig.suptitle('Resonant Organization Implementation Phase Comparison', fontsize=16)
        
        # Extract data
        phases = [r["phase"].capitalize() for r in phase_results]
        advantages = [r["avg_advantage_percent"] for r in phase_results]
        avg_sales = [r["avg_sales"] for r in phase_results]
        
        # Create bar chart of advantage %
        bars = ax.bar(phases, advantages, color=['#E6B0AA', '#5DADE2', '#7DCEA0'])
        
        # Add text labels above bars
        for i, v in enumerate(advantages):
            ax.text(i, v + 1, f"{v:.1f}%", ha='center')
        
        ax.set_ylabel('Advantage % Over Reference')
        ax.set_title('Performance Advantage by Implementation Phase')
        ax.grid(True, alpha=0.3, axis='y')
        
        # Add second axis for absolute sales
        ax2 = ax.twinx()
        line = ax2.plot(phases, avg_sales, 'r-o', label='Avg. Total Sales')
        ax2.set_ylabel('Total Sales ($)', color='r')
        ax2.tick_params(axis='y', labelcolor='r')
        
        # Add annotation for sales values
        for i, v in enumerate(avg_sales):
            ax2.annotate(f"${v:.0f}", 
                       xy=(i, v),
                       xytext=(i-0.1, v+max(avg_sales)*0.05),
                       color='darkred',
                       fontsize=9)
        
        # Add combined legend
        bars_legend = ax.legend([bars[0]], ['Advantage %'], loc='upper left')
        ax.add_artist(bars_legend)
        ax2.legend(loc='upper right')
        
        # Adjust layout
        plt.tight_layout(rect=[0, 0, 1, 0.95])
        
        # Save or show the visualization
        if filename:
            plt.savefig(filename)
            plt.close()
        else:
            plt.show()

def run_full_resonant_sales_analysis():
    """Run a complete demonstration of the Resonant Sales Framework simulator."""
    print("== Resonant Organization Sales Team Simulator ==")
    print("\nThis simulator demonstrates how organizing sales teams according to the")
    print("Resonant Organization framework affects performance and outcomes.")
    print("\nBased on the Pirouette Framework parameters:")
    print("- Time-Adherence (Ta): Temporal coherence and rhythm of operations")
    print("- Gladiator Force (Γ): Permeability of boundaries and flexibility")
    print("- Ki Constants: Natural frequencies for cyclical operations\n")
    
    # First, run a single detailed simulation
    print("\n1. Running detailed single simulation (90 days)...")
    simulator = ResonantSalesSimulator(simulation_days=90, seed=42)
    results = simulator.run_simulation()
    
    # Display summary metrics
    summary = results["summary"]
    print("\nSimulation Complete:")
    print(f"- Total Sales: ${summary['total_sales']:.2f}")
    print(f"- Reference Sales (non-resonant team): ${summary['reference_total_sales']:.2f}")
    print(f"- Advantage: +{summary['advantage_over_reference']*100:.2f}%")
    print(f"- Final Time-Adherence: {summary['final_ta']:.2f}")
    print(f"- Final Gladiator Force: {summary['final_gladiator']:.2f}")
    
    # Create visualization of the detailed results
    print("\nGenerating detailed visualization...")
    simulator.visualize_results("resonant_sales_simulation.png")
    print("Visualization saved to 'resonant_sales_simulation.png'")
    
    # Run parameter experiments
    print("\n2. Running parameter sensitivity analysis...")
    experiment = ResonantSalesExperiment()
    
    # Simplified parameter sweep for demonstration (fewer runs)
    sweep_results = experiment.run_parameter_sweep(
        initial_ta_values=[0.6, 0.8],
        initial_gladiator_values=[0.3, 0.5],
        market_volatility_values=[0.1, 0.3],
        simulation_days=60,
        runs_per_config=2
    )
    
    # Create visualization of parameter sweep
    print("\nGenerating parameter sweep visualization...")
    experiment.visualize_parameter_sweep("parameter_sweep_results.png")
    print("Visualization saved to 'parameter_sweep_results.png'")
    
    # Run phase comparison
    print("\n3. Running implementation phase comparison...")
    phase_results = experiment.run_phase_comparison(
        simulation_days=60,
        runs_per_phase=3
    )
    
    # Create visualization of phase comparison
    print("\nGenerating phase comparison visualization...")
    experiment.visualize_phase_comparison("phase_comparison_results.png")
    print("Visualization saved to 'phase_comparison_results.png'")
    
    print("\nAnalysis complete!")
    print("The simulations demonstrate how a sales team organized according to")
    print("Resonant Organization principles can achieve significantly better results")
    print("through properly balanced Time-Adherence and Gladiator Force parameters,")
    print("aligned with natural Ki-resonant cycles.")

# Run the simulation if executed directly
if __name__ == "__main__":
    run_full_resonant_sales_analysis()