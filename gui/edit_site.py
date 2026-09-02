import customtkinter as ctk

from core.site_manager import SiteManager
from core.platforms import get_platform_names


class EditSiteWindow(ctk.CTkToplevel):

    def __init__(self, parent, security, site_id, on_saved=None):
        super().__init__(parent)

        self.parent = parent
        self.security = security
        self.site_id = site_id
        self.on_saved = on_saved
        self.manager = SiteManager()

        self.title("Editar site")
        self.geometry("500x750")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.create_widgets()
        self.load_site()

    # =========================
    # INTERFACE
    # =========================

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Editar site",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(30, 25)
        )

        # Nome

        ctk.CTkLabel(
            self,
            text="Nome do site"
        ).pack(
            anchor="w",
            padx=40
        )

        self.name_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ex: Meu site"
        )

        self.name_entry.pack(
            padx=40,
            pady=(5, 15),
            fill="x"
        )

        # Plataforma

        ctk.CTkLabel(
            self,
            text="Plataforma"
        ).pack(
            anchor="w",
            padx=40
        )

        self.platform_menu = ctk.CTkOptionMenu(
            self,
            values=get_platform_names(),
            command=self.platform_changed
        )

        self.platform_menu.pack(
            padx=40,
            pady=(5, 15),
            fill="x"
        )

        # Username

        ctk.CTkLabel(
            self,
            text="Username"
        ).pack(
            anchor="w",
            padx=40
        )

        self.username_entry = ctk.CTkEntry(
            self,
            placeholder_text="Username"
        )

        self.username_entry.pack(
            padx=40,
            pady=(5, 15),
            fill="x"
        )

        # Password

        ctk.CTkLabel(
            self,
            text="Password"
        ).pack(
            anchor="w",
            padx=40
        )

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Password",
            show="*"
        )

        self.password_entry.pack(
            padx=40,
            pady=(5, 15),
            fill="x"
        )

        # API Key

        ctk.CTkLabel(
            self,
            text="API Key / Token"
        ).pack(
            anchor="w",
            padx=40
        )

        self.api_key_entry = ctk.CTkEntry(
            self,
            placeholder_text="API Key / Token",
            show="*"
        )

        self.api_key_entry.pack(
            padx=40,
            pady=(5, 15),
            fill="x"
        )

        # Domínio

        ctk.CTkLabel(
            self,
            text="Domínio"
        ).pack(
            anchor="w",
            padx=40
        )

        self.domain_entry = ctk.CTkEntry(
            self,
            placeholder_text="Ex: xmavsx.pythonanywhere.com"
        )

        self.domain_entry.pack(
            padx=40,
            pady=(5, 15),
            fill="x"
        )

        # Intervalo

        ctk.CTkLabel(
            self,
            text="Intervalo (minutos)"
        ).pack(
            anchor="w",
            padx=40
        )

        self.interval_entry = ctk.CTkEntry(
            self,
            placeholder_text="60"
        )

        self.interval_entry.pack(
            padx=40,
            pady=(5, 20),
            fill="x"
        )

        # Erro

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="#ff5555"
        )

        self.error_label.pack(
            pady=(0, 10)
        )

        # Guardar

        ctk.CTkButton(
            self,
            text="Guardar alterações",
            command=self.save_changes
        ).pack(
            padx=40,
            pady=5,
            fill="x"
        )

        # Cancelar

        ctk.CTkButton(
            self,
            text="Cancelar",
            fg_color="transparent",
            border_width=1,
            command=self.destroy
        ).pack(
            padx=40,
            pady=5,
            fill="x"
        )

    # =========================
    # CARREGAR SITE
    # =========================

    def load_site(self):

        site = self.manager.get_site(
            self.site_id
        )

        if site is None:

            self.show_error(
                "Site não encontrado."
            )

            return

        self.name_entry.insert(
            0,
            site.name
        )

        self.platform_menu.set(
            site.platform
        )

        self.platform_changed(
            site.platform
        )

        self.domain_entry.delete(
            0,
            "end"
        )

        if site.domain:
            self.domain_entry.insert(
                0,
                site.domain
            )

        self.interval_entry.insert(
            0,
            str(site.interval_minutes)
        )

        try:

            credentials = self.manager.get_site_credentials(
                self.site_id,
                self.security.encryption
            )

            if credentials.get("username"):
                self.username_entry.insert(
                    0,
                    credentials["username"]
                )

            if credentials.get("password"):
                self.password_entry.insert(
                    0,
                    credentials["password"]
                )

            if credentials.get("api_key"):
                self.api_key_entry.insert(
                    0,
                    credentials["api_key"]
                )

        except Exception as error:

            self.show_error(
                f"Erro ao carregar credenciais: {error}"
            )

    # =========================
    # ALTERAR PLATAFORMA
    # =========================

    def platform_changed(self, platform):

        if platform == "PythonAnywhere":

            self.domain_entry.configure(
                state="normal",
                placeholder_text="Ex: xmavsx.pythonanywhere.com"
            )

        elif platform == "Supabase":

            self.domain_entry.configure(
                state="normal",
                placeholder_text="Ex: lrccdnvqjwfosmrwqjoh"
            )

        else:

            self.domain_entry.configure(
                state="normal"
            )

    # =========================
    # GUARDAR
    # =========================

    def save_changes(self):

        name = self.name_entry.get().strip()
        platform = self.platform_menu.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        api_key = self.api_key_entry.get()
        domain = self.domain_entry.get().strip()
        interval_text = self.interval_entry.get().strip()

        if not name:

            self.show_error(
                "Introduz o nome do site."
            )

            return

        try:

            interval = int(
                interval_text
            )

            if interval <= 0:
                raise ValueError

        except ValueError:

            self.show_error(
                "O intervalo deve ser um número maior que zero."
            )

            return

        if platform == "PythonAnywhere" and not domain:

            self.show_error(
                "Introduz o domínio do PythonAnywhere."
            )

            return

        try:

            encryption = self.security.encryption

        except RuntimeError:

            self.show_error(
                "A aplicação está bloqueada."
            )

            return

        try:

            self.manager.update_site(
                site_id=self.site_id,
                name=name,
                platform=platform,
                interval_minutes=interval,
                username=username or None,
                password=password or None,
                api_key=api_key or None,
                domain=domain or None,
                encryption=encryption
            )

        except Exception as error:

            self.show_error(
                f"Erro ao guardar: {error}"
            )

            return

        if self.on_saved:
            self.on_saved()

        self.destroy()

    # =========================
    # ERRO
    # =========================

    def show_error(self, message):

        self.error_label.configure(
            text=message
        )