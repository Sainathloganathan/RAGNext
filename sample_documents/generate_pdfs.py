import os

def text_to_pdf(title, subtitle, sections, output_path):
    """
    Generates a clean PDF 1.4 document without external dependencies.
    """
    lines = []
    lines.append(f"%PDF-1.4")
    
    # We will build pages.
    # Page size: 612 x 792 (Standard Letter: 8.5 x 11 inches)
    margin_x = 54
    top_y = 738
    bottom_y = 54
    line_height = 14
    
    # Format stream commands
    content_lines = []
    content_lines.append("BT")
    
    # Document Header
    content_lines.append(f"/F2 16 Tf")
    content_lines.append(f"{margin_x} {top_y} Td")
    content_lines.append(f"({escape_pdf(title)}) Tj")
    
    curr_y = top_y - 22
    content_lines.append(f"0 -22 Td")
    content_lines.append(f"/F1 10 Tf")
    content_lines.append(f"({escape_pdf(subtitle)}) Tj")
    
    curr_y -= 25
    content_lines.append(f"0 -25 Td")
    
    for sec_title, sec_body in sections:
        # Check if we need space
        content_lines.append(f"/F2 12 Tf")
        content_lines.append(f"({escape_pdf(sec_title)}) Tj")
        content_lines.append(f"0 -18 Td")
        curr_y -= 18
        
        content_lines.append(f"/F1 10 Tf")
        for bline in sec_body:
            content_lines.append(f"({escape_pdf(bline)}) Tj")
            content_lines.append(f"0 -14 Td")
            curr_y -= 14
            
        content_lines.append(f"0 -10 Td")
        curr_y -= 10
        
    content_lines.append("ET")
    
    stream_content = "\n".join(content_lines)
    stream_bytes = stream_content.encode('latin1')
    stream_len = len(stream_bytes)
    
    # Objects
    # 1: Catalog
    # 2: Pages
    # 3: Page 1
    # 4: Font F1 (Helvetica)
    # 5: Font F2 (Helvetica-Bold)
    # 6: Contents
    
    offsets = {}
    output = bytearray()
    
    def write_str(s):
        output.extend(s.encode('latin1'))
        
    write_str("%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    
    offsets[1] = len(output)
    write_str("1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
    
    offsets[2] = len(output)
    write_str("2 0 obj\n<< /Type /Pages /Kids [3 0 R] /Count 1 >>\nendobj\n")
    
    offsets[3] = len(output)
    write_str("3 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Contents 6 0 R /Resources << /Font << /F1 4 0 R /F2 5 0 R >> >> >>\nendobj\n")
    
    offsets[4] = len(output)
    write_str("4 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>\nendobj\n")
    
    offsets[5] = len(output)
    write_str("5 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>\nendobj\n")
    
    offsets[6] = len(output)
    write_str(f"6 0 obj\n<< /Length {stream_len} >>\nstream\n")
    output.extend(stream_bytes)
    write_str("\nendstream\nendobj\n")
    
    xref_offset = len(output)
    write_str("xref\n0 7\n")
    write_str("0000000000 65535 f \n")
    for i in range(1, 7):
        write_str(f"{offsets[i]:010d} 00000 n \n")
        
    write_str(f"trailer\n<< /Size 7 /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n")
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "wb") as f:
        f.write(output)
    print(f"Generated PDF at: {output_path} ({len(output)} bytes)")


def escape_pdf(text):
    return text.replace('\\', '\\\\').replace('(', '\\(').replace(')', '\\)')


# --- DATA FOR THE 3 DOCUMENTS ---

DOC1_SECTIONS = [
    ("SECTION 1: REMOTE NETWORK ACCESS", [
        "1.1 All remote employees must connect to corporate infrastructure via Cisco AnyConnect VPN.",
        "1.2 VPN session idle timeout is set to 8 hours. Split-tunneling is enabled for non-work internet traffic."
    ]),
    ("SECTION 2: PASSWORD AND AUTHENTICATION STANDARDS", [
        "2.1 Passwords must be at least 8 characters long, including one number and one symbol.",
        "2.2 Mandatory password rotation is enforced every 90 days across all corporate directories.",
        "2.3 Two-Factor Authentication (2FA) is optional for standard non-administrative user accounts."
    ]),
    ("SECTION 3: HARDWARE AND DEVICE MANAGEMENT (BYOD)", [
        "3.1 Bring Your Own Device (BYOD) is permitted: Personal laptops may be used if registered with IT.",
        "3.2 Employees are responsible for maintaining updated antivirus software on personal equipment."
    ]),
    ("SECTION 4: DATA TRANSFER AND STORAGE", [
        "4.1 Offline data backup to encrypted USB flash drives is permitted for business continuity.",
        "4.2 File transfers over standard email attachments are allowed up to 25 MB per message."
    ])
]

DOC2_SECTIONS = [
    ("SECTION 1: REMOTE NETWORK ACCESS", [
        "1.1 Cisco AnyConnect is retired. All remote access must route through Cloudflare Zero Trust gateway.",
        "1.2 Maximum idle session timeout is reduced to 2 hours. Split-tunneling is strictly disabled."
    ]),
    ("SECTION 2: PASSWORD AND AUTHENTICATION STANDARDS", [
        "2.1 Passwords must be at least 12 characters in length.",
        "2.2 Password rotation interval is set to 180 days.",
        "2.3 Multi-Factor Authentication (MFA) is mandatory for all users via SMS OTP or Authenticator app."
    ]),
    ("SECTION 3: HARDWARE AND DEVICE MANAGEMENT", [
        "3.1 BYOD personal laptops are strictly prohibited for engineering, finance, and production access.",
        "3.2 Employees must use company-issued Lenovo ThinkPads with BitLocker encryption and Defender."
    ]),
    ("SECTION 4: DATA TRANSFER AND STORAGE", [
        "4.1 External USB mass storage devices and removable flash drives are blocked at OS level.",
        "4.2 Cloud storage is restricted to corporate Microsoft OneDrive with Data Loss Prevention (DLP)."
    ])
]

DOC3_SECTIONS = [
    ("SECTION 1: REMOTE NETWORK ACCESS", [
        "1.1 All remote connections require Zero Trust Network Access (ZTNA) with continuous posture check.",
        "1.2 Maximum idle session timeout is 30 minutes. Re-authentication is enforced at every resumption."
    ]),
    ("SECTION 2: PASSWORD AND AUTHENTICATION STANDARDS", [
        "2.1 Traditional passwords are deprecated in favor of FIDO2 WebAuthn hardware keys (YubiKey 5).",
        "2.2 For fallback systems requiring passphrases, minimum length is 16 characters with no periodic rotation.",
        "2.3 SMS-based 2FA is strictly banned due to SIM-swapping risks. Only FIDO2 hardware keys allowed."
    ]),
    ("SECTION 3: HARDWARE AND DEVICE MANAGEMENT", [
        "3.1 BYOD personal devices are 100% prohibited across all departments without exception.",
        "3.2 Only company hardware with CrowdStrike Falcon EDR, TPM 2.0, and remote wipe is permitted."
    ]),
    ("SECTION 4: DATA TRANSFER AND ARTIFICIAL INTELLIGENCE USAGE", [
        "4.1 USB storage ports remain permanently disabled at hardware BIOS level.",
        "4.2 Corporate AI Policy: Employees may only use internal offline document systems (RAGNext/Ollama).",
        "     Uploading internal source code or customer PII to public cloud AI tools is a critical violation."
    ])
]

if __name__ == "__main__":
    base_dir = r"E:\project\RAGNext\RAGNext"
    
    # 1. Output to sample_documents/
    sample_dir = os.path.join(base_dir, "sample_documents")
    
    # 2. Output to frontend/public/downloads/ for 1-click browser download
    downloads_dir = os.path.join(base_dir, "frontend", "public", "downloads")
    
    targets = [sample_dir, downloads_dir]
    
    for target in targets:
        text_to_pdf(
            "CYBER KNIGHTS ENTERPRISE - INFOSEC POLICY",
            "Version 1.0 (Superseded) | Effective: Jan 1, 2022 | Expiration: Dec 31, 2023",
            DOC1_SECTIONS,
            os.path.join(target, "Remote_Work_Security_Policy_v1.0.pdf")
        )
        text_to_pdf(
            "CYBER KNIGHTS ENTERPRISE - INFOSEC POLICY",
            "Version 2.0 (Superseded) | Effective: Jan 1, 2024 | Expiration: Dec 31, 2024",
            DOC2_SECTIONS,
            os.path.join(target, "Remote_Work_Security_Policy_v2.0.pdf")
        )
        text_to_pdf(
            "CYBER KNIGHTS ENTERPRISE - INFOSEC POLICY",
            "Version 3.0 (Active) | Effective: Jan 1, 2025 | Expiration: Indefinite / Active",
            DOC3_SECTIONS,
            os.path.join(target, "Remote_Work_Security_Policy_v3.0.pdf")
        )
