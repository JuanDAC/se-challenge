from contextlib import contextmanager
from typing import Iterable

from injector import Module, inject, singleton
from app.config.environment import get_environment_variables
from app.ports.transactional.transaction_manager import (
    TransactionManagerPort,
)


from injector import inject
from sqlalchemy import create_engine, MetaData, Engine
from sqlalchemy.orm import Session, sessionmaker

env = get_environment_variables()

DATABASE = f"{env.DB_DIALECT}://{env.DB_USER}:{env.DB_PASSWORD}"
DATABASE_SELECTOR = f"{env.DB_HOST}:{env.DB_PORT}/{env.DB_NAME}"

DATABASE_URL = f"{DATABASE}@{DATABASE_SELECTOR}"

def get_engine() -> Engine:
    engine = create_engine(
        DATABASE_URL,
        echo=env.DEBUG,
        future=True,
        pool_size=10,
        max_overflow=20,
        pool_recycle=3600,
        pool_timeout=30,
    )


    engine = create_engine(DATABASE_URL)
    metadata = MetaData(schema=env.DB_SCHEMA)
    metadata.reflect(bind=engine)
    return engine


@inject
def get_session(engine: Engine) -> sessionmaker[Session]:
    session = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )
    return session


class TransactionManager(TransactionManagerPort[Session]):
    @inject
    def __init__(self, session_local: sessionmaker[Session]):
        self.session_local = session_local

    @contextmanager
    def get_transaction_context(self) -> Iterable[Session]:
        session = self.session_local()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()



class ConfigModule(Module):
    def configure(self, binder):
        binder.bind(Engine, to=get_engine, scope=singleton)
        binder.bind(sessionmaker[Session], to=get_session, scope=singleton)
        binder.bind(TransactionManagerPort, to=TransactionManager, scope=singleton)

