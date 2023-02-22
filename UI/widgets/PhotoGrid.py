from UI.widgets.Photo import Photo
from UI.widgets.baseclass.PhotoGridBase import PhotoGridBase

from UI.widgets import grid_positions


class PhotoGrid(PhotoGridBase):

    def __init__(self, *args):
        PhotoGridBase.__init__(self, *args)
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextMovePhotosEvent = None
        self.contextCopyPhotosEvent = None
        self.__photos = []

    def photos(self):
        return self.__photos

    def drawPhoto(self, metadata, position=(0, 0)):
        photo = self.newPhoto(metadata)
        photo.drawPixmap()
        self.layout.addLayout(photo, position[0], position[1])

    def drawPhotos(self, metadataList, max_columns=5):
        self.__clear()
        positions = grid_positions(len(metadataList), max_columns)
        for position, metadata in zip(positions, metadataList):
            self.drawPhoto(metadata, position)

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContexMovePhotosEvent(self, callback):
        self.contextMovePhotosEvent = callback

    def setContexCopyPhotosEvent(self, callback):
        self.contextCopyPhotosEvent = callback

    def newPhoto(self, metadata):
        photo = Photo(metadata)
        photo.setClickEvent(self.click)
        photo.setDoubleClickEvent(self.doubleClick)
        photo.setContextTagEvent(self.contextTagEvent)
        photo.setContextLandmarksEvent(self.contextLandmarksEvent)
        photo.setContextMovePhotosEvent(self.contextMovePhotosEvent)
        photo.setContextCopyPhotosEvent(self.contextCopyPhotosEvent)
        self.__photos.append(photo)
        return photo

    def __clear(self):
        for photo in self.__photos:
            photo.deleteWidget()
        self.__photos = []
