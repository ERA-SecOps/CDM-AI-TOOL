# 🛡️ Cyber Defense Matrix (CDM) AI Automation Lab

An interactive, open-source security engineering lab that bridges Sounil Yu’s 5x5 **Cyber Defense Matrix** with automated SecOps workflows. 

This tool provides real-time local network scanning, synthetic endpoint telemetry generation, and OS-native threat containment payload creation.

---

## ⚡ Key Features

- **Dual-Mode Operation:**
  - **Simulation Mode:** Generates synthetic endpoint data for cloud demos and educational testing without touching network interfaces.
  - **Live Network Mode:** Executes Layer 2 ARP discovery via `scapy` to map live endpoints across local subnets.
- **Automated Containment Engine:** Generates OS-native firewall containment rules (`pfctl` for macOS, `iptables` for Linux) to isolate flagged assets.
- **Interactive Matrix Grid:** Dynamically tracks operational coverage across the 5x5 Cyber Defense Matrix (Assets $\times$ Functions).

---

## 🚀 Quick Start

### 1. Download & One-Click Launch

- **macOS / Linux:** Double-click `Run-CDM-Lab.command`
- **Windows:** Double-click `Run-CDM-Lab.bat`

### 2. Manual Terminal Launch

```bash
# Clone the repository
git clone [https://github.com/your-username/cdm-ai-tool.git](https://github.com/your-username/cdm-ai-tool.git)
cd cdm-ai-tool

# Set up virtual environment & dependencies
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Launch Streamlit
streamlit run app.py