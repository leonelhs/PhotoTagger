from PySide6.QtWidgets import QGridLayout

from UI.widgets import grid_positions
from UI.widgets.baseclass.PhotoContainerBase import PhotoContainerBase


class PhotoGrid(PhotoContainerBase):

    def __init__(self, *args):
        PhotoContainerBase.__init__(self, *args)
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextNewGalleryEvent = None

    def initLayout(self, layout):
        self.layout = QGridLayout(self.scroll_contents)
        self.layout.setContentsMargins(0, 0, 0, 0)
        pass

    def appendPhoto(self, face, position=(0, 0)):
        photo = self.newPhoto(face)
        self.layout.addLayout(photo, position[0], position[1])

    def populate_grid(self, thumbnails, max_columns=5):
        self.clearLayout()
        positions = grid_positions(len(thumbnails), max_columns)
        for position, thumbnail in zip(positions, thumbnails):
            self.appendPhoto(thumbnail, position)

    def newPhoto(self, face):
        photo = super().newPhoto(face)
        photo.setContextTagEvent(self.contextTagEvent)
        photo.setContextLandmarksEvent(self.contextLandmarksEvent)
        photo.setContextNewGalleryEvent(self.contextNewGalleryEvent)
        return photo

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContextNewGalleryEvent(self, callback):
        self.contextNewGalleryEvent = callback

    def clearLayout(self):
        while self.layout.count():
            child = self.layout.takeAt(0)
            if child.layout():
                child.layout().itemAt(0).widget().deleteLater()
                child.layout().itemAt(1).widget().deleteLater()
                child.layout().deleteLater()
