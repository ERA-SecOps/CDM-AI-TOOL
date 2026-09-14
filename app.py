import streamlit as st
import pandas as pd
from faker import Faker
import random
import json
import base64
from datetime import datetime

# 1. Page Configuration (Must be the first Streamlit command)
st.set_page_config(
    page_title="ERA SecOps | Cyber Defense Matrix Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 2. Inject CSS Theme & Header Suppressor
st.markdown("""
<style>
    /* Completely Hide Streamlit Top Header Bar & White Stripe */
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

    /* Dark Theme Base */
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

    /* Top Command Header */
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

    /* Enterprise Metric Cards */
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

    /* Custom Matrix Display Table */
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

# Helper: Inline SVG to Base64
def svg_to_base64(svg_str):
    return f"data:image/svg+xml;base64,{base64.b64encode(svg_str.encode('utf-8')).decode('utf-8')}"

SHIELD_SVG = svg_to_base64('<svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#58a6ff" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/></svg>')

# State Management
if "inventory" not in st.session_state:
    st.session_state.inventory = []
if "telemetry_logs" not in st.session_state:
    st.session_state.telemetry_logs = []

fake = Faker()

# Top Command Header
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

# Top KPI Metrics Row
c1, c2, c3, c4 = st.columns(4)
with c1:
    st.markdown(f"""
    <div class="metric-container">
        <div class="metric-header">Active Inventory</div>
        <div class="metric-value">{len(st.session_state.inventory)}</div>
        <div class="metric-footer">↑ Asset Sync Active</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown("""
    <div class="metric-container">
        <div class="metric-header">Threat Status</div>
        <div class="metric-value" style="color: #3fb950;">LOW</div>
        <div class="metric-footer">Zero Critical Alerts</div>
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

# Sidebar Controls
st.sidebar.markdown("### 🎛️ Operations Control")
sim_type = st.sidebar.selectbox("Select Attack Scenario", ["Baseline Operations", "Ransomware Execution", "Credential Harvesting", "Data Exfiltration"])

if st.sidebar.button("⚡ Run AI Discovery Scan", type="primary", use_container_width=True):
    new_assets = []
    for _ in range(5):
        host = f"WORKSTATION-{random.randint(100, 999)}"
        ip = fake.ipv4_private()
        os_name = random.choice(["Windows 11 Enterprise", "macOS Sequoia", "Ubuntu 24.04 LTS"])
        new_assets.append({"Hostname": host, "IP Address": ip, "OS": os_name, "Status": "Monitored"})
        
        # Telemetry Log Generation
        st.session_state.telemetry_logs.append({
            "Timestamp": datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S'),
            "Event": "ASSET_DISCOVERED",
            "Target": f"{host} ({ip})",
            "NIST Function": "Identify",
            "Asset Class": "Devices",
            "Severity": "INFO"
        })
    st.session_state.inventory.extend(new_assets)
    st.sidebar.success("Discovered 5 new devices!")

if st.sidebar.button("🧹 Reset Telemetry", use_container_width=True):
    st.session_state.inventory = []
    st.session_state.telemetry_logs = []
    st.rerun()

# Main Grid & Telemetry Tabs
tab_matrix, tab_telemetry = st.tabs(["🧩 5x5 Cyber Defense Matrix Engine", "📜 SIEM Telemetry Console"])

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
        st.info("No active telemetry generated. Run an AI Discovery Scan from the left sidebar.")