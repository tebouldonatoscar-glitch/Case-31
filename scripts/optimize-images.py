#!/usr/bin/env python3
"""Resize source photos into responsive WebP + JPEG sets for assets/images/."""
import os
from PIL import Image, ImageOps

SRC_DIR = "/root/.claude/uploads/a4884827-c0c0-5abd-8b4a-4b9cb7865cc6"
OUT_DIR = os.path.join(os.path.dirname(__file__), "..", "assets", "images")

# (source filename, output basename, [target widths], crop aspect ratio or None)
JOBS = [
    ("f18b163f-691be614f64b4d47b5e873a6839fbbdf.jpeg", "hero-entrance", [640, 960, 1440], None),
    ("3a4130cb-53063ec0f37a47e1945f42c00de9fee5.jpeg", "meat-board", [640, 960, 1440], None),
    ("c5862cbe-9da817e664dd4ca7aa150183fa0a8578.jpeg", "meat-ribs", [640, 960, 1440], None),
    ("5fa327c4-ab22b9e3deaa4e27ab36ad3227d85683.jpeg", "padthai", [480, 720, 1080], None),
    ("15fb6d2a-ee71dec6284a4a64a46680f0c3781154.jpeg", "terrace", [452, 678], None),
]

os.makedirs(OUT_DIR, exist_ok=True)

for src_name, basename, widths, _ in JOBS:
    path = os.path.join(SRC_DIR, src_name)
    im = Image.open(path)
    im = ImageOps.exif_transpose(im).convert("RGB")
    ow, oh = im.size
    for w in widths:
        w = min(w, ow)
        h = round(oh * (w / ow))
        resized = im.resize((w, h), Image.LANCZOS)
        jpg_path = os.path.join(OUT_DIR, f"{basename}-{w}.jpg")
        webp_path = os.path.join(OUT_DIR, f"{basename}-{w}.webp")
        resized.save(jpg_path, "JPEG", quality=80, optimize=True, progressive=True)
        resized.save(webp_path, "WEBP", quality=78, method=6)
        print(f"{basename}-{w}: jpg={os.path.getsize(jpg_path)//1024}KB webp={os.path.getsize(webp_path)//1024}KB")
