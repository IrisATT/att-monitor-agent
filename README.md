# 🖥️ Monitor Agent

A lightweight Python-based monitoring agent that tracks server health (CPU, RAM, Disk, Load, Uptime, etc.) and reports it to a centralized admin dashboard via HTTP.

---

## 📦 Features

- Monitor system metrics every 30 seconds:
  - ✅ CPU usage (%)
  - ✅ RAM usage (%)
  - ✅ Disk usage (%)
  - ✅ Load average
  - ✅ Uptime (seconds)
  - ✅ OS, Hostname, IP, MAC Address
- Works on **Ubuntu**, **Debian**, **CentOS**, and other Linux distros
- Easy to install via `.tar.gz` package or one-liner shell script
- Sends data securely using your admin-generated API key
- Runs as a background **`systemd` service**

---

## 🚀 Installation

### 🔧 Method 1: One-liner auto-install

```bash
curl -sL https://your-domain.com/install.sh | bash
```

This script will:

- Download and extract the monitoring agent
- Prompt you for your API key and server URL
- Register the agent as a systemd service

---

### 📦 Method 2: Manual from GitHub Release

```bash
# Download the latest release
curl -sL https://github.com/your-org/monitor-agent/releases/download/v1.0.0/monitor-agent-v1.0.0.tar.gz -o monitor-agent.tar.gz

# Extract
tar -xzf monitor-agent.tar.gz
cd monitor-agent

# Install manually
sudo bash install.sh
```

---

## 🔐 Configuration

After running the script, you'll be prompted to input:

- ✅ **API Key** — generated from your admin dashboard
- 🌐 **Monitoring API URL** — e.g. `https://your-api.com/api/monitor`

This data will be saved into:

```ini
/opt/monitor-agent/config.ini
```

**Sample config:**

```ini
[DEFAULT]
SERVER_URL = https://your-api.com/api/monitor
API_KEY = your-server-api-key
INTERVAL_SECONDS = 30
```

---

## 🔄 Service Control

Once installed, the agent runs continuously in the background via `systemd`.

```bash
# Check status
sudo systemctl status monitor-agent

# Restart
sudo systemctl restart monitor-agent

# Stop
sudo systemctl stop monitor-agent

# View logs
cat /var/log/monitor-agent.log
```

---

## 📁 File Structure

```
monitor-agent/
├── agent.py                 # Main monitoring script
├── config.ini               # Generated at install time
├── monitor-agent.service    # systemd unit file
├── requirements.txt         # Python dependencies
├── install.sh               # Bootstrap installer
```

---

## 📤 API Request Format

Every 30 seconds, this agent POSTs data to your backend:

**Request headers:**

```
POST /api/monitor
Content-Type: application/json
X-API-KEY: your-api-key
```

**Sample payload:**

```json
{
  "hostname": "web-1",
  "ip": "192.168.1.10",
  "os": "Linux",
  "platform": "Ubuntu 22.04",
  "mac": "00:1A:2B:3C:4D:5E",
  "cpu_percent": 13.7,
  "memory_percent": 62.3,
  "disk_percent": 70.1,
  "load_avg": 1.03,
  "uptime_seconds": 304500,
  "timestamp": "2025-05-02 11:45:23"
}
```

You can validate this key and store data accordingly in your backend.

---

## 🛡️ Security Notes

- Each agent uses a unique API Key
- Data is sent securely over HTTPS
- You can revoke or regenerate keys from the dashboard

---

## 📄 License

MIT License — © 2025 Your Company

---

## 👨‍💻 Maintainer

Developed and maintained by [your-name].  
Contributions and feedback welcome via Issues and Pull Requests.
