import customtkinter as ctk
from tkinter import filedialog, messagebox
import json
import os

SETTINGS_FILE = "settings.json"
DEFAULT_SETTINGS = {
    "theme": "system",
    "output_folder": "",
    "button_color": "#1a73e8" 
}

class SettingsTab(ctk.CTkFrame):
    def __init__(self, master, main_window):
        super().__init__(master, fg_color="transparent")
        self.main_window = main_window
        self.settings = self.load_settings()

        ctk.CTkLabel(self, text="Settings", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(18, 2))

        theme_row = ctk.CTkFrame(self, fg_color="transparent")
        theme_row.pack(fill="x", padx=40, pady=(10, 10))
        ctk.CTkLabel(theme_row, text="Theme:", width=100, anchor="w").pack(side="left")
        self.theme_var = ctk.StringVar(value=self.settings.get("theme", "system"))
        self.theme_menu = ctk.CTkOptionMenu(
            theme_row, variable=self.theme_var, values=["system", "light", "dark"], width=120,
            command=self.change_theme
        )
        self.theme_menu.pack(side="left")

        folder_row = ctk.CTkFrame(self, fg_color="transparent")
        folder_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(folder_row, text="Output folder:", width=100, anchor="w").pack(side="left")
        self.folder_entry = ctk.CTkEntry(folder_row, width=260)
        self.folder_entry.pack(side="left", padx=(0, 8))
        self.folder_entry.insert(0, self.settings.get("output_folder", ""))
        ctk.CTkButton(folder_row, text="Browse", width=70, command=self.select_folder).pack(side="left")
        self.folder_entry.bind("<FocusOut>", lambda e: self.save_settings())
        self.folder_entry.bind("<Return>", lambda e: self.save_settings())

        self.status_label = ctk.CTkLabel(self, text="", text_color="green", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(0, 5))

    def load_settings(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    return json.load(f)
            except Exception:
                return DEFAULT_SETTINGS.copy()
        return DEFAULT_SETTINGS.copy()

    def save_settings(self):
        self.settings["theme"] = self.theme_var.get()
        self.settings["output_folder"] = self.folder_entry.get().strip()

        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(self.settings, f, indent=4)
            self.status_label.configure(text="Settings saved!", text_color="green")
        except Exception as e:
            self.status_label.configure(text="Failed to save settings.", text_color="red")
            messagebox.showerror("Error", str(e))

    def select_folder(self):
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)
            self.save_settings()

    def change_theme(self, theme):
        ctk.set_appearance_mode(theme)
        self.save_settings()
        self.status_label.configure(text=f"Theme set to {theme}", text_color="green")

    def change_button_color(self, color_name):
        self.save_settings()
        self.status_label.configure(text=f"Button color set to {color_name}", text_color="green")