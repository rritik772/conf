import os
from os import path

def getFullPath(location: str, isFile=False, mkdir=False) -> str:
    location = path.expanduser(path.expandvars(location))

    dir = path.dirname(location) if isFile else location
    if not path.exists(dir) and mkdir:
        os.mkdir(dir)

    location = path.realpath(location)

    return location
