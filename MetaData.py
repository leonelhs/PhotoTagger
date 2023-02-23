class MetaData:
    def __init__(self, data):
        self.path = data["path"]
        self.folder = data["folder"]
        self.file = data["file"]
        self.tags = data["tags"]
        self.encodings = data["encodings"]
        self.landmarks = data["landmarks"]
        self.pixmap = data["pixmap"].toqpixmap()

