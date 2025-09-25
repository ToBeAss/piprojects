import re
import socket
import subprocess
import time
from datetime import datetime
import sys
import os

# Add the parent directory to sys.path to allow imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src import discord

def get_ipv4(prefer_iface="wlan0", timeout_s=45):
    """
    Wait up to timeout_s for an IPv4 on prefer_iface.
    Falls back to default-route trick if needed.
    """
    deadline = time.time() + timeout_s
    ip = None
    while time.time() < deadline and not ip:
        # Try explicit interface first (iproute2)
        try:
            out = subprocess.check_output(
                ["ip", "-4", "addr", "show", prefer_iface],
                text=True
            )
            m = re.search(r"inet\s+(\d+\.\d+\.\d+\.\d+)", out)
            if m:
                ip = m.group(1)
                break
        except Exception:
            pass

        # Fallback: default-route trick (works once network is up)
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            # target never contacted; just selects the outbound iface
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            if ip and ip != "127.0.0.1":
                break
        except Exception:
            pass

        time.sleep(2)

    return ip

import subprocess, shutil, re

def _run(cmd):
    return subprocess.check_output(cmd, text=True).strip()

def get_ssid():
    # 1) Try iwgetid (absolute path for systemd)
    for candidate in ("/sbin/iwgetid", "/usr/sbin/iwgetid", shutil.which("iwgetid")):
        if candidate:
            try:
                ssid = _run([candidate, "-r"])
                if ssid:
                    return ssid
            except Exception:
                pass

    # 2) Ask NM for the active connection name on wlan0
    nmcli = shutil.which("nmcli") or "/usr/bin/nmcli"
    try:
        # e.g., "preconfigured" / "OfficeGuest" / "PhoneHotspot"
        con_name = _run([nmcli, "-t", "-g", "GENERAL.CONNECTION", "device", "show", "wlan0"])
        if con_name and con_name != "--":
            # Map connection → actual SSID (handles spaces/special chars)
            ssid = _run([nmcli, "-t", "-g", "802-11-wireless.ssid", "connection", "show", con_name])
            if ssid:
                return ssid
    except Exception:
        pass

    # 3) Last resort: parse kernel link info (works without NM)
    try:
        out = _run(["/sbin/iw", "dev", "wlan0", "link"])
        m = re.search(r"SSID:\s*(.+)", out)
        if m:
            return m.group(1).strip()
    except Exception:
        pass

    return None

def announce_reboot(webhook, iface="wlan0"):
    host = socket.gethostname()
    ip = get_ipv4(prefer_iface=iface, timeout_s=45)  # wait a bit for DHCP
    ssid = get_ssid()
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    msg = (
        f"🟢 System rebooted @ {ts}\n"
        f"• Host: `{host}`\n"
        f"• Interface: `{iface}`\n"
        f"• IP: `{ip or 'not assigned yet'}`\n"
        f"• SSID: `{ssid or 'unknown'}`"
    )
    discord.send_to_discord(webhook, msg)