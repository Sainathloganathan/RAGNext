import os
import sys
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak
)
from reportlab.pdfgen import canvas

# Palette Constants
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
        # Page 1: Top decorative accent
        if self._pageNumber == 1:
            self.saveState()
            self.setFillColor(colors.HexColor("#1E40AF"))
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
            self.drawString(32, 826, "MRD | RAGNext — Autonomous Version-Aware Document Intelligence Engine")
            self.drawRightString(595.27 - 32, 826, "Team Cyber Knights (SH-SVA-04)")

            # Running Footer
            self.setStrokeColor(BORDER_COLOR)
            self.setLineWidth(0.5)
            self.line(32, 28, 595.27 - 32, 28)
            self.setFillColor(TEXT_MUTED)
            self.setFont("Helvetica", 7.5)
            self.drawString(32, 18, "Market Requirements Document (MRD) — Stage 2 Evaluation")
            self.drawRightString(595.27 - 32, 18, f"Page {self._pageNumber} of {total_pages}")
            self.restoreState()

def create_mrd_pdf(output_path="RAGNext_Stage2_MRD_Cyber_Knights.pdf"):
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
        textColor=NAVY_HEADER,
        alignment=1,
        spaceAfter=2
    )

    style_sub = ParagraphStyle(
        'CoverSub',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=11,
        textColor=GREEN_ACCENT,
        alignment=1,
        spaceAfter=7
    )

    style_h1 = ParagraphStyle(
        'Heading1Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9.5,
        leading=11.5,
        textColor=NAVY_HEADER,
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
    # PAGE 1: STRATEGIC PROBLEM, TARGET MARKET & EXECUTIVE SUMMARY
    # =========================================================================
    story.append(Spacer(1, 14))
    story.append(Paragraph("MARKET REQUIREMENTS DOCUMENT (MRD)", style_title))
    story.append(Paragraph("RAGNext: Autonomous Version-Aware Document Intelligence Engine with Verifiable Grounding", style_sub))

    meta_data = [
        [Paragraph("Problem Statement ID", style_td_bold), Paragraph("SH-SVA-04 (Smart Virtual Assistant for Version-Aware Search)", style_td),
         Paragraph("Team Name", style_td_bold), Paragraph("Cyber Knights (Sainath Loganathan, Tahir Azeem)", style_td)],
        [Paragraph("Target Market", style_td_bold), Paragraph("Regulated Enterprises (BFSI, Healthcare, Defense, SMBs)", style_td),
         Paragraph("Core Architecture", style_td_bold), Paragraph("Temporal Lineage Graph + Pre-Retrieval Filtering + Air-Gapped Local LLM", style_td)]
    ]
    t_meta = Table(meta_data, colWidths=[95, 170, 75, 191])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), BG_LIGHT),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.8),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.8),
    ]))
    story.append(t_meta)
    story.append(Spacer(1, 3))

    story.append(Paragraph("1. Executive Summary & Problem Framing (The Core Market Pain)", style_h1))
    story.append(Paragraph(
        "Modern enterprises operate on hundreds of evolving standard operating procedures, compliance manuals, and security guidelines. Conventional vector search engines (RAG) treat documents as flat text chunks and retrieve information based purely on semantic cosine distance. When an organization updates a policy (e.g., <b>Leave Policy: v1.0 [15 days] ➔ v2.0 [18 days] ➔ v3.0 [20 days]</b>), outdated clauses frequently score higher similarity than active ones due to exact keyword density. Standard AI systems blindly hallucinate answers from superseded documents. In heavily regulated industries (banking, healthcare, legal, defense), acting on obsolete policies leads to regulatory fines, severe audit failures, and operational disputes.",
        style_body
    ))
    story.append(Paragraph(
        "<b>The RAGNext Solution:</b> RAGNext is an autonomous, version-aware enterprise intelligence engine that structures documents into <b>Temporal Revision Lineage Graphs</b>, enforces <b>Pre-Retrieval Policy State Filtering</b> (ACTIVE, SUPERSEDED, DRAFT), autonomously detects <b>Conflicting Active Policies</b>, and guarantees <b>100% Offline Air-Gapped Data Privacy</b> with verifiable page citations.",
        style_body
    ))
    story.append(Spacer(1, 2))

    story.append(Paragraph("2. Target Market & User Segments", style_h1))
    target_data = [
        [Paragraph("Market Segment", style_th), Paragraph("Key Stakeholder", style_th), Paragraph("Core Need & Pain Addressed", style_th), Paragraph("Market Fit / Compliance Standard", style_th)],
        [Paragraph("Regulated BFSI & Defense", style_td_bold), Paragraph("Compliance Officers / CISOs", style_td), Paragraph("Cannot risk citing deprecated policies; zero data leakage to cloud APIs.", style_td), Paragraph("ISO 27001 (A.5.37), NIST SP 800-53 (AU-10), CISA Zero Trust", style_td)],
        [Paragraph("Healthcare & Pharma", style_td_bold), Paragraph("Clinical SOP Auditors", style_td), Paragraph("Must ensure clinical protocols in use reflect latest active drug/safety revisions.", style_td), Paragraph("HIPAA Privacy Rule, GxP Document Lineage", style_td)],
        [Paragraph("Enterprise HR & Operations", style_td_bold), Paragraph("Employees / HR Leads", style_td), Paragraph("Resolves benefit/leave disputes; guarantees employees always see active rules.", style_td), Paragraph("Internal Corporate Governance & Employee Trust", style_td)],
        [Paragraph("Legal & Internal Audit", style_td_bold), Paragraph("Regulatory Auditors", style_td), Paragraph("Requires bi-directional search: query historical rules (in v1.0) with verifiable citations.", style_td), Paragraph("Statutory Audit Defense & Dispute Reconciliation", style_td)]
    ]
    t_target = Table(target_data, colWidths=[90, 85, 205, 151])
    t_target.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_target)
    story.append(Spacer(1, 3))

    story.append(Paragraph("3. Core Value Proposition & Business Impact", style_h1))
    impact_data = [
        [Paragraph("Metric / Value Pillar", style_th), Paragraph("Conventional RAG Baseline", style_th), Paragraph("RAGNext Expected Impact", style_th)],
        [Paragraph("Outdated Policy Leakage", style_td_bold), Paragraph("35% - 48% citation of superseded chunks", style_td), Paragraph("<b>0% Leakage:</b> Hard pre-retrieval filtering eliminates inactive chunks.", style_td)],
        [Paragraph("Audit Turnaround Time", style_td_bold), Paragraph("4 - 8 hours manual PDF diffing per audit inquiry", style_td), Paragraph("<b>60% Reduction:</b> Instant temporal provenance and clause citations.", style_td)],
        [Paragraph("Cloud Data Sovereignty", style_td_bold), Paragraph("High risk: Uploads confidential IP to third-party clouds", style_td), Paragraph("<b>100% Air-Gapped:</b> Local Ollama LLM + embedded local vector store.", style_td)],
        [Paragraph("Factual Groundedness", style_td_bold), Paragraph("Unverified generative text with frequent hallucinations", style_td), Paragraph("<b>> 95% Grounded:</b> Verbatim excerpts with exact document & page numbers.", style_td)]
    ]
    t_impact = Table(impact_data, colWidths=[110, 190, 231])
    t_impact.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_impact)

    # END OF PAGE 1
    story.append(PageBreak())

    # =========================================================================
    # PAGE 2: PERSONAS, USER JOURNEY & VERSION POLICY MATRIX
    # =========================================================================
    story.append(Paragraph("4. User Personas (Representative Profiles)", style_h1))
    persona_data = [
        [Paragraph("Persona Profile", style_th), Paragraph("Operational Goals & Responsibilities", style_th), Paragraph("Current Pain Point in Unversioned Search", style_th), Paragraph("RAGNext Solution Feature", style_th)],
        [Paragraph("<b>Rajesh</b><br/>Compliance & Risk Lead", style_td), Paragraph("Ensure policy compliance, audit historical incident records, eliminate legal exposure.", style_td), Paragraph("Search engines mix old and new PDF clauses; manual revision cross-checks take days.", style_td), Paragraph("Historical Query Intent, Conflict Alert Sentinel, and downloadable audit logs.", style_td)],
        [Paragraph("<b>Priya</b><br/>Knowledge Worker / Employee", style_td), Paragraph("Get quick, authoritative answers to day-to-day policy questions (leave, VPN, benefits).", style_td), Paragraph("Searches return deprecated 2021 guidelines; risks disciplinary/policy violations.", style_td), Paragraph("Default Active Pre-Filtering with visible `[Active v3.0, Page 1]` citation badges.", style_td)],
        [Paragraph("<b>Dev</b><br/>IT & Security Administrator", style_td), Paragraph("Deploy secure, private document search; maintain 100% uptime without high API costs.", style_td), Paragraph("Cloud AI APIs leak proprietary policies and incur unpredictable token billing.", style_td), Paragraph("100% offline air-gapped architecture with local Ollama and zero cloud fees.", style_td)]
    ]
    t_persona = Table(persona_data, colWidths=[80, 140, 155, 156])
    t_persona.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.2),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.2),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_persona)
    story.append(Spacer(1, 3))

    story.append(Paragraph("5. User Journey Comparison: Conventional RAG vs. RAGNext", style_h1))
    journey_data = [
        [Paragraph("Workflow Stage", style_th), Paragraph("Conventional RAG Journey (Systemic Flaw)", style_th), Paragraph("RAGNext Version-Aware Journey (Engineered Fix)", style_th)],
        [Paragraph("1. Ingestion & Storage", style_td_bold), Paragraph("Dumps all PDF versions into a flat vector index. Version dates and parent linkages are discarded.", style_td), Paragraph("Extracts SemVer, dates, and builds a directed <b>Revision Lineage Tree</b> (v1.0 ➔ v2.0 ➔ v3.0).", style_td)],
        [Paragraph("2. Chunking & Indexing", style_td_bold), Paragraph("Splits text into arbitrary token chunks without preserving page coordinates or status flags.", style_td), Paragraph("<b>Page-Aware Chunker</b> retains exact page numbers, character offsets, and lifecycle status.", style_td)],
        [Paragraph("3. Policy Query Execution", style_td_bold), Paragraph("Performs blind cosine similarity. Old v1.0 clause matches keywords and outranks active v3.0.", style_td), Paragraph("<b>Pre-Retrieval Filter</b> isolates search strictly to `status = 'ACTIVE'` chunks. v1.0 is excluded.", style_td)],
        [Paragraph("4. Historical Inquiries", style_td_bold), Paragraph("Cannot filter by past dates; mixes clauses from different years into a fabricated answer.", style_td), Paragraph("Detects historical intent (e.g. 'in v1.0') and retrieves requested version with warning banner.", style_td)],
        [Paragraph("5. Conflicting Active Rules", style_td_bold), Paragraph("Silently blends conflicting policies together into a nonsensical synthesis.", style_td), Paragraph("<b>Conflict Sentinel</b> flags an active contradiction alert and halts automated guessing.", style_td)],
        [Paragraph("6. Answer Grounding", style_td_bold), Paragraph("Black-box AI response without traceable evidence or page verification.", style_td), Paragraph("Structured output with verbatim quotes, confidence ratings, and exact page citations.", style_td)]
    ]
    t_journey = Table(journey_data, colWidths=[85, 220, 226])
    t_journey.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_journey)
    story.append(Spacer(1, 3))

    story.append(Paragraph("6. Proposed Version-to-Action Policy Matrix", style_h1))
    policy_data = [
        [Paragraph("Query Intent / Trigger", style_th), Paragraph("Target Retrieval Scope", style_th), Paragraph("System Action & Output Behavior", style_th)],
        [Paragraph("General Policy Query", style_td_bold), Paragraph("Active Version (Latest)", style_td), Paragraph("Hard filter `status = 'ACTIVE'`. Ignores superseded chunks. Cites active version with page proof.", style_td)],
        [Paragraph("Historical Query ('in v1.0')", style_td_bold), Paragraph("Target Historical Revision", style_td), Paragraph("Retrieves target historical version; attaches prominent `⚠️ [Historical Record — Superseded]` warning.", style_td)],
        [Paragraph("Conflicting Active Policies", style_td_bold), Paragraph("Multiple Active Documents", style_td), Paragraph("Suspends single answer. Dispatches administrative `Conflict Warning` and displays side-by-side diff.", style_td)],
        [Paragraph("Out-of-Scope / Missing Fact", style_td_bold), Paragraph("Zero Relevant Chunks", style_td), Paragraph("Zero-hallucination guardrail: Returns explicit `Insufficient Evidence in Active Documents` report.", style_td)]
    ]
    t_policy = Table(policy_data, colWidths=[100, 105, 326])
    t_policy.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_policy)

    # END OF PAGE 2
    story.append(PageBreak())

    # =========================================================================
    # PAGE 3: REQUIREMENTS, TECH STACK, COMPETITORS & MVP ROADMAP
    # =========================================================================
    story.append(Paragraph("7. Requirements Matrix (MoSCoW Priorities & NFRs)", style_h1))
    req_data = [
        [Paragraph("ID", style_th), Paragraph("Pri.", style_th), Paragraph("Functional Requirement Description", style_th), Paragraph("Target Acceptance Metric", style_th)],
        [Paragraph("FR01-03", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Multi-format ingestion (PDF, DOCX, TXT), SemVer parsing, and page-aware chunking.", style_td), Paragraph("Preserves exact page numbers and SHA-256 hashes.", style_td)],
        [Paragraph("FR04-06", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Lineage tree construction, vector indexing, and hard pre-retrieval active filtering.", style_td), Paragraph("100% exclusion of superseded chunks on general queries.", style_td)],
        [Paragraph("FR07-09", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Historical query intent routing, conflict sentinel alerts, and grounded page citations.", style_td), Paragraph("Verbatim quote + page citation on every response.", style_td)],
        [Paragraph("FR10-12", style_td_center), Paragraph("MUST", style_td_bold), Paragraph("Honest missing evidence reporting, web dashboard with drawer, and 1-click seed dataset.", style_td), Paragraph("0% hallucinations on out-of-scope questions.", style_td)],
        [Paragraph("NFR01-04", style_td_center), Paragraph("NFR", style_td_bold), Paragraph("Air-gapped execution, latency <2.5s extractive / <5s LLM, dual-mode DB/AI fallback.", style_td), Paragraph("Zero outbound network telemetry; zero crash fallback.", style_td)]
    ]
    t_req = Table(req_data, colWidths=[40, 30, 290, 171])
    t_req.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_req)
    story.append(Spacer(1, 3))

    story.append(Paragraph("8. Architectural Stack & Competitor Comparison", style_h1))
    comp_data = [
        [Paragraph("Solution Architecture", style_th), Paragraph("Version Lineage", style_th), Paragraph("Pre-Filter", style_th), Paragraph("Conflict Sentinel", style_th), Paragraph("Data Sovereignty", style_th), Paragraph("Verifiable Citations", style_th)],
        [Paragraph("Standard RAG (LangChain/Pinecone)", style_td_bold), Paragraph("None (flat chunks)", style_td), Paragraph("No (cosine only)", style_td), Paragraph("None (silent blend)", style_td), Paragraph("Public Cloud API", style_td), Paragraph("Vague / Untraced", style_td)],
        [Paragraph("Enterprise Search (Elasticsearch)", style_td_bold), Paragraph("None (keyword BM25)", style_td), Paragraph("Date filters only", style_td), Paragraph("None", style_td), Paragraph("On-Premises", style_td), Paragraph("Snippets only", style_td)],
        [Paragraph("M365 Copilot / Cloud LLMs", style_td_bold), Paragraph("Basic file timestamps", style_td), Paragraph("Weak prompt filter", style_td), Paragraph("None", style_td), Paragraph("Public Cloud API", style_td), Paragraph("Document title only", style_td)],
        [Paragraph("<b>RAGNext (Cyber Knights)</b>", style_td_bold), Paragraph("<b>Directed Tree Graph</b>", style_td), Paragraph("<b>Hard Pre-Filter</b>", style_td), Paragraph("<b>Autonomous Alert</b>", style_td), Paragraph("<b>100% Air-Gapped</b>", style_td), Paragraph("<b>Page + Quote Proof</b>", style_td)]
    ]
    t_comp = Table(comp_data, colWidths=[110, 80, 80, 80, 85, 96])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), GREEN_DARK),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.9),
        ('ROWBACKGROUNDS', (0,1), (-1,-2), [WHITE, BG_LIGHT]),
        ('BACKGROUND', (0,-1), (-1,-1), BG_ACCENT)
    ]))
    story.append(t_comp)
    story.append(Spacer(1, 3))

    story.append(Paragraph("9. MVP Live Hackathon Demonstration Workflow & Key KPIs", style_h1))
    mvp_data = [
        [Paragraph("Demo Step", style_th), Paragraph("Action Performed in UI", style_th), Paragraph("Expected System Output & Evaluation Criteria", style_th)],
        [Paragraph("1. Seed Dataset", style_td_bold), Paragraph("Click 'Seed Demo Dataset' on Dashboard.", style_td), Paragraph("Loads 3-version Leave Policy (v1.0=15d, v2.0=18d, v3.0=20d) and Remote Work Security Policy.", style_td)],
        [Paragraph("2. Lineage Inspection", style_td_bold), Paragraph("Open Document Library ➔ Click 'Versions'.", style_td), Paragraph("Displays interactive version tree showing v3.0 [Active] and v1.0/v2.0 [Superseded].", style_td)],
        [Paragraph("3. Current Query", style_td_bold), Paragraph("Ask: 'What is the current annual leave allowance?'", style_td), Paragraph("Answers <b>20 days</b> citing <b>v3.0, Page 1</b>. Outdated 15/18 day clauses strictly suppressed.", style_td)],
        [Paragraph("4. Historical Query", style_td_bold), Paragraph("Ask: 'What was the allowance in version 2?'", style_td), Paragraph("Answers <b>18 days</b> citing <b>v2.0 (Historical)</b> with prominent warning banner.", style_td)],
        [Paragraph("5. Missing Evidence", style_td_bold), Paragraph("Ask: 'Where is maternity leave explained?'", style_td), Paragraph("Honest guardrail: Reports insufficient evidence rather than hallucinating rules.", style_td)],
        [Paragraph("6. Conflict Sentinel", style_td_bold), Paragraph("Simulate two active documents in same group.", style_td), Paragraph("Dashboard triggers live Conflict Alert warning user before contradictory answers are served.", style_td)]
    ]
    t_mvp = Table(mvp_data, colWidths=[70, 160, 301])
    t_mvp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), HEADER_BLUE),
        ('BOX', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('INNERGRID', (0,0), (-1,-1), 0.4, BORDER_COLOR),
        ('TOPPADDING', (0,0), (-1,-1), 1.9),
        ('BOTTOMPADDING', (0,0), (-1,-1), 1.9),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [WHITE, BG_LIGHT])
    ]))
    story.append(t_mvp)
    story.append(Spacer(1, 3))

    story.append(Paragraph("10. Business Model, Sustainability & Compliance Alignment", style_h1))
    story.append(Paragraph(
        "<b>Monetization & Sustainability:</b> (1) <i>Enterprise On-Premises License:</i> Annual per-node fee for air-gapped banking, healthcare, and defense deployments. (2) <i>Managed Private Cloud SaaS:</i> Single-tenant hosted instances for mid-market legal and tech firms. (3) <i>Turnkey Compliance Add-on:</i> Automated policy revision diffing and regulatory audit export reports. (4) <i>Open-Core Ecosystem:</i> Free developer core with commercial enterprise connectors (SharePoint, Google Drive).<br/>"
        "<b>Regulatory Compliance Alignment:</b> Aligned with <b>NIST SP 800-53 Rev. 5</b> (Controls SI-12 Information Handling & AU-10 Audit Provenance), <b>ISO/IEC 27001:2022</b> (Control A.5.37 Documented Information Governance), and <b>CISA Zero Trust Data Pillar</b> requirements for continuous data lineage, policy integrity, and air-gapped protection.",
        style_body
    ))

    # Build PDF
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated {output_path}")

if __name__ == "__main__":
    create_mrd_pdf()
