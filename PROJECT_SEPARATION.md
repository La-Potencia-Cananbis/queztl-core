# Project Separation Complete ✅

Two distinct projects using the same infrastructure:

---

## 🦅 Sena's AI Tech (senasaitech.com)
**Technical distributed computing platform**

### Purpose:
- High-performance cluster management
- Performance monitoring and benchmarking
- GIS/mapping tools
- 3D graphics demonstrations
- Professional technical services

### Files:
```
~/queztl-core/frontend/
├── home.html           ← Main landing page
├── index.html          ← Monitoring dashboard
├── contact.html        ← Contact form
├── gis-*.html          ← GIS platforms
├── 3dmark-*.html       ← 3D showcases
└── web3-*.html         ← Web3 features
```

### Branding:
- Professional/technical
- Blue/purple gradients
- Clean modern design
- Focus on performance and reliability

---

## 🚩 New Mexico Socialists (newmexicosocialists.com)
**Political activism and propaganda generation**

### Purpose:
- Revolutionary propaganda creation
- AI-generated socialist memes
- Communist theory library
- Facebook auto-posting
- Political organizing

### Files:
```
~/queztl-core/nm-socialists-project/
├── backend/
│   ├── communist_theory_library.py
│   ├── meme_generator.py
│   ├── content_runner.py
│   ├── facebook_meme_poster.py
│   └── auto_meme_poster.py
├── frontend/
│   ├── beast_image_ui.html
│   └── theory_library.html
└── README.md
```

### Branding:
- Red/revolutionary theme
- Bold socialist imagery
- Activist-focused
- Propaganda aesthetic

---

## Shared Infrastructure

Both projects use the same cluster:

- **Beast** (192.168.1.105) - GPU for image generation
- **Sloth** (192.168.1.102) - Storage and services
- **Optiplexes** (Coming Tuesday) - Additional compute

But serve **completely separate content** through different domains.

---

## Deployment Strategy

### Option 1: Different Ports (Current)
```bash
# Sena's AI Tech
cd ~/queztl-core/frontend && python3 -m http.server 8080

# NM Socialists  
cd ~/queztl-core/nm-socialists-project/frontend && python3 -m http.server 8081
```

Then point DNS:
- senasaitech.com → your-ip:8080
- newmexicosocialists.com → your-ip:8081

### Option 2: Nginx Virtual Hosts (Recommended)
```nginx
# /etc/nginx/sites-available/senasaitech
server {
    server_name senasaitech.com www.senasaitech.com;
    root /home/user/queztl-core/frontend;
    index home.html;
    listen 80;
}

# /etc/nginx/sites-available/newmexicosocialists
server {
    server_name newmexicosocialists.com www.newmexicosocialists.com;
    root /home/user/queztl-core/nm-socialists-project/frontend;
    index index.html;
    listen 80;
}
```

Both on port 80, nginx routes by domain name.

---

## Next Steps

1. **Deploy Sena's AI Tech** (senasaitech.com)
   - Already running at http://localhost:8080/home.html
   - Configure DNS A record
   - Setup SSL with Let's Encrypt

2. **Build NM Socialists frontend**
   - Create index.html landing page
   - Setup meme gallery
   - Integrate theory library UI

3. **Configure Nginx** (Monday after reimage)
   - Install on Beast or Sloth
   - Setup virtual hosts
   - Enable SSL for both domains

---

**No confusion, clean separation!** 🎯
