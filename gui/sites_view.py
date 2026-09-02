import customtkinter as ctk

from gui.add_site import AddSiteWindow
from gui.edit_site import EditSiteWindow

from core.site_manager import SiteManager


class SitesView(ctk.CTkFrame):

    def __init__(self, parent, security):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.security = security
        self.manager = SiteManager()

        self.create_widgets()
        self.load_sites()

    # =========================
    # INTERFACE
    # =========================

    def create_widgets(self):

        header = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        header.pack(
            fill="x",
            pady=(0, 30)
        )

        title = ctk.CTkLabel(
            header,
            text="Os meus sites",
            font=ctk.CTkFont(
                size=32,
                weight="bold"
            )
        )

        title.pack(
            side="left"
        )

        add_button = ctk.CTkButton(
            header,
            text="+ Adicionar site",
            command=self.open_add_site
        )

        add_button.pack(
            side="right"
        )

        self.sites_container = ctk.CTkScrollableFrame(
            self
        )

        self.sites_container.pack(
            fill="both",
            expand=True
        )

    # =========================
    # CARREGAR SITES
    # =========================

    def load_sites(self):

        if not self.winfo_exists():
            return

        for widget in self.sites_container.winfo_children():
            widget.destroy()

        sites = self.manager.list_sites()

        if not sites:

            empty_label = ctk.CTkLabel(
                self.sites_container,
                text="Ainda não tens nenhum site configurado.",
                font=ctk.CTkFont(size=16),
                text_color="gray"
            )

            empty_label.pack(
                pady=100
            )

            return

        for site in sites:
            self.create_site_card(site)

    # =========================
    # RECARREGAR COM SEGURANÇA
    # =========================

    def refresh_sites(self):

        """
        Recarrega os cartões depois de o evento
        do botão terminar.

        Isto evita o erro:
        TclError: bad window path name
        """

        self.after(
            100,
            self.load_sites
        )

    # =========================
    # CARTÃO DO SITE
    # =========================

    def create_site_card(self, site):

        card = ctk.CTkFrame(
            self.sites_container
        )

        card.pack(
            fill="x",
            padx=10,
            pady=8
        )

        name_label = ctk.CTkLabel(
            card,
            text=site.name,
            font=ctk.CTkFont(
                size=18,
                weight="bold"
            )
        )

        name_label.pack(
            anchor="w",
            padx=20,
            pady=(15, 3)
        )

        platform_label = ctk.CTkLabel(
            card,
            text=f"Plataforma: {site.platform}",
            text_color="gray"
        )

        platform_label.pack(
            anchor="w",
            padx=20
        )

        if getattr(site, "domain", None):

            domain_label = ctk.CTkLabel(
                card,
                text=f"Domínio: {site.domain}",
                text_color="gray"
            )

            domain_label.pack(
                anchor="w",
                padx=20
            )

        interval_label = ctk.CTkLabel(
            card,
            text=f"Intervalo: {site.interval_minutes} minutos",
            text_color="gray"
        )

        interval_label.pack(
            anchor="w",
            padx=20
        )

        if site.last_execution:

            last_execution_text = (
                f"Última execução: {site.last_execution}"
            )

        else:

            last_execution_text = (
                "Última execução: nunca"
            )

        last_execution_label = ctk.CTkLabel(
            card,
            text=last_execution_text,
            text_color="gray"
        )

        last_execution_label.pack(
            anchor="w",
            padx=20
        )

        status = (
            "🟢 Ativo"
            if site.active
            else "🔴 Inativo"
        )

        status_label = ctk.CTkLabel(
            card,
            text=status
        )

        status_label.pack(
            anchor="w",
            padx=20,
            pady=(3, 10)
        )

        buttons = ctk.CTkFrame(
            card,
            fg_color="transparent"
        )

        buttons.pack(
            anchor="e",
            padx=20,
            pady=(0, 15)
        )

        toggle_text = (
            "Desativar"
            if site.active
            else "Ativar"
        )

        ctk.CTkButton(
            buttons,
            text=toggle_text,
            width=100,
            command=lambda: self.toggle_site(
                site.id,
                site.active
            )
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Editar",
            width=100,
            command=lambda: self.edit_site(
                site.id
            )
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Executar",
            width=100,
            command=lambda: self.execute_site(
                site.id
            )
        ).pack(
            side="left",
            padx=5
        )

        ctk.CTkButton(
            buttons,
            text="Apagar",
            width=100,
            fg_color="#b91c1c",
            hover_color="#991b1b",
            command=lambda: self.delete_site(
                site.id
            )
        ).pack(
            side="left",
            padx=5
        )

    # =========================
    # ADICIONAR SITE
    # =========================

    def open_add_site(self):

        AddSiteWindow(
            self,
            self.security,
            on_saved=self.refresh_sites
        )

    # =========================
    # ATIVAR / DESATIVAR
    # =========================

    def toggle_site(
        self,
        site_id,
        current_state
    ):

        try:

            self.manager.set_active(
                site_id,
                not current_state
            )

            self.refresh_sites()

        except Exception as error:

            self.show_error(
                str(error)
            )
            
    # =========================
    # EDITAR SITE
    # =========================

    def edit_site(self, site_id):

        site = self.manager.get_site(site_id)

        if site is None:
            self.show_error(
                "Site não encontrado."
            )
            return

        EditSiteWindow(
            self,
            self.security,
            site_id,
            on_saved=self.refresh_sites
        )


    # =========================
    # EXECUTAR SITE
    # =========================

    def execute_site(self, site_id):

        if not self.security.is_unlocked():

            self.show_error(
                "A aplicação está bloqueada."
            )

            return

        try:

            result = self.manager.execute_site(
                site_id,
                self.security.encryption
            )

            self.show_success(
                result["message"],
                result["execution_time"]
            )

            self.refresh_sites()

        except Exception as error:

            self.show_error(
                str(error)
            )

    # =========================
    # RESULTADO COM SUCESSO
    # =========================

    def show_success(
        self,
        message,
        execution_time
    ):

        window = ctk.CTkToplevel(self)

        window.title("Execução concluída")
        window.geometry("500x280")
        window.resizable(False, False)

        window.transient(self)
        window.grab_set()

        ctk.CTkLabel(
            window,
            text="🟢 Execução concluída",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color="#22c55e"
        ).pack(
            pady=(35, 20)
        )

        ctk.CTkLabel(
            window,
            text=message,
            font=ctk.CTkFont(size=15),
            wraplength=420,
            justify="center"
        ).pack(
            padx=30,
            pady=10
        )

        ctk.CTkLabel(
            window,
            text=f"Execução: {execution_time}",
            text_color="gray"
        ).pack(
            pady=10
        )

        ctk.CTkButton(
            window,
            text="Fechar",
            command=window.destroy
        ).pack(
            pady=15
        )

    # =========================
    # ERRO
    # =========================

    def show_error(self, message):

        window = ctk.CTkToplevel(self)

        window.title("Erro")
        window.geometry("500x250")
        window.resizable(False, False)

        window.transient(self)
        window.grab_set()

        ctk.CTkLabel(
            window,
            text="🔴 Erro",
            font=ctk.CTkFont(
                size=24,
                weight="bold"
            ),
            text_color="#ef4444"
        ).pack(
            pady=(35, 20)
        )

        ctk.CTkLabel(
            window,
            text=message,
            font=ctk.CTkFont(size=15),
            wraplength=420,
            justify="center"
        ).pack(
            padx=30,
            pady=10
        )

        ctk.CTkButton(
            window,
            text="Fechar",
            command=window.destroy
        ).pack(
            pady=15
        )

    # =========================
    # APAGAR SITE
    # =========================

    def delete_site(self, site_id):

        try:

            self.manager.delete_site(
                site_id
            )

            self.refresh_sites()

        except Exception as error:

            self.show_error(
                str(error)
            )