import shutil

import PIL.Image
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import QMenu

from FaceTagger import FACE_TAGS

from UI.widgets.baseclass.PhotoBase import PhotoBase


def openImage(path):
    return PIL.Image.open(path)


def get_line(array):
    for i in range(0, len(array), 2):
        yield array[i:i + 2]


class Photo(PhotoBase):

    def __init__(self, metadata, *args):
        PhotoBase.__init__(self, metadata, *args)
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextMovePhotosEvent = None
        self.contextCopyPhotosEvent = None

    def deleteWidget(self):
        self.frame().deleteLater()
        self.label().deleteLater()
        self.deleteLater()

    def moveFile(self, new_path):
        shutil.move(self.filePath(), new_path)
        self.deleteWidget()

    def copyFile(self, new_path):
        shutil.copy(self.filePath(), new_path)
        self.deleteWidget()

    def clone(self):
        return Photo(self.face())

    def drawFaceLandmarks(self):
        painter = QPainter(self.pixmap())
        painter.setPen(QColor(255, 255, 0))
        for marks in self.landmarks():
            for positions in marks:
                for position in get_line(marks[positions]):
                    if len(position) > 1:
                        painter.drawLine(*position[0], *position[1])

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContextMovePhotosEvent(self, callback):
        self.contextMovePhotosEvent = callback

    def setContextCopyPhotosEvent(self, callback):
        self.contextCopyPhotosEvent = callback

    def contextMenuEvent(self, event):
        context = QMenu(self.frame())
        tagAction = context.addAction("Tag this person")
        marksAction = context.addAction("Show face landmarks")
        moveTaggedFilesAction = context.addAction("Move files tagged")
        copyTaggedFilesAction = context.addAction("Copy files tagged")

        action = context.exec_(event.globalPos())
        if action == tagAction:
            self.contextTagEvent(event, self)
        elif action == marksAction:
            self.contextLandmarksEvent(event, self)
        elif action == moveTaggedFilesAction:
            self.contextMovePhotosEvent(event, self)
        elif action == copyTaggedFilesAction:
            self.contextCopyPhotosEvent(event, self)

    def saveTags(self, tags):
        image_original = openImage(self.filePath())
        exif = image_original.getexif()
        exif[FACE_TAGS] = tags
        image_original.save(self.filePath(), exif=exif)

    def setTags(self, tags):
        if not tags:
            tags = "Unknown"
        super().setTags(tags)

    def getOriginalPhoto(self):
        original_photo = self.clone()
        pixmap = openImage(self.filePath()).toqpixmap()
        original_photo.setPixmap(pixmap)
        return original_photo
