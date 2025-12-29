# 🔐 XAVASENA PRIVATE ACCESS
# Solo para ti carnal - nadie más entra

## 🔑 Tu Master Key

```bash
XAVASENA_MASTER_KEY="b8f3d9e7a6c5f1d2e4a9b7c6d8f3e1a2b4c7d9e6f8a1c3d5e7f9a2b4c6d8e1f3"
```

## 📡 Llamar tu STANDALONE CORE (Solo tú)

### Desde cualquier lugar:

```bash
# Tu master key
export OWNER_KEY="b8f3d9e7a6c5f1d2e4a9b7c6d8f3e1a2b4c7d9e6f8a1c3d5e7f9a2b4c6d8e1f3"

# Llamar tu core
curl -X POST https://queztl-core-backend.onrender.com/api/standalone/process \
  -H "Content-Type: application/json" \
  -H "X-Owner-Key: $OWNER_KEY" \
  -d '{
    "task_type": "video_enhancement",
    "input_data": {
      "video": "test.mp4"
    },
    "autonomous": true
  }'
```

## 🎯 Endpoints (Todos protegidos - Solo tú)

```bash
# Status de tu core
curl https://queztl-core-backend.onrender.com/api/standalone/status \
  -H "X-Owner-Key: $OWNER_KEY"

# Procesar task
curl -X POST https://queztl-core-backend.onrender.com/api/standalone/process \
  -H "X-Owner-Key: $OWNER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"task_type": "...", "input_data": {...}}'

# Entrenar modelo
curl -X POST https://queztl-core-backend.onrender.com/api/standalone/train \
  -H "X-Owner-Key: $OWNER_KEY" \
  -H "Content-Type: application/json" \
  -d '{"model_name": "...", "training_data": [...]}'

# Ver tus modelos
curl https://queztl-core-backend.onrender.com/api/standalone/models \
  -H "X-Owner-Key: $OWNER_KEY"
```

## 🌍 Desde tu nuevo spot

1. **Guarda tu master key:**
   ```bash
   echo 'export XAVASENA_KEY="b8f3d9e7a6c5f1d2e4a9b7c6d8f3e1a2b4c7d9e6f8a1c3d5e7f9a2b4c6d8e1f3"' >> ~/.bashrc
   source ~/.bashrc
   ```

2. **Test rápido:**
   ```bash
   curl https://queztl-core-backend.onrender.com/api/standalone/status \
     -H "X-Owner-Key: $XAVASENA_KEY"
   ```

3. **Si cambia tu IP, actualiza en Render:**
   - Ve a Render.com dashboard
   - Abre queztl-core-backend
   - Environment variables
   - Agrega: `AUTHORIZED_IP_1=tu.nueva.ip`

## 🔒 Seguridad

- ✅ Solo TU master key funciona
- ✅ Sin créditos de APIs externas
- ✅ Todo corre en TU backend
- ✅ Data nunca sale de tu control
- ✅ Nadie más puede acceder

## 💾 Guardar esto seguro

```bash
# En tu nueva máquina
mkdir -p ~/.quetzalcore
echo "b8f3d9e7a6c5f1d2e4a9b7c6d8f3e1a2b4c7d9e6f8a1c3d5e7f9a2b4c6d8e1f3" > ~/.quetzalcore/key
chmod 600 ~/.quetzalcore/key

# Usar
export OWNER_KEY=$(cat ~/.quetzalcore/key)
```

## 🦅 Tu Core, Tu Control

- 💰 $0 en créditos
- 🌐 0 external API calls
- 🔒 100% privado
- 🎯 100% autónomo
- 👑 100% tuyo

¡Dale ese!
