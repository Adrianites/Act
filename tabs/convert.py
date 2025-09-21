import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import json

VIDEO_FORMATS = ["mp4", "avi", "mov", "webm", "mkv", "gif"]
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
    def _log_error(self, msg):
        if hasattr(self, '_main_window') and self._main_window and hasattr(self._main_window, 'log_error'):
            self._main_window.log_error(msg)
    def __init__(self, master):
        super().__init__(master)
        self._main_window = None
        parent = master
        while parent is not None:
            if hasattr(parent, 'log_error'):
                self._main_window = parent
                break
            parent = getattr(parent, 'master', None)
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
        try:
            file_path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        except Exception as e:
            self._log_error(f"File dialog error: {e}")
            messagebox.showerror("File Error", "Could not open file dialog.\n\nDetails: " + str(e))
            return
        if file_path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, file_path)
            self.status_label.configure(text="")
            self.update_output_formats(file_path)

    def update_output_formats(self, file_path):
        try:
            ext = os.path.splitext(file_path)[1][1:].lower()
            file_type = EXT_TO_TYPE.get(ext)
            def dedup(seq):
                seen = set()
                return [x for x in seq if not (x in seen or seen.add(x))]
            if file_type == "video":
                formats = dedup(VIDEO_FORMATS + AUDIO_FORMATS + IMAGE_FORMATS)
            elif file_type == "audio":
                formats = dedup(AUDIO_FORMATS + IMAGE_FORMATS)
            elif file_type == "image":
                formats = dedup(IMAGE_FORMATS)
            else:
                formats = []
            self.format_menu.configure(values=formats)
            if formats:
                self.format_var.set(formats[0])
            else:
                self.format_var.set("")
        except Exception as e:
            self._log_error(f"Update output formats error: {e}")
            messagebox.showerror("Format Error", "Could not update output formats.\n\nDetails: " + str(e))

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
            import sys
            creationflags = 0
            if sys.platform == "win32":
                creationflags = getattr(subprocess, 'CREATE_NO_WINDOW', 0)
            input_ext = os.path.splitext(input_file)[1][1:].lower()
            is_video_to_image = EXT_TO_TYPE.get(input_ext) == "video" and output_format.lower() in IMAGE_FORMATS
            if output_format.lower() == "ico":
                probe = subprocess.run([
                    'ffprobe', '-v', 'error', '-select_streams', 'v:0',
                    '-show_entries', 'stream=width,height', '-of', 'csv=p=0', input_file
                ], capture_output=True, text=True, creationflags=creationflags)
                dims = probe.stdout.strip().split(',')
                if len(dims) == 2:
                    width, height = int(dims[0]), int(dims[1])
                    if width > 256 or height > 256:
                        scale_arg = f"scale='min(256,iw)':'min(256,ih)'"
                        cmd = [
                            'ffmpeg', '-y', '-i', input_file,
                            '-vf', scale_arg,
                            '-frames:v', '1', output_file
                        ]
                    else:
                        cmd = ['ffmpeg', '-y', '-i', input_file, '-frames:v', '1', output_file]
                else:
                    cmd = ['ffmpeg', '-y', '-i', input_file, '-frames:v', '1', output_file]
                subprocess.run(cmd, check=True, creationflags=creationflags)
            elif is_video_to_image:
                subprocess.run(['ffmpeg', '-y', '-i', input_file, '-frames:v', '1', output_file], check=True, creationflags=creationflags)
            else:
                subprocess.run(['ffmpeg', '-y', '-i', input_file, output_file], check=True, creationflags=creationflags)
            self.status_label.configure(text=f"Success! Saved to:\n{output_file}", text_color="green")
            messagebox.showinfo("Success", f"File converted to {output_file}")
        except Exception as e:
            self.status_label.configure(text="Conversion failed.", text_color="red")
            messagebox.showerror("Error", str(e))
            if self._main_window and hasattr(self._main_window, 'log_error'):
                self._main_window.log_error(f"[ConvertTab] {str(e)}")