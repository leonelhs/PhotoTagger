import os.path


class MetaData:
    def __init__(self, data):
        self.folder = data["folder"]
        self.file = data["file"]
        self.tags = data["tags"]
        self.encodings = data["encodings"]
        self.landmarks = data["landmarks"]
        self.bounds = data["bounds"]
        self.pixmap = data["pixmap"]
        self.path = os.path.join(self.folder, self.file)


