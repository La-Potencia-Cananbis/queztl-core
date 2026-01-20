# Queztl Website System - Quick Reference

## 🚀 Quick Commands

```bash
# Initial setup (run once)
cd ~/queztl-core
./setup-website.sh

# Start all services
./start.sh

# Stop all services
./stop-services.sh

# Check status
curl http://localhost:8003/health
curl http://localhost:8080
```

## 📦 What You Have Now

### ✅ Completed Features

1. **Contact Form System**
   - Beautiful responsive form at `/frontend/contact.html`
   - FastAPI backend with email + database
   - Stores member info in SQLite
   - Sends email notifications via SMTP
   - Admin endpoints for member management

2. **Dynamic Content Generator**
   - Auto-generates memes using Beast API
   - 3 themes: Revolutionary, Tech, Nature
   - Runs every 30 minutes (configurable)
   - Caches locally, uploads to Sloth
   - Facebook auto-posting ready (needs Meta API key)

3. **Service Management**
   - `setup-website.sh` - Interactive setup wizard
   - `start-services.sh` - Start all services
   - `stop-services.sh` - Stop all services
   - `start.sh` - Quick start with loaded configs

4. **Database System**
   - SQLite on Sloth for member data
   - Contact submissions tracking
   - Statistics and analytics endpoints

## 🔧 Configuration Files

```
~/queztl-core/
├── .config/
│   ├── email.env       # SMTP credentials
│   ├── dyndns.env      # DynDNS domain
│   └── meta.env        # Facebook API key
├── data/
│   └── members.db      # Member database
├── logs/
│   ├── contact_api.log
│   ├── content_runner.log
│   └── webserver.log
└── frontend/generated/ # Generated memes
```

## 🌐 Access Points

| Service | URL | Purpose |
|---------|-----|---------|
| Website | http://localhost:8080 | Main site |
| Contact Form | http://localhost:8080/contact.html | Member signup |
| Contact API | http://localhost:8003 | Form backend |
| Beast API | http://192.168.1.105:8001 | Image generation |
| Sloth Storage | http://192.168.1.102:8000 | Permanent storage |

## 📊 Database Schema

```sql
members (
  id INTEGER PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT UNIQUE NOT NULL,
  phone TEXT,
  message TEXT,
  member_type TEXT,     -- 'recruit', 'member', 'supporter'
  submitted_at TIMESTAMP,
  contacted BOOLEAN
)
```

## 🔌 API Endpoints

### Contact API (Port 8003)

```bash
# Submit form
POST /submit
{
  "name": "John Doe",
  "email": "john@example.com",
  "phone": "555-1234",
  "message": "Hello",
  "member_type": "recruit"
}

# Get all members
GET /members

# Get statistics
GET /stats

# Mark as contacted
PATCH /members/{id}/contacted

# Health check
GET /health
```

## 🎨 Content Runner Options

```bash
# Single run (generate once)
python3 backend/content_runner.py --single

# Continuous (every 30 min)
python3 backend/content_runner.py --continuous

# Custom interval (every 60 min)
python3 backend/content_runner.py --continuous --interval 60

# With Facebook posting
python3 backend/content_runner.py --continuous --facebook
```

## 📝 Monitoring Commands

```bash
# View logs
tail -f ~/queztl-core/logs/contact_api.log
tail -f ~/queztl-core/logs/content_runner.log
tail -f ~/queztl-core/logs/webserver.log

# Check processes
ps aux | grep "contact_form_api\|content_runner\|http.server"

# Test APIs
curl http://localhost:8003/health
curl http://192.168.1.105:8001/health

# View database
sqlite3 ~/queztl-core/data/members.db "SELECT * FROM members;"
sqlite3 ~/queztl-core/data/members.db "SELECT COUNT(*) FROM members;"
```

## ⚙️ Email Setup (Gmail)

1. Enable 2-Factor Authentication in Google Account
2. Go to Security → App Passwords
3. Generate password for "Mail"
4. Use in `setup-website.sh` or add to `.config/email.env`:

```bash
export SMTP_SERVER="smtp.gmail.com"
export SMTP_PORT="587"
export SENDER_EMAIL="your-email@gmail.com"
export SENDER_PASSWORD="your-app-password"
export RECIPIENT_EMAIL="admin@gmail.com"
```

## 🌍 DynDNS Setup

**Quick DuckDNS Example:**

```bash
# Install
mkdir ~/duckdns
echo "url='https://www.duckdns.org/update?domains=YOUR_DOMAIN&token=YOUR_TOKEN&ip=' | curl -k -o ~/duckdns/duck.log -K -" > ~/duckdns/duck.sh
chmod +x ~/duckdns/duck.sh

# Add to cron (update every 5 min)
crontab -e
# Add: */5 * * * * ~/duckdns/duck.sh >/dev/null 2>&1

# Configure router port forwarding: 80 -> 8080
```

## 📱 Facebook Auto-Posting

When Meta approves your app:

1. Get access token from Facebook Developer Console
2. Add to `.config/meta.env`:
   ```bash
   export META_API_KEY="your-meta-api-key"
   ```
3. Start with Facebook posting:
   ```bash
   python3 backend/content_runner.py --continuous --facebook
   ```

## 🔐 Security Checklist

- [ ] Use Gmail App Password, not main password
- [ ] Protect `.config/*.env` files (chmod 600)
- [ ] Add JWT auth for admin endpoints
- [ ] Set up HTTPS with Let's Encrypt
- [ ] Implement rate limiting on contact form
- [ ] Regular database backups
- [ ] Configure Mac firewall
- [ ] Update CORS origins to your domain

## 🐛 Troubleshooting

**Contact form not working?**
```bash
# Check API
curl http://localhost:8003/health

# View logs
tail -f ~/queztl-core/logs/contact_api.log

# Test manually
curl -X POST http://localhost:8003/submit \
  -H "Content-Type: application/json" \
  -d '{"name":"Test","email":"test@example.com","phone":"","message":"Test","member_type":"recruit"}'
```

**Content runner fails?**
```bash
# Check Beast
curl http://192.168.1.105:8001/health

# Check dependencies
pip3 list | grep aiohttp

# View logs
tail -f ~/queztl-core/logs/content_runner.log
```

**Can't access from network?**
```bash
# Check if running
sudo lsof -i :8080

# Test from another machine
curl http://YOUR_MAC_IP:8080

# Check Mac firewall
sudo /usr/libexec/ApplicationFirewall/socketfilterfw --getglobalstate
```

## 📚 Full Documentation

See `WEBSITE_SETUP.md` for complete details on:
- Architecture diagrams
- Advanced configuration
- Custom meme templates
- Production deployment
- SSL/HTTPS setup
- Database management
- API documentation

## 🚀 Next Steps

1. Run setup wizard: `./setup-website.sh`
2. Configure email credentials
3. Start services: `./start.sh`
4. Test contact form locally
5. Set up DynDNS for public access
6. Configure SSL certificate
7. Wait for Meta API approval
8. Mount Sloth storage permanently

---

**Status:** ✅ All components built and ready to use!
