from pathlib import Path

from security.encryption import (
    EncryptionManager,
    load_protected_key,
)


class SecuritySession:

    def __init__(
        self,
        password: str,
        key_path: Path
    ):
        self.password = password
        self.key_path = key_path

        self._encryption = None

    def unlock(self) -> bool:

        try:

            key = load_protected_key(
                self.password,
                self.key_path
            )

            self._encryption = EncryptionManager(
                key
            )

            return True

        except Exception:

            self._encryption = None

            return False

    def lock(self):

        self._encryption = None

    @property
    def encryption(self) -> EncryptionManager:

        if self._encryption is None:
            raise RuntimeError(
                "A sessão de segurança está bloqueada."
            )

        return self._encryption
