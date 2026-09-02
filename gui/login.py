import customtkinter as ctk


class LoginWindow(ctk.CTkToplevel):

    def __init__(self, parent, security, on_success=None):
        super().__init__(parent)

        self.parent = parent
        self.security = security
        self.on_success = on_success

        self.title("Desbloquear Site Manager")
        self.geometry("500x400")
        self.resizable(False, False)

        self.transient(parent)
        self.grab_set()

        self.protocol(
            "WM_DELETE_WINDOW",
            self.close_application
        )

        self.create_widgets()

    def create_widgets(self):

        title = ctk.CTkLabel(
            self,
            text="SITE MANAGER",
            font=ctk.CTkFont(
                size=28,
                weight="bold"
            )
        )

        title.pack(
            pady=(50, 10)
        )

        description = ctk.CTkLabel(
            self,
            text="Introduz a tua palavra-passe mestre",
            text_color="gray"
        )

        description.pack(
            pady=(0, 30)
        )

        self.password_entry = ctk.CTkEntry(
            self,
            placeholder_text="Palavra-passe mestre",
            show="•"
        )

        self.password_entry.pack(
            fill="x",
            padx=60,
            pady=10
        )

        self.password_entry.bind(
            "<Return>",
            lambda event: self.login()
        )

        self.error_label = ctk.CTkLabel(
            self,
            text="",
            text_color="#ff5555"
        )

        self.error_label.pack(
            pady=5
        )

        self.login_button = ctk.CTkButton(
            self,
            text="Entrar",
            command=self.login
        )

        self.login_button.pack(
            fill="x",
            padx=60,
            pady=15
        )

    def login(self):

        password = self.password_entry.get()

        if not password:

            self.show_error(
                "Introduz a palavra-passe."
            )

            return

        self.login_button.configure(
            state="disabled",
            text="A desbloquear..."
        )

        self.update_idletasks()

        success = self.security.unlock(
            password
        )

        if success:

            if self.on_success:
                self.on_success()

            self.destroy()

        else:

            self.login_button.configure(
                state="normal",
                text="Entrar"
            )

            self.password_entry.delete(
                0,
                "end"
            )

            self.show_error(
                "Palavra-passe incorreta."
            )

            self.password_entry.focus()

    def show_error(self, message):

        self.error_label.configure(
            text=message
        )

    def close_application(self):

        self.parent.destroy()
