import customtkinter as ctk

from security.security_manager import SecurityManager
from paths import (
    MASTER_PASSWORD_PATH,
    ENCRYPTION_KEY_PATH,
)


class SetupPasswordWindow(ctk.CTkToplevel):

    def __init__(self, parent, on_success=None):
        super().__init__(parent)

        self.parent = parent
        self.on_success = on_success

        self.security = SecurityManager(
            MASTER_PASSWORD_PATH,
            ENCRYPTION_KEY_PATH
        )

        self.title("Configuração inicial")
        self.geometry("500x450")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="Configuração inicial",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(40, 10)
        )

        description = ctk.CTkLabel(
            self,
            text=(
                "Cria uma palavra-passe mestre para proteger\n"
                "as credenciais dos teus sites."
            ),
            justify="center",
            text_color="gray"
        )

        description.pack(
            pady=(0, 30)
        )

        ctk.CTkLabel(
            self,
            text="Palavra-passe mestre"
        ).pack(
            anchor="w",
            padx=50
        )

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Mínimo 8 caracteres",
            show="•"
        )

        self.password_entry.pack(
            fill="x",
            padx=50,
            pady=(5, 15)
        )

        ctk.CTkLabel(
            self,
            text="Confirmar palavra-passe"
        ).pack(
            anchor="w",
            padx=50
        )

        self.confirm_entry = ctk.CTkEntry(
            self,
            placeholder_text="Repete a palavra-passe",
            show="•"
        )

        self.confirm_entry.pack(
            fill="x",
            padx=50,
            pady=(5, 15)
        )

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="#ff5555"
        )

        self.error_label.pack(
            pady=5
        )

        self.create_button = ctk.CTkButton(
            self,
            text="Criar password mestre",
            command=self.setup_password
        )

        self.create_button.pack(
            fill="x",
            padx=50,
            pady=10
        )

    def setup_password(self):

        password = self.password_entry.get()
        confirmation = self.confirm_entry.get()

        if len(password) < 8:

            self.show_error(
                "A password deve ter pelo menos 8 caracteres."
            )

            return

        if password != confirmation:

            self.show_error(
                "As passwords não coincidem."
            )

            return

        try:

            self.security.setup(
                password
            )

        except Exception as error:

            self.show_error(
                f"Erro: {error}"
            )

            return

        if self.on_success:
            self.on_success(password)

        self.destroy()

    def show_error(self, message):

        self.error_label.configure(
            text=message
        )
