import customtkinter as ctk
from tkinter import messagebox
import subprocess
import os

class YTDTab(ctk.CTkFrame):
    def _log_error(self, msg):
        parent = getattr(self, 'master', None)
        while parent is not None:
            if hasattr(parent, 'log_error'):
                parent.log_error(f"[YTDTab] {msg}")
                break
            parent = getattr(parent, 'master', None)
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")
        ctk.CTkLabel(self, text="YT Downloader", font=ctk.CTkFont(size=22, weight="bold")).pack(pady=(18, 2))

        url_row = ctk.CTkFrame(self, fg_color="transparent")
        url_row.pack(fill="x", padx=40, pady=(10, 10))
        ctk.CTkLabel(url_row, text="Video URL:", width=100, anchor="w").pack(side="left")
        self.url_entry = ctk.CTkEntry(url_row, width=260)
        self.url_entry.pack(side="left", padx=(0, 8))

        folder_row = ctk.CTkFrame(self, fg_color="transparent")
        folder_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(folder_row, text="Output folder:", width=100, anchor="w").pack(side="left")
        self.folder_entry = ctk.CTkEntry(folder_row, width=260)
        self.folder_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(folder_row, text="Browse", width=70, command=self.select_folder).pack(side="left")

        ctk.CTkButton(self, text="Download", command=self.download_video, width=120).pack(pady=18)

        self.status_label = ctk.CTkLabel(self, text="", text_color="green", font=ctk.CTkFont(size=12))
        self.status_label.pack(pady=(0, 5))

    def select_folder(self):
        from tkinter import filedialog
        try:
            folder = filedialog.askdirectory(title="Select output folder")
        except Exception as e:
            self._log_error(f"Folder dialog error: {e}")
            messagebox.showerror("Folder Error", "Could not open folder dialog.\n\nDetails: " + str(e))
            return
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

    def download_video(self):
        url = self.url_entry.get().strip()
        output_folder = self.folder_entry.get().strip()
        if not url:
            self._log_error("No video URL entered.")
            messagebox.showwarning("No URL", "Please enter a video URL.")
            return
        if not output_folder or not os.path.isdir(output_folder):
            self._log_error("No valid output folder selected.")
            messagebox.showwarning("No output folder", "Please select a valid output folder.")
            return
        self.status_label.configure(text="Downloading...", text_color="yellow")
        self.update_idletasks()
        exe_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(exe_dir)
        ytdlp_path = os.path.join(parent_dir, "yt-dlp.exe")
        if not os.path.isfile(ytdlp_path):
            self._log_error("yt-dlp.exe not found in the application directory.")
            self.status_label.configure(text="yt-dlp.exe not found!", text_color="red")
            messagebox.showerror("Error", "yt-dlp.exe not found in the application directory.")
            return
        try:
            result = subprocess.run(
                [ytdlp_path, "-P", output_folder, url],
                capture_output=True, text=True
            )
            if result.returncode == 0:
                self.status_label.configure(text="Download complete!", text_color="green")
                messagebox.showinfo("Success", "Video downloaded successfully.")
            else:
                self._log_error(f"[WinError] {result.stderr}")
                self.status_label.configure(text="Download failed.", text_color="red")
                messagebox.showerror("Error", result.stderr)
        except Exception as e:
            self._log_error(f"[WinError] {e}")
            self.status_label.configure(text="Download failed.", text_color="red")
            messagebox.showerror("Error", str(e))
