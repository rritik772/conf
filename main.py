from click import argument, command, option


from src.applicationSettings import ApplicationSettings
from src.database import Database, FileInfo

cli_options = {
    "dir": {
        "short": '-d',
        "long": "--dir",
        "help": "Dir to cd'ed into",
        "default": "__current",
        "required": False
    },
    "follow": {
        "short": "-f",
        "long": "--follow",
        "help": "Follow upto n times",
        "default": 3,
        "required": False
    },
    "store": {
        "short": "-s",
        "long": "--store",
        "help": "Store file name",
        "default": "~/.config/conf/db.sqlite",
        "required": False
    }
}

dir = cli_options["dir"]
follow = cli_options["follow"]
store = cli_options["store"]

@command()
@argument("filename",    required=True)
@option(dir['short'],    dir['long'],    default=dir['default'],    help=dir['help'],    required=dir["required"])
@option(follow['short'], follow['long'], default=follow['default'], help=follow['help'], required=follow["required"])
@option(store['short'],  store['long'],  default=store['default'],  help=store['help'],  required=store["required"])
def setupApplication(filename, dir, follow, store):
    applicationSettings = ApplicationSettings()
    database = Database()

    applicationSettings.filename = filename
    applicationSettings.follow = follow
    applicationSettings.database_file = store

    applicationSettings.setDir(dir)

    database.initDatabse(applicationSettings.database_file)
    database.createTable()

    files = database.searchFile(applicationSettings.filename)
    if len(files):
        openFile(files[0])
    else:
        print('No files found')


def openFile(file: FileInfo):
    import sys
    import os
    from os import path
    from subprocess import Popen, PIPE

    database = Database()

    filename = file[0]
    rootDir = file[1]
    relDir = file[2]
    __rank__ = file[3]

    real_file_path = path.join(rootDir, relDir, filename)
    if not path.exists(real_file_path):
        print("Looks like file doesn't exist")
        return

    rel_file_path = path.join(relDir, filename)

    try:
        database.incRank(filename)
        editor = path.expandvars("$EDITOR")

        p: Popen = Popen(
            [ editor, rel_file_path ], 
            start_new_session=True, 
            cwd=rootDir,
        )

        p.wait()
        sys.exit(0)

    except Exception as err:
        print(err)
        sys.exit(1)


if __name__ == "__main__":
    setupApplication()
