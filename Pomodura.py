import tkinter as tk
from tkinter import messagebox
import ctypes
import os
import threading
import pystray
from PIL import Image, ImageDraw

class PomodoroTimer:
    def __init__(self, root):
        self.root = root
        self.root.title("Pomodoro Timer")
        self.root.geometry("350x180")
        self.root.configure(bg="#f0f0f0")
        self.create_tray_icon()

        # Timer durations in seconds
        self.work_duration = 25 * 60
        self.short_break_duration = 5 * 60
        self.long_break_duration = 15 * 60
        
        self.mode = "Work"  # "Work" or "Break"
        self.remaining_time = self.work_duration
        self.cycle_count = 0  # Count of completed work sessions
        
        self.running = False
        self.paused = False
        
        # Options
        self.lock_on_break = False
        self.minimize_to_tray = True
        
        # Main timer display
        self.time_var = tk.StringVar()
        self.time_var.set(f"{self.mode}: {self.format_time(self.remaining_time)}")
        self.timer_label = tk.Label(root, textvariable=self.time_var,
                                    font=("Helvetica", 36), bg="#f0f0f0")
        self.timer_label.pack(pady=10)
        
        # Cycle display
        self.cycle_var = tk.StringVar()
        self.cycle_var.set(f"Cycle: {self.cycle_count}")
        self.cycle_label = tk.Label(root, textvariable=self.cycle_var,
                                    font=("Helvetica", 12), bg="#f0f0f0")
        self.cycle_label.pack(pady=5)
        
        # Buttons
        button_frame = tk.Frame(root, bg="#f0f0f0")
        button_frame.pack(pady=10)
        self.start_button = tk.Button(button_frame, text="Start", width=8, command=self.start_timer)
        self.start_button.grid(row=0, column=0, padx=5)
        self.pause_button = tk.Button(button_frame, text="Pause", width=8, command=self.pause_timer)
        self.pause_button.grid(row=0, column=1, padx=5)
        self.reset_button = tk.Button(button_frame, text="Reset", width=8, command=self.reset_timer)
        self.reset_button.grid(row=0, column=2, padx=5)
        
        # Menu
        menubar = tk.Menu(root)
        options_menu = tk.Menu(menubar, tearoff=0)
        options_menu.add_command(label="Settings", command=self.open_settings)
        options_menu.add_command(label="Minimize to Tray", command=self.hide_window)
        menubar.add_cascade(label="Options", menu=options_menu)
        root.config(menu=menubar)
        
        # Override close event
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # Tray icon placeholder
        self.icon = None

        # Mini timer window and label
        self.mini_window = None
        self.mini_label = None
        self._offset_x = 0
        self._offset_y = 0

    def format_time(self, seconds):
        minutes, seconds = divmod(seconds, 60)
        return f"{minutes:02}:{seconds:02}"
    
    def update_time(self):
        if self.running:
            self.time_var.set(f"{self.mode}: {self.format_time(self.remaining_time)}")
            self.update_mini_window()  # Update mini window if it exists [1]
            if self.remaining_time > 0:
                self.remaining_time -= 1
                self.root.after(1000, self.update_time)
            else:
                self.running = False
                self.handle_session_end()
    
    def handle_session_end(self):
        if self.mode == "Work":
            self.cycle_count += 1
            self.cycle_var.set(f"Cycle: {self.cycle_count}")
            if self.lock_on_break and os.name == 'nt':
                self.lock_screen()  # Lock the workstation on Windows [2]
            # Every 4th work session gets a longer break.
            self.remaining_time = self.long_break_duration if self.cycle_count % 4 == 0 else self.short_break_duration
            self.mode = "Break"
            self.time_var.set(f"{self.mode}: {self.format_time(self.remaining_time)}")
            self.running = True
            self.update_time()
        elif self.mode == "Break":
            self.mode = "Work"
            self.remaining_time = self.work_duration
            self.time_var.set(f"{self.mode}: {self.format_time(self.remaining_time)}")
            self.running = True
            self.update_time()
    
    def start_timer(self):
        if not self.running:
            self.running = True
            self.paused = False
            self.update_time()
    
    def pause_timer(self):
        if self.running:
            self.running = False
            self.paused = True
    
    def reset_timer(self):
        self.running = False
        self.paused = False
        self.mode = "Work"
        self.cycle_count = 0
        self.remaining_time = self.work_duration
        self.time_var.set(f"{self.mode}: {self.format_time(self.remaining_time)}")
        self.cycle_var.set(f"Cycle: {self.cycle_count}")
        self.update_mini_window()
    
    def lock_screen(self):
        if os.name == 'nt':
            ctypes.windll.user32.LockWorkStation()
        else:
            print("Locking screen not implemented for this OS.")
    
    def open_settings(self):
        settings_window = tk.Toplevel(self.root)
        settings_window.title("Settings")
        settings_window.geometry("300x150")
        settings_window.grab_set()
        
        lock_var = tk.BooleanVar(value=self.lock_on_break)
        tray_var = tk.BooleanVar(value=self.minimize_to_tray)
        
        tk.Checkbutton(settings_window, text="Lock screen on break", variable=lock_var).pack(anchor="w", pady=5, padx=10)
        tk.Checkbutton(settings_window, text="Enable minimize to tray", variable=tray_var).pack(anchor="w", pady=5, padx=10)
        
        def save_settings():
            self.lock_on_break = lock_var.get()
            self.minimize_to_tray = tray_var.get()
            settings_window.destroy()
        
        tk.Button(settings_window, text="Save", command=save_settings).pack(pady=10)
    
    def hide_window(self):
        self.root.withdraw()

    def on_closing(self):
        if self.minimize_to_tray:
            self.hide_window()
        else:
            self.root.destroy()
    
    def create_image(self):
        width = 64
        height = 64
        image = Image.new("RGB", (width, height), "black")
        dc = ImageDraw.Draw(image)
        dc.text((width // 4, height // 3), "P", fill="white")
        return image
    
    def create_tray_icon(self):
        image = self.create_image()
        menu = pystray.Menu(
            pystray.MenuItem("Show", self.show_window),
            pystray.MenuItem("Start", self.start_timer),
            pystray.MenuItem("Pause", self.pause_timer),
            pystray.MenuItem("Reset Timer", self.reset_timer),
            pystray.MenuItem("Mini Timer", self.show_mini_timer),
            pystray.MenuItem("Quit", self.quit_app)
        )
        self.icon = pystray.Icon("pomodoro", image, "Pomodoro Timer", menu)
        threading.Thread(target=self.icon.run, daemon=True).start()
    
    def show_window(self, icon, item):
        self.root.after(0, self._show_window)
    
    def _show_window(self):
        self.root.deiconify()
        if self.icon:
            self.icon.stop()
            self.icon = None

    def show_mini_timer(self, icon, item):
        self.root.after(0, self._show_mini_timer)
    
    def _show_mini_timer(self):
        if self.mini_window is None or not tk.Toplevel.winfo_exists(self.mini_window):
            self.mini_window = tk.Toplevel(self.root)
            self.mini_window.overrideredirect(True)  # Remove titlebar [3]
            self.mini_window.geometry("260x50")
            self.mini_window.attributes("-topmost", True)
            self.mini_window.attributes("-alpha", 0.66)
            self.mini_label = tk.Label(self.mini_window, text=f"{self.mode}: {self.format_time(self.remaining_time)}",
                                       font=("Helvetica", 32))
            self.mini_label.pack(expand=True, fill="both")
            self.update_mini_window()
            
            # Bind events for dragging the window from anywhere in it.
            self.mini_window.bind("<ButtonPress-1>", self.start_move)
            self.mini_window.bind("<B1-Motion>", self.do_move)
            self.mini_label.bind("<ButtonPress-1>", self.start_move)
            self.mini_label.bind("<B1-Motion>", self.do_move)
        else:
            self.mini_window.deiconify()
            self.mini_window.lift()
    
    def start_move(self, event):
        self._offset_x = event.x
        self._offset_y = event.y
    
    def do_move(self, event):
        x = event.x_root - self._offset_x
        y = event.y_root - self._offset_y
        self.mini_window.geometry(f"+{x}+{y}")
    
    def update_mini_window(self):
        if self.mini_window is not None and tk.Toplevel.winfo_exists(self.mini_window):
            self.mini_label.config(text=f"{self.mode}: {self.format_time(self.remaining_time)}")
            # Change background color based on mode: red-ish for work, light green for break.
            bg_color = "#ff9999" if self.mode == "Work" else "#90EE90"
            self.mini_window.configure(bg=bg_color)
            self.mini_label.configure(bg=bg_color)
    
    def quit_app(self, icon, item):
        if self.icon:
            self.icon.stop()
        self.root.after(0, self.root.destroy)

if __name__ == "__main__":
    root = tk.Tk()
    app = PomodoroTimer(root)
    root.mainloop()
