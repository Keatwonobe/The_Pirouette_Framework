
import subprocess
from pathlib import Path

ROOT = Path(".").resolve()
MAP = str(ROOT / "section_map.json")
SECTION_WRITER = str(ROOT / "section_writer.py")
DEBATE_FUSER = str(ROOT / "debate_fuser.py")
MANIFESTO_WEAVE = str(ROOT / "manifesto_weave.py")
GRAND = str(ROOT / "grand_builder.py")

def run(cmd):
    print("▶", " ".join(cmd))
    subprocess.run(cmd, check=True)

def main():
    import argparse
    p = argparse.ArgumentParser(description="Section-based autopoietic build.")
    p.add_argument("--sections", nargs="+", default=["I","II","III","IV","V","VI","SYN"])
    p.add_argument("--brief", default="State the core ideas and formalism relevant to this section.")
    p.add_argument("--title", default="Manifesto Module: Resonant Unification")
    args = p.parse_args()

    # 1) draft sections
    for sid in args.sections:
        run(["python", SECTION_WRITER, MAP, sid, "--brief", args.brief])
    # 2) curate via debate
    for pth in Path("./sections_out").glob("*.md"):
        run(["python", DEBATE_FUSER, str(pth)])
    # 3) weave manifesto module
    run(["python", MANIFESTO_WEAVE, "./sections_curated", MAP, "--title", args.title])
    # 4) assemble grand
    run(["python", GRAND, MAP, "./manifesto_modules"])

if __name__=="__main__":
    main()
