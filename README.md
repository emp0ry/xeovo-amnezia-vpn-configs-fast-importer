<p align="center">
  <img src="https://xeovo.com/static/images/logo.svg" width="510" alt="Xeovo Logo">
</p>

<h1 align="center">AmneziaVPN Converter</h1>
<p align="center">
  <strong><code>AmneziaVPN.backup</code></strong> file containing
  <strong>all Xeovo locations</strong>, ready for instant import into AmneziaVPN.
  <br>
  No more importing configs one by one - everything is generated automatically.
</p>

## 🚀 What This Does

This script:

- Reads a Xeovo `.conf` file
- Extracts all required keys and parameters
- Generates a full **AmneziaVPN backup**
- Creates multiple servers by replacing the endpoint with:
```
<location_code>.gw.xeovo.com:<original_port>
```
- Keeps:
- same keys
- same routing
- same port
- only hostname changes per location

Output file:
```
AmneziaVPN.backup
````

Ready to import into:
- Windows AmneziaVPN
- macOS AmneziaVPN
- Linux AmneziaVPN
- Android / iOS (via backup restore)

---

## 🌍 Included Locations

The generated backup contains:

| Code | Location |
|------|----------|
| al | Albania (Tirana) |
| au | Australia (Sydney) |
| br | Brazil (São Paulo) |
| ca | Canada (Montreal) |
| ch | Switzerland (Zurich) |
| de | Germany (Falkenstein) |
| fi | Finland (Helsinki) |
| fr | France (Paris) |
| jp | Japan (Tokyo) |
| lu | Luxembourg (Roost) |
| lv | Latvia (Riga) |
| nl | Netherlands (Amsterdam) |
| no | Norway (Sandefjord) |
| pl | Poland (Warsaw) |
| ro | Romania (Iasi) |
| se | Sweden (Stockholm) |
| sg | Singapore |
| ua | Ukraine (Kyiv) |
| uk | United Kingdom (London) |
| us-lv | USA (Las Vegas) |
| us-mia | USA (Miami) |
| us-nyc | USA (New York) |
| random | Random |

---

## 🛠️ Installation

### 1. Clone the Repository
```bash
git clone https://github.com/emp0ry/xeovo-amnezia-vpn-conf-fast-importer.git
cd xeovo-amnezia-vpn-conf-fast-importer
````

### 2. Install Python (if not already installed)

#### Windows

Download from: [https://www.python.org](https://www.python.org)
(make sure to check **"Add Python to PATH"**)

#### Linux

Ubuntu / Debian:

```bash
sudo apt-get update
sudo apt-get install -y python3
```

CentOS / RHEL:

```bash
sudo yum install -y python3
```

#### macOS

```bash
brew install python3
```

Verify:

```bash
python --version
# or
python3 --version
```

---

### 3. Install Tkinter (Linux only, if missing)

On some Linux systems Tkinter is not installed by default.

Ubuntu / Debian:

```bash
sudo apt-get install -y python3-tk
```

CentOS / RHEL:

```bash
sudo yum install -y python3-tkinter
```

Windows and macOS usually include Tkinter by default.

---

### 4. Dependencies

This project uses **only standard Python libraries**:

* `configparser`
* `json`
* `os`
* `tkinter`

No external dependencies.
No `pip install` required.

---

### 5. Prepare Xeovo `.conf` File

Your Xeovo config must look like this:

```ini
[Interface]
Address = 10.0.0.2/32
PrivateKey = ...
DNS = 1.1.1.1
Jc = 10
Jmin = 100
Jmax = 1000
S1 = 10
S2 = 20
H1 = ...
H2 = ...
H3 = ...
H4 = ...

[Peer]
PublicKey = ...
AllowedIPs = 0.0.0.0/0, ::/0
Endpoint = au.gw.xeovo.com:51820
```

---

## ▶️ Usage

Run the script:

```bash
python main.py
# or
python3 main.py
```

What happens:

1. File picker opens
2. Select your `.conf`
3. Script parses config
4. Generates:

   ```
   AmneziaVPN.backup
   ```
5. File saved in script directory

---

## 📋 Example Output

```
Parsed Configuration Data:
--------------------------------------------------
Address: 10.0.0.2/32
PrivateKey: <private_key>
DNS: 1.1.1.1
Jc: 10
Jmin: 100
Jmax: 1000
S1: 10
S2: 20
H1: <hash1>
H2: <hash2>
H3: <hash3>
H4: <hash4>
PublicKey: <public_key>
AllowedIPs: 0.0.0.0/0, ::/0
Endpoint: au.gw.xeovo.com:51820

AmneziaVPN.backup file created at: AmneziaVPN.backup
```

---

## 📥 Import into AmneziaVPN

1. Open **AmneziaVPN**
2. Go to **Settings → Backup / Restore**
3. Click **Import**
4. Select:

   ```
   AmneziaVPN.backup
   ```
5. All Xeovo servers appear instantly

---

## ⚙️ How It Works (Internally)

For each location:

* Replaces:

  ```
  Endpoint = original_host:port
  ```

  with:

  ```
  <code>.gw.xeovo.com:port
  ```

Everything else stays unchanged:

* keys
* MTU
* routing
* allowed IPs
* jitter / hashes

---

## 🔐 Security Warning

The backup file contains:

* your **PrivateKey**
* full VPN configuration

Treat it like a password:

* ❌ do not upload publicly
* ❌ do not commit to git
* ❌ do not share with strangers

Delete after import if not needed.

---

## 🧠 Notes

* Default port fallback: **51820**
* Output always saved next to script
* Works with both **AmneziaWG** and **AWG**
* No network calls, fully offline

---

## 💖 Support the Project  

[![Buy Me a Coffee](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://www.buymeacoffee.com/emp0ry)  

---

## 📜 License

Released under the [MIT License](LICENSE).
