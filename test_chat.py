import urllib.request
import urllib.error
import json

url = "http://127.0.0.1:8000/chat"
payload = json.dumps({"message": "What is UPI?"}).encode()

req = urllib.request.Request(
    url,
    data=payload,
    headers={"Content-Type": "application/json"},
    method="POST",
)

try:
    with urllib.request.urlopen(req, timeout=30) as resp:
        print("STATUS:", resp.status)
        print(json.dumps(json.loads(resp.read()), indent=2, ensure_ascii=False))
except urllib.error.HTTPError as e:
    print("HTTP ERROR:", e.code)
    print(e.read().decode("utf-8", errors="replace"))
except Exception as ex:
    print("ERROR:", ex)
