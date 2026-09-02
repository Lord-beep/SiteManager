import customtkinter as ctk

from gui.dashboard import DashboardFrame
from gui.sites_view import SitesView


class SiteManagerApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Site Manager")
        self.geometry("1100x700")
        self.minsize(900, 600)

        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        self.create_sidebar()
        self.create_content_area()

        self.show_dashboard()

    # =========================
    # SIDEBAR
    # =========================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=220,
            corner_radius=0
        )

        self.sidebar.pack(
            side="left",
            fill="y"
        )

        self.sidebar.pack_propagate(False)

        title = ctk.CTkLabel(
            self.sidebar,
            text="SITE MANAGER",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        title.pack(
            padx=20,
            pady=(30, 40)
        )

        self.dashboard_button = ctk.CTkButton(
            self.sidebar,
            text="🏠  Dashboard",
            command=self.show_dashboard
        )

        self.dashboard_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.sites_button = ctk.CTkButton(
            self.sidebar,
            text="🌐  Sites",
            command=self.show_sites
        )

        self.sites_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="⚙  Definições",
            command=self.show_settings
        )

        self.settings_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

    # =========================
    # CONTENT
    # =========================

    def create_content_area(self):

        self.content_area = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color="transparent"
        )

        self.content_area.pack(
            side="right",
            fill="both",
            expand=True,
            padx=30,
            pady=30
        )

    # =========================
    # PAGE MANAGEMENT
    # =========================

    def clear_content(self):

        for widget in self.content_area.winfo_children():
            widget.destroy()

    def show_dashboard(self):

        self.clear_content()

        dashboard = DashboardFrame(
            self.content_area
        )

        dashboard.pack(
            fill="both",
            expand=True
        )

    def show_sites(self):

        self.clear_content()

        sites = SitesView(
            self.content_area
        )

        sites.pack(
            fill="both",
            expand=True
        )

    def show_settings(self):

        self.clear_content()

        label = ctk.CTkLabel(
            self.content_area,
            text="Definições",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        label.pack(
            anchor="w"
        )


if __name__ == "__main__":

    app = SiteManagerApp()

    app.mainloop()
