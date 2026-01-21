# GIS Canonical Selection

**Canonical page:** `frontend/gis-studio-pro.html`

**Why:** most complete/modern variant among existing GIS pages.

**Next steps to make it live:**
1) Serve via nginx alongside main site (copy into web root or mount as /gis/).
2) Wire data/API calls to FastAPI endpoints (once cluster stable).
3) Remove/ignore other GIS variants after validation: `gis-real.html`, `gis-simple.html`, `gis-studio-dashboard.html`, `gis-studio-integrated.html`, `gis-studio.html`, `gis-work.html`, `gis.html`.

**Minimal hosting option now:**
- Copy `frontend/gis-studio-pro.html` and supporting assets to `/var/www/frontend-new/gis/` and link from main site when ready.
