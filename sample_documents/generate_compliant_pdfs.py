import os
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def create_policy_pdf(title, version_tag, sections, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    doc = SimpleDocTemplate(
        output_path,
        pagesize=letter,
        rightMargin=54,
        leftMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontName='Helvetica-Bold',
        fontSize=18,
        leading=22,
        textColor=colors.HexColor('#0F172A'),
        spaceAfter=6
    )
    
    subtitle_style = ParagraphStyle(
        'DocSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=colors.HexColor('#059669'),
        spaceAfter=12
    )
    
    h2_style = ParagraphStyle(
        'SectionHeading',
        parent=styles['Heading2'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=colors.HexColor('#1E293B'),
        spaceBefore=10,
        spaceAfter=4
    )
    
    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#334155'),
        spaceAfter=4
    )
    
    story = []
    
    # Header
    story.append(Paragraph(title, title_style))
    story.append(Paragraph(version_tag, subtitle_style))
    story.append(HRFlowable(width="100%", thickness=1, color=colors.HexColor('#E2E8F0'), spaceAfter=14))
    
    for sec_title, sec_paragraphs in sections:
        story.append(Paragraph(sec_title, h2_style))
        for p_text in sec_paragraphs:
            story.append(Paragraph(p_text, body_style))
        story.append(Spacer(1, 6))
        
    doc.build(story)
    print(f"Generated compliant PDF at: {output_path}")

DOC1_SECTIONS = [
    ("SECTION 1: REMOTE NETWORK ACCESS", [
        "1.1 All remote employees must connect to corporate infrastructure via Cisco AnyConnect VPN.",
        "1.2 VPN session idle timeout is set to 8 continuous hours. Split-tunneling is enabled by default for non-corporate internet traffic."
    ]),
    ("SECTION 2: PASSWORD AND AUTHENTICATION STANDARDS", [
        "2.1 Passwords must be at least 8 characters in length, containing at least one numeral and one special character.",
        "2.2 Mandatory password rotation is enforced every 90 days across all accounts.",
        "2.3 Two-Factor Authentication (2FA) is recommended but optional for standard user accounts."
    ]),
    ("SECTION 3: HARDWARE AND DEVICE MANAGEMENT (BYOD)", [
        "3.1 Bring Your Own Device (BYOD) is permitted: Personal Windows or macOS laptops may be used for remote work, provided employees register their device MAC address with corporate IT.",
        "3.2 Antivirus software of the employee's choice must be active and updated on personal devices."
    ]),
    ("SECTION 4: DATA TRANSFER AND STORAGE", [
        "4.1 Offline data backup to encrypted USB flash drives is permitted for business continuity.",
        "4.2 File transfers over standard email attachments are allowed up to 25 MB per message."
    ])
]

DOC2_SECTIONS = [
    ("SECTION 1: REMOTE NETWORK ACCESS", [
        "1.1 Cisco AnyConnect has been retired. All remote access must route through Cloudflare Zero Trust / WireGuard gateway.",
        "1.2 Maximum idle session timeout is reduced to 2 continuous hours. Split-tunneling is strictly disabled."
    ]),
    ("SECTION 2: PASSWORD AND AUTHENTICATION STANDARDS", [
        "2.1 Passwords must be at least 12 characters in length.",
        "2.2 Password rotation interval is set to 180 days.",
        "2.3 Multi-Factor Authentication (MFA) is mandatory for all users via SMS OTP or Microsoft Authenticator app."
    ]),
    ("SECTION 3: HARDWARE AND DEVICE MANAGEMENT", [
        "3.1 BYOD personal laptops are strictly prohibited for engineering, finance, and production database access.",
        "3.2 Employees must use company-issued Lenovo ThinkPads with BitLocker encryption and Defender antivirus."
    ]),
    ("SECTION 4: DATA TRANSFER AND STORAGE", [
        "4.1 External USB mass storage devices and removable flash drives are blocked at the operating system level.",
        "4.2 Cloud storage is restricted to corporate Microsoft OneDrive with Data Loss Prevention (DLP) tagging."
    ])
]

DOC3_SECTIONS = [
    ("SECTION 1: REMOTE NETWORK ACCESS", [
        "1.1 All remote connections require Zero Trust Network Access (ZTNA) with continuous device posture checks.",
        "1.2 Maximum idle session timeout is 30 minutes. Re-authentication is enforced at every connection resumption."
    ]),
    ("SECTION 2: PASSWORD AND AUTHENTICATION STANDARDS", [
        "2.1 Traditional passwords are deprecated in favor of FIDO2 WebAuthn hardware keys (YubiKey 5 Series).",
        "2.2 For fallback systems requiring passphrases, minimum length is 16 characters with no periodic rotation required.",
        "2.3 SMS-based 2FA is strictly banned due to SIM-swapping and interception vulnerabilities. Only FIDO2 hardware keys or push verification are allowed."
    ]),
    ("SECTION 3: HARDWARE AND DEVICE MANAGEMENT", [
        "3.1 BYOD personal devices are 100% prohibited across all departments without exception.",
        "3.2 Only company hardware with CrowdStrike Falcon EDR, TPM 2.0, and remote wipe capabilities may access company assets."
    ]),
    ("SECTION 4: DATA TRANSFER AND ARTIFICIAL INTELLIGENCE USAGE", [
        "4.1 USB storage ports remain permanently disabled at the hardware BIOS level.",
        "4.2 Corporate AI Policy: Employees may only use internal offline document intelligence systems (such as RAGNext with local Ollama inference). Uploading internal company code, documents, or customer PII to public cloud AI tools (ChatGPT, Claude) is classified as a Critical Security Violation."
    ])
]

if __name__ == "__main__":
    base_dir = r"E:\project\RAGNext\RAGNext"
    sample_dir = os.path.join(base_dir, "sample_documents")
    downloads_dir = os.path.join(base_dir, "frontend", "public", "downloads")
    
    for target in [sample_dir, downloads_dir]:
        create_policy_pdf(
            "CYBER KNIGHTS ENTERPRISE CORP - INFOSEC POLICY",
            "VERSION 1.0 (SUPERSEDED) | EFFECTIVE: JAN 1, 2022 | EXPIRES: DEC 31, 2023",
            DOC1_SECTIONS,
            os.path.join(target, "Remote_Work_Security_Policy_v1.0.pdf")
        )
        create_policy_pdf(
            "CYBER KNIGHTS ENTERPRISE CORP - INFOSEC POLICY",
            "VERSION 2.0 (SUPERSEDED) | EFFECTIVE: JAN 1, 2024 | EXPIRES: DEC 31, 2024",
            DOC2_SECTIONS,
            os.path.join(target, "Remote_Work_Security_Policy_v2.0.pdf")
        )
        create_policy_pdf(
            "CYBER KNIGHTS ENTERPRISE CORP - INFOSEC POLICY",
            "VERSION 3.0 (ACTIVE) | EFFECTIVE: JAN 1, 2025 | EXPIRES: ACTIVE / INDEFINITE",
            DOC3_SECTIONS,
            os.path.join(target, "Remote_Work_Security_Policy_v3.0.pdf")
        )
