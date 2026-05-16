#!/usr/bin/env pythonw
"""MJPEG screen stream — Hanako can poll to see your screen"""
import os, io, time, threading
from http.server import HTTPServer, BaseHTTPRequestHandler
from PIL import ImageGrab

PORT = 9750
INTERVAL = 0.3
SCREENSHOT_DIR = "H:/hanako_Project/tools/screenshots"
os.makedirs(SCREENSHOT_DIR, exist_ok=True)

_current_frame = None
_ocr_frame = None
_running = True

def capture_loop():
    global _current_frame, _ocr_frame
    while _running:
        try:
            img = ImageGrab.grab()
            # Low-res for streaming (1280px)
            if img.size[0] > 1280:
                ratio = 1280 / img.size[0]
                low = img.resize((1280, int(img.size[1] * ratio)))
            else:
                low = img
            buf = io.BytesIO()
            low.save(buf, "JPEG", quality=60)
            _current_frame = buf.getvalue()
            # Full-res for OCR
            buf2 = io.BytesIO()
            img.save(buf2, "JPEG", quality=92)
            _ocr_frame = buf2.getvalue()
        except:
            pass
        time.sleep(INTERVAL)

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/screen.jpg":
            if _current_frame:
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", len(_current_frame))
                self.end_headers()
                self.wfile.write(_current_frame)
            else:
                self.send_response(503)
                self.end_headers()
        elif self.path == "/ocr.jpg":
            if _ocr_frame:
                self.send_response(200)
                self.send_header("Content-Type", "image/jpeg")
                self.send_header("Content-Length", len(_ocr_frame))
                self.end_headers()
                self.wfile.write(_ocr_frame)
            else:
                self.send_response(503)
                self.end_headers()
        elif self.path == "/":
            self.send_response(200)
            self.send_header("Content-Type", "text/html")
            self.end_headers()
            self.wfile.write(b"<html><body><img src='/screen.jpg' style='max-width:100%'><script>setInterval(()=>{document.querySelector('img').src='/screen.jpg?'+Date.now()},300)</script></body></html>")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, *args):
        pass

threading.Thread(target=capture_loop, daemon=True).start()
print(f"[Screen Stream] http://127.0.0.1:{PORT}/screen.jpg | HTML: http://127.0.0.1:{PORT}/")
HTTPServer(("127.0.0.1", PORT), Handler).serve_forever()
