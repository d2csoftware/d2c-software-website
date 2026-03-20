"""
Crop all logos tightly (remove transparent/white padding),
and fix any remaining issues.
"""
from PIL import Image
import numpy as np
import os

LOGOS_DIR = "/home/ubuntu/d2c-website/logos"

def tight_crop(img_path, padding=10):
    """Crop image to its non-transparent bounding box."""
    img = Image.open(img_path).convert("RGBA")
    data = np.array(img)
    
    # Find non-transparent pixels
    alpha = data[:,:,3]
    rows = np.any(alpha > 20, axis=1)
    cols = np.any(alpha > 20, axis=0)
    
    if not rows.any() or not cols.any():
        print(f"SKIP {os.path.basename(img_path)} - all transparent!")
        return
    
    rmin, rmax = np.where(rows)[0][[0, -1]]
    cmin, cmax = np.where(cols)[0][[0, -1]]
    
    # Add padding
    h, w = data.shape[:2]
    rmin = max(0, rmin - padding)
    rmax = min(h-1, rmax + padding)
    cmin = max(0, cmin - padding)
    cmax = min(w-1, cmax + padding)
    
    cropped = img.crop((cmin, rmin, cmax+1, rmax+1))
    cropped.save(img_path)
    print(f"Cropped {os.path.basename(img_path)}: {img.size} -> {cropped.size}")

# Crop all logos tightly
for fname in sorted(os.listdir(LOGOS_DIR)):
    if fname.endswith(".png"):
        tight_crop(os.path.join(LOGOS_DIR, fname))

print("\nDone cropping.")

# Special check: Virgin logo - if it's all white/near-white transparent, 
# it will work with the CSS filter. Let's verify.
virgin_path = os.path.join(LOGOS_DIR, "virgin.png")
img = Image.open(virgin_path).convert("RGBA")
data = np.array(img)
alpha = data[:,:,3]
opaque = data[alpha > 20]
if len(opaque) > 0:
    avg_r = opaque[:,0].mean()
    avg_g = opaque[:,1].mean()
    avg_b = opaque[:,2].mean()
    print(f"\nVirgin logo opaque pixels avg RGB: ({avg_r:.0f}, {avg_g:.0f}, {avg_b:.0f})")
    if avg_r > 200 and avg_g > 200 and avg_b > 200:
        print("Virgin logo is white - will work with CSS filter (white -> black -> white)")
    elif avg_r > 150 and avg_g < 80 and avg_b < 80:
        print("Virgin logo is RED - will convert to white silhouette OK")
    else:
        print("Virgin logo has mixed colours - should still convert to white silhouette OK")
else:
    print("Virgin logo appears to be fully transparent!")
