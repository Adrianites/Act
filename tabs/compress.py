import customtkinter as ctk
from tkinter import filedialog, messagebox
import subprocess
import os
import json

VIDEO_FORMATS = ["mp4", "avi", "mov", "webm", "gif", "mkv"]
AUDIO_FORMATS = ["mp3", "wav", "flac", "aac", "ogg", "wma", "m4a"]
IMAGE_FORMATS = ["png", "jpg", "jpeg", "gif", "bmp", "tiff", "webp"]

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
}

SETTINGS_FILE = "settings.json"

class CompressTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master)
        ctk.CTkLabel(self, text="Compress Tool", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(18, 2))
        ctk.CTkLabel(
            self,
            text="Note: The larger the file, the more inaccurate the final size may be.",
            font=ctk.CTkFont(size=12),
            text_color="orange"
        ).pack(pady=(0, 10))

        input_row = ctk.CTkFrame(self)
        input_row.pack(fill="x", padx=40, pady=(10, 10))
        ctk.CTkLabel(input_row, text="Input file:", width=100, anchor="w").pack(side="left")
        self.input_entry = ctk.CTkEntry(input_row, width=260)
        self.input_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(input_row, text="Browse", width=70, command=self.select_file).pack(side="left")

        size_row = ctk.CTkFrame(self)
        size_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(size_row, text="Target size (MB):", width=120, anchor="w").pack(side="left", padx=(0, 8))
        self.size_var = ctk.DoubleVar(value=8)
        self.size_slider = ctk.CTkSlider(size_row, from_=1, to=100, variable=self.size_var, width=180)
        self.size_slider.pack(side="left", padx=(0, 8))
        self.size_entry = ctk.CTkEntry(size_row, width=60, textvariable=self.size_var)
        self.size_entry.pack(side="left")

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

        ctk.CTkButton(self, text="Compress", command=self.compress_file, width=120).pack(pady=18)

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

    def compress_file(self):
        input_file = self.input_entry.get().strip()
        output_name = self.output_entry.get().strip()
        output_format = self.format_var.get()
        target_size_mb = self.size_var.get()
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
        if target_size_mb < 1:
            messagebox.showwarning("Invalid size", "Target size must be at least 1 MB.")
            return

        self.status_label.configure(text="Compressing...", text_color="yellow")
        self.update_idletasks()

        try:
            ext = os.path.splitext(input_file)[1][1:].lower()
            file_type = EXT_TO_TYPE.get(ext)
            if file_type == "video":
                # Get duration
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                duration = float(result.stdout.strip()) if result.stdout.strip() else 0
                if duration == 0:
                    raise Exception("Could not determine video duration.")
                target_bitrate = int((target_size_mb * 8192) / duration)
                ffmpeg_cmd = [
                    'ffmpeg', '-y', '-i', input_file,
                    '-b:v', f'{target_bitrate}k',
                    '-bufsize', f'{target_bitrate}k',
                    output_file
                ]
            elif file_type == "audio":
                result = subprocess.run(
                    ['ffprobe', '-v', 'error', '-show_entries', 'format=duration', '-of', 'default=noprint_wrappers=1:nokey=1', input_file],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
                )
                duration = float(result.stdout.strip()) if result.stdout.strip() else 0
                if duration == 0:
                    raise Exception("Could not determine audio duration.")
                target_bitrate = int((target_size_mb * 8192) / duration)
                ffmpeg_cmd = [
                    'ffmpeg', '-y', '-i', input_file,
                    '-b:a', f'{target_bitrate}k',
                    output_file
                ]
            elif file_type == "image":
                if output_format in ["jpg", "jpeg"]:
                    qscale = int(2 + (target_size_mb - 1) * (31 - 2) / 99)
                    qscale = max(2, min(qscale, 31))
                    ffmpeg_cmd = [
                        'ffmpeg', '-y', '-i', input_file,
                        '-q:v', str(qscale),
                        output_file
                    ]
                elif output_format == "png":
                    compression_level = int(9 - min(max(target_size_mb, 1), 9))
                    ffmpeg_cmd = [
                        'ffmpeg', '-y', '-i', input_file,
                        '-compression_level', str(compression_level),
                        output_file
                    ]
                else:
                    raise Exception("Unsupported image format for compression.")
            else:
                raise Exception("Unsupported file type for compression.")

            subprocess.run(ffmpeg_cmd, check=True)
            actual_size = os.path.getsize(output_file) / (1024 * 1024)
            self.status_label.configure(
                text=f"Done! Output size: {actual_size:.2f} MB\nSaved to: {output_file}",
                text_color="green"
            )
            messagebox.showinfo("Success", f"File compressed to {actual_size:.2f} MB\nSaved to: {output_file}")
        except Exception as e:
            self.status_label.configure(text="Compression failed.", text_color="red")
            messagebox.showerror("Error", str(e))