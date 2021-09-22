import json

from nupyserver.server import Server


class Services:
    _services = []

    def register_service(self, service):
        service.register_services()
        service.register_routes()

    def add_service(self, serviceId, serviceType):
        self._services.append({
            "@id": serviceId,
            "@type": serviceType
        })

    def create_index(self):
        return {"version": "3.0.0", "resources": self._services}


class BaseService:
    def __init__(self, services: Services, server: Server):
        self.__services = services
        self.__server = server

    @property
    def services(self): return self.__services

    @property
    def server(self): return self.__server

    @property
    def config(self): return self.__server.config

    @property
    def db(self): return self.__server.db

    def register_services(self):
        pass

    def register_routes(self):
        pass