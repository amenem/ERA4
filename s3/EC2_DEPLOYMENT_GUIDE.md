# 🚀 EC2 Deployment Guide for ERA4 Frontend

This guide covers deploying your ERA4 Frontend application to Amazon EC2 with Amazon Linux.

## 📋 **Prerequisites**

- AWS Account with EC2 access
- Basic knowledge of AWS services
- SSH key pair for EC2 access
- Domain name (optional, for production)

## 🏗️ **Option 1: Manual Deployment (Recommended for Learning)**

### Step 1: Launch EC2 Instance

1. **Go to AWS Console** → **EC2** → **Launch Instance**
2. **Choose Amazon Linux 2023** (latest version)
3. **Instance Type**: `t3.micro` (free tier) or `t3.small` for production
4. **Key Pair**: Create or select existing SSH key pair
5. **Security Group**: Allow ports 22 (SSH), 80 (HTTP), 443 (HTTPS)
6. **Storage**: 8GB minimum (20GB recommended)

### Step 2: Connect to Instance

```bash
# Connect via SSH
ssh -i your-key.pem ec2-user@YOUR_EC2_PUBLIC_IP

# Update system
sudo yum update -y
```

### Step 3: Deploy Application

```bash
# Clone your repository
git clone https://github.com/amenem/ERA4.git
cd ERA4/s3

# Make deployment script executable
chmod +x deploy_ec2.sh

# Run deployment script
./deploy_ec2.sh
```

### Step 4: Verify Deployment

```bash
# Check service status
sudo systemctl status era4-frontend
sudo systemctl status nginx

# Check logs
sudo journalctl -u era4-frontend -f
sudo tail -f /var/log/nginx/error.log
```

## 🐳 **Option 2: Docker Deployment (Easier Management)**

### Step 1: Install Docker on EC2

```bash
# Install Docker
sudo yum install -y docker
sudo systemctl start docker
sudo systemctl enable docker
sudo usermod -a -G docker ec2-user

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/latest/download/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Logout and login again for group changes
exit
# SSH back in
```

### Step 2: Deploy with Docker

```bash
# Clone repository
git clone https://github.com/amenem/ERA4.git
cd ERA4/s3

# Build and run with Docker Compose
docker-compose up -d --build

# Check status
docker-compose ps
docker-compose logs -f
```

## 🔧 **Configuration Options**

### Environment Variables

Create `.env` file for Docker deployment:

```bash
# .env
NODE_ENV=production
PORT=8001
LOG_LEVEL=info
```

### Custom Domain Setup

1. **Route 53**: Point domain to EC2 public IP
2. **SSL Certificate**: Use AWS Certificate Manager
3. **Update Nginx**: Configure SSL and domain name

## 📊 **Monitoring & Maintenance**

### Health Checks

```bash
# Application health
curl http://YOUR_EC2_IP/health

# Service status
sudo systemctl status era4-frontend
sudo systemctl status nginx
```

### Logs

```bash
# Application logs
sudo journalctl -u era4-frontend -f

# Nginx logs
sudo tail -f /var/log/nginx/access.log
sudo tail -f /var/log/nginx/error.log

# Docker logs (if using Docker)
docker-compose logs -f era4-frontend
docker-compose logs -f nginx
```

### Performance Monitoring

```bash
# System resources
htop
df -h
free -h

# Network connections
netstat -tulpn
ss -tulpn
```

## 🚨 **Troubleshooting**

### Common Issues

1. **Port 80 blocked**: Check security group and firewall
2. **Service won't start**: Check logs and dependencies
3. **Static files not loading**: Verify file permissions and paths
4. **High memory usage**: Optimize worker processes

### Debug Commands

```bash
# Check service configuration
sudo systemctl cat era4-frontend

# Test Nginx config
sudo nginx -t

# Check file permissions
ls -la /opt/era4-frontend/
ls -la /opt/era4-frontend/s3/static/

# Test application directly
curl http://localhost:8001/
```

## 🔒 **Security Best Practices**

1. **Security Groups**: Only open necessary ports
2. **Firewall**: Configure firewalld properly
3. **Updates**: Regular system updates
4. **Monitoring**: Set up CloudWatch alarms
5. **Backups**: Regular EBS snapshots

## 📈 **Scaling Options**

### Vertical Scaling
- Increase instance size (t3.micro → t3.medium → t3.large)

### Horizontal Scaling
- Use Application Load Balancer
- Multiple EC2 instances
- Auto Scaling Groups

### Container Orchestration
- Amazon ECS
- Amazon EKS (Kubernetes)
- AWS App Runner

## 💰 **Cost Optimization**

1. **Reserved Instances**: For predictable workloads
2. **Spot Instances**: For non-critical applications
3. **Right-sizing**: Monitor and adjust instance types
4. **Auto Scaling**: Scale down during low usage

## 🎯 **Next Steps**

1. **Set up monitoring**: CloudWatch, logging
2. **Configure backups**: EBS snapshots, AMI creation
3. **Set up CI/CD**: GitHub Actions, AWS CodePipeline
4. **Add SSL**: AWS Certificate Manager
5. **Set up CDN**: CloudFront for static files

## 📞 **Support**

- **AWS Support**: For infrastructure issues
- **Application Logs**: For code-related problems
- **Community**: GitHub issues, Stack Overflow

---

**Happy Deploying! 🚀**

Your ERA4 Frontend will be accessible at: `http://YOUR_EC2_PUBLIC_IP` 