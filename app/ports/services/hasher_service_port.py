from pydantic import BaseModel
from app.ports.command import Command
from abc import ABC, abstractmethod


class HashDataSchema(BaseModel):
    """
    Define los parámetros para la operación de hashing.
    """

    data_to_hash: str


class VerifyDataSchema(BaseModel):
    """
    Define los parámetros para la operación de verificación de hash.
    """

    plain_data: str
    hashed_data: str


class VerifyResultSchema(BaseModel):
    """
    Define el resultado de la verificación.
    """

    is_valid: bool
    needs_update: bool


class HasherServicePort(Command[HashDataSchema, str], ABC):
    """
    Puerto (Interfaz) para un servicio de hashing.
    Define el contrato para hashear datos y verificar hashes.
    """

    @abstractmethod
    def execute(self) -> str:
        """
        Hashea los datos proporcionados y retorna la cadena hasheada.
        """
        pass


class VerifyDataServicePort(Command[VerifyDataSchema, VerifyResultSchema], ABC):
    """
    Puerto (Interfaz) para un servicio de verificación de datos.
    Define el contrato para verificar hashes.
    """

    @abstractmethod
    def execute(self) -> VerifyResultSchema:
        """
        Verifica si los datos en texto plano coinciden con el hash almacenado.
        Retorna un objeto VerifyResultSchema con el resultado de la verificación.
        """
        pass
