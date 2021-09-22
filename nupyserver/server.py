from fastapi import FastAPI

from nupyserver.config import Config
from nupyserver.database import Database
from nupyserver.v3 import init as init_v3


class Server(FastAPI):
    def __init__(self):
        self.config = Config()
        self.db = Database(self.config.get("_app", "db"))
        FastAPI.__init__(self, title="NuPyServer")
        init_v3(self)

    def __init_services__(self):
        pass


app = Server()
