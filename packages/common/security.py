from cryptography.fernet import Fernet

from packages.common.config import get_settings


class SecretCipher:
    def __init__(self) -> None:
        settings = get_settings()
        self._cipher = Fernet(settings.secrets_encryption_key.encode("utf-8"))

    def encrypt(self, plaintext: str) -> str:
        return self._cipher.encrypt(plaintext.encode("utf-8")).decode("utf-8")

    def decrypt(self, ciphertext: str) -> str:
        return self._cipher.decrypt(ciphertext.encode("utf-8")).decode("utf-8")
