# Zipper Mode — Light sweep (time-optimized)
# Reduce grid to keep under execution limits:
# - size=192
# - kappas = [0.2, 0.9]
# - params: control vs corridor only
# - limit saved figures to corridor runs only (per image, 1 pre/post + 1 spectrum)
import numpy as np, pandas as pd, matplotlib.pyplot as plt, os
from PIL import Image

def polar_grid(n: int = 192, r_max: float = 1.0):
    lin = np.linspace(-r_max, r_max, n)
    x, y = np.meshgrid(lin, lin); r = np.sqrt(x*x + y*y) + 1e-12
    theta = np.arctan2(y, x); return x, y, r, theta

def dominant_angular_mode(field, theta, max_m=8):
    n = field.shape[0]; mask = np.ones_like(field, bool); c = n//2
    rr = np.sqrt((np.indices(field.shape)[0]-c)**2 + (np.indices(field.shape)[1]-c)**2)
    mask[rr<4]=False; amps=[]
    for m in range(1, max_m+1):
        c0 = np.sum(field[mask]*np.cos(m*theta[mask])); s0=np.sum(field[mask]*np.sin(m*theta[mask]))
        amps.append((m, float(np.hypot(c0,s0))))
    amps.sort(key=lambda t:t[1], reverse=True); return int(amps[0][0])

def helical_time_evolve(field, kappa, t, omega=2*np.pi*1.0):
    return np.cos(kappa*omega*t)*field + np.sin(kappa*omega*t)*np.gradient(field, axis=0)

def psi_3to2_collapse_strong(field, theta, Ta, Gamma):
    m3 = np.cos(3*theta); m2 = np.cos(2*theta); a3=np.sum(field*m3)
    field_no_m3 = field - (a3/(np.sum(m3*m3)+1e-12))*m3
    E = np.sqrt(np.mean(field_no_m3**2)+1e-12); m2u=m2/np.sqrt(np.mean(m2**2)+1e-12)
    refill = E*m2u; g=float(np.clip((1.0-Ta)*Gamma,0.0,1.0))
    return (1.0-g)*field + g*refill, g

def detect_frequency(signal, dt):
    from numpy.fft import rfft, rfftfreq
    sig=signal-np.mean(signal); yf=np.abs(rfft(sig)); xf=rfftfreq(len(sig), dt)
    if len(xf)<3: return 0.0,0.0,xf,yf
    yf[0]=0.0; i=int(np.argmax(yf)); peak=float(yf[i]); noise=float(np.median(yf[yf>0])) if np.any(yf>0) else 1e-12
    return float(xf[i]), float(peak/(noise+1e-12)), xf, yf

def phase_flux_space(field, dx=1.0):
    gx,gy=np.gradient(field,dx,dx); return float(np.mean(np.hypot(gx,gy)))
def phase_flux_time(signal, dt):
    d=np.gradient(signal,dt); return float(np.mean(np.abs(d)))

def ingest_field(path, size=192):
    img=Image.open(path).convert("L").resize((size,size))
    arr=np.array(img).astype(np.float32); arr=(arr-arr.mean())/(arr.std()+1e-12); return np.tanh(arr/2.5)

def run_one(field, kappa, Ta, Gamma, Ki, outdir=None, tag=None, save_figs=False):
    n=field.shape[0]; x,y,r,theta=polar_grid(n,1.0)
    lobes_before=dominant_angular_mode(field, theta); space_flux=phase_flux_space(field)
    evolved=helical_time_evolve(field, kappa, t=6.0)
    collapsed, gate=psi_3to2_collapse_strong(evolved, theta, Ta, Gamma)
    lobes_after=dominant_angular_mode(collapsed, theta)
    t=np.arange(0,6.0,1/160.0); base=float(np.tanh(collapsed.mean())); phi=base*np.sin(Ki*t)
    dt=1/160.0; f,snr,xf,yf=detect_frequency(phi, dt); time_flux=phase_flux_time(phi, dt)
    bal=abs(space_flux-time_flux)/(abs(space_flux)+abs(time_flux)+1e-12)
    verdict=bool((Ta<=0.35) and (Gamma>=0.75) and (lobes_after<=2) and (snr>=5.0) and (bal<0.9))
    fp=sp=None
    if save_figs and outdir and tag:
        os.makedirs(outdir, exist_ok=True)
        plt.figure(figsize=(8,4)); plt.subplot(1,2,1); plt.imshow(field, cmap="gray"); plt.axis("off"); plt.title(f"Pre (lobes≈{lobes_before})")
        plt.subplot(1,2,2); plt.imshow(collapsed, cmap="gray"); plt.axis("off"); plt.title(f"Post (lobes≈{lobes_after})")
        plt.tight_layout(); fp=os.path.join(outdir, f"{tag}_pre_post.png"); plt.savefig(fp); plt.close()
        plt.figure(figsize=(6,4)); plt.plot(xf,yf); plt.xlabel("Frequency"); plt.ylabel("Amplitude"); plt.title(f"Ki spectrum (SNR={snr:.1f}, peak={f:.2f})")
        plt.tight_layout(); sp=os.path.join(outdir, f"{tag}_spectrum.png"); plt.savefig(sp); plt.close()
    return {"lobes_before":int(lobes_before), "lobes_after":int(lobes_after), "gate":float(gate), "beat_peak":float(f), "beat_SNR":float(snr),
            "phase_balance_error":float(bal), "verdict_pass":verdict, "field_png":fp or "", "spectrum_png":sp or ""}

images=[
    "zen_unbralight.png",
    "abstrewn_indignindigo.png",
    "dreamveil_oceanheart_3.png",
    "neverwonder_usewhy.png",
    "thanalon_amiss.png",
]

kappas=[0.2, 0.9]
params=[(0.90,0.40,2*np.pi*0.6), (0.28,0.88,2*np.pi*0.8)]  # control, corridor
rows=[]; base="zipper_gallery_light"; os.makedirs(base, exist_ok=True)

for pth in images:
    slug=os.path.splitext(os.path.basename(pth))[0]
    field=ingest_field(pth, size=192)
    out=os.path.join(base, slug); os.makedirs(out, exist_ok=True)
    for i,k in enumerate(kappas):
        for j,(Ta,Gamma,Ki) in enumerate(params):
            tag=f"{slug}_k{k:.2f}_{'ctrl' if j==0 else 'corr'}"
            res=run_one(field,k,Ta,Gamma,Ki,outdir=out,tag=tag,save_figs=(j==1))
            rows.append({"image":slug,"kappa":k,"Ta":Ta,"Gamma":Gamma,"Ki":Ki/(2*np.pi),
                         **res,"prepost_png":res["field_png"],"spectrum_png":res["spectrum_png"]})

atlas=pd.DataFrame(rows)
csv="zipper_atlas.csv"; atlas.to_csv(csv, index=False)

# Aggregate plots
plt.figure(figsize=(6,4))
for k in kappas:
    sel=atlas[atlas["kappa"]==k]
    pr=float(np.mean(sel["verdict_pass"])) if len(sel) else 0.0
    plt.scatter([k],[pr])
plt.xlabel("kappa"); plt.ylabel("Pass-rate"); plt.title("Pass-rate vs κ (light)"); plt.tight_layout()
pass_png="zipper_passrate_vs_kappa_light.png"; plt.savefig(pass_png); plt.close()

plt.figure(figsize=(6,4))
for k in kappas:
    sel=atlas[atlas["kappa"]==k]
    plt.scatter([k],[float(np.mean(sel["beat_SNR"])) if len(sel) else 0.0])
plt.xlabel("kappa"); plt.ylabel("Average Ki SNR"); plt.title("Average Ki SNR vs κ (light)"); plt.tight_layout()
snr_png="zipper_avg_snr_vs_kappa_light.png"; plt.savefig(snr_png); plt.close()

{"atlas_csv": csv, "gallery_dir": base, "passrate_png": pass_png, "snr_png": snr_png}
