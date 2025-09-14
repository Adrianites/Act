import customtkinter as ctk
from tkinter import messagebox
import subprocess
import os

class YTDTab(ctk.CTkFrame):
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
        folder = filedialog.askdirectory(title="Select output folder")
        if folder:
            self.folder_entry.delete(0, "end")
            self.folder_entry.insert(0, folder)

    def download_video(self):
        url = self.url_entry.get().strip()
        output_folder = self.folder_entry.get().strip()
        if not url:
            messagebox.showwarning("No URL", "Please enter a video URL.")
            return
        if not output_folder or not os.path.isdir(output_folder):
            messagebox.showwarning("No output folder", "Please select a valid output folder.")
            return
        self.status_label.configure(text="Downloading...", text_color="yellow")
        self.update_idletasks()
        try:
            result = subprocess.run([
                "yt-dlp", "-P", output_folder, url
            ], capture_output=True, text=True)
            if result.returncode == 0:
                self.status_label.configure(text="Download complete!", text_color="green")
                messagebox.showinfo("Success", "Video downloaded successfully.")
            else:
                self.status_label.configure(text="Download failed.", text_color="red")
                messagebox.showerror("Error", result.stderr)
        except Exception as e:
            self.status_label.configure(text="Download failed.", text_color="red")
            messagebox.showerror("Error", str(e))
