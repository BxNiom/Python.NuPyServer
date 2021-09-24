from datetime import datetime, timedelta

from fastapi import FastAPI

from nupyserver.checkout import CheckOut
from nupyserver.config import Config
from nupyserver.database import Database


class Server(FastAPI):
    def __init__(self):
        self.config = Config()
        self.db = Database(self.config.get("db"))
        self.checkout = CheckOut(self.db, self.config)
        self._nextCheckout = None
        self._run_checkout()

        FastAPI.__init__(self, title="NuPyServer")

        self._init_services()

    def _init_services(self):
        from nupyserver.v3 import init as init_v3
        init_v3(self)

        @self.middleware("http")
        def checkout_run(req, call_next):
            response = call_next(req)
            self._run_checkout()
            return response

    def _run_checkout(self):
        if self._nextCheckout is None or self._nextCheckout < datetime.now():
            self._nextCheckout = datetime.now() + timedelta(minutes=self.config.getint("checkout_min", fallback=5))
            self.checkout.run()


app = Server()
