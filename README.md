# FinSaathi — AI Agent for Digital Financial Literacy
### IBM Problem Statement #7 | Powered by IBM Granite + RAG

---

## 🎯 Overview

**FinSaathi** is an AI-powered Digital Financial Literacy Agent that helps Indian users navigate essential financial tools and practices. It uses **Retrieval-Augmented Generation (RAG)** to provide accurate, source-grounded answers about:

- 💳 **UPI & Digital Payments** — how to send/receive money, UPI IDs, daily limits
- 🛡️ **Fraud Prevention** — phishing, vishing, UPI scams, OLX fraud, what to do if scammed
- 📊 **Interest Rates & Loans** — safe rates, EMI calculation, CIBIL scores
- 💰 **Budgeting & Savings** — 50/30/20 rule, emergency fund, savings goals
- 🏛️ **Government Schemes** — PM Jan Dhan, MUDRA loans, APY, PMSBY, PMJJBY
- 📈 **Investments & Insurance** — FD, SIP, PPF, term life, health insurance

**Multilingual Support**: Users can ask questions in **12 Indian languages** — Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Punjabi, Malayalam, Odia, Urdu, and English.

---

## 🏗️ Architecture

```
User (any language)
       │
       ▼
┌─────────────────────────┐
│   FastAPI Backend        │
│   Language Detection     │  ← langdetect
│   Translation Layer      │  ← deep-translator (Google Translate)
└──────────┬──────────────┘
           │ English query
           ▼
┌─────────────────────────┐
│   RAG Pipeline           │
│   ┌───────────────────┐ │
│   │  ChromaDB Vector  │ │  ← multilingual-e5-base embeddings
│   │  Knowledge Base   │ │    (12 financial topic documents)
│   └─────────┬─────────┘ │
│             │ top-3 docs  │
│             ▼            │
│   IBM Granite 3-8B-Instruct │  ← ibm-watsonx-ai SDK
│   (grounded generation)  │
└──────────┬──────────────┘
           │ English answer
           ▼
   Translation back → User language
           │
           ▼
   Chat Interface (HTML/CSS/JS)
```

### Key Design Decisions
| Component | Choice | Reason |
|---|---|---|
| LLM | IBM Granite 3-8B-Instruct | **Mandatory** per problem statement; strong instruction-following |
| Embeddings | `multilingual-e5-base` | Excellent on Indian scripts; runs locally (no extra API cost) |
| Vector DB | ChromaDB | Lightweight, no server needed, persistent on disk |
| Translation | `deep-translator` (Google Translate) | Reliable for 12 Indian languages |
| Backend | FastAPI | Async, fast, auto-generated OpenAPI docs |
| Frontend | Vanilla HTML/CSS/JS | Zero dependencies, works on any device |

---

## 📁 Project Structure

```
Digital Fin Lit -- IBM/
├── main.py              ← FastAPI app + REST endpoints
├── rag_engine.py        ← ChromaDB + Granite RAG pipeline
├── knowledge_base.py    ← 12 curated financial documents
├── multilingual.py      ← Language detection + translation
├── requirements.txt     ← Python dependencies
├── .env.example         ← Environment variable template
├── static/
│   └── index.html       ← Full chat UI (single-page app)
└── data/
    └── chroma_db/       ← Auto-created: vector index (persistent)
```

---

## 🚀 Quick Start

### Prerequisites
- Python 3.10+
- IBM Cloud Lite account with watsonx.ai enabled ([cloud.ibm.com](https://cloud.ibm.com))

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure IBM Credentials
```bash
cp .env.example .env
```
Edit `.env` and fill in:
```env
IBM_API_KEY=your_ibm_cloud_api_key
IBM_PROJECT_ID=your_watsonx_project_id
IBM_WATSONX_URL=https://us-south.ml.cloud.ibm.com
```

**How to get IBM credentials:**
1. Log in to [cloud.ibm.com](https://cloud.ibm.com)
2. Create a **watsonx.ai** service (Lite tier is free)
3. Create a **project** in watsonx.ai Studio
4. Generate an **API key** under Manage → Access → API Keys
5. Copy your **Project ID** from the project settings

### 3. Run the Application
```bash
python main.py
```
Open your browser at: **http://localhost:8000**

### 4. API Documentation
Auto-generated Swagger UI: **http://localhost:8000/docs**

---

## 🌐 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Serves the chat UI |
| `GET` | `/health` | Health check + IBM config status |
| `POST` | `/chat` | Main chat endpoint (RAG pipeline) |
| `GET` | `/categories` | Topic categories for UI chips |
| `GET` | `/suggest?category=upi` | Suggested questions per category |

### Example Chat Request
```bash
curl -X POST http://localhost:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "UPI से पैसे कैसे भेजें?", "language": "hi"}'
```

### Example Response
```json
{
  "answer": "UPI से पैसे भेजने के लिए...",
  "detected_language": "hi",
  "language_name": "Hindi (हिन्दी)",
  "sources": ["NPCI / RBI Guidelines"],
  "categories": ["upi"],
  "retrieved_docs": [
    {"title": "How to Send Money via UPI", "source": "NPCI / RBI Guidelines", "score": 0.94}
  ],
  "response_time_ms": 1240
}
```

---

## 🌍 Supported Languages

| Code | Language | Script |
|---|---|---|
| `en` | English | Latin |
| `hi` | Hindi | Devanagari |
| `ta` | Tamil | Tamil |
| `te` | Telugu | Telugu |
| `bn` | Bengali | Bengali |
| `mr` | Marathi | Devanagari |
| `gu` | Gujarati | Gujarati |
| `kn` | Kannada | Kannada |
| `pa` | Punjabi | Gurmukhi |
| `ml` | Malayalam | Malayalam |
| `or` | Odia | Odia |
| `ur` | Urdu | Arabic |

---

## 🔒 Safety Features

1. **Fraud Alert System** — Detects urgency keywords (e.g., "someone asked my OTP") and prepends an immediate safety alert before answering
2. **Grounded Responses** — All answers are sourced from verified RBI/NPCI/Government content; the model cannot hallucinate facts not in the knowledge base
3. **Source Attribution** — Every response shows which document/portal the information came from
4. **Quick Answers** — Common safety terms (UPI PIN, 1930 helpline) return instant hardcoded answers, bypassing any potential model error

---

## 📚 Knowledge Base Sources

All documents are sourced from official Indian government and regulatory portals:
- **RBI** (Reserve Bank of India) — rbi.org.in
- **NPCI** (National Payments Corporation of India) — npci.org.in
- **cybercrime.gov.in** — National Cyber Crime Reporting Portal
- **SEBI** — sebi.gov.in (investment regulations)
- **IRDAI** — irdai.gov.in (insurance regulations)
- **Ministry of Finance** — Jan Dhan, MUDRA, APY schemes
- **AMFI** — amfiindia.com (mutual fund education)

---

## 🛠️ Extending the Knowledge Base

To add new financial topics:
1. Open `knowledge_base.py`
2. Add a new dict to the `FINANCIAL_DOCUMENTS` list with the schema:
```python
{
    "id": "unique_id",
    "category": "category_key",
    "title": "Document Title",
    "content": "...",
    "source": "Source Portal",
    "tags": ["tag1", "tag2"],
}
```
3. Restart the server — the document will be auto-embedded and indexed on startup

---

## 📄 License

This project is submitted for the IBM Problem Statement #7 — AI Agent for Digital Financial Literacy.
Built with IBM Cloud Lite services and IBM Granite language model.
