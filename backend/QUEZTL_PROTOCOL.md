# Queztl Protocol Stack (QPS)
## Next-Gen Communication Layer for AIOSC

## Vision
**Fuck REST. Build something faster.**
- Binary protocol over WebSockets (10x faster)
- Direct browser connection via HTML5
- Open source community protocol
- Backward compatible with REST (for now)

## Protocol Layers

```
┌─────────────────────────────────────────────────────────────┐
│                    APPLICATION LAYER                         │
│              (Your AIOSC capabilities)                       │
└────────────────────┬────────────────────────────────────────┘
                     │
┌────────────────────▼────────────────────────────────────────┐
│                 QUEZTL PROTOCOL (QP/1.0)                     │
│         Binary message format, real-time streaming          │
│  Type: Command (0x01) | Data (0x02) | Stream (0x03)        │
└──────┬──────────────┬──────────────┬───────────────────────┘
       │              │              │
┌──────▼──────┐  ┌───▼──────┐  ┌───▼──────┐
│ WebSocket   │  │ WebRTC   │  │WebTransp │
│ (Default)   │  │ (P2P)    │  │ (HTTP/3) │
└─────────────┘  └──────────┘  └──────────┘
       │              │              │
┌──────▼──────────────▼──────────────▼───────────────────────┐
│                      HTML5 Browser                           │
│           No plugins, pure JavaScript client                 │
└─────────────────────────────────────────────────────────────┘
```

## Why This Rocks

### vs REST
```
REST Request:
1. Open TCP connection
2. Send HTTP headers (200-500 bytes overhead)
3. Wait for response
4. Parse JSON
5. Close connection
= ~100-200ms latency

Queztl Protocol:
1. Persistent WebSocket (already open)
2. Send binary message (4 bytes header + data)
3. Streaming response (real-time chunks)
4. Binary decode (50x faster than JSON)
= ~5-10ms latency

SPEEDUP: 10-20x faster
```

### HTML5 Native
```javascript
// Pure JavaScript - no backend needed
const qp = new QueztlProtocol('wss://api.queztl.com');

// Send command
await qp.execute('text-to-3d', {
  prompt: 'dragon',
  quality: 'high'
});

// Stream results in real-time
qp.onProgress((percent, preview) => {
  updateUI(percent);
  render3DPreview(preview);
});

// Get final result
qp.onComplete((model) => {
  download(model, 'dragon.gltf');
});
```

## Protocol Specification

### Message Format (Binary)
```
┌──────────┬──────────┬──────────┬──────────────┐
│  Magic   │  Type    │  Length  │   Payload    │
│ (2 bytes)│ (1 byte) │ (4 bytes)│  (N bytes)   │
└──────────┴──────────┴──────────┴──────────────┘
  0x5150    0x01-0xFF   uint32     data

Magic: "QP" (0x5150) - Identifies Queztl Protocol
Type:
  0x01 = COMMAND (execute capability)
  0x02 = DATA (send data chunk)
  0x03 = STREAM (streaming response)
  0x04 = ACK (acknowledgment)
  0x05 = ERROR (error response)
  0x10 = AUTH (authentication)
  0x11 = HEARTBEAT (keepalive)
Length: Size of payload in bytes
Payload: Binary data (capability-specific)
```

### Example Messages

#### 1. Authentication
```
Client -> Server:
┌──────┬────┬────────┬─────────────────────────────┐
│ 5150 │ 10 │ 000020 │ {"token": "eyJhbGc..."} │
└──────┴────┴────────┴─────────────────────────────┘

Server -> Client:
┌──────┬────┬────────┬──────────────────────────┐
│ 5150 │ 04 │ 000010 │ {"auth": "success"}      │
└──────┴────┴────────┴──────────────────────────┘
```

#### 2. Execute Capability
```
Client -> Server:
┌──────┬────┬────────┬──────────────────────────────────┐
│ 5150 │ 01 │ 000050 │ {                                │
│      │    │        │   "cap": "text-to-3d",          │
│      │    │        │   "params": {"prompt": "car"}   │
│      │    │        │ }                                │
└──────┴────┴────────┴──────────────────────────────────┘

Server -> Client (Progress Stream):
┌──────┬────┬────────┬──────────────────────────┐
│ 5150 │ 03 │ 000015 │ {"progress": 25}         │
└──────┴────┴────────┴──────────────────────────┘
┌──────┬────┬────────┬──────────────────────────┐
│ 5150 │ 03 │ 000015 │ {"progress": 50}         │
└──────┴────┴────────┴──────────────────────────┘
┌──────┬────┬────────┬──────────────────────────┐
│ 5150 │ 03 │ 000015 │ {"progress": 100}        │
└──────┴────┴────────┴──────────────────────────┘

Server -> Client (Result):
┌──────┬────┬────────┬──────────────────────────┐
│ 5150 │ 02 │ 005000 │ <binary 3D model data>   │
└──────┴────┴────────┴──────────────────────────┘
```

## Implementation Stack

### Server Side (Python)
```python
import struct
import asyncio
import websockets

class QueztlProtocol:
    MAGIC = b'QP'
    
    # Message types
    COMMAND = 0x01
    DATA = 0x02
    STREAM = 0x03
    ACK = 0x04
    ERROR = 0x05
    AUTH = 0x10
    HEARTBEAT = 0x11
    
    @staticmethod
    def pack(msg_type: int, payload: bytes) -> bytes:
        """Pack message into binary format"""
        header = struct.pack('!2sBL', 
            QueztlProtocol.MAGIC,    # Magic bytes
            msg_type,                # Message type
            len(payload)             # Payload length
        )
        return header + payload
    
    @staticmethod
    def unpack(data: bytes) -> tuple:
        """Unpack binary message"""
        magic, msg_type, length = struct.unpack('!2sBL', data[:7])
        if magic != QueztlProtocol.MAGIC:
            raise ValueError("Invalid magic bytes")
        payload = data[7:7+length]
        return msg_type, payload
    
    @staticmethod
    async def handle_client(websocket, path):
        """Handle client connection"""
        async for message in websocket:
            msg_type, payload = QueztlProtocol.unpack(message)
            
            if msg_type == QueztlProtocol.COMMAND:
                # Execute capability
                result = await execute_capability(payload)
                
                # Stream progress
                async for progress in result:
                    response = QueztlProtocol.pack(
                        QueztlProtocol.STREAM,
                        json.dumps({"progress": progress}).encode()
                    )
                    await websocket.send(response)
                
                # Send final result
                response = QueztlProtocol.pack(
                    QueztlProtocol.DATA,
                    result.data
                )
                await websocket.send(response)
```

### Client Side (JavaScript)
```javascript
class QueztlProtocol {
  constructor(url) {
    this.ws = new WebSocket(url);
    this.ws.binaryType = 'arraybuffer';
    this.handlers = {};
    
    this.ws.onmessage = (event) => {
      const msg = this.unpack(event.data);
      this.handleMessage(msg);
    };
  }
  
  pack(type, payload) {
    // Magic: "QP" (0x5150)
    // Type: 1 byte
    // Length: 4 bytes
    // Payload: N bytes
    
    const magic = new Uint8Array([0x51, 0x50]);
    const typeByte = new Uint8Array([type]);
    const length = new Uint32Array([payload.byteLength]);
    
    const buffer = new ArrayBuffer(7 + payload.byteLength);
    const view = new Uint8Array(buffer);
    
    view.set(magic, 0);
    view.set(typeByte, 2);
    view.set(new Uint8Array(length.buffer), 3);
    view.set(new Uint8Array(payload), 7);
    
    return buffer;
  }
  
  unpack(data) {
    const view = new DataView(data);
    const magic = view.getUint16(0);
    const type = view.getUint8(2);
    const length = view.getUint32(3);
    const payload = data.slice(7, 7 + length);
    
    if (magic !== 0x5150) {
      throw new Error('Invalid magic bytes');
    }
    
    return { type, payload };
  }
  
  async execute(capability, params) {
    const payload = new TextEncoder().encode(
      JSON.stringify({ cap: capability, params })
    );
    
    const message = this.pack(0x01, payload); // COMMAND
    this.ws.send(message);
  }
  
  onProgress(callback) {
    this.handlers.progress = callback;
  }
  
  onComplete(callback) {
    this.handlers.complete = callback;
  }
  
  handleMessage(msg) {
    switch(msg.type) {
      case 0x03: // STREAM
        const progress = JSON.parse(
          new TextDecoder().decode(msg.payload)
        );
        this.handlers.progress?.(progress);
        break;
      
      case 0x02: // DATA
        this.handlers.complete?.(msg.payload);
        break;
    }
  }
}

// Usage
const qp = new QueztlProtocol('wss://api.queztl.com');

qp.onProgress((data) => {
  console.log(`Progress: ${data.progress}%`);
});

qp.onComplete((model) => {
  console.log('Model received:', model);
});

await qp.execute('text-to-3d', {
  prompt: 'spaceship',
  quality: 'high'
});
```

## Advanced Features

### 1. Binary Compression
```python
import zlib

# Compress large payloads
compressed = zlib.compress(payload)
# Add compression flag to header
```

### 2. Multiplexing (Multiple Streams)
```
Add stream ID to header:
┌──────┬────┬────────┬──────────┬──────────┐
│Magic │Type│StreamID│  Length  │ Payload  │
└──────┴────┴────────┴──────────┴──────────┘
```

### 3. Direct P2P via WebRTC
```javascript
// For local processing (no server)
const peer = new RTCPeerConnection();
const channel = peer.createDataChannel('queztl');

// Use Queztl Protocol over data channel
channel.send(qp.pack(0x01, payload));
```

## REST Compatibility Layer

Keep REST for now, but route through QP internally:

```python
@app.post("/execute/{capability}")
async def rest_execute(capability: str, request: Request):
    """REST endpoint that uses QP internally"""
    
    # Convert REST to QP
    payload = await request.json()
    qp_message = QueztlProtocol.pack(
        QueztlProtocol.COMMAND,
        json.dumps(payload).encode()
    )
    
    # Execute via QP
    result = await qp_handler.execute(qp_message)
    
    # Convert back to REST response
    return JSONResponse(result)
```

## Performance Benchmarks

### Target Metrics
```
REST API:
- Latency: 100-200ms
- Throughput: 100 req/s
- Overhead: 500 bytes/req

Queztl Protocol:
- Latency: 5-10ms (20x faster)
- Throughput: 10,000 msg/s (100x faster)
- Overhead: 7 bytes/msg (70x smaller)
```

## Open Source Community

### 1. Specification (queztl-protocol.org)
- Complete protocol spec
- Binary format docs
- Reference implementations

### 2. Libraries
```
queztl-py     - Python server
queztl-js     - JavaScript client
queztl-rs     - Rust (high performance)
queztl-go     - Go (cloud native)
```

### 3. Tools
```
qp-cli        - Command line client
qp-debug      - Protocol debugger
qp-bench      - Performance benchmarking
```

## Roadmap

### Phase 1: MVP (This Week)
- [ ] Binary protocol spec v1.0
- [ ] Python WebSocket server
- [ ] JavaScript client library
- [ ] Basic commands (auth, execute, stream)

### Phase 2: Performance (Next Week)
- [ ] Binary compression
- [ ] Multiplexing support
- [ ] Connection pooling
- [ ] Benchmark vs REST

### Phase 3: Advanced (Month 1)
- [ ] WebRTC P2P mode
- [ ] HTTP/3 WebTransport
- [ ] Multi-language clients
- [ ] Protocol debugger tool

### Phase 4: Community (Month 2+)
- [ ] Open source release
- [ ] Documentation site
- [ ] Community SDKs
- [ ] Adoption by other projects

## Why This Will Win

1. **10-20x Faster** than REST
   - Binary vs text encoding
   - Persistent connections
   - No HTTP overhead

2. **HTML5 Native**
   - Works in any browser
   - No plugins or installs
   - Progressive Web App ready

3. **Open Source**
   - Community driven
   - Multi-language support
   - Becomes industry standard

4. **Backward Compatible**
   - Keep REST for old clients
   - Gradual migration
   - Best of both worlds

## Next Steps

1. **Build QP Server** (Python WebSocket + binary protocol)
2. **Build QP Client** (JavaScript library for browsers)
3. **Wire to AIOSC** (Execute capabilities via QP)
4. **Benchmark** (Prove 10x faster than REST)
5. **Open Source** (Release to community)

**Let's build the future of web protocols.** 🚀
