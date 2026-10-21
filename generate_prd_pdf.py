import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

# Corporate Palette Constants
NAVY_HEADER = colors.HexColor("#1A365D")
GREEN_ACCENT = colors.HexColor("#15803D")
GREEN_DARK = colors.HexColor("#065F46")
TEXT_DARK = colors.HexColor("#1E293B")
TEXT_MUTED = colors.HexColor("#64748B")
BORDER_COLOR = colors.HexColor("#CBD5E1")
BG_LIGHT = colors.HexColor("#F8FAFC")
BG_ACCENT = colors.HexColor("#F0FDF4")
WHITE = colors.HexColor("#FFFFFF")
HEADER_BLUE = colors.HexColor("#1E40AF")
PRIORITY_MUST = colors.HexColor("#FEE2E2")
PRIORITY_SHOULD = colors.HexColor("#FEF3C7")
PRIORITY_COULD = colors.HexColor("#E0E7FF")

class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, total_pages):
        # Page 1: Emerald Top Accent
        if self._pageNumber == 1:
            self.saveState()
            self.setFillColor(GREEN_DARK)
            self.rect(0, 818, 595.27, 24, fill=1, stroke=0)
            self.setFillColor(GREEN_ACCENT)
            self.rect(0, 814, 595.27, 4, fill=1, stroke=0)
            self.restoreState()
        else:
            # Pages 2 and 3: Running Header
            self.saveState()
            self.setFillColor(NAVY_HEADER)
            self.rect(0, 818, 595.27, 24, fill=1, stroke=0)
            self.setFillColor(WHITE)
            self.setFont("Helvetica-Bold", 8)
            self.drawString(32, 826, "PRD | RAGNext — Autonomous Version-Aware Document Intelligence Engine")
            self.drawRightString(595.27 - 32, 826, "Team Cyber Knights (SH-SVA-04)")

            # Running Footer
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(32, 28, 595.27 - 32, 28)
            self.setFillColor(TEXT_MUTED)
            self.setFont("Helvetica", 7.5)
            self.drawString(32, 18, "Product Requirements Document (PRD) — Engineering Specification")
            self.drawRightString(595.27 - 32, 18, f"Page {self._pageNumber} of {total_pages}")
            self.restoreState()

def create_prd_pdf(output_path="RAGNext_Stage2_PRD_Cyber_Knights.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=32,
        rightMargin=32,
        topMargin=28,
        bottomMargin=28
    )

    styles = getSampleStyleSheet()

    style_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=18,
        textColor=GREEN_DARK,
        alignment=1,
        spaceAfter=2
    )

    style_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=NAVY_HEADER,
        alignment=1,
        spaceAfter=7
    )

    style_h1 = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=GREEN_DARK,
        spaceBefore=4,
        spaceAfter=2,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.0,
        leading=8.8,
        textColor=TEXT_DARK,
        spaceAfter=2
    )

    style_th = ParagraphStyle(
        'TH',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.8,
        leading=8.2,
        textColor=WHITE
    )

    style_td = ParagraphStyle(
        'TD',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.0,
        textColor=TEXT_DARK
    )

    style_td_bold = ParagraphStyle(
        'TDBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=6.5,
        leading=8.0,
        textColor=TEXT_DARK
    )

    style_td_center = ParagraphStyle(
        'TDCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=6.5,
        leading=8.0,
        textColor=TEXT_DARK,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: VISION, SCOPE & SYSTEM ARCHITECTURE
    # =========================================================================
    story.append(Spacer(1, 14))
    story.append(Paragraph("PRODUCT REQUIREMENTS DOCUMENT (PRD)", style_title))
    story.append(Paragraph("RAGNext: Autonomous Version-Aware Document Intelligence Engine with Verifiable Grounding", style_sub))

    meta_data = [
        [Paragraph("Product Name", style_td_bold), Paragraph("RAGNext (Cyber Knights Document Intelligence)", style_td),
         Paragraph("Problem Statement ID", style_td_bold), Paragraph("SH-SVA-04 (Version-Aware Smart Virtual Assistant)", style_td)],
        [Paragraph("Authors / Team", style_td_bold), Paragraph("Sainath Loganathan, Tahir Azeem (Cyber Knights)", style_td),
         Paragraph("Target Release", style_td_bold), Paragraph("Stage 2 Evaluation & Enterprise Air-Gapped MVP", style_td)]
    ]
    t_meta = Table(meta_data, colWidths=[85, 180, 95, 171])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_ACCENT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 3))

    story.append(Paragraph("1. Executive Summary & Problem Scope Boundaries", style_h1))
    story.append(Paragraph(
        "<b>Core Principle:</b> <i>'Find the right information, from the right document version, with verifiable evidence.'</i><br/>"
        "Conventional vector RAG systems treat all document chunks equally and retrieve answers based strictly on semantic cosine distance. When policies undergo revisions (e.g. Leave Policy v1.0 ➔ v2.0 ➔ v3.0), older superseded clauses frequently score higher similarity than active ones due to exact keyword density. RAGNext eliminates this vulnerability by binding temporal lifecycle states to document embeddings and enforcing pre-retrieval policy filters.",
        style_body
    ))

    scope_data = [
        [Paragraph("Scope Dimension", style_th), Paragraph("In-Scope for Release v1.0 (Hackathon MVP)", style_th), Paragraph("Out-of-Scope (Future Enterprise Roadmap)", style_th)],
        [Paragraph("Document Formats", style_td_bold), Paragraph("PDF (page-aware text extraction), DOCX (mammoth), TXT, and Markdown up to 25 MB.", style_td), Paragraph("Scanned raster images requiring heavy OCR pipelines; audio/video transcripts.", style_td)],
        [Paragraph("Lifecycle States", style_td_bold), Paragraph("ACTIVE, SUPERSEDED, DRAFT, ARCHIVED with automatic lineage state transitions.", style_td), Paragraph("Git-style three-way branch merging of conflicting document text.", style_td)],
        [Paragraph("Retrieval Logic", style_td_bold), Paragraph("Pre-retrieval temporal filtering, historical version routing, and conflict sentinel detection.", style_td), Paragraph("Cross-lingual translation of foreign language legal policies.", style_td)],
        [Paragraph("Inference & Storage", style_td_bold), Paragraph("100% offline local inference via Ollama (llama3.2 + nomic-embed-text), SQLite/Postgres.", style_td), Paragraph("Cloud-hosted commercial AI APIs (OpenAI/Anthropic) to ensure air-gapped sovereignty.", style_td)]
    ]
    t_scope = Table(scope_data, colWidths=[90, 220, 221])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_scope)
    story.append(Spacer(1, 3))

    story.append(Paragraph("2. Decoupled 3-Tier System Architecture & Technology Stack", style_h1))
    arch_data = [
        [Paragraph("Architecture Layer", style_th), Paragraph("Technology Choice", style_th), Paragraph("Technical Role & Rationale", style_th)],
        [Paragraph("Presentation Tier", style_td_bold), Paragraph("React 18 + Vite + Bootstrap 5 + Lucide Icons", style_td), Paragraph("Snappy Virtual DOM updates, responsive grid, real-time citation cards, and visual revision trees.", style_td)],
        [Paragraph("API Gateway & Logic", style_td_bold), Paragraph("Node.js 18+ / Express.js (ES Modules)", style_td), Paragraph("Asynchronous non-blocking I/O for concurrent document uploads, chunking, and REST query routing.", style_td)],
        [Paragraph("Document Ingestion", style_td_bold), Paragraph("pdf-parse (page hook) + mammoth (DOCX) + Multer", style_td), Paragraph("Page-coordinate extraction, cryptographic upload hashing (`doc_<timestamp>_<hash>`), and traversal defense.", style_td)],
        [Paragraph("Chunking Engine", style_td_bold), Paragraph("Context-Preserving Semantic Chunker", style_td), Paragraph("Splits text into 500-char segments with 100-char overlap, attaching source page number and version ID.", style_td)],
        [Paragraph("Metadata Database", style_td_bold), Paragraph("PostgreSQL Adapter + Local Persistent Store Fallback", style_td), Paragraph("Relational integrity for revision trees; automatic zero-friction fallback to disk JSON/SQLite for hackathons.", style_td)],
        [Paragraph("Vector Store", style_td_bold), Paragraph("Embedded Persistent Vector DB (Chroma-spec)", style_td), Paragraph("In-memory cosine ranking with disk persistence; supports hard metadata filtering on version lifecycle.", style_td)],
        [Paragraph("AI Inference Engine", style_td_bold), Paragraph("Ollama (llama3.2) + nomic-embed-text", style_td), Paragraph("100% offline air-gapped dense embeddings and chat synthesis with zero cloud telemetry or SaaS fees.", style_td)],
        [Paragraph("Fail-Safe Fallback", style_td_bold), Paragraph("Deterministic Grounded Extractive Synthesizer", style_td), Paragraph("Guarantees 100% service uptime: deterministically extracts verified excerpts if LLM is offline.", style_td)]
    ]
    t_arch = Table(arch_data, colWidths=[90, 165, 276])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_arch)

    # END OF PAGE 1
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: FUNCTIONAL (MoSCoW) & NON-FUNCTIONAL REQUIREMENTS
    # =========================================================================
    story.append(Paragraph("3. Functional Requirements (MoSCoW Matrix)", style_h1))
    fr_data = [
        [Paragraph("ID", style_th), Paragraph("Pri.", style_th), Paragraph("Requirement Title", style_th), Paragraph("Detailed Acceptance Criteria", style_th)],
        [Paragraph("FR-01", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Multi-Format Ingestion", style_td_bold), Paragraph("Parses PDF, DOCX, TXT files up to 25MB; generates SHA-256 hash and sanitizes filename safely.", style_td)],
        [Paragraph("FR-02", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Document Grouping", style_td_bold), Paragraph("Organizes revisions into logical parent groups (e.g. 'Leave Policy' ➔ v1.0, v2.0, v3.0).", style_td)],
        [Paragraph("FR-03", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("SemVer & Lifecycle", style_td_bold), Paragraph("Parses SemVer tags; automatically transitions older active versions to SUPERSEDED when promoted.", style_td)],
        [Paragraph("FR-04", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Page-Aware Chunking", style_td_bold), Paragraph("Splits documents into 500-char chunks with 100-char overlap, binding exact page numbers to metadata.", style_td)],
        [Paragraph("FR-05", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Local Vector Embeddings", style_td_bold), Paragraph("Computes 768-dim embeddings via nomic-embed-text; fallback to deterministic 128-dim subword vectors.", style_td)],
        [Paragraph("FR-06", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Pre-Retrieval Filter", style_td_bold), Paragraph("Restricts general policy search strictly to `status = 'ACTIVE'`, blocking superseded chunks completely.", style_td)],
        [Paragraph("FR-07", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Historical Query Routing", style_td_bold), Paragraph("Identifies version intent (e.g. 'in v1.0') and routes retrieval to that version with a warning badge.", style_td)],
        [Paragraph("FR-08", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Verifiable Citations", style_td_bold), Paragraph("Every answer must output document name, version tag, page number, and verbatim excerpt.", style_td)],
        [Paragraph("FR-09", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Conflict Sentinel", style_td_bold), Paragraph("Flags a prominent alert when multiple active policies coexist in the same group, preventing silent blends.", style_td)],
        [Paragraph("FR-10", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Missing Evidence Gate", style_td_bold), Paragraph("Returns explicit insufficient evidence status if similarity score < 0.45 or query is unanswerable.", style_td)],
        [Paragraph("FR-11", style_td_center), Paragraph("SHOULD", style_td_bold), Paragraph("1-Click Seed Dataset", style_td_bold), Paragraph("Dashboard button instantly loads Leave Policy and Remote Security Policy revision test suites.", style_td)],
        [Paragraph("FR-12", style_td_center), Paragraph("SHOULD", style_td_bold), Paragraph("Audit Telemetry Log", style_td_bold), Paragraph("Stores complete query string, cited version IDs, matched chunk IDs, latency, and timestamp.", style_td)],
        [Paragraph("FR-13", style_td_center), Paragraph("COULD", style_td_bold), Paragraph("Visual Version Diff", style_td_bold), Paragraph("Interactive UI diff showing clause additions, removals, and changes between two revisions.", style_td)]
    ]
    t_fr = Table(fr_data, colWidths=[34, 40, 115, 342])
    t_fr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('TEXTCOLOR', (1,1), (1,10), colors.HexColor("#991B1B")),
        ('TEXTCOLOR', (1,11), (1,12), colors.HexColor("#854D0E")),
        ('TEXTCOLOR', (1,13), (1,13), colors.HexColor("#3730A3")),
    ]))
    story.append(t_fr)
    story.append(Spacer(1, 3))

    story.append(Paragraph("4. Non-Functional Engineering Requirements (NFR)", style_h1))
    nfr_data = [
        [Paragraph("ID", style_th), Paragraph("NFR Category", style_th), Paragraph("Engineering Target Metric", style_th), Paragraph("Verification & Validation Procedure", style_th)],
        [Paragraph("NFR-01", style_td_center), Paragraph("Inference Latency", style_td_bold), Paragraph("< 2.5s (Extractive); < 4.0s (Ollama)", style_td), Paragraph("Benchmarked on standard developer CPU/GPU across 50 consecutive queries.", style_td)],
        [Paragraph("NFR-02", style_td_center), Paragraph("Retrieval Speed", style_td_bold), Paragraph("< 150 ms across 10,000 chunks", style_td), Paragraph("In-memory vector cosine distance timing tracked via backend performance middleware.", style_td)],
        [Paragraph("NFR-03", style_td_center), Paragraph("Air-Gapped Security", style_td_bold), Paragraph("Zero External Cloud Data Outbound", style_td), Paragraph("Packet monitoring confirming zero outbound HTTP requests to external AI APIs.", style_td)],
        [Paragraph("NFR-04", style_td_center), Paragraph("High Availability", style_td_bold), Paragraph("100% Service Uptime Fallback", style_td), Paragraph("Automatic fallback to deterministic extractive synthesizer if Ollama daemon halts.", style_td)],
        [Paragraph("NFR-05", style_td_center), Paragraph("Storage Sanitization", style_td_bold), Paragraph("Zero Path Traversal / MIME-sniffed", style_td), Paragraph("Automated path sanitization tests preventing `../` directory injection attacks.", style_td)],
        [Paragraph("NFR-06", style_td_center), Paragraph("Evidence Grounding", style_td_bold), Paragraph("> 95% Verified Citation Accuracy", style_td), Paragraph("Factuality benchmark comparing synthesized claims to verbatim source document excerpts.", style_td)]
    ]
    t_nfr = Table(nfr_data, colWidths=[38, 90, 140, 263])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_nfr)

    # END OF PAGE 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: DATA SCHEMA, REST APIS & VERIFICATION MATRIX
    # =========================================================================
    story.append(Paragraph("5. Relational Data Model & Storage Schema", style_h1))
    schema_data = [
        [Paragraph("Entity Table", style_th), Paragraph("Key Fields & Types", style_th), Paragraph("Relational Integrity & Lifecycle Constraints", style_th)],
        [Paragraph("document_groups", style_td_bold), Paragraph("id (UUID), name (TEXT), category (TEXT), description, created_at", style_td), Paragraph("Parent entity for version lineages; cascades deletion to versions.", style_td)],
        [Paragraph("document_versions", style_td_bold), Paragraph("id (UUID), group_id (FK), version_string, status, effective_date, file_path, checksum", style_td), Paragraph("Enforces lifecycle status ('ACTIVE', 'SUPERSEDED', 'DRAFT', 'ARCHIVED'); SHA-256 integrity.", style_td)],
        [Paragraph("document_chunks", style_td_bold), Paragraph("id (UUID), version_id (FK), chunk_index (INT), page_number (INT), content (TEXT), embedding", style_td), Paragraph("Stores exact document page numbers and chunk offsets for verifiable citations.", style_td)],
        [Paragraph("audit_logs", style_td_bold), Paragraph("id (UUID), query_text, cited_version_id, confidence, engine_used, latency_ms, timestamp", style_td), Paragraph("Tamper-evident query telemetry for ISO 27001 and NIST SP 800-53 audit compliance.", style_td)]
    ]
    t_schema = Table(schema_data, colWidths=[95, 185, 251])
    t_schema.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_schema)
    story.append(Spacer(1, 3))

    story.append(Paragraph("6. REST API Endpoints Specification", style_h1))
    api_data = [
        [Paragraph("HTTP Method & Route", style_th), Paragraph("Request Payload / Headers", style_th), Paragraph("Response Behavior & Output Codes", style_th)],
        [Paragraph("POST /api/documents/upload", style_td_bold), Paragraph("Multipart: file, group_id, version_string, status, effective_date", style_td), Paragraph("201 Created: Sanitizes file, chunks text, generates embeddings, updates lineage tree.", style_td)],
        [Paragraph("GET /api/documents", style_td_bold), Paragraph("Query params: category, search (Optional)", style_td), Paragraph("200 OK: Returns list of document groups with active version number and total counts.", style_td)],
        [Paragraph("GET /api/documents/:id/versions", style_td_bold), Paragraph("Path: Document Group ID", style_td), Paragraph("200 OK: Returns complete parent-child version lineage tree with lifecycle statuses.", style_td)],
        [Paragraph("POST /api/chat/query", style_td_bold), Paragraph("JSON: { query: string, document_id?: string }", style_td), Paragraph("200 OK: Classifies intent, filters active version, generates answer with page citations.", style_td)],
        [Paragraph("POST /api/demo/seed", style_td_bold), Paragraph("Empty body (Trigger)", style_td), Paragraph("200 OK: Loads Leave Policy and Remote Security Policy 3-version demo datasets.", style_td)],
        [Paragraph("GET /api/health", style_td_bold), Paragraph("Empty body", style_td), Paragraph("200 OK: Reports connection status for PostgreSQL, SQLite fallback, and local Ollama.", style_td)]
    ]
    t_api = Table(api_data, colWidths=[120, 160, 251])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_api)
    story.append(Spacer(1, 3))

    story.append(Paragraph("7. Automated Test Suite & Hackathon Verification Matrix", style_h1))
    test_data = [
        [Paragraph("Test Case #", style_th), Paragraph("Verification Scenario", style_th), Paragraph("Input Query / Action", style_th), Paragraph("Pass / Fail Criteria", style_th)],
        [Paragraph("TEST-01", style_td_center), Paragraph("Metadata Ingestion", style_td_bold), Paragraph("Upload 3-version Leave Policy", style_td), Paragraph("PASS: Creates v1.0, v2.0, v3.0 parent-child lineage in metadata DB.", style_td)],
        [Paragraph("TEST-02", style_td_center), Paragraph("Active Version Query", style_td_bold), Paragraph("'What is the annual leave allowance?'", style_td), Paragraph("PASS: Returns 20 days citing v3.0 [Active], Page 1. Rejects v1.0/v2.0.", style_td)],
        [Paragraph("TEST-03", style_td_center), Paragraph("Historical Query", style_td_bold), Paragraph("'What was the allowance in version 2?'", style_td), Paragraph("PASS: Returns 18 days citing v2.0 with [Historical Record] banner.", style_td)],
        [Paragraph("TEST-04", style_td_center), Paragraph("Missing Evidence Gate", style_td_bold), Paragraph("'Where is maternity leave explained?'", style_td), Paragraph("PASS: Returns explicit Insufficient Evidence status without hallucinating.", style_td)],
        [Paragraph("TEST-05", style_td_center), Paragraph("Conflict Sentinel Alert", style_td_bold), Paragraph("Simulate two concurrent active versions", style_td), Paragraph("PASS: Dispatches live Conflict Sentinel alert, halting single answer.", style_td)],
        [Paragraph("TEST-06", style_td_center), Paragraph("Deletion Cleanup", style_td_bold), Paragraph("Delete document group", style_td), Paragraph("PASS: Cascades deletion across metadata DB and in-memory vector store.", style_td)]
    ]
    t_test = Table(test_data, colWidths=[45, 105, 140, 241])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_test)

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_prd_pdf()
