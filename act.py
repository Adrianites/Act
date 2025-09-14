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

class act(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ACT")
        self.geometry("560x420")
        self.resizable(False, False)

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