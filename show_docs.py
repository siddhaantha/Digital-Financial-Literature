import sys, json
d = json.load(sys.stdin)
for i, r in enumerate(d["retrieved_docs"]):
    print(f"{i+1}. {r['title']} | score: {r['score']}")
