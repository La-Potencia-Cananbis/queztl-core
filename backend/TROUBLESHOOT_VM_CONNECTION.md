# Ubuntu VM Connection Troubleshooting

## ❌ Current Issue
```
ssh: connect to host 192.168.1.100 port 22: Operation timed out
```

This means:
- ❌ Network cannot reach 192.168.1.100
- ❌ Port 22 is not responding
- ❌ VM may be offline, off network, or has wrong IP

---

## 🔍 Step 1: Verify VM is Online

### Option A: Check if VM responds to ping
```bash
ping -c 4 192.168.1.100
```

**Expected output:**
```
64 bytes from 192.168.1.100: icmp_seq=1 ttl=64 time=2.5 ms
```

**If you get "no answer":**
- VM is offline or not on network
- IP address is wrong
- Network is disconnected

---

## 🔧 Step 2: Find the Correct VM IP

If 192.168.1.100 is not responding, you need to find your actual VM IP.

### If you can SSH into VM directly:
```bash
# On your Ubuntu VM terminal (not SSH), run:
hostname -I
```

This shows the VM's actual IP address.

### If you have network access to VM:
```bash
# On your Mac, scan your network (requires arp-scan):
brew install arp-scan
sudo arp-scan -l 192.168.1.0/24
```

This shows all devices on your network.

### If using DHCP (common):
Check your router's DHCP client list:
1. Open your router admin page (usually 192.168.1.1)
2. Look for "Connected Devices" or "DHCP Clients"
3. Find your Ubuntu VM in the list
4. Note its IP address

---

## 🚨 Step 3: Verify VM Network Configuration

If you have terminal access to the VM, check network status:

```bash
# On Ubuntu VM:
ip addr show
# or
ifconfig
```

Look for an IP starting with 192.168.x.x or 10.0.x.x

**If no IP is assigned:**
- Network interface is not connected
- DHCP is not configured
- Network cable/interface is down

---

## 🔐 Step 4: Verify SSH is Running

If VM is online, check if SSH service is running:

```bash
# On Ubuntu VM:
sudo systemctl status ssh
```

**If SSH is not running:**
```bash
sudo systemctl start ssh
sudo systemctl enable ssh
```

---

## 📋 Pre-Deployment Checklist (REVISED)

Before running deployment, verify ALL of these:

✅ **Network Access**
- [ ] VM is powered on
- [ ] VM is connected to network (cable/WiFi)
- [ ] Mac and VM are on same network
- [ ] Can ping VM: `ping <vm-ip>`

✅ **SSH Access**
- [ ] SSH service is running on VM: `sudo systemctl status ssh`
- [ ] Port 22 is open: `sudo ufw allow 22/tcp`
- [ ] Can SSH manually: `ssh ubuntu@<vm-ip>`

✅ **System Resources**
- [ ] At least 5GB disk space: `df -h`
- [ ] At least 2GB RAM available: `free -h`
- [ ] Ports 8000 and 8080 are free: `sudo netstat -tlnp | grep 8000`

✅ **Credentials**
- [ ] You know the Ubuntu username (default: `ubuntu`)
- [ ] You have SSH credentials (password or key)
- [ ] SSH key has correct permissions: `chmod 600 ~/.ssh/your-key.pem`

---

## 🎯 Most Common Issues & Solutions

### Issue 1: "Operation timed out"
**Cause:** Can't reach the VM
**Solution:**
1. Verify IP address with `hostname -I` on VM
2. Ping the correct IP from Mac
3. Check both are on same network
4. Check firewall isn't blocking port 22

### Issue 2: "Connection refused"
**Cause:** VM is reachable but SSH is not listening
**Solution:**
```bash
# On Ubuntu VM:
sudo systemctl restart ssh
sudo systemctl enable ssh
```

### Issue 3: "Permission denied"
**Cause:** Wrong SSH key or credentials
**Solution:**
```bash
# Try with explicit key:
ssh -i ~/.ssh/your-key.pem ubuntu@<vm-ip>

# Or try password auth:
ssh -o PreferredAuthentications=password ubuntu@<vm-ip>
```

### Issue 4: "Could not resolve hostname"
**Cause:** DNS issue or bad hostname
**Solution:** Use IP address instead of hostname

---

## 🚀 Once VM is Accessible

Once you can SSH successfully, run deployment:

```bash
# Test SSH first:
ssh ubuntu@<YOUR-ACTUAL-IP> 'echo OK'

# If that works, run deployment:
./deploy-to-ubuntu-vm.sh <YOUR-ACTUAL-IP>
```

---

## 📞 Quick Diagnostic Command

Run this on your Mac to test everything:

```bash
VM_IP="192.168.1.100"

echo "Testing $VM_IP..."
echo ""

echo "1. Checking network ping..."
ping -c 1 $VM_IP && echo "✅ Ping works" || echo "❌ Ping failed"

echo ""
echo "2. Checking SSH port..."
nc -zv $VM_IP 22 && echo "✅ SSH port open" || echo "❌ SSH port closed"

echo ""
echo "3. Testing SSH connection..."
ssh -o ConnectTimeout=5 ubuntu@$VM_IP 'echo ✅ SSH works' || echo "❌ SSH failed"
```

---

## 🔧 What to do NOW

1. **Verify the IP address:**
   ```bash
   ssh ubuntu@<vm-ip> 'hostname -I'
   ```
   If this works, you have the right IP!

2. **Find correct IP if needed:**
   - Check VM directly: `hostname -I`
   - Check your router's DHCP table
   - Use arp-scan: `sudo arp-scan -l 192.168.1.0/24`

3. **Once you have correct IP:**
   ```bash
   # Test connection:
   ssh ubuntu@<correct-ip> 'echo connected'
   
   # If that works, run deployment:
   ./deploy-to-ubuntu-vm.sh <correct-ip>
   ```

---

## ❓ Still Having Issues?

Try these diagnostics:

```bash
# Test if any IP on 192.168.1.x is Ubuntu:
for i in {1..254}; do
  ping -c 1 192.168.1.$i &
done
wait

# Install network tools if needed:
brew install nmap
nmap -p 22 192.168.1.0/24

# Verbose SSH debug:
ssh -vvv ubuntu@<ip> 2>&1 | tail -20
```

---

## Summary

**Your current status:**
- ❌ Cannot reach 192.168.1.100
- 🔍 Need to find correct VM IP address
- ✅ Once found, deployment will work

**Next step:** Find your actual VM IP and update the deployment command!

