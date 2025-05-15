from passlib.context import CryptContext
from typing import Optional, Any

from app.config.settings import get_settings

settings = get_settings()


def initialize_crypt_context(config: Optional[dict[str, Any]] = None) -> CryptContext:
    """
    Helper para inicializar CryptContext de forma consistente.
    """
    final_settings = config or settings.crypt_context_settings
    try:
        pwd_context = CryptContext(**final_settings)
        return pwd_context
    except Exception as e:
        raise RuntimeError(f"No se pudo inicializar CryptContext: {e}")
