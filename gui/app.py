import customtkinter as ctk

from paths import (
    MASTER_PASSWORD_PATH,
    ENCRYPTION_KEY_PATH,
)

from security.security_manager import SecurityManager

from gui.login import LoginWindow
from gui.setup_password import SetupPasswordWindow
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

        self.security = SecurityManager(
            MASTER_PASSWORD_PATH,
            ENCRYPTION_KEY_PATH
        )

        self.create_sidebar()
        self.create_content_area()

        self.start_security()

    # =========================
    # SECURITY
    # =========================

    def start_security(self):

        if not self.security.has_master_password():
            self.show_setup_password()
        else:
            self.show_login()

    def show_setup_password(self):

        SetupPasswordWindow(
            self,
            on_success=self.security_setup_success
        )

    def security_setup_success(self, password):

        if self.security.unlock(password):
            self.show_dashboard()
        else:
            self.destroy()

    def show_login(self):

        LoginWindow(
            self,
            self.security,
            on_success=self.login_success
        )

    def login_success(self):

        self.show_dashboard()

    def lock_application(self):

        self.security.lock()

        self.clear_content()

        self.show_login()

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
            text="Dashboard",
            command=self.show_dashboard
        )

        self.dashboard_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.sites_button = ctk.CTkButton(
            self.sidebar,
            text="Sites",
            command=self.show_sites
        )

        self.sites_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.settings_button = ctk.CTkButton(
            self.sidebar,
            text="Definições",
            command=self.show_settings
        )

        self.settings_button.pack(
            padx=20,
            pady=10,
            fill="x"
        )

        self.lock_button = ctk.CTkButton(
            self.sidebar,
            text="Bloquear",
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=self.lock_application
        )

        self.lock_button.pack(
            side="bottom",
            padx=20,
            pady=30,
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

        if not self.security._session:
            return

        self.clear_content()

        dashboard = DashboardFrame(
            self.content_area
        )

        dashboard.pack(
            fill="both",
            expand=True
        )

    def show_sites(self):

            for widget in self.content_area.winfo_children():
                widget.destroy()

            sites = SitesView(
                self.content_area,
                self.security
            )

            sites.pack(
                fill="both",
                expand=True
            )


    def show_settings(self):

        if not self.security._session:
            return

        self.clear_content()

        title = ctk.CTkLabel(
            self.content_area,
            text="Definições",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        title.pack(
            anchor="w",
            pady=(0, 30)
        )

        # =========================
        # APARÊNCIA
        # =========================

        appearance_frame = ctk.CTkFrame(
            self.content_area
        )

        appearance_frame.pack(
            fill="x",
            pady=10
        )

        appearance_title = ctk.CTkLabel(
            appearance_frame,
            text="Aparência",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        appearance_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        appearance_description = ctk.CTkLabel(
            appearance_frame,
            text="Escolhe o tema da aplicação.",
            text_color="gray"
        )

        appearance_description.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        self.theme_menu = ctk.CTkOptionMenu(
            appearance_frame,
            values=[
                "Escuro",
                "Claro",
                "Sistema"
            ],
            command=self.change_theme
        )

        self.theme_menu.set("Escuro")

        self.theme_menu.pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

        # =========================
        # SEGURANÇA
        # =========================

        security_frame = ctk.CTkFrame(
            self.content_area
        )

        security_frame.pack(
            fill="x",
            pady=10
        )

        security_title = ctk.CTkLabel(
            security_frame,
            text="Segurança",
            font=ctk.CTkFont(
                size=20,
                weight="bold"
            )
        )

        security_title.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        security_description = ctk.CTkLabel(
            security_frame,
            text="Protege os dados guardados no Site Manager.",
            text_color="gray"
        )

        security_description.pack(
            anchor="w",
            padx=20,
            pady=(0, 15)
        )

        ctk.CTkButton(
            security_frame,
            text="Bloquear aplicação",
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=self.lock_application
        ).pack(
            anchor="w",
            padx=20,
            pady=(0, 20)
        )

    # =========================
    # THEME
    # =========================

    def change_theme(self, choice):

        if choice == "Escuro":
            ctk.set_appearance_mode("dark")

        elif choice == "Claro":
            ctk.set_appearance_mode("light")

        else:
            ctk.set_appearance_mode("system")


if __name__ == "__main__":

    app = SiteManagerApp()

    app.mainloop()
