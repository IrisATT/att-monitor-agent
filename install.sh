#!/bin/bash

set -e

VERSION="v1.0.0"
DOWNLOAD_URL="https://github.com/your-org/monitor-agent/releases/download/${VERSION}/monitor-agent-${VERSION}.tar.gz"

echo "📥 Đang tải monitor agent..."
curl -L $DOWNLOAD_URL -o /tmp/monitor-agent.tar.gz

echo "📦 Đang giải nén..."
mkdir -p /opt/monitor-agent
tar -xzf /tmp/monitor-agent.tar.gz -C /opt/monitor-agent --strip-components=1

echo "🔧 Cấu hình..."
read -p "Nhập API Key: " API_KEY
read -p "Nhập URL nhận dữ liệu [https://your-api.com/api/monitor]: " SERVER_URL
SERVER_URL=${SERVER_URL:-https://your-api.com/api/monitor}

cat <<EOF > /opt/monitor-agent/config.ini
[DEFAULT]
SERVER_URL = ${SERVER_URL}
API_KEY = ${API_KEY}
INTERVAL_SECONDS = 30
EOF

echo "📦 Cài Python và thư viện..."
apt-get update -y && apt-get install -y python3 python3-pip
pip3 install -r /opt/monitor-agent/requirements.txt

echo "⚙️ Cài đặt service..."
cp /opt/monitor-agent/monitor-agent.service /etc/systemd/system/monitor-agent.service
systemctl daemon-reload
systemctl enable monitor-agent
systemctl restart monitor-agent

echo "✅ Cài đặt hoàn tất!"
