#!/bin/bash

# ERA4 Frontend EC2 Deployment Script for Amazon Linux
# This script sets up the environment and deploys the FastAPI application

set -e  # Exit on any error

echo "🚀 Starting ERA4 Frontend EC2 Deployment..."

# Update system packages
echo "📦 Updating system packages..."
sudo yum update -y

# Install Python 3.9+ and development tools
echo "🐍 Installing Python and development tools..."
sudo yum install -y python3 python3-pip python3-devel gcc

# Install additional system dependencies
echo "🔧 Installing system dependencies..."
sudo yum install -y git nginx

# Verify Python version
python3 --version
pip3 --version

# Create application directory
echo "📁 Setting up application directory..."
sudo mkdir -p /opt/era4-frontend
sudo chown ec2-user:ec2-user /opt/era4-frontend
cd /opt/era4-frontend

# Clone or copy your application (if not already present)
# If you're running this on the EC2 instance directly:
# git clone https://github.com/amenem/ERA4.git .
# cd ERA4/s3

# Install UV (faster than pip)
echo "⚡ Installing UV package manager..."
curl -LsSf https://astral.sh/uv/install.sh | sh
source ~/.bashrc

# Create virtual environment and install dependencies
echo "📚 Installing Python dependencies..."
uv sync

# Download animal images
echo "🖼️ Downloading animal images..."
uv run python setup_images.py

# Create systemd service file
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/era4-frontend.service > /dev/null <<EOF
[Unit]
Description=ERA4 Frontend FastAPI Application
After=network.target

[Service]
Type=exec
User=ec2-user
WorkingDirectory=/opt/era4-frontend/s3
Environment=PATH=/opt/era4-frontend/.venv/bin
ExecStart=/opt/era4-frontend/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Create Nginx configuration
echo "🌐 Configuring Nginx..."
sudo tee /etc/nginx/conf.d/era4-frontend.conf > /dev/null <<EOF
server {
    listen 80;
    server_name _;

    # Proxy to FastAPI application
    location / {
        proxy_pass http://127.0.0.1:8001;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }

    # Serve static files directly (optional optimization)
    location /static/ {
        alias /opt/era4-frontend/s3/static/;
        expires 1y;
        add_header Cache-Control "public, immutable";
    }
}
EOF

# Remove default Nginx site
sudo rm -f /etc/nginx/conf.d/default.conf

# Test Nginx configuration
echo "🧪 Testing Nginx configuration..."
sudo nginx -t

# Start and enable services
echo "🚀 Starting services..."
sudo systemctl daemon-reload
sudo systemctl enable era4-frontend
sudo systemctl start era4-frontend
sudo systemctl enable nginx
sudo systemctl start nginx

# Configure firewall (if using security groups, this might not be needed)
echo "🔥 Configuring firewall..."
sudo yum install -y firewalld
sudo systemctl enable firewalld
sudo systemctl start firewalld
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload

# Check service status
echo "📊 Checking service status..."
sudo systemctl status era4-frontend --no-pager
sudo systemctl status nginx --no-pager

echo "✅ Deployment completed successfully!"
echo "🌐 Your application should be accessible at: http://YOUR_EC2_PUBLIC_IP"
echo "📚 API Documentation: http://YOUR_EC2_PUBLIC_IP/docs"
echo ""
echo "📋 Useful commands:"
echo "  - Check app logs: sudo journalctl -u era4-frontend -f"
echo "  - Check nginx logs: sudo tail -f /var/log/nginx/error.log"
echo "  - Restart app: sudo systemctl restart era4-frontend"
echo "  - Restart nginx: sudo systemctl restart nginx" 