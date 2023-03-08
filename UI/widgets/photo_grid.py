from UI.widgets.photo import Photo
from UI.widgets.baseclass.photo_grid_base import PhotoGridBase

from UI.widgets import grid_positions


class PhotoGrid(PhotoGridBase):

    def __init__(self, *args):
        PhotoGridBase.__init__(self, *args)
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextMovePhotosEvent = None
        self.contextCropFacesEvent = None
        self.__photos = []

    def photos(self):
        return self.__photos

    def drawPhoto(self, metadata, position=(0, 0)):
        photo = self.newPhoto(metadata)
        self.layout.addLayout(photo, position[0], position[1])

    def drawPhotos(self, metadataList, max_columns=5):
        self.clear()
        positions = grid_positions(len(metadataList), max_columns)
        for position, metadata in zip(positions, metadataList):
            self.drawPhoto(metadata, position)

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContexMovePhotosEvent(self, callback):
        self.contextMovePhotosEvent = callback

    def setContexCropFacesEvent(self, callback):
        self.contextCropFacesEvent = callback

    def newPhoto(self, metadata):
        photo = Photo(metadata)
        photo.setClickEvent(self.click)
        photo.setDoubleClickEvent(self.doubleClick)
        photo.setContextTagEvent(self.contextTagEvent)
        photo.setContextLandmarksEvent(self.contextLandmarksEvent)
        photo.setContextMovePhotosEvent(self.contextMovePhotosEvent)
        photo.setContextCropFaceEvent(self.contextCropFacesEvent)
        self.__photos.append(photo)
        return photo

    def clear(self):
        try:
            for photo in self.__photos:
                photo.deleteWidget()
        except RuntimeError:
            print("Photo widget already deleted.")
        finally:
            self.__photos = []