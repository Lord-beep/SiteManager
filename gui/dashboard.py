import customtkinter as ctk

from core.site_manager import SiteManager


class DashboardFrame(ctk.CTkFrame):

    def __init__(self, parent):
        super().__init__(
            parent,
            fg_color="transparent"
        )

        self.manager = SiteManager()

        self.create_widgets()
        self.load_dashboard()

    # =========================
    # UI
    # =========================

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Dashboard",
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
        # CARDS
        # =========================

        self.cards_frame = ctk.CTkFrame(
            self,
            fg_color="transparent"
        )

        self.cards_frame.pack(
            fill="x",
            pady=(0, 30)
        )

        self.cards_frame.grid_columnconfigure(
            (0, 1, 2),
            weight=1
        )

        self.total_card = self.create_card(
            self.cards_frame,
            "Total de sites",
            "0",
            0
        )

        self.active_card = self.create_card(
            self.cards_frame,
            "Sites ativos",
            "0",
            1
        )

        self.inactive_card = self.create_card(
            self.cards_frame,
            "Sites inativos",
            "0",
            2
        )

        # =========================
        # RECENTES
        # =========================

        recent_title = ctk.CTkLabel(
            self,
            text="Sites configurados",
            font=ctk.CTkFont(
                size=22,
                weight="bold"
            )
        )

        recent_title.pack(
            anchor="w",
            pady=(0, 15)
        )

        self.sites_container = ctk.CTkScrollableFrame(
            self
        )

        self.sites_container.pack(
            fill="both",
            expand=True
        )

    def create_card(
        self,
        parent,
        title,
        value,
        column
    ):

        card = ctk.CTkFrame(
            parent,
            height=120
        )

        card.grid(
            row=0,
            column=column,
            padx=8,
            sticky="nsew"
        )

        card.grid_propagate(False)

        title_label = ctk.CTkLabel(
            card,
            text=title,
            text_color="gray",
            font=ctk.CTkFont(
                size=14
            )
        )

        title_label.pack(
            anchor="w",
            padx=20,
            pady=(20, 5)
        )

        value_label = ctk.CTkLabel(
            card,
            text=value,
            font=ctk.CTkFont(
                size=30,
                weight="bold"
            )
        )

        value_label.pack(
            anchor="w",
            padx=20
        )

        return value_label

    # =========================
    # DATA
    # =========================

    def load_dashboard(self):

        sites = self.manager.list_sites()

        total = len(sites)

        active = sum(
            1 for site in sites
            if site.active
        )

        inactive = total - active

        self.total_card.configure(
            text=str(total)
        )

        self.active_card.configure(
            text=str(active)
        )

        self.inactive_card.configure(
            text=str(inactive)
        )

        self.load_sites(sites)

    # =========================
    # SITES
    # =========================

    def load_sites(self, sites):

        for widget in self.sites_container.winfo_children():
            widget.destroy()

        if not sites:

            label = ctk.CTkLabel(
                self.sites_container,
                text="Ainda não tens nenhum site configurado.",
                text_color="gray",
                font=ctk.CTkFont(
                    size=16
                )
            )

            label.pack(
                pady=80
            )

            return

        for site in sites:

            self.create_site_row(site)

    def create_site_row(self, site):

        row = ctk.CTkFrame(
            self.sites_container
        )

        row.pack(
            fill="x",
            padx=5,
            pady=5
        )

        # Nome

        name = ctk.CTkLabel(
            row,
            text=site.name,
            font=ctk.CTkFont(
                size=17,
                weight="bold"
            )
        )

        name.pack(
            side="left",
            padx=15,
            pady=15
        )

        # Plataforma

        platform = ctk.CTkLabel(
            row,
            text=site.platform,
            text_color="gray"
        )

        platform.pack(
            side="left",
            padx=20
        )

        # Estado

        if site.active:

            status_text = "Ativo"
            status_color = "#22c55e"

        else:

            status_text = "Inativo"
            status_color = "#ef4444"

        status = ctk.CTkLabel(
            row,
            text=status_text,
            text_color=status_color
        )

        status.pack(
            side="right",
            padx=20
        )

        # Última execução

        last_execution = (
            site.last_execution
            if site.last_execution
            else "Nunca"
        )

        execution = ctk.CTkLabel(
            row,
            text=f"Última execução: {last_execution}",
            text_color="gray"
        )

        execution.pack(
            side="right",
            padx=20
        )
