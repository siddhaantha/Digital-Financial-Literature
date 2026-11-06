"""
rag_engine.py
RAG (Retrieval-Augmented Generation) pipeline using:
  - ChromaDB for vector storage
  - Sentence Transformers for embeddings
  - IBM Granite (via ibm-watsonx-ai) for generation
"""

import os
import logging
from typing import Optional
from dotenv import load_dotenv

import chromadb
from chromadb.config import Settings
from sentence_transformers import SentenceTransformer

from knowledge_base import FINANCIAL_DOCUMENTS

load_dotenv()
logger = logging.getLogger(__name__)

# ── Configuration ──────────────────────────────────────────────────────────────
IBM_API_KEY    = os.getenv("IBM_API_KEY", "")
IBM_PROJECT_ID = os.getenv("IBM_PROJECT_ID", "")
IBM_WX_URL     = os.getenv("IBM_WATSONX_URL", "https://us-south.ml.cloud.ibm.com")
GRANITE_MODEL  = os.getenv("GRANITE_MODEL_ID", "ibm/granite-4-h-small")
CHROMA_DIR     = os.getenv("CHROMA_PERSIST_DIR", "./data/chroma_db")
COLLECTION_NAME = "financial_literacy"

# ── Embedding Model ────────────────────────────────────────────────────────────
# Uses multilingual-e5-base: excellent on Indian languages, runs locally (no API cost)
EMBED_MODEL_NAME = "intfloat/multilingual-e5-base"


class RAGEngine:
    """
    Core RAG engine:
      1. Indexes the curated financial knowledge base into ChromaDB.
      2. Retrieves the most relevant documents for a user query.
      3. Calls IBM Granite to generate a grounded, accurate response.
    """

    def __init__(self):
        self._embed_model: Optional[SentenceTransformer] = None
        self._chroma_client: Optional[chromadb.PersistentClient] = None
        self._collection = None
        self._watsonx_model = None
        self._ibm_available = False

    # ── Lazy Initialisation ────────────────────────────────────────────────────

    def _get_embed_model(self) -> SentenceTransformer:
        if self._embed_model is None:
            logger.info("Loading embedding model: %s", EMBED_MODEL_NAME)
            self._embed_model = SentenceTransformer(EMBED_MODEL_NAME)
        return self._embed_model

    def _get_chroma_collection(self):
        if self._collection is not None:
            return self._collection
        os.makedirs(CHROMA_DIR, exist_ok=True)
        self._chroma_client = chromadb.PersistentClient(
            path=CHROMA_DIR,
            settings=Settings(anonymized_telemetry=False),
        )
        self._collection = self._chroma_client.get_or_create_collection(
            name=COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )
        return self._collection

    def _get_watsonx_model(self):
        """Lazily initialise IBM Granite via watsonx.ai SDK."""
        if self._watsonx_model is not None:
            return self._watsonx_model
        if not IBM_API_KEY or not IBM_PROJECT_ID:
            logger.warning("IBM credentials not set — using fallback response mode.")
            self._ibm_available = False
            return None
        try:
            from ibm_watsonx_ai import Credentials
            from ibm_watsonx_ai.foundation_models import ModelInference
            from ibm_watsonx_ai.metanames import GenTextParamsMetaNames as GenParams

            creds = Credentials(url=IBM_WX_URL, api_key=IBM_API_KEY)
            params = {
                GenParams.MAX_NEW_TOKENS: 1024,
                GenParams.MIN_NEW_TOKENS: 50,
                GenParams.TEMPERATURE: 0.3,
                GenParams.TOP_P: 0.9,
                GenParams.REPETITION_PENALTY: 1.1,
                GenParams.STOP_SEQUENCES: ["Human:", "User:"],
            }
            self._watsonx_model = ModelInference(
                model_id=GRANITE_MODEL,
                credentials=creds,
                project_id=IBM_PROJECT_ID,
                params=params,
            )
            self._ibm_available = True
            logger.info("IBM Granite model initialised: %s", GRANITE_MODEL)
        except Exception as exc:
            logger.error("Failed to initialise IBM Granite: %s", exc)
            self._ibm_available = False
        return self._watsonx_model

    # ── Index Building ─────────────────────────────────────────────────────────

    def build_index(self) -> int:
        """
        Embed all documents from the knowledge base and store in ChromaDB.
        Returns the number of documents indexed.
        Skips documents already present (idempotent).
        """
        collection = self._get_chroma_collection()
        model = self._get_embed_model()

        existing_ids = set(collection.get()["ids"])
        new_docs = [d for d in FINANCIAL_DOCUMENTS if d["id"] not in existing_ids]

        if not new_docs:
            logger.info("Index already up-to-date (%d documents).", len(existing_ids))
            return len(existing_ids)

        # multilingual-e5-base requires "passage: " prefix for indexed documents
        texts = [f"{d['title']}\n{d['content']}" for d in new_docs]
        prefixed = [f"passage: {t}" for t in texts]
        embeddings = model.encode(prefixed, normalize_embeddings=True).tolist()

        collection.add(
            ids=[d["id"] for d in new_docs],
            embeddings=embeddings,
            documents=texts,
            metadatas=[
                {
                    "category": d["category"],
                    "title": d["title"],
                    "source": d["source"],
                    "tags": ", ".join(d.get("tags", [])),
                }
                for d in new_docs
            ],
        )
        total = len(existing_ids) + len(new_docs)
        logger.info("Indexed %d new documents. Total: %d", len(new_docs), total)
        return total

    # ── Retrieval ──────────────────────────────────────────────────────────────

    def retrieve(self, query_en: str, n_results: int = 3) -> list[dict]:
        """
        Retrieve the top-n most relevant documents for an English query.
        Returns a list of dicts with keys: title, content, source, category.
        """
        collection = self._get_chroma_collection()
        model = self._get_embed_model()

        # multilingual-e5-base requires "query: " prefix for query embeddings
        query_embedding = model.encode([f"query: {query_en}"], normalize_embeddings=True).tolist()
        results = collection.query(
            query_embeddings=query_embedding,
            n_results=min(n_results, collection.count()),
            include=["documents", "metadatas", "distances"],
        )

        retrieved = []
        for doc, meta, dist in zip(
            results["documents"][0],
            results["metadatas"][0],
            results["distances"][0],
        ):
            retrieved.append(
                {
                    "title": meta.get("title", ""),
                    "content": doc,
                    "source": meta.get("source", ""),
                    "category": meta.get("category", ""),
                    "relevance_score": round(1 - dist, 3),
                }
            )
        return retrieved

    # ── Generation ─────────────────────────────────────────────────────────────

    def _build_prompt(self, user_query: str, context_docs: list[dict]) -> str:
        """Build the prompt for IBM Granite with retrieved context."""
        context_text = ""
        for i, doc in enumerate(context_docs, 1):
            context_text += (
                f"\n[Document {i}] {doc['title']} (Source: {doc['source']})\n"
                f"{doc['content'][:1200]}\n"
                f"{'─' * 60}\n"
            )

        prompt = f"""<|system|>
You are a helpful, trustworthy Digital Financial Literacy Assistant for Indian users.
Your role is to educate users about UPI payments, online fraud prevention, interest rates,
budgeting, savings, government schemes, and personal finance.

RULES:
1. Answer ONLY based on the provided context documents. Do not invent information.
2. Be clear, simple, and practical — many users may be first-time digital finance learners.
3. Always warn about safety risks when relevant (e.g. UPI PIN, OTP, scams).
4. If the user's question is not covered by the context, say so politely and suggest they
   visit rbi.org.in, npci.org.in, or cybercrime.gov.in for authoritative guidance.
5. Format responses with clear numbered steps or bullet points when appropriate.
6. Keep responses concise (under 300 words) but complete.
<|user|>
CONTEXT DOCUMENTS:
{context_text}

USER QUESTION: {user_query}
<|assistant|>"""
        return prompt

    def generate(self, query_en: str, context_docs: list[dict], target_lang: str = "en") -> str:
        """Generate a response using IBM Granite with the retrieved context."""
        model = self._get_watsonx_model()
        prompt = self._build_prompt(query_en, context_docs)

        if model and self._ibm_available:
            try:
                response = model.generate_text(prompt=prompt)
                return response.strip() if response else self._fallback_response(query_en, context_docs, target_lang)
            except Exception as exc:
                logger.error("Granite generation error: %s", exc)
                return self._fallback_response(query_en, context_docs, target_lang)
        else:
            return self._fallback_response(query_en, context_docs, target_lang)

    def _fallback_response(
        self, query_en: str, context_docs: list[dict], target_lang: str = "en"
    ) -> str:
        """
        Deterministic fallback when IBM Granite is unavailable.
        Extracts the most relevant excerpt from the top retrieved document,
        ending at a section boundary, and translates it into target_lang.
        """
        from multilingual import translate_from_english

        if not context_docs:
            body = (
                "I'm sorry, I couldn't find specific information on that topic in my "
                "knowledge base. For authoritative guidance on financial matters, please "
                "visit rbi.org.in or call the RBI helpline at 14448."
            )
            return translate_from_english(body, target_lang)

        top_doc = context_docs[0]
        content = top_doc["content"].strip()

        # Split into sections on ALL-CAPS header lines (e.g. "HOW IT WORKS:")
        # Keep at most 2 complete sections to avoid a wall of text.
        import re
        section_pattern = re.compile(r'^[A-Z][A-Z\s&/()–-]{3,}:?\s*$', re.MULTILINE)
        splits = section_pattern.split(content)
        headers = section_pattern.findall(content)

        if len(splits) > 1:
            # Reconstruct: title intro + first full section
            intro = splits[0].strip()
            first_section = (headers[0].strip() + "\n" + splits[1].strip()) if headers else splits[1].strip()
            excerpt = (top_doc["title"] + "\n\n" + intro + "\n\n" + first_section).strip()
        else:
            # No section headers found — take the first 20 non-empty lines
            lines = [l.strip() for l in content.split("\n") if l.strip()]
            excerpt = top_doc["title"] + "\n\n" + "\n".join(lines[:20])

        # Translate the knowledge-base excerpt into the user's language
        translated_excerpt = translate_from_english(excerpt, target_lang)

        # Keep the technical note in English (env var names must not be translated)
        note = (
            "Note: IBM Granite AI is not configured. Showing curated knowledge base content.\n"
            "Set `IBM_API_KEY` and `IBM_PROJECT_ID` in your .env file to enable full AI responses."
        )

        return f"{translated_excerpt}\n\n📌 Source: {top_doc['source']}\n\n{note}"

    # ── Full RAG Pipeline ──────────────────────────────────────────────────────

    def answer(self, query_en: str, target_lang: str = "en") -> dict:
        """
        Full RAG pipeline: retrieve → generate.
        Returns dict with keys: answer, sources, category.
        target_lang is passed to fallback so it can translate the excerpt.
        When in fallback mode, sources lists only the top doc shown.
        """
        docs = self.retrieve(query_en, n_results=3)
        answer_text = self.generate(query_en, docs, target_lang=target_lang)

        # If Granite is unavailable the fallback shows only docs[0].
        # Report only that source to avoid misleading multi-source attribution.
        if not self._ibm_available and docs:
            sources = [docs[0]["source"]]
        else:
            sources = list(dict.fromkeys(d["source"] for d in docs))  # ordered-unique

        categories = list(dict.fromkeys(d["category"] for d in docs))

        return {
            "answer": answer_text,
            "sources": sources,
            "categories": categories,
            "retrieved_docs": [
                {"title": d["title"], "source": d["source"], "score": d["relevance_score"]}
                for d in docs
            ],
        }


# Module-level singleton
_engine: Optional[RAGEngine] = None


def get_engine() -> RAGEngine:
    """Return (and lazily initialise) the global RAG engine singleton."""
    global _engine
    if _engine is None:
        _engine = RAGEngine()
        _engine.build_index()
    return _engine
