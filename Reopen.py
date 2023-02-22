import contextlib
from datetime import datetime
from sqlite3 import connect as connect


class DbConnection(contextlib.closing):
    def __init__(self, database):
        self.database = connect(database)
        super().__init__(self.database)


class Reopen:
    def __init__(self):
        self.database = "gallery.db"
        self._create_schema()

    def appendRecents(self, file_path):
        with DbConnection(self.database) as con:
            with con as cur:
                data = (file_path, datetime.now())
                try:
                    cur.execute("INSERT INTO recents(folder, opened) VALUES(?, ?)", data)
                except:
                    pass

    def fetchRecents(self):
        with DbConnection(self.database) as con:
            with con as cur:
                query = "SELECT folder FROM recents ORDER BY opened DESC LIMIT 10"
                return cur.execute(query).fetchall()

    def _create_schema(self):
        with DbConnection(self.database) as con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS recents(
                    folder TEXT NOT NULL UNIQUE , 
                    opened DATETIME, 
                    PRIMARY KEY (folder));
                """)

