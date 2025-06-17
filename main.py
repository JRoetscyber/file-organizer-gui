import sys
import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
import datetime

CONFIG_FILE = "config.json"
LOG_FILE = "log.txt"

class FileOrganizerGUI(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("File Organizer")
        self.geometry("500x350")
        self.selected_folder = None
        self.config_data = self.load_config()

        # Label
        self.label = tk.Label(self, text="Choose folder to organize")
        self.label.pack(pady=(10, 5))

        # Folder picker
        folder_frame = tk.Frame(self)
        folder_frame.pack(pady=5)
        self.folder_button = tk.Button(folder_frame, text="Pick Folder", command=self.pick_folder)
        self.folder_button.pack(side=tk.LEFT)
        self.folder_path_label = tk.Label(folder_frame, text="No folder selected", anchor="w")
        self.folder_path_label.pack(side=tk.LEFT, padx=10)

        # Start button
        self.start_button = tk.Button(self, text="Start Organizing", command=self.start_organizing)
        self.start_button.pack(pady=10)

        # Config button (optional)
        self.config_button = tk.Button(self, text="Edit Config", command=self.open_config)
        self.config_button.pack(pady=5)

        # Status/log message box (scrollable)
        self.log_box = scrolledtext.ScrolledText(self, height=10, state='disabled')
        self.log_box.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.show_recent_log_entries()

    def load_config(self):
        """Load config.json or show error popup if missing/invalid."""
        if not os.path.exists(CONFIG_FILE):
            messagebox.showerror("Config Error", f"{CONFIG_FILE} is missing. Please create or restore it.")
            self.quit()
            return {}
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Config Error", f"Failed to load config: {e}")
            self.quit()
            return {}

    def pick_folder(self):
        """Open folder picker dialog."""
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.selected_folder = folder
            self.folder_path_label.config(text=folder)
            self.log(f"Selected folder: {folder}")
        else:
            self.log("No folder selected.")

    def start_organizing(self):
        """Ask for confirmation, then organize files."""
        if not self.selected_folder:
            messagebox.showwarning("No Folder", "Please select a folder first.")
            self.log("Please select a folder first.")
            return
        # Ask for confirmation
        answer = messagebox.askyesno("Are you sure?", f"Organize files in:\n{self.selected_folder}?")
        if not answer:
            self.log("Organizing cancelled by user.")
            return
        self.log(f"Started organizing: {self.selected_folder}")
        try:
            self.organize_files()
            self.log("Done organizing.")
            messagebox.showinfo("Done", "Sorting complete!")
        except Exception as e:
            self.log(f"Error: {e}")
            messagebox.showerror("Error", f"An error occurred: {e}")

    def organize_files(self):
        """Move files into folders based on config.json."""
        folder = self.selected_folder
        config = self.config_data
        ext_to_folder = {}
        for folder_name, exts in config.items():
            for ext in exts:
                ext_to_folder[ext.lower()] = folder_name

        others_folder = os.path.join(folder, "Others")
        if not os.path.exists(others_folder):
            os.makedirs(others_folder)

        for item in os.listdir(folder):
            item_path = os.path.join(folder, item)
            # Skip directories and hidden files
            if not os.path.isfile(item_path) or item.startswith('.'):
                continue
            _, ext = os.path.splitext(item)
            ext = ext.lower()
            target_folder = ext_to_folder.get(ext)
            if target_folder:
                dest_folder = os.path.join(folder, target_folder)
                if not os.path.exists(dest_folder):
                    try:
                        os.makedirs(dest_folder)
                    except Exception as e:
                        self.log(f"Failed to create folder {dest_folder}: {e}")
                        self.write_log(f"ERROR: Failed to create folder {dest_folder}: {e}")
                        dest_folder = others_folder
            else:
                dest_folder = others_folder

            dest_path = os.path.join(dest_folder, item)
            base, extension = os.path.splitext(item)
            counter = 1
            # Handle file name conflicts
            while os.path.exists(dest_path):
                dest_path = os.path.join(dest_folder, f"{base} ({counter}){extension}")
                counter += 1
            try:
                shutil.move(item_path, dest_path)
                msg = f"Moved: {item} -> {os.path.basename(dest_folder)}"
                self.log(msg)
                self.write_log(f"Moved {item} → {os.path.relpath(dest_path, folder)}")
            except PermissionError:
                err = f"Permission denied: {item}"
                self.log(err)
                self.write_log(f"ERROR: Permission denied for {item}")
            except Exception as e:
                err = f"Failed to move {item}: {e}"
                self.log(err)
                self.write_log(f"ERROR: Failed to move {item}: {e}")

    def write_log(self, message):
        """Write a log entry to log.txt with timestamp."""
        timestamp = datetime.datetime.now().strftime("[%Y-%m-%d %H:%M]")
        with open(LOG_FILE, "a", encoding="utf-8") as f:
            f.write(f"{timestamp} {message}\n")

    def show_recent_log_entries(self):
        """Show last 10 log entries in the GUI log box."""
        if not os.path.exists(LOG_FILE):
            return
        try:
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
                last_lines = lines[-10:] if len(lines) > 10 else lines
                self.log_box.config(state='normal')
                self.log_box.insert(tk.END, "--- Recent log entries ---\n")
                for line in last_lines:
                    self.log_box.insert(tk.END, line)
                self.log_box.insert(tk.END, "\n")
                self.log_box.config(state='disabled')
        except Exception:
            pass

    def open_config(self):
        """Open config.json in the default editor."""
        try:
            if sys.platform == "win32":
                os.startfile(CONFIG_FILE)
            elif sys.platform == "darwin":
                os.system(f"open {CONFIG_FILE}")
            else:
                os.system(f"xdg-open {CONFIG_FILE}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not open config: {e}")

    def log(self, message):
        """Show a message in the GUI log box."""
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

if __name__ == "__main__":
    app = FileOrganizerGUI()
    app.mainloop()
