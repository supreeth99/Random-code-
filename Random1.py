import tkinter as tk
from tkinter import messagebox
import win32serviceutil
import win32service
import subprocess
import os
import time
import threading

SERVICE_NAME = "MyAppService"
SERVICE_EXE_PATH = r"C:\path\to\your\api.exe"  # Update this with the path to your EXE


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
            subprocess.run(
                ["python", "service_script.py", "install"], check=True, cwd=os.path.dirname(SERVICE_EXE_PATH)
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
            subprocess.run(
                ["python", "service_script.py", "remove"], check=True, cwd=os.path.dirname(SERVICE_EXE_PATH)
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
    
import tkinter as tk
from tkinter import messagebox
import subprocess
import psutil
import os
import time
import threading

# List of EXEs to manage (Update these paths as needed)
EXE_PATHS = [
    r"C:\path\to\service1.exe",
    r"C:\path\to\service2.exe",
    r"C:\path\to\service3.exe",
]


class ExeManagerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Multiple EXE Manager")
        self.root.geometry("500x400")

        self.processes = {}  # To store references to running processes (independent for each EXE)

        # Create a frame to hold the EXE entries
        self.exe_frame = tk.Frame(root)
        self.exe_frame.pack(fill="both", expand=True, pady=10)

        # Initialize UI components for each EXE
        self.exe_controls = []
        for exe_path in EXE_PATHS:
            self.create_exe_control(exe_path)

        # Start background thread to monitor process statuses
        self.running = True
        self.monitor_thread = threading.Thread(target=self.monitor_process_status, daemon=True)
        self.monitor_thread.start()

    def create_exe_control(self, exe_path):
        """Create controls for each EXE (status, start, stop buttons)."""
        frame = tk.Frame(self.exe_frame, bd=2, relief="groove", pady=5)
        frame.pack(fill="x", padx=10, pady=5)

        exe_name = os.path.basename(exe_path)

        # Label for the EXE name
        name_label = tk.Label(frame, text=exe_name, font=("Arial", 12, "bold"))
        name_label.grid(row=0, column=0, padx=5, sticky="w")

        # Status label
        status_label = tk.Label(frame, text="Status: Unknown", width=20, bg="gray", fg="white")
        status_label.grid(row=0, column=1, padx=5)

        # Start button
        start_button = tk.Button(frame, text="Start", width=10, command=lambda: self.start_process(exe_path, status_label))
        start_button.grid(row=0, column=2, padx=5)

        # Stop button
        stop_button = tk.Button(frame, text="Stop", width=10, command=lambda: self.stop_process(exe_path, status_label))
        stop_button.grid(row=0, column=3, padx=5)

        # Add to list for future reference
        self.exe_controls.append({"path": exe_path, "status_label": status_label})

    def update_status(self, status_label, status, color):
        """Update the status label for a specific EXE."""
        status_label.config(text=f"Status: {status}", bg=color)

    def is_process_running(self, exe_path):
        """Check if the EXE is running as a process."""
        exe_name = os.path.basename(exe_path)
        for proc in psutil.process_iter(attrs=["pid", "name"]):
            if proc.info["name"] == exe_name:
                return True
        return False

    def refresh_status(self):
        """Check and update the status of all EXEs."""
        for control in self.exe_controls:
            exe_path = control["path"]
            status_label = control["status_label"]
            if self.is_process_running(exe_path):
                self.update_status(status_label, "Running", "green")
            else:
                self.update_status(status_label, "Not Running", "red")

    def monitor_process_status(self):
        """Monitor the status of all EXEs in the background."""
        while self.running:
            self.refresh_status()
            time.sleep(2)

    def start_process(self, exe_path, status_label):
        """Start the EXE process."""
        if self.is_process_running(exe_path):
            messagebox.showinfo("Info", f"{os.path.basename(exe_path)} is already running.")
            return

        try:
            process = subprocess.Popen([exe_path], cwd=os.path.dirname(exe_path))
            self.processes[exe_path] = process
            self.update_status(status_label, "Running", "green")
            messagebox.showinfo("Success", f"{os.path.basename(exe_path)} started successfully!")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to start {os.path.basename(exe_path)}: {str(e)}")

    def stop_process(self, exe_path, status_label):
        """Stop the EXE process."""
        exe_name = os.path.basename(exe_path)
        try:
            for proc in psutil.process_iter(attrs=["pid", "name"]):
                if proc.info["name"] == exe_name:
                    proc.terminate()
                    self.update_status(status_label, "Not Running", "red")
                    messagebox.showinfo("Success", f"{exe_name} stopped successfully!")
                    return
            messagebox.showinfo("Info", f"{exe_name} is not running.")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to stop {exe_name}: {str(e)}")

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
    


import os
import shutil

def delete_all_files(directory):
    try:
        # Check if the directory exists
        if not os.path.exists(directory):
            print(f"The directory '{directory}' does not exist.")
            return

        # Loop through all files in the directory
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            # Check if it's a file and delete it
            if os.path.isfile(file_path):
                os.remove(file_path)
                print(f"Deleted file: {file_path}")
            # Optional: If directories should also be deleted
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
                print(f"Deleted directory: {file_path}")

        print("All files and directories have been deleted successfully.")
    
    except Exception as e:
        print(f"Error: {e}")

# Example usage
directory_path = r"C:\path\to\your\directory"  # Update with your path
delete_all_files(directory_path)

