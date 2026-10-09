# RAGNext — Version-Aware Document Intelligence Engine

> An **Edutorial Design** interactive web application built with a high-prestige White & Royal Blue aesthetic, showcasing the next-generation Version-Aware Retrieval-Augmented Generation (RAG) system.

---

## 📖 System Architecture & Overview

Standard retrieval engines fail when documents evolve over time, retrieving outdated information based solely on semantic similarity. **RAGNext** solves this by maintaining a temporal version lineage graph, guaranteeing that queries retrieve only valid active versions with page-level citations and verifiable source evidence.

### Core Sections & Features:
1. **Chapter 01: Existing Problem vs Proposed Solution** (Slide 1)
   - Dual-ledger comparative analysis of document sprawl, revision drift, hallucination risk vs. temporal validity and grounded answers.
2. **Chapter 02: Idea Overview & Capabilities** (Slide 2)
   - 8-pillar architectural card grid covering multi-format ingestion (PDF, DOCX, PPT, TXT), deep semantic extraction, and sub-second retrieval.
3. **Chapter 03: 6-Stage System Pipeline Workflow** (Slide 3)
   - Step-by-step interactive stepper:
     1. Ingest Documents
     2. Read & Understand
     3. Store with Version Lineage (`v1.0` ➔ `v2.0` ➔ `v3.0 ✔`)
     4. User Question
     5. Find Latest Version & Retrieve
     6. Structured Output (Source, Version, Page, Evidence)
4. **Chapter 04: Live Interactive RAG Sandbox**
   - Testbench across 4 enterprise domains (*HR Policies*, *Engineering SOPs*, *Clinical Guidelines*, *Finance Directives*) with active version status badges, highlighted evidence inspection, and latency metrics.
5. **Chapter 05: Target Users & Industry Use-Cases** (Slide 4)
   - Detailed dossier cards for *Company Employees*, *Engineers*, *Government Officers*, *Finance & Compliance Teams*, and *Healthcare Staff*.
6. **Chapter 06: Impact & ROI Calculator**
   - Real-time productivity and risk reduction calculator.
7. **Pitch Deck / Presentation Mode**
   - Full-screen slide deck view designed for pitch presentations directly reflecting Slides 1 through 4.

---

## 🚀 How to Run Locally

Open `index.html` directly in any modern browser, or serve it via Python:

```bash
# Start a lightweight local server
python -m http.server 8085

# Open in browser:
http://localhost:8085
```

---

## 🎨 Design System
- **Theme**: "Edutorial Design" (Editorial + Educational)
- **Palette**: Pure White (`#FFFFFF`, `#F8FAFC`), Ice Blue (`#EFF6FF`), Royal/Sapphire Blue (`#1E40AF`, `#2563EB`, `#0EA5E9`), Deep Navy Ink (`#0F172A`).
- **Typography**: Newsreader (Editorial Serif), Plus Jakarta Sans (Clean Modern Sans), JetBrains Mono (Code/Metadata).