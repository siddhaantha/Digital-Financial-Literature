import sys, json, urllib.request, urllib.error

def test(label, payload):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(
        "http://127.0.0.1:8000/chat",
        data=data,
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=40) as resp:
            d = json.loads(resp.read())
            print(f"=== {label} ===")
            print(f"  HTTP 200 | lang={d['detected_language']} ({d['language_name']}) | {d['response_time_ms']}ms")
            print(f"  top_doc : {d['retrieved_docs'][0]['title']} (score {d['retrieved_docs'][0]['score']})")
            print(f"  sources : {d['sources']}")
            print(f"  answer  : {d['answer'][:300]}")
            print()
    except urllib.error.HTTPError as e:
        print(f"=== {label} === HTTP {e.code}: {e.read().decode()}")

test("English  — what is upi?",           {"message": "what is upi?"})
test("Kannada  — UPI ಎಂದರೇನು?",          {"message": "UPI \u0c8e\u0c82\u0ca6\u0cb0\u0cc7\u0ca8\u0cc1?"})
test("Hindi    — UPI क्या है?",            {"message": "UPI \u0915\u094d\u092f\u093e \u0939\u0948?"})
