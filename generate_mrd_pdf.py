import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, BaseDocTemplate, PageTemplate, Frame
)
from reportlab.graphics.shapes import (
    Drawing, Rect, String, Line, Group, Polygon
)
from reportlab.pdfgen import canvas

# Palette Constants
NAVY_HEADER = colors.HexColor("#1A365D")   # Sample dark navy header bar
GREEN_ACCENT = colors.HexColor("#15803D")  # Sample deep green section heading
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
    """
    Two-pass canvas to accurately draw headers and footers with total page count.
    """
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
        # Page 1 is the cover page
        if self._pageNumber == 1:
            # Draw top decorative accent bar
            self.saveState()
            self.setFillColor(colors.HexColor("#3B82F6"))
            self.rect(0, 815, 595.27, 27, fill=1, stroke=0)
            self.setFillColor(colors.HexColor("#1D4ED8"))
            self.rect(0, 810, 595.27, 5, fill=1, stroke=0)
            self.restoreState()
            return

        # Pages 2 to 9: Running Header
        self.saveState()
        # Header banner rectangle
        self.setFillColor(NAVY_HEADER)
        self.rect(0, 815, 595.27, 27, fill=1, stroke=0)

        # Header text
        self.setFillColor(WHITE)
        self.setFont("Helvetica-Bold", 8.5)
        self.drawString(36, 824, "MRD | RAGNext — Version-Aware Document Intelligence Engine")
        self.drawRightString(595.27 - 36, 824, "Team Cyber Knights")

        # Running Footer
        self.setStrokeColor(BORDER_COLOR)
        self.setLineWidth(0.5)
        self.line(36, 36, 595.27 - 36, 36)

        self.setFillColor(TEXT_MUTED)
        self.setFont("Helvetica", 8)
        self.drawString(36, 24, "Stage 2 - Market Requirements Document")
        self.drawRightString(595.27 - 36, 24, f"Page {self._pageNumber}")
        self.restoreState()

def create_mrd_pdf(output_path="RAGNext_Stage2_MRD_Cyber_Knights.pdf"):
    # Page setup: A4 = 595.27 x 841.89 points
    # Margins: 36 pt left & right, 44 pt top, 44 pt bottom
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        leftMargin=36,
        rightMargin=36,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Base typography styles
    style_cover_cat = ParagraphStyle(
        'CoverCategory',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=11,
        leading=14,
        textColor=colors.HexColor("#475569"),
        alignment=1, # Center
        spaceAfter=14
    )

    style_cover_title = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=21,
        leading=26,
        textColor=GREEN_DARK,
        alignment=1, # Center
        spaceAfter=10
    )

    style_cover_sub = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=11,
        leading=15,
        textColor=colors.HexColor("#334155"),
        alignment=1, # Center
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

    style_body_bold_intro = ParagraphStyle(
        'BodyBoldIntro',
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

    style_table_cell_priority = ParagraphStyle(
        'TableCellPriority',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=7.2,
        leading=9.0,
        alignment=1
    )

    story = []

    # =========================================================================
    # PAGE 1: COVER PAGE
    # =========================================================================
    story.append(Spacer(1, 140))
    story.append(Paragraph("MARKET REQUIREMENTS DOCUMENT", style_cover_cat))
    story.append(Paragraph("Autonomous Version-Aware Document<br/>Intelligence Engine with Verifiable Grounding", style_cover_title))
    story.append(Paragraph("Stage 2 Submission | Two-Stage Student Hackathon", style_cover_sub))
    story.append(Spacer(1, 15))

    cover_meta_data = [
        [Paragraph("Team Name", style_table_cell_bold), Paragraph("Cyber Knights", style_table_cell)],
        [Paragraph("Team Members", style_table_cell_bold), Paragraph("Sainath Loganathan, Tahir Azeem", style_table_cell)],
        [Paragraph("Institution / Department", style_table_cell_bold), Paragraph("B.E. Computer Science and Engineering (Cybersecurity & AI Lab)", style_table_cell)],
        [Paragraph("Domain", style_table_cell_bold), Paragraph("Enterprise AI, Document Governance, Cybersecurity & Compliance", style_table_cell)],
        [Paragraph("Technology", style_table_cell_bold), Paragraph("Local LLMs (Ollama / Llama 3.2), Vector Embeddings, Temporal Lineage Graph, Node.js, React", style_table_cell)],
        [Paragraph("Document", style_table_cell_bold), Paragraph("MRD (Stage 2) building on the validated Stage 1 Problem Framing PPT", style_table_cell)],
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
        "<b>Validated problem (Stage 1):</b> Traditional vector search and RAG systems blindly retrieve clauses from older or superseded document versions based on cosine similarity alone, leading to severe hallucinations, compliance violations, and outdated policy guidance.",
        ParagraphStyle(
            'CoverValidated',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=8.5,
            leading=12.5,
            textColor=TEXT_DARK,
            alignment=1
        )
    )
    story.append(p_valid_problem)
    story.append(Spacer(1, 28))

    p_slogan = Paragraph(
        "<i><b>Problem First – Solution Next – Technology Last</b></i>",
        ParagraphStyle(
            'CoverSlogan',
            parent=styles['Normal'],
            fontName='Helvetica-BoldOblique',
            fontSize=10,
            leading=13,
            textColor=GREEN_ACCENT,
            alignment=1
        )
    )
    story.append(p_slogan)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: CONTENTS, EXECUTIVE SUMMARY, TARGET MARKET
    # =========================================================================
    story.append(Paragraph("Contents", style_h1))

    toc_data = [
        [Paragraph("#", style_table_header), Paragraph("Section", style_table_header), Paragraph("#", style_table_header), Paragraph("Section", style_table_header)],
        [Paragraph("1", style_table_cell_center), Paragraph("Executive Summary", style_table_cell), Paragraph("8", style_table_cell_center), Paragraph("Technology Requirements", style_table_cell)],
        [Paragraph("2", style_table_cell_center), Paragraph("Target Market / User Segment", style_table_cell), Paragraph("9", style_table_cell_center), Paragraph("Competitor / Existing Solution Analysis", style_table_cell)],
        [Paragraph("3", style_table_cell_center), Paragraph("User Personas", style_table_cell), Paragraph("10", style_table_cell_center), Paragraph("Innovation", style_table_cell)],
        [Paragraph("4", style_table_cell_center), Paragraph("User Journey", style_table_cell), Paragraph("11", style_table_cell_center), Paragraph("MVP Definition", style_table_cell)],
        [Paragraph("5", style_table_cell_center), Paragraph("Solution Concept and Architecture", style_table_cell), Paragraph("12", style_table_cell_center), Paragraph("Success Metrics / KPIs", style_table_cell)],
        [Paragraph("6", style_table_cell_center), Paragraph("Functional Requirements (with priority)", style_table_cell), Paragraph("13", style_table_cell_center), Paragraph("Business / Sustainability Model", style_table_cell)],
        [Paragraph("7", style_table_cell_center), Paragraph("Non-Functional Requirements", style_table_cell), Paragraph("14", style_table_cell_center), Paragraph("Risk Analysis", style_table_cell)],
        [Paragraph("", style_table_cell_center), Paragraph("", style_table_cell), Paragraph("15", style_table_cell_center), Paragraph("Stage 1 Traceability and Checklist; References", style_table_cell)],
    ]
    t_toc = Table(toc_data, colWidths=[25, 235, 25, 238])
    t_toc.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_toc)
    story.append(Spacer(1, 4))

    story.append(Paragraph("1. Executive Summary", style_h1))
    story.append(Paragraph(
        "<b>Problem.</b> Modern enterprises operate across dozens of evolving policies, contracts, compliance handbooks, and SOPs. Conventional vector similarity search blindly retrieves clauses purely based on cosine distance. When policies undergo revisions (e.g., Leave Policy v1.0 ➔ v2.0 ➔ v3.0, or Remote Work Security Policy v1.0 ➔ v3.0), older superseded clauses frequently outscore active ones due to syntactic keywords. This leads to hallucinated answers, costly regulatory non-compliance, and dangerous operational errors. Stage 1 root-cause analysis traced this to one fundamental underlying gap: <b>a total absence of temporal version awareness, revision lineage tracking, and verifiable citation mechanisms in standard RAG pipelines.</b>",
        style_body
    ))
    story.append(Paragraph(
        "<b>Target users.</b> Compliance officers, legal auditors, cybersecurity/SOC analysts, HR directors, enterprise knowledge workers, and organizations in heavily regulated industries (BFSI, Healthcare, Defense, SMBs).",
        style_body
    ))
    story.append(Paragraph(
        "<b>Proposed solution.</b> <b>RAGNext</b> — an autonomous, version-aware Document Intelligence Engine that structures enterprise documents into dynamic revision lineages, applies pre-retrieval temporal validity filtering, proactively flags conflicting active revisions, and produces grounded answers backed by verbatim quotes and exact page citations.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Major benefit.</b> Completely eliminates superseded clause hallucinations; ensures employees and auditors receive authoritative, current-version information while preserving verifiable historical inquiry on demand.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Expected impact (from Stage 1 impact analysis):</b> 100% elimination of outdated policy citations, 60% reduction in document audit turnaround time, zero regulatory penalties from stale guidance, and offline air-gapped data sovereignty.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("2. Target Market / User Segment", style_h1))
    target_market_data = [
        [Paragraph("Category", style_table_header), Paragraph("Segment", style_table_header), Paragraph("Role in the solution", style_table_header)],
        [Paragraph("Primary users", style_table_cell_bold), Paragraph("Compliance officers, legal auditors, policy admins, SOC analysts", style_table_cell), Paragraph("Ingest documents, manage version life cycles, inspect conflict alerts, audit AI citations and verification logs.", style_table_cell)],
        [Paragraph("Secondary users", style_table_cell_bold), Paragraph("Enterprise employees, knowledge workers, HR & IT staff", style_table_cell), Paragraph("Query active policies; receive instant verified answers with verbatim page references and version tags.", style_table_cell)],
        [Paragraph("Decision maker", style_table_cell_bold), Paragraph("Chief Information Security Officers (CISO), Chief Legal Officers (CLO), IT Directors", style_table_cell), Paragraph("Approve adoption, enforce organizational compliance governance, mandate air-gapped data privacy.", style_table_cell)],
        [Paragraph("Beneficiaries", style_table_cell_bold), Paragraph("Entire enterprise workforce, end customers, audit regulators", style_table_cell), Paragraph("Guaranteed truthfulness, elimination of outdated guidance, and continuous compliance audit-readiness.", style_table_cell)],
        [Paragraph("Ecosystem stakeholders", style_table_cell_bold), Paragraph("Document Stores (SharePoint, Drive), Vector DBs, Enterprise ERPs", style_table_cell), Paragraph("Ingestion sources, metadata repositories, downstream verification consumers.", style_table_cell)],
        [Paragraph("Potential market", style_table_cell_bold), Paragraph("Regulated sectors (BFSI, Healthcare, Legal, Defense) and SMBs", style_table_cell), Paragraph("Organizations that require strict document compliance without expensive cloud SaaS exposure.", style_table_cell)],
    ]
    t_target = Table(target_market_data, colWidths=[95, 160, 268])
    t_target.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.8),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_target)
    story.append(Spacer(1, 3))
    story.append(Paragraph(
        "<i>The framework adheres to NIST SP 800-53 (Audit & Accountability, Information Integrity), ISO/IEC 27001:2022 (Documented Information Governance), and CISA Data Pillar principles, which require continuous data provenance and temporal validity.</i>",
        ParagraphStyle('NoteText', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=6.8, leading=8.5, textColor=TEXT_MUTED)
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: USER PERSONAS & USER JOURNEY
    # =========================================================================
    story.append(Paragraph("3. User Personas", style_h1))

    persona_a_text = """
    <b>Persona A: Enterprise Compliance & Risk Auditor</b><br/>
    <b>Role:</b> Manages regulatory compliance, corporate policies, and audits for an enterprise (name: <i>Rajesh, Head of Compliance</i>).<br/>
    <b>Operational goal:</b> Prevent employees from relying on superseded policies and provide verifiable, clause-level evidence during audits.<br/>
    <b>Current difficulty:</b> Multiple conflicting PDF versions circulate across shared drives; vector search tools mix old and new policy clauses; manual diffing of revisions takes hours.<br/>
    <b>Information needed:</b> Clear active vs historical revision lineage, exact page/paragraph citations, and automated alerts for contradictory active policies.<br/>
    <b>Decision needs:</b> Which version is legally binding, whether an older rule applied at a historical incident date, when to deprecate obsolete versions.<br/>
    <b>Technology usage:</b> Proficient with compliance dashboards, DMS portals, and document diffing; expects explainable evidence, not a black-box AI.<br/>
    <b>Expectations:</b> 100% grounded answers, zero superseded hallucinations, and transparent audit logs for all AI-retrieved facts.
    """

    persona_b_text = """
    <b>Persona B: Enterprise Knowledge Worker / Policy Consumer</b><br/>
    <b>Role:</b> Executes daily operations referencing corporate guidelines, benefits, and security manuals (name: <i>Priya, Operations Lead</i>).<br/>
    <b>Goal:</b> Rapid, accurate answers to policy questions (leave entitlement, remote security rules, procurement limits) without reading 80-page manuals.<br/>
    <b>Current problem:</b> A search on the intranet returns outdated rules from 2021; she risks policy violations because search results don't indicate if a rule has been updated.<br/>
    <b>Technology usage:</b> Daily use of intranet, Slack/Teams, web apps; expects conversational AI speed without complex prompting.<br/>
    <b>Expectations:</b> Clear answers showing exactly which document version was cited (e.g., 'Policy v3.0 [Active]'), direct quotes, and immediate warning if an older rule is cited.
    """

    personas_table_data = [
        [Paragraph(persona_a_text, style_body), Paragraph(persona_b_text, style_body)]
    ]
    t_personas = Table(personas_table_data, colWidths=[258, 265])
    t_personas.setStyle(TableStyle([
        ('BOX', (0,0), (0,0), 0.7, colors.HexColor("#93C5FD")),
        ('BOX', (1,0), (1,0), 0.7, colors.HexColor("#A7F3D0")),
        ('BACKGROUND', (0,0), (0,0), colors.HexColor("#EFF6FF")),
        ('BACKGROUND', (1,0), (1,0), BG_ACCENT),
        ('TOPPADDING', (0,0), (-1,-1), 5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('LEFTPADDING', (0,0), (-1,-1), 7),
        ('RIGHTPADDING', (0,0), (-1,-1), 7),
    ]))
    story.append(t_personas)
    story.append(Paragraph(
        "<i>Personas are representative profiles synthesized from enterprise stakeholder interviews in Stage 1; refined for regulated enterprise requirements.</i>",
        ParagraphStyle('PersonaNote', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=6.8, leading=8.5, textColor=TEXT_MUTED, spaceAfter=4)
    ))

    story.append(Paragraph("4. User Journey", style_h1))
    story.append(Paragraph("<b>Current journey (conventional unversioned RAG)</b>", style_body_bold_intro))

    current_journey_data = [
        [Paragraph("Step", style_table_header), Paragraph("What happens", style_table_header), Paragraph("Problem", style_table_header)],
        [Paragraph("1", style_table_cell_center), Paragraph("User uploads multiple PDF revisions into a standard vector database.", style_table_cell), Paragraph("All versions chunked identically; temporal context and version metadata lost.", style_table_cell)],
        [Paragraph("2", style_table_cell_center), Paragraph("Employee asks: 'What is the annual leave allowance?'", style_table_cell), Paragraph("Vector search performs blind cosine similarity across all chunks.", style_table_cell)],
        [Paragraph("3", style_table_cell_center), Paragraph("Chunk from v1.0 (15 days) has higher keyword similarity than v3.0 (20 days).", style_table_cell), Paragraph("Outdated clause retrieved due to keyword density; active v3.0 ignored.", style_table_cell)],
        [Paragraph("4", style_table_cell_center), Paragraph("LLM synthesizes answer claiming allowance is 15 days without citation.", style_table_cell), Paragraph("Black-box answer hallucinated from superseded document.", style_table_cell)],
        [Paragraph("5", style_table_cell_center), Paragraph("Employee plans leave based on obsolete clause; HR audit flags error.", style_table_cell), Paragraph("Employee frustration, operational dispute, and manual correction cost.", style_table_cell)],
    ]
    t_cur_j = Table(current_journey_data, colWidths=[30, 275, 218])
    t_cur_j.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_cur_j)
    story.append(Spacer(1, 4))

    story.append(Paragraph("<b>Proposed journey (RAGNext version-aware document intelligence)</b>", style_body_bold_intro))
    prop_journey_data = [
        [Paragraph("Step", style_table_header), Paragraph("What happens", style_table_header), Paragraph("Benefit", style_table_header)],
        [Paragraph("1", style_table_cell_center), Paragraph("Document uploaded; engine extracts version, effective date, status, and SHA-256.", style_table_cell), Paragraph("Cryptographic provenance and structured temporal metadata captured.", style_table_cell)],
        [Paragraph("2", style_table_cell_center), Paragraph("Page-aware chunker preserves coordinates; lineage engine builds revision graph.", style_table_cell), Paragraph("Exact page context preserved; document revisions formally linked.", style_table_cell)],
        [Paragraph("3", style_table_cell_center), Paragraph("Employee asks: 'What is the annual leave allowance?'", style_table_cell), Paragraph("Query classified as general policy inquiry; active filter applied.", style_table_cell)],
        [Paragraph("4", style_table_cell_center), Paragraph("Temporal pre-filter restricts vector search strictly to Active version (v3.0).", style_table_cell), Paragraph("Superseded chunks (v1.0, v2.0) are completely eliminated from retrieval.", style_table_cell)],
        [Paragraph("5", style_table_cell_center), Paragraph("Grounded engine returns '20 days' with exact citation: 'Leave Policy v3.0, Page 1'.", style_table_cell), Paragraph("Verifiable, authoritative answer with verbatim supporting evidence.", style_table_cell)],
        [Paragraph("6", style_table_cell_center), Paragraph("Auditor requests: 'What was it in v2.0?'; engine retrieves v2.0 with historical tag.", style_table_cell), Paragraph("Full historical transparency without risk of accidental contamination.", style_table_cell)],
    ]
    t_prop_j = Table(prop_journey_data, colWidths=[30, 275, 218])
    t_prop_j.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.3),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_prop_j)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 4: SOLUTION CONCEPT, ARCHITECTURE DIAGRAM & POLICY MATRIX
    # =========================================================================
    story.append(Paragraph("5. Solution Concept and Architecture", style_h1))
    story.append(Paragraph(
        "RAGNext is a modular document intelligence engine positioned between enterprise users and organizational knowledge repositories. Each module directly addresses a verified pain point from Stage 1:",
        style_body
    ))

    module_data = [
        [Paragraph("Module", style_table_header), Paragraph("What it does", style_table_header), Paragraph("Stage 1 problem it addresses", style_table_header)],
        [Paragraph("Multi-Format Ingestion", style_table_cell_bold), Paragraph("Parses PDF, DOCX, TXT with page-level boundary preservation and SHA-256 deduplication.", style_table_cell), Paragraph("Loss of structural layout and untracked file duplicates.", style_table_cell)],
        [Paragraph("Page-Aware Chunker", style_table_cell_bold), Paragraph("Splits text by semantic paragraphs while preserving exact source page numbers.", style_table_cell), Paragraph("Untraceable quotes and missing page citations in answers.", style_table_cell)],
        [Paragraph("Temporal Lineage Engine", style_table_cell_bold), Paragraph("Constructs directed version trees (v1.0 ➔ v2.0 ➔ v3.0) and manages lifecycle states.", style_table_cell), Paragraph("Flat document storage with no awareness of revision history.", style_table_cell)],
        [Paragraph("Temporal Filter & Vector Store", style_table_cell_bold), Paragraph("Enforces metadata pre-filtering on vector embeddings before cosine similarity ranking.", style_table_cell), Paragraph("Superseded clauses polluting search results and RAG contexts.", style_table_cell)],
        [Paragraph("Conflict Detection Sentinel", style_table_cell_bold), Paragraph("Identifies overlapping active documents within same domain; dispatches admin alerts.", style_table_cell), Paragraph("Silent policy contradictions leading to compliance liability.", style_table_cell)],
        [Paragraph("Grounded Synthesis Engine", style_table_cell_bold), Paragraph("Synthesizes responses strictly from retrieved chunks with verbatim quotes and citations.", style_table_cell), Paragraph("LLM hallucination, fabricated policy rules, and lack of proof.", style_table_cell)],
        [Paragraph("Audit & Compliance Store", style_table_cell_bold), Paragraph("Records full telemetry: queries, matched chunks, version IDs, scores, and timestamps.", style_table_cell), Paragraph("Lack of audit trail required by ISO 27001 and NIST SP 800-53.", style_table_cell)],
    ]
    t_mod = Table(module_data, colWidths=[115, 245, 163])
    t_mod.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_mod)
    story.append(Spacer(1, 4))

    # Clean Vector Drawing for Architecture Diagram
    d = Drawing(523, 115)
    # Background box for diagram
    d.add(Rect(0, 0, 523, 115, fillColor=colors.HexColor("#F8FAFC"), strokeColor=BORDER_COLOR, strokeWidth=0.5, rx=4, ry=4))

    # Box Helper Function
    def draw_box(x, y, w, h, title, sub, fill, stroke):
        g = Group()
        g.add(Rect(x, y, w, h, fillColor=fill, strokeColor=stroke, strokeWidth=0.8, rx=3, ry=3))
        g.add(String(x + w/2, y + h - 12, title, fontName="Helvetica-Bold", fontSize=7.5, textAnchor="middle", fillColor=TEXT_DARK))
        g.add(String(x + w/2, y + 8, sub, fontName="Helvetica", fontSize=6.2, textAnchor="middle", fillColor=TEXT_MUTED))
        return g

    def draw_arrow(x1, y1, x2, y2, stroke=colors.HexColor("#475569")):
        g = Group()
        g.add(Line(x1, y1, x2, y2, strokeColor=stroke, strokeWidth=1))
        # Arrowhead
        if x2 > x1: # Right
            g.add(Polygon([x2, y2, x2-4, y2+2.5, x2-4, y2-2.5], fillColor=stroke, strokeColor=stroke))
        elif x2 < x1: # Left
            g.add(Polygon([x2, y2, x2+4, y2+2.5, x2+4, y2-2.5], fillColor=stroke, strokeColor=stroke))
        elif y2 > y1: # Up
            g.add(Polygon([x2, y2, x2+2.5, y2-4, x2-2.5, y2-4], fillColor=stroke, strokeColor=stroke))
        elif y2 < y1: # Down
            g.add(Polygon([x2, y2, x2+2.5, y2+4, x2-2.5, y2+4], fillColor=stroke, strokeColor=stroke))
        return g

    # Row 1 (Ingestion Pipeline) y = 72
    d.add(draw_box(10, 72, 110, 32, "Document Ingestion", "PDF, DOCX, TXT + SHA-256", colors.HexColor("#EFF6FF"), colors.HexColor("#3B82F6")))
    d.add(draw_arrow(120, 88, 140, 88))

    d.add(draw_box(140, 72, 115, 32, "Page-Aware Chunker", "Page boundaries + offsets", colors.HexColor("#EFF6FF"), colors.HexColor("#3B82F6")))
    d.add(draw_arrow(255, 88, 275, 88))

    d.add(draw_box(275, 72, 115, 32, "Temporal Lineage Graph", "v1.0 ➔ v2.0 ➔ v3.0 Trees", colors.HexColor("#ECFDF5"), colors.HexColor("#10B981")))
    d.add(draw_arrow(390, 88, 410, 88))

    d.add(draw_box(410, 72, 103, 32, "Metadata & Vector DB", "PostgreSQL / SQLite + Chroma", colors.HexColor("#FEF3C7"), colors.HexColor("#F59E0B")))

    # Connect to Row 2
    d.add(draw_arrow(460, 72, 460, 48))

    # Row 2 (Retrieval & Synthesis) y = 16
    d.add(draw_box(10, 16, 110, 32, "User & Auditor Chat", "Natural language queries", colors.HexColor("#F3E8FF"), colors.HexColor("#8B5CF6")))
    d.add(draw_arrow(120, 32, 140, 32))

    d.add(draw_box(140, 16, 115, 32, "Temporal Rule Engine", "Active vs Historical routing", colors.HexColor("#ECFDF5"), colors.HexColor("#10B981")))
    d.add(draw_arrow(255, 32, 275, 32))

    d.add(draw_box(275, 16, 115, 32, "Conflict Sentinel", "Active overlap detector", colors.HexColor("#FEE2E2"), colors.HexColor("#EF4444")))
    d.add(draw_arrow(390, 32, 410, 32))

    d.add(draw_box(410, 16, 103, 32, "Grounded Synthesizer", "Verifiable page citations", colors.HexColor("#ECFDF5"), colors.HexColor("#10B981")))

    story.append(d)
    story.append(Paragraph(
        "<i>Figure 1: Solution architecture — version-aware ingestion, temporal filtering, and grounded citation loop</i>",
        ParagraphStyle('FigCap', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=7, leading=9, textColor=TEXT_MUTED, alignment=1, spaceBefore=3, spaceAfter=4)
    ))

    story.append(Paragraph("<b>Proposed version-to-action policy (rules enforced during retrieval)</b>", style_body_bold_intro))
    policy_matrix_data = [
        [Paragraph("Query Intent / Trigger", style_table_header), Paragraph("Target Version Scope", style_table_header), Paragraph("Automated Enforcement Action & Output Behavior", style_table_header)],
        [Paragraph("General Policy Query", style_table_cell_bold), Paragraph("Active Version (Latest)", style_table_cell), Paragraph("Hard metadata pre-filter (status='Active'). Ignores all superseded chunks. Answers strictly from active version with page citations.", style_table_cell)],
        [Paragraph("Historical Inquiry ('in v2.0')", style_table_cell_bold), Paragraph("Specific Version Requested", style_table_cell), Paragraph("Retrieves target historical version. Attaches prominent '[Historical Revision — Superseded]' warning banner to prevent accidental compliance reliance.", style_table_cell)],
        [Paragraph("Conflicting Active Policies", style_table_cell_bold), Paragraph("Multiple Active Versions", style_table_cell), Paragraph("Suspends automated single answer. Issues administrative 'Conflicting Active Revisions Detected' alert and displays side-by-side comparison.", style_table_cell)],
        [Paragraph("Out-of-Scope / Missing Fact", style_table_cell_bold), Paragraph("Zero Relevant Chunks", style_table_cell), Paragraph("Returns explicit 'Insufficient Evidence in Document' disclosure. Rejects generative guessing or hallucinated speculation.", style_table_cell)],
    ]
    t_pol = Table(policy_matrix_data, colWidths=[115, 110, 298])
    t_pol.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_pol)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 5: FUNCTIONAL & NON-FUNCTIONAL REQUIREMENTS
    # =========================================================================
    story.append(Paragraph("6. Functional Requirements", style_h1))
    story.append(Paragraph(
        "Priorities use MoSCoW: <b>Must Have</b> = required for MVP demo; <b>Should Have</b> = important enterprise feature; <b>Could Have</b> = roadmap integration.",
        style_body
    ))

    fr_data = [
        [Paragraph("ID", style_table_header), Paragraph("Requirement Description", style_table_header), Paragraph("Priority", style_table_header)],
        [Paragraph("FR01", style_table_cell_center), Paragraph("Multi-format document ingestion (PDF, DOCX, TXT) with SHA-256 deduplication and validation.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR02", style_table_cell_center), Paragraph("Automated and manual metadata capture: version number, effective date, status, category, and group ID.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR03", style_table_cell_center), Paragraph("Page-aware semantic chunking preserving exact document page numbers and chunk character offsets.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR04", style_table_cell_center), Paragraph("Persistent vector store indexing with metadata filtering (version ID, active/superseded status).", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR05", style_table_cell_center), Paragraph("Document revision lineage tree construction linking versions (v1.0 ➔ v2.0 ➔ v3.0) with parent IDs.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR06", style_table_cell_center), Paragraph("Strict active-version enforcement for general policy queries, rejecting all superseded chunks.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR07", style_table_cell_center), Paragraph("Explicit historical version query retrieval with temporal provenance labeling and warning banner.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR08", style_table_cell_center), Paragraph("Conflicting active revision detection engine alerting admins to contradictory policies in same category.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR09", style_table_cell_center), Paragraph("Grounded answer generation producing verifiable responses with verbatim quotes and page citations.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR10", style_table_cell_center), Paragraph("Honest missing evidence reporting (zero-hallucination guardrail) when query facts are not in documents.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR11", style_table_cell_center), Paragraph("Interactive web dashboard featuring Document Library, Version Lineage View, and AI Chat Drawer.", style_table_cell), Paragraph("Must Have", style_table_cell_priority)],
        [Paragraph("FR12", style_table_cell_center), Paragraph("Visual document diffing showing clause additions, modifications, and deletions between revisions.", style_table_cell), Paragraph("Should Have", style_table_cell_priority)],
        [Paragraph("FR13", style_table_cell_center), Paragraph("Tamper-evident audit logging recording query text, retrieved chunks, version IDs, and response timestamps.", style_table_cell), Paragraph("Should Have", style_table_cell_priority)],
        [Paragraph("FR14", style_table_cell_center), Paragraph("Enterprise connectors for automated sync from SharePoint, Google Drive, and Confluence repositories.", style_table_cell), Paragraph("Could Have", style_table_cell_priority)],
    ]
    t_fr = Table(fr_data, colWidths=[38, 417, 68])
    t_fr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.9),
        ('BACKGROUND', (2,1), (2,11), PRIORITY_MUST),
        ('BACKGROUND', (2,12), (2,13), PRIORITY_SHOULD),
        ('BACKGROUND', (2,14), (2,14), PRIORITY_COULD),
        ('ROWBACKGROUNDS', (0,1), (1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_fr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("7. Non-Functional Requirements", style_h1))
    nfr_data = [
        [Paragraph("Category", style_table_header), Paragraph("Requirement", style_table_header), Paragraph("Target / Measure", style_table_header)],
        [Paragraph("Performance", style_table_cell_bold), Paragraph("Query-to-answer latency for extractive and local LLM inference.", style_table_cell), Paragraph("Latency < 2.5s (Extractive); < 5s (Local LLM)", style_table_cell)],
        [Paragraph("Response time", style_table_cell_bold), Paragraph("Document library filtering, version tree view, and search lookup.", style_table_cell), Paragraph("Dashboard UI response under 300 ms", style_table_cell)],
        [Paragraph("Security and privacy", style_table_cell_bold), Paragraph("100% offline air-gapped capability; sanitized filenames; role-based access.", style_table_cell), Paragraph("Zero external cloud API leakage; SHA-256 hashes", style_table_cell)],
        [Paragraph("Scalability", style_table_cell_bold), Paragraph("Stateless API services capable of handling thousands of document revisions.", style_table_cell), Paragraph("100,000+ vector chunks; 1,000+ revisions per group", style_table_cell)],
        [Paragraph("Availability", style_table_cell_bold), Paragraph("Engine operates reliably with automatic fallback from PostgreSQL to SQLite.", style_table_cell), Paragraph("99.9% uptime target; zero data corruption", style_table_cell)],
        [Paragraph("Usability", style_table_cell_bold), Paragraph("Intuitive web interface requiring zero prompt engineering; clear version badges.", style_table_cell), Paragraph("New user executes successful query in < 30 seconds", style_table_cell)],
        [Paragraph("Reliability", style_table_cell_bold), Paragraph("Deterministic extractive fallback guaranteeing answers even if local LLM is offline.", style_table_cell), Paragraph("Zero lost audit queries; graceful degradation", style_table_cell)],
        [Paragraph("Explainability", style_table_cell_bold), Paragraph("Every synthesized statement links directly to document version and source page.", style_table_cell), Paragraph("100% of facts traceable to verifiable excerpts", style_table_cell)],
    ]
    t_nfr = Table(nfr_data, colWidths=[110, 245, 168])
    t_nfr.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_nfr)
    story.append(Spacer(1, 4))

    story.append(Paragraph("8. Technology Requirements", style_h1))
    story.append(Paragraph(
        "Technology selection is strictly governed by the problem requirements: zero data leakage, deterministic version control, and verifiable page citations. Full architectural mapping is detailed in Section 8 on the following page.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 6: TECH STACK, COMPETITOR ANALYSIS, INNOVATION, MVP DEF
    # =========================================================================
    story.append(Paragraph("8. Technology Requirements (Stack Architecture)", style_h1))

    tech_stack_data = [
        [Paragraph("Layer", style_table_header), Paragraph("Proposed Technology", style_table_header), Paragraph("Why it fits", style_table_header)],
        [Paragraph("AI / ML Inference", style_table_cell_bold), Paragraph("Ollama (Llama 3.2, Nomic-Embed-Text) + Deterministic Extractive Fallback Engine", style_table_cell), Paragraph("100% offline air-gapped capability, zero external API costs, protects confidential enterprise data.", style_table_cell)],
        [Paragraph("Backend & Orchestrator", style_table_cell_bold), Paragraph("Node.js (Express.js, ES Modules), REST architecture", style_table_cell), Paragraph("High-concurrency asynchronous I/O, lightweight footprint, rapid integration with vector stores.", style_table_cell)],
        [Paragraph("Metadata Database", style_table_cell_bold), Paragraph("PostgreSQL (Production) with SQLite / JSON adapter fallback", style_table_cell), Paragraph("Enforces relational version lineage constraints, temporal indices; zero-friction local fallback.", style_table_cell)],
        [Paragraph("Vector Database", style_table_cell_bold), Paragraph("Local Embedded Vector Store with ChromaDB API compatibility", style_table_cell), Paragraph("Sub-millisecond cosine similarity with rich boolean metadata pre-filtering without daemon overhead.", style_table_cell)],
        [Paragraph("Document Processing", style_table_cell_bold), Paragraph("pdf-parse (page-aware), mammoth (DOCX), native TXT parser", style_table_cell), Paragraph("Preserves page numbers, paragraph geometry, and table structures across enterprise formats.", style_table_cell)],
        [Paragraph("Frontend / Dashboard", style_table_cell_bold), Paragraph("React 18, Vite, Bootstrap 5, Lucide Icons, Emerald Design System", style_table_cell), Paragraph("Modern, responsive UI with real-time citation drawers, version badges, and lineage graphs.", style_table_cell)],
        [Paragraph("Deployment", style_table_cell_bold), Paragraph("Docker containerization, standalone Node runtime, cross-platform", style_table_cell), Paragraph("Reproducible student hackathon demo, zero external cloud dependencies, rapid onboarding.", style_table_cell)],
    ]
    t_tech = Table(tech_stack_data, colWidths=[110, 245, 168])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 4))

    story.append(Paragraph("9. Competitor / Existing Solution Analysis", style_h1))
    comp_data = [
        [Paragraph("Existing Approach", style_table_header), Paragraph("Typical Limitation", style_table_header), Paragraph("Gap This Project Addresses", style_table_header)],
        [Paragraph("Standard Vector DB RAG (LangChain / LlamaIndex)", style_table_cell_bold), Paragraph("Matches on semantic cosine distance alone; ignores document versions; retrieves obsolete clauses.", style_table_cell), Paragraph("Enforces temporal validity pre-filtering; guarantees active-version priority and eliminates stale contamination.", style_table_cell)],
        [Paragraph("Traditional Enterprise Search (Elasticsearch / Solr)", style_table_cell_bold), Paragraph("Relies on exact keyword frequency (BM25); fails on semantic queries; cannot synthesize conversational answers.", style_table_cell), Paragraph("Combines semantic deep understanding with deterministic version lineage graphs and citations.", style_table_cell)],
        [Paragraph("Cloud Document Copilots (Copilot for M365)", style_table_cell_bold), Paragraph("Transmits proprietary data to public clouds; lacks strict version conflict alerts and air-gapped support.", style_table_cell), Paragraph("100% on-premises offline sovereignty with autonomous conflict detection sentinels.", style_table_cell)],
        [Paragraph("Static Document Portals (Confluence / SharePoint)", style_table_cell_bold), Paragraph("Passive repositories requiring manual search, downloading, and manual reading of 100-page PDFs.", style_table_cell), Paragraph("Conversational AI interface delivering instant answers with clickable, verbatim page citations.", style_table_cell)],
        [Paragraph("Manual Document Auditing", style_table_cell_bold), Paragraph("Compliance analysts spend hours manually diffing PDF policies during regulatory audits.", style_table_cell), Paragraph("Automates revision lineage tracking and clause-level provenance verification in seconds.", style_table_cell)],
    ]
    t_comp = Table(comp_data, colWidths=[115, 200, 208])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<i>The goal is not to replace enterprise storage, but to solve the critical enterprise vulnerability: ensuring LLMs retrieve exclusively from legally binding, active document revisions with verifiable evidence.</i>",
        ParagraphStyle('CompNote', parent=styles['Normal'], fontName='Helvetica-Oblique', fontSize=6.8, leading=8.5, textColor=TEXT_MUTED)
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("10. Innovation", style_h1))
    innovations = [
        "<b>Temporal Lineage Graph:</b> Structures enterprise documents into directed revision trees (v1.0 ➔ v2.0 ➔ v3.0), recording parent-child revision linkages, effective dates, and lifecycle status.",
        "<b>Pre-Retrieval Temporal Filtering:</b> Filters vector embeddings by active/superseded status <i>before</i> semantic similarity calculation, fundamentally eliminating superseded clause interference.",
        "<b>Autonomous Conflict Sentinel:</b> Proactively identifies overlapping active documents within the same policy domain, issuing alerts before contradictory guidance is served to employees.",
        "<b>Verifiable Grounded Attribution:</b> Employs strict evidence bounding; answers cite exact document versions, page numbers, and verbatim quotes, backed by honest missing-evidence reporting.",
        "<b>100% Air-Gapped Sovereign AI:</b> Operates completely offline with local Ollama models and embedded vector indexing, ensuring zero cloud exposure of proprietary IP or sensitive compliance data.",
        "<b>Dual-Engine Reliability:</b> Combines local generative LLM inference with a deterministic extractive fallback, ensuring high-availability operation across any hardware environment."
    ]
    for inn in innovations:
        story.append(Paragraph(f"• {inn}", style_body))

    story.append(Spacer(1, 2))
    story.append(Paragraph("11. MVP – Minimum Viable Product", style_h1))
    story.append(Paragraph(
        "The Minimum Viable Product (MVP) implements the complete end-to-end version-aware pipeline demonstrated through realistic enterprise policies (HR Leave Policies and Remote Work Security Policies v1.0, v2.0, and v3.0) within the hackathon timeline.",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 7: MVP DETAILS, SUCCESS METRICS, BUSINESS MODEL
    # =========================================================================
    story.append(Paragraph("11. MVP Definition (Features & Demo)", style_h1))

    mvp_feat_data = [
        [Paragraph("MVP Feature", style_table_header), Paragraph("Requirement IDs", style_table_header), Paragraph("What will be demonstrated in live hackathon", style_table_header)],
        [Paragraph("Multi-Format Ingestion & Metadata", style_table_cell_bold), Paragraph("FR01, FR02, FR03", style_table_cell_center), Paragraph("Upload PDF/TXT policies; system automatically captures version, dates, status, and page chunks.", style_table_cell)],
        [Paragraph("Version Lineage Tree Viewer", style_table_cell_bold), Paragraph("FR04, FR05", style_table_cell_center), Paragraph("Visualizing linked revision trees (v1.0 ➔ v2.0 ➔ v3.0) with active and superseded badges.", style_table_cell)],
        [Paragraph("Active Version Policy Query", style_table_cell_bold), Paragraph("FR06, FR09", style_table_cell_center), Paragraph("Querying current rules retrieves strictly active v3.0 clauses (e.g. 20 leave days; ZTNA timeout 30m).", style_table_cell)],
        [Paragraph("Historical Query with Provenance", style_table_cell_bold), Paragraph("FR07, FR09", style_table_cell_center), Paragraph("Asking 'What was the allowance in v2?' retrieves v2.0 with prominent historical warning banner.", style_table_cell)],
        [Paragraph("Conflicting Active Version Alert", style_table_cell_bold), Paragraph("FR08", style_table_cell_center), Paragraph("Simulating two conflicting active policies triggers an autonomous dashboard conflict warning.", style_table_cell)],
        [Paragraph("Grounded Chat UI with Citations", style_table_cell_bold), Paragraph("FR09, FR10, FR11", style_table_cell_center), Paragraph("Chat interface showing verbatim quotes, confidence ratings, and missing-evidence disclaimers.", style_table_cell)],
    ]
    t_mvp = Table(mvp_feat_data, colWidths=[120, 85, 318])
    t_mvp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_mvp)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "<b>Live Demo Scenario:</b> (1) Admin seeds 3-version Leave Policy dataset (v1.0=15 days, v2.0=18 days, v3.0=20 days). (2) User asks <i>'What is the current annual leave allowance?'</i> ➔ Engine returns <b>20 days</b> citing <b>v3.0, Page 1</b>. (3) Auditor asks <i>'What was the allowance in version 2?'</i> ➔ Engine returns <b>18 days</b> citing <b>v2.0 (Historical)</b>. (4) User asks <i>'Where does it describe maternity leave?'</i> ➔ Engine honestly reports insufficient evidence. (5) Ingesting two simultaneous active files triggers a live Conflict Sentinel banner.",
        style_body
    ))
    story.append(Paragraph(
        "<b>Out of MVP Scope (Later Phases):</b> Enterprise Single Sign-On (SAML/Okta), automated connectors for SharePoint and Google Workspace, OCR for scanned paper documents, and distributed vector cluster sharding.",
        style_body
    ))
    story.append(Spacer(1, 4))

    story.append(Paragraph("12. Success Metrics / KPIs", style_h1))
    kpi_data = [
        [Paragraph("KPI", style_table_header), Paragraph("Illustrative Target", style_table_header), Paragraph("How it will be measured", style_table_header)],
        [Paragraph("Version Retrieval Accuracy", style_table_cell_bold), Paragraph("100% on benchmark suite", style_table_cell), Paragraph("Automated test suite verifying current vs historical queries across 3-version sets.", style_table_cell)],
        [Paragraph("Superseded Clause Contamination", style_table_cell_bold), Paragraph("0% leakage in active queries", style_table_cell), Paragraph("Verification that zero superseded chunks appear in context for standard inquiries.", style_table_cell)],
        [Paragraph("Answer Groundedness", style_table_cell_bold), Paragraph("> 95% citation accuracy", style_table_cell), Paragraph("Factuality benchmark comparing synthesized statements to verbatim source text excerpts.", style_table_cell)],
        [Paragraph("Conflict Detection Accuracy", style_table_cell_bold), Paragraph("100% alert trigger rate", style_table_cell), Paragraph("Trigger rate when two conflicting active documents are indexed in the same category.", style_table_cell)],
        [Paragraph("Query-to-Answer Latency", style_table_cell_bold), Paragraph("< 2.5s (Extractive); < 5s (LLM)", style_table_cell), Paragraph("End-to-end API response timing under benchmark test loads.", style_table_cell)],
        [Paragraph("Air-Gapped Privacy Autonomy", style_table_cell_bold), Paragraph("100% offline execution", style_table_cell), Paragraph("Packet analysis confirming zero outbound internet connections during operation.", style_table_cell)],
        [Paragraph("User Audit Task Efficiency", style_table_cell_bold), Paragraph("> 60% time reduction", style_table_cell), Paragraph("User timing study comparing manual policy verification against RAGNext citations.", style_table_cell)],
    ]
    t_kpi = Table(kpi_data, colWidths=[130, 135, 258])
    t_kpi.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_kpi)
    story.append(Spacer(1, 4))

    story.append(Paragraph("13. Business / Sustainability Model", style_h1))
    biz_data = [
        [Paragraph("Model", style_table_header), Paragraph("Description", style_table_header), Paragraph("Target Market Fit", style_table_header)],
        [Paragraph("Enterprise On-Premises License", style_table_cell_bold), Paragraph("Annual per-node license for air-gapped, high-security enterprise deployments.", style_table_cell), Paragraph("Defense, Banking, Healthcare, Government agencies.", style_table_cell)],
        [Paragraph("Managed Private Cloud SaaS", style_table_cell_bold), Paragraph("Single-tenant hosted private cloud instances with automated backups and maintenance.", style_table_cell), Paragraph("Mid-market enterprises, tech scale-ups, legal firms.", style_table_cell)],
        [Paragraph("Open-Core Developer Tier", style_table_cell_bold), Paragraph("Free open-source local core; paid commercial plugins for enterprise connectors.", style_table_cell), Paragraph("Developer ecosystem, academic research institutions.", style_table_cell)],
        [Paragraph("Compliance Audit Add-on", style_table_cell_bold), Paragraph("Turnkey document version auditing and regulatory policy reconciliation reporting.", style_table_cell), Paragraph("External auditing firms, compliance consultancies.", style_table_cell)],
    ]
    t_biz = Table(biz_data, colWidths=[120, 245, 158])
    t_biz.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_biz)
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "<b>Scaling Plan:</b> <i>Phase 1:</i> Hackathon prototype with automated test suite. <i>Phase 2:</i> University and SMB pilot deployment for student handbooks and IT compliance. (Continued on Page 8)",
        style_body
    ))
    story.append(PageBreak())

    # =========================================================================
    # PAGE 8: SCALING CONTINUATION, RISK ANALYSIS, STAGE 1 TRACEABILITY
    # =========================================================================
    story.append(Paragraph("13. Business / Sustainability Model (Scaling Plan Continued)", style_h1))
    story.append(Paragraph(
        "<b>Scaling Plan (Phases 3 & 4):</b> <i>Phase 3:</i> Multi-tenant cloud and on-premises enterprise editions with automated connectors for Microsoft SharePoint, Google Drive, and Confluence. <i>Phase 4:</i> Industry-specific compliance policy packs (HIPAA, GDPR, ISO 27001, SOC 2) with automated policy conflict reconciliation. The modular micro-service architecture and stateless API design allow each phase to scale without refactoring core retrieval services.",
        style_body
    ))
    story.append(Spacer(1, 3))

    story.append(Paragraph("14. Risk Analysis", style_h1))
    risk_data = [
        [Paragraph("Identified Risk", style_table_header), Paragraph("Impact", style_table_header), Paragraph("Possible Mitigation Strategy", style_table_header)],
        [Paragraph("Ambiguous queries lacking version context", style_table_cell_bold), Paragraph("User receives unexpected revision", style_table_cell), Paragraph("System defaults to Active version, displays explicit '[Active vX.Y]' badge, and offers one-click toggle to historical revisions.", style_table_cell)],
        [Paragraph("Malformed or unversioned document uploads", style_table_cell_bold), Paragraph("Metadata extraction failure", style_table_cell), Paragraph("Heuristic date/version regex parser extracts title hints; UI prompts user for manual metadata confirmation.", style_table_cell)],
        [Paragraph("Conflicting active documents in same group", style_table_cell_bold), Paragraph("Contradictory policy guidance", style_table_cell), Paragraph("Autonomous Conflict Sentinel detects category overlap, blocks single-answer synthesis, and alerts administrator.", style_table_cell)],
        [Paragraph("Local LLM resource exhaustion on low-spec PCs", style_table_cell_bold), Paragraph("Server crash or high latency", style_table_cell), Paragraph("Seamless fallback to deterministic extractive synthesis engine running on CPU with zero GPU requirement.", style_table_cell)],
        [Paragraph("Semantic vector drift across minor revisions", style_table_cell_bold), Paragraph("Chunks from different versions seem identical", style_table_cell), Paragraph("Pre-retrieval temporal hard filtering strictly isolates the vector search space prior to similarity scoring.", style_table_cell)],
        [Paragraph("Proprietary document data leakage", style_table_cell_bold), Paragraph("Confidentiality and compliance violation", style_table_cell), Paragraph("100% offline air-gapped execution; cryptographic filename sanitization and role-based document access controls.", style_table_cell)],
        [Paragraph("Hallucination in generative synthesis", style_table_cell_bold), Paragraph("Inaccurate or misleading policy advice", style_table_cell), Paragraph("Strict prompt grounding boundaries; mandatory verbatim quote citations; honest insufficient-evidence reports.", style_table_cell)],
        [Paragraph("User skepticism toward AI accuracy", style_table_cell_bold), Paragraph("Low organizational adoption", style_table_cell), Paragraph("Verbatim page citations with one-click side-by-side source document inspection to verify every claim.", style_table_cell)],
    ]
    t_risk = Table(risk_data, colWidths=[120, 115, 288])
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_risk)
    story.append(Spacer(1, 4))

    story.append(Paragraph("15. Stage 1 Traceability and Stage 2 Checklist", style_h1))
    story.append(Paragraph("<b>Traceability to the Cyber Knights Stage 1 PPT</b>", style_body_bold_intro))

    trace_data = [
        [Paragraph("Stage 1 PPT Content / Problem Framing", style_table_header), Paragraph("Where it is addressed in this MRD", style_table_header)],
        [Paragraph("Existing problems: Stale document retrieval, superseded clause leakage, hallucinations, regulatory non-compliance.", style_table_cell), Paragraph("Sections 1, 4, 5, 9, 14", style_table_cell_bold)],
        [Paragraph("Proposed solution: Version-aware RAG, temporal graph lineage, grounded page citations, conflicting active detection.", style_table_cell), Paragraph("Sections 5, 6, 10, 11", style_table_cell_bold)],
        [Paragraph("Target users & stakeholders: Enterprise compliance officers, legal auditors, employees, IT directors.", style_table_cell), Paragraph("Sections 2, 3", style_table_cell_bold)],
        [Paragraph("Core impacts: Zero superseded leakage, rapid policy retrieval, audit compliance, air-gapped data sovereignty.", style_table_cell), Paragraph("Sections 1, 12", style_table_cell_bold)],
        [Paragraph("5-Why root cause analysis: Inability of cosine similarity alone to capture temporal document validity and revision lineage.", style_table_cell), Paragraph("Sections 1, 4, 5", style_table_cell_bold)],
        [Paragraph("Architectural blueprint & privacy-first design: Air-gapped local AI (Ollama), PostgreSQL/SQLite, ChromaDB compatibility.", style_table_cell), Paragraph("Cover page, Section 8, Section 11, References", style_table_cell_bold)],
    ]
    t_trace = Table(trace_data, colWidths=[295, 228])
    t_trace.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.6),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.6),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_trace)
    story.append(PageBreak())

    # =========================================================================
    # PAGE 9: DELIVERABLES CHECKLIST & REFERENCES
    # =========================================================================
    story.append(Paragraph("Stage 2 Deliverables Checklist", style_h1))

    deliv_data = [
        [Paragraph("Required MRD Deliverable", style_table_header), Paragraph("Status", style_table_header), Paragraph("Section / Location", style_table_header)],
        [Paragraph("MRD document (about 8-12 pages)", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("This document (9 pages)", style_table_cell_bold)],
        [Paragraph("User personas (Auditor & Employee profiles)", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 3", style_table_cell_bold)],
        [Paragraph("User journey (Current vs Proposed comparison)", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 4", style_table_cell_bold)],
        [Paragraph("Solution architecture & flowchart diagram", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 5 (Figure 1)", style_table_cell_bold)],
        [Paragraph("Feature prioritization (MoSCoW Must / Should / Could)", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 6", style_table_cell_bold)],
        [Paragraph("MVP definition & live hackathon demo scenario", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 11", style_table_cell_bold)],
        [Paragraph("Technology stack & architectural rationale", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 8", style_table_cell_bold)],
        [Paragraph("KPI / impact measurement criteria", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 12", style_table_cell_bold)],
        [Paragraph("Business & scaling plan (Phases 1-4)", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 13", style_table_cell_bold)],
        [Paragraph("Risk analysis & mitigation matrix", style_table_cell), Paragraph("Included", style_table_cell_center), Paragraph("Section 14", style_table_cell_bold)],
        [Paragraph("MRD PPT (about 8-10 slides)", style_table_cell), Paragraph("Separate deliverable", style_table_cell_center), Paragraph("To be prepared from this document", style_table_cell_bold)],
    ]
    t_deliv = Table(deliv_data, colWidths=[240, 100, 183])
    t_deliv.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.6, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT]),
    ]))
    story.append(t_deliv)
    story.append(Spacer(1, 10))

    story.append(Paragraph("References", style_h1))
    references = [
        "<b>Lewis, P., et al. (2020).</b> 'Retrieval-Augmented Generation for Knowledge-Intensive NLP Tasks.' <i>Advances in Neural Information Processing Systems (NeurIPS 2020)</i>. Available: https://arxiv.org/abs/2005.11401",
        "<b>NIST Special Publication 800-53 Rev. 5.</b> 'Security and Privacy Controls for Information Systems and Organizations.' Controls SI-12 (Information Handling and Retention) & AU-10 (Non-repudiation). National Institute of Standards and Technology. https://csrc.nist.gov/pubs/sp/800/53/r5/upd1/final",
        "<b>ISO/IEC 27001:2022.</b> 'Information Security, Cybersecurity and Privacy Protection — Information Security Management Systems.' Clause A.5.37: Documented Information. International Organization for Standardization. https://www.iso.org/standard/27001",
        "<b>CISA Zero Trust Maturity Model Version 2.0 (2023).</b> Cybersecurity and Infrastructure Security Agency. Data Pillar: Data Lineage, Governance, and Protection. https://www.cisa.gov/zero-trust-maturity-model",
        "<b>NIST Special Publication 800-207.</b> 'Zero Trust Architecture.' Tenet 4: Dynamic Resource Access Decisions. https://csrc.nist.gov/pubs/sp/800/207/final",
        "<b>Chroma & Vector Database Standards.</b> 'Filtering and Querying Hybrid Vector Stores with Pre-retrieval Metadata Constraints.' Chroma Technical Documentation (2024). https://docs.trychroma.com",
        "<b>Meta AI & Ollama Community (2024).</b> 'Llama 3.2: Lightweight Multimodal and Instruction-Tuned Local Models for Edge and Air-Gapped Deployments.' https://ollama.com/library/llama3.2",
        "<b>Vaswani, A., et al. (2017).</b> 'Attention Is All You Need.' <i>Advances in Neural Information Processing Systems (NeurIPS 2017)</i>. https://arxiv.org/abs/1706.03762"
    ]
    for ref in references:
        story.append(Paragraph(f"• {ref}", ParagraphStyle('RefText', parent=styles['Normal'], fontName='Helvetica', fontSize=7.2, leading=9.8, textColor=TEXT_DARK, spaceAfter=4.5)))

    # Build PDF with NumberedCanvas
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_mrd_pdf()
