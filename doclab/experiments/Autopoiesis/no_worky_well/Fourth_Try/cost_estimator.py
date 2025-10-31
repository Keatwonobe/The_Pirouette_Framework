
from pathlib import Path

def estimate(n_modules:int, law_in:int=5000, law_out:int=1600, phil_in:int=6000, phil_out:int=1200, art_in:int=5000, art_out:int=900):
    law_usd = (n_modules*law_in)/1_000_000*1.25 + (n_modules*law_out)/1_000_000*10.0
    return {
        "modules": n_modules,
        "law_tokens": {"in": n_modules*law_in, "out": n_modules*law_out, "usd_estimate": round(law_usd,2)},
        "phil_tokens": {"in": n_modules*phil_in, "out": n_modules*phil_out, "credit": "Gemini $300"},
        "art_tokens": {"in": n_modules*art_in, "out": n_modules*art_out}
    }

if __name__ == "__main__":
    print(estimate(20))
