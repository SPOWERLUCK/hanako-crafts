"""Hanako 状态控制 CLI — MCP 桌宠直连"""

import sys, json
from urllib.request import urlopen, Request

HOST = "http://127.0.0.1:19741"

EMOTIONS = {
    "working":     ("working", 0.8),
    "thinking":    ("thinking", 0.9),
    "idle":        ("idle", 0.5),
    "proud":       ("happy", 0.9),
    "sleeping":    ("sleeping", 0.3),
    "frustrated":  ("frustrated", 0.7),
    "tired":       ("tired", 0.4),
    "waiting":     ("waiting", 0.6),
    "questioning": ("questioning", 0.7),
    "happy":       ("happy", 0.85),
    "concentrating": ("concentrating", 0.9),
    "composing":    ("concentrating", 0.75),
    "done":         ("happy", 0.95),
}


def main():
    if len(sys.argv) < 2:
        print("usage: hanako_state.py <emotion>")
        print(f"emotions: {', '.join(EMOTIONS)}")
        return 1

    action = sys.argv[1]
    msg = " ".join(sys.argv[2:]) if len(sys.argv) > 2 else ""

    if action not in EMOTIONS:
        print(f"未知情绪: {action}")
        return 1

    em, intensity = EMOTIONS[action]
    data = json.dumps({"emotion": em, "intensity": intensity}).encode()
    req = Request(f"{HOST}/emotion", data=data, headers={"Content-Type": "application/json"})
    try:
        resp = urlopen(req, timeout=3)
        result = json.loads(resp.read())
        print(f"OK: {action} → {em} ({intensity})")
    except Exception as e:
        print(f"ERR: {e}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
