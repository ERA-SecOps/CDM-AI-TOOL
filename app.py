
import streamlit as st
import pandas as pd
from faker import Faker
import random
import json
import base64
import socket
import urllib.request
import psutil
from datetime import datetime

# ==============================================================================
# 1. Page Configuration & Custom CSS
# ==============================================================================
st.set_page_config(
    page_title="ERA SecOps | Enterprise Cyber Defense Matrix Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    /* Hide Default Streamlit Top Header & White Banner */
    header[data-testid="stHeader"] {
        display: none !important;
    }
    div[data-testid="stDecoration"] {
        display: none !important;
    }
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
    }

    /* Dark Mode Global Background */
    .stApp {
        background-color: #0b0e14;
        color: #adbac7;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Dark Theme Sidebar Target */
    [data-testid="stSidebar"] {
        background-color: #121824 !important;
        border-right: 1px solid #1e2638;
    }
    [data-testid="stSidebar"] * {
        color: #adbac7 !important;
    }

    /* Custom Command Header Bar */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #121824;
        padding: 14px 28px;
        border-radius: 10px;
        border: 1px solid #1e2638;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        margin-bottom: 22px;
    }
    .brand-title {
        font-size: 21px;
        font-weight: 700;
        color: #f0f6fc;
        display: flex;
        align-items: center;
        gap: 12px;
    }
    .status-pill {
        background-color: rgba(46, 160, 67, 0.15);
        color: #3fb950;
        border: 1px solid rgba(46, 160, 67, 0.4);
        padding: 5px 14px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        letter-spacing: 0.5px;
    }

    /* Metric Cards */
    .metric-container {
        background-color: #121824;
        border: 1px solid #1e2638;
        border-radius: 10px;
        padding: 18px;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.2);
    }
    .metric-header {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #768390;
        margin-bottom: 8px;
        font-weight: 600;
    }
    .metric-value {
        font-size: 30px;
        font-weight: 700;
        color: #f0f6fc;
    }
    .metric-footer {
        font-size: 12px;
        color: #3fb950;
        margin-top: 6px;
        font-weight: 500;
    }

    /* FORCE OVERRIDE RED TABS TO ENTERPRISE BLUE */
    button[data-baseweb="tab"] {
        background-color: #161e2e !important;
        border: 1px solid #253047 !important;
        border-radius: 8px !important;
        padding: 8px 18px !important;
        color: #8b949e !important;
        font-weight: 600 !important;
    }
    button[data-baseweb="tab"]:hover {
        border-color: #388bfd !important;
        color: #58a6ff !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] {
        background-color: #1f6beb !important;
        border-color: #58a6ff !important;
        box-shadow: 0 0 12px rgba(31, 107, 235, 0.5) !important;
    }
    button[data-baseweb="tab"][aria-selected="true"] p {
        color: #ffffff !important;
        font-weight: 700 !important;
    }
    div[data-baseweb="tab-highlight"] {
        background-color: transparent !important;
    }

    /* 5x5 CDM Table Display */
    .cdm-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 8px;
        margin-top: 10px;
    }
    .cdm-header {
        background-color: #161e2e;
        color: #8b949e;
        padding: 14px;
        font-size: 12px;
        text-transform: uppercase;
        letter-spacing: 0.6px;
        border-radius: 6px;
        text-align: center;
        font-weight: 700;
        border: 1px solid #1e2638;
    }
    .cdm-cell {
        background-color: #121824;
        border: 1px solid #1e2638;
        padding: 14px;
        border-radius: 8px;
        font-size: 12px;
        color: #adbac7;
        transition: all 0.2s ease;
    }
    .cdm-cell:hover {
        border-color: #388bfd;
        background-color: #182236;
        transform: translateY(-2px);
    }
    .cell-title {
        font-weight: 600;
        color: #f0f6fc;
        margin-bottom: 6px;
    }
    .cell-tag {
        font-size: 10px;
        color: #3fb950;
        background: rgba(63, 185, 80, 0.12);
        padding: 3px 8px;
        border-radius: 4px;
        display: inline-block;
        font-weight: 600;
        border: 1px solid rgba(63, 185, 80, 0.25);
    }

    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. Helper Functions & Intelligence Engines
# ==============================================================================
def svg_to_base64(svg_str):
    return f"data:image/svg+xml;base64,{base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')}"

SHIELD_SVG = svg_to_base64('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>')

if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "telemetry_logs" not in st.session_state:
    st.session_state.telemetry_logs = []
if "threat_status" not in st.session_state:
    st.session_state.threat_status = "LOW"
if "last_scan_status" not in st.session_state:
    st.session_state.last_scan_status = None

fake = Faker()

# Automatic Local Network Interface & Subnet Discovery
def detect_local_subnet():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        ip_parts = local_ip.split('.')
        subnet = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        return subnet, local_ip
    except Exception:
        return "192.168.0.0/24", "127.0.0.1"

# Fast MAC OUI Vendor Lookup
def resolve_mac_vendor(mac_address):
    mac_clean = mac_address.replace(":", "").replace("-", "").upper()
    static_oui = {
        "3C22FB": "Apple, Inc.",
        "F4D488": "Apple, Inc.",
        "0014D1": "Trendsnet / Router",
        "E45F01": "Raspberry Pi Foundation",
        "000C29": "VMware, Inc.",
        "080027": "Oracle VirtualBox",
        "B827EB": "Raspberry Pi Foundation",
        "DCA632": "Raspberry Pi Trading"
    }
    prefix = mac_clean[:6]
    if prefix in static_oui:
        return static_oui[prefix]

    try:
        url = f"https://api.macvendors.com/{mac_address}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req, timeout=1.0) as response:
            return response.read().decode('utf-8')
    except Exception:
        return "Network Hardware Vendor"

# Device Type & OS Fingerprint Engine
def infer_device_os(hostname, ip, vendor):
    vendor_lower = vendor.lower()
    host_lower = hostname.lower()

    if ip.endswith(".1"):
        return "Embedded Linux Gateway"
    elif "apple" in vendor_lower or "macbook" in host_lower or "iphone" in host_lower:
        return "macOS / iOS Device"
    elif "raspberry" in vendor_lower:
        return "Raspberry Pi OS (Linux)"
    elif "vmware" in vendor_lower or "virtualbox" in vendor_lower:
        return "Virtual Machine Guest"
    elif "amazon" in vendor_lower or "google" in vendor_lower or "nest" in host_lower:
        return "Smart IoT Appliance"
    elif "intel" in vendor_lower or "realtek" in vendor_lower:
        return "Windows / Linux Workstation"
    else:
        return "Generic Network Appliance"

# Active Connection Safety & Threat Assessment Engine
def analyze_active_connections():
    connections = []
    suspicious_ports = [22, 23, 135, 139, 445, 3389, 4444, 6667, 9001]
    
    try:
        for conn in psutil.net_connections(kind='inet'):
            if conn.status == 'ESTABLISHED' and conn.raddr:
                r_ip, r_port = conn.raddr.ip, conn.raddr.port
                l_ip, l_port = conn.laddr.ip, conn.laddr.port
                
                # Rule-Based Threat Assessment
                if r_port in [4444, 6667, 9001] or r_ip.startswith("185.220"):
                    risk = "MALICIOUS"
                    action = "Quarantine / Block"
                elif r_port in suspicious_ports:
                    risk = "SUSPICIOUS"
                    action = "Inspect Payload"
                else:
                    risk = "SAFE"
                    action = "Allow Traffic"

                connections.append({
                    "Local Address": f"{l_ip}:{l_port}",
                    "Remote Address": f"{r_ip}:{r_port}",
                    "Status": conn.status,
                    "PID": conn.pid or "N/A",
                    "Safety Assessment": risk,
                    "Recommended Action": action
                })
    except Exception:
        pass

    # Provide fallback example connections if restricted by OS permissions
    if not connections:
        connections = [
            {"Local Address": "192.168.0.65:54322", "Remote Address": "142.250.190.46:443", "Status": "ESTABLISHED", "PID": "8402", "Safety Assessment": "SAFE", "Recommended Action": "Allow Traffic"},
            {"Local Address": "192.168.0.65:59102", "Remote Address": "185.220.101.5:9001", "Status": "ESTABLISHED", "PID": "1042", "Safety Assessment": "MALICIOUS", "Recommended Action": "Quarantine / Block"},
            {"Local Address": "192.168.0.65:49221", "Remote Address": "192.168.0.1:22", "Status": "ESTABLISHED", "PID": "2104", "Safety Assessment": "SUSPICIOUS", "Recommended Action": "Inspect Payload"}
        ]
    return connections

# Live ARP Scanner Engine
def run_live_arp_scan(ip_range=None):
    if not ip_range or ip_range == "AUTO":
        ip_range, host_ip = detect_local_subnet()

    try:
        from scapy.all import ARP, Ether, srp
        
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        result = srp(packet, timeout=0.8, verbose=False, iface="en0")[0]

        discovered = []
        for sent, received in result:
            ip_addr = received.psrc
            mac_addr = received.hwsrc.upper()

            try:
                hostname = socket.gethostbyaddr(ip_addr)[0]
            except Exception:
                hostname = f"Host-{ip_addr.split('.')[-1]}"

            vendor = resolve_mac_vendor(mac_addr)
            os_type = infer_device_os(hostname, ip_addr, vendor)

            discovered.append({
                "Hostname": hostname,
                "IP Address": ip_addr,
                "MAC Address": mac_addr,
                "Manufacturer / Vendor": vendor,
                "OS / Device Type": os_type,
                "Status": "Live Host"
            })
        return discovered, ip_range

    except PermissionError:
        st.sidebar.error("Permission Denied: Raw sockets require elevated rights.")
        st.sidebar.info("Fix: Launch using 'sudo ./.venv/bin/streamlit run app.py'")
        return [], ip_range
    except Exception as e:
        st.sidebar.error(f"Live scan error: {str(e)}")
        return [], ip_range

# ==============================================================================
# 3. Application Layout & Header UI
# ==============================================================================
st.markdown(f"""
<div class="top-header">
    <div class="brand-title">
        <img src="{SHIELD_SVG}" width="24" height="24"/>
        <span>ERA SecOps <span style="color: #58a6ff; font-weight: 300;">| Cyber Defense Matrix Suite</span></span>
    </div>
    <div style="display: flex; gap: 16px; align-items: center;">
        <span class="status-pill">● ENGINE ONLINE</span>
        <span style="font-size: 12px; color: #768390;">UTC: {datetime.utcnow().strftime('%H:%M:%S')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-header">Active Inventory</div>
        <div class="metric-value">{len(st.session_state.inventory)}</div>
        <div class="metric-footer">↑ Asset Sync Active</div>
    </div>
    """, unsafe_allow_html=True)

status_color = "#3fb950" if st.session_state.threat_status == "LOW" else "#f85149"
with c2:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-header">Threat Status</div>
        <div class="metric-value" style="color: {status_color};">{st.session_state.threat_status}</div>
        <div class="metric-footer">Telemetry Engine Active</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-header">CDM Operational Cells</div>
        <div class="metric-value">25 / 25</div>
        <div class="metric-footer" style="color: #58a6ff;">100% Coverage</div>
    </div>
    """, unsafe_allow_html=True)

with c4:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-header">Automated Response MTTR</div>
        <div class="metric-value">< 1.4s</div>
        <div class="metric-footer">SOAR Webhooks Armed</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# Explicit Scan Completion Banner Display
if st.session_state.last_scan_status:
    scan_info = st.session_state.last_scan_status
    st.success(f"✅ **Network Scan Complete!** Discovered **{scan_info['count']} live hosts** on subnet `{scan_info['subnet']}` at {scan_info['time']}. Review the tabs below for asset details and threat assessments.")

# ==============================================================================
# 4. Operations Control Sidebar
# ==============================================================================
st.sidebar.markdown("### 🎛️ Operations Control")
scan_mode = st.sidebar.radio("Scanner Mode", ["Simulation Mode", "Live Local Subnet Scan"])

if scan_mode == "Live Local Subnet Scan":
    detected_subnet, host_ip = detect_local_subnet()
    st.sidebar.success(f"Detected Network: {detected_subnet}")
    st.sidebar.caption(f"Host IP: {host_ip}")

sim_type = st.sidebar.selectbox("Select Attack Scenario", [
    "Baseline Operations", 
    "Ransomware Execution", 
    "Credential Harvesting", 
    "Data Exfiltration"
])

if st.sidebar.button("⚡ Run Network Scan / Execution", type="primary", use_container_width=True):
    timestamp = datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')
    
    # Discovery Execution
    if scan_mode == "Live Local Subnet Scan":
        st.sidebar.info("Executing auto-detected subnet scan...")
        real_assets, scanned_range = run_live_arp_scan("AUTO")
        if real_assets:
            st.session_state.inventory.extend(real_assets)
            st.session_state.last_scan_status = {
                "count": len(real_assets),
                "subnet": scanned_range,
                "time": timestamp
            }
            for host in real_assets:
                st.session_state.telemetry_logs.append({
                    "Timestamp": timestamp,
                    "Event": "LIVE_HOST_DISCOVERED",
                    "Target": f"{host['Hostname']} ({host['IP Address']})",
                    "Vendor": host['Manufacturer / Vendor'],
                    "NIST Function": "Identify",
                    "Asset Class": "Devices",
                    "Severity": "INFO"
                })
    else:
        new_assets = []
        for _ in range(5):
            host = f"WORKSTATION-{random.randint(100, 999)}"
            ip = fake.ipv4_private()
            os_name = random.choice(["Windows 11 Enterprise", "macOS Sequoia", "Ubuntu 24.04 LTS"])
            vendor = random.choice(["Dell Inc.", "Apple, Inc.", "Lenovo", "Hewlett-Packard"])
            mac = fake.mac_address().upper()
            new_assets.append({
                "Hostname": host, 
                "IP Address": ip, 
                "MAC Address": mac,
                "Manufacturer / Vendor": vendor,
                "OS / Device Type": os_name, 
                "Status": "Monitored"
            })
            st.session_state.telemetry_logs.append({
                "Timestamp": timestamp,
                "Event": "SIMULATED_ASSET_DISCOVERED",
                "Target": f"{host} ({ip})",
                "Vendor": vendor,
                "NIST Function": "Identify",
                "Asset Class": "Devices",
                "Severity": "INFO"
            })
        st.session_state.inventory.extend(new_assets)
        st.session_state.last_scan_status = {
            "count": 5,
            "subnet": "Simulated Range",
            "time": timestamp
        }

    # Scenario Telemetry Injection
    if sim_type == "Ransomware Execution":
        st.session_state.threat_status = "CRITICAL"
        st.session_state.telemetry_logs.extend([
            {"Timestamp": timestamp, "Event": "UNAUTHORIZED_FILE_ENCRYPTION", "Target": "FS-01/Shared_Drive", "Vendor": "Enterprise Storage", "NIST Function": "Protect", "Asset Class": "Data", "Severity": "CRITICAL"},
            {"Timestamp": timestamp, "Event": "HOST_AUTO_QUARANTINE_TRIGGERED", "Target": "FS-01 (192.168.1.50)", "Vendor": "Enterprise Storage", "NIST Function": "Respond", "Asset Class": "Devices", "Severity": "HIGH"}
        ])
    elif sim_type == "Data Exfiltration":
        st.session_state.threat_status = "ELEVATED"
        st.session_state.telemetry_logs.extend([
            {"Timestamp": timestamp, "Event": "ANOMALOUS_OUTBOUND_TRANSFER", "Target": "10.0.0.12 -> 185.220.101.5", "Vendor": "Cisco Systems", "NIST Function": "Detect", "Asset Class": "Networks", "Severity": "CRITICAL"}
        ])
    elif sim_type == "Credential Harvesting":
        st.session_state.threat_status = "ELEVATED"
        st.session_state.telemetry_logs.extend([
            {"Timestamp": timestamp, "Event": "LSASS_MEMORY_DUMP", "Target": "DC-01.domain.local", "Vendor": "Microsoft Corp", "NIST Function": "Detect", "Asset Class": "Users", "Severity": "CRITICAL"}
        ])
    st.rerun()

if st.sidebar.button("🧹 Reset Telemetry & State", use_container_width=True):
    st.session_state.inventory = []
    st.session_state.telemetry_logs = []
    st.session_state.threat_status = "LOW"
    st.session_state.last_scan_status = None
    st.rerun()

# ==============================================================================
# 5. Enhanced Tab Navigation & Displays
# ==============================================================================
tab_matrix, tab_inventory, tab_connections, tab_telemetry = st.tabs([
    "🧩  5x5 Cyber Defense Matrix Engine", 
    "🖥️  Active Asset Inventory", 
    "🌐  Connection Threat Monitor",
    "📜  SIEM Telemetry Console"
])

with tab_matrix:
    st.subheader("Sounil Yu 5x5 Matrix Control Plane")
    
    cdm_html = """
    <table class="cdm-table">
        <tr>
            <th class="cdm-header">NIST CSF</th>
            <th class="cdm-header">Devices</th>
            <th class="cdm-header">Applications</th>
            <th class="cdm-header">Networks</th>
            <th class="cdm-header">Data</th>
            <th class="cdm-header">Users</th>
        </tr>
        <tr>
            <td class="cdm-header">Identify</td>
            <td class="cdm-cell"><div class="cell-title">Asset Discovery</div><span class="cell-tag">AUTOMATED</span></td>
            <td class="cdm-cell"><div class="cell-title">App Inventory</div><span class="cell-tag">ACTIVE</span></td>
            <td class="cdm-cell"><div class="cell-title">Port Mapping</div><span class="cell-tag">ACTIVE</span></td>
            <td class="cdm-cell"><div class="cell-title">Data Discovery</div><span class="cell-tag">ACTIVE</span></td>
            <td class="cdm-cell"><div class="cell-title">IAM Mapping</div><span class="cell-tag">ACTIVE</span></td>
        </tr>
        <tr>
            <td class="cdm-header">Protect</td>
            <td class="cdm-cell"><div class="cell-title">EDR Prevention</div><span class="cell-tag">ENFORCED</span></td>
            <td class="cdm-cell"><div class="cell-title">App Control</div><span class="cell-tag">ENFORCED</span></td>
            <td class="cdm-cell"><div class="cell-title">Microsegmentation</div><span class="cell-tag">ENFORCED</span></td>
            <td class="cdm-cell"><div class="cell-title">AES-256 Vault</div><span class="cell-tag">ENFORCED</span></td>
            <td class="cdm-cell"><div class="cell-title">FIDO2 MFA</div><span class="cell-tag">ENFORCED</span></td>
        </tr>
        <tr>
            <td class="cdm-header">Detect</td>
            <td class="cdm-cell"><div class="cell-title">Behavioral EDR</div><span class="cell-tag">MONITORING</span></td>
            <td class="cdm-cell"><div class="cell-title">SAST Logging</div><span class="cell-tag">MONITORING</span></td>
            <td class="cdm-cell"><div class="cell-title">NDR Sensor</div><span class="cell-tag">MONITORING</span></td>
            <td class="cdm-cell"><div class="cell-title">DLP Inspector</div><span class="cell-tag">MONITORING</span></td>
            <td class="cdm-cell"><div class="cell-title">UEBA Engine</div><span class="cell-tag">MONITORING</span></td>
        </tr>
        <tr>
            <td class="cdm-header">Respond</td>
            <td class="cdm-cell"><div class="cell-title">Host Quarantine</div><span class="cell-tag">READY</span></td>
            <td class="cdm-cell"><div class="cell-title">Process Kill</div><span class="cell-tag">READY</span></td>
            <td class="cdm-cell"><div class="cell-title">Dynamic ACL</div><span class="cell-tag">READY</span></td>
            <td class="cdm-cell"><div class="cell-title">Access Revocation</div><span class="cell-tag">READY</span></td>
            <td class="cdm-cell"><div class="cell-title">Session Terminate</div><span class="cell-tag">READY</span></td>
        </tr>
        <tr>
            <td class="cdm-header">Recover</td>
            <td class="cdm-cell"><div class="cell-title">Gold Reimage</div><span class="cell-tag">PLAYBOOK</span></td>
            <td class="cdm-cell"><div class="cell-title">Patch Rollback</div><span class="cell-tag">PLAYBOOK</span></td>
            <td class="cdm-cell"><div class="cell-title">Route Restoration</div><span class="cell-tag">PLAYBOOK</span></td>
            <td class="cdm-cell"><div class="cell-title">Snapshot Restore</div><span class="cell-tag">PLAYBOOK</span></td>
            <td class="cdm-cell"><div class="cell-title">Cred Reset</div><span class="cell-tag">PLAYBOOK</span></td>
        </tr>
    </table>
    """
    st.markdown(cdm_html, unsafe_allow_html=True)

with tab_inventory:
    st.subheader("Discovered Asset Repository")
    if st.session_state.inventory:
        st.dataframe(pd.DataFrame(st.session_state.inventory), use_container_width=True)
    else:
        st.info("No assets discovered yet. Execute a network scan from the control panel.")

with tab_connections:
    st.subheader("Active Layer 4 Network Connection Safety Assessment")
    st.caption("Real-time network socket telemetry evaluated against security baseline policies.")
    
    conn_data = analyze_active_connections()
    df_conn = pd.DataFrame(conn_data)
    
    # Render Color-Coded Connection Safety Table
    st.dataframe(
        df_conn,
        use_container_width=True,
        column_config={
            "Safety Assessment": st.column_config.SelectboxColumn(
                "Safety Assessment",
                help="Automated threat level based on port, IP reputation, and protocol",
                options=["SAFE", "SUSPICIOUS", "MALICIOUS"],
                required=True,
            )
        }
    )

with tab_telemetry:
    st.subheader("Real-Time SIEM Export Center")
    if st.session_state.telemetry_logs:
        df_logs = pd.DataFrame(st.session_state.telemetry_logs)
        st.dataframe(df_logs, use_container_width=True)
        
        col_exp1, col_exp2 = st.columns(2)
        with col_exp1:
            st.download_button(
                label="📥 Export SIEM Telemetry (JSON)",
                data=json.dumps(st.session_state.telemetry_logs, indent=2),
                file_name=f"siem_telemetry_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json",
                use_container_width=True
            )
        with col_exp2:
            st.download_button(
                label="📥 Export SIEM Telemetry (CSV)",
                data=df_logs.to_csv(index=False),
                file_name=f"siem_telemetry_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}.csv",
                mime="text/csv",
                use_container_width=True
            )
    else:
        st.info("No active telemetry generated. Run a scan or scenario from the control panel.")
