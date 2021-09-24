import logging
import pathlib
from os import getenv
from os.path import join, exists


class Config(object):
    def __init__(self):
        self._dict = {}
        self._boolValues = {"yes": True, "true": True, "enable": True, "no": False, "false": False, "disable": True}

        log = logging.getLogger("Config")

        # load config from environment
        self._set("dev", str(getenv("NPS_DEV", "0") == "1"))
        self._set("storage", getenv("NPS_STORAGE", "/nupyserver"))
        self._set("checkout_min", getenv("NPS_CHECKOUT", "5"))

        # add app internal config values
        self._set("db", join(self.get("storage"), "nupyserver.db"))
        self._set("checkout", join(self.get("storage"), "checkout"))
        self._set("packages", join(self.get("storage"), "packages"))
        self._set("log", join(self.get("storage"), "log"))

        # Check directories
        if not exists(self.get("log")):
            log.info("Log directory not found. Try to create...")
            pathlib.Path(self.get("log")).mkdir(parents=True, exist_ok=True)

        if not exists(self.get("checkout")):
            log.info("Checkout directory not found. Try to create...")
            pathlib.Path(self.get("checkout")).mkdir(parents=True, exist_ok=True)

        if not exists(self.get("packages")):
            log.info("Package directory not found. Try to create...")
            pathlib.Path(self.get("packages")).mkdir(parents=True, exist_ok=True)

        if self.getboolean("dev"):
            self.print_debug()

    def _set(self, name: str, value):
        self._dict[name] = str(value)

    def get(self, name: str, fallback=None):
        return self._dict[name] if name in self._dict else fallback

    def getint(self, name: str, fallback=None):
        strVal = self.get(name, fallback=None)
        if strVal:
            try:
                return int(strVal)
            except:
                pass

        return fallback

    def getboolean(self, name: str, fallback: bool = None):
        if name in self._dict:
            if self._dict[name] in self._boolValues:
                return self._boolValues[self._dict[name]]

        return fallback

    def print_debug(self):
        print("Config {")
        for name in self._dict:
            print(f"  {name} = {self._dict[name]}")

        print("}")
