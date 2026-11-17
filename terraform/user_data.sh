#!/bin/bash
set -e

# 1. Update system and install Python, Git, and curl
apt-get update -y
apt-get install -y python3-pip python3-venv git curl gnupg

# 2. Install MongoDB 8.0 Community Edition (Ubuntu 24.04 ARM64)
curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
  gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor

echo "deb [ arch=arm64 signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] https://repo.mongodb.org/apt/ubuntu noble/mongodb-org/8.0 multiverse" | \
  tee /etc/apt/sources.list.d/mongodb-org-8.0.list

apt-get update -y
apt-get install -y mongodb-org

systemctl start mongod
systemctl enable mongod

# 3. Clone your project repository
cd /home/ubuntu
git clone ${github_repo_url} event-pipeline
chown -R ubuntu:ubuntu /home/ubuntu/event-pipeline

# 4. Set up Python virtual environment & install dependencies
sudo -u ubuntu bash -c "
  cd /home/ubuntu/event-pipeline
  python3 -m venv venv
  source venv/bin/activate
  pip install --upgrade pip
  pip install -r requirements.txt
"

# 5. Run the pipeline once immediately to verify
sudo -u ubuntu bash -c "
  cd /home/ubuntu/event-pipeline
  source venv/bin/activate
  python generator.py
  python pipeline.py
"

# 6. Schedule automated hourly runs via cron
CRON_JOB="0 * * * * cd /home/ubuntu/event-pipeline && /home/ubuntu/event-pipeline/venv/bin/python generator.py && /home/ubuntu/event-pipeline/venv/bin/python pipeline.py >> /home/ubuntu/event-pipeline/cron.log 2>&1"
(crontab -u ubuntu -l 2>/dev/null; echo "$CRON_JOB") | crontab -u ubuntu -