import numpy as np
import matplotlib.pyplot as plt
from astropy.coordinates import SkyCoord
import astropy.units as u
from astropy.table import Table

# Try to import astroquery for the real data pull
try:
    from astroquery.gaia import Gaia
    from astroquery.vizier import Vizier
    GAIA_AVAILABLE = True
except ImportError:
    GAIA_AVAILABLE = False
    print(" [!] WARNING: 'astroquery' library not found.")
    print("     To pull real Gaia data, please run: pip install astroquery")

# ======================
# CONFIGURATION
# ======================
# The Maw Coordinates (Cold Spot Core)
TARGET_L = 204.1 
TARGET_B = -63.9
SEARCH_RADIUS = 10.0  # Degrees (Wide net)
LIMIT = 2000          # Max stars to retrieve

def query_gaia_data():
    if not GAIA_AVAILABLE:
        print("[!] Astroquery not installed. Cannot retrieve real stars.")
        return None
        
    print(f"[*] Connecting to ESA Gaia Archive (DR3)...")
    print(f"    Target: Galactic l={TARGET_L:.2f}, b={TARGET_B:.2f}")
    
    # Get center RA/DEC
    c = SkyCoord(l=TARGET_L*u.deg, b=TARGET_B*u.deg, frame='galactic')
    c_icrs = c.icrs
    
    query = f"""
    SELECT TOP {LIMIT}
        source_id, ra, dec, parallax, pmra, pmdec, radial_velocity,
        phot_g_mean_mag, bp_rp
    FROM gaiadr3.gaia_source
    WHERE 
        1=CONTAINS(
            POINT('ICRS', ra, dec), 
            CIRCLE('ICRS', {c_icrs.ra.deg}, {c_icrs.dec.deg}, {SEARCH_RADIUS}) 
        )
        AND parallax > 0.5 
        AND sqrt(power(pmra,2) + power(pmdec,2)) > 5.0 
    """
    
    job = Gaia.launch_job(query)
    results = job.get_results()
    print(f"[*] Retrieved {len(results)} real stars from Gaia.")
    return results

def analyze_kinematics(stars):
    print("[*] Processing Kinematics...")
    
    # Helper to strip units if they exist, to avoid "km^2/s^2" errors
    def safe_val(col):
        if hasattr(col, 'unit') and col.unit is not None:
            return col.value
        return col

    # Extract raw values
    ra = safe_val(stars['ra'])
    dec = safe_val(stars['dec'])
    plx = safe_val(stars['parallax'])
    pmra = safe_val(stars['pmra'])
    pmdec = safe_val(stars['pmdec'])
    rv = safe_val(stars['radial_velocity'])
    
    # Handle NaNs in Radial Velocity (set to 0 if missing, though ideally we'd filter)
    rv = np.nan_to_num(rv, nan=0.0)
    
    # Convert to SkyCoord with explicit units
    # Parallax (mas) -> Distance (pc)
    dist_pc = 1000.0 / plx
    
    c = SkyCoord(ra=ra*u.deg, 
                 dec=dec*u.deg, 
                 distance=dist_pc*u.pc,
                 pm_ra_cosdec=pmra*u.mas/u.yr, 
                 pm_dec=pmdec*u.mas/u.yr,
                 radial_velocity=rv*u.km/u.s,
                 frame='icrs')
    
    g = c.galactic
    
    # Extract plotting data
    l = g.l.deg
    b = g.b.deg
    
    # Proper motion in Galactic Frame
    pm_l = g.pm_l_cosb.value
    pm_b = g.pm_b.value
    
    # Magnitudes for plotting size
    mags = safe_val(stars['phot_g_mean_mag'])
    
    return l, b, pm_l, pm_b, mags

def plot_maw_dynamics(l, b, pml, pmb, mags):
    print("[*] Visualizing Gaia Velocity Field...")
    
    fig = plt.figure(figsize=(14, 10), facecolor='#080808')
    ax = fig.add_subplot(111)
    ax.set_facecolor('#080808')
    
    # 1. The Maw (Target)
    maw = plt.Circle((TARGET_L, TARGET_B), 1.5, color='lime', alpha=0.1)
    ax.add_patch(maw)
    ax.scatter(TARGET_L, TARGET_B, marker='+', s=200, color='lime', zorder=20)
    ax.text(TARGET_L, TARGET_B-2, "COLD SPOT CORE", color='lime', ha='center', fontsize=10, fontweight='bold')
    
    # 2. Real Stars
    # Size by brightness
    # Handle masked/nan mags
    mags = np.nan_to_num(mags, nan=15)
    sizes = (20 - mags) * 3
    sizes[sizes < 1] = 1
    
    # Scatter
    speed = np.sqrt(pml**2 + pmb**2)
    sc = ax.scatter(l, b, s=sizes, c=speed, cmap='cool', alpha=0.8, edgecolors='none')
    
    # 3. Velocity Vectors (The Stream)
    q = ax.quiver(l, b, pml, pmb, color='cyan', alpha=0.5, scale=500, width=0.0015, headwidth=3)
    
    # 4. Streamlines (The Topology)
    try:
        from scipy.interpolate import Rbf
        # Clean data for RBF
        mask = np.isfinite(l) & np.isfinite(b) & np.isfinite(pml) & np.isfinite(pmb)
        l_c, b_c, u_c, v_c = l[mask], b[mask], pml[mask], pmb[mask]
        
        # Reduce sample for speed if needed
        if len(l_c) > 1000:
            idx = np.random.choice(len(l_c), 1000, replace=False)
            l_c, b_c, u_c, v_c = l_c[idx], b_c[idx], u_c[idx], v_c[idx]

        gl = np.linspace(TARGET_L - SEARCH_RADIUS, TARGET_L + SEARCH_RADIUS, 100)
        gb = np.linspace(TARGET_B - SEARCH_RADIUS, TARGET_B + SEARCH_RADIUS, 100)
        GL, GB = np.meshgrid(gl, gb)
        
        rbf_u = Rbf(l_c, b_c, u_c, function='linear', smooth=2)
        rbf_v = Rbf(l_c, b_c, v_c, function='linear', smooth=2)
        
        U_grid = rbf_u(GL, GB)
        V_grid = rbf_v(GL, GB)
        
        ax.streamplot(GL, GB, U_grid, V_grid, color='white', density=1.2, linewidth=0.5, arrowsize=0.5, alpha=0.3)
    except Exception as e:
        print(f"[!] Streamline error: {e}")

    # Formatting
    ax.set_xlim(TARGET_L + SEARCH_RADIUS, TARGET_L - SEARCH_RADIUS) # Invert L
    ax.set_ylim(TARGET_B - SEARCH_RADIUS, TARGET_B + SEARCH_RADIUS)
    
    ax.set_title("GAIA DR3: Real Stellar Kinematics around the Cold Spot", color='white', fontsize=16)
    ax.set_xlabel("Galactic Longitude (l)", color='gray')
    ax.set_ylabel("Galactic Latitude (b)", color='gray')
    ax.grid(True, color='#222222', linestyle=':')
    
    cbar = plt.colorbar(sc, ax=ax)
    cbar.set_label("Proper Motion Speed (mas/yr)", color='gray')
    cbar.ax.yaxis.set_tick_params(color='gray', labelcolor='gray')
    
    plt.savefig("gaia_maw_investigation.png")
    print("✅ Gaia Map Saved: gaia_maw_investigation.png")
    
    # 5. Metrics
    center_idx = 50
    u_cen = U_grid[center_idx, center_idx]
    v_cen = V_grid[center_idx, center_idx]
    
    print("\n" + "="*50)
    print("GAIA KINEMATIC REPORT:")
    print(f"Flow at Core: pm_l={u_cen:.2f}, pm_b={v_cen:.2f} mas/yr")
    
    # Radial Divergence Check
    # Filter stars within 3 degrees
    core_dist = np.sqrt((l - TARGET_L)**2 + (b - TARGET_B)**2)
    core_mask = core_dist < 3.0
    
    if np.sum(core_mask) > 10:
        cl, cb = l[core_mask], b[core_mask]
        cu, cv = pml[core_mask], pmb[core_mask]
        
        # Radial projection
        rx, ry = cl - TARGET_L, cb - TARGET_B
        dot = cu*rx + cv*ry
        mean_div = np.mean(dot)
        
        if mean_div < 0:
            print("⚡ CONVERGENCE: Stars near the core are turning INWARD.")
        else:
            print("DIVERGENCE: Stars near the core are turning OUTWARD (Repulsion/Wake).")

if __name__ == "__main__":
    data = query_gaia_data()
    if data:
        l, b, pml, pmb, mags = analyze_kinematics(data)
        plot_maw_dynamics(l, b, pml, pmb, mags)