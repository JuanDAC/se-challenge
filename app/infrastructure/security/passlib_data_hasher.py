from app.ports.services.hasher_service_port import HasherServicePort
from app.config.settings import get_settings
from app.infrastructure.security.crypt_constext import initialize_crypt_context


settings = get_settings()


class PasslibDataHasher(HasherServicePort):
    """
    Implementación concreta de HasherServicePort que utiliza Passlib (bcrypt por defecto)
    para hashear datos. Sigue el patrón Command.
    """

    def __init__(self):
        """
        Constructor para PasslibDataHasher.
        """
        super().__init__()
        self.pwd_context = initialize_crypt_context()

    def execute(self) -> str:
        """
        Hashea los datos usando el esquema por defecto configurado en CryptContext (bcrypt).
        Los datos a hashear se esperan en `self.params.data_to_hash`.
        """
        if not hasattr(self, "params") or not self.params:
            raise ValueError(
                "Parámetros no establecidos para PasslibDataHasher. Llama a set_params con HashDataSchema primero."
            )
        if not self.params.data_to_hash:
            raise ValueError(
                "No se proporcionaron datos para hashear (data_to_hash no puede estar vacío)."
            )

        try:
            hashed_value = self.pwd_context.hash(self.params.data_to_hash)
            return hashed_value
        except Exception as e:
            raise RuntimeError(
                "Ocurrió un error interno durante el proceso de hashing."
            )
