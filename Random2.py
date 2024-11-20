import tkinter as tk
from tkinter import messagebox
import subprocess
import psutil  # To monitor running processes
import os
import time
import threading

EXE_PATH = r"C:\path\to\your\compiled_service.exe"  # Update this with your EXE file path


class ExeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Process Manager")
        self.root.geometry("400x250")

        self.process = None  # Reference to the running EXE process

        # Status label
        self.status_label = tk.Label(
            root, text="Process Status: Unknown", font=("Arial", 14), bg="gray", fg="white"
        )
        self.status_label.pack(fill="x", pady=10)

        # Status box
        self.status_box = tk.Canvas(root, width=50, height=50, bg="gray", bd=0, highlightthickness=0)
        self.status_box.pack(pady=10)

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.start_button = tk.Button(
            self.button_frame, text="Start Process", command=self.start_process, width=15
        )
        self.start_button.grid(row=0, column=0, padx=5)

        self.stop_button = tk.Button(
            self.button_frame, text="Stop Process", command=self.stop_process, width=15
        )
        self.stop_button.grid(row=0, column=1, padx=5)

        self.refresh_button = tk.Button(
            root, text="Refresh Status", command=self.refresh_status, width=20
        )
        self.refresh_button.pack(pady=5)

        # Start background thread to monitor process status
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_process_status, daemon=True)
        self.monitor_thread.start()

    def update_status(self, status, color):
        """Update the status label and status box color."""
        self.status_label.config(text=f"Process Status: {status}", bg=color)
        self.status_box.config(bg=color)

    def is_process_running(self):
        """Check if the EXE is running as a process."""
        exe_name = os.path.basename(EXE_PATH)
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"] == exe_name:
                return True
        return False

    def refresh_status(self):
        """Check and update the process status."""
        if self.is_process_running():
            self.update_status("Running", "green")
        else:
            self.update_status("Not Running", "red")

    def monitor_process_status(self):
        """Monitor the process status in the background."""
        while self.running:
            self.refresh_status()
            time.sleep(2)

    def start_process(self):
        """Start the EXE process."""
        if self.is_process_running():
            messagebox.showinfo("Info", "Process is already running.")
            return

        try:
            self.process = subprocess.Popen([EXE_PATH], cwd=os.path.dirname(EXE_PATH))
            messagebox.showinfo("Success", "Process started successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start process: {str(e)}")

    def stop_process(self):
        """Stop the EXE process."""
        exe_name = os.path.basename(EXE_PATH)
        try:
            for proc in psutil.process_iter(attrs=["pid", "name"]):
                if proc.info["name"] == exe_name:
                    proc.terminate()
                    messagebox.showinfo("Success", "Process stopped successfully!")
                    return
            messagebox.showinfo("Info", "Process is not running.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop process: {str(e)}")

    def on_close(self):
        """Stop monitoring and close the app."""
        self.running = False
        self.root.destroy()


# Create the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = ExeManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()