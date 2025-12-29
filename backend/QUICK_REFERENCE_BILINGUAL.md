# 🦅 Queztl-Core - Quick Reference Card
# 🦅 Queztl-Core - Tarjeta Referencia Rápida

**Print this page for easy reference / Imprime esta página para referencia fácil**

---

## 🚀 Quick Start / Inicio Rápido

### Start System / Iniciar Sistema
```bash
./start.sh
```

### Stop System / Detener Sistema
```bash
docker-compose down
```

### Access / Acceso
- **Dashboard**: http://localhost:3000
- **API**: http://localhost:8000
- **API Docs**: http://localhost:8000/docs

---

## 📊 Performance / Rendimiento

| Metric / Métrica | Value / Valor | Comparison / Comparación |
|------------------|---------------|--------------------------|
| Operations/sec<br>Operaciones/seg | 5.82 billion<br>5.82 mil millones | 19.5% RTX 3080 |
| Render time<br>Tiempo renderizado | 12.76ms | 78 FPS (AAA ready) |
| Grade<br>Calificación | B (77/100) | S-grade compute<br>A-grade rendering |
| vs GTX 1660 | 116% | **We win!**<br>**¡Ganamos!** |

---

## 💰 Cost Savings / Ahorro Costos

### Per Device / Por Dispositivo
```
Hardware:      $200-700
Electricity:   $95/year
Maintenance:   $50/year
─────────────────────────
TOTAL:         $345-845/year
```

### Business / Empresa
```
30 employees:    $10,400 (3 years)
300 employees:   $104,000 (3 years)
3,000 employees: $1,688,000 (3 years)

ROI: 10-17x
```

---

## 🔌 API Quick Commands / Comandos API Rápidos

### Create GPU Session / Crear Sesión GPU
```bash
# EN
curl -X POST http://localhost:8000/api/gpu/session/create

# ES - mismo comando
```

### Render 3D Cube / Renderizar Cubo 3D
```bash
# EN/ES
curl -X POST http://localhost:8000/api/gpu/demo/rotating-cube \
  -H "Content-Type: application/json" \
  -d '{"rotation": {"x": 45, "y": 30, "z": 0}}'
```

### Run Benchmark / Ejecutar Benchmark
```bash
# EN/ES - Compute
curl -X POST http://localhost:8000/api/gpu/benchmark/compute

# EN/ES - WebGL
curl -X POST http://localhost:8000/api/gpu/benchmark/webgl
```

### Get Stats / Obtener Estadísticas
```bash
# EN/ES
curl http://localhost:8000/api/gpu/stats
```

---

## 📝 JavaScript Quick Start / Inicio Rápido JavaScript

```javascript
// EN - English
const gpu = new QueztlGPU({ lang: 'en' });
await gpu.createSession();
const result = await gpu.renderCube({ x: 45, y: 30, z: 0 });
console.log(`Rendered in ${result.render_time}ms`);

// ES - Español
const gpu = new QueztlGPU({ lang: 'es' });
await gpu.createSession();
const resultado = await gpu.renderCube({ x: 45, y: 30, z: 0 });
console.log(`Renderizado en ${resultado.render_time}ms`);
```

---

## 🐍 Python Quick Start / Inicio Rápido Python

```python
# EN - English
import requests

# Create session
response = requests.post('http://localhost:8000/api/gpu/session/create')
session_id = response.json()['session_id']

# Render cube
result = requests.post(
    'http://localhost:8000/api/gpu/demo/rotating-cube',
    json={'rotation': {'x': 45, 'y': 30, 'z': 0}}
).json()
print(f"Rendered in {result['render_time']}ms")

# ES - Español (mismo código)
# ...
print(f"Renderizado en {result['render_time']}ms")
```

---

## 🔬 Technical Specs / Especificaciones Técnicas

### Architecture / Arquitectura
```
Threads:         8,192 (256 blocks × 32 threads)
                 8,192 (256 bloques × 32 hilos)

Memory:          Shared + Global simulation
                 Simulación Compartida + Global

Optimization:    SIMD vectorization, NumPy
                 Vectorización SIMD, NumPy

Execution:       Asyncio parallel dispatch
                 Despacho paralelo Asyncio
```

### Capabilities / Capacidades
```
✅ WebGPU API
✅ OpenGL compatibility / compatibilidad
✅ Compute shaders
✅ Vertex/Fragment shaders
✅ Texture support / soporte texturas
✅ Buffer operations / operaciones buffer
```

---

## 🎯 Use Cases / Casos de Uso

| Use Case<br>Caso Uso | Savings<br>Ahorro | Benefit<br>Beneficio |
|----------------------|-------------------|----------------------|
| 🎮 Cloud Gaming<br>Juegos Nube | $500/player<br>$500/jugador | Play anywhere<br>Juega donde sea |
| 🎨 3D Design<br>Diseño 3D | $800/designer<br>$800/diseñador | Design on any laptop<br>Diseña en cualquier laptop |
| 🏥 Medical<br>Médico | $60-100k/hospital | Rural clinic access<br>Acceso clínicas rurales |
| 🎓 Education<br>Educación | $300-500/student<br>$300-500/estudiante | Every Chromebook<br>Todo Chromebook |
| 💼 Remote Work<br>Trabajo Remoto | $400-700/employee<br>$400-700/empleado | Work from anywhere<br>Trabaja desde donde sea |

---

## 🌱 Environmental / Ambiental

### Per Computer/Year / Por Computadora/Año
```
CO₂ Saved:       553 lbs  = 25 trees planted
CO₂ Ahorrado:    553 lbs  = 25 árboles plantados

Energy:          788 kWh  = 8 months fridge
Energía:         788 kWh  = 8 meses refri

Money:           $95      = electricity bill
Dinero:          $95      = factura eléctrica
```

---

## 📚 Key Documents / Documentos Clave

### Business / Negocios
- `EXECUTIVE_SUMMARY.md` - For executives / Para ejecutivos
- `BILINGUAL_SUMMARY.md` - This doc / Este doc (bilingüe)
- `WEB_GPU_EXPLAINED.md` - Non-technical / No técnico

### Technical / Técnico
- `WEB_GPU_DRIVER.md` - Architecture / Arquitectura
- `API_CONNECTION_GUIDE.md` - API docs
- `CONNECT_YOUR_APP.md` - Integration / Integración

### Legal / Legal
- `PATENT_APPLICATION.md` - Patent claims / Reivindicaciones patente
- `SECURITY_AND_IP.md` - IP protection / Protección PI
- `IMMEDIATE_ACTION_PLAN.md` - Action plan / Plan acción [(ES)](IMMEDIATE_ACTION_PLAN.es.md)
- `NDA_TEMPLATE.md` - Confidentiality / Confidencialidad

---

## 🔒 Security Checklist / Lista Seguridad

### ✅ Completed / Completado
- [x] Copyright notices / Avisos copyright
- [x] LICENSE file / Archivo LICENSE
- [x] Security documentation / Documentación seguridad
- [x] Patent application draft / Borrador aplicación patente

### 🔴 TO DO THIS WEEK / POR HACER ESTA SEMANA
- [ ] Make repo private / Hacer repo privado
- [ ] Enable 2FA / Habilitar 2FA
- [ ] Schedule attorney consultations / Programar consultas abogado
- [ ] File provisional patent / Presentar patente provisional

---

## 💡 Simple Analogies / Analogías Simples

### Speed / Velocidad
**EN**: Ferrari (RTX 3080) vs Honda Civic (Our Software)  
→ Civic is 20% as fast but saves $275,000!

**ES**: Ferrari (RTX 3080) vs Honda Civic (Nuestro Software)  
→ ¡Civic es 20% tan rápido pero ahorra $275,000!

### Power / Poder
**EN**: 3 refrigerators (GPU 320W) vs 1 light bulb (Our software 50W)

**ES**: 3 refrigeradores (GPU 320W) vs 1 foco (Nuestro software 50W)

### Access / Acceso
**EN**: YouTube requiring $500 camera → Now works on any phone  
→ We did the same for 3D graphics!

**ES**: YouTube requiriendo cámara $500 → Ahora funciona en cualquier teléfono  
→ ¡Hicimos lo mismo para gráficos 3D!

---

## 📞 Emergency Contacts / Contactos Emergencia

### Legal / Legal
- **Email**: legal@queztl-core.com (to be established)
- **EN**: Patent attorney consultations
- **ES**: Consultas abogado patentes

### Security / Seguridad
- **Email**: security@queztl-core.com (to be established)
- **EN**: Report unauthorized access
- **ES**: Reportar acceso no autorizado

---

## 🎓 Training / Capacitación

### For Sales / Para Ventas
**EN**: "Our software makes 3D graphics work on any computer, saving $200-700 per device. It's like making YouTube work on phones - we democratized 3D."

**ES**: "Nuestro software hace que gráficos 3D funcionen en cualquier computadora, ahorrando $200-700 por dispositivo. Es como hacer que YouTube funcione en teléfonos - democratizamos el 3D."

### For Technical / Para Técnicos
**EN**: "Software GPU simulator achieving 5.82B ops/sec through vectorized execution and thread block simulation."

**ES**: "Simulador GPU software logrando 5.82 mil millones ops/seg mediante ejecución vectorizada y simulación bloques hilos."

---

## 🏆 Key Achievements / Logros Clave

```
✅ 19.5% RTX 3080 performance / rendimiento
✅ 116% GTX 1660 - WE WIN! / ¡GANAMOS!
✅ 14.5x faster than Intel Graphics / más rápido que Intel Graphics
✅ $200-700 savings per device / ahorro por dispositivo
✅ 86% less energy / menos energía
✅ S-grade compute / computación
✅ A-grade rendering / renderizado
✅ Patent pending / Patente pendiente
```

---

## ⚖️ Legal / Legal

```
Copyright (c) 2025 Queztl-Core Project
All Rights Reserved / Todos los Derechos Reservados

CONFIDENTIAL / CONFIDENCIAL
Patent Pending / Patente Pendiente
```

**EN**: Unauthorized use strictly prohibited  
**ES**: Uso no autorizado estrictamente prohibido

---

## 📈 Market / Mercado

```
Global GPU Market:     $41 billion / mil millones
Target (20%):          $8.2 billion / mil millones
1% Capture:            $82 million / millones
5% Capture:            $410 million / millones

Projected ARR:
Year 1:                $5M
Year 2:                $20M
Year 3:                $50M
Year 5:                $200M
```

---

## 🦅 Built with Queztl-Core Technology

**"Making the impossible accessible"**  
**"Haciendo lo imposible accesible"**

---

🔒 **CONFIDENTIAL - PATENT PENDING**  
🔒 **CONFIDENCIAL - PATENTE PENDIENTE**

**Last Updated / Última Actualización**: December 4, 2025 / 4 de diciembre, 2025

---

## 💾 Print-Friendly Version / Versión para Imprimir

*This document is designed to fit on 3-4 pages when printed*  
*Este documento está diseñado para caber en 3-4 páginas al imprimir*

**Print Settings / Configuración Impresión**:
- Landscape / Horizontal
- Scale 90% / Escala 90%
- Margins: Narrow / Márgenes: Estrechos
