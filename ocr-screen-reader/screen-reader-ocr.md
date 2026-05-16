# Screen Reader OCR Skill

## When to use
User asks you to "read the screen", "look at this", "OCR", "截屏识别", "看一眼", or you need to see what's on the desktop.

## How it works
Uses EasyOCR (pure Python, CPU-only, no GPU needed, no external binary) to capture the screen and extract text.

## One-time setup (user must do once)

```bash
pip install easyocr pillow
```

That's it. No Tesseract, no external installer, no GPU required.

## Usage — Standard flow

When the user asks you to read the screen, run this Python script:

```python
from PIL import ImageGrab
import easyocr

# Take screenshot
img = ImageGrab.grab()

# OCR with Chinese + English (CPU mode)
reader = easyocr.Reader(['ch_sim', 'en'], gpu=False)
result = reader.readtext(img)

# Print results — group by vertical position
for bbox, text, conf in result:
    if conf > 0.3 and len(text.strip()) > 1:
        print(f'[{conf:.2f}] {text}')
```

## Usage — Crop a region

```python
img = ImageGrab.grab(bbox=(left, top, right, bottom))
```

## Before running
1. Say "I'm checking your screen now"
2. Screenshots are in-memory only unless user asks to save

## Notes
- EasyOCR downloads model files (~200MB) on first run — one-time only
- Works entirely on CPU, zero GPU usage
- Best on clear text: code editors, web pages, chat windows
- Chinese recognition may be imperfect on stylized/artistic fonts
- For game UIs or image-heavy screens, results will be limited
- First run may take 30-60 seconds to load models; subsequent runs are faster
