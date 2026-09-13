import streamlit as st
import pandas as pd
import random
from faker import Faker

fake = Faker()

st.set_page_config(page_title="CDM AI Automation Lab", layout="wide")
st.title("🛡️ Cyber Defense Matrix: AI Automation Lab")

# --- SESSION STATE INITIALIZATION ---
if 'inventory' not in st.session_state:
    st.session_state.inventory = []
if 'blocked_ips' not in st.session_state:
    st.session_state.blocked_ips = []

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
    if st.button("🗑️ Clear Inventory"):
        st.session_state.inventory = []
        st.session_state.blocked_ips = []

if st.session_state.inventory:
    st.subheader("Current Asset Inventory")
    st.table(pd.DataFrame(st.session_state.inventory))

# --- 2. RESPOND FUNCTION ---
st.header("2. Respond Column: Automated Threat Containment")

if st.session_state.inventory:
    target_device = st.session_state.inventory[0]
    st.warning(f"⚠️ Simulated Malicious Traffic Detected from: **{target_device['Hostname']}** ({target_device['IP Address']})")
    
    if st.button("⚡ Execute AI Auto-Isolation Script"):
        st.session_state.blocked_ips.append(target_device['IP Address'])
        st.success(f"Generated firewall rule: `iptables -A INPUT -s {target_device['IP Address']} -j DROP`. Device isolated.")

if st.session_state.blocked_ips:
    st.subheader("Active Firewall Isolation Rules")
    st.table(matrix_df.style.map(highlight_ai))

# --- 3. MATRIX COVERAGE GRID ---
st.header("3. Cyber Defense Matrix Coverage")
assets = ["Devices", "Applications", "Networks", "Data", "Users"]
functions = ["Identify", "Protect", "Detect", "Respond", "Recover"]

matrix_df = pd.DataFrame("⚪ Empty", index=assets, columns=functions)

# Update cell statuses based on action
if st.session_state.inventory:
    matrix_df.at["Devices", "Identify"] = "🔵 AI ACTIVE"
if st.session_state.blocked_ips:
    matrix_df.at["Devices", "Respond"] = "🔵 AI ACTIVE"

# Updated styling function using map() instead of applymap()
def highlight_ai(val):
    if 'ACTIVE' in str(val):
        return 'background-color: #1f77b4; color: white; font-weight: bold'
    return ''

st.table(matrix_df.style.map(highlight_ai))