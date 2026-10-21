# 🛡️ PRODUCT REQUIREMENTS DOCUMENT (PRD)
## RAGNext — Autonomous Version-Aware Document Intelligence Engine with Verifiable Grounding

* **Document Version:** `v1.0`
* **Problem Statement ID:** `SH-SVA-04`
* **Team Name:** `Cyber Knights`
* **Authors:** Sainath Loganathan, Tahir Azeem
* **Target Release:** Hackathon Stage 2 Evaluation & Enterprise MVP
* **Classification:** Technical Specification & Product Requirements

---

## 1. Executive Summary & Product Vision

### 1.1 Product Vision
To build an enterprise-grade, offline-first Document Intelligence Engine that eliminates superseded document hallucinations by combining **Temporal Version Lineage Graphs**, **Pre-Retrieval Policy State Filtering**, and **Verifiable Page-Level Citation Grounding**. 

### 1.2 Core Principle
> *"Find the right information, from the right document version, with verifiable evidence."*

### 1.3 Problem Statement
Modern enterprises maintain hundreds of evolving standard operating procedures (SOPs), security guidelines, compliance manuals, and human resource policies. Conventional Retrieval-Augmented Generation (RAG) systems encode all document chunks into vector embeddings and retrieve information purely based on semantic cosine similarity.

When an organization updates a policy (e.g., from `v1.0` to `v2.0` to `v3.0`):
1. **Superseded Clause Hallucination:** Outdated clauses frequently score higher semantic similarity than newer clauses because of exact keyword matches.
2. **Missing Document Provenance:** Language models synthesize answers without indicating which revision was cited or whether the cited rule is legally binding.
3. **Silent Version Conflicts:** When multiple departments upload conflicting policies marked active at the same time, standard systems silently blend contradictory rules.
4. **Cloud Privacy Risk:** Transmitting confidential internal governance documents to public cloud AI APIs introduces severe data privacy and regulatory compliance liabilities.

### 1.4 The RAGNext Solution
RAGNext solves these systemic vulnerabilities through an autonomous, version-aware engine featuring:
* **Explicit Version Lineages:** Documents are grouped into lineage hierarchies (`Parent Group` ➔ `Versions v1.0, v2.0, v3.0...`).
* **State Lifecycle Management:** Enforces formal statuses (`DRAFT`, `ACTIVE`, `SUPERSEDED`, `ARCHIVED`).
* **Temporal Pre-Retrieval Filtering:** Filters out inactive revisions before vector retrieval executes.
* **Bi-directional Historical Querying:** Allows compliance officers to query past versions explicitly (e.g., *"What was the policy in 2023 under v1.0?"*) while protecting general users from superseded guidance.
* **Conflict Detection Engine:** Flags conflicting active versions before generation occurs.
* **100% Offline & Air-Gapped Operation:** Powered by local Ollama LLMs (`llama3.2`) and local embeddings (`nomic-embed-text`) with zero cloud dependencies.

---

## 2. Target Market, Personas & User Journeys

### 2.1 Target Segments
1. **Regulated Enterprises (BFSI, Healthcare, Legal, Defense):** Organizations subject to strict audit trails, ISO 27001, and NIST 800-53 standards.
2. **Enterprise HR, IT & Operations:** Departments frequently updating benefits, remote work security, and procurement policies.
3. **Internal Audit & Compliance Teams:** Teams conducting historical investigations or contract reconciliations.

### 2.2 User Personas

| Persona | Role | Primary Goal | Pain Point in Conventional RAG |
| :--- | :--- | :--- | :--- |
| **Rajesh (Compliance & Risk Lead)** | Ensures policy compliance & prepares audit defense | Audit past revisions, verify effective dates, detect contradictory rules | Search tools return outdated clauses; manual PDF cross-referencing takes days |
| **Priya (Knowledge Worker / Employee)** | Consults policies for day-to-day operations | Instant, accurate answers to policy questions (leave, security, BYOD) | Risks policy violation because search tools cite deprecated policies without warning |
| **Dev / IT Administrator** | Deploys and manages internal infrastructure | Maintain secure, low-latency, private document search | High cloud API costs, data leakage risks, complex vector DB maintenance |

### 2.3 User Journeys

#### A. Policy Consumer Journey (Default / Active Mode)
1. User opens **AI Document Chat**.
2. Submits question: *"What is the maximum allowed idle session timeout for remote VPN?"*
3. Engine performs pre-retrieval filtering on `STATUS = 'ACTIVE'`.
4. Engine retrieves chunk from **`Remote_Work_Security_Policy_v3.0`** (30 minutes).
5. Synthesizes response with explicit metadata badge (`v3.0 [Active]`), page citation (`Page 1`), and verbatim excerpt.

#### B. Compliance Auditor Journey (Historical Mode)
1. Auditor opens **AI Document Chat** or **Version History**.
2. Submits question: *"What was the password rotation cycle under Version 1.0?"*
3. Query analyzer identifies explicit historical version intent (`v1.0`).
4. Engine retrieves chunk from **`v1.0`** (90 days).
5. Synthesizes response with a yellow warning badge: `⚠️ HISTORICAL RECORD (v1.0 - SUPERSEDED)`.

---

## 3. System Architecture & Tech Stack

```
+--------------------------------------------------------------------------+
|                         RAGNext Web Application                          |
|         React 18 + Vite + Bootstrap 5 + Lucide Icons + Responsive UI     |
+------------------------------------+-------------------------------------+
                                     |  REST API / JSON
                                     v
+------------------------------------+-------------------------------------+
|                     Node.js / Express Backend Engine                     |
|                                                                          |
|  [Document Ingestion]   [Chunking & Hash]    [Temporal Filter Engine]    |
|  [Version LifeCycle]    [Conflict Detector]  [Grounded Synthesis Engine] |
+-----------+------------------------+-----------------------+-------------+
            |                        |                       |
            v                        v                       v
+-----------+-----------+  +---------+-----------+  +--------+-------------+
|    Metadata Database  |  |    Vector Database  |  |  Local AI Inference  |
|  SQLite / PostgreSQL  |  |  ChromaDB / JSON    |  |  Ollama (llama3.2)   |
|  - document_groups    |  |  - Cosine Distance  |  |  Local Embeddings    |
|  - document_versions  |  |  - 768-dim Vectors  |  |  (nomic-embed-text)  |
|  - chunks & audit     |  |  - Metadata Filter  |  |  Extractive Fallback |
+-----------------------+  +---------------------+  +----------------------+
```

### 3.1 Technology Stack Matrix

| Layer | Component | Choice | Rationale |
| :--- | :--- | :--- | :--- |
| **Frontend** | Framework | React 18 + Vite | Rapid Hot-Module Replacement, component reusability, lightweight bundle |
| **Frontend** | Styling | Bootstrap 5 + Custom CSS Tokens | Clean White + Emerald Green corporate theme, responsive layouts |
| **Frontend** | Icons | Lucide React | Modern, lightweight icon suite |
| **Backend** | Runtime & API | Node.js (v18+) + Express.js (ES Modules) | Asynchronous I/O, robust middleware ecosystem |
| **Document Parsing** | File Readers | `pdf-parse`, `mammoth` (DOCX), UTF-8 TXT | Multi-format support with page-level boundary preservation |
| **Metadata Store** | Database | SQLite (Primary/Zero-Config) / Postgres (Enterprise) | ACID compliance, relational integrity for version trees, zero setup friction |
| **Vector Store** | Embeddings DB | Embedded Persistent Vector Store (ChromaDB-compatible) | Fast in-memory cosine ranking with disk persistence in `vectors.json` |
| **Inference** | LLM Engine | Ollama (`llama3.2:latest`) | Open-weights, low resource footprint (2.0 GB), local execution |
| **Embeddings** | Vector Model | Ollama (`nomic-embed-text:latest`) | High-performing 768-dimensional local text embeddings |
| **Fallback Engine** | Synthesis Fallback | Deterministic Grounded Extractor | Guarantees 100% functionality even when Ollama is offline or unavailable |

---

## 4. Functional Requirements (FR)

Requirements are prioritized using the **MoSCoW** framework:
* **Must Have (M):** Mandatory for MVP & evaluation.
* **Should Have (S):** High priority, enhances user experience.
* **Could Have (C):** Desirable, planned for subsequent enterprise release.
* **Won't Have (W):** Explicitly out of scope for current release.

### 4.1 Document Ingestion & Version Lifecycle Management

| ID | Priority | Requirement | Acceptance Criteria |
| :--- | :---: | :--- | :--- |
| **FR-01** | **Must** | Multi-Format Document Upload | System must ingest `.pdf`, `.docx`, `.txt`, and `.md` files up to 25 MB. |
| **FR-02** | **Must** | Document Group Association | Uploading a document must allow associating it with a new or existing Document Group. |
| **FR-03** | **Must** | Semantic Version Parsing | System must extract or allow input of SemVer strings (e.g., `v1.0`, `v2.0`). |
| **FR-04** | **Must** | Automatic Supersession Workflow | When a new version is marked `ACTIVE`, previous active versions in the same group must transition to `SUPERSEDED` automatically unless a conflict is declared. |
| **FR-05** | **Must** | Cryptographic File Storage | Uploaded files must be renamed to `doc_<timestamp>_<hash>.<ext>` and stored safely. |

### 4.2 Document Chunking & Vectorization

| ID | Priority | Requirement | Acceptance Criteria |
| :--- | :---: | :--- | :--- |
| **FR-06** | **Must** | Context-Preserving Chunking | Documents must be split into 500-character chunks with 100-character overlap, respecting sentence boundaries. |
| **FR-07** | **Must** | Page-Aware Tracking | Every chunk must retain its source metadata: `document_id`, `version_id`, `page_number`, and `chunk_index`. |
| **FR-08** | **Must** | Vector Embedding Generation | Chunks must be embedded using `nomic-embed-text` (or fallback token-frequency vectors) and saved to persistent vector store. |

### 4.3 Version-Aware Retrieval & Chat Intelligence

| ID | Priority | Requirement | Acceptance Criteria |
| :--- | :---: | :--- | :--- |
| **FR-09** | **Must** | Temporal Pre-Retrieval Filtering | Default search must strictly query chunks where `document_versions.status = 'ACTIVE'`. |
| **FR-10** | **Must** | Historical Version Intent Detection | If the query mentions a specific version (e.g., *"in v1.0"*), system switches retrieval scope to that historical version. |
| **FR-11** | **Must** | Verifiable Citations | Every AI response must return the exact version number, document title, page number, and supporting excerpt. |
| **FR-12** | **Must** | Conflicting Version Flagging | If two documents in the same group have `status = 'ACTIVE'`, system returns a prominent Conflict Alert. |
| **FR-13** | **Must** | Missing Evidence Rejection | If the similarity score is below threshold (0.45) or the question is out of scope, the system must report insufficient evidence rather than hallucinating. |
| **FR-14** | **Should** | Seed Dataset One-Click Loader | Provide a one-click demo dataset seeding button loading `Leave Policy` and `Remote Work Security Policy` revision lineages. |
| **FR-15** | **Could** | Side-by-Side Version Diff View | Visual clause-level diff comparison between two selected document versions. |

---

## 5. Non-Functional Requirements (NFR)

### 5.1 Performance & Latency
* **NFR-01 (Inference Latency):** AI responses using local Ollama (`llama3.2`) must stream or complete within **< 3.5 seconds** on standard developer hardware (CPU/GPU).
* **NFR-02 (Retrieval Latency):** Vector search across 10,000 document chunks must execute in **< 150 milliseconds**.
* **NFR-03 (Ingestion Throughput):** A 30-page PDF document must parse, chunk, embed, and index in **< 8 seconds**.

### 5.2 Security & Data Sovereignty
* **NFR-04 (Air-Gapped Operation):** Zero external HTTP calls to cloud AI endpoints (OpenAI, Anthropic, Google). All data remains strictly within the local host network.
* **NFR-05 (Path Traversal Protection):** Upload filenames and storage paths must be strictly sanitized against directory traversal attacks (`../`).
* **NFR-06 (MIME Type Validation):** File payloads must be validated by content sniffing, not just file extension.

### 5.3 Reliability & Availability
* **NFR-07 (Graceful Degradation):** If Ollama is stopped or unavailable, the backend must automatically fall back to deterministic grounded extractive synthesis without crashing.
* **NFR-08 (Persistent State):** All document metadata, version states, and vector indices must survive application restarts.

---

## 6. Data Model & Database Schema

### 6.1 Entity Relationship Overview
* **`document_groups` (1 : N) ➔ `document_versions` (1 : N) ➔ `chunks`**
* **`conversations` (1 : N) ➔ `messages`**
* **`audit_logs`**

### 6.2 Relational Schema Specifications

```sql
-- 1. Logical Document Groups
CREATE TABLE document_groups (
    id TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    category TEXT DEFAULT 'general',
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Document Version Records
CREATE TABLE document_versions (
    id TEXT PRIMARY KEY,
    group_id TEXT NOT NULL REFERENCES document_groups(id) ON DELETE CASCADE,
    version_string TEXT NOT NULL,          -- e.g. '1.0', '2.0', '3.0'
    status TEXT NOT NULL,                  -- 'ACTIVE', 'SUPERSEDED', 'DRAFT', 'ARCHIVED'
    effective_date DATE,
    expiration_date DATE,
    file_path TEXT NOT NULL,
    file_name TEXT NOT NULL,
    file_type TEXT NOT NULL,
    file_size INTEGER NOT NULL,
    page_count INTEGER DEFAULT 1,
    checksum TEXT NOT NULL,
    is_conflict BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Document Chunks & Embeddings Index
CREATE TABLE chunks (
    id TEXT PRIMARY KEY,
    version_id TEXT NOT NULL REFERENCES document_versions(id) ON DELETE CASCADE,
    chunk_index INTEGER NOT NULL,
    page_number INTEGER NOT NULL,
    content TEXT NOT NULL,
    token_count INTEGER,
    vector_id TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 4. Audit Trail & Queries
CREATE TABLE audit_logs (
    id TEXT PRIMARY KEY,
    query_text TEXT NOT NULL,
    version_intent TEXT,
    retrieved_chunk_ids TEXT,              -- JSON array
    cited_version_ids TEXT,                -- JSON array
    latency_ms INTEGER,
    has_conflict BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 7. REST API Endpoints Specification

### 7.1 Health & Diagnostics
* `GET /api/health` — Checks status of backend, database adapter, and vector store.
* `GET /api/settings` — Checks Ollama connectivity, model availability, and storage directory.

### 7.2 Document Management
* `GET /api/documents` — Lists all document groups and their active version summaries.
* `POST /api/documents/upload` — Multipart file upload (`file`, `groupId`, `groupName`, `version`, `effectiveDate`, `status`).
* `GET /api/documents/:id` — Retrieves detailed metadata for a single document.
* `DELETE /api/documents/:id` — Deletes document version and cascades deletion across chunks and vectors.

### 7.3 Version Lineage
* `GET /api/versions/:groupId` — Returns complete version lineage tree for a document group with status badges.
* `PATCH /api/versions/:id/status` — Promotes or supersedes a version (`status`: `'ACTIVE' | 'SUPERSEDED'`).

### 7.4 Version-Aware Chat & Synthesis
* `POST /api/chat`
  * **Request Body:**
    ```json
    {
      "query": "What is the idle timeout for VPN?",
      "groupId": "doc_group_remote_security",
      "versionFilter": null
    }
    ```
  * **Response Body:**
    ```json
    {
      "answer": "Under the active Remote Work Security Policy v3.0, the maximum idle session timeout is 30 minutes with required re-authentication.",
      "versionCited": "v3.0",
      "status": "ACTIVE",
      "isSuperseded": false,
      "conflictDetected": false,
      "citations": [
        {
          "documentName": "Remote_Work_Security_Policy_v3.0.txt",
          "version": "v3.0",
          "page": 1,
          "excerpt": "1.2 Maximum idle session timeout is 30 minutes. Re-authentication is enforced at every connection resumption."
        }
      ],
      "latencyMs": 842
    }
    ```

---

## 8. User Interface & Screen Specifications

1. **Dashboard (`/`)**:
   * Metrics bar: Total Documents, Active Versions, Superseded Versions, System Status.
   * "Seed Demo Dataset" button for instant hackathon demonstrations.
   * Recent document lineage table with status badges.

2. **Document Library (`/documents`)**:
   * Grouped view of enterprise policies.
   * Version badges: Green (`ACTIVE`), Yellow (`SUPERSEDED`), Blue (`DRAFT`).
   * One-click action to inspect lineage history or download source file.

3. **Document Ingestion Portal (`/upload`)**:
   * Drag-and-drop zone supporting PDF, DOCX, TXT.
   * Form inputs for Group Name, Version Tag (`v1.0`), Effective Date, and Initial Status.
   * Real-time upload, parsing, chunking, and indexing progress indicators.

4. **AI Document Chat (`/chat`)**:
   * Conversational query interface with auto-scrolling message history.
   * Visual citation cards showing Document Title, Version Badge, Page Number, and Exact Supporting Quote.
   * Conflict banner when query touches ambiguous active documents.
   * Quick demo query chips for instant testing.

5. **Version History & Lineage (`/versions/:groupId`)**:
   * Visual timeline depicting document evolution (`v1.0 ➔ v2.0 ➔ v3.0`).
   * Modification timestamps, author notes, and status transition controls.

6. **System Settings (`/settings`)**:
   * Local Ollama engine status (`llama3.2` and `nomic-embed-text` detection).
   * SQLite / Postgres adapter status and vector index chunk counts.

---

## 9. Success Metrics & Key Performance Indicators (KPIs)

| Metric | Target | Measurement Method |
| :--- | :---: | :--- |
| **Superseded Clause Citation Rate** | **0.0%** | Automated test suite verifying current-version queries never cite older clauses |
| **Grounding Citation Accuracy** | **100%** | Every synthesized claim has a corresponding page number and excerpt |
| **Hallucination Rate on Missing Data**| **0.0%** | System returns insufficient evidence when information is not in indexed chunks |
| **Audit Turnaround Reduction** | **> 60%** | Time taken by auditors to locate historical clauses compared to manual PDF reading |
| **Local Inference Reliability** | **100%** | Extractive fallback triggers seamlessly if Ollama service is stopped |

---

## 10. Release Milestones & Roadmap

* **Stage 1 (Completed):** Problem framing, root-cause analysis, and market validation presentation.
* **Stage 2 / Current MVP (Operational):**
  * Fully functioning React 18 UI + Express backend.
  * Local SQLite persistent storage + embedded vector store.
  * Ollama `llama3.2` and `nomic-embed-text` integration.
  * Complete Leave Policy and Remote Work Security Policy multi-version test suite.
* **Phase 3 (Enterprise Scale):**
  * Automated OCR for scanned historical documents (Tesseract / EasyOCR).
  * Direct connectors for Microsoft SharePoint, Google Drive, and Confluence.
  * Role-Based Access Control (RBAC) with Active Directory / LDAP integration.

---

*Authored by Team Cyber Knights for Hackathon Problem Statement SH-SVA-04.*
