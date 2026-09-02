from pathlib import Path
import os

from security.encryption import (
    EncryptionManager,
    create_protected_key,
    load_protected_key,
)

from security.master_password import (
    MasterPasswordManager,
)


class SecurityManager:

    def __init__(
        self,
        password_file: Path,
        encryption_key_file: Path,
    ):
        self.master_password = MasterPasswordManager(
            password_file
        )

        self.encryption_key_file = encryption_key_file

        self._session = None

    # =========================
    # PASSWORD MESTRE
    # =========================

    def has_master_password(self) -> bool:
        return self.master_password.has_password()

    def setup(self, password: str) -> None:

        self.master_password.setup_password(
            password
        )

        create_protected_key(
            password,
            self.encryption_key_file
        )

    # =========================
    # LOGIN / DESBLOQUEAR
    # =========================

    def unlock(self, password: str) -> bool:

        if not self.master_password.verify_password(
            password
        ):
            return False

        try:

            key = load_protected_key(
                password,
                self.encryption_key_file
            )

            self._session = EncryptionManager(
                key
            )

            return True

        except Exception:

            self._session = None

            return False

    # =========================
    # BLOQUEAR
    # =========================

    def lock(self) -> None:

        self._session = None

    # =========================
    # VERIFICAR ESTADO
    # =========================

    def is_unlocked(self) -> bool:

        return self._session is not None

    # =========================
    # ENCRIPTAÇÃO
    # =========================

    @property
    def encryption(self) -> EncryptionManager:

        if self._session is None:

            raise RuntimeError(
                "A aplicação está bloqueada."
            )

        return self._session
