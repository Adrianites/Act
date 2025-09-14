import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import json

VIDEO_FORMATS = ["mp4", "avi", "mov", "webm", "gif", "mkv"]
AUDIO_FORMATS = ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"]
IMAGE_FORMATS = ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp", "ico"]

EXT_TO_TYPE = {
    "mp4": "video",
    "avi": "video",
    "mov": "video",
    "webm": "video",
    "gif": "video",
    "mkv": "video",
    "mp3": "audio",
    "wav": "audio",
    "flac": "audio",
    "aac": "audio",
    "ogg": "audio",
    "wma": "audio",
    "m4a": "audio",
    "png": "image",
    "jpg": "image",
    "jpeg": "image",
    "bmp": "image",
    "tiff": "image",
    "webp": "image",
    "ico": "image",
}
SETTINGS_FILE = "settings.json"


class ConvertTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Convert Tool", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(18, 2))

        input_row = ctk.CTkFrame(self)
        input_row.pack(fill="x", padx=40, pady=(10, 10))
        ctk.CTkLabel(input_row, text="Input file:", width=100, anchor="w").pack(side="left")
        self.input_entry = ctk.CTkEntry(input_row, width=260)
        self.input_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(input_row, text="Browse", width=70, command=self.select_file).pack(side="left")

        output_row = ctk.CTkFrame(self)
        output_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(output_row, text="Output name:", width=100, anchor="w").pack(side="left")
        self.output_entry = ctk.CTkEntry(output_row, width=260)
        self.output_entry.pack(side="left")

        format_row = ctk.CTkFrame(self)
        format_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(format_row, text="Output format:", width=100, anchor="w").pack(side="left")
        self.format_var = ctk.StringVar(value="")
        self.format_menu = ctk.CTkOptionMenu(format_row, variable=self.format_var, values=[], width=120)
        self.format_menu.pack(side="left")

        ctk.CTkButton(self, text="Convert", command=self.convert_file, width=120).pack(pady=18)

        self.status_label = ctk.CTkLabel(self, text="", text_color="green", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(0, 5))

    def select_file(self):
        filetypes = [("All files", "*.*")]
        file_path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        if file_path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, file_path)
            self.status_label.configure(text="")
            self.update_output_formats(file_path)

    def update_output_formats(self, file_path):
        ext = os.path.splitext(file_path)[1][1:].lower()
        file_type = EXT_TO_TYPE.get(ext)
        if file_type == "video":
            formats = VIDEO_FORMATS + AUDIO_FORMATS + IMAGE_FORMATS
        elif file_type == "audio":
            formats = AUDIO_FORMATS
        elif file_type == "image":
            formats = IMAGE_FORMATS
        else:
            formats = []
        self.format_menu.configure(values=formats)
        if formats:
            self.format_var.set(formats[0])
        else:
            self.format_var.set("")

    def get_output_folder(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("output_folder", "")
            except Exception:
                return ""
        return ""

    def convert_file(self):
        input_file = self.input_entry.get().strip()
        output_name = self.output_entry.get().strip()
        output_format = self.format_var.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showwarning("No file", "Please select a valid input file.")
            return
        if not output_name:
            messagebox.showwarning("No output name", "Please enter an output file name.")
            return
        if not output_format:
            messagebox.showwarning("No output format", "Please select an output format.")
            return
        if not output_name.lower().endswith(f".{output_format}"):
            output_name += f".{output_format}"
        output_folder = self.get_output_folder()
        output_file = filedialog.asksaveasfilename(
            initialfile=output_name,
            defaultextension=f".{output_format}",
            filetypes=[(f"{output_format.upper()} files", f"*.{output_format}")],
            initialdir=output_folder if output_folder else None
        )
        if not output_file:
            return
        self.status_label.configure(text="Converting...", text_color="yellow")
        self.update_idletasks()
        try:
            subprocess.run(['ffmpeg', '-y', '-i', input_file, output_file], check=True)
            self.status_label.configure(text=f"Success! Saved to:\n{output_file}", text_color="green")
            messagebox.showinfo("Success", f"File converted to {output_file}")
        except Exception as e:
            self.status_label.configure(text="Conversion failed.", text_color="red")
            messagebox.showerror("Error", str(e))