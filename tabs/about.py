import customtkinter as ctk

DEPENDENCIES = [
    ("CustomTkinter", "https://github.com/TomSchimansky/CustomTkinter"),
    ("Pillow", "https://pypi.org/project/pillow/"),
    ("FFmpeg", "https://ffmpeg.org/"),
    ("yt-dlp", "https://github.com/yt-dlp/yt-dlp"),
    ("Python", "https://python.org/"),
    ("tkinter", "https://docs.python.org/3/library/tkinter.html"),
]

class AboutTab(ctk.CTkFrame):
    def __init__(self, master):
        super().__init__(master, fg_color="transparent")

        ctk.CTkLabel(
            self,
            text="About",
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="transparent"
        ).pack(pady=(18, 2))

        ctk.CTkLabel(
            self,
            text="This application uses the following dependencies:\n",
            justify="center",
            font=ctk.CTkFont(size=14),
            fg_color="transparent"
        ).pack(padx=40, pady=(10, 0))

        for name, url in DEPENDENCIES:
            label = ctk.CTkLabel(
                self,
                text=name,
                font=ctk.CTkFont(size=15, weight="bold", underline=True),
                text_color="#1976d2",
                cursor="hand2",
                fg_color="transparent"
            )
            label.pack(pady=2)
            label.bind("<Button-1>", lambda e, link=url, dep=name: self.copy_link(link, dep))

        ctk.CTkLabel(
            self,
            text="Adrian's Conversion Tool",
            font=ctk.CTkFont(size=16, weight="bold"),
            fg_color="transparent"
        ).pack(side="bottom", pady=20)

        self.status_label = ctk.CTkLabel(
            self,
            text="",
            font=ctk.CTkFont(size=12),
            text_color="green",
            fg_color="transparent"
        )
        self.status_label.place(relx=0.5, rely=0.85, anchor="s")

    def copy_link(self, link, dep):
        self.clipboard_clear()
        self.clipboard_append(link)
        self.status_label.configure(text=f"{dep} link copied!")
        self.after(1500, lambda: self.status_label.configure(text=""))