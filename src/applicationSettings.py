import os

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
        self.follow = { '.git', 'Makefile', 'CMake' }

        self.__init = True

    def setDir(self, dir):
        if dir == "__current":
            self.dir = getFullPath(os.curdir)
            return

        self.dir = getFullPath(dir)
