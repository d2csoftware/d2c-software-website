"""
Audit logos: check dimensions, transparency, dominant colours,
and whether the image will render as a white square under
CSS filter: brightness(0) invert(1).

A logo renders as a white square if:
  - It has a white/light solid background AND the actual logo pixels
    are also light/white (so inverting gives white on white), OR
  - The image is entirely white/near-white to begin with.

Strategy: after brightness(0) every pixel becomes black (0,0,0) or
transparent. After invert(1) every pixel becomes white (255,255,255)
or transparent. So the result is always white shapes on transparent.
The PROBLEM occurs when the SOURCE image has a solid white/light
background (no transparency) — the background also becomes white,
giving a white square.

Detection: check whether the image has an alpha channel with
meaningful transparency. If it has NO alpha (or alpha is all 255),
AND the background is white/light, it will look like a white square.
"""

from PIL import Image
import os, json

LOGOS_DIR = "/home/ubuntu/d2c-website/logos"

results = {}

for fname in sorted(os.listdir(LOGOS_DIR)):
    if not fname.endswith(".png"):
        continue
    path = os.path.join(LOGOS_DIR, fname)
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    pixels = list(img.getdata())

    total = len(pixels)
    transparent = sum(1 for p in pixels if p[3] < 30)
    semi_transparent = sum(1 for p in pixels if 30 <= p[3] < 200)
    opaque = total - transparent - semi_transparent

    # Check corners for background colour
    corners = [
        img.getpixel((0, 0)),
        img.getpixel((w-1, 0)),
        img.getpixel((0, h-1)),
        img.getpixel((w-1, h-1)),
    ]
    corner_alpha = [c[3] for c in corners]
    corner_rgb   = [(c[0], c[1], c[2]) for c in corners]

    # Is background transparent?
    bg_transparent = all(a < 30 for a in corner_alpha)
    # Is background white/light?
    bg_white = all(r > 220 and g > 220 and b > 220 for r,g,b in corner_rgb)
    # Is background dark?
    bg_dark  = all(r < 50 and g < 50 and b < 50 for r,g,b in corner_rgb)

    trans_pct = transparent / total * 100

    # Verdict
    if bg_transparent or trans_pct > 40:
        verdict = "OK - transparent background"
    elif bg_dark:
        verdict = "CAUTION - dark background (logo may be white, will still work)"
    elif bg_white:
        verdict = "PROBLEM - white/light solid background, will render as white square"
    else:
        verdict = "CHECK - coloured background, needs review"

    results[fname] = {
        "size": f"{w}x{h}",
        "transparent_pct": round(trans_pct, 1),
        "bg_transparent": bg_transparent,
        "bg_white": bg_white,
        "bg_dark": bg_dark,
        "corners_alpha": corner_alpha,
        "verdict": verdict,
    }
    print(f"{fname:30s}  {verdict}")

print("\n--- Summary ---")
for k, v in results.items():
    print(f"{k:30s}  trans={v['transparent_pct']:5.1f}%  {v['verdict']}")
