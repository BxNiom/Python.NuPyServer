__version__ = "0.1.0"

from nupyserver.v3.services import Services


def init(server):
    _services = Services()

    @server.get("/v3/index.json")
    def services_index(): return _services.create_index()