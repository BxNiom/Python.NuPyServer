from fastapi import FastAPI

from nupyserver.checkout import CheckOut
from nupyserver.config import Config
from nupyserver.database import Database


class Server(FastAPI):
    def __init__(self):
        self.config = Config()
        self.db = Database(self.config.get("_app", "db"))
        self.checkout = CheckOut(self.db, self.config)
        self.checkout.run()

        FastAPI.__init__(self, title="NuPyServer")

        self._init_services()

    def _init_services(self):
        if self.config.getboolean("protocols", "version3", fallback=True):
            from nupyserver.v3 import init as init_v3
            init_v3(self)


app = Server()
