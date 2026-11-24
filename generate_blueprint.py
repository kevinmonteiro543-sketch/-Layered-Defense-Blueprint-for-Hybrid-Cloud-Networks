#!/usr/bin/env python3
"""
================================================================================
LAYERED DEFENSE BLUEPRINT FOR HYBRID CLOUD NETWORKS
================================================================================
Core Architecture Script:
1. Programmatically generates hybrid cloud network topology diagram (hybrid_topology.png)
   utilizing the Python 'diagrams' library.
2. Provides CLI formatting functions to render comprehensive Firewall Rules Tables
   and Cybersecurity Risk Assessment Tables directly in the console.

Author: Autonomous Cybersecurity Architecture Agent
Repository: https://github.com/kevinmonteiro543-sketch/-Layered-Defense-Blueprint-for-Hybrid-Cloud-Networks.git
================================================================================
"""

import os
import sys
import argparse

# ------------------------------------------------------------------------------
# 1. Environment & Graphviz Auto-Configuration
# ------------------------------------------------------------------------------
def configure_graphviz_path():
    """Ensure Graphviz binary path is in PATH on Windows systems."""
    potential_paths = [
        r"C:\Program Files (x86)\Graphviz\bin",
        r"C:\Program Files\Graphviz\bin",
        r"C:\Program Files (x86)\Graphviz\bin\dot.exe",
        r"C:\Program Files\Graphviz\bin\dot.exe",
    ]
    current_path = os.environ.get("PATH", "")
    for p in potential_paths:
        dir_path = os.path.dirname(p) if p.endswith(".exe") else p
        if os.path.exists(dir_path) and dir_path not in current_path:
            os.environ["PATH"] = dir_path + os.pathsep + current_path
            break

configure_graphviz_path()

# ------------------------------------------------------------------------------
# 2. Topology Diagram Generation Function
# ------------------------------------------------------------------------------
def generate_topology_diagram(output_filename="hybrid_topology"):
    """
    Programmatically creates the Hybrid Cloud Network Topology diagram
    reflecting defense-in-depth principles across On-Premises, Interconnect, and Cloud.
    """
    print("[*] Generating Hybrid Cloud Network Topology Diagram via 'diagrams' library...")
    try:
        from diagrams import Diagram, Cluster, Edge
        from diagrams.onprem.client import Users, Client
        from diagrams.generic.network import Firewall, Router, Switch, VPN
        from diagrams.onprem.network import Internet
        from diagrams.onprem.compute import Server
        from diagrams.onprem.security import Vault
        from diagrams.aws.network import TransitGateway, DirectConnect, ALB, NATGateway, InternetGateway, VPC
        from diagrams.aws.compute import EC2, EKS
        from diagrams.aws.database import RDS
        from diagrams.aws.security import WAF, Shield, Guardduty, SecurityHub
        from diagrams.aws.management import Cloudwatch
    except ImportError as e:
        print(f"[-] Error importing diagrams library: {e}")
        print("[-] Please run: pip install diagrams")
        return False

    graph_attr = {
        "fontsize": "22",
        "fontname": "Helvetica-Bold",
        "bgcolor": "#F8FAFC",
        "pad": "0.6",
        "splines": "ortho",
        "nodesep": "0.7",
        "ranksep": "0.8",
    }

    node_attr = {
        "fontsize": "11",
        "fontname": "Helvetica",
    }

    edge_attr = {
        "fontsize": "10",
        "fontname": "Helvetica",
    }

    with Diagram(
        "Layered Defense Blueprint for Hybrid Cloud Networks",
        show=False,
        filename=output_filename,
        outformat="png",
        direction="LR",
        graph_attr=graph_attr,
        node_attr=node_attr,
        edge_attr=edge_attr,
    ):
        # External Threat Surface / Public Traffic
        with Cluster("Untrusted External Boundary"):
            internet = Internet("Public Internet\n(WAN / Ingress)")
            remote_clients = Users("Remote Workforce\n& Global Users")

        # ----------------------------------------------------------------------
        # On-Premises Enterprise Datacenter
        # ----------------------------------------------------------------------
        with Cluster("On-Premises Corporate Datacenter (10.0.0.0/16)"):
            with Cluster("Perimeter DMZ Subnet (10.0.1.0/24)"):
                dmz_fw = Firewall("Perimeter NGFW\n(Stateful L7 DPI)")
                dmz_proxy = Server("WAF & Reverse Proxy\n(TLS 1.3 Offload)")
                dmz_bastion = Server("Secure PAM Bastion\n(MFA / Session Audit)")

            with Cluster("Internal Corporate Subnet (10.0.2.0/24)"):
                int_switch = Switch("Core Switch (802.1X NAC)")
                workstations = Client("Corporate Endpoints\n(EDR / Host Isolation)")
                app_servers = Server("Internal App Tier\n(Micro-segmented)")

            with Cluster("Identity & Management Subnet (10.0.3.0/24)"):
                ad_vault = Vault("Active Directory\n& HashiCorp Vault")
                onprem_nids = Server("Suricata NIDS Sensor\n(Core SPAN / Zeek)")

            onprem_router = Router("Edge Border Router\n(BGP / IPSec Endpoint)")

        # ----------------------------------------------------------------------
        # Hybrid Cloud Interconnect Transport Layer
        # ----------------------------------------------------------------------
        with Cluster("Encrypted Hybrid Interconnect"):
            dx_conn = DirectConnect("AWS Direct Connect\n(Primary 10 Gbps MACsec)")
            vpn_tunnel = VPN("IPsec VPN Tunnel\n(BGP Failover / AES-256)")

        # ----------------------------------------------------------------------
        # AWS Cloud VPC Environment
        # ----------------------------------------------------------------------
        with Cluster("AWS Production Cloud VPC (172.16.0.0/16)"):
            tgw = TransitGateway("AWS Transit Gateway\n(Segmented Route Tables)")

            with Cluster("Public Ingress Subnet (172.16.1.0/24)"):
                cloud_waf = WAF("AWS WAF & Shield\n(DDoS / Bot Control)")
                alb = ALB("Application Load Balancer\n(HTTPS Term / Path Route)")
                nat_gw = NATGateway("Managed NAT Gateway\n(Restricted Egress)")

            with Cluster("Private Application Subnet (172.16.2.0/24)"):
                cloud_eks = EKS("Microservices Cluster\n(EKS / Container HIDS)")
                vpc_mirror = Server("Cloud Traffic Mirror\n(Suricata NIDS Inspection)")

            with Cluster("Isolated Data Subnet (172.16.3.0/24)"):
                cloud_db = RDS("Aurora PostgreSQL Multi-AZ\n(KMS CMK Encrypted)")

            with Cluster("Cloud Security & Auditing Plane"):
                guardduty = Guardduty("Amazon GuardDuty\n(Threat Detection / ML)")
                sec_hub = SecurityHub("AWS Security Hub\n(CIS / NIST Posture)")
                cloudwatch = Cloudwatch("CloudWatch & SIEM\n(Immutable Audit Logs)")

        # ----------------------------------------------------------------------
        # Logical Network Flows & Security Inspection Edges
        # ----------------------------------------------------------------------
        # Ingress flows to On-Premises DMZ
        internet >> Edge(label="HTTPS / 443", color="#C53030") >> dmz_fw
        remote_clients >> Edge(label="MFA / 8443", color="#C53030") >> dmz_fw
        dmz_fw >> Edge(label="L7 Inspected", color="#2B6CB0") >> dmz_proxy
        dmz_fw >> Edge(label="Admin SSH/RDP", color="#2B6CB0") >> dmz_bastion

        # DMZ to Internal Subnets (Controlled)
        dmz_proxy >> Edge(label="Reverse Proxy (mTLS)", color="#2B6CB0") >> int_switch
        dmz_bastion >> Edge(label="PAM Bastion Session", color="#2B6CB0") >> int_switch

        # Internal LAN Routing & NIDS Tap
        int_switch >> Edge(color="#4A5568") >> workstations
        int_switch >> Edge(color="#4A5568") >> app_servers
        app_servers >> Edge(label="Kerberos/LDAPS", color="#2B6CB0") >> ad_vault
        int_switch >> Edge(label="SPAN Port Tap", style="dashed", color="#D69E2E") >> onprem_nids

        # Hybrid Transit Connection
        int_switch >> Edge(color="#4A5568") >> onprem_router
        onprem_router >> Edge(label="10G Dedicated Link", color="#2F855A") >> dx_conn >> Edge(color="#2F855A") >> tgw
        onprem_router >> Edge(label="IPsec Overlay (AES-GCM)", style="dashed", color="#2F855A") >> vpn_tunnel >> Edge(color="#2F855A") >> tgw

        # Cloud Ingress & Application Flow
        internet >> Edge(label="HTTPS Web Traffic", color="#C53030") >> cloud_waf >> alb
        alb >> Edge(label="Private Ingress (Port 8080)", color="#2B6CB0") >> cloud_eks
        cloud_eks >> Edge(label="Port 5432 Only", color="#2F855A") >> cloud_db
        cloud_eks >> Edge(label="Outbound OS Patches", color="#718096") >> nat_gw

        # Hybrid VPC Integration (Private East-West Transit)
        tgw >> Edge(label="Private Subnet Routing", color="#2B6CB0") >> cloud_eks

        # Cloud Telemetry, Mirroring & SIEM Integration
        cloud_eks >> Edge(label="VPC Traffic Mirror", style="dashed", color="#D69E2E") >> vpc_mirror
        cloud_eks >> Edge(style="dotted", color="#E53E3E") >> guardduty
        guardduty >> Edge(color="#805AD5") >> sec_hub
        sec_hub >> Edge(label="Security Findings", color="#805AD5") >> cloudwatch
        onprem_nids >> Edge(label="TLS Syslog to SIEM", style="dotted", color="#805AD5") >> cloudwatch

    print(f"[+] Network topology successfully rendered: {output_filename}.png")
    return True

# ------------------------------------------------------------------------------
# 3. Security Data Structures: Firewall Rules & Risk Assessment
# ------------------------------------------------------------------------------
FIREWALL_RULES = [
    {
        "id": "FW-RULE-01",
        "boundary": "WAN -> On-Prem DMZ",
        "source": "Internet (0.0.0.0/0)",
        "destination": "DMZ WAF / Proxy (10.0.1.10)",
        "proto_port": "TCP / 443",
        "inspection": "L7 DPI / TLS Offload / ModSecurity",
        "action": "ALLOW",
        "justification": "Public web service ingress; terminates TLS and filters OWASP Top 10 vulnerabilities.",
    },
    {
        "id": "FW-RULE-02",
        "boundary": "WAN -> On-Prem DMZ",
        "source": "Admin IPs / WAN (0.0.0.0/0)",
        "destination": "PAM Bastion (10.0.1.20)",
        "proto_port": "TCP / 8443",
        "inspection": "L7 Stateful / FIDO2 MFA / Session Rec",
        "action": "ALLOW",
        "justification": "Secure administrator jump-host access; raw SSH (22) and RDP (3389) dropped at perimeter.",
    },
    {
        "id": "FW-RULE-03",
        "boundary": "DMZ -> Internal LAN",
        "source": "DMZ WAF / Proxy (10.0.1.10)",
        "destination": "Internal App Tier (10.0.2.50/28)",
        "proto_port": "TCP / 8443",
        "inspection": "L7 App-ID / Mutual TLS (mTLS)",
        "action": "ALLOW",
        "justification": "Sanitized reverse proxy request forwarding; prevents direct external access to internal LAN.",
    },
    {
        "id": "FW-RULE-04",
        "boundary": "Internal LAN -> Hybrid TGW",
        "source": "Internal Apps (10.0.2.0/24)",
        "destination": "Cloud Private App (172.16.2.0/24)",
        "proto_port": "TCP / 8080, 8443, 9092",
        "inspection": "L4 Stateful + L7 App-ID over IPsec",
        "action": "ALLOW",
        "justification": "Cross-premises microservice API calls and Apache Kafka event streaming over Direct Connect.",
    },
    {
        "id": "FW-RULE-05",
        "boundary": "Internal / Cloud -> Identity",
        "source": "Internal & Cloud Apps",
        "destination": "AD & Vault (10.0.3.10-15)",
        "proto_port": "TCP / 636, 88, 8200",
        "inspection": "Stateful Inspection / LDAP Signing",
        "action": "ALLOW",
        "justification": "Centralized identity validation (LDAPS/Kerberos) and ephemeral secrets retrieval via Vault.",
    },
    {
        "id": "FW-RULE-06",
        "boundary": "WAN -> Cloud Public Subnet",
        "source": "Internet (0.0.0.0/0)",
        "destination": "AWS Cloud ALB (172.16.1.100)",
        "proto_port": "TCP / 443",
        "inspection": "AWS WAF Managed Rules / Shield DDoS",
        "action": "ALLOW",
        "justification": "Cloud web ingress gateway; rate-limiting and bot mitigation enabled; HTTP redirected to HTTPS.",
    },
    {
        "id": "FW-RULE-07",
        "boundary": "Cloud Public -> Cloud Private",
        "source": "Cloud ALB (sg-alb-ingress)",
        "destination": "EKS Microservices (172.16.2.0/24)",
        "proto_port": "TCP / 8080",
        "inspection": "Security Group Reference / L4 Stateful",
        "action": "ALLOW",
        "justification": "Decoupled traffic distribution to container workloads; instances have no public IPs.",
    },
    {
        "id": "FW-RULE-08",
        "boundary": "Cloud Private -> Cloud Database",
        "source": "EKS Microservices (sg-app)",
        "destination": "Aurora PostgreSQL (172.16.3.50)",
        "proto_port": "TCP / 5432",
        "inspection": "L4 Stateful / Enforce TLS / IAM Auth",
        "action": "ALLOW",
        "justification": "Application data persistence; isolated DB subnet denies all traffic except authorized app tier.",
    },
    {
        "id": "FW-RULE-09",
        "boundary": "Private Tiers -> External WAN",
        "source": "Internal LAN & Cloud Private",
        "destination": "External Repositories (Whitelisted)",
        "proto_port": "TCP / 443",
        "inspection": "NAT Gateway / Forward Proxy FQDN Filter",
        "action": "ALLOW",
        "justification": "Outbound security patches (apt/yum) and container registry pulls; unrestricted egress blocked.",
    },
    {
        "id": "FW-RULE-10",
        "boundary": "All Hybrid Boundaries",
        "source": "ANY (*)",
        "destination": "ANY (*)",
        "proto_port": "ALL (*)",
        "inspection": "Stateful Packet Drop / SIEM Alerting",
        "action": "DENY",
        "justification": "Zero Trust baseline: implicit deny rule dropping all unregistered traffic and logging attempts.",
    },
]

RISK_ASSESSMENT_DATA = [
    {
        "threat_id": "THR-01",
        "threat_name": "Ransomware Lateral Movement via Interconnect",
        "likelihood": "High",
        "impact": "Critical",
        "mitigation": "Stateful boundary firewalls block SMB (445), RPC (135), and RDP (3389) over Direct Connect/VPN. Micro-segmentation on LAN, EDR canary traps, automated host quarantine, and WORM-locked cloud backups.",
        "residual_risk": "Low",
    },
    {
        "threat_id": "THR-02",
        "threat_name": "Zero-Day Remote Code Execution (RCE) on DMZ",
        "likelihood": "Medium",
        "impact": "Critical",
        "mitigation": "Dual WAF inspection (AWS WAF & On-Prem ModSecurity) with virtual patching. Read-only container root filesystems, non-root execution, and Suricata NIPS blocking egress reverse shells.",
        "residual_risk": "Low",
    },
    {
        "threat_id": "THR-03",
        "threat_name": "Insider Threat & Credential Harvesting",
        "likelihood": "Medium",
        "impact": "High",
        "mitigation": "802.1X NAC endpoint posture enforcement. Internal NIDS monitoring for Pass-the-Hash, Golden Ticket, and Kerberoasting. Dynamic ephemeral credentials via Vault and mandatory hardware FIDO2 MFA.",
        "residual_risk": "Low",
    },
    {
        "threat_id": "THR-04",
        "threat_name": "Man-in-the-Middle (MitM) & BGP Route Hijack",
        "likelihood": "Low",
        "impact": "High",
        "mitigation": "IEEE 802.1AE MACsec (256-bit) point-to-point encryption on Direct Connect. IPsec VPN overlay with IKEv2, AES-256-GCM, and Diffie-Hellman Group 21. BGP MD5 authentication and RPKI filtering.",
        "residual_risk": "Low",
    },
    {
        "threat_id": "THR-05",
        "threat_name": "Cloud Data Exfiltration via Compromised Container",
        "likelihood": "Medium",
        "impact": "Critical",
        "mitigation": "Strict IAM Roles for Service Accounts (IRSA) with least-privilege scoping. Database residing in isolated private subnet with zero internet route. Egress proxy FQDN whitelisting and GuardDuty ML anomaly alerts.",
        "residual_risk": "Low",
    },
]

# ------------------------------------------------------------------------------
# 4. CLI Table Output Functions
# ------------------------------------------------------------------------------
def print_cli_banner():
    """Prints a styled terminal banner."""
    banner = """
================================================================================
          LAYERED DEFENSE BLUEPRINT FOR HYBRID CLOUD NETWORKS
               Zero Trust Security Architecture & Operations
================================================================================
    """
    print(banner)

def print_firewall_rules_table():
    """Renders the Firewall Rules table with clean ASCII formatting."""
    print("\n" + "=" * 110)
    print(" SECTION 3: STATEFUL FIREWALL RULES & APPLICATION-LAYER FILTERING MATRIX")
    print("=" * 110)
    header = f"{'Rule ID':<11} | {'Boundary':<22} | {'Protocol/Port':<16} | {'Action':<6} | {'Justification':<45}"
    print(header)
    print("-" * 110)
    for rule in FIREWALL_RULES:
        rule_id = rule["id"]
        boundary = rule["boundary"]
        proto = rule["proto_port"]
        action = rule["action"]
        just = rule["justification"]
        if len(just) > 45:
            just = just[:42] + "..."
        print(f"{rule_id:<11} | {boundary:<22} | {proto:<16} | {action:<6} | {just:<45}")
    print("=" * 110)

def print_risk_assessment_table():
    """Renders the Cybersecurity Risk Assessment table with clean ASCII formatting."""
    print("\n" + "=" * 115)
    print(" SECTION 6: HYBRID CLOUD CYBERSECURITY RISK ASSESSMENT & MITIGATION MATRIX")
    print("=" * 115)
    header = f"{'ID':<7} | {'Identified Threat Vector':<38} | {'Likelihood':<10} | {'Impact':<10} | {'Residual Risk':<13}"
    print(header)
    print("-" * 115)
    for risk in RISK_ASSESSMENT_DATA:
        t_id = risk["threat_id"]
        t_name = risk["threat_name"]
        if len(t_name) > 38:
            t_name = t_name[:35] + "..."
        likelihood = risk["likelihood"]
        impact = risk["impact"]
        res_risk = risk["residual_risk"]
        print(f"{t_id:<7} | {t_name:<38} | {likelihood:<10} | {impact:<10} | {res_risk:<13}")
    print("=" * 115)
    print("\n[*] Mitigation Strategy Summary:")
    for risk in RISK_ASSESSMENT_DATA:
        print(f"  [{risk['threat_id']}] {risk['threat_name']}")
        print(f"      -> Mitigation: {risk['mitigation']}\n")

def print_security_tables():
    """CLI text-output function printing both security matrices."""
    print_cli_banner()
    print_firewall_rules_table()
    print_risk_assessment_table()

# ------------------------------------------------------------------------------
# 5. Main Execution Entry Point
# ------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(
        description="Layered Defense Blueprint for Hybrid Cloud Networks - Topology & CLI Matrix Generator"
    )
    parser.add_argument(
        "--no-diagram", action="store_true", help="Skip generating the network topology PNG diagram"
    )
    parser.add_argument(
        "--output-image", default="hybrid_topology", help="Base filename for generated topology diagram"
    )
    parser.add_argument(
        "--pdf", action="store_true", help="Also generate the comprehensive PDF blueprint report"
    )
    args = parser.parse_args()

    # Step 1: Print Security Tables to Terminal
    print_security_tables()

    # Step 2: Generate Diagram unless skipped
    if not args.no_diagram:
        generate_topology_diagram(args.output_image)

    # Step 3: Optional PDF compilation
    if args.pdf:
        try:
            from generate_pdf_report import build_pdf_blueprint
            build_pdf_blueprint()
        except ImportError:
            print("[-] generate_pdf_report module not found. Skipping PDF generation.")

if __name__ == "__main__":
    main()
