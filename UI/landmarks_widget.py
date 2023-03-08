import PIL.Image
from PySide6.QtCore import (QMetaObject, Qt, Signal)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QVBoxLayout, QWidget, QGraphicsScene)

from UI.widgets.image_graphics_wiew import ImageGraphicsView


def openImage(path):
    image = PIL.Image.open(path)
    return image.toqpixmap()


def get_line(array):
    for i in range(0, len(array), 2):
        yield array[i:i + 2]


def drawFaceLandmarks(pixmap, landmarks):
    painter = QPainter(pixmap)
    painter.setPen(QColor(255, 255, 0))
    for marks in landmarks:
        for positions in marks:
            for position in get_line(marks[positions]):
                if len(position) > 1:
                    painter.drawLine(*position[0], *position[1])


def drawFaceBound(pixmap, rect):
    painter = QPainter(pixmap)
    painter.setPen(QColor(255, 255, 0))
    try:
        painter.drawRect(rect['x'], rect['y'], rect['w'], rect['h'])
    except TypeError:
        print("No able to draw bounds")
        return None


class LandmarksWidget(QWidget):
    landmarksMessageHandler = Signal(str)

    def __init__(self, parent=None):
        super(LandmarksWidget, self).__init__(parent)
        self.__photoViewer = None
        self.__layout = None
        self.setupUi()

    def setupUi(self):
        self.__layout = QVBoxLayout(self)
        self.__photoViewer = ImageGraphicsView(self)
        self.__photoViewer.setAlignment(Qt.AlignCenter)
        self.__layout.addWidget(self.__photoViewer)
        QMetaObject.connectSlotsByName(self)

    def onFaceLandmarksRequest(self, photo):
        pixmap = openImage(photo.filePath())
        landmarks = photo.landmarks()
        bounds = photo.bounds()
        drawFaceBound(pixmap, bounds)
        drawFaceLandmarks(pixmap, landmarks)
        scene = QGraphicsScene()
        scene.addPixmap(pixmap)
        self.__photoViewer.setScene(scene)
        self.__photoViewer.redraw()
        self.resize(pixmap.width(), pixmap.height())
