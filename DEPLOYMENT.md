# 🚀 Automatic Deployment Setup

This document explains the automatic deployment system that triggers when PRs are merged into the main branch.

## 🔄 How It Works

### 1. Pull Request Testing
When you create or update a PR:
- **Comprehensive tests run automatically**
- **Coverage reports are generated**
- **Docker build is tested**
- **Security scanning is performed**
- **Results are commented on the PR**

### 2. Automatic Deployment on Merge
When a PR is merged to main:
- **`deploy-on-merge.yml` triggers immediately**
- **Pre-deployment tests run**
- **Docker image is built and pushed**
- **Production deployment is triggered**
- **Health checks are performed**
- **Deployment status is reported**

### 3. Production Deployment Process
The production deployment includes:
- ✅ Health checks before deployment
- ✅ Zero-downtime deployment
- ✅ Endpoint verification
- ✅ Automatic rollback on failure
- ✅ Resource limits and monitoring

## 🛠️ Setup Instructions

### 1. Configure GitHub Secrets
In your repository settings → Secrets and variables → Actions:

```
DOCKER_USERNAME=your-dockerhub-username
DOCKER_PASSWORD=your-dockerhub-password-or-token
```

### 2. Set Up Self-Hosted Runner (for production deployment)

#### Install Docker
```bash
sudo apt update
sudo apt install docker.io
sudo systemctl enable docker
sudo systemctl start docker
sudo usermod -aG docker $USER
```

#### Configure GitHub Runner
1. Go to repository Settings → Actions → Runners
2. Click "New self-hosted runner"
3. Follow the setup instructions
4. Ensure the runner has the `self-hosted` label

### 3. Update Production URLs
Edit these files to match your environment:
- `.github/workflows/deploy-on-merge.yml` - Update environment URL
- `.github/workflows/production-deploy.yml` - Update environment URL and container settings

## 🎯 Deployment Flow

```
PR Created → Tests Run → PR Approved → PR Merged → Automatic Deployment
     ↓              ↓           ↓            ↓              ↓
  test-pr.yml   Coverage    Manual     deploy-on-    production-
   workflow     Reports     Review     merge.yml     deploy.yml
```

## 📊 Monitoring

### Check Deployment Status
1. **GitHub Actions Tab**: View workflow runs and logs
2. **Deployments Section**: Track deployment history
3. **PR Comments**: Automatic status updates
4. **Production Logs**: `sudo docker logs fastapi-backend-container`

### Health Check Endpoints
The deployment automatically tests these endpoints:
- `GET /` - Main endpoint
- `GET /test` - Test endpoint
- `GET /try` - Try endpoint
- `GET /work` - Work endpoint
- `GET /testing` - Testing endpoint
- `GET /ansible` - Ansible endpoint
- `GET /metrics` - Prometheus metrics

## 🔧 Manual Operations

### Manual Deployment
If you need to deploy manually:
1. Go to Actions tab
2. Select "Production Deployment"
3. Click "Run workflow"
4. Optionally specify Docker image tag

### Rollback
Automatic rollback happens on failure, but for manual rollback:
```bash
# On production server
sudo docker stop fastapi-backend-container
sudo docker rm fastapi-backend-container

# Find previous image
sudo docker images sakthi1946/fastapi-backend

# Deploy previous version
sudo docker run -d -p 8000:8000 --name fastapi-backend-container sakthi1946/fastapi-backend:PREVIOUS_TAG
```

### View Logs
```bash
# Application logs
sudo docker logs fastapi-backend-container

# Follow logs in real-time
sudo docker logs -f fastapi-backend-container

# Container status
sudo docker ps | grep fastapi-backend
```

## 🚨 Troubleshooting

### Common Issues

#### 1. Docker Hub Authentication Failed
- Verify `DOCKER_USERNAME` and `DOCKER_PASSWORD` secrets
- Check Docker Hub permissions
- Ensure token has push permissions

#### 2. Self-Hosted Runner Issues
```bash
# Check runner status
sudo systemctl status actions.runner.*

# Restart runner
sudo systemctl restart actions.runner.*

# Check Docker
sudo systemctl status docker
```

#### 3. Deployment Health Check Failures
```bash
# Check application logs
sudo docker logs fastapi-backend-container

# Test endpoints manually
curl http://localhost:8000/
curl http://localhost:8000/metrics

# Check container resources
sudo docker stats fastapi-backend-container
```

#### 4. Port Conflicts
```bash
# Check what's using port 8000
sudo netstat -tulpn | grep 8000

# Kill conflicting processes
sudo fuser -k 8000/tcp
```

## 🔒 Security Considerations

### Secrets Management
- Never commit secrets to the repository
- Use GitHub Secrets for sensitive data
- Rotate Docker Hub tokens regularly

### Image Security
- Images are scanned with Trivy
- Multi-platform builds ensure compatibility
- Regular base image updates recommended

### Network Security
- Production deployment uses resource limits
- Container restart policies prevent downtime
- Health checks ensure service availability

## 📈 Performance Optimization

### Docker Optimizations
- Build caching reduces build times
- Multi-stage builds keep images small
- Resource limits prevent resource exhaustion

### Deployment Optimizations
- Zero-downtime deployment strategy
- Health checks before traffic routing
- Automatic cleanup of old images

## 🎉 Benefits

✅ **No Manual Deployment**: Automatic on every merge
✅ **Quality Assurance**: Tests run before deployment
✅ **Zero Downtime**: Health checks and rollback
✅ **Monitoring**: Full visibility into deployments
✅ **Scalability**: Multi-platform Docker images
✅ **Security**: Automated scanning and updates

## 📞 Support

If you encounter issues:
1. Check the GitHub Actions logs
2. Review the troubleshooting section
3. Check production server logs
4. Verify all secrets are configured correctly

The deployment system is designed to be robust and self-healing, with automatic rollback capabilities to ensure your service stays available.