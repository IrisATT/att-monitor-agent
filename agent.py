import psutil
import requests
import time
import socket
import platform
import uuid
import logging
import configparser
import os

# Setup logging
logging.basicConfig(
    filename="/var/log/monitor-agent.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# Load config
CONFIG_PATH = "/opt/monitor-agent/config.ini"
config = configparser.ConfigParser()
config.read(CONFIG_PATH)

SERVER_URL = config.get('DEFAULT', 'SERVER_URL', fallback='https://your-api.com/api/monitor')
API_KEY = config.get('DEFAULT', 'API_KEY', fallback='')
INTERVAL = config.getint('DEFAULT', 'INTERVAL_SECONDS', fallback=30)

def get_ip():
    try:
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)
    except:
        return "Unknown"

def get_mac():
    mac = uuid.getnode()
    return ':'.join(("%012X" % mac)[i:i+2] for i in range(0, 12, 2))

def get_network_stats(interval=1):
    io1 = psutil.net_io_counters()
    time.sleep(interval)
    io2 = psutil.net_io_counters()

    stats = {
        "bytes_sent_per_sec": (io2.bytes_sent - io1.bytes_sent) / interval,
        "bytes_recv_per_sec": (io2.bytes_recv - io1.bytes_recv) / interval,
        "packets_sent_per_sec": (io2.packets_sent - io1.packets_sent) / interval,
        "packets_recv_per_sec": (io2.packets_recv - io1.packets_recv) / interval,
        "total_bytes_sent": io2.bytes_sent,
        "total_bytes_recv": io2.bytes_recv,
        "errors_in": io2.errin,
        "errors_out": io2.errout,
        "drops_in": io2.dropin,
        "drops_out": io2.dropout,
    }
    return stats

def collect_metrics():
    network = get_network_stats()
    return {
        "hostname": socket.gethostname(),
        "ip": get_ip(),
        "os": platform.system(),
        "platform": platform.platform(),
        "mac": get_mac(),
        "cpu_percent": psutil.cpu_percent(interval=1),
        "memory_percent": psutil.virtual_memory().percent,
        "disk_percent": psutil.disk_usage('/').percent,
        "load_avg": os.getloadavg()[0] if hasattr(os, "getloadavg") else None,
        "uptime_seconds": time.time() - psutil.boot_time(),
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S"),
        **network,
    }

def send_metrics():
    data = collect_metrics()
    try:
        response = requests.post(
            SERVER_URL,
            json=data,
            headers={"X-API-KEY": API_KEY, "Content-Type": "application/json"},
            timeout=10
        )
        response.raise_for_status()
        logging.info("✅ Sent metrics successfully")
    except requests.RequestException as e:
        logging.error(f"❌ Failed to send metrics: {e}")

def main():
    logging.info("🟢 Agent started")
    while True:
        send_metrics()
        time.sleep(INTERVAL)

if __name__ == "__main__":
    main()