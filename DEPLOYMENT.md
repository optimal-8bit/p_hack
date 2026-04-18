# 🚀 Deployment Guide

Complete guide for deploying the Offline AI Health Assistant to production.

---

## Deployment Options

1. **Cloud Deployment** (Render + Vercel) - For online access
2. **Local Network Deployment** - For offline clinic use
3. **Hybrid Deployment** - Cloud with offline fallback

---

## Option 1: Cloud Deployment

### Backend: Deploy to Render

#### Prerequisites
- GitHub account
- Render account (free tier available)

#### Steps

1. **Push code to GitHub**
   ```bash
   cd py_server
   git init
   git add .
   git commit -m "Initial commit"
   git remote add origin https://github.com/yourusername/health-assistant.git
   git push -u origin main
   ```

2. **Create Render Web Service**
   - Go to [render.com](https://render.com)
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Configure:
     - **Name**: `health-assistant-api`
     - **Environment**: `Python 3`
     - **Build Command**: `pip install -r requirements.txt`
     - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
     - **Plan**: Free (or paid for better performance)

3. **Set Environment Variables**
   ```
   PYTHON_VERSION=3.10.0
   APP_NAME=Offline Health Assistant API
   APP_ENV=production
   API_PREFIX=/api/v1
   JWT_SECRET_KEY=<generate-secure-random-key>
   MONGO_URI=<your-mongodb-uri-if-needed>
   ```

4. **Deploy**
   - Click "Create Web Service"
   - Wait for deployment (5-10 minutes)
   - Note your API URL: `https://your-app.onrender.com`

5. **Verify Deployment**
   ```bash
   curl https://your-app.onrender.com/api/v1/health
   ```

#### Render Configuration File

The `render.yaml` file is already included:

```yaml
services:
  - type: web
    name: offline-health-assistant-api
    env: python
    buildCommand: pip install -r requirements.txt
    startCommand: uvicorn app.main:app --host 0.0.0.0 --port $PORT
```

---

### Frontend: Deploy to Vercel

#### Prerequisites
- Vercel account (free tier available)
- Node.js installed

#### Steps

1. **Install Vercel CLI**
   ```bash
   npm install -g vercel
   ```

2. **Configure Environment**
   ```bash
   cd react_web
   
   # Create .env.production
   echo "VITE_API_BASE_URL=https://your-app.onrender.com/api/v1" > .env.production
   ```

3. **Deploy**
   ```bash
   vercel --prod
   ```

4. **Follow Prompts**
   - Link to existing project or create new
   - Confirm settings
   - Wait for deployment

5. **Set Environment Variable in Vercel Dashboard**
   - Go to Vercel dashboard
   - Select your project
   - Settings → Environment Variables
   - Add: `VITE_API_BASE_URL` = `https://your-app.onrender.com/api/v1`
   - Redeploy

6. **Verify Deployment**
   - Visit your Vercel URL
   - Test diagnosis functionality

#### Alternative: Deploy via GitHub

1. **Push to GitHub**
   ```bash
   cd react_web
   git init
   git add .
   git commit -m "Initial commit"
   git push
   ```

2. **Import to Vercel**
   - Go to Vercel dashboard
   - "Add New" → "Project"
   - Import from GitHub
   - Configure environment variables
   - Deploy

---

## Option 2: Local Network Deployment (Offline Clinic)

Perfect for clinics without reliable internet.

### Architecture

```
┌─────────────────┐
│  Server Machine │  ← Backend + Frontend files
│  (192.168.1.100)│
└────────┬────────┘
         │
    Local WiFi/LAN
         │
    ┌────┴────┬────────┬────────┐
    │         │        │        │
┌───▼───┐ ┌──▼───┐ ┌──▼───┐ ┌──▼───┐
│Tablet │ │Laptop│ │Phone │ │ PC   │
└───────┘ └──────┘ └──────┘ └──────┘
```

### Setup

#### 1. Server Machine Setup

**Install Dependencies:**
```bash
# Install Python 3.10+
# Install Node.js 18+

# Backend
cd py_server
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt

# Frontend
cd ../react_web
npm install
```

**Get Server IP Address:**
```bash
# Windows
ipconfig
# Look for "IPv4 Address" (e.g., 192.168.1.100)

# Mac/Linux
ifconfig
# or
ip addr show
```

**Configure Frontend:**
```bash
cd react_web
echo "VITE_API_BASE_URL=http://192.168.1.100:8000/api/v1" > .env
npm run build
```

**Start Services:**

Create a startup script `start_server.sh` (Linux/Mac) or `start_server.bat` (Windows):

```bash
#!/bin/bash
# start_server.sh

# Start backend
cd py_server
source venv/bin/activate
uvicorn app.main:app --host 0.0.0.0 --port 8000 &

# Start frontend (serve built files)
cd ../react_web
npx serve -s dist -l 3000 &

echo "Services started!"
echo "Backend: http://192.168.1.100:8000"
echo "Frontend: http://192.168.1.100:3000"
```

Windows version (`start_server.bat`):
```batch
@echo off
cd py_server
call venv\Scripts\activate
start uvicorn app.main:app --host 0.0.0.0 --port 8000

cd ..\react_web
start npx serve -s dist -l 3000

echo Services started!
echo Backend: http://192.168.1.100:8000
echo Frontend: http://192.168.1.100:3000
```

#### 2. Client Device Setup

**Connect to Network:**
- Connect all devices to same WiFi/LAN
- No internet required

**Access Application:**
- Open browser on any device
- Navigate to: `http://192.168.1.100:3000`
- Start diagnosing patients!

#### 3. Auto-Start on Boot (Optional)

**Linux (systemd):**

Create `/etc/systemd/system/health-assistant.service`:
```ini
[Unit]
Description=Health Assistant Service
After=network.target

[Service]
Type=simple
User=youruser
WorkingDirectory=/path/to/project
ExecStart=/path/to/project/start_server.sh
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable:
```bash
sudo systemctl enable health-assistant
sudo systemctl start health-assistant
```

**Windows (Task Scheduler):**
1. Open Task Scheduler
2. Create Basic Task
3. Trigger: At startup
4. Action: Start program → `start_server.bat`

---

## Option 3: Hybrid Deployment

Combine cloud and local deployment for maximum flexibility.

### Setup

1. **Deploy to cloud** (Render + Vercel) for online access
2. **Setup local server** for offline use
3. **Configure frontend** with fallback:

```javascript
// apiClient.js
const API_BASE_URL = 
  import.meta.env.VITE_API_BASE_URL || 
  'http://192.168.1.100:8000/api/v1' || // Local fallback
  'https://your-app.onrender.com/api/v1'; // Cloud
```

---

## Database Considerations

### SQLite (Default)
- **Pros**: No setup, works offline, portable
- **Cons**: Single-file, limited concurrency
- **Best for**: Small clinics, offline use

### MongoDB (Optional)
- **Pros**: Scalable, cloud-ready
- **Cons**: Requires setup, internet for cloud
- **Best for**: Multi-clinic deployments

**To use MongoDB:**
1. Set `MONGO_URI` environment variable
2. Auth/users will use MongoDB
3. Diagnosis still uses SQLite

---

## Performance Optimization

### Backend

1. **Use Production ASGI Server**
   ```bash
   # Instead of uvicorn, use gunicorn with uvicorn workers
   pip install gunicorn
   gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker
   ```

2. **Enable Caching**
   - Add Redis for caching (optional)
   - Cache diagnosis results

3. **Optimize ONNX Model**
   - Use quantized model for faster inference
   - Enable ONNX optimizations

### Frontend

1. **Build Optimization**
   ```bash
   npm run build
   # Vite automatically optimizes
   ```

2. **Enable Compression**
   - Serve with gzip/brotli compression
   - Use CDN for static assets (if online)

3. **Image Optimization**
   - Compress images before upload
   - Limit image size (max 5MB)

---

## Security Considerations

### Production Checklist

- [ ] Change `JWT_SECRET_KEY` to secure random value
- [ ] Enable HTTPS (use Let's Encrypt)
- [ ] Configure CORS for specific origins
- [ ] Enable rate limiting
- [ ] Add input validation
- [ ] Sanitize file uploads
- [ ] Regular security updates
- [ ] Backup database regularly

### HTTPS Setup (Render)

Render provides automatic HTTPS. For local deployment:

```bash
# Generate self-signed certificate (development only)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes

# Run with HTTPS
uvicorn app.main:app --ssl-keyfile=key.pem --ssl-certfile=cert.pem
```

---

## Monitoring

### Health Checks

```bash
# Backend health
curl https://your-app.onrender.com/api/v1/health

# Expected response
{"status":"ok","mongo":"connected"}
```

### Logs

**Render:**
- View logs in Render dashboard
- Enable log persistence

**Local:**
```bash
# Backend logs
tail -f py_server/logs/app.log

# System logs
journalctl -u health-assistant -f
```

---

## Backup & Recovery

### Backup SQLite Database

```bash
# Backup
cp py_server/diagnosis.db py_server/diagnosis.db.backup

# Automated backup (cron)
0 0 * * * cp /path/to/diagnosis.db /path/to/backups/diagnosis-$(date +\%Y\%m\%d).db
```

### Restore

```bash
cp py_server/diagnosis.db.backup py_server/diagnosis.db
```

---

## Troubleshooting

### Common Issues

**Backend won't start:**
```bash
# Check Python version
python --version  # Should be 3.10+

# Check dependencies
pip list

# Check port availability
lsof -i :8000  # Mac/Linux
netstat -ano | findstr :8000  # Windows
```

**Frontend can't connect to backend:**
```bash
# Check VITE_API_BASE_URL
cat react_web/.env

# Test backend directly
curl http://localhost:8000/api/v1/health

# Check CORS settings in app/main.py
```

**Slow performance:**
- Check server resources (CPU, RAM)
- Optimize image sizes
- Use production build
- Enable caching

---

## Scaling

### Horizontal Scaling

**Load Balancer:**
```
        ┌─────────────┐
        │Load Balancer│
        └──────┬──────┘
               │
       ┌───────┴───────┐
       │               │
   ┌───▼───┐       ┌───▼───┐
   │API #1 │       │API #2 │
   └───────┘       └───────┘
```

**Setup:**
1. Deploy multiple backend instances
2. Use Nginx or cloud load balancer
3. Share SQLite via network filesystem (or use MongoDB)

### Vertical Scaling

- Upgrade server resources
- Use faster CPU for ONNX inference
- Add more RAM for caching

---

## Cost Estimation

### Cloud Deployment (Render + Vercel)

**Free Tier:**
- Render: Free (with limitations)
- Vercel: Free (hobby plan)
- **Total**: $0/month

**Paid Tier:**
- Render: $7-25/month
- Vercel: $20/month
- **Total**: $27-45/month

### Local Deployment

**Hardware:**
- Server: $300-500 (one-time)
- Router: $50-100 (one-time)
- **Total**: $350-600 (one-time)

**Operating Costs:**
- Electricity: ~$5-10/month
- Maintenance: Minimal

---

## Support

For deployment issues:
1. Check logs first
2. Review this guide
3. Test locally before deploying
4. Verify environment variables
5. Check network connectivity

---

**Ready to deploy! 🚀**

Choose the deployment option that best fits your use case and follow the steps above.
