import sys
import os
import json
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox

CONFIG_FILE = "config.json"

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

    def load_config(self):
        if not os.path.exists(CONFIG_FILE):
            # Create default config if missing
            default = {
                "Documents": [".pdf", ".docx", ".txt"],
                "Images": [".jpg", ".png"],
                "Audio": [".mp3", ".wav"]
            }
            with open(CONFIG_FILE, "w") as f:
                json.dump(default, f, indent=2)
            return default
        try:
            with open(CONFIG_FILE, "r") as f:
                return json.load(f)
        except Exception as e:
            messagebox.showerror("Config Error", f"Failed to load config: {e}")
            return {}

    def pick_folder(self):
        folder = filedialog.askdirectory(title="Select Folder")
        if folder:
            self.selected_folder = folder
            self.folder_path_label.config(text=folder)
            self.log(f"Selected folder: {folder}")
        else:
            self.log("No folder selected.")

    def start_organizing(self):
        if not self.selected_folder:
            messagebox.showwarning("No Folder", "Please select a folder first.")
            self.log("Please select a folder first.")
            return
        self.log(f"Started organizing: {self.selected_folder}")
        try:
            self.organize_files()
            self.log("Done organizing.")
        except Exception as e:
            self.log(f"Error: {e}")

    def organize_files(self):
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
            if os.path.isfile(item_path):
                _, ext = os.path.splitext(item)
                ext = ext.lower()
                target_folder = ext_to_folder.get(ext)
                if target_folder:
                    dest_folder = os.path.join(folder, target_folder)
                    if not os.path.exists(dest_folder):
                        os.makedirs(dest_folder)
                else:
                    dest_folder = others_folder
                dest_path = os.path.join(dest_folder, item)
                try:
                    shutil.move(item_path, dest_path)
                    self.log(f"Moved: {item} -> {os.path.basename(dest_folder)}")
                except Exception as e:
                    self.log(f"Failed to move {item}: {e}")

    def open_config(self):
        # Open config.json in default editor
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
        self.log_box.config(state='normal')
        self.log_box.insert(tk.END, message + "\n")
        self.log_box.see(tk.END)
        self.log_box.config(state='disabled')

if __name__ == "__main__":
    app = FileOrganizerGUI()
    app.mainloop()
