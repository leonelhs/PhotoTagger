from abc import abstractmethod

from PySide6.QtGui import Qt, QPixmap
from PySide6.QtWidgets import QVBoxLayout, QLabel


class PhotoBase(QVBoxLayout):

    def __init__(self, metadata, *args):
        QVBoxLayout.__init__(self, *args)
        self.__label = None
        self.__frame = None
        self.__click = None
        self.__doubleClick = None
        self.__metadata = metadata
        self.__initPhotoView()
        self.__initPhotoTag()
        self.__style()

    def __eq__(self, other):
        if self.tags() == other.tags():
            return True
        return False

    def __initPhotoView(self):
        self.__frame = QLabel()
        self.__frame.setPixmap(self.__metadata.pixmap.toqpixmap())
        self.__frame.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.__frame.mousePressEvent = self.clickEvent
        self.__frame.mouseDoubleClickEvent = self.doubleClickEvent
        self.__frame.contextMenuEvent = self.contextMenuEvent
        self.addWidget(self.__frame)

    def __initPhotoTag(self):
        self.__label = QLabel()
        self.__label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setTags(self.__metadata.tags)
        self.addWidget(self.__label)

    def frame(self):
        return self.__frame

    def metadata(self):
        return self.__metadata

    def label(self):
        return self.__label

    def tags(self):
        return self.__metadata.tags

    def setTags(self, tags):
        self.__metadata.tags = tags
        self.__label.setText(tags)

    def pixmap(self):
        return self.__metadata.pixmap.toqpixmap()

    def setPixmap(self, pixmap):
        self.__frame.setPixmap(pixmap)

    def filePath(self):
        return self.__metadata.path

    def cropFace(self):
        image = QPixmap(self.filePath())
        rect = self.bounds()
        try:
            return image.copy(rect['x'], rect['y'], rect['w'], rect['h'])
        except TypeError:
            print("No bounds where found at %s " % self.fileName())
            return None

    def fileName(self):
        return self.__metadata.file

    def folder(self):
        return self.__metadata.folder

    def encodings(self):
        return self.__metadata.encodings

    def landmarks(self):
        return self.__metadata.landmarks

    def bounds(self):
        return self.__metadata.bounds

    def clickEvent(self, event):
        self.__click(event, self)

    def doubleClickEvent(self, event):
        self.__doubleClick(event, self)

    def setClickEvent(self, callback):
        self.__click = callback

    def setDoubleClickEvent(self, callback):
        self.__doubleClick = callback

    def __style(self):
        self.__frame.setStyleSheet("QLabel::hover"
                                   "{border: 1px solid black;}")

    @abstractmethod
    def contextMenuEvent(self, event):
        pass
