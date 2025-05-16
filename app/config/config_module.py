from contextlib import contextmanager
from typing import Iterable
from sqlalchemy.engine.url import URL
from injector import Module, inject, singleton
from app.config.environment import get_environment_variables
from app.ports.transactional.transaction_manager import (
    TransactionManagerPort,
)
from sqlalchemy_utils import database_exists, create_database


from injector import inject
from sqlalchemy import create_engine, MetaData, Engine
from sqlalchemy.orm import Session, sessionmaker

from sqlalchemy.ext.declarative import declarative_base
env = get_environment_variables()


DATABASE = {
    'drivername': env.DB_DIALECT,
    'username': env.DB_USER,
    'password': env.DB_PASSWORD,
    'host': env.DB_HOST,
    'port': env.DB_PORT,
    'database': env.DB_DATABASE_NAME
}
DATABASE_URL = URL.create(**DATABASE)

print(f"Connecting to database: {DATABASE_URL}")

if not database_exists(DATABASE_URL):
    create_database(DATABASE_URL)
    print("Database created!")
else:
    print("Database already exists.")

Base = declarative_base()


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
    Base.metadata.create_all(bind=engine)



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
    def __init__(self, *arg, exclude_classes=None, **kwargs):
        super().__init__(*arg, **kwargs)
        self.exclude_classes = exclude_classes or []

    def configure(self, binder):
        super().configure(binder)

        bindings = [
            (Engine, get_engine),
            (sessionmaker[Session], get_session),
            (TransactionManagerPort, TransactionManager),
        ]
        for interface, implementation in bindings:
            if interface not in self.exclude_classes:
                binder.bind(interface, to=implementation, scope=singleton)

