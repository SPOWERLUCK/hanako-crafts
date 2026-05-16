"""hanako_emotion.py — 一行切换桌宠情绪（直连 MCP bridge）"""
import sys, json
from urllib.request import Request, urlopen

EMOTIONS = ["thinking","working","idle","happy","sleeping","frustrated","tired","waiting","questioning","concentrating","proud"]

if len(sys.argv) < 2:
    print(f"usage: hanako_emotion.py <emotion> [intensity]")
    print(f"emotions: {', '.join(EMOTIONS)}")
    sys.exit(1)

em = sys.argv[1]
intensity = float(sys.argv[2]) if len(sys.argv) > 2 else 0.8

if em == "proud": em = "happy"

data = json.dumps({
    "jsonrpc":"2.0","id":1,"method":"tools/call",
    "params":{"name":"hanako_emotion","arguments":{"emotion":em,"intensity":intensity}}
}).encode()

req = Request("http://127.0.0.1:19742/", data=data, headers={"Content-Type":"application/json"})
resp = urlopen(req, timeout=3)
result = json.loads(resp.read())
print(f"OK: {em} ({intensity})")
