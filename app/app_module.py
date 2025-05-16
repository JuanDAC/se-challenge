from injector import Injector, Module
from app.infrastructure.infrastructure_module import InfrastructureModule
from app.use_cases.use_cases_module import UseCasesModule
from app.config.config_module import ConfigModule


class AppModule(Module):
    def configure(self, binder):
        super().configure(binder)

        binder.install(ConfigModule())
        binder.install(InfrastructureModule())
        binder.install(UseCasesModule())


injector = Injector([AppModule()])
