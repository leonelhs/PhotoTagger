import io
import pickle
import sys

import pyexiv2

import PIL.Image
import numpy as np
from PySide6.QtCore import Qt
from PySide6.QtGui import QImage, QPixmap
from PySide6.QtWidgets import (
    QMainWindow, QApplication, QLabel
)


def serialize(data):
    return pickle.dumps(data, protocol=5)


def unSerialize(raw_bytes):
    return pickle.loads(raw_bytes)


def imageThumbnail(image):
    image.thumb((128, 128), PIL.Image.ANTIALIAS)


def imageNpArray(q_image):
    q_image = q_image.convertToFormat(QImage.Format.Format_RGB32)
    width = q_image.width()
    height = q_image.height()
    ptr = q_image.constBits()
    arr = np.array(ptr).reshape(height, width, 4)  # Copies the data
    return arr


def imageOpen(image_file):
    image = PIL.Image.open(image_file)
    return image.convert('RGB')


def imageQopen(image_file):
    return QImage(image_file)


def npArray2Pil(image):
    image = imageNpArray(image)
    return PIL.Image.fromarray(image)


def unserializePil(image):
    image.thumb((128, 128), PIL.Image.ANTIALIAS)
    image_bytes = serialize(image)
    raw_bytes = unSerialize(image_bytes)
    return raw_bytes.toqpixmap()


low_res = "/home/leonel/lr.jpg"
sample = "/home/leonel/test01.jpg"
error = "//home/leonel/errors/S5031975.jpg"
leonel = "/home/leonel/tiny/test06.jpg"
file_path = "/home/leonel/Martin-Yare.jpg"

myimage = None

thumb = None


def pilexif():
    size = (512, 512)
    im = PIL.Image.open(sample)
    im.thumbnail(size, PIL.Image.LANCZOS)
    exif = im.info['exif']
    im.save(sample, exif=exif)


with open(leonel, 'rb') as file:
    with pyexiv2.ImageData(file.read()) as img:
        exif = img.read_exif()
        thumb = img.read_thumbnail()
        # byte_io = io.BytesIO(img.get_bytes())
        # pil_image = PIL.Image.open(byte_io)
        # pil_image.thumbnail((128, 128), PIL.Image.LANCZOS)
        # img.modify_thumbnail(pil_image.tobytes())
        # byte_io = io.BytesIO(img.get_bytes())
        # pil_image = PIL.Image.open(byte_io)
        # pil_image.save(leonel)
        # myimage = pil_image
        # byte_io = io.BytesIO(thumb)
        # pil_image = PIL.Image.frombytes(200, thumb)
        # pil_image.show()
        image = PIL.Image.frombytes('RGB', (128, 128), thumb, 'raw')
        image.show()



class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()

        # image = imageQopen(leonel)
        # pixmap = QPixmap(image)
        # image2 = npArray2Pil(image)
        pixmap = myimage.toqpixmap()

        picture = QLabel()
        picture.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        picture.setPixmap(pixmap)
        self.setCentralWidget(picture)


def main():
    app = QApplication(sys.argv)
    w = MainWindow()
    w.show()
    app.exec()
