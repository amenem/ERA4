#!/bin/bash

# Quick EC2 Deployment Script for ERA4 Frontend
# Run this on your EC2 instance after cloning the repository

echo "🚀 Quick EC2 Deployment for ERA4 Frontend..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "❌ Please don't run as root. Use: sudo -u ec2-user ./quick_deploy.sh"
    exit 1
fi

# Check if we're in the right directory
if [ ! -f "main.py" ]; then
    echo "❌ Please run this script from the s3/ directory"
    echo "   cd ERA4/s3"
    exit 1
fi

echo "✅ Running from correct directory"

# Install UV if not present
if ! command -v uv &> /dev/null; then
    echo "⚡ Installing UV package manager..."
    curl -LsSf https://astral.sh/uv/install.sh | sh
    source ~/.bashrc
else
    echo "✅ UV already installed"
fi

# Install dependencies
echo "📚 Installing Python dependencies..."
uv sync

# Download images if not present
if [ ! -d "static/images" ] || [ ! -f "static/images/cat.jpg" ]; then
    echo "🖼️ Downloading animal images..."
    uv run python setup_images.py
else
    echo "✅ Images already present"
fi

# Create simple systemd service
echo "🔧 Creating systemd service..."
sudo tee /etc/systemd/system/era4-frontend.service > /dev/null <<EOF
[Unit]
Description=ERA4 Frontend FastAPI Application
After=network.target

[Service]
Type=exec
User=ec2-user
WorkingDirectory=$(pwd)
Environment=PATH=$(pwd)/.venv/bin
ExecStart=$(pwd)/.venv/bin/uvicorn main:app --host 0.0.0.0 --port 8001
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Enable and start service
echo "🚀 Starting service..."
sudo systemctl daemon-reload
sudo systemctl enable era4-frontend
sudo systemctl start era4-frontend

# Wait a moment for service to start
sleep 5

# Check status
echo "📊 Service status:"
sudo systemctl status era4-frontend --no-pager

# Test the application
echo "🧪 Testing application..."
if curl -s http://localhost:8001/ > /dev/null; then
    echo "✅ Application is running successfully!"
    echo ""
    echo "🌐 Access your application at:"
    echo "   - Frontend: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8001"
    echo "   - API Docs: http://$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4):8001/docs"
    echo ""
    echo "📋 Useful commands:"
    echo "   - Check logs: sudo journalctl -u era4-frontend -f"
    echo "   - Restart: sudo systemctl restart era4-frontend"
    echo "   - Stop: sudo systemctl stop era4-frontend"
else
    echo "❌ Application failed to start. Check logs:"
    echo "   sudo journalctl -u era4-frontend -f"
    exit 1
fi 