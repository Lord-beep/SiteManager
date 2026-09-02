import customtkinter as ctk

from core.site_manager import SiteManager
from core.platforms import get_platform_names


class AddSiteWindow(ctk.CTkToplevel):

    def __init__(self, parent, security, on_saved=None):
        super().__init__(parent)

        self.parent = parent
        self.security = security
        self.on_saved = on_saved
        self.manager = SiteManager()

        self.title("Adicionar site")
        self.geometry("500x750")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    # =========================
    # INTERFACE
    # =========================

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Adicionar site",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(30, 25)
        )

        # =========================
        # NOME
        # =========================

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

        # =========================
        # PLATAFORMA
        # =========================

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

        # =========================
        # USERNAME
        # =========================

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

        # =========================
        # PASSWORD
        # =========================

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

        # =========================
        # API KEY
        # =========================

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

        # =========================
        # DOMÍNIO / PROJECT REF
        # =========================

        ctk.CTkLabel(
            self,
            text="Domínio / Project Ref"
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

        # =========================
        # INTERVALO
        # =========================

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

        self.interval_entry.insert(
            0,
            "60"
        )

        self.interval_entry.pack(
            padx=40,
            pady=(5, 20),
            fill="x"
        )

        # =========================
        # ERRO
        # =========================

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="#ff5555"
        )

        self.error_label.pack(
            pady=(0, 10)
        )

        # =========================
        # GUARDAR
        # =========================

        ctk.CTkButton(
            self,
            text="Guardar site",
            command=self.save_site
        ).pack(
            padx=40,
            pady=5,
            fill="x"
        )

        # =========================
        # CANCELAR
        # =========================

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
    # ALTERAR PLATAFORMA
    # =========================

    def platform_changed(self, platform):
        """
        Altera os campos conforme a plataforma selecionada.
        """

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

            self.domain_entry.delete(
                0,
                "end"
            )

            self.domain_entry.configure(
                state="disabled"
            )

    # =========================
    # MOSTRAR ERRO
    # =========================

    def show_error(self, message):

        self.error_label.configure(
            text=message
        )

    # =========================
    # GUARDAR SITE
    # =========================

    def save_site(self):

        name = self.name_entry.get().strip()
        platform = self.platform_menu.get()
        username = self.username_entry.get().strip()
        password = self.password_entry.get()
        api_key = self.api_key_entry.get()
        domain = self.domain_entry.get().strip()
        interval_text = self.interval_entry.get().strip()

        # =========================
        # VALIDAR NOME
        # =========================

        if not name:

            self.show_error(
                "Introduz o nome do site."
            )

            return

        # =========================
        # VALIDAR INTERVALO
        # =========================

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

        # =========================
        # VALIDAR PYTHONANYWHERE
        # =========================

        if platform == "PythonAnywhere" and not domain:

            self.show_error(
                "Introduz o domínio do PythonAnywhere."
            )

            return

        # =========================
        # VALIDAR SUPABASE
        # =========================

        if platform == "Supabase" and not domain:

            self.show_error(
                "Introduz o Project Ref do Supabase."
            )

            return

        # =========================
        # VALIDAR API KEY SUPABASE
        # =========================

        if platform == "Supabase" and not api_key:

            self.show_error(
                "Introduz o Personal Access Token do Supabase."
            )

            return

        # =========================
        # OBTER ENCRIPTAÇÃO
        # =========================

        try:

            encryption = self.security.encryption

        except RuntimeError:

            self.show_error(
                "A aplicação está bloqueada."
            )

            return

        # =========================
        # GUARDAR
        # =========================

        try:

            site_id = self.manager.add_site(
                name=name,
                platform=platform,
                interval_minutes=interval,
                username=username or None,
                password=password or None,
                api_key=api_key or None,
                domain=domain or None,
                encryption=encryption,
            )

        except Exception as error:

            self.show_error(
                f"Erro ao guardar: {error}"
            )

            return

        # =========================
        # SUCESSO
        # =========================

        print(
            f"Site criado: {site_id}"
        )

        if self.on_saved:
            self.on_saved()

        self.destroy()