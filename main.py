# main.py — news-image-20261117 entry (Python 3.13, standard library only).
# The image is drawn by render.py (Pillow, run locally) and shipped beside
# this file as entry.png; this program only copies it to the output path,
# exactly the pattern the competition kit's starter uses. Copying bytes is
# deterministic by construction: two runs write the same file.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")

os.makedirs(OUT_DIR, exist_ok=True)
src = os.path.join(HERE, "entry.png")
dst = os.path.join(OUT_DIR, "entry.png")
shutil.copyfile(src, dst)
# The gate allows at most 1 MiB and 1024x1024 px; fail loudly instead of
# silently handing the grader a file that cannot pass it.
if os.path.getsize(dst) > 1048576:
    raise SystemExit("entry.png is over the 1 MiB cap")
