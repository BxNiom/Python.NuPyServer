import logging
import pathlib
from configparser import ConfigParser
from os.path import join, exists


class Config(ConfigParser):
    def __init__(self):
        log = logging.getLogger("Config")
        # TODO change
        dev = True

        ConfigParser.__init__(self)
        configFilePath = ("./venv" if dev else "") + "/etc/nupyserver.conf"

        # load config file
        self.read(configFilePath)

        # add app internal config values
        self.add_section("_app")
        self.set("_app", "dev", str(dev))
        self.set("_app", "db", join(self.get("server", "storage"), "nupyserver.db"))
        self.set("_app", "checkout", join(self.get("server", "storage"), "checkout"))
        self.set("_app", "packages", join(self.get("server", "storage"), "packages"))
        self.set("_app", "log", join(self.get("server", "storage"), "log"))
        self.set("_app", "ssl", str(self.has_option("server", "ssl_cert") and self.has_option("server", "ssl_key")))
        self.set("_app", "url",
                 f"http{'s' if self.getboolean('_app', 'ssl') else ''}://{self.get('server', 'host')}:" + \
                 f"{self.get('server', 'port')}")

        # Check directories
        if not exists(self.get("_app", "log")):
            log.info("Log directory not found. Try to create...")
            pathlib.Path(self.get("_app", "log")).mkdir(parents=True, exist_ok=True)

        if not exists(self.get("_app", "checkout")):
            log.info("Checkout directory not found. Try to create...")
            pathlib.Path(self.get("_app", "checkout")).mkdir(parents=True, exist_ok=True)

        if not exists(self.get("_app", "packages")):
            log.info("Package directory not found. Try to create...")
            pathlib.Path(self.get("_app", "packages")).mkdir(parents=True, exist_ok=True)

        if dev:
            self.print_debug()

    def print_debug(self):
        log = logging.getLogger("Config")
        log.debug("Config {")
        for section in self.sections():
            log.debug(f"  [{section}]")
            options = self.options(section)
            for item in options:
                log.debug(f"    {item} = {self.get(section, item)}")
        log.debug("}")
