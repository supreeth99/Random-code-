import tkinter as tk
from tkinter import messagebox
import win32serviceutil
import win32service
import subprocess
import os
import time
import threading

SERVICE_NAME = "MyAppService"  # Unique name for your service
SERVICE_EXE_PATH = r"C:\path\to\your\compiled_service.exe"  # Update this with your EXE path


class ServiceManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Service Manager")
        self.root.geometry("400x250")

        # Status label
        self.status_label = tk.Label(
            root, text="Service Status: Unknown", font=("Arial", 14), bg="gray", fg="white"
        )
        self.status_label.pack(fill="x", pady=10)

        # Status box
        self.status_box = tk.Canvas(root, width=50, height=50, bg="gray", bd=0, highlightthickness=0)
        self.status_box.pack(pady=10)

        # Buttons
        self.button_frame = tk.Frame(root)
        self.button_frame.pack(pady=10)

        self.install_button = tk.Button(
            self.button_frame, text="Install Service", command=self.install_service, width=15
        )
        self.install_button.grid(row=0, column=0, padx=5)

        self.start_button = tk.Button(
            self.button_frame, text="Start Service", command=self.start_service, width=15
        )
        self.start_button.grid(row=0, column=1, padx=5)

        self.stop_button = tk.Button(
            self.button_frame, text="Stop Service", command=self.stop_service, width=15
        )
        self.stop_button.grid(row=1, column=0, padx=5, pady=5)

        self.remove_button = tk.Button(
            self.button_frame, text="Remove Service", command=self.remove_service, width=15
        )
        self.remove_button.grid(row=1, column=1, padx=5, pady=5)

        self.refresh_button = tk.Button(
            root, text="Refresh Status", command=self.refresh_status, width=20
        )
        self.refresh_button.pack(pady=5)

        # Start background thread to monitor status
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_service_status, daemon=True)
        self.monitor_thread.start()

    def update_status(self, status, color):
        """Update the status label and status box color."""
        self.status_label.config(text=f"Service Status: {status}", bg=color)
        self.status_box.config(bg=color)

    def refresh_status(self):
        """Check and update the service status."""
        try:
            status = win32serviceutil.QueryServiceStatus(SERVICE_NAME)[1]
            if status == win32service.SERVICE_RUNNING:
                self.update_status("Running", "green")
            elif status == win32service.SERVICE_STOPPED:
                self.update_status("Stopped", "red")
            else:
                self.update_status("Pending", "orange")
        except Exception:
            self.update_status("Not Installed", "gray")

    def monitor_service_status(self):
        """Monitor the service status in the background."""
        while self.running:
            self.refresh_status()
            time.sleep(2)

    def install_service(self):
        """Install the service."""
        try:
            # Install the service with the compiled EXE
            subprocess.run(
                [
                    "sc", "create", SERVICE_NAME,
                    "binPath=", f'"{SERVICE_EXE_PATH}"',
                    "start=", "auto"
                ],
                check=True,
                shell=True
            )
            messagebox.showinfo("Success", "Service installed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to install service: {str(e)}")

    def start_service(self):
        """Start the service."""
        try:
            win32serviceutil.StartService(SERVICE_NAME)
            messagebox.showinfo("Success", "Service started successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start service: {str(e)}")

    def stop_service(self):
        """Stop the service."""
        try:
            win32serviceutil.StopService(SERVICE_NAME)
            messagebox.showinfo("Success", "Service stopped successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop service: {str(e)}")

    def remove_service(self):
        """Remove the service."""
        try:
            # Remove the service
            subprocess.run(
                ["sc", "delete", SERVICE_NAME],
                check=True,
                shell=True
            )
            messagebox.showinfo("Success", "Service removed successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to remove service: {str(e)}")

    def on_close(self):
        """Stop monitoring and close the app."""
        self.running = False
        self.root.destroy()


# Create the Tkinter application
if __name__ == "__main__":
    root = tk.Tk()
    app = ServiceManagerApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_close)
    root.mainloop()
