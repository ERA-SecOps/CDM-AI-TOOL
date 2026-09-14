import streamlit as st
import pandas as pd
from faker import Faker
import random
import json
import base64
import socket
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

    /* Dark Mode Theme */
    .stApp {
        background-color: #090d16;
        color: #adbac7;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    }
    
    /* Dark Theme Sidebar Target */
    [data-testid="stSidebar"] {
        background-color: #111622 !important;
        border-right: 1px solid #1c212e;
    }
    [data-testid="stSidebar"] * {
        color: #adbac7 !important;
    }

    /* Custom Command Header Bar */
    .top-header {
        display: flex;
        justify-content: space-between;
        align-items: center;
        background-color: #111622;
        padding: 12px 24px;
        border-radius: 8px;
        border: 1px solid #1c212e;
        margin-bottom: 20px;
    }
    .brand-title {
        font-size: 20px;
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
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
    }

    /* Metric Cards */
    .metric-container {
        background-color: #111622;
        border: 1px solid #1c212e;
        border-radius: 8px;
        padding: 16px;
        position: relative;
    }
    .metric-header {
        font-size: 11px;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #768390;
        margin-bottom: 8px;
    }
    .metric-value {
        font-size: 28px;
        font-weight: 700;
        color: #f0f6fc;
    }
    .metric-footer {
        font-size: 12px;
        color: #57ab5a;
        margin-top: 6px;
    }

    /* 5x5 Matrix Display Table */
    .cdm-table {
        width: 100%;
        border-collapse: separate;
        border-spacing: 6px;
        margin-top: 10px;
    }
    .cdm-header {
        background-color: #161b26;
        color: #768390;
        padding: 12px;
        font-size: 12px;
        text-transform: uppercase;
        border-radius: 4px;
        text-align: center;
    }
    .cdm-cell {
        background-color: #111622;
        border: 1px solid #1c212e;
        padding: 12px;
        border-radius: 6px;
        font-size: 12px;
        color: #adbac7;
        transition: all 0.2s ease;
    }
    .cdm-cell:hover {
        border-color: #316dca;
        background-color: #161c2e;
    }
    .cell-title {
        font-weight: 600;
        color: #f0f6fc;
        margin-bottom: 4px;
    }
    .cell-tag {
        font-size: 10px;
        color: #3fb950;
        background: rgba(63, 185, 80, 0.1);
        padding: 2px 6px;
        border-radius: 4px;
        display: inline-block;
    }

    #MainMenu, footer { visibility: hidden; }
</style>
""", unsafe_allow_html=True)

# ==============================================================================
# 2. Helper Functions & Session State Initialization
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

fake = Faker()

# Automatic Local Network Interface & Subnet Discovery
def detect_local_subnet():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.settimeout(0.5)
        # Connect to public DNS to determine default outbound route IP
        s.connect(("8.8.8.8", 80))
        local_ip = s.getsockname()[0]
        s.close()
        # Extract the network segment (assumes standard /24 subnet mask)
        ip_parts = local_ip.split('.')
        subnet = f"{ip_parts[0]}.{ip_parts[1]}.{ip_parts[2]}.0/24"
        return subnet, local_ip
    except Exception:
        return "192.168.0.0/24", "127.0.0.1"

# Out-Of-The-Box Live Local ARP Scanner Engine
def run_live_arp_scan(ip_range=None):
    if not ip_range or ip_range == "AUTO":
        ip_range, host_ip = detect_local_subnet()

    try:
        from scapy.all import ARP, Ether, srp
        
        # Build ARP Broadcast Frame
        arp = ARP(pdst=ip_range)
        ether = Ether(dst="ff:ff:ff:ff:ff:ff")
        packet = ether / arp

        # Fast sweep with timeout=0.8s
        result = srp(packet, timeout=0.8, verbose=False, iface="en0")[0]

        discovered = []
        for sent, received in result:
            try:
                hostname = socket.gethostbyaddr(received.psrc)[0]
            except Exception:
                hostname = "Network Device"

            discovered.append({
                "Hostname": hostname,
                "IP Address": received.psrc,
                "OS": f"MAC: {received.hwsrc}",
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
            st.sidebar.success(f"Discovered {len(real_assets)} live hosts on {scanned_range}!")
            for host in real_assets:
                st.session_state.telemetry_logs.append({
                    "Timestamp": timestamp,
                    "Event": "LIVE_HOST_DISCOVERED",
                    "Target": f"{host['Hostname']} ({host['IP Address']})",
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
            new_assets.append({"Hostname": host, "IP Address": ip, "OS": os_name, "Status": "Monitored"})
            st.session_state.telemetry_logs.append({
                "Timestamp": timestamp,
                "Event": "SIMULATED_ASSET_DISCOVERED",
                "Target": f"{host} ({ip})",
                "NIST Function": "Identify",
                "Asset Class": "Devices",
                "Severity": "INFO"
            })
        st.session_state.inventory.extend(new_assets)
        st.sidebar.success("Discovered 5 simulated assets!")

    # Scenario Telemetry Injection
    if sim_type == "Ransomware Execution":
        st.session_state.threat_status = "CRITICAL"
        st.session_state.telemetry_logs.extend([
            {"Timestamp": timestamp, "Event": "UNAUTHORIZED_FILE_ENCRYPTION", "Target": "FS-01/Shared_Drive", "NIST Function": "Protect", "Asset Class": "Data", "Severity": "CRITICAL"},
            {"Timestamp": timestamp, "Event": "HOST_AUTO_QUARANTINE_TRIGGERED", "Target": "FS-01 (192.168.1.50)", "NIST Function": "Respond", "Asset Class": "Devices", "Severity": "HIGH"}
        ])
    elif sim_type == "Data Exfiltration":
        st.session_state.threat_status = "ELEVATED"
        st.session_state.telemetry_logs.extend([
            {"Timestamp": timestamp, "Event": "ANOMALOUS_OUTBOUND_TRANSFER", "Target": "10.0.0.12 -> 185.220.101.5", "NIST Function": "Detect", "Asset Class": "Networks", "Severity": "CRITICAL"}
        ])
    elif sim_type == "Credential Harvesting":
        st.session_state.threat_status = "ELEVATED"
        st.session_state.telemetry_logs.extend([
            {"Timestamp": timestamp, "Event": "LSASS_MEMORY_DUMP", "Target": "DC-01.domain.local", "NIST Function": "Detect", "Asset Class": "Users", "Severity": "CRITICAL"}
        ])

if st.sidebar.button("🧹 Reset Telemetry & State", use_container_width=True):
    st.session_state.inventory = []
    st.session_state.telemetry_logs = []
    st.session_state.threat_status = "LOW"
    st.rerun()

# ==============================================================================
# 5. Tab Views (Matrix, Inventory, Telemetry)
# ==============================================================================
tab_matrix, tab_inventory, tab_telemetry = st.tabs([
    "🧩 5x5 Cyber Defense Matrix Engine", 
    "🖥️ Active Asset Inventory", 
    "📜 SIEM Telemetry Console"
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