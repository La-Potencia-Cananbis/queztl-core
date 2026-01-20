# Queztl Dynamic Website System

## 🌐 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                  Mac (Web Server + DynDNS)                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐     │
│  │ Web Server   │  │ Contact API  │  │ Content      │     │
│  │ Port 8080    │  │ Port 8003    │  │ Runner       │     │
│  └──────────────┘  └──────────────┘  └──────────────┘     │
└────────────┬───────────────┬──────────────┬────────────────┘
             │               │              │
             │               │              │ Image Generation
             │               │              ▼
             │               │         ┌─────────────────┐
             │               │         │ Beast           │
             │               │         │ 192.168.1.105   │
             │               │         │ Port 8001       │
             │               │         └─────────────────┘
             │               │
             │               │ Database + Storage
             │               ▼
             │          ┌─────────────────┐
             │          │ Sloth           │
             │          │ 192.168.1.102   │
             │          │ Port 8000       │
             │          └─────────────────┘
             │
             │ Public Access
             ▼
        DynDNS Domain
```

## 🚀 Quick Start

### 1. Configure Email (Required for Contact Form)

Edit `start-services.sh` and update:

```bash
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"  # Gmail App Password
export RECIPIENT_EMAIL="admin-email@gmail.com"
```

**Gmail App Password Setup:**
1. Go to Google Account → Security
2. Enable 2-Factor Authentication
3. Generate App Password for "Mail"
4. Use that password in the script

### 2. Start All Services

```bash
cd ~/queztl-core
./start-services.sh
```

This starts:
- ✅ Web server on port 8080
- ✅ Contact API on port 8003
- ✅ Content runner (generates memes every 30 min)

### 3. Access the Website

- **Local:** http://localhost:8080
- **Network:** http://your-mac-ip:8080
- **Contact Form:** http://localhost:8080/contact.html

### 4. Stop Services

```bash
./stop-services.sh
```

## 📦 Components

### 1. Contact Form API (`backend/contact_form_api.py`)

**Features:**
- ✉️ Email notifications via SMTP
- 💾 SQLite database for member storage
- 🔐 CORS-enabled for frontend
- 📊 Stats and member management endpoints

**Endpoints:**
- `POST /submit` - Submit contact form
- `GET /members` - List all members (admin)
- `GET /stats` - Get statistics
- `PATCH /members/{id}/contacted` - Mark as contacted
- `GET /health` - Health check

**Database Schema:**
```sql
members (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  message TEXT,
  member_type TEXT,  -- recruit, member, supporter
  submitted_at TIMESTAMP,
  contacted BOOLEAN
)
```

### 2. Content Runner (`backend/content_runner.py`)

**Features:**
- 🎨 Auto-generates memes using Beast API
- 💾 Caches images locally on Mac
- 📤 Uploads to Sloth for permanent storage
- 📱 Facebook auto-posting (ready for Meta API)
- ⏱️ Runs every 30 minutes

**Configuration:**
```python
BEAST_URL = "http://192.168.1.105:8001"
SLOTH_STORAGE = "http://192.168.1.102:8000"
LOCAL_CACHE = ~/queztl-core/frontend/generated
```

**Meme Themes:**
- Revolutionary (socialist realism style)
- Tech (cyberpunk aesthetic)
- Nature (photorealistic landscapes)

**Usage:**
```bash
# Single run
python3 backend/content_runner.py --single

# Continuous (every 30 min)
python3 backend/content_runner.py --continuous

# Custom interval
python3 backend/content_runner.py --continuous --interval 60
```

### 3. Frontend Contact Form (`frontend/contact.html`)

**Features:**
- 📱 Responsive design
- ✨ Beautiful gradient UI
- ✅ Form validation
- 🎯 Real-time submission feedback
- 📧 Automatic email notifications

**Form Fields:**
- Name (required)
- Email (required)
- Phone (optional)
- Interest type (required)
- Message (required)

## 🔧 Configuration

### Mount Sloth Storage (For Production)

```bash
# Create mount point
mkdir -p ~/sloth-storage

# Mount via NFS (example)
mount -t nfs 192.168.1.102:/storage ~/sloth-storage

# Or via SMB
mount -t smbfs //192.168.1.102/storage ~/sloth-storage

# Update environment variable
export SLOTH_DB_PATH="$HOME/sloth-storage/queztl/members.db"
```

### DynDNS Setup

1. **Choose Provider:** No-IP, DuckDNS, Dynu, etc.
2. **Install Client:**
   ```bash
   # Example: DuckDNS
   echo "url='https://www.duckdns.org/update?domains=YOUR_DOMAIN&token=YOUR_TOKEN&ip=' | curl -k -o ~/duckdns/duck.log -K -" > ~/duckdns/duck.sh
   chmod +x ~/duckdns/duck.sh
   ```
3. **Set Cron Job:**
   ```bash
   crontab -e
   # Add: */5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1
   ```
4. **Port Forwarding:** Forward ports 80/443 to Mac's 8080

### Facebook API Integration

When Meta approves your app:

1. **Get Access Token** from Facebook Developer Console
2. **Update Content Runner:**
   ```python
   # In backend/content_runner.py
   META_API_KEY = "your-meta-api-key"
   ```
3. **Enable Auto-Posting:**
   ```bash
   python3 backend/content_runner.py --continuous --facebook
   ```

## 📊 Monitoring

### Check Service Status

```bash
# View logs
tail -f ~/queztl-core/logs/contact_api.log
tail -f ~/queztl-core/logs/content_runner.log
tail -f ~/queztl-core/logs/webserver.log

# Check processes
ps aux | grep "contact_form_api\|content_runner\|http.server"

# Test APIs
curl http://localhost:8003/health
curl http://localhost:8080
curl http://192.168.1.105:8001/health
```

### View Member Database

```bash
# SQLite CLI
sqlite3 ~/queztl-core/data/members.db

# Queries
sqlite3 ~/queztl-core/data/members.db "SELECT * FROM members;"
sqlite3 ~/queztl-core/data/members.db "SELECT COUNT(*) FROM members;"
```

### API Stats

```bash
# Get statistics
curl http://localhost:8003/stats

# List members
curl http://localhost:8003/members
```

## 🔐 Security Considerations

### Production Checklist

- [ ] **Email Credentials:** Use app-specific passwords, not main password
- [ ] **Environment Variables:** Store secrets in `.env` file, not in scripts
- [ ] **API Authentication:** Add JWT tokens for admin endpoints
- [ ] **HTTPS:** Use Let's Encrypt for SSL certificates
- [ ] **Rate Limiting:** Implement rate limiting on contact form
- [ ] **CORS:** Restrict origins to your domain only
- [ ] **Database Backups:** Regular backups of members.db
- [ ] **Firewall:** Configure Mac firewall rules

### Recommended `.env` Setup

Create `~/queztl-core/.env`:
```bash
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SENDER_EMAIL=your-email@gmail.com
SENDER_PASSWORD=your-app-password
RECIPIENT_EMAIL=admin@gmail.com
SLOTH_DB_PATH=/path/to/sloth/storage/members.db
META_API_KEY=your-facebook-api-key
```

Load in scripts:
```bash
set -a
source ~/queztl-core/.env
set +a
```

## 🎨 Customization

### Add Custom Meme Templates

Edit `backend/content_runner.py`:

```python
MEME_TEMPLATES = {
    "your_theme": [
        {
            "prompt": "your prompt here",
            "style": "your style",
            "caption": "Your Caption"
        }
    ]
}
```

### Modify Contact Form Fields

Edit `frontend/contact.html` and `backend/contact_form_api.py` to add fields.

### Change Ports

Update in respective scripts:
- Web Server: Change `8080` in `start-services.sh`
- Contact API: Change `8003` in `contact_form_api.py`
- Beast: Configure at Beast server

## 🐛 Troubleshooting

### Contact Form Not Submitting

1. Check API is running: `curl http://localhost:8003/health`
2. View logs: `tail -f ~/queztl-core/logs/contact_api.log`
3. Check CORS settings in `contact_form_api.py`
4. Verify frontend API URL in `contact.html`

### Email Not Sending

1. Verify SMTP credentials
2. Check Gmail App Password is correct
3. Ensure 2FA is enabled on Gmail
4. Check logs for SMTP errors
5. Test manually:
   ```bash
   python3 -c "import smtplib; print('SMTP OK')"
   ```

### Content Runner Fails

1. Check Beast is online: `curl http://192.168.1.105:8001/health`
2. Verify aiohttp is installed: `pip3 list | grep aiohttp`
3. Check permissions on generated/ folder
4. View logs: `tail -f ~/queztl-core/logs/content_runner.log`

### Can't Access from Network

1. Check Mac firewall settings
2. Verify ports are open: `sudo lsof -i :8080`
3. Test from another machine: `curl http://mac-ip:8080`
4. Check router port forwarding

## 📝 Development

### Install Dependencies

```bash
pip3 install fastapi uvicorn aiohttp python-multipart
```

### Test Contact API

```bash
# Start API
python3 backend/contact_form_api.py

# Test submission
curl -X POST http://localhost:8003/submit \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Test User",
    "email": "test@example.com",
    "phone": "555-1234",
    "message": "Test message",
    "member_type": "recruit"
  }'
```

### Test Content Runner

```bash
# Single run
python3 backend/content_runner.py --single

# Check generated images
ls -lh ~/queztl-core/frontend/generated/
```

## 🚀 Next Steps

1. **Configure Email** - Update SMTP credentials
2. **Mount Sloth** - Set up network storage
3. **DynDNS** - Configure public domain
4. **SSL/HTTPS** - Set up Let's Encrypt
5. **Facebook API** - Complete Meta approval
6. **Monitoring** - Set up uptime monitoring
7. **Backups** - Automated database backups

## 📚 Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Gmail App Passwords](https://support.google.com/accounts/answer/185833)
- [DuckDNS Setup](https://www.duckdns.org/install.jsp)
- [Meta for Developers](https://developers.facebook.com/)

---

**Questions?** Check logs in `~/queztl-core/logs/` or open an issue on GitHub.
