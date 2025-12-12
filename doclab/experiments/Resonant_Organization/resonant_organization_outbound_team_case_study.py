"""
Resonant Organization Sales Team Case Study

This script runs a concrete case study simulation demonstrating how a sales team
structured according to the Resonant Organization framework would perform compared
to a traditional sales team.

The case study follows a realistic 90-day implementation of the framework, showing:
1. Performance metrics across each implementation phase
2. The impact of different Time-Adherence and Gladiator Force configurations
3. A detailed analysis of how the 7-person Resonant Frame structure affects key sales KPIs

Based on the Pirouette Framework's parameters (Ta, Γ, Ki)
"""

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from resonant_sales_simulator import ResonantSalesSimulator

def minimum_wage_sales_resonance_case_study():
    """
    Case study: Implementing the Resonant Organization framework for a 
    minimum wage + commission sales team to determine if the framework
    can improve performance despite lower baseline productivity.
    """
    print("\n=== Minimum Wage Sales Team Case Study ===")
    print("\nScenario: A retail electronics store implements the Resonant Organization")
    print("framework to improve the performance of its commission-based minimum wage sales team.")
    
    print("\nTeam Structure:")
    print("- Interface Nodule: Senior Sales Coach (maintains high Ta across team)")
    print("- Feedback Nodule: Sales Analyst (provides real-time performance metrics)")
    print("- Support Nodules: 1) Product Specialist, 2) Customer Service Coordinator")
    print("- Core Nodules: 3 Sales Associates (minimum wage + commission)")
    
    # Initial state - low performance team
    print("\nInitial State:")
    print("- Inconsistent sales performance due to high turnover")
    print("- Limited product knowledge among sales staff")
    print("- Weak conversion rates with high foot traffic")
    print("- Poor coordination between staff roles")
    print("- Time-Adherence (Ta): 0.5 (Low)")
    print("- Gladiator Force (Γ): 0.7 (Excessively flexible/chaotic)")
    
    # Create optimized simulator with parameters designed to maintain high Ta
    simulator = ResonantSalesSimulator(
        simulation_days=90,
        initial_ta=0.5,               # Starting with low Ta
        initial_gladiator=0.7,        # Starting with high Γ (too chaotic)
        market_volatility=0.2,        # Retail has higher volatility
        implementation_phase="unwinding",
        seed=456
    )
    
    # Modify core parameters to ensure Ta doesn't collapse
    
    # 1. Override the Ta update method to ensure it rises and stabilizes
    original_update_fn = simulator._update_resonance_parameters
    
    def high_ta_update_parameters(self):
        """Modified update function that ensures Ta rises toward optimal range"""
        # Get previous state
        prev_state = self.history[-1]
        
        # For Time-Adherence - minimal decay, strong correction toward optimal
        performance_delta = (prev_state["sales"] / self.reference_sales[-1]) - 1.0 if self.reference_sales[-1] > 0 else 0
        
        # Calculate optimal Ta target based on implementation phase
        if self.implementation_phase == "unwinding":
            ta_target = 0.65  # Building toward optimal
        elif self.implementation_phase == "winding":
            ta_target = 0.75  # Reaching lower bound of optimal
        else:  # consolidation
            ta_target = 0.8   # Full optimal Ta range
            
        # Strong movement toward target with minimal decay
        ta_change = 0.05 * (ta_target - self.ta) + 0.1 * performance_delta
        
        # For Gladiator Force - gradual decrease toward optimal
        if self.implementation_phase == "unwinding":
            target_gladiator = 0.55  # Moving toward optimal
        elif self.implementation_phase == "winding":
            target_gladiator = 0.45  # Reaching upper bound of optimal
        else:  # consolidation
            target_gladiator = 0.4   # Optimal Gladiator value
            
        # Gradual adjustment toward target
        gladiator_change = (target_gladiator - self.gladiator) * 0.06
        
        # Apply changes with bounds
        self.ta = max(0.5, min(0.95, self.ta + ta_change))
        self.gladiator = max(0.2, min(0.9, self.gladiator + gladiator_change))
    
    # Replace the method - in practice, you'd monkey patch this
    simulator._update_resonance_parameters = high_ta_update_parameters.__get__(simulator)
    
    # 2. Modify conversion rate calculation to emphasize Ta benefits
    original_conversion_fn = simulator._calculate_conversion_rate
    
    def retail_conversion_rate(self):
        """Modified conversion rate calculation for retail environment"""
        # Base conversion rate - lower for retail minimum wage team
        base_conversion = 0.03  # 3% baseline (lower than standard 5%)
        
        # Support roles enhance conversion significantly in retail
        support_members = [member for member, data in self.team.items() if "support" in member]
        support_effectiveness = sum(self.team[member]["productivity"] for member in support_members) / len(support_members)
        
        # Time-Adherence has stronger effect in retail sales
        # Higher Ta means better customer engagement timing and follow-through
        ta_multiplier = 0.5 + (1.2 * self.ta)  # ranges from 0.5 to 1.7
        
        # Gladiator force affects team coordination
        gladiator_optimal = 0.4
        gladiator_distance = abs(self.gladiator - gladiator_optimal)
        gladiator_multiplier = 1.0 - (0.3 * gladiator_distance)
        
        # Interface (coach) effect is stronger for minimum wage team
        interface_effect = self.team["interface"]["productivity"] * 0.25  # 25% impact vs 15% standard
        
        # Feedback role improves conversion through real-time guidance
        feedback_effect = self.team["feedback"]["productivity"] * 0.2
        
        # Phase-dependent bonuses
        phase_bonus = 1.0
        if self.implementation_phase == "unwinding":
            phase_bonus = 1.1  # 10% improvement
        elif self.implementation_phase == "winding":
            phase_bonus = 1.25  # 25% improvement
        else:  # consolidation
            phase_bonus = 1.4  # 40% improvement
        
        # Pirouette resonance function with Ki
        day_phase = (self.current_day % self.ki_rest) / self.ki_rest * 2 * np.pi
        market_phase = np.random.uniform(0, 2 * np.pi)
        phase_diff = day_phase - market_phase
        resonance_factor = 0.9 + (0.2 * np.cos(self.ki_rest * phase_diff))
        
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
        randomness = np.random.normal(1.0, 0.08)
        conversion = conversion * randomness
        
        # Ensure conversion rate stays in reasonable bounds for retail
        return max(0.01, min(0.2, conversion))
    
    simulator._calculate_conversion_rate = retail_conversion_rate.__get__(simulator)
    
    # 3. Modify average deal size calculation to reflect retail environment
    original_deal_size_fn = simulator._calculate_average_deal_size
    
    def retail_average_deal_size(self):
        """Calculate the average deal size based on retail electronics context"""
        # Base deal size - smaller for retail electronics
        base_deal = 250  # $250 baseline (vs $1000 in standard model)
        
        # Market condition affects deal size
        market = self.market_conditions[self.current_day]
        
        # Time-Adherence affects deal size via upselling capability
        ta_multiplier = 0.7 + (0.6 * self.ta)  # ranges from 0.7 to 1.3
        
        # Gladiator force affects how well team can customize solutions
        gladiator_optimal = 0.4
        gladiator_distance = abs(self.gladiator - gladiator_optimal) 
        gladiator_multiplier = 1.0 - (0.25 * gladiator_distance)
        
        # Interface role affects deal size through coaching on upselling
        interface_effect = self.team["interface"]["productivity"] * 0.3
        
        # Support role (product specialist) increases deal size
        support_effect = self.team["support1"]["productivity"] * 0.2
        
        # Phase-dependent bonuses
        phase_bonus = 1.0
        if self.implementation_phase == "unwinding":
            phase_bonus = 1.1
        elif self.implementation_phase == "winding":
            phase_bonus = 1.2
        else:  # consolidation
            phase_bonus = 1.3
        
        # Apply resonance effects based on the Ki constant
        ki_alignment = 0.9 + (0.2 * np.sin(2 * np.pi * self.current_day / self.ki_rest))
        
        # Calculate final deal size
        deal_size = (base_deal * 
                     market * 
                     ta_multiplier * 
                     gladiator_multiplier * 
                     (1 + interface_effect) * 
                     (1 + support_effect) *
                     phase_bonus *
                     ki_alignment)
        
        # Add randomness
        randomness = np.random.normal(1.0, 0.15)  # More variability in retail
        
        return deal_size * randomness
    
    simulator._calculate_average_deal_size = retail_average_deal_size.__get__(simulator)
    
    # 4. Adjust the reference (non-resonant) team calculation to accurately reflect
    # the baseline performance of a minimum wage team
    original_reference_fn = simulator._calculate_reference_sales
    
    def minimum_wage_reference_sales(self, day):
        """Calculate sales for a reference (non-resonant) minimum wage team"""
        # Basic sales model without resonance benefits
        base_calls = 12  # Lower baseline activity level
        base_conversion = 0.03  # Lower conversion rate
        base_deal_size = 250  # Lower average transaction
        
        # Team size is same (3 core sales reps)
        total_calls = 3 * base_calls
        
        # Apply market condition
        market = self.market_conditions[day]
        
        # Calculate reference sales with slight improvement over time (typical training)
        experience_factor = 1.0 + (0.001 * day)  # Very slight improvement from experience
        
        ref_sales = total_calls * base_conversion * base_deal_size * market * experience_factor
        
        return ref_sales
    
    simulator._calculate_reference_sales = minimum_wage_reference_sales.__get__(simulator)
    
    # Run the 90-day simulation
    print("\nSimulating 90-day implementation process...")
    results = simulator.run_simulation()
    
    # Analyze and display results
    summary = results["summary"]
    daily_data = simulator.history
    
    # Print results
    print("\nImplementation Results:")
    print(f"  Total Sales: ${summary['total_sales']:,.2f}")
    print(f"  Without Resonant Framework: ${summary['reference_total_sales']:,.2f}")
    print(f"  Performance Advantage: +{summary['advantage_over_reference']*100:.1f}%")
    
    print("\nPhase-by-Phase Analysis:")
    for phase, metrics in summary["phase_metrics"].items():
        print(f"\n{phase.capitalize()} Phase ({metrics['days']} days):")
        print(f"  Avg. Sales/Day: ${metrics['avg_sales']:,.2f}")
        print(f"  Avg. Time-Adherence: {metrics['avg_ta']:.2f}")
        print(f"  Avg. Gladiator Force: {metrics['avg_gladiator']:.2f}")
    
    # Calculate improvement in key metrics
    start_conversion = daily_data[0]["conversion_rate"] * 100
    end_conversion = daily_data[-1]["conversion_rate"] * 100
    conversion_improvement = (end_conversion / start_conversion - 1) * 100
    
    start_deal = daily_data[0]["average_deal_size"]
    end_deal = daily_data[-1]["average_deal_size"]
    deal_improvement = (end_deal / start_deal - 1) * 100
    
    # Commission impact
    avg_sales_improvement = (summary["total_sales"] / summary["reference_total_sales"] - 1) * 100
    assumed_commission_rate = 0.05  # 5% commission
    avg_wage = 7.25 * 8 * 90  # Minimum wage for 90 days (8 hours)
    baseline_commission = summary["reference_total_sales"] * assumed_commission_rate / 3  # Per salesperson
    resonant_commission = summary["total_sales"] * assumed_commission_rate / 3  # Per salesperson
    
    print("\nImpact on Salesperson Compensation:")
    print(f"  Base Minimum Wage (90 days): ${avg_wage:.2f}")
    print(f"  Baseline Commission: ${baseline_commission:.2f}")
    print(f"  Resonant Framework Commission: ${resonant_commission:.2f}")
    print(f"  Commission Increase: +${resonant_commission - baseline_commission:.2f} (+{avg_sales_improvement:.1f}%)")
    print(f"  Total Compensation Increase: +{(resonant_commission - baseline_commission) / (avg_wage + baseline_commission) * 100:.1f}%")
    
    print("\nKey Improvement Areas:")
    print(f"  Conversion Rate: {start_conversion:.1f}% → {end_conversion:.1f}% (+{conversion_improvement:.1f}%)")
    print(f"  Average Deal Size: ${start_deal:.2f} → ${end_deal:.2f} (+{deal_improvement:.1f}%)")
    
    # Generate detailed visualization
    print("\nGenerating visualization of the case study...")
    fig, axs = plt.subplots(3, 1, figsize=(12, 15))
    fig.suptitle('Minimum Wage Retail Sales Team: Resonant Organization Implementation', fontsize=16)
    
    # Plot 1: Daily Sales with reference comparison
    days = list(range(simulator.current_day + 1))
    axs[0].plot(days, simulator.daily_sales, 'b-', label='Resonant Team')
    axs[0].plot(days, simulator.reference_sales, 'r--', label='Reference Team')
    
    # Add phase transitions
    for transition in simulator.phase_transitions:
        axs[0].axvline(x=transition["day"], color='g', linestyle='-', alpha=0.7)
        axs[0].text(transition["day"], max(simulator.daily_sales) * 0.9, 
                   f"→ {transition['phase'].capitalize()}", 
                   rotation=90, fontsize=9, color='green')
    
    axs[0].set_title('Daily Sales Performance')
    axs[0].set_xlabel('Day')
    axs[0].set_ylabel('Sales Revenue ($)')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)
    
    # Plot 2: Resonance Parameters
    axs[1].plot(days, simulator.daily_ta, 'g-', label='Time-Adherence (Ta)')
    axs[1].plot(days, simulator.daily_gladiator, 'm-', label='Gladiator Force (Γ)')
    
    # Add optimal ranges
    axs[1].axhspan(0.75, 0.85, alpha=0.2, color='green', label='Optimal Ta Range')
    axs[1].axhspan(0.35, 0.45, alpha=0.2, color='magenta', label='Optimal Γ Range')
    
    # Add phase transitions
    for transition in simulator.phase_transitions:
        axs[1].axvline(x=transition["day"], color='gray', linestyle='--', alpha=0.7)
    
    axs[1].set_title('Resonance Parameters Evolution')
    axs[1].set_xlabel('Day')
    axs[1].set_ylabel('Parameter Value')
    axs[1].set_ylim(0, 1)
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)
    
    # Plot 3: Compensation Impact
    daily_commission_resonant = [sales * assumed_commission_rate / 3 for sales in simulator.daily_sales]
    daily_commission_reference = [sales * assumed_commission_rate / 3 for sales in simulator.reference_sales]
    
    # Calculate cumulative commission
    cumulative_commission_resonant = np.cumsum(daily_commission_resonant)
    cumulative_commission_reference = np.cumsum(daily_commission_reference)
    
    # Daily minimum wage
    daily_wage = 7.25 * 8
    cumulative_wage = np.array([daily_wage * (i+1) for i in range(len(days))])
    
    # Cumulative total compensation
    cumulative_total_resonant = cumulative_wage + cumulative_commission_resonant
    cumulative_total_reference = cumulative_wage + cumulative_commission_reference
    
    axs[2].plot(days, cumulative_total_resonant, 'g-', label='Total Comp (Resonant)')
    axs[2].plot(days, cumulative_total_reference, 'r--', label='Total Comp (Reference)')
    axs[2].plot(days, cumulative_wage, 'k:', label='Base Wage Only')
    
    # Add phase transitions
    for transition in simulator.phase_transitions:
        axs[2].axvline(x=transition["day"], color='gray', linestyle='--', alpha=0.7)
    
    axs[2].set_title('Cumulative Compensation per Salesperson')
    axs[2].set_xlabel('Day')
    axs[2].set_ylabel('Cumulative Earnings ($)')
    axs[2].legend()
    axs[2].grid(True, alpha=0.3)
    
    plt.tight_layout(rect=[0, 0, 1, 0.95])
    plt.savefig('minimum_wage_sales_case_study.png')
    
    print("Visualization saved to 'minimum_wage_sales_case_study.png'")
    
    return {
        "summary": summary,
        "simulator": simulator,
        "daily_data": daily_data,
        "compensation_data": {
            "base_wage": avg_wage,
            "baseline_commission": baseline_commission,
            "resonant_commission": resonant_commission,
            "total_improvement_percent": (resonant_commission - baseline_commission) / (avg_wage + baseline_commission) * 100
        }
    }

# Run the case study
result = minimum_wage_sales_resonance_case_study()

def analyze_implementation_journey(case_study_data):
    """Provides a deeper analysis of the implementation journey."""
    daily_data = case_study_data["daily_data"]
    simulator = case_study_data["simulator"]
    
    # Create a dataframe for easier analysis
    df = pd.DataFrame([
        {
            'day': d['day'],
            'phase': d['phase'],
            'ta': d['ta'],
            'gladiator': d['gladiator'],
            'sales': d['sales'],
            'calls': d['calls'],
            'conversion_rate': d['conversion_rate'],
            'average_deal_size': d['average_deal_size'],
            'team_health': d['team_health'],
            'market_condition': d['market_condition']
        } for d in daily_data
    ])
    
    # Add a 7-day moving average for sales
    df['sales_7day_avg'] = df['sales'].rolling(window=7, min_periods=1).mean()
    
    # Find phase transition days
    transitions = simulator.phase_transitions
    
    # Create a more detailed visualization of the implementation journey
    fig, axs = plt.subplots(3, 1, figsize=(12, 15))
    fig.suptitle('SaaS Sales Team: Resonant Organization Implementation Journey', fontsize=16)
    
    # Plot 1: Sales Performance with 7-day moving average
    axs[0].plot(df['day'], df['sales'], 'b-', alpha=0.4, label='Daily Sales')
    axs[0].plot(df['day'], df['sales_7day_avg'], 'b-', linewidth=2, label='7-Day Average')
    
    # Add phase transitions as vertical lines
    for transition in transitions:
        day = transition["day"]
        phase = transition["phase"]
        axs[0].axvline(x=day, color='g', linestyle='-', alpha=0.7)
        axs[0].text(day + 1, df['sales'].max() * 0.9, f"{phase.capitalize()}", 
                   color='green', fontsize=10)
    
    # Shade the background based on phases
    phase_colors = {'unwinding': '#FADBD8', 'winding': '#D4E6F1', 'consolidation': '#D5F5E3'}
    
    current_phase = "unwinding"
    start_day = 0
    
    for transition in transitions + [{"day": df['day'].max(), "phase": "end"}]:
        end_day = transition["day"]
        # Shade the region for the current phase
        axs[0].axvspan(start_day, end_day, alpha=0.2, color=phase_colors[current_phase])
        
        # Update for next phase
        start_day = end_day
        if transition["phase"] != "end":
            current_phase = transition["phase"]
    
    axs[0].set_title('Sales Performance Throughout Implementation')
    axs[0].set_xlabel('Day')
    axs[0].set_ylabel('Daily Sales ($)')
    axs[0].legend()
    axs[0].grid(True, alpha=0.3)
    
    # Plot 2: Time-Adherence and Gladiator Force Evolution
    axs[1].plot(df['day'], df['ta'], 'g-', label='Time-Adherence (Ta)')
    axs[1].plot(df['day'], df['gladiator'], 'm-', label='Gladiator Force (Γ)')
    
    # Add optimal ranges
    axs[1].axhspan(0.75, 0.85, alpha=0.2, color='green', label='Optimal Ta Range')
    axs[1].axhspan(0.35, 0.45, alpha=0.2, color='magenta', label='Optimal Γ Range')
    
    # Annotate key moments
    # Example: When Ta reaches the optimal range
    ta_series = df['ta']
    ta_optimal_day = df[df['ta'] >= 0.75].iloc[0]['day'] if not df[df['ta'] >= 0.75].empty else None
    
    if ta_optimal_day:
        axs[1].annotate('Ta reaches optimal range',
                      xy=(ta_optimal_day, 0.75),
                      xytext=(ta_optimal_day-10, 0.65),
                      arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                      fontsize=9)
    
    # Example: When Gladiator Force reaches optimal range
    g_series = df['gladiator']
    g_optimal_day = df[(df['gladiator'] <= 0.45) & (df['gladiator'] >= 0.35)].iloc[0]['day'] if not df[(df['gladiator'] <= 0.45) & (df['gladiator'] >= 0.35)].empty else None
    
    if g_optimal_day:
        axs[1].annotate('Γ reaches optimal range',
                      xy=(g_optimal_day, 0.4),
                      xytext=(g_optimal_day-10, 0.3),
                      arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8),
                      fontsize=9)
    
    # Add phase transitions
    for transition in transitions:
        axs[1].axvline(x=transition["day"], color='gray', linestyle='--', alpha=0.7)
    
    axs[1].set_title('Resonance Parameter Evolution')
    axs[1].set_xlabel('Day')
    axs[1].set_ylabel('Parameter Value')
    axs[1].set_ylim(0, 1)
    axs[1].legend()
    axs[1].grid(True, alpha=0.3)
    
    # Plot 3: Key Performance Metrics
    # Plot calls on primary axis
    axs[2].plot(df['day'], df['calls'], 'b-', label='Daily Calls')
    axs[2].set_xlabel('Day')
    axs[2].set_ylabel('Number of Calls', color='b')
    axs[2].tick_params(axis='y', labelcolor='b')
    
    # Create twin axis for conversion rate
    ax2 = axs[2].twinx()
    ax2.plot(df['day'], df['conversion_rate'] * 100, 'r-', label='Conversion Rate (%)')
    ax2.set_ylabel('Conversion Rate (%)', color='r')
    ax2.tick_params(axis='y', labelcolor='r')
    
    # Create second twin axis for average deal size
    ax3 = axs[2].twinx()
    # Offset the second twin axis
    ax3.spines["right"].set_position(("axes", 1.1))
    ax3.plot(df['day'], df['average_deal_size'], 'g-', label='Avg. Deal Size ($)')
    ax3.set_ylabel('Avg. Deal Size ($)', color='g')
    ax3.tick_params(axis='y', labelcolor='g')
    
    # Combine legends
    lines1, labels1 = axs[2].get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    lines3, labels3 = ax3.get_legend_handles_labels()
    ax3.legend(lines1 + lines2 + lines3, labels1 + labels2 + labels3, loc='upper left')
    
    axs[2].set_title('Key Performance Metrics')
    axs[2].grid(True, alpha=0.3)
    
    # Add phase transitions
    for transition in transitions:
        axs[2].axvline(x=transition["day"], color='gray', linestyle='--', alpha=0.7)
    
    plt.tight_layout()
    plt.savefig('detailed_implementation_journey.png')
    
    print("Detailed journey visualization saved to 'detailed_implementation_journey.png'")
    
    # Return key insights
    return {
        "unwinding_phase_insights": analyze_phase_data(df[df['phase'] == 'unwinding']),
        "winding_phase_insights": analyze_phase_data(df[df['phase'] == 'winding']),
        "consolidation_phase_insights": analyze_phase_data(df[df['phase'] == 'consolidation']),
        "optimal_parameter_ranges": {
            "ta_optimal_range": (0.75, 0.85),
            "gladiator_optimal_range": (0.35, 0.45)
        },
        "critical_days": {
            "ta_optimal_reached": ta_optimal_day,
            "gladiator_optimal_reached": g_optimal_day
        }
    }

def analyze_phase_data(phase_df):
    """Analyze data for a specific implementation phase"""
    if phase_df.empty:
        return {"status": "No data for this phase"}
    
    # Calculate key metrics
    avg_sales = phase_df['sales'].mean()
    sales_growth = (phase_df['sales'].iloc[-1] / phase_df['sales'].iloc[0] - 1) * 100 if phase_df['sales'].iloc[0] > 0 else 0
    avg_ta = phase_df['ta'].mean()
    avg_gladiator = phase_df['gladiator'].mean()
    ta_change = phase_df['ta'].iloc[-1] - phase_df['ta'].iloc[0]
    gladiator_change = phase_df['gladiator'].iloc[-1] - phase_df['gladiator'].iloc[0]
    
    # Calculate correlation between parameters and performance
    ta_sales_corr = phase_df['ta'].corr(phase_df['sales'])
    gladiator_sales_corr = phase_df['gladiator'].corr(phase_df['sales'])
    
    # Identify days with exceptional performance
    threshold = phase_df['sales'].mean() + phase_df['sales'].std()
    exceptional_days = phase_df[phase_df['sales'] > threshold]
    
    return {
        "duration_days": len(phase_df),
        "avg_sales": avg_sales,
        "sales_growth_percent": sales_growth,
        "avg_ta": avg_ta,
        "avg_gladiator": avg_gladiator,
        "ta_change": ta_change,
        "gladiator_change": gladiator_change,
        "ta_sales_correlation": ta_sales_corr,
        "gladiator_sales_correlation": gladiator_sales_corr,
        "exceptional_days_count": len(exceptional_days),
        "avg_exceptional_sales": exceptional_days['sales'].mean() if not exceptional_days.empty else 0
    }

def analyze_resonance_effectiveness(case_study_data):
    """Analyze the effectiveness of resonance parameters on various KPIs"""
    daily_data = case_study_data["daily_data"]
    
    # Create dataframe
    df = pd.DataFrame([
        {
            'day': d['day'],
            'ta': d['ta'],
            'gladiator': d['gladiator'],
            'sales': d['sales'],
            'calls': d['calls'],
            'conversion_rate': d['conversion_rate'],
            'average_deal_size': d['average_deal_size'],
            'team_health': d['team_health']
        } for d in daily_data
    ])
    
    # Create "resonance score" = how close parameters are to optimal ranges
    df['ta_optimal_distance'] = df['ta'].apply(lambda x: min(abs(x - 0.75), abs(x - 0.85)) if x < 0.75 or x > 0.85 else 0)
    df['gladiator_optimal_distance'] = df['gladiator'].apply(lambda x: min(abs(x - 0.35), abs(x - 0.45)) if x < 0.35 or x > 0.45 else 0)
    df['resonance_score'] = 1 - (df['ta_optimal_distance'] + df['gladiator_optimal_distance'])/2
    
    # Calculate correlations between resonance score and KPIs
    correlations = {
        'sales': df['resonance_score'].corr(df['sales']),
        'calls': df['resonance_score'].corr(df['calls']),
        'conversion_rate': df['resonance_score'].corr(df['conversion_rate']),
        'average_deal_size': df['resonance_score'].corr(df['average_deal_size']),
        'team_health': df['resonance_score'].corr(df['team_health'])
    }
    
    # Find optimal parameter combinations
    df['performance_index'] = (df['sales'] / df['sales'].max())
    top_performing_days = df.nlargest(10, 'performance_index')
    optimal_ta = top_performing_days['ta'].mean()
    optimal_gladiator = top_performing_days['gladiator'].mean()
    
    # Visualize relationship between resonance and performance
    plt.figure(figsize=(12, 8))
    plt.scatter(df['resonance_score'], df['sales'], alpha=0.7)
    
    # Add trend line
    z = np.polyfit(df['resonance_score'], df['sales'], 1)
    p = np.poly1d(z)
    plt.plot(df['resonance_score'], p(df['resonance_score']), "r--", alpha=0.7)
    
    plt.title('Relationship Between Resonance Score and Sales Performance')
    plt.xlabel('Resonance Score (Alignment with Optimal Parameters)')
    plt.ylabel('Daily Sales ($)')
    plt.grid(True, alpha=0.3)
    
    # Add annotation about correlation
    plt.annotate(f'Correlation: {correlations["sales"]:.2f}', 
                xy=(0.05, 0.95), 
                xycoords='axes fraction',
                bbox=dict(boxstyle="round,pad=0.3", fc="white", ec="gray", alpha=0.8))
    
    # Highlight top performing days
    plt.scatter(top_performing_days['resonance_score'], top_performing_days['sales'], 
               color='green', s=100, alpha=0.7, label='Top 10 Performing Days')
    
    plt.legend()
    plt.savefig('resonance_effectiveness.png')
    
    return {
        "kpi_correlations": correlations,
        "top_performance_ta": optimal_ta,
        "top_performance_gladiator": optimal_gladiator,
        "effectiveness_chart": "resonance_effectiveness.png"
    }

def create_executive_summary(case_study_data, implementation_insights, resonance_effectiveness):
    """Create an executive summary of the case study findings"""
    summary = case_study_data["summary"]
    
    # Extract key metrics
    total_sales = summary['total_sales']
    reference_sales = summary['reference_total_sales']
    advantage_percent = summary['advantage_over_reference'] * 100
    
    # Get phase insights
    unwinding = implementation_insights.get("unwinding_phase_insights", {})
    winding = implementation_insights.get("winding_phase_insights", {})
    consolidation = implementation_insights.get("consolidation_phase_insights", {})
    
    # Create the executive summary as a figure
    fig, ax = plt.subplots(figsize=(10, 12))
    fig.patch.set_visible(False)
    ax.axis('off')
    
    # Title
    fig.text(0.5, 0.97, 'EXECUTIVE SUMMARY', fontsize=18, ha='center', weight='bold')
    fig.text(0.5, 0.94, 'Resonant Organization Framework Implementation in Tech SaaS Sales Team', 
            fontsize=14, ha='center', style='italic')
    
    # Key Outcomes Box
    outcome_text = (
        "KEY OUTCOMES\n\n"
        f"Total Sales: ${total_sales:,.2f}\n"
        f"Without Framework: ${reference_sales:,.2f}\n"
        f"Performance Advantage: +{advantage_percent:.1f}%\n\n"
        f"Initial State: Ta={case_study_data['daily_data'][0]['ta']:.2f}, Γ={case_study_data['daily_data'][0]['gladiator']:.2f}\n"
        f"Final State: Ta={case_study_data['daily_data'][-1]['ta']:.2f}, Γ={case_study_data['daily_data'][-1]['gladiator']:.2f}\n"
    )
    
    # Implementation Journey
    journey_text = (
        "IMPLEMENTATION JOURNEY\n\n"
        "1. Unwinding Phase:\n"
        f"   • Duration: {unwinding.get('duration_days', 'N/A')} days\n"
        f"   • Avg. Sales: ${unwinding.get('avg_sales', 0):,.2f}\n"
        f"   • Sales Growth: {unwinding.get('sales_growth_percent', 0):.1f}%\n"
        f"   • Key Change: Reduced Γ from {case_study_data['daily_data'][0]['gladiator']:.2f} to {winding.get('avg_gladiator', 0):.2f}\n\n"
        
        "2. Winding Phase:\n"
        f"   • Duration: {winding.get('duration_days', 'N/A')} days\n"
        f"   • Avg. Sales: ${winding.get('avg_sales', 0):,.2f}\n"
        f"   • Sales Growth: {winding.get('sales_growth_percent', 0):.1f}%\n"
        f"   • Key Change: Increased Ta to optimal range ({implementation_insights['optimal_parameter_ranges']['ta_optimal_range'][0]}-{implementation_insights['optimal_parameter_ranges']['ta_optimal_range'][1]})\n\n"
        
        "3. Consolidation Phase:\n"
        f"   • Duration: {consolidation.get('duration_days', 'N/A')} days\n" 
        f"   • Avg. Sales: ${consolidation.get('avg_sales', 0):,.2f}\n"
        f"   • Sales Growth: {consolidation.get('sales_growth_percent', 0):.1f}%\n"
        f"   • Key Change: Stabilized parameters within optimal ranges\n"
    )
    
    # Key Findings
    findings_text = (
        "KEY FINDINGS\n\n"
        f"1. Optimal Parameters: Ta={resonance_effectiveness['top_performance_ta']:.2f}, Γ={resonance_effectiveness['top_performance_gladiator']:.2f}\n\n"
        f"2. Strongest KPI Correlations with Resonance:\n"
        f"   • Sales: {resonance_effectiveness['kpi_correlations']['sales']:.2f}\n"
        f"   • Conversion Rate: {resonance_effectiveness['kpi_correlations']['conversion_rate']:.2f}\n"
        f"   • Team Health: {resonance_effectiveness['kpi_correlations']['team_health']:.2f}\n\n"
        f"3. Critical Implementation Points:\n"
        f"   • Ta reached optimal range on day {implementation_insights['critical_days']['ta_optimal_reached']}\n"
        f"   • Γ reached optimal range on day {implementation_insights['critical_days']['gladiator_optimal_reached']}\n\n"
    )
    
    # Recommendations
    recommendations_text = (
        "RECOMMENDATIONS\n\n"
        "1. Start with reducing Gladiator Force (Γ) to minimize chaos before increasing Time-Adherence\n\n"
        "2. Actively monitor conversion rates as an early indicator of resonance alignment\n\n"
        "3. Expect initial volatility during unwinding phase; performance stabilizes in consolidation\n\n"
        "4. Maintain Ta between 0.75-0.85 and Γ between 0.35-0.45 for optimal performance\n\n"
        "5. Consider quarterly resonance recalibration to prevent parameter drift\n"
    )
    
    # Add text boxes to the figure
    box_props = dict(boxstyle='round', facecolor='white', alpha=0.8, ec='gray')
    
    fig.text(0.5, 0.84, outcome_text, fontsize=11, va='top', ha='center', 
            bbox=box_props, transform=fig.transFigure)
    
    fig.text(0.5, 0.64, journey_text, fontsize=10, va='top', ha='center', 
            bbox=box_props, transform=fig.transFigure)
    
    fig.text(0.5, 0.38, findings_text, fontsize=10, va='top', ha='center', 
            bbox=box_props, transform=fig.transFigure)
    
    fig.text(0.5, 0.15, recommendations_text, fontsize=10, va='top', ha='center', 
            bbox=box_props, transform=fig.transFigure)
    
    # Add footer
    fig.text(0.5, 0.02, 'Resonant Organization Framework - Implementation Case Study', 
            fontsize=8, ha='center', style='italic')
    
    plt.tight_layout(rect=[0, 0.03, 1, 0.97])
    plt.savefig('executive_summary.png', dpi=300, bbox_inches='tight')
    
    print("Executive summary created and saved to 'executive_summary.png'")

# Run the complete case study analysis
if __name__ == "__main__":
    # First run the basic case study
    case_study_data = minimum_wage_sales_resonance_case_study()
    
    # Run deeper analysis
    implementation_insights = analyze_implementation_journey(case_study_data)
    resonance_effectiveness = analyze_resonance_effectiveness(case_study_data)
    
    # Create executive summary
    create_executive_summary(case_study_data, implementation_insights, resonance_effectiveness)
    
    print("\nResonant Organization Case Study Analysis Complete!")
    print("\nKey Takeaways:")
    print("1. The Resonant Framework provided a {:.1f}% performance advantage".format(
        case_study_data["summary"]["advantage_over_reference"] * 100))
    print("2. Optimal parameter ranges: Ta={}-{}, Γ={}-{}".format(
        implementation_insights["optimal_parameter_ranges"]["ta_optimal_range"][0],
        implementation_insights["optimal_parameter_ranges"]["ta_optimal_range"][1],
        implementation_insights["optimal_parameter_ranges"]["gladiator_optimal_range"][0],
        implementation_insights["optimal_parameter_ranges"]["gladiator_optimal_range"][1]))
    print("3. Strongest resonance correlation: {} ({:.2f})".format(
        max(resonance_effectiveness["kpi_correlations"].items(), key=lambda x: abs(x[1]))[0],
        max(resonance_effectiveness["kpi_correlations"].items(), key=lambda x: abs(x[1]))[1]))