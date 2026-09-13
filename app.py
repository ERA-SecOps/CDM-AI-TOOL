import streamlit as st
import pandas as pd
import random
from faker import Faker

fake = Faker()

st.set_page_config(page_title="CDM AI Automation Lab", layout="wide")
st.title("🛡️ Cyber Defense Matrix: AI Automation Lab")

# --- SESSION STATE INITIALIZATION ---
state_keys = [
    'inventory', 'blocked_ips', 'app_protect', 'net_protect', 
    'data_protect', 'user_protect', 'app_detect', 'net_detect', 
    'data_detect', 'user_detect', 'data_recover', 'device_recover'
]

for key in state_keys:
    if key not in st.session_state:
        if key in ['inventory', 'blocked_ips']:
            st.session_state[key] = []
        else:
            st.session_state[key] = False

# --- 1. IDENTIFY FUNCTION ---
st.header("1. Identify Column: Automated Asset Discovery")
col1, col2 = st.columns(2)

with col1:
    if st.button("🚀 Run AI-Powered Network Scan"):
        new_assets = []
        for _ in range(5):
            new_assets.append({
                "Asset Type": "Device",
                "Hostname": f"WKSTN-{random.randint(1000, 9999)}",
                "IP Address": fake.ipv4(),
                "OS": random.choice(["macOS", "Windows 11", "Ubuntu 22.04"]),
                "Discovery Method": "AI Pattern Matching"
            })
        st.session_state.inventory = new_assets
        st.success("Scan Complete! AI identified 5 new devices.")

with col2:
    if st.button("🗑️ Reset Environment"):
        for key in state_keys:
            if key in ['inventory', 'blocked_ips']:
                st.session_state[key] = []
            else:
                st.session_state[key] = False

if st.session_state.inventory:
    st.subheader("Current Asset Inventory")
    st.table(pd.DataFrame(st.session_state.inventory))

# --- 2. PROTECT CONTROLS ---
st.header("2. Protect Column: Security Controls")
p_col1, p_col2, p_col3, p_col4 = st.columns(4)

with p_col1:
    if st.button("🔒 App Whitelisting"):
        st.session_state.app_protect = True
        st.success("App Control enforced.")

with p_col2:
    if st.button("🛡️ Network Microsegmentation"):
        st.session_state.net_protect = True
        st.success("Zero Trust ACLs deployed.")

with p_col3:
    if st.button("🔑 Enable Data Encryption"):
        st.session_state.data_protect = True
        st.success("AES-256 BitLocker/FileVault active.")

with p_col4:
    if st.button("👤 Enforce MFA & PAM"):
        st.session_state.user_protect = True
        st.success("FIDO2 Multi-Factor required.")

# --- 3. DETECT CONTROLS ---
st.header("3. Detect Column: Telemetry & Monitoring")
d_col1, d_col2, d_col3, d_col4 = st.columns(4)

with d_col1:
    if st.button("🔍 App SIEM Logging"):
        st.session_state.app_detect = True
        st.info("App telemetry active.")

with d_col2:
    if st.button("📡 Network IDS Engine"):
        st.session_state.net_detect = True
        st.info("Suricata/Zeek active.")

with d_col3:
    if st.button("💾 DLP Data Scanning"):
        st.session_state.data_detect = True
        st.info("DLP monitoring sensitive data.")

with d_col4:
    if st.button("🚨 User Anomaly Analytics"):
        st.session_state.user_detect = True
        st.info("UEBA tracking abnormal logins.")

# --- 4. RESPOND FUNCTION ---
st.header("4. Respond Column: Automated Threat Containment")

if st.session_state.inventory:
    target_device = st.session_state.inventory[0]
    st.warning(f"⚠️ Simulated Malicious Traffic Detected from: **{target_device['Hostname']}** ({target_device['IP Address']})")
    
    if st.button("⚡ Execute AI Auto-Isolation Script"):
        if target_device['IP Address'] not in st.session_state.blocked_ips:
            st.session_state.blocked_ips.append(target_device['IP Address'])
        st.success(f"Generated firewall rule: `iptables -A INPUT -s {target_device['IP Address']} -j DROP`. Device isolated.")

if st.session_state.blocked_ips:
    st.subheader("Active Firewall Isolation Rules")
    blocked_df = pd.DataFrame({"Blocked IP Address": st.session_state.blocked_ips, "Action": "INPUT DROP"})
    st.table(blocked_df)

# --- 5. RECOVER FUNCTION ---
st.header("5. Recover Column: Automated Remediation")
r_col1, r_col2 = st.columns(2)

with r_col1:
    if st.button("💾 Trigger Immutable Data Restore"):
        st.session_state.data_recover = True
        st.success("Data Recovery: Volume shadow copy snapshot restored.")

with r_col2:
    if st.button("🔄 Reimage Isolated Device"):
        st.session_state.device_recover = True
        st.success("Device Recovery: Golden image deployed to target workstation.")

# --- 6. MATRIX COVERAGE GRID ---
st.header("6. Cyber Defense Matrix Coverage")
assets = ["Devices", "Applications", "Networks", "Data", "Users"]
functions = ["Identify", "Protect", "Detect", "Respond", "Recover"]

matrix_df = pd.DataFrame("⚪ Empty", index=assets, columns=functions)

# Dynamic mapping of session states to matrix cells
cell_mappings = {
    ("Devices", "Identify"): bool(st.session_state.inventory),
    ("Devices", "Respond"): bool(st.session_state.blocked_ips),
    ("Devices", "Recover"): st.session_state.device_recover,
    ("Applications", "Protect"): st.session_state.app_protect,
    ("Applications", "Detect"): st.session_state.app_detect,
    ("Networks", "Protect"): st.session_state.net_protect,
    ("Networks", "Detect"): st.session_state.net_detect,
    ("Data", "Protect"): st.session_state.data_protect,
    ("Data", "Detect"): st.session_state.data_detect,
    ("Data", "Recover"): st.session_state.data_recover,
    ("Users", "Protect"): st.session_state.user_protect,
    ("Users", "Detect"): st.session_state.user_detect,
}

for (asset, func), is_active in cell_mappings.items():
    if is_active:
        matrix_df.at[asset, func] = "🔵 AI ACTIVE"

def highlight_ai(val):
    if 'ACTIVE' in str(val):
        return 'background-color: #1f77b4; color: white; font-weight: bold'
    return ''

st.table(matrix_df.style.map(highlight_ai))