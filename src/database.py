import sqlite3
from typing import NamedTuple

from src.utils.commonUtils import getFullPath


class FileInfo:
    def __init__(self, filename: str, rootDir: str, relDir: str, rank: int):
        if 0 in [len(filename), len(rootDir)]:
            raise ValueError('Filename and root must exist')

        self.filename = filename
        self.rootDir = rootDir
        self.relDir = relDir
        self.rank = rank


class Database:

    __instance = None
    __database_init = False

    def __new__(cls, *args, **kwargs):
        if not cls.__instance:
            cls.__instance = super(Database, cls).__new__(cls, *args, **kwargs)
        return cls.__instance

    def __copy__(self):
        raise TypeError("Database is a singleton class and cannot be copied.")

    def __deepcopy__(self):
        raise TypeError("Database is a singleton class and cannot be copied.")

    def __init__(self):
        if self.__instance:
            return

        self.db: sqlite3.Connection | None = None
        self.cursor: sqlite3.Cursor | None = None

    def initDatabse(self, file: str):
        if self.__database_init:
            return

        file = getFullPath(file, isFile=True, mkdir=True)
        self.db = sqlite3.connect(file)
        self.cursor = self.db.cursor()

    def createTable(self):
        if not self.db or not self.cursor:
            raise sqlite3.DatabaseError("Connection to database is not established")

        self.cursor.execute(
            "CREATE TABLE IF NOT EXISTS conf(filename TEXT PRIMARY KEY NOT NULL, rootDir TEXT NOT NULL, relDir TEXT NOT NULL, rank INT)"
        )
        self.cursor.execute("CREATE INDEX IF NOT EXISTS idx_rank ON conf (rank)")
        self.db.commit()

    def searchFile(self, filename: str) -> list[FileInfo]:
        if not len(filename):
            raise ValueError("No filename provided.")

        if not self.cursor:
            raise sqlite3.DatabaseError("Connection to database is not established")

        res = self.cursor.execute(
            "SELECT filename, rootDir, relDir, rank FROM conf where filename LIKE ? ORDER BY rank DESC",
            [(f"%{filename}%")],
        )
        res = res.fetchall()

        result = []
        for e in res:
            result.append(FileInfo(e[0], e[1], e[2], e[3]))

        return result

    def incRank(self, filename: str):
        if not len(filename):
            raise ValueError("No filename provided.")

        if not self.db or not self.cursor:
            raise sqlite3.DatabaseError("Connection to database is not established")

        self.cursor.execute(
            "UPDATE conf SET rank = rank + 1 WHERE filename = ?", [(filename)]
        )
        self.db.commit()

    def insertFileInfo(self, fileInfo: FileInfo):
        if not self.db or not self.cursor:
            raise sqlite3.DatabaseError("Connection to database is not established")

        self.cursor.execute(
            'INSERT INTO conf(filename, rootDir, relDir, rank) VALUES(?, ?, ?, ?)',
            ([ fileInfo.filename, fileInfo.rootDir, fileInfo.relDir, 0 ])
        )
        self.db.commit()
