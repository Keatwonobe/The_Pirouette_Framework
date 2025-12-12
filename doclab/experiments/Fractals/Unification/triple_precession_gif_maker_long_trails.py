import numpy as np
from PIL import Image, ImageDraw
from collections import deque
import colorsys
import sys

# =========================================================
#  PIROUETTE: FINAL ANALYTICAL RENDERER
# =========================================================

# --- CONFIG ---
OUTPUT_FILENAME_COMBINED = "triple_precession_readout.gif"
TOTAL_FRAMES = 1600 
PANEL_RES = 600         # Slightly reduced from 600 to save size

# OPTIMIZATION (COMPRESSION SETTINGS)
FRAME_SKIP = 3          # Was 3. Increased to 6 to halve the file size.
RENDER_DURATION_MS = 5000 # Increased duration to compensate for fewer frames.
                        # This keeps the "long" feel.

WIRE_PANEL_WIDTH = 300      
WIRE_STRIP_WIDTH = 100

# VIEW SETTINGS
ISO_ANGLE = 0.85       
WIDE_ZOOM = 180.0      
LEFT_ZOOM = 14.0       

# PHYSICS CONSTANTS
SRC_STRONG_M = np.array([-10.0, 10.0, 0.0])
SRC_STRONG_L = np.array([5.0, 5.0, -10.0])
SRC_AMP = 1.0
OMEGA_SYS = 0.06      

# DYNAMICS
TRAIL_LENGTH_MAP = TOTAL_FRAMES 
DRAG_FACTOR = 0.995    
ISO_ANGLE_2 = 0.85
KAPPA_TWIST_MAP = 0.7 

# COLORS
P1_COLOR = (255, 255, 255) 
P2_COLOR = (100, 255, 100) 
P3_COLOR = (100, 100, 255) 

# =========================================================
#  UNIFIED KERNEL
# =========================================================

def render_iso_field_unified(center_m, center_l, width, res, src_m_arr, src_l_arr, pulse, iso_angle, contour_scale):
    half_w = width / 2.0
    m_vals = np.linspace(center_m - half_w, center_m + half_w, res)
    l_vals = np.linspace(center_l - half_w, center_l + half_w, res)
    
    m_screen, l_screen = np.meshgrid(m_vals, l_vals)
    
    dm = m_screen - center_m
    aspect = 1.0 / np.cos(iso_angle)
    dl = (l_screen - center_l) * aspect
    
    m_world = center_m + dm
    l_world = center_l + dl
    
    M = m_world.flatten()[:, None]
    L = l_world.flatten()[:, None]
    
    SRC_M = src_m_arr[None, :]
    SRC_L = src_l_arr[None, :]
    
    dx = M - SRC_M
    dy = L - SRC_L
    dist = np.sqrt(dx*dx + dy*dy) + 1e-9
    
    k = (2 * np.pi) / 10.0
    phase = k * dist
    amp = (SRC_AMP / dist) * pulse
    
    psi_r = np.sum(amp * np.cos(phase), axis=1)
    psi_i = np.sum(amp * np.sin(phase), axis=1)
    
    amp_val = np.sqrt(psi_r**2 + psi_i**2)
    phase_val = np.arctan2(psi_i, psi_r)
    
    log_amp = np.log1p(amp_val)
    contour = 0.5 + 0.5 * np.sin(log_amp * contour_scale) 
    
    hue = (phase_val + np.pi) / (2 * np.pi)
    min_dist = np.min(dist, axis=1)
    val = contour * np.minimum(1.0, 1.5 / (min_dist * 0.15 + 1.0))
    
    h6 = hue * 6.0
    x = (1.0 - np.abs(np.remainder(h6, 2.0) - 1.0))
    
    r = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [1.0, x, 0.0, 0.0, x, 1.0])
    g = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [x, 1.0, 1.0, x, 0.0, 0.0])
    b = np.select([h6 < 1, h6 < 2, h6 < 3, h6 < 4, h6 < 5, h6 >= 5], [0.0, 0.0, x, 1.0, 1.0, x])
    
    r_final = r * val
    g_final = g * val
    b_final = b * val
    
    return np.stack([r_final.reshape(res, res), g_final.reshape(res, res), b_final.reshape(res, res)], axis=2)

def get_gradient(m, l, pulse):
    eps = 0.01
    def val(tm, tl):
        dx = tm - SRC_STRONG_M
        dy = tl - SRC_STRONG_L
        d = np.sqrt(dx**2 + dy**2) + 1e-9
        ph = (2*np.pi)/10.0 * d
        a = (SRC_AMP/d) * pulse
        pr = np.sum(a*np.cos(ph))
        pi = np.sum(a*np.sin(ph))
        return pr**2 + pi**2
    
    v0 = val(m, l)
    gm = (val(m+eps, l) - v0)/eps
    gl = (val(m, l+eps) - v0)/eps
    return gm, gl

# =========================================================
#  SIMULATION & ORCHESTRATION
# =========================================================

class IsoTracker:
    def __init__(self, start_m, start_l, zoom_level, trail_len):
        self.m = start_m
        self.l = start_l
        self.history = deque(maxlen=trail_len)
        self.zoom = zoom_level

    def project_trail(self, res, azimuth_phi, center_m, center_l):
        pts = []
        cx, cy = res/2, res/2
        scale = res / self.zoom
        aspect = np.cos(azimuth_phi)
        for (hm, hl) in self.history:
            dm = hm - center_m
            dl = hl - center_l
            pts.append((cx + dm * scale, cy - (dl * scale * aspect)))
        return pts

class ThreeQuarkSimulator:
    def __init__(self):
        center_m_start, center_l_start, r_offset = 0.0, 0.0, 2.0
        
        self.p1_m, self.p1_l = center_m_start + r_offset * np.cos(np.pi/6), center_l_start + r_offset * np.sin(np.pi/6)
        self.p1_vm, self.p1_vl = 0.1, 0.0
        self.history_1 = []
        
        self.p2_m, self.p2_l = center_m_start + r_offset * np.cos(5*np.pi/6), center_l_start + r_offset * np.sin(5*np.pi/6) 
        self.p2_vm, self.p2_vl = -0.1, 0.0
        self.history_2 = []
        
        self.p3_m, self.p3_l = center_m_start + r_offset * np.cos(9*np.pi/6), center_l_start + r_offset * np.sin(9*np.pi/6)
        self.p3_vm, self.p3_vl = 0.0, 0.1
        self.history_3 = []
    
    def simulate_step(self, m, l, vm, vl, f):
        pulse = 1.0 + 0.15 * np.sin(f * 0.1)
        omega = OMEGA_SYS
        gm, gl = get_gradient(m, l, pulse)
        
        # Physics Engine
        acc_m = (gm * 0.02) + (2 * omega * vl) + ((omega**2) * m) + (-KAPPA_TWIST_MAP * omega * m)
        acc_l = (gl * 0.02) + (-2 * omega * vm) + ((omega**2) * l) + (-KAPPA_TWIST_MAP * omega * l)
        
        vm = (vm + acc_m) * DRAG_FACTOR
        vl = (vl + acc_l) * DRAG_FACTOR
        return m + vm, l + vl, vm, vl

    def simulate_all(self):
        print("--- 🔬 STARTING SIMULATION & DATA DUMP ---")
        print("Frame, P1_m, P1_l, P2_m, P2_l, P3_m, P3_l")
        
        com_history = []
        
        for f in range(TOTAL_FRAMES):
            self.p1_m, self.p1_l, self.p1_vm, self.p1_vl = self.simulate_step(self.p1_m, self.p1_l, self.p1_vm, self.p1_vl, f)
            self.history_1.append((self.p1_m, self.p1_l))
            
            self.p2_m, self.p2_l, self.p2_vm, self.p2_vl = self.simulate_step(self.p2_m, self.p2_l, self.p2_vm, self.p2_vl, f)
            self.history_2.append((self.p2_m, self.p2_l))

            self.p3_m, self.p3_l, self.p3_vm, self.p3_vl = self.simulate_step(self.p3_m, self.p3_l, self.p3_vm, self.p3_vl, f)
            self.history_3.append((self.p3_m, self.p3_l))
            
            # --- DATA READOUT ---
            # This prints the CSV-style equation data to terminal
            print(f"{f}, {self.p1_m:.5f}, {self.p1_l:.5f}, {self.p2_m:.5f}, {self.p2_l:.5f}, {self.p3_m:.5f}, {self.p3_l:.5f}")
            
            center_m = (self.p1_m + self.p2_m + self.p3_m) / 3.0
            center_l = (self.p1_l + self.p2_l + self.p3_l) / 3.0
            com_history.append((center_m, center_l))

        print("✅ SIMULATION COMPLETE.")
        return self.history_1, self.history_2, self.history_3, com_history

def draw_precession_trail(draw_target, current_history, full_history_len, center_m, center_l, res_x, res_y, zoom, angle, trail_color, current_p_color, draw_line_gradient=False, infinite_persistence=False):
    cx, cy = res_x / 2.0, res_y / 2.0
    scale = res_y / zoom 
    aspect = np.cos(angle)
    
    trail_overlay = Image.new("RGBA", (res_x, res_y), (0,0,0,0))
    trail_draw = ImageDraw.Draw(trail_overlay)
    
    for i in range(len(current_history) - 1):
        (m1, l1) = current_history[i]
        (m2, l2) = current_history[i+1]
        
        p1 = (cx + (m1 - center_m) * scale, cy - ((l1 - center_l) * scale * aspect))
        p2 = (cx + (m2 - center_m) * scale, cy - ((l2 - center_l) * scale * aspect))
        
        if draw_line_gradient:
            progress = i / full_history_len 
            hue = (i % 100) / 100.0
            r,g,b = colorsys.hsv_to_rgb(hue, 1, 1)
            alpha = int(255 * (0.5 + 0.5 * progress))
            col = (int(r*255), int(g*255), int(b*255), alpha)
        elif infinite_persistence:
            col = (trail_color[0], trail_color[1], trail_color[2], 255)
        else: 
            progress = i / full_history_len 
            alpha = int(255 * (0.1 + 0.9 * progress)) 
            col = (trail_color[0], trail_color[1], trail_color[2], alpha)
        
        trail_draw.line([p1, p2], fill=col, width=2)

    draw_target.paste(trail_overlay, (0,0), trail_overlay)
    
    if current_history:
        (m_curr, l_curr) = current_history[-1]
        sx = cx + (m_curr - center_m) * scale
        sy = cy - ((l_curr - center_l) * scale * aspect)
        radius = 4
        ImageDraw.Draw(draw_target).ellipse([sx-radius, sy-radius, sx+radius, sy+radius], fill=current_p_color)

def run_illuminator_frames_infinite(p1_history):
    print("--- 💡 ILLUMINATOR: INFINITE PERSISTENCE MODE ---")
    
    start_m, start_l = p1_history[0]
    # NOTE: Set history length to TOTAL_FRAMES to never forget a point
    tracker = IsoTracker(start_m, start_l, LEFT_ZOOM, TOTAL_FRAMES)
    solver_m, solver_l = start_m, start_l
    frames_buffer = []
    
    for f in range(TOTAL_FRAMES):
        theta = OMEGA_SYS * f 
        rot_src_m = SRC_STRONG_M * np.cos(theta) - SRC_STRONG_L * np.sin(theta)
        rot_src_l = SRC_STRONG_M * np.sin(theta) + SRC_STRONG_L * np.cos(theta)
        
        rgb_data = render_iso_field_unified(solver_m, solver_l, tracker.zoom, PANEL_RES, 
                                            rot_src_m, rot_src_l, 1.0, ISO_ANGLE_2, 25.0)
        img_pil = Image.fromarray((rgb_data * 255).astype(np.uint8)).convert("RGB")
        
        gray = np.mean(rgb_data, axis=2)
        mid = PANEL_RES // 2
        r = 30
        sub = gray[max(0, mid-r):min(PANEL_RES, mid+r), max(0, mid-r):min(PANEL_RES, mid+r)]
        loc = np.unravel_index(np.argmax(sub), sub.shape) if sub.size > 0 else (r, r)
        
        scale = tracker.zoom / PANEL_RES
        aspect = np.cos(ISO_ANGLE_2)
        true_m = solver_m + ((loc[1] + max(0, mid-r)) - mid) * scale
        true_l = solver_l + ((loc[0] + max(0, mid-r)) - mid) * scale / aspect
        
        tracker.history.append((true_m, true_l))
        solver_m += (true_m - solver_m) * 0.1
        solver_l += (true_l - solver_l) * 0.1
        tracker.m, tracker.l = solver_m, solver_l
        
        # DRAW INFINITE TRAIL (SOLID YELLOW)
        draw = ImageDraw.Draw(img_pil)
        screen_pts = tracker.project_trail(PANEL_RES, ISO_ANGLE_2, tracker.m, tracker.l)
        
        if len(screen_pts) > 2:
            ribbon_overlay = Image.new("RGBA", img_pil.size, (0,0,0,0))
            ribbon_draw = ImageDraw.Draw(ribbon_overlay)
            
            # Draw lines in a batch? No, simple loop for now
            # Solid Yellow, No Alpha
            ribbon_draw.line(screen_pts, fill=(255, 215, 0, 255), width=2)
            img_pil.paste(ribbon_overlay, (0,0), ribbon_overlay)

        draw.text((10, 10), "VIEW: ISOMETRIC ILLUMINATOR", fill=(200, 200, 200))
        draw.text((10, 25), "PERSISTENCE: INFINITE", fill=(255, 215, 0))
        frames_buffer.append(img_pil)
        
        if f % 100 == 0: print(f"  Illuminator Frame {f}...")

    return frames_buffer

def combine_and_save():
    simulator = ThreeQuarkSimulator()
    p1, p2, p3, com = simulator.simulate_all()
    illuminator_frames = run_illuminator_frames_infinite(p1)
    
    print("--- 🎬 COMBINING & COMPRESSING ---")
    combined_frames = []
    all_histories = (p1, p2, p3)
    TOTAL_WIDTH = PANEL_RES * 2 + WIRE_PANEL_WIDTH
    
    for f in range(TOTAL_FRAMES):
        if f % FRAME_SKIP != 0: continue # SKIP FRAMES TO SAVE SIZE
            
        # 1. Map Frame
        img = Image.fromarray((render_iso_field_unified(com[f][0], com[f][1], WIDE_ZOOM, PANEL_RES, SRC_STRONG_M, SRC_STRONG_L, 1.0, ISO_ANGLE, 20.0) * 255).astype(np.uint8)).convert("RGB")
        draw_precession_trail(img, p1[:f+1], TOTAL_FRAMES, com[f][0], com[f][1], PANEL_RES, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, (255,255,255), P1_COLOR, draw_line_gradient=True)
        draw_precession_trail(img, p2[:f+1], TOTAL_FRAMES, com[f][0], com[f][1], PANEL_RES, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, (50,120,50), P2_COLOR)
        draw_precession_trail(img, p3[:f+1], TOTAL_FRAMES, com[f][0], com[f][1], PANEL_RES, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, (50,50,120), P3_COLOR)
        
        # 2. Wireframe (Infinite Persistence ON)
        wire_img = Image.new('RGB', (WIRE_PANEL_WIDTH, PANEL_RES), (0, 0, 0))
        ctr_m, ctr_l = p1[f]
        
        strip1 = Image.new('RGB', (WIRE_STRIP_WIDTH, PANEL_RES), (0,0,0))
        draw_precession_trail(strip1, p1[:f+1], TOTAL_FRAMES, ctr_m, ctr_l, WIRE_STRIP_WIDTH, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, (180,180,180), P1_COLOR, infinite_persistence=True)
        wire_img.paste(strip1, (0, 0))
        
        strip2 = Image.new('RGB', (WIRE_STRIP_WIDTH, PANEL_RES), (0,0,0))
        draw_precession_trail(strip2, p2[:f+1], TOTAL_FRAMES, ctr_m, ctr_l, WIRE_STRIP_WIDTH, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, (0,200,0), P2_COLOR, infinite_persistence=True)
        wire_img.paste(strip2, (WIRE_STRIP_WIDTH, 0))
        
        strip3 = Image.new('RGB', (WIRE_STRIP_WIDTH, PANEL_RES), (0,0,0))
        draw_precession_trail(strip3, p3[:f+1], TOTAL_FRAMES, ctr_m, ctr_l, WIRE_STRIP_WIDTH, PANEL_RES, WIDE_ZOOM, ISO_ANGLE, (0,0,200), P3_COLOR, infinite_persistence=True)
        wire_img.paste(strip3, (WIRE_STRIP_WIDTH*2, 0))
        
        # 3. Combine
        combined_img = Image.new('RGB', (TOTAL_WIDTH, PANEL_RES))
        combined_img.paste(img, (0, 0))
        combined_img.paste(illuminator_frames[f], (PANEL_RES, 0))
        combined_img.paste(wire_img, (PANEL_RES * 2, 0))
        
        ImageDraw.Draw(combined_img).line([(PANEL_RES, 0), (PANEL_RES, PANEL_RES)], fill=(100, 100, 100), width=2)
        ImageDraw.Draw(combined_img).line([(PANEL_RES * 2, 0), (PANEL_RES * 2, PANEL_RES)], fill=(100, 100, 100), width=2)
        
        combined_frames.append(combined_img)
        print(f"  Frame {f}/{TOTAL_FRAMES} Composed", end='\r')

    print(f"\nSaving {OUTPUT_FILENAME_COMBINED}...")
    combined_frames[0].save(OUTPUT_FILENAME_COMBINED, save_all=True, append_images=combined_frames[1:], duration=RENDER_DURATION_MS, loop=0)
    print("✅ DONE.")

if __name__ == "__main__":
    combine_and_save()