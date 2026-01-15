# Enterprise Knowledge RAG System

## 📌 Overview
This project is a production-oriented **Retrieval-Augmented Generation (RAG)** system designed specifically for enterprise knowledge bases. 

The core focus of this system is **correctness, traceability, observability, and safe deployment** rather than raw text generation. Unlike typical demo RAG projects, this architecture implements evaluation, logging, monitoring, and governance layers required in real-world AI environments.

> **Note:** In production mode, answer generation can be disabled to eliminate dependency on paid LLMs, while retrieval, evaluation, logging, and monitoring remain fully operational.

---

## 🚀 Key Features

### Advanced Retrieval Pipeline
* **Hybrid Retrieval:** Combines dense vector retrieval (**FAISS**) with sparse retrieval (**BM25**).
* **Query Optimization:** Includes query rewriting and multi-query expansion for improved recall.
* **Reranking:** LLM-based reranking with deterministic fallbacks to ensure the most relevant context is prioritized.

### Answer Generation (Local / Development)
* **Strict Grounding:** Prompting is engineered to ensure no external knowledge injection.
* **Safe Fallbacks:** Automatic fallback mechanisms when retrieved context is insufficient.
* **Deterministic Output:** Temperature settings optimized for consistency.

### Evaluation and Quality Control
* **LLM-as-a-Judge:** Faithfulness scoring and hallucination detection.
* **Agreement Metrics:** Comparison between human and LLM evaluation.
* **Non-Blocking:** Passive evaluation ensures system performance is not degraded.

### Asynchronous Evaluation Pipeline
* **Background Processing:** Evaluation runs asynchronously to maintain low user latency.
* **Resilience:** Evaluation failures do not impact the core serving path.

### Persistent Logging and Analytics (Supabase)
* **Auditability:** Structured schemas for query, answer, and evaluation logging.
* **Time-Series Metrics:** Aggregation using PostgreSQL RPC for high-performance analytics.

### Monitoring and Admin Dashboard
* **Health Tracking:** Monitor query volume and grounded vs. hallucinated answer rates.
* **Alerting:** Proactive detection of system degradation or low-score trends.

---

## 🏗 System Architecture Flow



1.  **User submits query**
2.  **Intent classification** (Routing only, non-blocking)
3.  **Query rewriting** & Multi-query expansion
4.  **Hybrid retrieval** (FAISS + BM25)
5.  **LLM-based reranking**
6.  **Context-grounded answer generation**
7.  **Synchronous database logging**
8.  **Asynchronous evaluation pipeline**
9.  **Metrics aggregation and alerts**

---

## 🛠 Tech Stack

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | FastAPI |
| **Vector Store** | FAISS |
| **Embeddings** | Nomic Embed |
| **Language Models** | Ollama (Local/Dev) |
| **Database** | Supabase (PostgreSQL) |
| **Evaluation** | Custom LLM-as-Judge Pipeline |
| **Deployment** | Docker, Railway |

---

## 📂 Project Structure

```text
├── api/                # FastAPI app, admin routes, metrics
├── retrieval/          # Intent class, rewriting, hybrid search, reranking
├── generation/         # Grounded answer generation
├── evaluation/         # Async evaluator, faithfulness scoring, alerts
├── db/                 # Database logging and Supabase utilities
├── config/             # Environment settings and feature flags
├── frontend/           # UI and Admin dashboard templates
├── data/               # Enterprise documents
└── index/              # FAISS vector index
```
⚙️ Configuration
----------------

System behavior is managed via environment variables to allow for seamless transitions between environments:

*   **Feature Flags:** Enable/disable generation or evaluation.
    
*   **Model Selection:** Configure embedding and generation models.
    
*   **Retrieval Parameters:** Fine-tune top-k results and reranking thresholds.
    

🧠 Design Philosophy
--------------------

*   **Correctness over Fluency:** Truthful answers are more valuable than "natural" sounding hallucinations.
    
*   **Observability First:** Never generate in the dark; every output must be logged and scored.
    
*   **Evaluation as a First-Class Citizen:** Evaluation is not an afterthought; it is integrated into the core lifecycle.
    
*   **Fail Safely:** The system is designed to fail gracefully rather than providing misleading information.

🔮 Future Extensions
--------------------

*   Authentication and Role-Based Access Control (RBAC).
    
*   Rate limiting and abuse prevention.
    
*   Multi-tenant knowledge base support.
    
*   Agentic RAG workflows for complex reasoning.
    
*   Document ingestion pipelines with OCR capabilities.
    

