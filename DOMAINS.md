# Domain Configuration

## Queztl-Core (Technical Platform)
**Domain**: senasaitech.com
**Purpose**: Distributed computing platform, monitoring, cluster management
**Content**: 
- Performance dashboards
- Cluster monitoring
- Stress testing tools
- GIS platforms
- 3D demos
- Contact forms

**Deploy**: `~/queztl-core/frontend/`

---

## New Mexico Socialists (Political Activism)
**Domain**: newmexicosocialists.com  
**Purpose**: Revolutionary propaganda, meme generation, theory library
**Content**:
- AI-generated propaganda
- Communist theory database
- Meme generator UI
- Facebook auto-posting

**Deploy**: `~/queztl-core/nm-socialists-project/`

---

## DNS Configuration
Both sites use the same Beast + Sloth cluster but serve different content.

```bash
# Point both domains to your public IP
senasaitech.com          -> Your-Public-IP:8080
newmexicosocialists.com  -> Your-Public-IP:8081
```

## Nginx Virtual Hosts
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
