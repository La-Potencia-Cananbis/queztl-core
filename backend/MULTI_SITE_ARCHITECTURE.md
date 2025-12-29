# QuetzalCore Multi-Site Architecture
## Separate URLs for Each Service

## 🦅 Main Sites

1. **Public Landing Page**
   - URL: https://lapotenciacann.com
   - Purpose: Public-facing marketing/info
   - Status: ✅ LIVE

2. **SenasAI Tech Corporate**
   - URL: https://senasaitech.com
   - Purpose: Corporate site, business info
   - Status: ✅ LIVE (same deployment as above for now)

## 🎯 Service-Specific URLs (Need to Deploy)

3. **QuetzalCore Portal** (Testing Dashboard)
   - Suggested URL: portal.lapotenciacann.com
   - Purpose: Internal testing dashboard with all services
   - Features: 5K Renderer, 3D Workload, GIS Studio, Mining, VM Console
   - Status: 🔧 CREATING NOW

4. **5K Renderer Studio**
   - Suggested URL: render.lapotenciacann.com
   - Purpose: Dedicated 5K rendering interface
   - Status: 🔧 NEED TO CREATE

5. **GIS Studio**
   - Suggested URL: gis.lapotenciacann.com
   - Purpose: Professional GIS processing
   - Status: 🔧 NEED TO CREATE

6. **3D Benchmark**
   - Suggested URL: 3dmark.lapotenciacann.com
   - Purpose: 3D performance testing
   - Status: 🔧 NEED TO CREATE

7. **Mining Dashboard**
   - Suggested URL: mining.lapotenciacann.com
   - Purpose: Crypto mining operations
   - Status: 🔧 NEED TO CREATE

8. **VM Console**
   - Suggested URL: vms.lapotenciacann.com
   - Purpose: Virtual machine management
   - Status: 🔧 NEED TO CREATE

## 📋 Deployment Strategy

### Option 1: Netlify Subdomains (Easiest)
- Create separate Netlify sites for each service
- Point subdomains to each site
- Each gets its own URL and deployment

### Option 2: Separate Repos (Most Flexible)
- Create separate repo for each service
- Deploy each to its own Netlify/Vercel
- Full independence

### Recommended: Start with Netlify Subdomains
1. Create QuetzalCore Portal first (testing dashboard)
2. Then create individual service sites
3. Configure DNS in Netlify for subdomains

## 🚀 Next Steps
1. Create QuetzalCore Portal with all services integrated
2. Deploy to Netlify as new site
3. Configure portal.lapotenciacann.com subdomain
4. Test everything there
5. Then create individual service sites
