# 🛡️ MARKET REQUIREMENTS DOCUMENT (MRD)
## RAGNext — Autonomous Version-Aware Document Intelligence Engine with Verifiable Grounding

* **Document Version:** `v2.0` (Stage 2 Hackathon Release)
* **Problem Statement ID:** `SH-SVA-04`
* **Team Name:** `Cyber Knights`
* **Authors:** Sainath Loganathan, Tahir Azeem
* **Target Audience:** Regulated Enterprises, Legal/Compliance Auditors, Enterprise HR/IT
* **Classification:** Market Requirements, Business Strategy & Product Definition

---

## 📌 Executive Summary & Problem Framing

### 1.1 The Core Problem (In Simple English)
In every company, documents never stay the same. Policies, security guidelines, and contracts constantly evolve:
* **2021 (Version 1.0):** Employee leave allowance is set to **15 days**.
* **2022 (Version 2.0):** Leave allowance increases to **18 days**.
* **2024 (Version 3.0 - Active):** Leave allowance increases to **20 days**.

When employees search using conventional AI tools (like standard RAG or ChatGPT), the AI performs a blind semantic search across all files. Because the old 2021 document has an exact keyword match, **the AI answers with outdated information: "15 days"**. 

This phenomenon is called **Superseded Document Hallucination**. In regulated sectors like banking, healthcare, and defense, relying on outdated policy documents causes severe regulatory fines, failed audits, and operational disputes.

### 1.2 The RAGNext Solution
**RAGNext** is an autonomous, **Version-Aware Document Intelligence Engine**. Instead of treating documents as a flat pile of text chunks:
1. It maps documents into **Revision Lineage Graphs** (`v1.0` ➔ `v2.0` ➔ `v3.0`).
2. It applies **Pre-Retrieval Policy State Filtering** (`ACTIVE`, `SUPERSEDED`, `DRAFT`, `ARCHIVED`).
3. It detects **Conflicting Active Policies** before answering.
4. It operates **100% Offline and Air-Gapped** using local AI models (Ollama / Llama 3.2), keeping proprietary company data secure.
5. It grounds every answer with **Verifiable Page Numbers and Verbatim Quotes**.

---

## 🎯 Target Market & User Segments

| User Segment | Role in Enterprise | Pain Point with Existing Search Tools | How RAGNext Solves It |
| :--- | :--- | :--- | :--- |
| **Regulated Enterprises** *(BFSI, Healthcare, Defense)* | Organizations bound by ISO 27001, HIPAA, and NIST 800-53 standards | High compliance risk if employees follow superseded policies or leak data to cloud APIs | Enforces strict active-version retrieval and 100% offline air-gapped data privacy |
| **Enterprise HR, IT & Operations** | Manages constantly evolving internal guidelines and employee benefits | Outdated internal wikis lead to employee confusion and policy disputes | Automatic supersession workflow ensures everyone receives the legally binding active rule |
| **Internal & External Auditors** | Evaluates historical compliance during incidents or regulatory reviews | Finding what rule was valid 2 years ago requires hours of manual PDF reading | Bi-directional querying allows instant historical audit queries (e.g. *"What was the rule in v1.0?"*) |
| **Knowledge Workers & Employees** | Needs quick, reliable answers for everyday operations | Cites deprecated guidelines without realizing newer versions exist | Conversational AI delivers instant answers with clickable page citations and version badges |

---

## 👥 User Personas

### 👨‍💼 Persona A: Compliance & Risk Auditor (Rajesh)
* **Role:** Head of Compliance & Enterprise Risk
* **Everyday Need:** Needs to verify whether an operational action taken in 2022 complied with the policy active *at that exact time*.
* **Current Pain:** Search tools return a mix of old and new clauses. Comparing revisions takes hours of manual PDF cross-referencing.
* **Expectation from RAGNext:** Verifiable audit logs, clear revision lineage trees, and zero superseded clause leakage.

### 👩‍💻 Persona B: Knowledge Worker / Policy Consumer (Priya)
* **Role:** Operations Lead / Employee
* **Everyday Need:** Needs quick answers to day-to-day policy questions (e.g., VPN timeouts, annual leave days, procurement thresholds).
* **Current Pain:** Searching the intranet surfaces obsolete drafts from 2021 without warning, putting her at risk of policy violations.
* **Expectation from RAGNext:** Fast conversational answers clearly tagged as `[Active v3.0]` with page citations and zero prompt complexity.

### 🛡️ Persona C: IT & Security Administrator (Dev)
* **Role:** Enterprise Infrastructure & Information Security Lead
* **Everyday Need:** Provide low-latency AI search for internal documentation without recurring cloud API fees or data leakage.
* **Current Pain:** Cloud AI tools (OpenAI, Microsoft Copilot) send private corporate files to third-party data centers, violating corporate governance.
* **Expectation from RAGNext:** 100% local execution on on-premise hardware with zero external network dependencies.

---

## 🗺️ User Journey: Conventional RAG vs. RAGNext

```
CONVENTIONAL RAG (Broken Journey)
User asks question ➔ Blind Vector Search over all PDFs ➔ Outdated v1.0 scores high match ➔ AI answers with expired 2021 rule ➔ Employee makes wrong decision ➔ Compliance Violation!

RAGNEXT (Version-Aware Journey)
User asks question ➔ Intent Classifier checks temporal context ➔ Hard Filter blocks 'SUPERSEDED' versions ➔ Vector Search queries ONLY 'ACTIVE v3.0' ➔ AI answers with current rule + Page Citation ➔ 100% Verified!
```

| Step | What Happens in Conventional RAG | What Happens in RAGNext |
| :--- | :--- | :--- |
| **1. Ingestion** | Uploads PDFs without capturing revision linkages or lifecycles. | Parses version numbers, effective dates, and builds a **Directed Lineage Graph**. |
| **2. Chunking** | Dumps text as a continuous blob without exact page coordinates. | **Page-Aware Chunker** stores exact page numbers and chunk offsets for verifiable proof. |
| **3. Search Execution** | Computes cosine similarity across *every* document chunk in the database. | **Pre-Retrieval Filter** isolates the search space *strictly* to `status = 'ACTIVE'`. |
| **4. Historical Inquiries** | Cannot filter by historical date or specific version number. | Recognizes queries like *"What was the rule in v1.0?"* and pulls historical records with a warning badge. |
| **5. Policy Conflicts** | Silently blends contradictory policies together into a confused answer. | **Conflict Sentinel** flags when two conflicting policies are active in the same group. |
| **6. Output Synthesis** | Synthesizes answers without source page proofs or version labels. | Delivers clean, structured answers with verbatim quotes, page numbers, and version tags. |

---

## 🏗️ System Architecture & Version Policy Matrix

### 5.1 Architectural Flow
```
┌────────────────────────────────────────────────────────────────────────┐
│                        RAGNext Web Application                         │
│           React 18 • Vite • Bootstrap 5 • Lucide Icons (SPA)           │
└───────────────────────────────────┬────────────────────────────────────┘
                                    │ REST API (JSON)
                                    ▼
┌────────────────────────────────────────────────────────────────────────┐
│                    Node.js & Express.js API Server                     │
│  ┌───────────────────────┐ ┌──────────────────────┐ ┌───────────────┐  │
│  │ Document Ingestion &  │ │ Version Lifecycle &  │ │ Query Intent  │  │
│  │ Multi-Format Parser   │ │ Conflict Sentinel    │ │ Classifier    │  │
│  └───────────────────────┘ └──────────────────────┘ └───────────────┘  │
└───────────────┬───────────────────┬───────────────────┬────────────────┘
                │                   │                   │
                ▼                   ▼                   ▼
     ┌────────────────────┐ ┌───────────────┐ ┌───────────────────┐
     │  Metadata Storage  │ │ Vector Store  │ │ AI Inference &    │
     │ PostgreSQL Adapter │ │ Embedded Disk │ │ Embeddings        │
     │ + Local JSON Store │ │ Cosine Engine │ │ Ollama (llama3.2) │
     │ (Zero-Config Dual) │ │ (Chroma-spec) │ │ + Grounded Fallback│
     └────────────────────┘ └───────────────┘ └───────────────────┘
```

### 5.2 Retrieval Enforcement Policy Matrix
| Trigger / Query Intent | Target Version Scope | System Action & Output Behavior |
| :--- | :--- | :--- |
| **Current Policy Query** *(Default)* | Latest Active Version (`v3.0`) | Applies hard pre-filter `status = 'ACTIVE'`. Outdated chunks are mathematically ignored. |
| **Historical Query** *(e.g. "in v1.0")* | Specific Requested Version | Routes retrieval to requested historical version. Attaches prominent `⚠️ [Historical Record — Superseded]` badge. |
| **Conflicting Active Policies** | Multiple Active Revisions | Suspends automated generation. Issues administrative `Conflict Warning` and displays side-by-side differences. |
| **Out-of-Scope / Missing Info** | Zero Relevant Chunks | Responds honestly: *"Insufficient Evidence in Active Documents"*, refusing to speculate or hallucinate. |

---

## 📋 Functional Requirements (MoSCoW Prioritization)

* **Must Have (M):** Critical for MVP and live hackathon demonstration.
* **Should Have (S):** High priority enterprise enhancements.
* **Could Have (C):** Future roadmap integrations.

| ID | Priority | Requirement Description |
| :---: | :---: | :--- |
| **FR01** | **Must Have** | Ingestion of multi-format documents (PDF, DOCX, TXT) with SHA-256 deduplication and cryptographic file sanitization. |
| **FR02** | **Must Have** | Structured metadata extraction: version string, effective date, status, category, and document group ID. |
| **FR03** | **Must Have** | Page-aware semantic chunking preserving exact document page numbers and chunk character offsets. |
| **FR04** | **Must Have** | Persistent vector store indexing supporting rich metadata pre-filtering (status and version constraints). |
| **FR05** | **Must Have** | Document revision lineage graph linking versions (`v1.0` ➔ `v2.0` ➔ `v3.0`) in a parent-child hierarchy. |
| **FR06** | **Must Have** | Strict active-version enforcement for general policy inquiries, blocking superseded chunks prior to similarity ranking. |
| **FR07** | **Must Have** | Explicit historical version query routing with temporal provenance labeling and warning banners. |
| **FR08** | **Must Have** | Conflict detection engine alerting administrators when multiple contradictory documents are marked active simultaneously. |
| **FR09** | **Must Have** | Grounded answer generation producing verifiable responses with verbatim quotes and page-level citations. |
| **FR10** | **Must Have** | Honest missing-evidence reporting (zero-hallucination guardrail) when query facts are not present in active documents. |
| **FR11** | **Must Have** | Interactive web dashboard featuring Document Library, Version Lineage View, and AI Chat Drawer. |
| **FR12** | **Should Have**| Side-by-side visual document diffing showing clause modifications between consecutive revisions. |
| **FR13** | **Should Have**| Tamper-evident audit logging recording query telemetry, matched chunks, version IDs, and response timestamps. |
| **FR14** | **Could Have**  | Automated enterprise sync connectors for Microsoft SharePoint, Google Drive, and Confluence. |

---

## ⚡ Non-Functional Requirements (NFR)

* **NFR-01 (Inference Latency):** Query-to-answer turnaround within `< 2.5s` for extractive synthesis and `< 5.0s` for local LLM inference.
* **NFR-02 (UI Responsiveness):** Dashboard search, library filtering, and version tree loading completed in `< 300ms`.
* **NFR-03 (Data Sovereignty & Air-Gapped Security):** 100% offline execution. Zero external HTTP requests to cloud AI services.
* **NFR-04 (Zero-Friction Reliability):** Automatic dual-mode database fallback (PostgreSQL ➔ Local persistent JSON store) and dual-mode AI fallback (Ollama LLM ➔ Deterministic Grounded Synthesizer).
* **NFR-05 (Path Traversal & Injection Defense):** File storage sanitized against directory traversal attacks (`../`) and MIME-sniffed before ingestion.
* **NFR-06 (Verifiable Grounding):** 100% of generated facts must map to exact document excerpts and page citations.

---

## ⚔️ Competitor & Existing Solution Analysis

| Dimension | Standard Vector RAG *(LangChain / Pinecone)* | Enterprise Search *(Elasticsearch)* | Cloud AI Copilots *(M365 Copilot)* | **RAGNext** |
| :--- | :--- | :--- | :--- | :--- |
| **Version Lineage** | ❌ None (Flat chunks) | ❌ None (Raw text) | ⚠️ Basic file dates | ✅ **Hierarchical Lineage Graph** |
| **Superseded Filtering**| ❌ Blind vector retrieval | ❌ Blind keyword matches | ⚠️ Prone to stale citations | ✅ **Pre-Retrieval State Filtering** |
| **Conflict Alerts** | ❌ None (Silent blends) | ❌ None | ❌ None | ✅ **Autonomous Conflict Sentinel** |
| **Data Privacy** | ⚠️ Depends on cloud DB | ✅ On-premise possible | ❌ Public cloud API | ✅ **100% Air-Gapped & Offline** |
| **Page Citation Proof** | ⚠️ Vague document hints | ❌ Text snippets only | ⚠️ General references | ✅ **Verifiable Page + Quote Grounding** |
| **Zero-Failure Fallback**| ❌ Server crash if LLM down | N/A | ❌ Cloud outage failure | ✅ **Deterministic Extractive Fallback** |

---

## 💡 Core Innovations

1. **Temporal Lineage Graph:** Converts unstructured document updates into an explicit version tree (`v1.0` ➔ `v2.0` ➔ `v3.0`), preserving the full revision lifecycle.
2. **Pre-Retrieval State Filtering:** Eliminates superseded clauses at the *mathematical retrieval root* rather than relying on LLM prompt instructions to ignore them.
3. **Autonomous Conflict Sentinel:** Flags overlapping active documents within the same policy domain before contradictory advice reaches employees.
4. **Verifiable Grounded Attribution:** Enforces that every claim is accompanied by a verbatim quote, version tag, and exact page number.
5. **Air-Gapped Privacy Autonomy:** Runs entirely on local consumer hardware via Ollama (`llama3.2`) and embedded vector storage with zero external data telemetry.
6. **Zero-Failure Dual Architecture:** Gracefully degrades from PostgreSQL to local storage and from local LLM to deterministic extractive synthesis, ensuring 100% uptime during live evaluations.

---

## 🚀 Minimum Viable Product (MVP) & Hackathon Demo Workflow

### 7.1 Live Hackathon Demonstration Flow
1. **Dashboard Overview:** Displays repository statistics (total documents, active versions, superseded versions, conflict alerts).
2. **One-Click Seeding:** Clicking *"Seed Demo Dataset"* populates the repository with the 3-version Leave Policy (`v1.0`=15 days, `v2.0`=18 days, `v3.0`=20 days) and Remote Work Security Policy.
3. **Document Library & Lineage Inspection:** Inspecting the *Annual Leave Policy* shows the active `v3.0` record and historical `v1.0` / `v2.0` revisions.
4. **Current Policy Query:** Asking *"What is the current annual leave allowance?"* returns **20 days** citing **v3.0, Page 1**.
5. **Historical Query:** Asking *"What was the allowance in version 2?"* retrieves **18 days** citing **v2.0 (Historical)** with a warning banner.
6. **Missing Evidence Query:** Asking *"Where is maternity leave explained?"* returns an honest *"Insufficient evidence"* report.
7. **Conflict Alert Simulation:** Adding two conflicting active policies triggers a live conflict banner warning the user of divergent guidelines.

---

## 📊 Success Metrics & Key Performance Indicators (KPIs)

* **Version Retrieval Accuracy:** 100% precision on distinguishing active vs historical policy queries.
* **Superseded Clause Contamination:** 0% leakage of superseded clauses into general policy query contexts.
* **Answer Groundedness:** > 95% citation accuracy backed by verbatim document text.
* **Conflict Trigger Rate:** 100% automated alert generation upon detection of multiple active documents in the same group.
* **Audit Turnaround Reduction:** > 60% faster policy reconciliation during compliance investigations.
* **Zero Cloud Exposure:** 100% of document processing, vector search, and model inference executed locally.

---

## 💼 Business & Sustainability Model

1. **Tier 1: Enterprise On-Premises License:** Annual per-node subscription for air-gapped, high-security enterprise deployments (Defense, Banking, Healthcare).
2. **Tier 2: Managed Private Cloud SaaS:** Single-tenant hosted private cloud instances with automated backups and maintenance for mid-market firms.
3. **Tier 3: Compliance & Audit Add-on:** Turnkey document version auditing, policy reconciliation reports, and regulatory compliance exports.
4. **Tier 4: Open-Core Ecosystem:** Free open-source local core for developers; paid commercial connectors for enterprise repositories (SharePoint, Google Drive).

### Four-Phase Growth Plan:
* **Phase 1 (Hackathon MVP):** Working version-aware engine with automated test suite and seed dataset.
* **Phase 2 (Pilot Deployment):** University and SMB pilot testing for employee handbooks and academic regulations.
* **Phase 3 (Enterprise Connectors):** Automated synchronization connectors for SharePoint, Confluence, and Google Workspace.
* **Phase 4 (Industry Compliance Packs):** Pre-built compliance packs for HIPAA, GDPR, ISO 27001, and SOC 2 audits.

---

## ⚠️ Risk Analysis & Mitigation Matrix

| Identified Risk | Business Impact | RAGNext Mitigation Strategy |
| :--- | :--- | :--- |
| **Ambiguous user query without version context** | User receives unexpected version | Defaults strictly to Active version, displays explicit `[Active vX.Y]` badge, and provides a one-click switch to historical versions. |
| **Malformed or unversioned document uploads** | Metadata extraction failure | Heuristic regex parser extracts version hints from document title/content; UI prompts user for manual confirmation. |
| **Multiple contradictory active versions** | Contradictory policy advice | Conflict Sentinel halts single-answer synthesis, displays a prominent conflict alert, and provides a side-by-side comparison. |
| **Hardware throttling on low-spec PCs** | AI model timeout | Automatic fallback to Deterministic Grounded Extractive Synthesizer running on CPU with zero GPU requirements. |
| **Proprietary data leakage** | Breach of compliance | 100% offline air-gapped architecture; zero cloud telemetry; cryptographic storage hashes. |
| **AI Hallucination** | Inaccurate policy advice | Strict prompt evidence bounding, mandatory page citations, and honest missing-evidence reports when data is absent. |

---

## 📜 Regulatory Standards & Industry Alignment

* **NIST SP 800-53 Rev. 5:** Controls **SI-12** (Information Handling and Retention) and **AU-10** (Non-repudiation and Provenance).
* **ISO/IEC 27001:2022:** Control **A.5.37** (Documented Information Governance and Version Validity).
* **CISA Zero Trust Maturity Model v2.0:** Data Pillar requirements for continuous data lineage, policy integrity, and air-gapped protection.
