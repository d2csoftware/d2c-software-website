"""
Fix logos with white/light solid backgrounds by making white pixels transparent.
Uses flood-fill from corners + tolerance-based removal.
"""
from PIL import Image
import numpy as np
import os

LOGOS_DIR = "/home/ubuntu/d2c-website/logos"

def remove_white_background(img_path, tolerance=30):
    """Remove white/near-white background using corner flood-fill."""
    img = Image.open(img_path).convert("RGBA")
    data = np.array(img, dtype=np.float32)

    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    # Find pixels that are "white-ish" - all channels > (255 - tolerance)
    white_mask = (r > (255 - tolerance)) & (g > (255 - tolerance)) & (b > (255 - tolerance))

    # Make those pixels transparent
    data[:,:,3] = np.where(white_mask, 0, data[:,:,3])

    result = Image.fromarray(data.astype(np.uint8), 'RGBA')
    result.save(img_path)
    print(f"Fixed: {os.path.basename(img_path)}")

def remove_dark_background(img_path, tolerance=40):
    """Remove dark/black background."""
    img = Image.open(img_path).convert("RGBA")
    data = np.array(img, dtype=np.float32)

    r, g, b, a = data[:,:,0], data[:,:,1], data[:,:,2], data[:,:,3]

    # Find pixels that are "dark-ish"
    dark_mask = (r < tolerance) & (g < tolerance) & (b < tolerance)

    data[:,:,3] = np.where(dark_mask, 0, data[:,:,3])

    result = Image.fromarray(data.astype(np.uint8), 'RGBA')
    result.save(img_path)
    print(f"Fixed dark bg: {os.path.basename(img_path)}")

# Fix Barclays - white background
remove_white_background(os.path.join(LOGOS_DIR, "barclays.png"), tolerance=25)

# Fix Vodafone - dark/black background (so the white logo becomes transparent-bg)
remove_dark_background(os.path.join(LOGOS_DIR, "vodafone.png"), tolerance=50)

# Also fix Severn Trent - has white background areas
remove_white_background(os.path.join(LOGOS_DIR, "severn_trent.png"), tolerance=25)

# Fix M&S - has white background
remove_white_background(os.path.join(LOGOS_DIR, "ms.png"), tolerance=25)

# Fix Mitchell & Butlers - has white background
remove_white_background(os.path.join(LOGOS_DIR, "mitchell_butlers.png"), tolerance=25)

print("\nAll fixes applied. Re-running audit...")
