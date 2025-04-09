# 🔥 Forge Launcher v1.8 – designed by LordKa

![Forge Launcher Screenshot](screenshots\mainscreen.png)  
*Example screenshot – replace with actual Forge Launcher view*

## 📋 Description

The **Forge Launcher** is a GUI-based utility that allows you to easily manage your local FORGE / Stable Diffusion WebUI instance.

It provides a convenient interface to:

- ✅ Start, Stop, and Restart the `webui-user.bat`
- ✅ Automatically monitor Forge-related processes (CMD and Python)
- ✅ Display current **RAM and VRAM usage**
- ✅ Minimize to System Tray and restore
- ✅ Auto-restart Forge if it crashes
- ✅ Remember the last selected `.bat` file location (via `forge_config.json`)
- ✅ Includes an English UI with a modern dark theme

---

## 📦 Installation

```bash
pip install tkinterdnd2 Pillow screeninfo send2trash piexif psutil pystray
```

> 💡 **Note:**  
> All required Python packages are automatically checked and installed at runtime.  
> Manual installation is optional if you prefer setting them up beforehand.

---

## 🚀 Features

| Feature | Description |
|--------|-------------|
| 🔁 Start/Stop/Restart | Controls the `webui-user.bat` directly |
| 🧠 Process Monitoring | Detects and tracks Python/CMD processes |
| 🖥 RAM Usage | Real-time total RAM usage for active Forge processes |
| 🎮 VRAM Usage | Uses `nvidia-smi` to show GPU memory usage |
| 🔄 Auto-Restart | If Forge crashes, it restarts automatically if enabled |
| 🧰 Config Saving | Remembers last used `.bat` location in `forge_config.json` |
| 🧳 Minimize to Tray | Closes window but keeps launcher active in tray |

---

## 🖼 UI Preview

⚠️ *(Insert your actual ForgeLauncher screenshot below this line)*

![ForgeLauncher GUI](screenshots\mainscreen.png)

---

## ⚙ Configuration

The config file is stored as:

```
forge_config.json
```

It holds the path to your Forge installation folder. You can change it via the **"Select Start BAT"** button in the GUI.

---

## 💻 How to Use

1. Launch the script:  
   ```bash
   python ForgeLauncher.py
   ```
2. Click `Start` to launch your Forge instance.
3. Use `Stop` or `Restart` as needed.
4. Check RAM/VRAM usage top right.
5. Use `Minimize to Tray` to hide the window.
6. Enable **Auto-Restart** for automatic recovery.

---

## 🧑‍💻 Author

**LordKa-Berlin**  
[GitHub Profile](https://github.com/LordKa-Berlin)  
Design & Development: GUI automation & SD integration tools

---

## 📜 License
