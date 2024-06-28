import os
from os import path
from typing import Optional

def getFullPath(location: str, isFile=False, mkdir=False) -> str:
    location = path.expanduser(path.expandvars(location))

    dir = path.dirname(location) if isFile else location
    if not path.exists(dir) and mkdir:
        os.mkdir(dir)

    location = path.realpath(location)

    return location

def lookForFollowFileOrDir(dir=os.getcwd(), follow=3) -> Optional[tuple[str, str]]:
    from src.applicationSettings import ApplicationSettings

    if not follow:
        return None

    applicationSettings = ApplicationSettings();

    to_be_seen = applicationSettings.follow

    ls = set(os.listdir(dir))
    file_found = to_be_seen.intersection(ls)
    if len(file_found):
        return ( dir, '' )

    parent_dir = path.dirname(dir)
    dir = path.basename(dir)

    lookedDir = lookForFollowFileOrDir(parent_dir, follow-1)
    if not lookedDir: return None

    return ( lookedDir[0], dir + "/" + lookedDir[1] )
