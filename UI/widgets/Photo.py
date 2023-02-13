from PySide6.QtGui import Qt
from PySide6.QtWidgets import QVBoxLayout, QLabel, QMenu


def fit_image(pixmap, size):
    return pixmap.scaled(size, size, Qt.KeepAspectRatio, Qt.SmoothTransformation)


class Photo(QVBoxLayout):

    def __init__(self, face, *args):
        QVBoxLayout.__init__(self, *args)
        # mouse events
        self.click = None
        self.doubleClick = None
        self.contextTagEvent = None
        self.contextLandmarksEvent = None
        self.contextNewGalleryEvent = None

        self.face = face
        self.tags = "Unknown"
        if face.tags:
            self.tags = face.tags

        self.frame = QLabel()
        self.frame.setAlignment(Qt.AlignCenter)
        self.frame.setPixmap(face.pixmap)
        self.addWidget(self.frame)
        self.label = QLabel()
        self.label.setText(self.tags)
        self.label.setAlignment(Qt.AlignCenter)
        self.addWidget(self.label)
        self.frame.mousePressEvent = self.clickEvent
        self.frame.mouseDoubleClickEvent = self.doubleClickEvent
        self.frame.contextMenuEvent = self.contextMenuEvent

    def getFrame(self):
        return self.frame

    def getFace(self):
        return self.face

    def getLabel(self):
        return self.label

    def setTag(self, tag):
        self.label.setText(tag)

    def setPixmap(self, pixmap):
        self.face.pixmap = pixmap
        self.frame.setPixmap(self.face.pixmap)

    def getPixmap(self):
        return self.face.pixmap

    def getFilePath(self):
        return self.face.image_path

    def getFileName(self):
        return self.face.face_id

    def getEncodings(self):
        return self.face.encodings

    def getLandmarks(self):
        return self.face.landmarks

    def clickEvent(self, event):
        self.click(event, self.face)

    def doubleClickEvent(self, event):
        self.doubleClick(event, self.face)

    def setClickEvent(self, callback):
        self.click = callback

    def setDoubleClickEvent(self, callback):
        self.doubleClick = callback

    def setContextTagEvent(self, callback):
        self.contextTagEvent = callback

    def setContextLandmarksEvent(self, callback):
        self.contextLandmarksEvent = callback

    def setContextNewGalleryEvent(self, callback):
        self.contextNewGalleryEvent = callback

    def contextMenuEvent(self, event):
        context = QMenu(self.frame)
        tagAction = context.addAction("Tag this person")
        marksAction = context.addAction("Show face landmarks")
        newGalleryAction = context.addAction("Create new gallery")

        action = context.exec_(event.globalPos())
        if action == tagAction:
            self.contextTagEvent(event, self.face)
        elif action == marksAction:
            self.contextLandmarksEvent(event, self.face)
        elif action == newGalleryAction:
            self.contextNewGalleryEvent(event, self.face)
