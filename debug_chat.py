"""
debug_chat.py — Calls the chat route handler directly (no HTTP) to get the full traceback.
"""
import asyncio, traceback, sys

# Ensure local modules resolve
sys.path.insert(0, ".")

async def main():
    from main import chat
    from main import ChatRequest
    req = ChatRequest(message="What is UPI?")
    try:
        result = await chat(req)
        import json
        print(json.dumps(result.model_dump(), indent=2, ensure_ascii=False))
    except Exception:
        traceback.print_exc()

asyncio.run(main())
