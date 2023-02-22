import pickle
import sys

import PIL.Image
from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel
)


def imageOpen(image_file):
    image = PIL.Image.open(image_file)
    return image.convert('RGB')


def imageThumbnail(image):
    return image.__thumbnail((128, 128), PIL.Image.ANTIALIAS)


def serialize(data):
    return pickle.dumps(data, protocol=5)


def unSerialize(raw_bytes):
    return pickle.loads(raw_bytes)


low_res = "/home/leonel/lr.jpg"
sample = "/home/leonel/hd.png"
leonel = "/home/leonel/fast/me-itesi.jpg"


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        image = imageOpen(low_res)
        image.thumbnail((128, 128), PIL.Image.ANTIALIAS)
        image_bytes = serialize(image)
        raw_bytes = unSerialize(image_bytes)
        pixmap = raw_bytes.toqpixmap()

        picture = QLabel()
        picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        picture.setPixmap(pixmap)
        self.setCentralWidget(picture)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()


def onCompareFaceMessage(self, known_face):
    tagged = []
    for unknown_face in self.imageList.__photos():
        if compareFaces(known_face.encodings, unknown_face.encodings):
            unknown_face.tags = known_face.tags
        tagged.append(unknown_face)
    self.viewer.drawPhotos(tagged)