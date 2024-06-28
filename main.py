import sys
from os import path
import atexit
from click import argument, command, option


from src.applicationSettings import ApplicationSettings
from src.database import Database, FileInfo
from src.utils.commonUtils import lookForFollowFileOrDir

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
    applicationSettings.follow_count = follow
    applicationSettings.database_file = store

    applicationSettings.setDir(dir)

    database.initDatabse(applicationSettings.database_file)
    database.createTable()

    files = database.searchFile(applicationSettings.filename)
    if len(files):
        openFile(files[0])
    else:
        result = lookForFollowFileOrDir()
        if not result:
            print('File does not exist')
            sys.exit(1)

        root_dir, rel_dir = result
        file_info = FileInfo(filename, root_dir, rel_dir, 0)

        file_path = path.join(root_dir, rel_dir, filename)
        if not path.exists(file_path):
            print('No such file exist')
            sys.exit(1)

        database.insertFileInfo(file_info)


def openFile(file: FileInfo):
    from os import path
    from subprocess import Popen, PIPE, run

    database = Database()

    filename = file.filename
    rootDir = file.rootDir
    relDir = file.relDir
    __rank__ = file.rank

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

def exit():
    database = Database()
    if not database.db:
        return

    database.db.close()

if __name__ == "__main__":
    atexit.register(exit)
    setupApplication()
