import os
import sys
from toml import load  as tomlLoad

from src.utils.commonUtils import getFullPath


class ApplicationSettings:

    __instance = None
    __init = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __copy__(self):
        raise TypeError(
            "ApplicationSettings is a singleton class and cannot be copied."
        )

    def __deepcopy__(self):
        raise TypeError(
            "ApplicationSettings is a singleton class and cannot be copied."
        )

    def __init__(self):
        if self.__init:
            return

        self.filename = ""
        self.follow_count = 3
        self.dir = "__current"
        self.database_file = "db.sqlite"
        self.follow = {".git", "Makefile", "CMake"}

        self.editors = {
            'code': {
                'dir': '-a',
                'file': '-g'
            }
        }

        self.configFile()
        self.__init = True

    def setDir(self, dir):
        if dir == "__current":
            self.dir = getFullPath(os.curdir)
            return

        self.dir = getFullPath(dir)

    def configFile(self):
        conf_path = ""

        if os.name == "nt":
            conf_path = getFullPath("%APPDATA%/conf/conf.toml")
        elif os.name == "posix":
            conf_path = getFullPath("~/.config/conf/conf.toml")
        else:
            raise ValueError(f"OS not described please pass config file is param.")

        if not os.path.exists(conf_path):
            print("config.toml does not exist. Proceeding with the defaults.")
            return

        try:
            conf_file = tomlLoad(conf_path)

            if 'editors' in conf_file:
                self.editors = conf_file['editors']
            if 'follow' in conf_file:
                self.follow = set(conf_file['follow'])
            if 'database_file' in conf_file:
                self.database_file = conf_file['database_file']

        except Exception as err:
            print(f"Cannot read file from {conf_path}. Err: ${err}")
            sys.exit(1)

