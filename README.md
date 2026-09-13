# 🛡️ Cyber Defense Matrix (CDM) AI Automation Lab

An interactive, state-driven security simulation engine built with **Python**, **Streamlit**, and **Pandas**. This tool models automated security controls across all 25 cells of Sounil Yu’s **Cyber Defense Matrix (CDM)**, mapping NIST Cybersecurity Framework (CSF) functions against core enterprise asset classes.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.10%2B-brightgreen.svg)
![Streamlit](https://img.shields.io/badge/streamlit-1.30%2B-ff4b4b.svg)

---

## 📌 Executive Summary

The **Cyber Defense Matrix AI Automation Lab** translates abstract security frameworks into an operational, interactive dashboard. By simulating endpoint discovery, policy enforcement, SIEM/IDS telemetry ingestion, automated threat containment, and disaster recovery workflows, the tool illustrates how automation and AI reduce MTTR (Mean Time to Respond) across heterogeneous asset ecosystems.

---

## 📐 Framework Alignment

The application strictly maps actions across the 5x5 Cyber Defense Matrix:

| Asset / Function | Identify | Protect | Detect | Respond | Recover |
| :--- | :---: | :---: | :---: | :---: | :---: |
| **Devices** | 🔵 AI Discovery Scan | ⚪ | ⚪ | 🔵 Auto IP Isolation | 🔵 Golden Image Reimage |
| **Applications** | ⚪ | 🔵 App Whitelisting | 🔵 SIEM Audit Logging | ⚪ | ⚪ |
| **Networks** | ⚪ | 🔵 Microsegmentation | 🔵 Suricata/Zeek IDS | ⚪ | ⚪ |
| **Data** | ⚪ | 🔵 AES-256 Encryption | 🔵 DLP Scanning | ⚪ | 🔵 Snapshot Restore |
| **Users** | ⚪ | 🔵 FIDO2 MFA / PAM | 🔵 UEBA Analytics | ⚪ | ⚪ |

---

## ✨ Key Features

* **Automated Asset Discovery (Identify):** Generates synthetic host telemetry (`Faker`), scanning network segments to inventory devices, operating systems, and IP addresses.
* **Zero Trust & App Control (Protect):** Simulates microsegmentation ACL deployments, executable whitelisting (AppLocker/macOS execution policy), full-disk encryption, and identity enforcement (MFA/PAM).
* **Multi-Layer Telemetry (Detect):** Streams mock log data across application audit trails, network IDS signatures, DLP inspection, and User and Entity Behavior Analytics (UEBA).
* **Automated Response (Respond):** Executes real-time threat containment scripts, dynamically generating and staging host-based firewall isolation rules (`iptables DROP`).
* **Resilience & Business Continuity (Recover):** Demonstrates automated snapshot restoration for immutable data storage and host reimaging for compromised devices.
* **Dynamic Grid Visualization:** Tracks security posture in real time using a styled, state-aware Matrix rendering engine.

---

## 🛠️ Tech Stack & Dependencies

* **Language:** Python 3.10+
* **Frontend Framework:** [Streamlit](https://streamlit.io/)
* **Data Processing:** Pandas
* **Synthetic Telemetry Generation:** Faker, Random

---

## 🚀 Quickstart Guide

### Prerequisites
* Python 3.10 or higher
* Git

### Local Setup

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/ERA-SecOps/cdm-ai-tool.git](https://github.com/ERA-SecOps/cdm-ai-tool.git)
   cd cdm-ai-tool