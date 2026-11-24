# main.py — entry program for news-image-20261124 (standard library only)
# Copies the pre-rendered entry.png shipped in this repository to
# /output/entry.png. No rendering happens here: the grading sandbox has no
# PIL and no system fonts, so the image is committed ready-made.
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))

if __name__ == "__main__":
    os.makedirs("/output", exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "entry.png"), "/output/entry.png")
    print("wrote /output/entry.png")
