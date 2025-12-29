# 🚀 Quick VM Setup & Deployment

## Problem: Can't Find Your Ubuntu VM

The IP `192.168.1.100` isn't responding. Let's find your actual VM IP.

---

## ✅ Step 1: Find Your VM's IP Address

### Option A: Direct Access to VM (Best)
If you have terminal access to the Ubuntu VM:

```bash
# Run this ON the Ubuntu VM:
hostname -I
```

**Example output:** `192.168.1.105`

This is your actual VM IP! Use this for deployment.

---

### Option B: Check Your Router's DHCP List
Most reliable if you can't access VM terminal:

1. Open your browser
2. Go to: `http://192.168.1.1` (or `http://192.168.0.1`)
3. Login with router credentials (check bottom/back of router)
4. Find "Connected Devices" or "DHCP Client List"
5. Look for "ubuntu" in the list
6. Note its IP address

---

### Option C: Use Network Scan from Mac
If you have `arp-scan` installed:

```bash
brew install arp-scan
sudo arp-scan -l 192.168.1.0/24 | grep -i ubuntu
```

Or use my simple network finder:

```bash
./FIND_VM_IP.sh
```

This will scan your network and show any machines with SSH open on port 22.

---

### Option D: Check Common Network Ranges
Try these IPs in order:

1. **192.168.1.x** (most common)
   ```bash
   for i in {1..20}; do ping -c 1 -W 0.5 192.168.1.$i &>/dev/null && echo "Found: 192.168.1.$i"; done
   ```

2. **192.168.0.x** (also common)
   ```bash
   for i in {1..20}; do ping -c 1 -W 0.5 192.168.0.$i &>/dev/null && echo "Found: 192.168.0.$i"; done
   ```

3. **10.0.0.x** (docker/VM networks)
   ```bash
   for i in {1..20}; do ping -c 1 -W 0.5 10.0.0.$i &>/dev/null && echo "Found: 10.0.0.$i"; done
   ```

---

## ✅ Step 2: Verify SSH Access

Once you have the IP, test SSH:

```bash
# Replace with your actual IP:
ssh ubuntu@192.168.1.105 'echo connected'
```

**Expected output:** `connected`

**If you see password prompt:**
- Enter the Ubuntu VM password
- Check "remember password" if your Mac asks

**If you see "Are you sure you want to continue?"**
- Type: `yes`
- This adds the VM to known hosts

---

## ✅ Step 3: Deploy GIS Studio

Once SSH works, run deployment:

```bash
./deploy-to-ubuntu-vm.sh 192.168.1.105
```

Replace `192.168.1.105` with your actual IP.

**Deployment will:**
- ✅ Transfer all GIS Studio files
- ✅ Install all dependencies (Python, FastAPI, GIS libraries)
- ✅ Create systemd services for auto-start
- ✅ Start both frontend (port 8080) and backend (port 8000)
- ✅ Show you the access URLs

**Time needed:** ~7-10 minutes

---

## 📊 Success Indicators

Deployment is complete when you can:

1. **See both services running:**
   ```bash
   ssh ubuntu@192.168.1.105 'sudo systemctl status gis-studio'
   ```

2. **Access the dashboards in your browser:**
   - API Tester: `http://192.168.1.105:8080/gis-studio-dashboard.html`
   - Info Page: `http://192.168.1.105:8080/gis-studio.html`
   - API Docs: `http://192.168.1.105:8000/docs`

3. **API responds:**
   ```bash
   curl http://192.168.1.105:8000/api/gis/studio/status
   ```

---

## 🔧 Troubleshooting

### "SSH: connect timed out"
- VM is not on network or powered off
- Wrong IP address
- Try different network ranges (see Step 1)

### "SSH: connection refused"
- SSH service not running on VM
- On Ubuntu VM, run: `sudo systemctl start ssh`

### "Permission denied"
- Wrong password
- Check you're using username: `ubuntu`
- Or specify SSH key: `ssh -i ~/.ssh/your-key.pem ubuntu@<ip>`

### "Could not resolve hostname"
- Make sure you're using an IP address, not a hostname
- Use `192.168.1.x` not `ubuntu.local`

---

## 🎯 What to Do Now

### Immediately:
1. Find your VM's actual IP (see Step 1)
2. Test SSH: `ssh ubuntu@<your-ip> 'echo OK'`
3. Run deployment: `./deploy-to-ubuntu-vm.sh <your-ip>`

### Expected Timeline:
- Finding IP: 1-2 minutes
- Testing SSH: 30 seconds
- Deployment: 7-10 minutes
- **Total: ~10-12 minutes from now**

---

## 🔍 More Tools Available

If you're still stuck:

```bash
# Read full troubleshooting guide:
cat TROUBLESHOOT_VM_CONNECTION.md

# See VM connection action plan:
cat VM_CONNECTION_ACTION_PLAN.txt

# Check Ubuntu installation guide:
cat UBUNTU_INSTALLATION_GUIDE.md

# View deployment guide:
cat UBUNTU_DEPLOYMENT_SUMMARY.txt
```

---

## 💡 Pro Tips

1. **Save your VM IP somewhere**
   - Once you find it, write it down
   - Most VMs keep same IP if on same network

2. **SSH key authentication is faster**
   - If you have SSH key setup, use it:
   - `ssh -i ~/.ssh/your-key.pem ubuntu@<ip>`

3. **Set static IP on VM** (optional, for permanence)
   - Edit `/etc/netplan/01-netcfg.yaml` on Ubuntu
   - Set a static IP so it never changes
   - Then you can always use same deployment command

---

**🚀 Once you have the IP, deployment is just one command!**
