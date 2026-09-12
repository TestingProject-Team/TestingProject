import os
from PIL import Image

dirs = [
    r"E:\TestingProject\ảnh file docx\01_infographic",
    r"E:\TestingProject\ảnh file docx\02_standard"
]

print("=== IMAGE VALIDATION & MARGIN REPORT ===")
for d in dirs:
    print(f"\nScanning: {os.path.basename(d)}")
    files = [f for f in os.listdir(d) if f.endswith(".png")]
    for f in sorted(files):
        p = os.path.join(d, f)
        img = Image.open(p)
        w, h = img.size
        print(f" - {f}: {w}x{h} px | DPI: {img.info.get('dpi', 'N/A')} | Mode: {img.mode}")
