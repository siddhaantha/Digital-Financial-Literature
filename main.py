"""
main.py
FastAPI backend for the Digital Financial Literacy AI Agent.
Exposes REST endpoints consumed by the frontend chat interface.
"""

import logging
import time
from contextlib import asynccontextmanager
from typing import Optional

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field

from rag_engine import get_engine
from multilingual import (
    detect_language,
    translate_to_english,
    translate_from_english,
    SUPPORTED_LANGUAGES,
    get_language_greeting,
)
from knowledge_base import CATEGORIES, QUICK_ANSWERS

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)


# ── Lifespan: warm up the RAG engine at startup ────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initialising RAG engine and building index...")
    engine = get_engine()
    logger.info("RAG engine ready.")
    yield
    logger.info("Shutting down.")


# ── App ────────────────────────────────────────────────────────────────────────

app = FastAPI(
    title="Digital Financial Literacy AI Agent",
    description=(
        "AI-powered financial literacy assistant for Indian users. "
        "Covers UPI, fraud prevention, interest rates, budgeting, "
        "government schemes, and personal finance. "
        "Powered by IBM Granite + RAG."
    ),
    version="1.0.0",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

# Serve the static frontend
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Request / Response Models ──────────────────────────────────────────────────

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="User's question")
    language: Optional[str] = Field(None, description="ISO language code override (e.g. 'hi')")
    session_id: Optional[str] = Field(None, description="Optional session identifier")


class SourceDoc(BaseModel):
    title: str
    source: str
    score: float


class ChatResponse(BaseModel):
    answer: str
    detected_language: str
    language_name: str
    sources: list[str]
    categories: list[str]
    retrieved_docs: list[SourceDoc]
    response_time_ms: int


class HealthResponse(BaseModel):
    status: str
    ibm_granite_configured: bool
    documents_indexed: int
    supported_languages: dict[str, str]


# ── Helpers ────────────────────────────────────────────────────────────────────

def _check_quick_answer(query_lower: str) -> Optional[str]:
    """Return an instant answer for extremely common, simple queries."""
    for keyword, answer in QUICK_ANSWERS.items():
        if keyword in query_lower:
            return answer
    return None


def _detect_fraud_alert(query_lower: str) -> Optional[str]:
    """
    Prepend an urgent safety alert if the user's query suggests they may be
    currently being defrauded.
    """
    urgent_phrases = [
        "someone asked my otp", "share otp", "give otp",
        "share upi pin", "give upi pin", "customer care asked",
        "i got scammed", "money deducted", "unauthorized transaction",
        "i sent money by mistake", "collect request",
    ]
    for phrase in urgent_phrases:
        if phrase in query_lower:
            return (
                "⚠️ URGENT SAFETY ALERT: If you are being asked to share your OTP or UPI PIN, "
                "DO NOT share it. Hang up immediately. If money has already been deducted, "
                "call your bank's 24×7 helpline NOW and call Cyber Crime Helpline 1930."
            )
    return None


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/", response_class=FileResponse)
async def serve_frontend():
    """Serve the main chat interface."""
    return FileResponse("static/index.html")


@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Health check — confirms service is running and reports config status."""
    import os
    engine = get_engine()
    collection = engine._get_chroma_collection()
    return HealthResponse(
        status="healthy",
        ibm_granite_configured=bool(os.getenv("IBM_API_KEY") and os.getenv("IBM_PROJECT_ID")),
        documents_indexed=collection.count(),
        supported_languages=SUPPORTED_LANGUAGES,
    )


@app.get("/categories")
async def get_categories():
    """Return available knowledge categories for the frontend topic chips."""
    return {"categories": CATEGORIES}


@app.post("/chat", response_model=ChatResponse)
async def chat(req: ChatRequest):
    """
    Main chat endpoint — full RAG pipeline with multilingual support.

    Pipeline:
      1. Detect language of user message
      2. Translate to English for retrieval + generation
      3. Check for urgent fraud-alert keywords
      4. Retrieve relevant documents from ChromaDB
      5. Generate grounded response via IBM Granite
      6. Translate response back to user's language
      7. Return structured response with source attribution
    """
    t0 = time.perf_counter()

    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")

    # 1. Language detection
    detected_lang = req.language or detect_language(req.message)
    if detected_lang not in SUPPORTED_LANGUAGES:
        detected_lang = "en"

    # 2. Translate query to English
    query_en = translate_to_english(req.message, source_lang=detected_lang)
    query_lower = query_en.lower()

    logger.info(
        "Query | lang=%s | original=%r | english=%r",
        detected_lang, req.message[:80], query_en[:80],
    )

    # 3. Fraud / urgency detection
    urgent_alert = _detect_fraud_alert(query_lower)

    # 4. Quick answers (bypass full RAG for trivial lookups)
    quick = _check_quick_answer(query_lower)
    if quick:
        final_answer = urgent_alert + "\n\n" + quick if urgent_alert else quick
        final_answer_translated = translate_from_english(final_answer, detected_lang)
        elapsed_ms = int((time.perf_counter() - t0) * 1000)
        return ChatResponse(
            answer=final_answer_translated,
            detected_language=detected_lang,
            language_name=SUPPORTED_LANGUAGES[detected_lang],
            sources=["Digital Financial Literacy Knowledge Base"],
            categories=["online_safety"],
            retrieved_docs=[],
            response_time_ms=elapsed_ms,
        )

    # 5 & 6. Full RAG pipeline
    engine = get_engine()
    rag_result = engine.answer(query_en, target_lang=detected_lang)
    answer_en = rag_result["answer"]

    # Prepend urgent alert if needed
    if urgent_alert:
        answer_en = urgent_alert + "\n\n" + answer_en

    # 7. Translate answer back to user's language
    final_answer = translate_from_english(answer_en, detected_lang)

    elapsed_ms = int((time.perf_counter() - t0) * 1000)
    logger.info("Response | lang=%s | time=%dms", detected_lang, elapsed_ms)

    return ChatResponse(
        answer=final_answer,
        detected_language=detected_lang,
        language_name=SUPPORTED_LANGUAGES[detected_lang],
        sources=rag_result["sources"],
        categories=rag_result["categories"],
        retrieved_docs=[SourceDoc(**d) for d in rag_result["retrieved_docs"]],
        response_time_ms=elapsed_ms,
    )


@app.get("/suggest")
async def get_suggestions(category: Optional[str] = None):
    """Return suggested questions, optionally filtered by category."""
    all_suggestions = {
        "upi": [
            "How do I send money via UPI?",
            "What is a UPI PIN and how do I create one?",
            "What are the daily UPI transaction limits?",
            "Someone asked for my UPI PIN to send money — is this safe?",
        ],
        "online_safety": [
            "How do I protect myself from online fraud?",
            "What should I do if I get scammed?",
            "How do I identify a phishing message?",
            "What is a collect request scam?",
        ],
        "interest_rates": [
            "What is a safe interest rate for a personal loan?",
            "How do I calculate EMI for a home loan?",
            "What is a CIBIL score and why does it matter?",
            "What is compound interest?",
        ],
        "budgeting": [
            "How do I create a monthly budget?",
            "What is the 50/30/20 rule?",
            "How much should I save for an emergency fund?",
            "How do I start saving money?",
        ],
        "government_schemes": [
            "What is PM Jan Dhan Yojana?",
            "How do I apply for a MUDRA loan?",
            "What government insurance schemes are free?",
            "What is Atal Pension Yojana?",
        ],
        "financial_planning": [
            "How should a beginner start investing?",
            "What is a SIP in mutual funds?",
            "Should I buy term insurance or endowment plan?",
            "What are tax-saving investments under Section 80C?",
        ],
    }
    if category and category in all_suggestions:
        return {"suggestions": all_suggestions[category]}
    # Return 2 from each category
    mixed = []
    for suggestions in all_suggestions.values():
        mixed.extend(suggestions[:2])
    return {"suggestions": mixed}


# ── Entry Point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn
    import os
    port = int(os.getenv("APP_PORT", 8000))
    host = os.getenv("APP_HOST", "0.0.0.0")
    uvicorn.run("main:app", host=host, port=port, reload=True)
