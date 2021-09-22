__version__ = "0.1.0"

import logging

from nupyserver.v3.autocomplete import AutoCompleteService
from nupyserver.v3.query import QueryService
from nupyserver.v3.services import Services
from nupyserver.v3.container import ContainerService


def init(server):
    logging.info("Loading protocol version 3...")

    _services = Services()
    _services.register_service(ContainerService(_services, server))
    _services.register_service(QueryService(_services, server))
    _services.register_service(AutoCompleteService(_services, server))

    @server.get("/v3/index.json")
    def services_index(): return _services.create_index()