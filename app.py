import streamlit as st
import pandas as pd
from faker import Faker
import random
import json
import base64
import socket
import psutil
import ipaddress
import platform
from datetime import datetime, timezone


# ==============================================================================
# 1. PAGE CONFIGURATION
# ==============================================================================

st.set_page_config(
    page_title="ERA SecOps | Enterprise Cyber Defense Matrix Platform",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ==============================================================================
# 2. CUSTOM CSS
# ==============================================================================

st.markdown(
    """
<style>

header[data-testid="stHeader"] {
    display: none !important;
}

div[data-testid="stDecoration"] {
    display: none !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 2rem !important;
}

.stApp {
    background-color: #0b0e14;
    color: #adbac7;
    font-family:
        -apple-system,
        BlinkMacSystemFont,
        "Segoe UI",
        Roboto,
        Helvetica,
        Arial,
        sans-serif;
}

[data-testid="stSidebar"] {
    background-color: #121824 !important;
    border-right: 1px solid #1e2638;
}

[data-testid="stSidebar"] * {
    color: #adbac7 !important;
}

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

.scan-complete {
    background: linear-gradient(
        135deg,
        rgba(46,160,67,0.15),
        rgba(31,107,235,0.10)
    );
    border: 1px solid #2ea043;
    border-radius: 10px;
    padding: 18px 22px;
    margin: 12px 0 20px 0;
}

.scan-complete-title {
    color: #3fb950;
    font-size: 18px;
    font-weight: 700;
    margin-bottom: 8px;
}

.scan-complete-text {
    color: #adbac7;
    font-size: 14px;
}

.scan-complete-time {
    color: #768390;
    font-size: 12px;
    margin-top: 6px;
}

.scan-panel {
    background-color: #121824;
    border: 1px solid #1e2638;
    border-radius: 10px;
    padding: 18px;
    margin: 10px 0 20px 0;
}

#MainMenu,
footer {
    visibility: hidden;
}

</style>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 3. HELPERS
# ==============================================================================

def utc_now_string():
    return datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%S")


def svg_to_base64(svg_str):
    return (
        "data:image/svg+xml;base64,"
        + base64.b64encode(svg_str.encode("utf-8")).decode("utf-8")
    )


SHIELD_SVG = svg_to_base64(
    """
    <svg xmlns="http://www.w3.org/2000/svg"
         width="24" height="24"
         viewBox="0 0 24 24"
         fill="none"
         stroke="#58a6ff"
         stroke-width="2"
         stroke-linecap="round"
         stroke-linejoin="round">
        <path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"/>
    </svg>
    """
)


# ==============================================================================
# 4. SESSION STATE
# ==============================================================================

if "inventory" not in st.session_state:
    st.session_state.inventory = []

if "telemetry_logs" not in st.session_state:
    st.session_state.telemetry_logs = []

if "threat_status" not in st.session_state:
    st.session_state.threat_status = "LOW"

if "last_scan_status" not in st.session_state:
    st.session_state.last_scan_status = None

if "scan_running" not in st.session_state:
    st.session_state.scan_running = False

if "scan_error" not in st.session_state:
    st.session_state.scan_error = None


fake = Faker()


# ==============================================================================
# 5. NETWORK DISCOVERY
# ==============================================================================

def detect_local_subnet():
    """
    Attempts to determine the local IPv4 address and /24 network.

    This does not require a hard-coded network interface.
    """

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        sock.settimeout(1.0)
        sock.connect(("8.8.8.8", 80))

        local_ip = sock.getsockname()[0]

        network = ipaddress.ip_network(
            f"{local_ip}/24",
            strict=False
        )

        return str(network), local_ip

    except Exception:
        return "192.168.1.0/24", "127.0.0.1"

    finally:
        sock.close()


# ==============================================================================
# 6. MAC VENDOR LOOKUP
# ==============================================================================

def resolve_mac_vendor(mac_address):
    mac_clean = (
        mac_address
        .replace(":", "")
        .replace("-", "")
        .upper()
    )

    static_oui = {
        "3C22FB": "Apple, Inc.",
        "F4D488": "Apple, Inc.",
        "0014D1": "TRENDnet / Router",
        "E45F01": "Raspberry Pi Foundation",
        "000C29": "VMware, Inc.",
        "080027": "Oracle VirtualBox",
        "B827EB": "Raspberry Pi Foundation",
        "DCA632": "Raspberry Pi Trading",
    }

    prefix = mac_clean[:6]

    if prefix in static_oui:
        return static_oui[prefix]

    return "Unknown / Network Hardware"


# ==============================================================================
# 7. DEVICE / OS FINGERPRINT
# ==============================================================================

def infer_device_os(hostname, ip, vendor):
    vendor_lower = vendor.lower()
    host_lower = hostname.lower()

    if ip.endswith(".1"):
        return "Embedded Linux Gateway"

    if (
        "apple" in vendor_lower
        or "macbook" in host_lower
        or "iphone" in host_lower
    ):
        return "macOS / iOS Device"

    if "raspberry" in vendor_lower:
        return "Raspberry Pi OS / Linux"

    if (
        "vmware" in vendor_lower
        or "virtualbox" in vendor_lower
    ):
        return "Virtual Machine Guest"

    if (
        "amazon" in vendor_lower
        or "google" in vendor_lower
        or "nest" in host_lower
    ):
        return "Smart IoT Appliance"

    if (
        "intel" in vendor_lower
        or "realtek" in vendor_lower
    ):
        return "Windows / Linux Workstation"

    return "Generic Network Appliance"


# ==============================================================================
# 8. LIVE ARP SCANNER
# ==============================================================================

def run_live_arp_scan(
    ip_range=None,
    progress_bar=None,
    status_box=None,
):
    """
    Performs a local ARP discovery scan.

    Returns:
        discovered_devices, scanned_network
    """

    if not ip_range or ip_range == "AUTO":
        ip_range, host_ip = detect_local_subnet()

    discovered = []

    try:
        from scapy.all import ARP, Ether, srp

    except ImportError:
        message = (
            "Scapy is not installed. Install it with: "
            "pip install scapy"
        )

        if status_box:
            status_box.error(f"❌ {message}")

        return [], ip_range

    try:

        if status_box:
            status_box.info(
                f"🔎 Initializing ARP discovery on `{ip_range}`..."
            )

        if progress_bar:
            progress_bar.progress(5)

        arp = ARP(pdst=ip_range)

        ether = Ether(
            dst="ff:ff:ff:ff:ff:ff"
        )

        packet = ether / arp

        if status_box:
            status_box.info(
                f"📡 Broadcasting ARP discovery across `{ip_range}`..."
            )

        if progress_bar:
            progress_bar.progress(15)

        result = srp(
            packet,
            timeout=2,
            verbose=False
        )[0]

        if progress_bar:
            progress_bar.progress(30)

        total = len(result)

        if total == 0:

            if progress_bar:
                progress_bar.progress(100)

            if status_box:
                status_box.warning(
                    "⚠️ Scan completed. No live hosts responded."
                )

            return [], ip_range

        for index, (_, received) in enumerate(
            result,
            start=1
        ):

            ip_addr = received.psrc
            mac_addr = received.hwsrc.upper()

            if status_box:
                status_box.info(
                    f"🔎 Processing device "
                    f"{index}/{total}: `{ip_addr}`"
                )

            try:
                hostname = socket.gethostbyaddr(
                    ip_addr
                )[0]

            except Exception:
                hostname = (
                    f"Host-{ip_addr.split('.')[-1]}"
                )

            vendor = resolve_mac_vendor(
                mac_addr
            )

            os_type = infer_device_os(
                hostname,
                ip_addr,
                vendor
            )

            discovered.append(
                {
                    "Hostname": hostname,
                    "IP Address": ip_addr,
                    "MAC Address": mac_addr,
                    "Manufacturer / Vendor": vendor,
                    "OS / Device Type": os_type,
                    "Status": "Live Host",
                }
            )

            if progress_bar:

                processing_progress = (
                    30
                    + int(
                        (index / total) * 65
                    )
                )

                progress_bar.progress(
                    min(processing_progress, 95)
                )

        if progress_bar:
            progress_bar.progress(100)

        if status_box:
            status_box.success(
                f"✅ Scan complete — "
                f"{len(discovered)} live host(s) discovered."
            )

        return discovered, ip_range

    except PermissionError:

        message = (
            "Permission denied. ARP/raw-packet scanning "
            "requires elevated privileges."
        )

        if status_box:
            status_box.error(f"❌ {message}")

        return [], ip_range

    except Exception as exc:

        if status_box:
            status_box.error(
                f"❌ Network scan failed: {exc}"
            )

        return [], ip_range


# ==============================================================================
# 9. INVENTORY MERGE
# ==============================================================================

def merge_inventory(new_assets):
    """
    Prevents duplicate assets from accumulating after repeated scans.
    Uses MAC address as the primary identity and IP as fallback.
    """

    existing = {
        (
            item.get("MAC Address")
            or item.get("IP Address")
        ): item
        for item in st.session_state.inventory
    }

    for asset in new_assets:

        key = (
            asset.get("MAC Address")
            or asset.get("IP Address")
        )

        existing[key] = asset

    st.session_state.inventory = list(
        existing.values()
    )


# ==============================================================================
# 10. ACTIVE CONNECTION MONITOR
# ==============================================================================

def analyze_active_connections():

    connections = []

    suspicious_ports = {
        22,
        23,
        135,
        139,
        445,
        3389,
        4444,
        6667,
        9001,
    }

    try:

        for conn in psutil.net_connections(
            kind="inet"
        ):

            if (
                conn.status == "ESTABLISHED"
                and conn.raddr
            ):

                r_ip = conn.raddr.ip
                r_port = conn.raddr.port

                l_ip = conn.laddr.ip
                l_port = conn.laddr.port

                if r_port in {
                    4444,
                    6667,
                    9001,
                }:

                    risk = "MALICIOUS"
                    action = "Investigate / Isolate"

                elif r_port in suspicious_ports:

                    risk = "SUSPICIOUS"
                    action = "Inspect Connection"

                else:

                    risk = "SAFE"
                    action = "Allow Traffic"

                connections.append(
                    {
                        "Local Address":
                            f"{l_ip}:{l_port}",

                        "Remote Address":
                            f"{r_ip}:{r_port}",

                        "Status":
                            conn.status,

                        "PID":
                            conn.pid or "N/A",

                        "Safety Assessment":
                            risk,

                        "Recommended Action":
                            action,
                    }
                )

    except Exception:
        pass

    return connections


# ==============================================================================
# 11. REPORT GENERATOR
# ==============================================================================

def build_full_report():

    scan_info = (
        st.session_state.last_scan_status
        or {}
    )

    return {
        "report": {
            "application":
                "ERA SecOps Cyber Defense Matrix Suite",

            "generated_utc":
                utc_now_string(),

            "platform":
                platform.platform(),

            "python":
                platform.python_version(),
        },

        "scan": scan_info,

        "summary": {
            "assets":
                len(st.session_state.inventory),

            "telemetry_events":
                len(st.session_state.telemetry_logs),

            "threat_status":
                st.session_state.threat_status,
        },

        "assets":
            st.session_state.inventory,

        "telemetry":
            st.session_state.telemetry_logs,

        "connections":
            analyze_active_connections(),
    }


# ==============================================================================
# 12. HEADER
# ==============================================================================

st.markdown(
    f"""
<div class="top-header">

    <div class="brand-title">

        <img
            src="{SHIELD_SVG}"
            width="24"
            height="24"
        />

        <span>
            ERA SecOps
            <span style="
                color:#58a6ff;
                font-weight:300;
            ">
                | Cyber Defense Matrix Suite
            </span>
        </span>

    </div>

    <div style="
        display:flex;
        gap:16px;
        align-items:center;
    ">

        <span class="status-pill">
            ● ENGINE ONLINE
        </span>

        <span style="
            font-size:12px;
            color:#768390;
        ">
            UTC: {utc_now_string().split(" ")[1]}
        </span>

    </div>

</div>
""",
    unsafe_allow_html=True,
)


# ==============================================================================
# 13. METRICS
# ==============================================================================

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-header">
                Active Inventory
            </div>

            <div class="metric-value">
                {len(st.session_state.inventory)}
            </div>

            <div class="metric-footer">
                ↑ Asset Sync Active
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


status_color = (
    "#3fb950"
    if st.session_state.threat_status == "LOW"
    else "#f85149"
)

with c2:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-header">
                Threat Status
            </div>

            <div class="metric-value"
                 style="color:{status_color};">
                {st.session_state.threat_status}
            </div>

            <div class="metric-footer">
                Telemetry Engine Active
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c3:
    st.markdown(
        """
        <div class="metric-container">
            <div class="metric-header">
                CDM Operational Cells
            </div>

            <div class="metric-value">
                25 / 25
            </div>

            <div class="metric-footer"
                 style="color:#58a6ff;">
                100% Coverage
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


with c4:
    st.markdown(
        """
        <div class="metric-container">
            <div class="metric-header">
                Automated Response MTTR
            </div>

            <div class="metric-value">
                &lt; 1.4s
            </div>

            <div class="metric-footer">
                SOAR Webhooks Armed
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 14. PERSISTENT SCAN COMPLETION
# ==============================================================================

if st.session_state.last_scan_status:

    scan_info = (
        st.session_state.last_scan_status
    )

    st.markdown(
        f"""
        <div class="scan-complete">

            <div class="scan-complete-title">
                ✅ NETWORK SCAN COMPLETE
            </div>

            <div class="scan-complete-text">
                Discovered
                <strong style="color:#f0f6fc;">
                    {scan_info.get("count", 0)}
                </strong>
                live host(s) on
                <code>
                    {scan_info.get("subnet", "Unknown")}
                </code>
            </div>

            <div class="scan-complete-time">
                Completed:
                {scan_info.get("time", "Unknown")} UTC
            </div>

        </div>
        """,
        unsafe_allow_html=True,
    )

    persistent_report = json.dumps(
        build_full_report(),
        indent=2,
        default=str,
    )

    st.download_button(
        label="📄 Click here to get the full report",
        data=persistent_report,
        file_name=(
            "era_secops_full_scan_report.json"
        ),
        mime="application/json",
        use_container_width=True,
    )


# ==============================================================================
# 15. SIDEBAR CONTROL PANEL
# ==============================================================================

st.sidebar.markdown(
    "### 🎛️ Operations Control"
)

scan_mode = st.sidebar.radio(
    "Scanner Mode",
    [
        "Simulation Mode",
        "Live Local Subnet Scan",
    ],
)


detected_subnet, host_ip = detect_local_subnet()


if scan_mode == "Live Local Subnet Scan":

    st.sidebar.success(
        f"Detected Network: {detected_subnet}"
    )

    st.sidebar.caption(
        f"Host IP: {host_ip}"
    )


sim_type = st.sidebar.selectbox(
    "Select Attack Scenario",
    [
        "Baseline Operations",
        "Ransomware Execution",
        "Credential Harvesting",
        "Data Exfiltration",
    ],
)


# ==============================================================================
# 16. RUN SCAN
# ==============================================================================

run_scan = st.sidebar.button(
    "⚡ Run Network Scan / Execution",
    type="primary",
    use_container_width=True,
)


if run_scan:

    st.session_state.scan_running = True
    st.session_state.scan_error = None

    timestamp = utc_now_string()

    st.markdown(
        """
        <div class="scan-panel">
            <h3 style="margin:0;color:#f0f6fc;">
                🔍 Network Discovery Engine
            </h3>
            <p style="color:#768390;margin-bottom:0;">
                Active scan execution in progress...
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    progress_bar = st.progress(
        0,
        text="Initializing scanner..."
    )

    status_box = st.empty()

    # ==============================================================
    # LIVE MODE
    # ==============================================================

    if scan_mode == "Live Local Subnet Scan":

        status_box.info(
            f"🚀 Starting live scan of "
            f"`{detected_subnet}`..."
        )

        real_assets, scanned_range = (
            run_live_arp_scan(
                ip_range="AUTO",
                progress_bar=progress_bar,
                status_box=status_box,
            )
        )

        if real_assets:

            merge_inventory(real_assets)

            for host in real_assets:

                st.session_state.telemetry_logs.append(
                    {
                        "Timestamp": timestamp,
                        "Event": "LIVE_HOST_DISCOVERED",
                        "Target": (
                            f"{host['Hostname']} "
                            f"({host['IP Address']})"
                        ),
                        "Vendor": host[
                            "Manufacturer / Vendor"
                        ],
                        "NIST Function": "Identify",
                        "Asset Class": "Devices",
                        "Severity": "INFO",
                        "Source": "LIVE_ARP_SCAN",
                    }
                )

        st.session_state.last_scan_status = {
            "count": len(real_assets),
            "subnet": scanned_range,
            "time": timestamp,
            "mode": "Live Local Subnet Scan",
        }

    # ==============================================================
    # SIMULATION MODE
    # ==============================================================

    else:

        total_simulated = 5
        new_assets = []

        status_box.info(
            "🧪 Starting simulated asset discovery..."
        )

        for i in range(total_simulated):

            host = (
                f"WORKSTATION-"
                f"{random.randint(100, 999)}"
            )

            ip = fake.ipv4_private()

            os_name = random.choice(
                [
                    "Windows 11 Enterprise",
                    "macOS Sequoia",
                    "Ubuntu 24.04 LTS",
                ]
            )

            vendor = random.choice(
                [
                    "Dell Inc.",
                    "Apple, Inc.",
                    "Lenovo",
                    "Hewlett-Packard",
                ]
            )

            mac = fake.mac_address().upper()

            new_assets.append(
                {
                    "Hostname": host,
                    "IP Address": ip,
                    "MAC Address": mac,
                    "Manufacturer / Vendor": vendor,
                    "OS / Device Type": os_name,
                    "Status": "Simulated / Monitored",
                }
            )

            st.session_state.telemetry_logs.append(
                {
                    "Timestamp": timestamp,
                    "Event": "SIMULATED_ASSET_DISCOVERED",
                    "Target": f"{host} ({ip})",
                    "Vendor": vendor,
                    "NIST Function": "Identify",
                    "Asset Class": "Devices",
                    "Severity": "INFO",
                    "Source": "SIMULATION",
                }
            )

            percent = int(
                ((i + 1) / total_simulated) * 100
            )

            progress_bar.progress(
                percent,
                text=(
                    f"Simulating asset "
                    f"{i + 1}/{total_simulated}"
                ),
            )

            status_box.info(
                f"🧪 Discovering simulated asset "
                f"{i + 1}/{total_simulated}..."
            )

        merge_inventory(new_assets)

        status_box.success(
            "✅ Simulation scan complete."
        )

        st.session_state.last_scan_status = {
            "count": total_simulated,
            "subnet": "Simulated Range",
            "time": timestamp,
            "mode": "Simulation Mode",
        }

    # ==============================================================
    # ATTACK SCENARIO TELEMETRY
    # ==============================================================

    if sim_type == "Ransomware Execution":

        st.session_state.threat_status = "CRITICAL"

        st.session_state.telemetry_logs.extend(
            [
                {
                    "Timestamp": timestamp,
                    "Event": "UNAUTHORIZED_FILE_ENCRYPTION",
                    "Target": "FS-01/Shared_Drive",
                    "Vendor": "Enterprise Storage",
                    "NIST Function": "Protect",
                    "Asset Class": "Data",
                    "Severity": "CRITICAL",
                    "Source": "SIMULATION",
                },
                {
                    "Timestamp": timestamp,
                    "Event": "HOST_AUTO_QUARANTINE_TRIGGERED",
                    "Target": "FS-01",
                    "Vendor": "Enterprise Storage",
                    "NIST Function": "Respond",
                    "Asset Class": "Devices",
                    "Severity": "HIGH",
                    "Source": "SIMULATION",
                },
            ]
        )

    elif sim_type == "Data Exfiltration":

        st.session_state.threat_status = "ELEVATED"

        st.session_state.telemetry_logs.append(
            {
                "Timestamp": timestamp,
                "Event": "ANOMALOUS_OUTBOUND_TRANSFER",
                "Target": "Simulated outbound transfer",
                "Vendor": "Network Telemetry",
                "NIST Function": "Detect",
                "Asset Class": "Networks",
                "Severity": "CRITICAL",
                "Source": "SIMULATION",
            }
        )

    elif sim_type == "Credential Harvesting":

        st.session_state.threat_status = "ELEVATED"

        st.session_state.telemetry_logs.append(
            {
                "Timestamp": timestamp,
                "Event": "CREDENTIAL_ACCESS_SIMULATION",
                "Target": "Simulated Domain Controller",
                "Vendor": "Microsoft Corp",
                "NIST Function": "Detect",
                "Asset Class": "Users",
                "Severity": "CRITICAL",
                "Source": "SIMULATION",
            }
        )

    # ==============================================================
    # FINAL COMPLETION
    # ==============================================================

    progress_bar.progress(
        100,
        text="✅ Scan complete"
    )

    completed_count = (
        st.session_state
        .last_scan_status
        .get("count", 0)
    )

    status_box.success(
        f"✅ **SCAN COMPLETE** — "
        f"{completed_count} live host(s) discovered."
    )

    final_report = json.dumps(
        build_full_report(),
        indent=2,
        default=str,
    )

    st.download_button(
        label="📄 Click here to get the full report",
        data=final_report,
        file_name=(
            "era_secops_full_scan_report.json"
        ),
        mime="application/json",
        type="primary",
        use_container_width=True,
    )

    st.session_state.scan_running = False


# ==============================================================================
# 17. RESET
# ==============================================================================

if st.sidebar.button(
    "🧹 Reset Telemetry & State",
    use_container_width=True,
):

    st.session_state.inventory = []
    st.session_state.telemetry_logs = []
    st.session_state.threat_status = "LOW"
    st.session_state.last_scan_status = None
    st.session_state.scan_running = False
    st.session_state.scan_error = None

    st.rerun()


# ==============================================================================
# 18. TABS
# ==============================================================================

(
    tab_matrix,
    tab_inventory,
    tab_connections,
    tab_telemetry,
) = st.tabs(
    [
        "🧩 5x5 Cyber Defense Matrix Engine",
        "🖥️ Active Asset Inventory",
        "🌐 Connection Threat Monitor",
        "📜 SIEM Telemetry Console",
    ]
)


# ==============================================================================
# 19. CYBER DEFENSE MATRIX
# ==============================================================================

with tab_matrix:

    st.subheader(
        "Sounil Yu 5x5 Matrix Control Plane"
    )

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

            <td class="cdm-cell">
                <div class="cell-title">Asset Discovery</div>
                <span class="cell-tag">AUTOMATED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">App Inventory</div>
                <span class="cell-tag">ACTIVE</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Port Mapping</div>
                <span class="cell-tag">ACTIVE</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Data Discovery</div>
                <span class="cell-tag">ACTIVE</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">IAM Mapping</div>
                <span class="cell-tag">ACTIVE</span>
            </td>
        </tr>

        <tr>
            <td class="cdm-header">Protect</td>

            <td class="cdm-cell">
                <div class="cell-title">EDR Prevention</div>
                <span class="cell-tag">ENFORCED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">App Control</div>
                <span class="cell-tag">ENFORCED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Microsegmentation</div>
                <span class="cell-tag">ENFORCED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">AES-256 Vault</div>
                <span class="cell-tag">ENFORCED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">FIDO2 MFA</div>
                <span class="cell-tag">ENFORCED</span>
            </td>
        </tr>

        <tr>
            <td class="cdm-header">Detect</td>

            <td class="cdm-cell">
                <div class="cell-title">EDR Telemetry</div>
                <span class="cell-tag">MONITORING</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Runtime Detection</div>
                <span class="cell-tag">MONITORING</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">IDS / IPS</div>
                <span class="cell-tag">MONITORING</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">DLP Monitoring</div>
                <span class="cell-tag">MONITORING</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">UEBA</div>
                <span class="cell-tag">MONITORING</span>
            </td>
        </tr>

        <tr>
            <td class="cdm-header">Respond</td>

            <td class="cdm-cell">
                <div class="cell-title">Host Isolation</div>
                <span class="cell-tag">AUTOMATED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">App Termination</div>
                <span class="cell-tag">AUTOMATED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Network Blocking</div>
                <span class="cell-tag">AUTOMATED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Data Containment</div>
                <span class="cell-tag">AUTOMATED</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Account Lockout</div>
                <span class="cell-tag">AUTOMATED</span>
            </td>
        </tr>

        <tr>
            <td class="cdm-header">Recover</td>

            <td class="cdm-cell">
                <div class="cell-title">Device Restore</div>
                <span class="cell-tag">READY</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Application Recovery</div>
                <span class="cell-tag">READY</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Network Restoration</div>
                <span class="cell-tag">READY</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Data Recovery</div>
                <span class="cell-tag">READY</span>
            </td>

            <td class="cdm-cell">
                <div class="cell-title">Identity Recovery</div>
                <span class="cell-tag">READY</span>
            </td>
        </tr>

    </table>
    """

    st.markdown(
        cdm_html,
        unsafe_allow_html=True,
    )


# ==============================================================================
# 20. ACTIVE ASSET INVENTORY
# ==============================================================================

with tab_inventory:

    st.subheader("Active Asset Inventory")

    if st.session_state.inventory:

        inventory_df = pd.DataFrame(
            st.session_state.inventory
        )

        st.dataframe(
            inventory_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No assets discovered yet. "
            "Run a network scan to populate the inventory."
        )


# ==============================================================================
# 21. CONNECTION THREAT MONITOR
# ==============================================================================

with tab_connections:

    st.subheader("Connection Threat Monitor")

    connections = analyze_active_connections()

    if connections:

        connections_df = pd.DataFrame(
            connections
        )

        st.dataframe(
            connections_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No established network connections "
            "were detected."
        )


# ==============================================================================
# 22. SIEM TELEMETRY CONSOLE
# ==============================================================================

with tab_telemetry:

    st.subheader("SIEM Telemetry Console")

    if st.session_state.telemetry_logs:

        telemetry_df = pd.DataFrame(
            st.session_state.telemetry_logs
        )

        st.dataframe(
            telemetry_df,
            use_container_width=True,
            hide_index=True,
        )

    else:

        st.info(
            "No telemetry events have been generated yet."
        )


# ==============================================================================
# 23. FOOTER
# ==============================================================================

st.markdown(
    """
    <div style="
        text-align:center;
        color:#768390;
        font-size:11px;
        margin-top:30px;
        padding:15px;
        border-top:1px solid #1e2638;
    ">
        ERA SecOps Cyber Defense Matrix Suite
        • Local Security Operations Platform
        • Enterprise Defense Telemetry
    </div>
    """,
    unsafe_allow_html=True,
)
