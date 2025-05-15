from app.infrastructure.security.crypt_constext import initialize_crypt_context
from app.ports.services.hasher_service_port import (
    VerifyDataServicePort,
    VerifyResultSchema,
)


class PasslibDataVerifier(VerifyDataServicePort):
    """
    Implementación concreta de VerifyDataServicePort que utiliza Passlib para
    verificar datos contra un hash. Sigue el patrón Command.
    """

    def __init__(self):
        """
        Constructor para PasslibDataVerifier.
        """
        super().__init__()
        self.pwd_context = initialize_crypt_context()

    def execute(self) -> VerifyResultSchema:
        """
        Verifica los datos en texto plano contra un hash existente.
        Los datos se esperan en `self.params.plain_data` y `self.params.hashed_data`.
        """
        if not hasattr(self, "params") or not self.params:
            raise ValueError(
                "Parámetros no establecidos para PasslibDataVerifier. Llama a set_params con VerifyDataSchema primero."
            )
        if not self.params.plain_data or not self.params.hashed_data:
            raise ValueError(
                "Tanto plain_data como hashed_data deben ser proporcionados para la verificación."
            )

        try:
            is_valid = self.pwd_context.verify(
                self.params.plain_data, self.params.hashed_data
            )
            if is_valid and self.pwd_context.needs_update(self.params.hashed_data):
                return VerifyResultSchema(is_valid=True, needs_update=True)
            return VerifyResultSchema(is_valid=is_valid, needs_update=False)
        except Exception as e:
            return VerifyResultSchema(is_valid=False, needs_update=False)
