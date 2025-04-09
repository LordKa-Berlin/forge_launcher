# Forge Launcher v1.8
# Datum: 2025-04-09
# Version: 18 – designed by LordKa
# Beschreibung:
# Dieses GUI-Tool dient zur einfachen Steuerung von FORGE (z. B. SD-WebUI)
# Funktionen:
# - Starten, Stoppen und Neustarten der webui-user.bat
# - Automatische Überwachung der Prozesse (cmd und python)
# - RAM- und VRAM-Auslastung anzeigen
# - Minimize to Tray mit Wiederherstellung
# - Automatischer Neustart bei Absturz
# - Auswahl und Speicherung des BAT-Pfads über JSON-Konfiguration
# - Englische GUI-Beschriftungen

import subprocess
import os
import sys

# === Automatische Modulinstallation ===
def ensure_package(package):
    try:
        __import__(package)
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package])

for pkg in ["tkinter", "psutil", "pystray", "Pillow"]:
    ensure_package(pkg)

import tkinter as tk
from tkinter import ttk
import psutil
import threading
import time
import pystray
from PIL import Image as PILImage, ImageDraw

# === Konfiguration ===
# === Konfigurationspfad laden ===
CONFIG_FILE = "forge_config.json"
FORGE_PATH = "D:\FORGE\webui"  # Defaultwert, wird überschrieben wenn Datei existiert

if os.path.exists(CONFIG_FILE):
    try:
        import json
        with open(CONFIG_FILE, "r", encoding="utf-8") as f:
            config = json.load(f)
            FORGE_PATH = config.get("FORGE_PATH", FORGE_PATH)
    except Exception as e:
        print(f"[WARNUNG] Konfig konnte nicht geladen werden: {e}")
VERSION = "1.8"

class ForgeLauncher:
    def __init__(self, root):
        self.root = root
        self.root.title("Forge Launcher")
        self.root.configure(bg="#1F1F1F")
        self.root.geometry("430x440")
        self.root.resizable(True, True)

        self.forge_pids = set()
        self.restart_on_crash = tk.BooleanVar(value=False)
        self.running = True

        self.build_gui()
        self.monitor_thread = threading.Thread(target=self.monitor_forge, daemon=True)
        self.monitor_thread.start()

    def get_monitored_pids(self):
        return set(proc.pid for proc in psutil.process_iter(['name']) if proc.info['name'] and ('python' in proc.info['name'].lower() or 'cmd' in proc.info['name'].lower()))
        return set(proc.pid for proc in psutil.process_iter(['name']) if proc.info['name'] and 'python' in proc.info['name'].lower())

    def update_status(self, message):
        self.status_var.set(message)
        self.status_box.configure(state="normal")
        self.status_box.delete("1.0", tk.END)
        self.status_box.insert("1.0", message)
        self.status_box.configure(state="disabled")

    def build_gui(self):
        top_frame = tk.Frame(self.root, bg="#1F1F1F")
        top_frame.pack(fill=tk.X, pady=5, padx=5)

        self.always_on_top_var = tk.BooleanVar(value=True)
        tk.Checkbutton(
            top_frame, text="Always on Top", variable=self.always_on_top_var,
            command=self.toggle_always_on_top, bg="#000000", fg="#FFA500",
            selectcolor="#000000", activebackground="#1F1F1F", activeforeground="#FFA500"
        ).pack(side=tk.LEFT)

        self.status_var = tk.StringVar(value="Ready")
        self.status_box = tk.Text(self.root, height=2, width=65, bg="#000000", fg="#FFA500", bd=0, wrap="word")
        self.status_box.insert("1.0", self.status_var.get())
        self.status_box.configure(state="disabled")
        self.status_box.pack(pady=(5, 10))
        

        btn_frame = tk.Frame(self.root, bg="#1F1F1F")
        btn_frame.pack(pady=5)

        tk.Button(btn_frame, text="Start", command=self.start_forge,
                  bg="#FFA500", fg="#000000", width=20).pack(pady=2)

        tk.Button(btn_frame, text="Stop", command=self.stop_forge,
                  bg="#FFA500", fg="#000000", width=20).pack(pady=2)

        tk.Button(btn_frame, text="Restart", command=self.restart_forge,
                  bg="#FFA500", fg="#000000", width=20).pack(pady=2)

        tk.Checkbutton(btn_frame, text="Auto-Restart on crash",
                       variable=self.restart_on_crash, bg="#000000",
                       fg="#FFA500", selectcolor="#000000",
                       activebackground="#1F1F1F", activeforeground="#FFA500").pack(pady=2)

        tk.Button(btn_frame, text="Minimize to Tray", command=self.minimize_to_tray,
                  bg="#FFA500", fg="#000000").pack(pady=2)

        tk.Button(btn_frame, text="Select Start BAT", command=self.select_bat_path,
                  bg="#FFA500", fg="#000000").pack(pady=2)

        usage_frame = tk.Frame(top_frame, bg="#1F1F1F")
        usage_frame.pack(side=tk.RIGHT)

        self.ram_label = tk.Label(usage_frame, text="RAM: -", bg="#1F1F1F", fg="#FFA500")
        self.ram_label.pack(side=tk.LEFT, padx=5)

        self.vram_label = tk.Label(usage_frame, text="VRAM: -", bg="#1F1F1F", fg="#FFA500")
        self.vram_label.pack(side=tk.LEFT, padx=5)

        bottom_frame = tk.Frame(self.root, bg="#1F1F1F")
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X, pady=5)

        tk.Label(bottom_frame, text=f"v{VERSION} – designed by LordKa", fg="#FFA500", bg="#1F1F1F").pack()

        self.toggle_always_on_top()

    def toggle_always_on_top(self):
        self.root.wm_attributes("-topmost", self.always_on_top_var.get())

    def start_forge(self):
        try:
            before_pids = self.get_monitored_pids()
            subprocess.Popen(["cmd", "/c", "start", "webui-user.bat"], cwd=FORGE_PATH)
            time.sleep(4)
            after_pids = self.get_monitored_pids()
            self.forge_pids = after_pids - before_pids
            if self.forge_pids:
                self.update_status(f"Forge gestartet (Python-PIDs: {', '.join(map(str, self.forge_pids))})")
                print("[DEBUG] Neue Python-Prozesse:", self.forge_pids)
            else:
                self.status_var.set("Fehler: Keine neuen Python-Prozesse gefunden")
        except Exception as e:
            self.status_var.set(f"Fehler: {e}")
            print("[EXCEPTION]", e)

    def stop_forge(self):
        try:
            if self.forge_pids:
                for pid in list(self.forge_pids):
                    if psutil.pid_exists(pid):
                        proc = psutil.Process(pid)
                        info = f"Beende PID {pid}: {proc.name()} {proc.cmdline()}"
                        print(info)
                        proc.terminate()
                self.status_var.set("Forge-Prozesse beendet")
                self.forge_pids.clear()
            else:
                self.status_var.set("Keine Forge-Prozesse bekannt")
                print("[DEBUG] Keine bekannten PIDs zum Beenden")
        except Exception as e:
            self.status_var.set(f"Fehler: {e}")
            print("[EXCEPTION]", e)

    def restart_forge(self):
        self.stop_forge()
        time.sleep(2)
        self.start_forge()

    def monitor_forge(self):
        while self.running:
            time.sleep(5)
            still_running = [pid for pid in self.forge_pids if psutil.pid_exists(pid)]
            if not still_running and self.forge_pids:
                self.status_var.set("Forge abgestürzt")
                self.forge_pids.clear()
                if self.restart_on_crash.get():
                    self.status_var.set("Forge wird neu gestartet...")
                    self.start_forge()
            self.update_ram_usage(still_running)
            self.update_vram_usage()

    def update_ram_usage(self, active_pids):
        total = 0
        for pid in active_pids:
            try:
                proc = psutil.Process(pid)
                total += proc.memory_info().rss // (1024 * 1024)
            except:
                pass
        self.ram_label.config(text=f"RAM: {total} MB")

    def update_vram_usage(self):
        try:
            result = subprocess.run(["nvidia-smi", "--query-gpu=memory.used", "--format=csv,noheader,nounits"], capture_output=True, text=True)
            if result.returncode == 0:
                vram = result.stdout.strip().split("\n")[0]
                self.vram_label.config(text=f"VRAM: {vram} MB")
            else:
                self.vram_label.config(text="VRAM: nicht verfügbar")
        except Exception:
            self.vram_label.config(text="VRAM: nvidia-smi fehlt")

    def minimize_to_tray(self):
        self.root.withdraw()

        def show_window(icon, item):
            self.root.after(0, self.root.deiconify)
            icon.stop()

        image = PILImage.new('RGB', (64, 64), color='black')
        draw = ImageDraw.Draw(image)
        draw.rectangle((0, 0, 64, 64), fill="#FFA500")

        menu = pystray.Menu(
            pystray.MenuItem('Open', show_window),
            pystray.MenuItem('Exit', lambda icon, item: self.on_close())
        )
        icon = pystray.Icon("ForgeLauncher", image, "Forge Launcher", menu)
        threading.Thread(target=icon.run, daemon=True).start()

    def select_bat_path(self):
        import json
        from tkinter import filedialog
        file_path = filedialog.askopenfilename(filetypes=[("Batch-Dateien", "*.bat")])
        if file_path:
            global FORGE_PATH
            FORGE_PATH = os.path.dirname(file_path)
            try:
                with open(CONFIG_FILE, "w", encoding="utf-8") as f:
                    json.dump({"FORGE_PATH": FORGE_PATH}, f, indent=4)
            except Exception as e:
                print(f"[Fehler beim Speichern der Konfiguration] {e}")
            self.update_status(f"Neuer Pfad gesetzt: {FORGE_PATH}")

    def on_close(self):
        self.running = False
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = ForgeLauncher(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
