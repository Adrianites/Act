import customtkinter as ctk
import json
import os

SETTINGS_FILE = "settings.json"
DEFAULT_THEME = "system"

def get_theme():
    if os.path.exists(SETTINGS_FILE):
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                return data.get("theme", DEFAULT_THEME)
        except Exception:
            return DEFAULT_THEME
    return DEFAULT_THEME

ctk.set_appearance_mode(get_theme())

from tabs.convert import ConvertTab
from tabs.compress import CompressTab
from tabs.caption import CaptionTab

from tabs.settings import SettingsTab
from tabs.about import AboutTab
from tabs.ytd import YTDTab

class ErrorLogWindow(ctk.CTkToplevel):
    def __init__(self, master, log_list, on_close=None):
        super().__init__(master)
        self.title("Error Log")
        self.geometry("600x300")
        self.resizable(True, True)
        self.text = ctk.CTkTextbox(self, width=580, height=260)
        self.text.pack(padx=10, pady=10, fill="both", expand=True)
        self.on_close = on_close
        self.protocol("WM_DELETE_WINDOW", self._on_close)
        self.update_logs(log_list)

    def update_logs(self, log_list):
        self.text.configure(state="normal")
        self.text.delete("1.0", "end")
        self.text.insert("end", "\n".join(log_list))
        self.text.configure(state="disabled")
        self.text.see("end")

    def _on_close(self):
        if self.on_close:
            self.on_close()
        self.destroy()


class act(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ACT")
        self.geometry("560x420")
        self.resizable(False, False)

        self.error_log = []
        self.error_log_window = None

        self.tabview = ctk.CTkTabview(self, width=540, height=390)
        self.tabview.pack(padx=10, pady=10, fill="both", expand=True)

        self.tabview.add("Convert")
        self.convert_tab = ConvertTab(self.tabview.tab("Convert"))
        self.convert_tab.pack(fill="both", expand=True)

        self.tabview.add("Compress")
        self.compress_tab = CompressTab(self.tabview.tab("Compress"))
        self.compress_tab.pack(fill="both", expand=True)

        self.tabview.add("Caption")
        self.caption_tab = CaptionTab(self.tabview.tab("Caption"), self)
        self.caption_tab.pack(fill="both", expand=True)

        self.tabview.add("YTD")
        self.ytd_tab = YTDTab(self.tabview.tab("YTD"))
        self.ytd_tab.pack(fill="both", expand=True)

        self.tabview.add("Settings")
        self.settings_tab = SettingsTab(self.tabview.tab("Settings"), self)
        self.settings_tab.pack(fill="both", expand=True)

        self.tabview.add("About")
        self.about_tab = AboutTab(self.tabview.tab("About"))
        self.about_tab.pack(fill="both", expand=True)

        self._last_tab = self.tabview.get()
        self.after(200, self._check_tab_change)


    def log_error(self, msg):
        self.error_log.append(msg)
        if len(self.error_log) > 500:
            self.error_log = self.error_log[-500:]
        if self.error_log_window is not None:
            try:
                if self.error_log_window.winfo_exists():
                    self.error_log_window.update_logs(self.error_log)
                else:
                    self.error_log_window = None
            except Exception:
                self.error_log_window = None

    def show_error_log(self):
        if self.error_log_window is not None:
            try:
                if self.error_log_window.winfo_exists():
                    self.error_log_window.lift()
                    self.error_log_window.focus_force()
                    return
                else:
                    self.error_log_window = None
            except Exception:
                self.error_log_window = None
        self.error_log_window = ErrorLogWindow(self, self.error_log, on_close=self._on_log_window_close)

    def _on_log_window_close(self):
        self.error_log_window = None

    def _check_tab_change(self):
        current_tab = self.tabview.get()
        if current_tab != self._last_tab:
            if self._last_tab == "Caption":
                self.caption_tab.close_preview()
            self._last_tab = current_tab
        self.after(200, self._check_tab_change)

if __name__ == "__main__":
    app = act()
    app.mainloop()