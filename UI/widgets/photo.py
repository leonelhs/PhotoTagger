import shutil

from PySide6.QtWidgets import QMenu
from UI.widgets.baseclass.photo_base import PhotoBase


class Photo(PhotoBase):
    def __init__(self, metadata, *args):
        PhotoBase.__init__(self, metadata, *args)
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextMovePhotosEvent = None
        self.contextCropFaceEvent = None

    def deleteWidget(self):
        self.frame().deleteLater()
        self.label().deleteLater()
        self.deleteLater()

    def moveFile(self, callback, new_folder):
        try:
            shutil.move(self.filePath(), new_folder)
            self.deleteWidget()
            callback(self.fileName(), self.folder(), new_folder)
        except shutil.Error:
            print("No able to mve file: %s" % self.filePath())
        except FileNotFoundError:
            print("No able to mve file: %s" % self.filePath())

    def copyFile(self, new_path):
        shutil.copy(self.filePath(), new_path)
        self.deleteWidget()

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContextMovePhotosEvent(self, callback):
        self.contextMovePhotosEvent = callback

    def setContextCropFaceEvent(self, callback):
        self.contextCropFaceEvent = callback

    def contextMenuEvent(self, event):
        context = QMenu(self.frame())
        tagAction = context.addAction("Tag this person")
        marksAction = context.addAction("Show face landmarks")
        moveTaggedFilesAction = context.addAction("Move photos tagged")
        cropFacesAction = context.addAction("Create faces photo set")

        action = context.exec_(event.globalPos())
        if action == tagAction:
            self.contextTagEvent(event, self)
        elif action == marksAction:
            self.contextLandmarksEvent(event, self)
        elif action == moveTaggedFilesAction:
            self.contextMovePhotosEvent(event, self)
        elif action == cropFacesAction:
            self.contextCropFaceEvent(event, self)

    def writeTags(self, callback, tags):
        super().setTags(tags)
        folder = self.folder()
        file = self.fileName()
        callback(tags, folder, file)
