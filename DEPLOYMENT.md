# Deployment Guide

This guide covers different deployment options for the GRC Multi-Agent Governance System.

## Table of Contents
1. [Local Deployment](#local-deployment)
2. [Docker Deployment](#docker-deployment)
3. [Cloud Deployment](#cloud-deployment)
4. [Production Considerations](#production-considerations)

---

## Local Deployment

### Prerequisites
- Python 3.8 or higher
- pip package manager
- Git (optional, for cloning)

### Step 1: Clone or Download

```bash
# Option 1: Clone from GitHub
git clone https://github.com/HimJoe/policy-as-code.git
cd policy-as-code

# Option 2: Download ZIP and extract
# Then navigate to the directory
cd policy-as-code
```

### Step 2: Create Virtual Environment (Recommended)

```bash
# Create virtual environment
python -m venv venv

# Activate on macOS/Linux
source venv/bin/activate

# Activate on Windows
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Run the Application

**Option A: Web Interface**
```bash
streamlit run streamlit_app.py
```
Then open your browser to `http://localhost:8501`

**Option B: Command Line Demo**
```bash
python demo.py
```

**Option C: Python API**
```python
from grc_agent_system import GRCMultiAgentSystem
import asyncio

async def main():
    system = GRCMultiAgentSystem()
    # Your code here

asyncio.run(main())
```

---

## Docker Deployment

### Step 1: Create Dockerfile

Create a file named `Dockerfile`:

```dockerfile
FROM python:3.10-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application files
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit
CMD ["streamlit", "run", "streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Step 2: Create docker-compose.yml (Optional)

```yaml
version: '3.8'

services:
  grc-system:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./policies:/app/policies
      - ./logs:/app/logs
    environment:
      - PYTHONUNBUFFERED=1
    restart: unless-stopped
```

### Step 3: Build and Run

```bash
# Build the image
docker build -t grc-policy-as-code .

# Run the container
docker run -p 8501:8501 grc-policy-as-code

# Or use docker-compose
docker-compose up -d
```

---

## Cloud Deployment

### Streamlit Cloud (Easiest)

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Initial commit"
   git push origin main
   ```

2. **Deploy on Streamlit Cloud**
   - Go to [share.streamlit.io](https://share.streamlit.io)
   - Sign in with GitHub
   - Click "New app"
   - Select your repository
   - Set main file to `streamlit_app.py`
   - Click "Deploy"

3. **Your app will be live at:**
   `https://[your-app-name].streamlit.app`

### AWS EC2

1. **Launch EC2 Instance**
   - Choose Ubuntu 20.04 LTS
   - t2.micro for testing, t2.medium+ for production
   - Configure security group to allow port 8501

2. **Connect and Setup**
   ```bash
   ssh -i your-key.pem ubuntu@your-instance-ip

   # Update system
   sudo apt update && sudo apt upgrade -y

   # Install Python and pip
   sudo apt install python3-pip python3-venv -y

   # Clone repository
   git clone https://github.com/HimJoe/policy-as-code.git
   cd policy-as-code

   # Create virtual environment
   python3 -m venv venv
   source venv/bin/activate

   # Install dependencies
   pip install -r requirements.txt

   # Run with nohup
   nohup streamlit run streamlit_app.py --server.port=8501 --server.address=0.0.0.0 &
   ```

3. **Access**
   Open `http://your-instance-ip:8501`

### Heroku

1. **Create Procfile**
   ```
   web: streamlit run streamlit_app.py --server.port=$PORT --server.address=0.0.0.0
   ```

2. **Create setup.sh**
   ```bash
   mkdir -p ~/.streamlit/
   echo "\
   [server]\n\
   port = $PORT\n\
   enableCORS = false\n\
   headless = true\n\
   \n\
   " > ~/.streamlit/config.toml
   ```

3. **Deploy**
   ```bash
   heroku login
   heroku create your-app-name
   git push heroku main
   ```

### Google Cloud Run

1. **Create Dockerfile** (see Docker section)

2. **Deploy**
   ```bash
   # Build and push to Google Container Registry
   gcloud builds submit --tag gcr.io/YOUR_PROJECT_ID/grc-policy-as-code

   # Deploy to Cloud Run
   gcloud run deploy grc-policy-as-code \
     --image gcr.io/YOUR_PROJECT_ID/grc-policy-as-code \
     --platform managed \
     --region us-central1 \
     --allow-unauthenticated
   ```

### Azure Web App

1. **Create requirements.txt** (already exists)

2. **Deploy**
   ```bash
   # Login to Azure
   az login

   # Create resource group
   az group create --name GRCPolicyGroup --location eastus

   # Create App Service plan
   az appservice plan create --name GRCPolicyPlan --resource-group GRCPolicyGroup --sku B1 --is-linux

   # Create web app
   az webapp create --resource-group GRCPolicyGroup --plan GRCPolicyPlan --name your-app-name --runtime "PYTHON|3.10"

   # Deploy
   az webapp up --name your-app-name --resource-group GRCPolicyGroup
   ```

---

## Production Considerations

### 1. Environment Variables

Create a `.env` file (not committed to Git):

```bash
# Application Settings
APP_ENV=production
DEBUG=False
SECRET_KEY=your-secret-key-here

# Database (if adding persistence)
DATABASE_URL=postgresql://user:password@host:port/dbname

# Logging
LOG_LEVEL=INFO
LOG_FILE=/var/log/grc-system.log

# Authentication (if adding)
AUTH_ENABLED=True
AUTH_PROVIDER=oauth2
```

### 2. Database for Audit Logs

**PostgreSQL Setup:**
```python
# Add to grc_agent_system.py
import psycopg2

class DatabaseAuditLogger:
    def __init__(self, db_url):
        self.conn = psycopg2.connect(db_url)

    def log_decision(self, decision):
        cursor = self.conn.cursor()
        cursor.execute("""
            INSERT INTO audit_log (timestamp, user_id, action, status, risk_score)
            VALUES (%s, %s, %s, %s, %s)
        """, (
            decision['timestamp'],
            decision['user_id'],
            decision['action'],
            decision['status'],
            decision['risk_score']
        ))
        self.conn.commit()
```

### 3. Reverse Proxy with Nginx

```nginx
server {
    listen 80;
    server_name your-domain.com;

    location / {
        proxy_pass http://localhost:8501;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

### 4. SSL/TLS with Let's Encrypt

```bash
# Install Certbot
sudo apt install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d your-domain.com

# Auto-renewal is set up automatically
```

### 5. Process Management with Systemd

Create `/etc/systemd/system/grc-system.service`:

```ini
[Unit]
Description=GRC Policy as Code System
After=network.target

[Service]
Type=simple
User=ubuntu
WorkingDirectory=/home/ubuntu/policy-as-code
Environment="PATH=/home/ubuntu/policy-as-code/venv/bin"
ExecStart=/home/ubuntu/policy-as-code/venv/bin/streamlit run streamlit_app.py --server.port=8501

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl daemon-reload
sudo systemctl enable grc-system
sudo systemctl start grc-system
sudo systemctl status grc-system
```

### 6. Monitoring and Logging

**Application Logging:**
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('/var/log/grc-system.log'),
        logging.StreamHandler()
    ]
)
```

**Monitoring with Prometheus:**
- Add metrics endpoints
- Track request counts, latency, errors
- Set up alerting rules

### 7. Backup and Recovery

```bash
# Backup policies
tar -czf policies-backup-$(date +%Y%m%d).tar.gz policies/

# Backup database
pg_dump -U username dbname > backup-$(date +%Y%m%d).sql

# Automated backup with cron
0 2 * * * /path/to/backup-script.sh
```

### 8. Security Checklist

- [ ] Enable HTTPS/SSL
- [ ] Implement authentication (OAuth2, SAML)
- [ ] Add rate limiting
- [ ] Configure CORS properly
- [ ] Use environment variables for secrets
- [ ] Enable audit logging
- [ ] Regular security updates
- [ ] Input validation and sanitization
- [ ] SQL injection prevention
- [ ] XSS protection

### 9. Performance Optimization

- Use caching for frequently accessed rules
- Implement connection pooling for databases
- Add CDN for static assets
- Enable gzip compression
- Optimize database queries
- Consider horizontal scaling

### 10. High Availability

**Load Balancer Setup:**
```yaml
# docker-compose for multiple instances
version: '3.8'

services:
  nginx:
    image: nginx:latest
    ports:
      - "80:80"
    volumes:
      - ./nginx.conf:/etc/nginx/nginx.conf
    depends_on:
      - app1
      - app2

  app1:
    build: .
    environment:
      - INSTANCE=1

  app2:
    build: .
    environment:
      - INSTANCE=2
```

---

## Testing Deployment

### Health Check Endpoint

Add to `streamlit_app.py`:
```python
# Create a simple health check
import requests

def health_check():
    try:
        # Check if system is responsive
        system = GRCMultiAgentSystem()
        return {"status": "healthy", "timestamp": datetime.now()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}
```

### Smoke Tests

```bash
# Test endpoints
curl http://localhost:8501/_stcore/health

# Test import
python -c "from grc_agent_system import GRCMultiAgentSystem; print('OK')"

# Run demo
python demo.py
```

---

## Troubleshooting

### Common Issues

1. **Port already in use**
   ```bash
   # Find process using port
   lsof -i :8501

   # Kill process
   kill -9 <PID>
   ```

2. **Module not found**
   ```bash
   # Ensure virtual environment is activated
   which python

   # Reinstall dependencies
   pip install -r requirements.txt
   ```

3. **Permission denied**
   ```bash
   # Fix file permissions
   chmod +x streamlit_app.py

   # Fix directory permissions
   chmod -R 755 /path/to/app
   ```

4. **Memory issues**
   - Increase instance size
   - Optimize rule loading
   - Use pagination for large datasets

---

## Support

For deployment issues:
- Check [GitHub Issues](https://github.com/HimJoe/policy-as-code/issues)
- Review logs: `tail -f /var/log/grc-system.log`
- Contact maintainers

---

**Ready to Deploy?**

Start with local deployment, then move to cloud when ready for production!
