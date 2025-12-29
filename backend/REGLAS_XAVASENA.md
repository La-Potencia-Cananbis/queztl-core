# 🦅 REGLAS DE XAVASENA - NUNCA OLVIDES ESTO, PENDEJO!

## ❌ LO QUE NUNCA HACER (CRITICAL - READ FIRST!)

### 1. **NO LOCAL HOST - JAMÁS!**
- ❌ NO correr nada en el Mac (localhost:3000, localhost:8000, etc.)
- ❌ NO instalar dependencias en el Mac (pip install, npm install local)
- ❌ NO usar recursos del Mac para servicios
- ❌ NO "python3 -m http.server" en el Mac
- ❌ NO background processes en el Mac
- ✅ TODO debe correr en la NUBE (Render.com, Netlify, etc.)

### 2. **NO MEZCLAR SERVICIOS**
- ❌ NO poner todo en la misma URL
- ❌ NO "throw everything on lapotenciacann.com"
- ✅ Cada servicio necesita su PROPIA URL
- ✅ Arquitectura multi-sitio siempre

### 3. **NO DEPENDENCIES EN MAC**
- ❌ NO "pip3 install requests" en el Mac
- ❌ NO "npm install" localmente
- ❌ NO instalar nada que requiera el Mac para correr
- ✅ Solo git commands para push a la nube

## ✅ LO QUE SÍ HACER (EL ESTILO XAVASENA)

### 1. **TODO AUTÓNOMO EN LA NUBE**
```
Backend → Render.com (https://queztl-core-backend.onrender.com)
Frontend → Netlify (auto-deploy desde GitHub)
Cada servicio → Su propia URL subdomain
```

### 2. **ARQUITECTURA MULTI-SITIO**
```
Público: lapotenciacann.com
Portal: portal.lapotenciacann.com
5K Renderer: render.lapotenciacann.com
GIS Studio: gis.lapotenciacann.com
3D Benchmark: 3dmark.lapotenciacann.com
Mining: mining.lapotenciacann.com
VMs: vms.lapotenciacann.com
```

### 3. **WORKFLOW CORRECTO**
```
1. Edit code
2. git commit
3. git push origin main
4. Render/Netlify auto-deploy
5. Test en URLs cloud
6. DONE - Mac puede apagarse
```

### 4. **CUANDO SUBIR ALGO (Video, Archivo, etc.)**
- Backend endpoint con UploadFile (FastAPI)
- Procesar en el servidor (Render)
- Devolver resultado via URL o base64
- NO procesar en el Mac

### 5. **TESTING**
- ✅ curl a URLs cloud
- ✅ Browser a URLs cloud
- ❌ NO "localhost" anything

## 🎯 COMANDOS PERMITIDOS EN MAC

### Git Operations (OK)
```bash
git add .
git commit -m "message"
git push origin main
git status
```

### Testing Cloud Services (OK)
```bash
curl https://queztl-core-backend.onrender.com/api/...
curl https://lapotenciacann.com
```

### File Editing (OK)
```bash
code backend/main.py
vim dashboard/index.html
```

## 🚫 COMANDOS PROHIBIDOS EN MAC

### NO Background Services
```bash
❌ python3 -m http.server 8000 &
❌ npm run dev &
❌ uvicorn main:app &
❌ nohup python script.py &
```

### NO Local Installs
```bash
❌ pip3 install anything
❌ npm install anything
❌ brew install anything-for-services
```

### NO Local Execution
```bash
❌ python script.py (unless just for editing/testing logic)
❌ node server.js
❌ ./run-local.sh
```

## 💡 ESTILO DE COMUNICACIÓN XAVASENA

- **Directo y claro**: "No localhost buey"
- **Sin juegos**: "Sie,pre e tiras loco por tener cosas corriendo en my Mac"
- **Chicano style**: "Dale", "Órale", "Listo ese", "Bueno later"
- **No bullshit**: Si algo no jala, dilo directo
- **Get it done**: "Do it an bueno later!"

## 🦅 PRIORIDADES XAVASENA

1. **Autonomía** - Sistema corre solo sin el Mac
2. **Cloud-first** - Todo en Render/Netlify/cloud
3. **Separation** - Cada servicio su URL
4. **Real functionality** - No synthetic benchmarks, REAL shit (video processing, etc.)
5. **Production ready** - No demos, sistemas que funcionan

## 📝 CUANDO CREAR CÓDIGO

### Backend (Python)
- Siempre en `/backend/`
- Push a GitHub
- Render auto-deploys
- Test en https://queztl-core-backend.onrender.com

### Frontend (HTML/JS/React)
- Separate folder para cada servicio
- Push a GitHub
- Netlify auto-deploys
- Each gets subdomain

### NO crear:
- Scripts que corren en Mac
- Servidores locales
- Processes que necesitan Mac prendido

## 🎬 EJEMPLO: 5K VIDEO RENDERER (LO QUE QUIERES)

### ❌ MAL (Vieja forma)
```python
# Processar video en Mac
cap = cv2.VideoCapture('local_video.mp4')
# Mac hace el trabajo
```

### ✅ BIEN (Estilo Xavasena)
```python
@app.post("/api/render/5k-video")
async def render_video(file: UploadFile):
    # Upload video a backend cloud
    # Render.com procesa (GPU cloud)
    # Devuelve download URL
    # Mac NO hace nada
```

## 🔥 RECORDATORIOS FINALES

1. **"Te dije que nada local"** - Significa NO LOCALHOST, todo cloud
2. **"Don't throw everything on the same URL"** - Cada servicio su URL
3. **"Deply netlify buey"** - Push a GitHub, deja que Netlify auto-deploy
4. **"Esta tiene que hacer system donde puedo subir video"** - Backend endpoint con upload, proceso en cloud

## ✅ CHECKLIST ANTES DE HACER ALGO

- [ ] ¿Va a correr en el Mac? → ❌ NO LO HAGAS
- [ ] ¿Necesita el Mac prendido? → ❌ REDISEÑA
- [ ] ¿Está en la misma URL que otro servicio? → ❌ SEPARA
- [ ] ¿Es un demo/synthetic? → ❌ HAZLO REAL
- [ ] ¿Auto-deploy desde GitHub? → ✅ PERFECTO
- [ ] ¿Cada servicio su URL? → ✅ PERFECTO
- [ ] ¿Corre en cloud sin Mac? → ✅ PERFECTO

---

**LÉELO CADA VEZ QUE EMPIEZES A TRABAJAR, PENDEJO! 🦅**

**NO MÁS LOCALHOST. NO MÁS MAC RESOURCES. TODO EN LA NUBE, CARNAL!**
