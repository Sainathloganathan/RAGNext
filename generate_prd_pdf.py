import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether
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
        # Page 1: Cover page banner
        if self._pageNumber == 1:
            self.saveState()
            self.setFillColor(colors.HexColor("#059669")) # Emerald Accent Bar
            self.rect(0, 815, 595.27, 27, fill=1, stroke=0)
            self.setFillColor(GREEN_DARK)
            self.rect(0, 810, 595.27, 5, fill=1, stroke=0)
            self.restoreState()
            return

        # Pages 2+: Running Header
        self.saveState()
        self.setFillColor(NAVY_HEADER)
        self.rect(0, 815, 595.27, 27, fill=1, stroke=0)

        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 8.5)
        self.drawString(36, 824, "PRD | RAGNext — Autonomous Version-Aware Document Intelligence Engine")
        self.drawRightString(595.27 - 36, 824, "Team Cyber Knights (SH-SVA-04)")

        # Running Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(36, 36, 595.27 - 36, 36)

        self.setFillColor(TEXT_MUTED)
        self.setFont("Helvetica", 8)
        self.drawString(36, 24, "Confidential — Product Requirements Document (PRD)")
        self.drawRightString(595.27 - 36, 24, f"Page {self._pageNumber} of {total_pages}")
        self.restoreState()

def create_prd_pdf(output_path="RAGNext_Stage2_PRD_Cyber_Knights.pdf"):
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    style_cover_cat = ParagraphStyle(
        'CoverCategory',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#475569"),
        alignment=1,
        spaceAfter=14
    )

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=26,
        textColor=GREEN_DARK,
        alignment=1,
        spaceAfter=10
    )

    style_cover_sub = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#334155"),
        alignment=1,
        spaceAfter=22
    )

    style_h1 = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11.5,
        leading=14,
        textColor=GREEN_ACCENT,
        spaceBefore=7,
        spaceAfter=4,
        keepWithNext=True
    )

    style_body = ParagraphStyle(
        'BodyTextCustom',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.8,
        leading=10.2,
        textColor=TEXT_DARK,
        spaceAfter=3.5
    )

    style_table_header = ParagraphStyle(
        'TableHeader',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.8,
        leading=9.5,
        textColor=WHITE,
        alignment=0
    )

    style_table_cell = ParagraphStyle(
        'TableCell',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.0,
        textColor=TEXT_DARK
    )

    style_table_cell_bold = ParagraphStyle(
        'TableCellBold',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.0,
        textColor=TEXT_DARK
    )

    style_table_cell_center = ParagraphStyle(
        'TableCellCenter',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=7.2,
        leading=9.0,
        textColor=TEXT_DARK,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 140))
    story.append(Paragraph("PRODUCT REQUIREMENTS DOCUMENT (PRD)", style_cover_cat))
    story.append(Paragraph("Autonomous Version-Aware Document<br/>Intelligence Engine with Verifiable Grounding", style_cover_title))
    story.append(Paragraph("Stage 2 Engineering Specification | Hackathon Problem Statement SH-SVA-04", style_cover_sub))
    story.append(Spacer(1, 15))

    cover_meta_data = [
        [Paragraph("Product Name", style_table_cell_bold), Paragraph("RAGNext (Cyber Knights Document Intelligence)", style_table_cell)],
        [Paragraph("Document Type", style_table_cell_bold), Paragraph("Product Requirements Document (PRD) — Release v1.0", style_table_cell)],
        [Paragraph("Problem Statement ID", style_table_cell_bold), Paragraph("SH-SVA-04 (Smart Virtual Assistant for Version-Aware Document Search)", style_table_cell)],
        [Paragraph("Team Members", style_table_cell_bold), Paragraph("Sainath Loganathan, Tahir Azeem", style_table_cell)],
        [Paragraph("Core Architecture", style_table_cell_bold), Paragraph("Temporal Version Lineage Graph, Pre-Retrieval State Filtering, Local Ollama Inference", style_table_cell)],
        [Paragraph("Target Environment", style_table_cell_bold), Paragraph("Enterprise Air-Gapped / Offline-First / Zero Cloud Telemetry", style_table_cell)],
    ]
    t_cover = Table(cover_meta_data, colWidths=[140, 383])
    t_cover.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (0,-1), BG_ACCENT),
        ('BACKGROUND', (1,0), (1,-1), WHITE),
        ('BOX', (0,0), (-1,-1), 0.7, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 4.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4.5),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_cover)
    story.append(Spacer(1, 35))

    p_valid_problem = Paragraph(
        "<b>Core Principle:</b> <i>'Find the right information, from the right document version, with verifiable evidence.'</i><br/>"
        "RAGNext eliminates superseded document hallucinations by combining revision lineage graphs, metadata pre-retrieval filtering, and exact page-level grounded citations.",
        ParagraphStyle('CoverValidated', parent=styles['Normal'], fontName='Helvetica', fontSize=8.5, leading=12.5, textColor=TEXT_DARK, alignment=1)
    )
    story.append(p_valid_problem)
    story.append(Spacer(1, 28))

    story.append(Paragraph("<b>Problem First – Architecture Next – Verifiable Intelligence Always</b>", ParagraphStyle(
        'CoverSlogan', parent=styles['Normal'], fontName='Helvetica-Bold', fontSize=10, leading=13, textColor=GREEN_ACCENT, alignment=1
    )))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: TABLE OF CONTENTS & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Paragraph("Table of Contents", style_h1))
    toc_data = [
        [Paragraph("#", style_table_header), Paragraph("Section", style_table_header), Paragraph("#", style_table_header), Paragraph("Section", style_table_header)],
        [Paragraph("1", style_table_cell_center), Paragraph("Executive Summary & Product Vision", style_table_cell), Paragraph("6", style_table_cell_center), Paragraph("Non-Functional Requirements (NFR)", style_table_cell)],
        [Paragraph("2", style_table_cell_center), Paragraph("Problem Statement & Scope", style_table_cell), Paragraph("7", style_table_cell_center), Paragraph("Data Model & Database Schema", style_table_cell)],
        [Paragraph("3", style_table_cell_center), Paragraph("User Personas & User Journeys", style_table_cell), Paragraph("8", style_table_cell_center), Paragraph("REST API Endpoints Specification", style_table_cell)],
        [Paragraph("4", style_table_cell_center), Paragraph("System Architecture & Tech Stack", style_table_cell), Paragraph("9", style_table_cell_center), Paragraph("UI & Screen Workflows", style_table_cell)],
        [Paragraph("5", style_table_cell_center), Paragraph("Functional Requirements (MoSCoW)", style_table_cell), Paragraph("10", style_table_cell_center), Paragraph("Success Metrics & Milestones", style_table_cell)],
    ]
    t_toc = Table(toc_data, colWidths=[25, 235, 25, 238])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 6))

    story.append(Paragraph("1. Executive Summary & Product Vision", style_h1))
    story.append(Paragraph(
        "<b>1.1 Product Vision:</b> RAGNext is an autonomous, version-aware enterprise document intelligence engine designed to eliminate superseded clause hallucinations. Unlike conventional vector-only RAG pipelines, RAGNext embeds temporal lifecycle states directly into document embeddings and metadata graphs, guaranteeing that employees and compliance officers receive authoritative, current-version information with verifiable page-level evidence.",
        style_body
    ))
    story.append(Paragraph(
        "<b>1.2 Business Impact:</b> 100% elimination of outdated policy citations, 60% reduction in document audit turnaround time, complete defense against regulatory non-compliance fines, and zero cloud API dependency through local air-gapped LLM inference.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Problem Statement & Scope Boundaries", style_h1))
    scope_data = [
        [Paragraph("Scope Area", style_table_header), Paragraph("In-Scope (Current Release v1.0)", style_table_header), Paragraph("Out-of-Scope (Future Releases)", style_table_header)],
        [Paragraph("Document Formats", style_table_cell_bold), Paragraph("PDF, DOCX, TXT, Markdown with page-aware extraction.", style_table_cell), Paragraph("Scanned raster images, audio/video transcripts.", style_table_cell)],
        [Paragraph("Version Lifecycle", style_table_cell_bold), Paragraph("DRAFT, ACTIVE, SUPERSEDED, ARCHIVED states with auto-transitions.", style_table_cell), Paragraph("Git-style three-way file merging of conflicting clauses.", style_table_cell)],
        [Paragraph("Retrieval Logic", style_table_cell_bold), Paragraph("Pre-retrieval temporal filtering, explicit historical intent routing.", style_table_cell), Paragraph("Cross-lingual translation of foreign language policies.", style_table_cell)],
        [Paragraph("Inference & Storage", style_table_cell_bold), Paragraph("Local Ollama (llama3.2 + nomic-embed-text), SQLite, local vector store.", style_table_cell), Paragraph("Third-party cloud AI APIs (OpenAI/Anthropic) to maintain sovereignty.", style_table_cell)],
    ]
    t_scope = Table(scope_data, colWidths=[90, 215, 218])
    t_scope.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_scope)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: USER PERSONAS & ARCHITECTURE
    # =========================================================================
    story.append(Paragraph("3. User Personas & System Workflows", style_h1))
    persona_text = [
        [Paragraph("Persona Profile", style_table_header), Paragraph("Goals & Responsibilities", style_table_header), Paragraph("RAGNext Solution Feature", style_table_header)],
        [Paragraph("<b>Rajesh</b><br/>Compliance & Risk Auditor", style_table_cell), Paragraph("Audits historical policies; verifies clause validity at past incident dates; avoids legal penalties.", style_table_cell), Paragraph("Historical Version Query Mode; automatic active conflict sentinel; downloadable audit logs.", style_table_cell)],
        [Paragraph("<b>Priya</b><br/>Knowledge Worker / Employee", style_table_cell), Paragraph("Needs rapid, trusted answers to policy questions (remote work security, leave benefits).", style_table_cell), Paragraph("Default Active Pre-Filtering; returns clear badges (v3.0 [Active]) with verbatim page citations.", style_table_cell)],
        [Paragraph("<b>Dev / IT Admin</b><br/>Systems Administrator", style_table_cell), Paragraph("Ensures system availability; protects company data privacy; avoids high cloud API costs.", style_table_cell), Paragraph("100% offline local inference via Ollama; zero external cloud data transfer.", style_table_cell)],
    ]
    t_per = Table(persona_text, colWidths=[110, 205, 208])
    t_per.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_per)
    story.append(Spacer(1, 6))

    story.append(Paragraph("4. System Architecture & Technical Specifications", style_h1))
    story.append(Paragraph(
        "RAGNext employs a decoupled, three-tier architecture ensuring high throughput, modularity, and zero cloud dependency:",
        style_body
    ))

    arch_data = [
        [Paragraph("Tier", style_table_header), Paragraph("Technology Component", style_table_header), Paragraph("Operational Function", style_table_header)],
        [Paragraph("Presentation Tier", style_table_cell_bold), Paragraph("React 18 + Vite + Bootstrap 5 + Lucide", style_table_cell), Paragraph("Responsive dashboard, document library, version graph viewer, and AI chat with citation cards.", style_table_cell)],
        [Paragraph("Application Tier", style_table_cell_bold), Paragraph("Node.js 18+ / Express.js (ES Modules)", style_table_cell), Paragraph("REST API gateway, multipart document parser, temporal filter engine, and conflict detector.", style_table_cell)],
        [Paragraph("Parsing Engine", style_table_cell_bold), Paragraph("pdf-parse, mammoth (DOCX), text/markdown", style_table_cell), Paragraph("Page-aware coordinate extraction, 500-char semantic chunking with 100-char overlap.", style_table_cell)],
        [Paragraph("Metadata Storage", style_table_cell_bold), Paragraph("SQLite / PostgreSQL (Dual Adapter)", style_table_cell), Paragraph("Relational integrity for document groups, versions, statuses, and audit event logs.", style_table_cell)],
        [Paragraph("Vector Store", style_table_cell_bold), Paragraph("Embedded Persistent Vector DB / ChromaDB", style_table_cell), Paragraph("High-speed cosine distance calculation with pre-retrieval version ID filtering.", style_table_cell)],
        [Paragraph("Inference Engine", style_table_cell_bold), Paragraph("Ollama (llama3.2 + nomic-embed-text)", style_table_cell), Paragraph("Local 768-dim embeddings and conversational grounded synthesis with deterministic fallback.", style_table_cell)],
    ]
    t_arch = Table(arch_data, colWidths=[90, 180, 253])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_arch)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: FUNCTIONAL REQUIREMENTS (MoSCoW)
    # =========================================================================
    story.append(Paragraph("5. Functional Requirements (MoSCoW Matrix)", style_h1))
    
    fr_data = [
        [Paragraph("ID", style_table_header), Paragraph("Priority", style_table_header), Paragraph("Functional Requirement", style_table_header), Paragraph("Detailed Acceptance Criteria", style_table_header)],
        [Paragraph("FR-01", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Multi-Format Ingestion", style_table_cell), Paragraph("Ingests PDF, DOCX, TXT up to 25 MB; generates SHA-256 checksum and preserves page boundaries.", style_table_cell)],
        [Paragraph("FR-02", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Document Grouping", style_table_cell), Paragraph("Associates multiple versions into a unified parent group (e.g., 'Remote Work Security Policy').", style_table_cell)],
        [Paragraph("FR-03", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Lifecycle Management", style_table_cell), Paragraph("Supports ACTIVE, SUPERSEDED, DRAFT, ARCHIVED states; transitions older versions when promoted.", style_table_cell)],
        [Paragraph("FR-04", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Context-Aware Chunking", style_table_cell), Paragraph("Splits text into 500-char chunks with 100-char overlap; attaches page_number and version_id.", style_table_cell)],
        [Paragraph("FR-05", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Vector Embeddings", style_table_cell), Paragraph("Embeds chunks via local Ollama (nomic-embed-text) with fallback token frequency vectors.", style_table_cell)],
        [Paragraph("FR-06", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Temporal Pre-Filter", style_table_cell), Paragraph("Eliminates non-active versions from retrieval candidate set before cosine distance ranking.", style_table_cell)],
        [Paragraph("FR-07", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Historical Query Routing", style_table_cell), Paragraph("Detects queries targeting historical revisions (e.g. 'in v1.0') and routes retrieval accordingly.", style_table_cell)],
        [Paragraph("FR-08", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Verifiable Citations", style_table_cell), Paragraph("Returns document name, version tag, page number, and verbatim excerpt for every synthesized claim.", style_table_cell)],
        [Paragraph("FR-09", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Conflict Sentinel", style_table_cell), Paragraph("Flags a prominent alert when multiple active policies coexist within the same group.", style_table_cell)],
        [Paragraph("FR-10", style_table_cell_bold), Paragraph("MUST", style_table_cell_bold), Paragraph("Missing Evidence Gate", style_table_cell), Paragraph("Returns explicit insufficient evidence status if similarity score < 0.45 or query is out-of-scope.", style_table_cell)],
        [Paragraph("FR-11", style_table_cell_bold), Paragraph("SHOULD", style_table_cell_bold), Paragraph("1-Click Seed Dataset", style_table_cell), Paragraph("Dashboard button instantly loads Leave Policy and Remote Security Policy test suites.", style_table_cell)],
        [Paragraph("FR-12", style_table_cell_bold), Paragraph("SHOULD", style_table_cell_bold), Paragraph("Audit Telemetry Log", style_table_cell), Paragraph("Records query string, retrieved chunk IDs, cited versions, latency, and timestamp to audit store.", style_table_cell)],
        [Paragraph("FR-13", style_table_cell_bold), Paragraph("COULD", style_table_cell_bold), Paragraph("Side-by-Side Diff View", style_table_cell), Paragraph("Interactive UI diff showing clause additions, removals, and changes between two revisions.", style_table_cell)],
    ]
    t_fr = Table(fr_data, colWidths=[32, 45, 145, 301])
    t_fr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('TEXTCOLOR', (1,1), (1,10), colors.HexColor("#991B1B")),
        ('TEXTCOLOR', (1,11), (1,12), colors.HexColor("#854D0E")),
        ('TEXTCOLOR', (1,13), (1,13), colors.HexColor("#3730A3")),
    ]))
    story.append(t_fr)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: NON-FUNCTIONAL REQUIREMENTS & DATA SCHEMA
    # =========================================================================
    story.append(Paragraph("6. Non-Functional Requirements (NFR)", style_h1))
    nfr_data = [
        [Paragraph("ID", style_table_header), Paragraph("Category", style_table_header), Paragraph("Target Metric", style_table_header), Paragraph("Validation Method", style_table_header)],
        [Paragraph("NFR-01", style_table_cell_bold), Paragraph("Inference Latency", style_table_cell), Paragraph("< 3.5 seconds response time", style_table_cell), Paragraph("Benchmarked on local Ollama llama3.2 using 50 consecutive queries.", style_table_cell)],
        [Paragraph("NFR-02", style_table_cell_bold), Paragraph("Retrieval Speed", style_table_cell), Paragraph("< 150 ms for 10,000 chunks", style_table_cell), Paragraph("Vector distance timing tracked in backend processing middleware.", style_table_cell)],
        [Paragraph("NFR-03", style_table_cell_bold), Paragraph("Data Sovereignty", style_table_cell), Paragraph("100% Air-Gapped / Zero Cloud Outbound", style_table_cell), Paragraph("Network packet monitoring verifying zero outbound requests during inference.", style_table_cell)],
        [Paragraph("NFR-04", style_table_cell_bold), Paragraph("Fault Tolerance", style_table_cell), Paragraph("100% Service Availability Fallback", style_table_cell), Paragraph("Automatic switch to deterministic extractive synthesis if Ollama is halted.", style_table_cell)],
        [Paragraph("NFR-05", style_table_cell_bold), Paragraph("Security & Sanitization", style_table_cell), Paragraph("Cryptographic file hashes; no path traversal", style_table_cell), Paragraph("Path sanitization tests preventing '../' injection in upload routes.", style_table_cell)],
    ]
    t_nfr = Table(nfr_data, colWidths=[40, 95, 140, 248])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_nfr)
    story.append(Spacer(1, 6))

    story.append(Paragraph("7. Data Model & Database Schema", style_h1))
    story.append(Paragraph(
        "RAGNext structures enterprise documents into an explicit relational hierarchy ensuring temporal integrity and cascade-safe updates:",
        style_body
    ))

    schema_data = [
        [Paragraph("Table Name", style_table_header), Paragraph("Key Columns", style_table_header), Paragraph("Relationships & Constraints", style_table_header)],
        [Paragraph("document_groups", style_table_cell_bold), Paragraph("id, name, category, description, created_at", style_table_cell), Paragraph("Top-level grouping container; 1-to-N with document_versions.", style_table_cell)],
        [Paragraph("document_versions", style_table_cell_bold), Paragraph("id, group_id, version_string, status, effective_date, file_path, checksum, is_conflict", style_table_cell), Paragraph("Foreign Key ➔ document_groups(id) ON DELETE CASCADE. Enforces status lifecycle.", style_table_cell)],
        [Paragraph("chunks", style_table_cell_bold), Paragraph("id, version_id, chunk_index, page_number, content, token_count, vector_id", style_table_cell), Paragraph("Foreign Key ➔ document_versions(id) ON DELETE CASCADE. Stores page coordinates.", style_table_cell)],
        [Paragraph("audit_logs", style_table_cell_bold), Paragraph("id, query_text, version_intent, retrieved_chunk_ids, cited_version_ids, latency_ms", style_table_cell), Paragraph("Immutable query audit trail required by ISO 27001 and NIST 800-53 standards.", style_table_cell)],
    ]
    t_sch = Table(schema_data, colWidths=[95, 195, 233])
    t_sch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_sch)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: API SPECIFICATION & SCREEN WORKFLOWS
    # =========================================================================
    story.append(Paragraph("8. REST API Endpoints Specification", style_h1))
    api_data = [
        [Paragraph("Method", style_table_header), Paragraph("Endpoint Route", style_table_header), Paragraph("Payload / Parameters", style_table_header), Paragraph("Response Description", style_table_header)],
        [Paragraph("GET", style_table_cell_bold), Paragraph("/api/health", style_table_cell), Paragraph("None", style_table_cell), Paragraph("Returns server, database adapter, and vector store health status.", style_table_cell)],
        [Paragraph("GET", style_table_cell_bold), Paragraph("/api/documents", style_table_cell), Paragraph("None", style_table_cell), Paragraph("Lists all document groups, version counts, and active version details.", style_table_cell)],
        [Paragraph("POST", style_table_cell_bold), Paragraph("/api/documents/upload", style_table_cell), Paragraph("file (multipart), groupId, version, status", style_table_cell), Paragraph("Parses document, extracts pages, chunks text, generates embeddings.", style_table_cell)],
        [Paragraph("GET", style_table_cell_bold), Paragraph("/api/versions/:groupId", style_table_cell), Paragraph("groupId (path)", style_table_cell), Paragraph("Returns ordered revision lineage tree with conflict indicators.", style_table_cell)],
        [Paragraph("PATCH", style_table_cell_bold), Paragraph("/api/versions/:id/status", style_table_cell), Paragraph("{ status: 'ACTIVE' | 'SUPERSEDED' }", style_table_cell), Paragraph("Updates version lifecycle state; propagates supersession.", style_table_cell)],
        [Paragraph("POST", style_table_cell_bold), Paragraph("/api/chat", style_table_cell), Paragraph("{ query, groupId, versionFilter }", style_table_cell), Paragraph("Executes version-aware RAG, returns answer with exact citations.", style_table_cell)],
        [Paragraph("POST", style_table_cell_bold), Paragraph("/api/demo/seed", style_table_cell), Paragraph("None", style_table_cell), Paragraph("Seeds multi-version Leave Policy and Remote Security Policy test files.", style_table_cell)],
    ]
    t_api = Table(api_data, colWidths=[40, 115, 140, 228])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_api)
    story.append(Spacer(1, 6))

    story.append(Paragraph("9. UI & Screen Workflows", style_h1))
    screen_data = [
        [Paragraph("Screen / Route", style_table_header), Paragraph("Key Visual Elements", style_table_header), Paragraph("User Actions Supported", style_table_header)],
        [Paragraph("Dashboard (/)", style_table_cell_bold), Paragraph("KPI cards (Docs, Active, Superseded), 1-Click Demo Seed, quick activity feed.", style_table_cell), Paragraph("Quick status review, instantaneous demo dataset provisioning.", style_table_cell)],
        [Paragraph("Document Library (/documents)", style_table_cell_bold), Paragraph("Grouped document cards, active version badges, format badges.", style_table_cell), Paragraph("Inspect revision histories, download files, delete outdated groups.", style_table_cell)],
        [Paragraph("Ingestion Portal (/upload)", style_table_cell_bold), Paragraph("Drag-and-drop file zone, metadata inputs, parsing progress bar.", style_table_cell), Paragraph("Upload new document revisions, assign version numbers, set status.", style_table_cell)],
        [Paragraph("AI Chat (/chat)", style_table_cell_bold), Paragraph("Conversational bubble stream, citation cards, conflict alert banner.", style_table_cell), Paragraph("Ask natural language questions; inspect exact version, page, and excerpt.", style_table_cell)],
        [Paragraph("Version History (/versions/:id)", style_table_cell_bold), Paragraph("Interactive timeline (v1.0 ➔ v2.0 ➔ v3.0), status toggles.", style_table_cell), Paragraph("Promote draft to active, supersede versions, view clause diffs.", style_table_cell)],
        [Paragraph("Settings (/settings)", style_table_cell_bold), Paragraph("Ollama connectivity pill, model selector, DB adapter indicator.", style_table_cell), Paragraph("Test local LLM connection, inspect vector chunk counts.", style_table_cell)],
    ]
    t_scr = Table(screen_data, colWidths=[105, 205, 213])
    t_scr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.4),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_scr)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: KPIS, TEST MATRIX & RELEASE MILESTONES
    # =========================================================================
    story.append(Paragraph("10. Success Metrics, Test Matrix & Release Milestones", style_h1))
    
    kpi_data = [
        [Paragraph("Key Performance Indicator (KPI)", style_table_header), Paragraph("Benchmark Target", style_table_header), Paragraph("Observed Test Result", style_table_header)],
        [Paragraph("Superseded Clause Citation Rate", style_table_cell_bold), Paragraph("0.0% (Zero Tolerance)", style_table_cell), Paragraph("0.0% — Active filter successfully rejects v1.0 and v2.0 clauses.", style_table_cell)],
        [Paragraph("Grounded Citation Precision", style_table_cell_bold), Paragraph("100% with Page Coordinates", style_table_cell), Paragraph("100% — Every claim includes doc title, version, page, and quote.", style_table_cell)],
        [Paragraph("Missing Evidence Rejection", style_table_cell_bold), Paragraph("0.0% Hallucinations on Unseen Data", style_table_cell), Paragraph("Verified — Reports 'insufficient evidence' for out-of-scope queries.", style_table_cell)],
        [Paragraph("End-to-End Local Inference Speed", style_table_cell_bold), Paragraph("< 4.0 seconds per query", style_table_cell), Paragraph("1.2 - 2.8 seconds on Ollama llama3.2 (local host).", style_table_cell)],
        [Paragraph("Offline Air-Gap Compliance", style_table_cell_bold), Paragraph("100% Zero External Requests", style_table_cell), Paragraph("Verified — Zero outbound telemetry or external cloud API calls.", style_table_cell)],
    ]
    t_kpi = Table(kpi_data, colWidths=[150, 150, 223])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 8))

    story.append(Paragraph("<b>Release Milestones & Delivery Roadmap:</b>", style_body))
    milestone_data = [
        [Paragraph("Phase", style_table_header), Paragraph("Milestone Deliverables", style_table_header), Paragraph("Status", style_table_header)],
        [Paragraph("Stage 1 (Framing)", style_table_cell_bold), Paragraph("Problem definition, root-cause analysis, market opportunity framing PPT.", style_table_cell), Paragraph("COMPLETED", style_table_cell_bold)],
        [Paragraph("Stage 2 (MRD Submission)", style_table_cell_bold), Paragraph("Formal 9-page Market Requirements Document (PDF) with user personas and business model.", style_table_cell), Paragraph("COMPLETED", style_table_cell_bold)],
        [Paragraph("Stage 2 (PRD & MVP Release)", style_table_cell_bold), Paragraph("Functional React 18 UI, Express backend, Ollama integration, automated RAG test suite, PRD.", style_table_cell), Paragraph("ACTIVE / OPERATIONAL", style_table_cell_bold)],
        [Paragraph("Stage 3 (Enterprise Scale)", style_table_cell_bold), Paragraph("OCR scanner integration, enterprise SharePoint connectors, Active Directory RBAC.", style_table_cell), Paragraph("PLANNED ROADMAP", style_table_cell)],
    ]
    t_ms = Table(milestone_data, colWidths=[110, 313, 100])
    t_ms.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
        ('TEXTCOLOR', (2,1), (2,3), GREEN_ACCENT),
    ]))
    story.append(t_ms)

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PRD PDF at: {output_path}")

if __name__ == "__main__":
    output_filename = "RAGNext_Stage2_PRD_Cyber_Knights.pdf"
    if len(sys.argv) > 1:
        output_filename = sys.argv[1]
    create_prd_pdf(output_filename)
