"""
Final logo fix:
1. Replace Virgin with red script version (index 8 from search - red circle with white text)
   or index 3 (red script on transparent) - use index 3 (D4jQGFGC8Xdv.png)
2. Replace Aldi with black/white version (index 1 - tCvlfs7nZMOh.png - monochrome)
3. Replace Severn Trent with cleaner version (index 4 - GeIntwEOM1Ee.png)
4. Re-crop all

For logos that have coloured blocks (Aldi, Severn Trent), the brightness(0) invert(1) 
CSS filter will still convert them to white silhouettes - but the coloured block shape 
will be visible as a white rectangle. This is actually fine for a "trusted by" carousel.

The real fix needed:
- Virgin: current file is white-on-transparent (invisible in viewer). 
  Replace with red script version that has transparent background.
- Aldi: use the monochrome version (index 1) which is cleaner as a silhouette
"""

import shutil
import os
from PIL import Image
import numpy as np

LOGOS_DIR = "/home/ubuntu/d2c-website/logos"
SEARCH_DIR = "/home/ubuntu/upload/search_images"

# Replace Virgin with the red script version (D4jQGFGC8Xdv.png = Logo.wine version)
# or use 8cRwrqcrBzB4.png (Freebie Supply - red circle)
# Best: D4jQGFGC8Xdv.png is the clean red script on white background
# We'll use it and remove the white background

virgin_src = os.path.join(SEARCH_DIR, "D4jQGFGC8Xdv.png")
virgin_dst = os.path.join(LOGOS_DIR, "virgin.png")
shutil.copy(virgin_src, virgin_dst)
print(f"Replaced virgin.png with red script version")

# Remove white background from new Virgin logo
img = Image.open(virgin_dst).convert("RGBA")
data = np.array(img, dtype=np.float32)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
white_mask = (r > 230) & (g > 230) & (b > 230)
data[:,:,3] = np.where(white_mask, 0, data[:,:,3])
result = Image.fromarray(data.astype(np.uint8))
result.save(virgin_dst)
print(f"Removed white bg from virgin.png")

# Replace Aldi with the monochrome version (tCvlfs7nZMOh.png)
aldi_src = os.path.join(SEARCH_DIR, "tCvlfs7nZMOh.png")
aldi_dst = os.path.join(LOGOS_DIR, "aldi.png")
shutil.copy(aldi_src, aldi_dst)
print(f"Replaced aldi.png with monochrome version")

# Remove white background from Aldi
img = Image.open(aldi_dst).convert("RGBA")
data = np.array(img, dtype=np.float32)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
white_mask = (r > 230) & (g > 230) & (b > 230)
data[:,:,3] = np.where(white_mask, 0, data[:,:,3])
result = Image.fromarray(data.astype(np.uint8))
result.save(aldi_dst)
print(f"Removed white bg from aldi.png")

# Replace Severn Trent with cleaner version (GeIntwEOM1Ee.png)
st_src = os.path.join(SEARCH_DIR, "GeIntwEOM1Ee.png")
st_dst = os.path.join(LOGOS_DIR, "severn_trent.png")
shutil.copy(st_src, st_dst)
print(f"Replaced severn_trent.png with cleaner version")

# Remove white background from Severn Trent
img = Image.open(st_dst).convert("RGBA")
data = np.array(img, dtype=np.float32)
r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]
white_mask = (r > 230) & (g > 230) & (b > 230)
data[:,:,3] = np.where(white_mask, 0, data[:,:,3])
result = Image.fromarray(data.astype(np.uint8))
result.save(st_dst)
print(f"Removed white bg from severn_trent.png")

# Now tight-crop all three
def tight_crop(img_path, padding=8):
    img = Image.open(img_path).convert("RGBA")
    data = np.array(img)
    alpha = data[:,:,3]
    rows = np.any(alpha > 20, axis=1)
    cols = np.any(alpha > 20, axis=0)
    if not rows.any() or not cols.any():
        print(f"SKIP {os.path.basename(img_path)} - all transparent!")
        return
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    h, w = data.shape[:2]
    rmin = max(0, rmin - padding)
    rmax = min(h-1, rmax + padding)
    cmin = max(0, cmin - padding)
    cmax = min(w-1, cmax + padding)
    cropped = img.crop((cmin, rmin, cmax+1, rmax+1))
    cropped.save(img_path)
    print(f"Cropped {os.path.basename(img_path)}: {img.size} -> {cropped.size}")

tight_crop(virgin_dst)
tight_crop(aldi_dst)
tight_crop(st_dst)

# Final audit
print("\n--- Final audit ---")
for fname in sorted(os.listdir(LOGOS_DIR)):
    if not fname.endswith(".png"):
        continue
    path = os.path.join(LOGOS_DIR, fname)
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    data = np.array(img)
    alpha = data[:,:,3]
    trans_pct = (alpha < 30).sum() / alpha.size * 100
    opaque = data[alpha > 20]
    if len(opaque) > 0:
        avg = opaque[:,:3].mean(axis=0)
        print(f"{fname:30s}  {w}x{h}  trans={trans_pct:.0f}%  avg_rgb=({avg[0]:.0f},{avg[1]:.0f},{avg[2]:.0f})")
    else:
        print(f"{fname:30s}  {w}x{h}  EMPTY!")
