from abc import abstractmethod

from PySide6.QtWidgets import QScrollArea, QWidget, QGridLayout


class PhotoGridBase(QScrollArea):
    def __init__(self, *args):
        QScrollArea.__init__(self, *args)
        self.click = None
        self.doubleClick = None
        self.setWidgetResizable(True)
        self.scroll_contents = QWidget()
        self.layout = QGridLayout(self.scroll_contents)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setWidget(self.scroll_contents)

    @abstractmethod
    def drawPhoto(self, face):
        pass

    def setClickEvent(self, callback):
        self.click = callback

    def setDoubleClickEvent(self, callback):
        self.doubleClick = callback

    def getWidth(self):
        return self.size().width()


