import tkinter as tk
import time
import threading
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode

# --- Configuration ---
DELAY = 0.01  # Time between clicks in seconds
BUTTON = Button.left
START_STOP_KEY = KeyCode(char='s') # Hotkey to toggle the clicker
# ---------------------

class AutoClicker(threading.Thread):
    def __init__(self, delay, button):
        super(AutoClicker, self).__init__()
        self.delay = delay
        self.button = button
        self.running = False
        self.program_running = True
        self.mouse = Controller()

    def start_clicking(self):
        self.running = True

    def stop_clicking(self):
        self.running = False

    def exit(self):
        self.stop_clicking()
        self.program_running = False

    def run(self):
        while self.program_running:
            while self.running:
                self.mouse.click(self.button)
                time.sleep(self.delay)
            time.sleep(0.1)

class AutoclickerGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Autoclicker")
        self.root.geometry("300x250")
        self.root.attributes("-topmost", True) # Keeps the window on top of games/apps

        self.hotkeys_enabled = False

        self.click_thread = AutoClicker(DELAY, BUTTON)
        self.click_thread.start()

        self.setup_ui()

        # Start listener in a non-blocking way
        self.listener = Listener(on_press=self.on_press)
        self.listener.start()

        self.update_status()

    def setup_ui(self):
        self.status_label = tk.Label(self.root, text="Status: PAUSED", fg="red", font=("Helvetica", 14, "bold"))
        self.status_label.pack(pady=15)

        delay_frame = tk.Frame(self.root)
        delay_frame.pack(pady=5)
        tk.Label(delay_frame, text="Delay (sec):").pack(side=tk.LEFT)
        self.delay_entry = tk.Entry(delay_frame, width=8)
        self.delay_entry.insert(0, str(DELAY))
        self.delay_entry.pack(side=tk.LEFT, padx=5)

        tk.Button(self.root, text="Update Delay", command=self.update_delay).pack(pady=5)

        tk.Label(self.root, text=f"Start/Pause Hotkey: '{START_STOP_KEY.char}'").pack()

        self.toggle_hotkeys_button = tk.Button(self.root, text="Enable Hotkeys", command=self.toggle_hotkeys)
        self.toggle_hotkeys_button.pack(pady=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def update_delay(self):
        try:
            self.click_thread.delay = float(self.delay_entry.get())
        except ValueError:
            pass # Ignore invalid characters

    def toggle_hotkeys(self):
        self.hotkeys_enabled = not self.hotkeys_enabled
        if self.hotkeys_enabled:
            self.toggle_hotkeys_button.config(text="Disable Hotkeys")
        else:
            self.click_thread.stop_clicking() # Ensure clicking stops when disabled
            self.toggle_hotkeys_button.config(text="Enable Hotkeys")

    def on_press(self, key):
        if not self.hotkeys_enabled:
            return # Ignore hotkeys if they are disabled
        if key == START_STOP_KEY:
            if self.click_thread.running:
                self.click_thread.stop_clicking()
            else:
                self.click_thread.start_clicking()

    def update_status(self):
        if not self.hotkeys_enabled:
            self.status_label.config(text="Status: DISABLED", fg="grey")
        elif self.click_thread.running:
            self.status_label.config(text="Status: RUNNING", fg="green")
        else:
            self.status_label.config(text="Status: PAUSED", fg="red")
        self.root.after(100, self.update_status) # Loop UI update safely every 100ms

    def on_closing(self):
        self.click_thread.exit()
        self.listener.stop()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AutoclickerGUI(root)
    root.mainloop()