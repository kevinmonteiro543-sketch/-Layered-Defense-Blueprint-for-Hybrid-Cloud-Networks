#!/usr/bin/env python3
"""
================================================================================
HYBRID CLOUD DEFENSE BLUEPRINT - ACADEMIC / EXECUTIVE PDF GENERATOR
================================================================================
Generates a publication-grade, professional PDF report:
'Hybrid_Cloud_Defense_Blueprint.pdf'

Incorporating:
1. Executive Cover & Enterprise Application Context (NIST / ISO / PCI-DSS)
2. Hybrid Network Topology (Embedded High-Res Architecture Diagram & Walkthrough)
3. Granular Stateful Firewall & L7 Inspection Rules Table
4. IDS/IPS Deployment Strategy (NIDS vs HIDS Sensor Placement Justification)
5. Comprehensive Malware Defense Strategy (EDR, Email/CDR, Zero-Day Sandboxing)
6. Cybersecurity Risk Assessment Matrix (5 Enterprise Threats, Likelihood, Impact, Mitigation)
7. Complete Appendices containing 'generate_blueprint.py' Source Code

Author: Autonomous Cybersecurity Architecture Agent
================================================================================
"""

import os
import sys
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, Image, KeepTogether, PageBreak, HRFlowable, Preformatted
)
from reportlab.pdfgen import canvas

# ------------------------------------------------------------------------------
# 1. Numbered Canvas for Running Headers and Footers ("Page X of Y")
# ------------------------------------------------------------------------------
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super(NumberedCanvas, self).__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super(NumberedCanvas, self).showPage()
        super(NumberedCanvas, self).save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        page_w, page_h = letter

        # Running Top Header (Pages 2+)
        if self._pageNumber > 1:
            self.setFont("Helvetica-Bold", 8)
            self.setFillColor(colors.HexColor("#1E3A8A"))  # Deep Blue
            self.drawString(40, page_h - 28, "LAYERED DEFENSE BLUEPRINT // HYBRID CLOUD NETWORKS")

            self.setFont("Helvetica", 8)
            self.setFillColor(colors.HexColor("#64748B"))  # Slate Grey
            self.drawRightString(page_w - 40, page_h - 28, "CYBERSECURITY ARCHITECTURE SPECIFICATION")

            # Header hairline
            self.setStrokeColor(colors.HexColor("#CBD5E1"))
            self.setLineWidth(0.75)
            self.line(40, page_h - 32, page_w - 40, page_h - 32)

        # Running Bottom Footer (All Pages)
        self.setStrokeColor(colors.HexColor("#CBD5E1"))
        self.setLineWidth(0.75)
        self.line(40, 36, page_w - 40, 36)

        self.setFont("Helvetica-Bold", 7)
        self.setFillColor(colors.HexColor("#DC2626"))  # Red security banner
        self.drawString(40, 24, "CONFIDENTIAL // RESTRICTED")

        self.setFont("Helvetica", 7)
        self.setFillColor(colors.HexColor("#64748B"))
        self.drawString(160, 24, "NIST SP 800-53 Rev 5 | ISO/IEC 27001 | Zero Trust Architecture")

        page_str = f"Page {self._pageNumber} of {page_count}"
        self.setFont("Helvetica-Bold", 7.5)
        self.setFillColor(colors.HexColor("#1E293B"))
        self.drawRightString(page_w - 40, 24, page_str)

        self.restoreState()

# ------------------------------------------------------------------------------
# 2. PDF Document Generation Core
# ------------------------------------------------------------------------------
def build_pdf_blueprint(output_pdf_path="Hybrid_Cloud_Defense_Blueprint.pdf", image_path="hybrid_topology.png"):
    print(f"[*] Compiling professional PDF report: {output_pdf_path}...")

    # Document setup: Letter size with 40pt left/right, 38pt top/bottom margins
    doc = SimpleDocTemplate(
        output_pdf_path,
        pagesize=letter,
        leftMargin=40,
        rightMargin=40,
        topMargin=38,
        bottomMargin=42,
    )

    printable_width = letter[0] - 80  # 612 - 80 = 532 pt

    # Base Stylesheet
    base_styles = getSampleStyleSheet()

    # Custom Color Palette
    c_primary = colors.HexColor("#0F172A")    # Slate 900
    c_accent = colors.HexColor("#1E40AF")     # Blue 800
    c_secondary = colors.HexColor("#0D9488")  # Teal 600
    c_body = colors.HexColor("#1E293B")       # Slate 800
    c_subtext = colors.HexColor("#475569")    # Slate 600
    c_bg_light = colors.HexColor("#F8FAFC")   # Slate 50
    c_border = colors.HexColor("#CBD5E1")     # Slate 300
    c_red = colors.HexColor("#DC2626")        # Red 600
    c_green = colors.HexColor("#16A34A")      # Green 600

    # Typography Styles
    title_style = ParagraphStyle(
        "DocTitle",
        parent=base_styles["Title"],
        fontName="Helvetica-Bold",
        fontSize=20,
        leading=24,
        textColor=c_primary,
        alignment=0,
        spaceAfter=3,
    )

    subtitle_style = ParagraphStyle(
        "DocSubtitle",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=10.5,
        leading=14,
        textColor=c_accent,
        spaceAfter=8,
    )

    h1_style = ParagraphStyle(
        "Heading1_Custom",
        parent=base_styles["Heading1"],
        fontName="Helvetica-Bold",
        fontSize=12.5,
        leading=16,
        textColor=c_primary,
        spaceBefore=8,
        spaceAfter=4,
        keepWithNext=True,
    )

    h2_style = ParagraphStyle(
        "Heading2_Custom",
        parent=base_styles["Heading2"],
        fontName="Helvetica-Bold",
        fontSize=10,
        leading=13,
        textColor=c_accent,
        spaceBefore=6,
        spaceAfter=3,
        keepWithNext=True,
    )

    body_style = ParagraphStyle(
        "Body_Custom",
        parent=base_styles["BodyText"],
        fontName="Helvetica",
        fontSize=8.5,
        leading=11.8,
        textColor=c_body,
        spaceAfter=5,
    )

    bullet_style = ParagraphStyle(
        "Bullet_Custom",
        parent=body_style,
        fontSize=8.2,
        leading=11.2,
        leftIndent=12,
        firstLineIndent=-8,
        spaceAfter=3,
    )

    callout_text = ParagraphStyle(
        "CalloutText",
        parent=body_style,
        fontSize=8,
        leading=11,
        textColor=colors.HexColor("#1E3A8A"),
    )

    table_cell = ParagraphStyle(
        "TableCell",
        parent=base_styles["Normal"],
        fontName="Helvetica",
        fontSize=7,
        leading=9.2,
        textColor=c_body,
    )

    table_cell_bold = ParagraphStyle(
        "TableCellBold",
        parent=table_cell,
        fontName="Helvetica-Bold",
    )

    table_header = ParagraphStyle(
        "TableHeader",
        parent=base_styles["Normal"],
        fontName="Helvetica-Bold",
        fontSize=7.2,
        leading=9.5,
        textColor=colors.white,
    )

    code_style = ParagraphStyle(
        "CodeText",
        parent=base_styles["Normal"],
        fontName="Courier",
        fontSize=6.2,
        leading=7.8,
        textColor=colors.HexColor("#0F172A"),
    )

    story = []

    # ==========================================================================
    # PAGE 1: TITLE & SECTION 1 - INTRODUCTION & REAL-WORLD APPLICATION
    # ==========================================================================
    meta_box = [
        [
            Paragraph("<b>DOCUMENT:</b> Architectural Defense Blueprint", table_cell),
            Paragraph("<b>VERSION:</b> 1.0 (Production Release)", table_cell),
            Paragraph(f"<b>DATE:</b> {datetime.now().strftime('%B %d, %Y')}", table_cell),
        ],
        [
            Paragraph("<b>FRAMEWORK:</b> NIST SP 800-53 / Zero Trust", table_cell),
            Paragraph("<b>CLASSIFICATION:</b> Enterprise Restricted", table_cell),
            Paragraph("<b>STATUS:</b> Approved Architecture", table_cell),
        ]
    ]
    t_meta = Table(meta_box, colWidths=[177, 177, 178])
    t_meta.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F1F5F9")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#CBD5E1")),
        ('INNERGRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('LEFTPADDING', (0,0), (-1,-1), 6),
        ('RIGHTPADDING', (0,0), (-1,-1), 6),
    ]))

    story.append(Paragraph("Layered Defense Blueprint for Hybrid Cloud Networks", title_style))
    story.append(Paragraph("A Rigorous Zero-Trust & Defense-in-Depth Architectural Specification", subtitle_style))
    story.append(t_meta)
    story.append(Spacer(1, 8))

    story.append(Paragraph("1. Introduction & Real-World Application", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=1, spaceAfter=5))

    sec1_text = (
        "Modern enterprise computing demands hybrid cloud infrastructures that bridge on-premises data centers "
        "with hyperscale public cloud providers (such as AWS and Azure). This architectural blueprint defines a "
        "comprehensive, defense-in-depth security model engineered for enterprise environments handling sensitive, "
        "regulated workloads (such as online banking transactions, electronic health records, and customer PII). "
        "Traditional perimeter-only defense models are obsolete against sophisticated adversaries capable of supply-chain "
        "compromise, credential stuffing, and advanced persistent threat (APT) lateral propagation. Consequently, this blueprint "
        "operationalizes a <b>Zero Trust Architecture (ZTA)</b> adhering strictly to <b>NIST SP 800-207</b> guidelines: "
        "<i>never trust, always verify, and assume breach</i> across every network plane."
    )
    story.append(Paragraph(sec1_text, body_style))

    pillars_table = [
        [
            Paragraph(
                "<b>ARCHITECTURAL PILLARS & REGULATORY COMPLIANCE MAPPING:</b><br/>"
                "• <b>PCI-DSS v4.0 Requirement 1:</b> Enforce and maintain network security controls restricting inbound/outbound traffic.<br/>"
                "• <b>NIST SP 800-53 Rev 5 (SC-7 / AC-4):</b> Boundary protection, information flow enforcement, and micro-segmentation.<br/>"
                "• <b>HIPAA Security Rule (§ 164.312):</b> End-to-end encryption in transit (MACsec/TLS 1.3) and isolated data tiers.<br/>"
                "• <b>Zero Trust Micro-Segmentation:</b> Default-deny stateful boundary inspection and cryptographic identity validation.",
                callout_text
            )
        ]
    ]
    t_pillars = Table(pillars_table, colWidths=[printable_width])
    t_pillars.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#EFF6FF")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BFDBFE")),
        ('LINELEFT', (0,0), (0,-1), 3.5, c_accent),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_pillars)
    story.append(Spacer(1, 6))

    topo_intro = (
        "<b>Architectural Scope & Boundary Overview:</b><br/>"
        "The system establishes four segregated trust boundaries: (1) Untrusted External Boundary (Internet, Remote Workforce); "
        "(2) On-Premises Enterprise Datacenter (DMZ, Internal LAN, Core Identity Subnet); (3) Encrypted Hybrid Interconnect "
        "(Dedicated 10G AWS Direct Connect with MACsec Layer 2 encryption and IPsec BGP failover); and (4) AWS Cloud VPC "
        "(Multi-AZ Public Ingress, Private Containerized Microservices, Isolated Database Tier, and Cloud Security Telemetry). "
        "The following section visualizes the holistic topology and outlines the component security specifications."
    )
    story.append(Paragraph(topo_intro, body_style))

    # ==========================================================================
    # PAGE 2: SECTION 2 - TOPOLOGY DIAGRAM & DETAILED ZONE WALKTHROUGH
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("2. Hybrid Network Topology Architecture", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=1, spaceAfter=5))

    # Embed Topology Diagram (scaled cleanly to fit upper half of page 2)
    if os.path.exists(image_path):
        disp_w = 520
        disp_h = 240
        story.append(Image(image_path, width=disp_w, height=disp_h))
        story.append(Paragraph("<b>Figure 1:</b> Programmatically Generated Hybrid Cloud Defense Network Topology (via <code>generate_blueprint.py</code> / <code>diagrams</code> engine).", ParagraphStyle("Cap", parent=body_style, fontSize=7, textColor=c_subtext, alignment=1, spaceBefore=2, spaceAfter=5)))

    story.append(Paragraph("<b>Detailed Security Zone Walkthrough & Interconnect Specifications:</b>", h2_style))
    story.append(Paragraph("• <b>On-Premises DMZ Subnet (10.0.1.0/24):</b> Serves as the public exposure buffer. Hosts active-passive Next-Generation Firewalls (NGFW), Web Application Firewall (WAF) reverse proxies terminating external TLS 1.3, and a hardened Privileged Access Management (PAM) Bastion host requiring hardware FIDO2 MFA. External direct access to internal subnets is strictly blocked.", bullet_style))
    story.append(Paragraph("• <b>Internal Corporate Subnet (10.0.2.0/24):</b> Segregated corporate user workstations and internal application tiers governed by 802.1X Network Access Control (NAC). East-West workstation communication is disabled to prevent peer-to-peer worm propagation.", bullet_style))
    story.append(Paragraph("• <b>Core Identity & Vault Subnet (10.0.3.0/24):</b> Houses Active Directory Domain Controllers, Kerberos KDC, HashiCorp Vault for dynamic secret distribution, and a dedicated Suricata/Zeek Network Intrusion Detection (NIDS) sensor passively inspecting mirrored core switch SPAN traffic.", bullet_style))
    story.append(Paragraph("• <b>Encrypted Hybrid Interconnect:</b> Dual-path connectivity comprising a primary 10 Gbps AWS Direct Connect private circuit hardened with IEEE 802.1AE MACsec 256-bit point-to-point hardware encryption, overlaid with a route-based IPsec VPN tunnel (AES-256-GCM, SHA-384, Diffie-Hellman Group 21) running dynamic BGP peering for automated sub-second failover.", bullet_style))
    story.append(Paragraph("• <b>AWS Cloud VPC (172.16.0.0/16):</b> Organized into three multi-Availability Zone tiers: <i>Public Ingress</i> (AWS WAF, Shield, Dual-AZ ALB), <i>Private Application</i> (EKS microservices, VPC Traffic Mirroring target), and an <i>Isolated Database Tier</i> (Aurora PostgreSQL Multi-AZ with zero route to the internet, protected by customer-managed KMS encryption).", bullet_style))
    story.append(Paragraph("• <b>Unified Cloud Security & Telemetry Plane:</b> Amazon GuardDuty analyzes CloudTrail and VPC Flow Logs using ML anomaly detection, AWS Security Hub aggregates compliance postures, and logs stream to an on-premises Splunk SIEM.", bullet_style))

    # ==========================================================================
    # PAGE 3: SECTION 3 - FIREWALL RULES TABLE
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("3. Stateful Firewall Rules & Boundary Filtering Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=1, spaceAfter=5))

    fw_intro = (
        "Network traffic boundaries enforce stateful packet inspection alongside Layer 7 Application-ID filtering. "
        "Security policies follow a strict Zero-Trust default-deny baseline: any packet not explicitly whitelisted by rule ID "
        "is dropped, logged, and alerted to the Security Operations Center (SOC)."
    )
    story.append(Paragraph(fw_intro, body_style))

    from generate_blueprint import FIREWALL_RULES

    fw_table_data = [
        [
            Paragraph("<b>Rule ID</b>", table_header),
            Paragraph("<b>Boundary</b>", table_header),
            Paragraph("<b>Source</b>", table_header),
            Paragraph("<b>Destination</b>", table_header),
            Paragraph("<b>Port/Proto</b>", table_header),
            Paragraph("<b>Inspection Level</b>", table_header),
            Paragraph("<b>Action</b>", table_header),
            Paragraph("<b>Security Justification</b>", table_header),
        ]
    ]

    for r in FIREWALL_RULES:
        action_color = c_green if r["action"] == "ALLOW" else c_red
        fw_table_data.append([
            Paragraph(f"<b>{r['id']}</b>", table_cell_bold),
            Paragraph(r["boundary"], table_cell),
            Paragraph(r["source"], table_cell),
            Paragraph(r["destination"], table_cell),
            Paragraph(r["proto_port"], table_cell),
            Paragraph(r["inspection"], table_cell),
            Paragraph(f"<font color='{action_color.hexval()}'><b>{r['action']}</b></font>", table_cell_bold),
            Paragraph(r["justification"], table_cell),
        ])

    col_widths = [50, 64, 58, 64, 48, 76, 36, 136]
    t_fw = Table(fw_table_data, colWidths=col_widths, repeatRows=1)
    t_fw.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 3),
        ('RIGHTPADDING', (0,0), (-1,-1), 3),
    ]))
    story.append(t_fw)
    story.append(Spacer(1, 8))

    fw_notes = (
        "<b>Boundary Enforcement Policy:</b> All inter-zone flows require bidirectional state verification. Session states "
        "are tracked using dynamic TCP sequence window validation and strict handshake enforcement. Layer 7 rules enforce "
        "decryption of approved TLS connections at boundary proxies for deep payload inspection before re-encrypting with "
        "internal certificates."
    )
    story.append(Paragraph(fw_notes, body_style))

    # ==========================================================================
    # PAGE 4: SECTION 4 - IDS/IPS DEPLOYMENT STRATEGY
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("4. IDS/IPS Deployment Strategy (Sensor Placement Justification)", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=1, spaceAfter=5))

    ids_text1 = (
        "An effective intrusion detection and prevention architecture combines <b>Network Intrusion Detection/Prevention Systems (NIDS/NIPS)</b> "
        "and <b>Host-based Intrusion Detection Systems (HIDS)</b> to eliminate enterprise blind spots. While NIDS excels at detecting broad "
        "reconnaissance, wire exploits, and lateral traffic flows across network segments, it is blind to encrypted TLS payloads without active "
        "man-in-the-middle decryption. Conversely, HIDS (EDR agents) possesses complete visibility into OS process trees, memory injection, "
        "and decrypted application buffers, but lacks the holistic multi-segment network context."
    )
    story.append(Paragraph(ids_text1, body_style))

    sensor_data = [
        [
            Paragraph("<b>Sensor Location</b>", table_header),
            Paragraph("<b>Type & Mode</b>", table_header),
            Paragraph("<b>Monitored Boundary</b>", table_header),
            Paragraph("<b>Architectural Justification & Threat Coverage</b>", table_header),
        ],
        [
            Paragraph("<b>Perimeter DMZ</b>", table_cell_bold),
            Paragraph("NIPS (Inline)", table_cell),
            Paragraph("WAN to On-Prem DMZ", table_cell),
            Paragraph("Placed directly behind perimeter NGFW. Intercepts web application exploits, CVE-targeted buffer overflows, and known malicious IPs prior to hitting reverse proxies. Equipped with hardware bypass fail-open.", table_cell),
        ],
        [
            Paragraph("<b>Core Switch SPAN</b>", table_cell_bold),
            Paragraph("NIDS (Passive)", table_cell),
            Paragraph("Internal LAN & Identity Subnet", table_cell),
            Paragraph("Taps mirrored core switch ports. Detects East-West lateral reconnaissance, ARP poisoning, rogue DHCP servers, SMB worm activity, and Kerberos ticket-granting anomalies without introducing latency.", table_cell),
        ],
        [
            Paragraph("<b>Interconnect Gateway</b>", table_cell_bold),
            Paragraph("NIDS (Passive)", table_cell),
            Paragraph("Direct Connect & IPsec VPN", table_cell),
            Paragraph("Monitors cross-premises transit traffic. Enforces compliance with microservice communication schemas, detects anomalous data staging, and spots cross-environment pivot attempts.", table_cell),
        ],
        [
            Paragraph("<b>Cloud VPC Mirror</b>", table_cell_bold),
            Paragraph("Cloud NIDS (Suricata)", table_cell),
            Paragraph("EKS App Tier ENIs", table_cell),
            Paragraph("Leverages AWS VPC Traffic Mirroring to mirror container network interface packets to a dedicated Suricata cluster. Inspects unencrypted HTTP microservice payloads post-ALB decryption.", table_cell),
        ],
        [
            Paragraph("<b>Workstations & EC2</b>", table_cell_bold),
            Paragraph("HIDS / EDR (Agent)", table_cell),
            Paragraph("Endpoint OS Kernel & Memory", table_cell),
            Paragraph("CrowdStrike Falcon and OSSEC agents installed on all endpoints and nodes. Overcomes TLS encryption blind spots by monitoring syscalls, LSASS memory dumping, PowerShell execution, and file integrity.", table_cell),
        ],
    ]
    t_sensor = Table(sensor_data, colWidths=[90, 75, 105, 262])
    t_sensor.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_accent),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_sensor)
    story.append(Spacer(1, 8))

    correlation_text = (
        "<b>Unified Event Correlation & Security Orchestration (SOAR):</b><br/>"
        "Security telemetry from Suricata, Zeek, OSSEC, and CrowdStrike Falcon is formatted in Common Event Format (CEF) / OCSF "
        "and streamed over TLS to an on-premises and cloud-mirrored SIEM/SOAR cluster. Automated SOAR playbooks execute dynamic "
        "containment actions: when an alert triggers a confidence threshold &gt; 90 (e.g. Kerberoasting or C2 beaconing), the SOAR engine "
        "automatically pushes an ephemeral drop rule to the perimeter NGFW, revokes active OAuth/Kerberos tokens in HashiCorp Vault, "
        "and quarantines the compromised host via the EDR API within 45 seconds."
    )
    story.append(Paragraph(correlation_text, body_style))

    # ==========================================================================
    # PAGE 5: SECTION 5 - MALWARE DEFENSE STRATEGY
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("5. Malware Defense Strategy", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=1, spaceAfter=5))

    mal_intro = (
        "Modern malware campaigns leverage polymorphic payloads, living-off-the-land binaries (LOLBins), and "
        "staged command-and-control (C2) communication. The blueprint implements a multi-layered malware defense pipeline "
        "spanning endpoints, email vectors, zero-day dynamic detonation chambers, and micro-segmentation:"
    )
    story.append(Paragraph(mal_intro, body_style))

    story.append(Paragraph("<b>A. Next-Generation Endpoint Detection & Response (EDR / XDR):</b>", h2_style))
    story.append(Paragraph("Every corporate workstation, server, and cloud container host runs a centralized EDR daemon (CrowdStrike Falcon / Microsoft Defender for Endpoint). EDR features include: (1) Machine-learning behavioral anomaly detection superseding static signature scanning; (2) Kernel-level hook protection safeguarding against LSASS memory access and process hollowing; (3) Integration with Microsoft AMSI (Antimalware Scan Interface) to deobfuscate scripts executed in PowerShell, VBScript, and JavaScript; (4) Automated isolation triggers that sever network connectivity if ransomware behaviors (rapid file entropy increases or Volume Shadow Copy deletion) are detected.", bullet_style))

    story.append(Paragraph("<b>B. Email Security Gateway & Content Disarm and Reconstruction (CDR):</b>", h2_style))
    story.append(Paragraph("Inbound and outbound corporate email passes through a Secure Email Gateway (SEG) enforcing: (1) Cryptographic authentication via strict SPF, 2048-bit DKIM, and DMARC enforcement (<code>p=reject; sp=reject; pct=100;</code>) eliminating domain spoofing; (2) Content Disarm and Reconstruction (CDR) that tears apart inbound Office documents and PDFs, strips all macros, embedded OLE objects, and active scripts, and synthesizes a safe, reconstructed document before mailbox delivery; (3) Dynamic Time-of-Click URL inspection replacing hyperlinked URLs with inspection proxy redirects.", bullet_style))

    story.append(Paragraph("<b>C. Zero-Day Dynamic Sandboxing (Detonation Chambers):</b>", h2_style))
    story.append(Paragraph("Unidentified binaries, executables, and high-risk attachments intercepted by firewalls, email gateways, or proxy filters are dynamically routed to an isolated, multi-OS hypervisor detonation sandbox (e.g., Cuckoo / Palo Alto WildFire). The detonation engine executes files in customized virtual environments instrumented with kernel telemetry to analyze: (1) Anti-evasion countermeasures (such as prolonged sleep timers, registry hypervisor detection checks, and mouse-motion heuristics); (2) Process spawning, memory mutations, and unauthorized registry writes; (3) Outbound network beaconing, DNS tunneling, and C2 handshakes. Dynamic signatures (YARA rules, SHA-256 hashes, domain IOCs) are automatically compiled within 60 seconds and pushed globally across all boundary firewalls via automated STIX/TAXII threat intelligence pipelines.", bullet_style))

    story.append(Paragraph("<b>D. Lateral Movement Containment & Micro-Segmentation:</b>", h2_style))
    story.append(Paragraph("Should an endpoint suffer a zero-day compromise, lateral movement is stopped dead via host firewalls and 802.1X NAC disabling peer-to-peer workstation traffic. East-West traffic between servers is restricted to explicit application dependency graphs (e.g., Kubernetes Cilium NetworkPolicies and AWS Security Groups). Raw administrative protocols (SSH, RDP, WinRM) are prohibited between servers, routing exclusively through the PAM Bastion host with audited session recordings.", bullet_style))

    # ==========================================================================
    # PAGE 6: SECTION 6 - RISK ASSESSMENT TABLE
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("6. Cybersecurity Risk Assessment Matrix", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=1, spaceAfter=5))

    risk_intro = (
        "A formal risk assessment was conducted following <b>NIST SP 800-30 Revision 1</b> guidelines. Five critical threat "
        "scenarios targeting hybrid cloud topologies were evaluated across likelihood, impact, blueprint mitigation, and "
        "calculated residual risk:"
    )
    story.append(Paragraph(risk_intro, body_style))

    from generate_blueprint import RISK_ASSESSMENT_DATA

    risk_table_data = [
        [
            Paragraph("<b>ID</b>", table_header),
            Paragraph("<b>Identified Threat Vector</b>", table_header),
            Paragraph("<b>Likelihood</b>", table_header),
            Paragraph("<b>Impact</b>", table_header),
            Paragraph("<b>Blueprint Defense & Architectural Mitigation</b>", table_header),
            Paragraph("<b>Residual Risk</b>", table_header),
        ]
    ]

    for r in RISK_ASSESSMENT_DATA:
        lik_text = f"<font color='{c_red.hexval()}'><b>{r['likelihood']}</b></font>" if r['likelihood'] == 'High' else r['likelihood']
        risk_table_data.append([
            Paragraph(f"<b>{r['threat_id']}</b>", table_cell_bold),
            Paragraph(f"<b>{r['threat_name']}</b>", table_cell),
            Paragraph(lik_text, table_cell),
            Paragraph(f"<font color='{c_red.hexval()}'><b>{r['impact']}</b></font>", table_cell_bold),
            Paragraph(r["mitigation"], table_cell),
            Paragraph(f"<font color='{c_green.hexval()}'><b>{r['residual_risk']}</b></font>", table_cell_bold),
        ])

    t_risk = Table(risk_table_data, colWidths=[42, 105, 52, 48, 235, 50], repeatRows=1)
    t_risk.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), c_primary),
        ('ALIGN', (0,0), (-1,-1), 'LEFT'),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, c_border),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, c_bg_light]),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 4),
        ('RIGHTPADDING', (0,0), (-1,-1), 4),
    ]))
    story.append(t_risk)
    story.append(Spacer(1, 8))

    sla_box = [
        [
            Paragraph(
                "<b>INCIDENT RESPONSE & REMEDIATION SERVICE LEVEL AGREEMENTS (SLAs):</b><br/>"
                "• <b>Critical Threat Containment (P1):</b> Automated isolation within 60 seconds; SOC triage within 15 minutes.<br/>"
                "• <b>High Threat Mitigation (P2):</b> In-line rule update within 30 minutes; root-cause analysis within 4 hours.<br/>"
                "• <b>Disaster Recovery Objectives:</b> Recovery Time Objective (RTO) &lt; 1 hour; Recovery Point Objective (RPO) &lt; 5 minutes via cross-region Aurora and immutable S3 backups.",
                callout_text
            )
        ]
    ]
    t_sla = Table(sla_box, colWidths=[printable_width])
    t_sla.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,-1), colors.HexColor("#F0FDF4")),
        ('BOX', (0,0), (-1,-1), 1, colors.HexColor("#BBF7D0")),
        ('LINELEFT', (0,0), (0,-1), 3.5, c_green),
        ('TOPPADDING', (0,0), (-1,-1), 4),
        ('BOTTOMPADDING', (0,0), (-1,-1), 4),
        ('LEFTPADDING', (0,0), (-1,-1), 8),
        ('RIGHTPADDING', (0,0), (-1,-1), 8),
    ]))
    story.append(t_sla)

    # ==========================================================================
    # PAGES 7+: SECTION 7 - SOURCE CODE APPENDIX
    # ==========================================================================
    story.append(PageBreak())
    story.append(Paragraph("7. Source Code Appendix: generate_blueprint.py", h1_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=c_accent, spaceBefore=1, spaceAfter=5))

    src_intro = (
        "The following is the complete, verifiable Python implementation of <code>generate_blueprint.py</code>. "
        "It programmatically constructs the hybrid cloud network topology diagram using the <code>diagrams</code> library, "
        "and encapsulates CLI rendering functions for the security matrices."
    )
    story.append(Paragraph(src_intro, body_style))

    script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate_blueprint.py")
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            code_text = f.read()
    else:
        code_text = "# generate_blueprint.py source code"

    story.append(Preformatted(code_text, code_style))

    # Build the document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"[+] PDF Blueprint compiled successfully: {output_pdf_path}")
    return True

if __name__ == "__main__":
    build_pdf_blueprint()
