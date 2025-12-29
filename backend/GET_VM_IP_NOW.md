# 🔍 Find Your Ubuntu VM's IP - Right Now!

## Quick Question: Can you access the Ubuntu VM's terminal?

### YES - I can see the VM terminal
Run this command ON the Ubuntu VM:
```bash
hostname -I
```

You'll get output like: `192.168.1.105`

Then come back here and tell me the IP, or run:
```bash
./smart-deploy.sh 192.168.1.105
```

---

### NO - I can't access the VM terminal

Do ONE of these:

**OPTION 1: Check your router (Easiest)**
1. Open browser: http://192.168.1.1
2. Login (check router for password)
3. Look for "Connected Devices" or "DHCP Clients"
4. Find "ubuntu" VM in the list
5. Note the IP address

**OPTION 2: Network scan command**
```bash
# On your Mac, try this (requires nmap):
brew install nmap
nmap -p 22 192.168.0.0/24
nmap -p 22 10.0.0.0/24
```

**OPTION 3: Check your DHCP server**
If running on same Mac:
```bash
# Show DHCP assigned IPs
arp -a | grep -i "ubuntu\|bridge"
```

---

## 💡 Most Common IP Ranges

Try these in order:
- 192.168.1.x (most common)
- 192.168.0.x (also common)
- 10.0.0.x (docker/VM networks)
- 172.16.0.x (sometimes)

---

## Once You Have the IP

Just run:
```bash
./smart-deploy.sh 192.168.1.105    # Replace with your IP
```

Done! ✅

