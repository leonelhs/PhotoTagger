import shutil

from PySide6.QtWidgets import QMenu
from UI.widgets.baseclass.photo_base import PhotoBase


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

    def writeTags(self, callback, tags):
        super().setTags(tags)
        folder = self.folder()
        file = self.fileName()
        callback((tags, folder, file))
