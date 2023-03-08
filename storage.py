import contextlib
import pickle
from datetime import datetime
from sqlite3 import connect as connect

from meta_data import MetaData


def serialize(data):
    return pickle.dumps(data)


def unserialize(raw):
    return pickle.loads(raw)


def serializeValues(values):
    return [(
        row.folder,
        row.file,
        row.tags,
        serialize(row.encodings),
        serialize(row.landmarks),
        serialize(row.bounds),
        serialize(row.pixmap)
    ) for row in values]


def unserializeValues(values):
    return [MetaData({
        "folder": row[0],
        "file": row[1],
        "tags": row[2],
        "encodings": unserialize(row[3]),
        "landmarks": unserialize(row[4]),
        "bounds": unserialize(row[5]),
        "pixmap": unserialize(row[6])
    }) for row in values]


class DbConnection(contextlib.closing):
    def __init__(self, database):
        self.database = connect(database)
        super().__init__(self.database)


class Storage:
    def __init__(self):
        self.database = "gallery.db"
        self._create_schema()

    def exists(self, folder):
        with DbConnection(self.database) as con:
            try:
                query = "SELECT folder FROM gallery WHERE folder = ?"
                if folder in con.execute(query, (folder,)).fetchone():
                    return True
            except:
                pass
                return False

    def saveGallery(self, folder, values):
        values = serializeValues(values)
        with DbConnection(self.database) as con:
            with con as ins:
                gallery = (folder, datetime.now())
                ins.execute("INSERT INTO gallery(folder, opened) VALUES(?, ?)", gallery)
            with con as cur:
                query = "INSERT INTO " \
                        "faces(folder, file, tags, encodings, landmarks, bounds, thumbnail) " \
                        "VALUES(?,?,?,?,?,?,?)"
                cur.executemany(query, values)
                con.commit()

    def fetchGalleries(self):
        with DbConnection(self.database) as con:
            query = "SELECT folder FROM gallery ORDER BY opened DESC LIMIT 10"
            return con.execute(query).fetchall()

    def fetchAllFaces(self, folder):
        with DbConnection(self.database) as con:
            query = "SELECT * FROM faces WHERE folder = ? order by tags"
            result = con.execute(query, (folder,)).fetchall()
            return unserializeValues(result)

    def fetchFaceBy(self, folder, file):
        with DbConnection(self.database) as con:
            query = "SELECT * FROM faces WHERE folder = ? AND file = ?"
            return con.execute(query, (folder, file)).fetchone()

    def updateAllTags(self, values):
        with DbConnection(self.database) as con:
            query = "UPDATE faces SET tags = ? WHERE folder = ? AND file = ?"
            con.execute(query, values)
            con.commit()

    def updateFolderPath(self, values):
        with DbConnection(self.database) as con:
            query = "UPDATE faces SET folder = ? WHERE folder = ? AND file = ?"
            con.execute(query, values)
            con.commit()

    def _create_schema(self):
        with DbConnection(self.database) as con:
            con.executescript("""
                CREATE TABLE IF NOT EXISTS gallery(
                    folder TEXT NOT NULL UNIQUE , 
                    opened DATETIME, 
                    PRIMARY KEY (folder));

                CREATE TABLE IF NOT EXISTS faces(
                    folder TEXT NOT NULL,
                    file TEXT NOT NULL,
                    tags TEXT, 
                    encodings BLOB, 
                    landmarks BLOB,
                    bounds BLOB,
                    thumbnail BLOB,
                    PRIMARY KEY (folder, file));
                """)
