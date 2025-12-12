import numpy as np
import matplotlib.pyplot as plt
from matplotlib.collections import LineCollection
from matplotlib.colors import LinearSegmentedColormap
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
logger = logging.getLogger("HEARTBEAT_REACTOR_V3")

class HeartbeatReactorV3:
    def __init__(self, cycles=15):
        self.cycles = cycles
        self.dt = 0.005 # Reasonable timestep
        
        # --- REACTOR GEOMETRY ---
        self.r_intake = 8.0    
        self.r_singularity = 0.1 
        self.r_exhaust = 24.0  
        
        # --- PHYSICS ---
        self.friction_proton = 0.05 
        self.pressure_muon = 0.12 
        self.coupling_efficiency = 0.95 
        
        # --- SAFETY LIMITS ---
        self.max_velocity = 50.0 # Speed of Light limit (prevents tunneling)
        
    def gradient(self, m, l):
        # Standard Hénon-Heiles
        dm = m + 2 * m * l
        dl = l + m**2 - l**2
        return dm, dl

    def run_cycle(self):
        logger.info(f"[-] INITIALIZING HEARTBEAT PROTOCOL V3 ({self.cycles} Cycles)...")
        
        t_hist, r_hist, e_hist, p_hist = [], [], [], []
        harvest_log = []
        
        # Initial State
        theta = 0.0
        m = self.r_intake * np.cos(theta)
        l = self.r_intake * np.sin(theta)
        
        vm = -0.5 * np.cos(theta) - 1.0 * np.sin(theta)
        vl = -0.5 * np.sin(theta) + 1.0 * np.cos(theta)
        
        phase = "PROTON"
        cycle_count = 0
        total_steps = 0
        max_steps = 500000 
        
        while cycle_count < self.cycles and total_steps < max_steps:
            # 1. METRICS & LOGGING
            r_sq = m**2 + l**2
            r = np.sqrt(r_sq)
            v_sq = vm**2 + vl**2
            ke = 0.5 * v_sq
            
            if total_steps % 10 == 0:
                t_hist.append(total_steps * self.dt)
                r_hist.append(r)
                e_hist.append(ke)
                p_hist.append(0 if phase == "PROTON" else 1)
            
            # 2. BOUNDARY CHECKS (Before Physics)
            if phase == "PROTON" and r < self.r_singularity:
                phase = "MUON"
                vm *= self.coupling_efficiency
                vl *= self.coupling_efficiency
                # Push out to clean start
                m, l = m * 2.0, l * 2.0 
                continue # Re-evaluate state

            if phase == "MUON" and r > self.r_exhaust:
                # HARVEST
                yield_energy = ke
                harvest_log.append(yield_energy)
                
                if cycle_count % 5 == 0:
                    logger.info(f"    [+] Cycle {cycle_count} Yield: {yield_energy:.2e} J")
                
                phase = "PROTON"
                cycle_count += 1
                
                # RESET
                angle = np.arctan2(l, m)
                m = self.r_intake * np.cos(angle)
                l = self.r_intake * np.sin(angle)
                
                injection_speed = 1.5
                vm = -0.5 * np.cos(angle) - injection_speed * np.sin(angle)
                vl = -0.5 * np.sin(angle) + injection_speed * np.cos(angle)
                continue
            
            # 3. PHYSICS
            grad_m, grad_l = self.gradient(m, l)
            
            if phase == "PROTON":
                fm = -grad_m - (self.friction_proton * vm)
                fl = -grad_l - (self.friction_proton * vl)
            
            elif phase == "MUON":
                fm = -grad_m + (self.pressure_muon * m)
                fl = -grad_l + (self.pressure_muon * l)

            # 4. INTEGRATION (Symplectic Euler)
            vm += fm * self.dt
            vl += fl * self.dt
            
            # VELOCITY CLAMP
            v_curr = np.sqrt(vm**2 + vl**2)
            if v_curr > self.max_velocity:
                scale = self.max_velocity / v_curr
                vm *= scale
                vl *= scale
            
            m += vm * self.dt
            l += vl * self.dt
            
            total_steps += 1
            
        return np.array(r_hist), np.array(e_hist), np.array(p_hist), np.array(harvest_log)

    def render_dashboard(self):
        r, e, p, harvest = self.run_cycle()
        
        logger.info("[-] Generating Reactor Dashboard V3...")
        
        fig = plt.figure(figsize=(16, 10), facecolor='#0b0b0b')
        gs = fig.add_gridspec(2, 2)
        
        # PLOT 1: Phase Loop
        ax1 = fig.add_subplot(gs[0, 0], facecolor='#000000')
        points = np.array([r, e]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        cmap = LinearSegmentedColormap.from_list("reactor_mode", ["#00ccff", "#ffaa00"])
        lc = LineCollection(segments, cmap=cmap, norm=plt.Normalize(0, 1))
        lc.set_array(p)
        lc.set_linewidth(0.5)
        ax1.add_collection(lc)
        
        ax1.set_xlim(0, 26)
        ymax = np.max(e) if len(e) > 0 else 1
        ax1.set_ylim(0, ymax * 1.1)
        ax1.set_xlabel("Radius (r)", color='white')
        ax1.set_ylabel("Energy (E)", color='white')
        ax1.set_title("Phase Space Holonomy (Heartbeat Loop)", color='white')
        ax1.axvline(self.r_intake, color='#00ccff', linestyle=':')
        ax1.axvline(self.r_exhaust, color='#ffaa00', linestyle=':')
        ax1.tick_params(colors='white')
        
        # PLOT 2: Power Output
        ax2 = fig.add_subplot(gs[0, 1], facecolor='#000000')
        cycles = np.arange(1, len(harvest) + 1)
        ax2.plot(cycles, harvest, 'o-', color='#00ff00', linewidth=2)
        ax2.fill_between(cycles, harvest, 0, color='#00ff00', alpha=0.2)
        ax2.set_xlabel("Cycle Number", color='white')
        ax2.set_ylabel("Yield (J)", color='white')
        ax2.set_title(f"Reactor Output (Mean: {np.mean(harvest):.1f} J)", color='white')
        ax2.grid(color='#333333', linestyle=':')
        ax2.tick_params(colors='white')
        
        # PLOT 3: Stability Trace
        ax3 = fig.add_subplot(gs[1, :], facecolor='#000000')
        steps = np.arange(len(e))
        ax3.scatter(steps, e, c=p, cmap=cmap, s=1, alpha=0.5)
        ax3.set_xlabel("Time Steps", color='white')
        ax3.set_ylabel("System Energy", color='white')
        ax3.set_title("System Stability Trace", color='white')
        ax3.tick_params(colors='white')
        
        plt.tight_layout()
        plt.savefig("heartbeat_reactor_dashboard_v3.png", dpi=150)
        logger.info("[+] Dashboard Saved: 'heartbeat_reactor_dashboard_v3.png'")
        plt.show()

if __name__ == "__main__":
    reactor = HeartbeatReactorV3(cycles=20)
    reactor.render_dashboard()