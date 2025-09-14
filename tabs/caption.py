import customtkinter as ctk
from customtkinter import CTkImage
from tkinter import filedialog, messagebox
import subprocess
import os
from PIL import Image
import json

CAPTION_INPUT_FORMATS = ["mp4", "avi", "mov", "webm", "gif", "mkv", "png", "jpg", "jpeg"]
CAPTION_OUTPUT_FORMATS = ["gif", "png", "jpg", "jpeg"]
FONT_COLORS = ["white", "black", "red", "yellow", "green", "blue", "orange", "purple", "cyan"]
BORDER_COLORS = ["black", "white", "red", "yellow", "green", "blue", "orange", "purple", "cyan"]
POSITIONS = ["bottom", "center", "top"]
SETTINGS_FILE = "settings.json"


class CaptionTab(ctk.CTkFrame):
    def __init__(self, master, main_window):
        super().__init__(master, fg_color="transparent")
        self.main_window = main_window

        self.left_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.left_frame.pack(side="left", fill="both", expand=True)
        self.right_frame = ctk.CTkFrame(self, width=340, fg_color="transparent")
        self.right_frame.pack_propagate(False)
        self.right_frame.pack_forget()

        scroll = ctk.CTkScrollableFrame(self.left_frame, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=0, pady=0)

        ctk.CTkLabel(
            scroll,
            text="Caption Tool",
            font=ctk.CTkFont(size=22, weight="bold"),
            fg_color="transparent"
        ).pack(pady=(18, 2))

        
        self.preview_shown = False
        self.toggle_btn = ctk.CTkButton(
            self.left_frame, text="Show Preview >", width=120, command=self.toggle_preview
        )
        self.toggle_btn.pack(anchor="ne", padx=8, pady=(8, 0))

        
        input_row = ctk.CTkFrame(scroll, fg_color="transparent")
        input_row.pack(fill="x", padx=40, pady=(10, 10))
        ctk.CTkLabel(input_row, text="Input file:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.input_entry = ctk.CTkEntry(input_row, width=260)
        self.input_entry.pack(side="left", padx=(0, 8))
        ctk.CTkButton(input_row, text="Browse", width=70, command=self.select_file).pack(side="left")

        
        caption_row = ctk.CTkFrame(scroll, fg_color="transparent")
        caption_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(caption_row, text="Caption text:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.caption_entry = ctk.CTkEntry(caption_row, width=260)
        self.caption_entry.pack(side="left")

        
        font_size_row = ctk.CTkFrame(scroll, fg_color="transparent")
        font_size_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(font_size_row, text="Font size:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.font_size_var = ctk.IntVar(value=32)
        self.font_size_slider = ctk.CTkSlider(font_size_row, from_=10, to=1000, variable=self.font_size_var, width=180)
        self.font_size_slider.pack(side="left", padx=(0, 8))
        self.font_size_entry = ctk.CTkEntry(font_size_row, width=60, textvariable=self.font_size_var)
        self.font_size_entry.pack(side="left")

        
        font_color_row = ctk.CTkFrame(scroll, fg_color="transparent")
        font_color_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(font_color_row, text="Font color:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.font_color_var = ctk.StringVar(value=FONT_COLORS[0])
        self.font_color_menu = ctk.CTkOptionMenu(font_color_row, variable=self.font_color_var, values=FONT_COLORS, width=120)
        self.font_color_menu.pack(side="left")

        
        border_color_row = ctk.CTkFrame(scroll, fg_color="transparent")
        border_color_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(border_color_row, text="Border color:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.border_color_var = ctk.StringVar(value=BORDER_COLORS[0])
        self.border_color_menu = ctk.CTkOptionMenu(border_color_row, variable=self.border_color_var, values=BORDER_COLORS, width=120)
        self.border_color_menu.pack(side="left")

        
        border_width_row = ctk.CTkFrame(scroll, fg_color="transparent")
        border_width_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(border_width_row, text="Border width:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.border_width_var = ctk.IntVar(value=2)
        self.border_width_slider = ctk.CTkSlider(border_width_row, from_=0, to=10, variable=self.border_width_var, width=180)
        self.border_width_slider.pack(side="left", padx=(0, 8))
        self.border_width_entry = ctk.CTkEntry(border_width_row, width=60, textvariable=self.border_width_var)
        self.border_width_entry.pack(side="left")

        
        position_row = ctk.CTkFrame(scroll, fg_color="transparent")
        position_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(position_row, text="Position:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.position_var = ctk.StringVar(value=POSITIONS[0])
        self.position_menu = ctk.CTkOptionMenu(position_row, variable=self.position_var, values=POSITIONS, width=120)
        self.position_menu.pack(side="left")

        
        output_row = ctk.CTkFrame(scroll, fg_color="transparent")
        output_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(output_row, text="Output name:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.output_entry = ctk.CTkEntry(output_row, width=260)
        self.output_entry.pack(side="left")

        
        format_row = ctk.CTkFrame(scroll, fg_color="transparent")
        format_row.pack(fill="x", padx=40, pady=(0, 10))
        ctk.CTkLabel(format_row, text="Output format:", width=100, anchor="w", fg_color="transparent").pack(side="left")
        self.format_var = ctk.StringVar(value=CAPTION_OUTPUT_FORMATS[0])
        self.format_menu = ctk.CTkOptionMenu(format_row, variable=self.format_var, values=CAPTION_OUTPUT_FORMATS, width=120)
        self.format_menu.pack(side="left")

        
        ctk.CTkButton(scroll, text="Add Caption", command=self.caption_file, width=120).pack(pady=18)

        
        self.status_label = ctk.CTkLabel(scroll, text="", text_color="green", font=ctk.CTkFont(size=12), fg_color="transparent")
        self.status_label.pack(pady=(0, 5))

        
        self._preview_img = None
        self._preview_path = None

        
        self.right_preview_label = ctk.CTkLabel(self.right_frame, text="Preview will appear here", width=320, height=180, fg_color="transparent")
        self.right_preview_label.pack(padx=10, pady=10)

        
        self.caption_entry.bind("<KeyRelease>", lambda e: self.update_live_preview())
        self.font_size_slider.configure(command=lambda v: self.update_live_preview())
        self.font_size_entry.bind("<KeyRelease>", lambda e: self.update_live_preview())
        self.font_color_menu.configure(command=lambda v: self.update_live_preview())
        self.border_color_menu.configure(command=lambda v: self.update_live_preview())
        self.border_width_slider.configure(command=lambda v: self.update_live_preview())
        self.border_width_entry.bind("<KeyRelease>", lambda e: self.update_live_preview())
        self.position_menu.configure(command=lambda v: self.update_live_preview())

    def toggle_preview(self):
        if self.preview_shown:
            self.close_preview()
        else:
            self.right_frame.pack(side="right", fill="y")
            self.toggle_btn.configure(text="< Hide Preview")
            self.main_window.geometry("900x420") 
            if self._preview_path:
                self.show_preview(self._preview_path, right=True)
            self.preview_shown = True

    def close_preview(self):
        if self.preview_shown:
            self.right_frame.pack_forget()
            self.toggle_btn.configure(text="Show Preview >")
            self.main_window.geometry("560x420") 
            self.preview_shown = False

    def select_file(self):
        filetypes = [("Supported files", "*.mp4 *.avi *.mov *.webm *.gif *.mkv *.png *.jpg *.jpeg"), ("All files", "*.*")]
        file_path = filedialog.askopenfilename(title="Select file", filetypes=filetypes)
        if file_path:
            self.input_entry.delete(0, "end")
            self.input_entry.insert(0, file_path)
            self.status_label.configure(text="")
            self._preview_path = file_path
            self.show_preview(file_path)
            self.update_live_preview()

    def show_preview(self, file_path, right=False):
        ext = os.path.splitext(file_path)[1].lower()
        try:
            if ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]:
                img = Image.open(file_path)
                img.thumbnail((320, 180))
                self._preview_img = CTkImage(light_image=img, dark_image=img, size=img.size)
                if right:
                    self.right_preview_label.configure(image=self._preview_img, text="")
                else:
                    self.right_preview_label.configure(image=None, text="")
            elif ext in [".mp4", ".avi", ".mov", ".webm", ".mkv"]:
                thumb_path = file_path + "_thumb.jpg"
                subprocess.run([
                    "ffmpeg", "-y", "-i", file_path, "-vf", "thumbnail,scale=320:180", "-frames:v", "1", thumb_path
                ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                if os.path.exists(thumb_path):
                    img = Image.open(thumb_path)
                    self._preview_img = CTkImage(light_image=img, dark_image=img, size=img.size)
                    if right:
                        self.right_preview_label.configure(image=self._preview_img, text="")
                    else:
                        self.right_preview_label.configure(image=None, text="")
                    os.remove(thumb_path)
                else:
                    if right:
                        self.right_preview_label.configure(image=None, text="No preview available")
            else:
                if right:
                    self.right_preview_label.configure(image=None, text="No preview available")
        except Exception:
            if right:
                self.right_preview_label.configure(image=None, text="No preview available")

    def update_live_preview(self):
        input_file = self.input_entry.get().strip()
        if not input_file or not os.path.exists(input_file):
            return
        caption_text = self.caption_entry.get().strip()
        font_size = self.font_size_var.get()
        font_color = self.font_color_var.get()
        border_color = self.border_color_var.get()
        border_width = self.border_width_var.get()
        position = self.position_var.get()
        output_format = "png"

        if position == "top":
            y_expr = "20"
        elif position == "center":
            y_expr = "(h-text_h)/2"
        else:
            y_expr = "h-text_h-20"

        drawtext = (
            f"drawtext=text='{caption_text}':"
            f"fontcolor={font_color}:fontsize={font_size}:"
            f"bordercolor={border_color}:borderw={border_width}:"
            f"x=(w-text_w)/2:y={y_expr}"
        )

        preview_file = "preview_temp.png"
        ext = os.path.splitext(input_file)[1].lower()
        try:
            if ext in [".png", ".jpg", ".jpeg", ".gif", ".bmp", ".tiff", ".webp"]:
                ffmpeg_cmd = [
                    "ffmpeg", "-y", "-i", input_file,
                    "-vf", drawtext,
                    "-frames:v", "1",
                    preview_file
                ]
            elif ext in [".mp4", ".avi", ".mov", ".webm", ".mkv"]:
                ffmpeg_cmd = [
                    "ffmpeg", "-y", "-i", input_file,
                    "-vf", f"thumbnail,scale=320:180,{drawtext}",
                    "-frames:v", "1",
                    preview_file
                ]
            else:
                return
            subprocess.run(ffmpeg_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            if os.path.exists(preview_file):
                self._preview_path = preview_file
                if self.preview_shown:
                    self.show_preview(preview_file, right=True)
        except Exception:
            pass

    def get_output_folder(self):
        if os.path.exists(SETTINGS_FILE):
            try:
                with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    return data.get("output_folder", "")
            except Exception:
                return ""
        return ""

    def caption_file(self):
        input_file = self.input_entry.get().strip()
        caption_text = self.caption_entry.get().strip()
        output_name = self.output_entry.get().strip()
        output_format = self.format_var.get()
        font_size = self.font_size_var.get()
        font_color = self.font_color_var.get()
        border_color = self.border_color_var.get()
        border_width = self.border_width_var.get()
        position = self.position_var.get()
        if not input_file or not os.path.exists(input_file):
            messagebox.showwarning("No file", "Please select a valid input file.")
            return
        if not caption_text:
            messagebox.showwarning("No caption", "Please enter a caption.")
            return
        if not output_name:
            messagebox.showwarning("No output name", "Please enter an output file name.")
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

        if position == "top":
            y_expr = "20"
        elif position == "center":
            y_expr = "(h-text_h)/2"
        else: 
            y_expr = "h-text_h-20"

        drawtext = (
            f"drawtext=text='{caption_text}':"
            f"fontcolor={font_color}:fontsize={font_size}:"
            f"bordercolor={border_color}:borderw={border_width}:"
            f"x=(w-text_w)/2:y={y_expr}"
        )

        self.status_label.configure(text="Processing...", text_color="yellow")
        self.update_idletasks()

        try:
            ffmpeg_cmd = [
                "ffmpeg", "-y", "-i", input_file,
                "-vf", drawtext,
                output_file
            ]
            subprocess.run(ffmpeg_cmd, check=True)
            self.status_label.configure(text=f"Done! Saved to: {output_file}", text_color="green")
            messagebox.showinfo("Success", f"Captioned file saved to: {output_file}")

            self._preview_path = output_file
            if self.preview_shown:
                self.show_preview(output_file, right=True)
        except Exception as e:
            self.status_label.configure(text="Captioning failed.", text_color="red")
            messagebox.showerror("Error", str(e))