from os.path import join
from tagger import unserialize


class Face:
    def __init__(self, folder, file, tags, encodings, landmarks, thumbnail):
        self.folder = folder
        self.file = file
        self.tags = tags
        self.encodings = unserialize(encodings)
        self.landmarks = unserialize(landmarks)
        self.thumbnail = unserialize(thumbnail).toqpixmap()
        self.path = join(folder, file)
