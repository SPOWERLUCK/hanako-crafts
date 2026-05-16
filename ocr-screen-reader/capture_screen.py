"""Screen capture for Hanako — saves screenshot on demand"""
import os, time, threading
from datetime import datetime
from PIL import ImageGrab

OUT_DIR = "D:/ComfyUI_V1.1/ComfyUI_windows_portable/ComfyUI/output/screenshots"
os.makedirs(OUT_DIR, exist_ok=True)
print(f"[Capture] Listening for triggers. Screenshots saved to {OUT_DIR}")
print("[Capture] Type 'shot' and Enter to capture, 'q' to quit.")

while True:
    cmd = input().strip().lower()
    if cmd == "q":
        break
    elif cmd == "shot":
        ts = datetime.now().strftime("%H%M%S")
        path = os.path.join(OUT_DIR, f"screen_{ts}.png")
        img = ImageGrab.grab()
        img.save(path)
        print(f"[Capture] Saved: {path} ({img.size})")
    elif cmd == "":
        pass
    else:
        print("[Capture] Unknown. 'shot' to capture, 'q' to quit.")
