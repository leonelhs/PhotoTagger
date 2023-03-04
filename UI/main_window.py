from PySide6.QtCore import (QCoreApplication, QMetaObject, Signal, QThreadPool)
from PySide6.QtWidgets import (QHBoxLayout, QMenuBar,
                               QProgressBar, QStatusBar,
                               QVBoxLayout, QWidget, QMainWindow, QMenu, QFileDialog)

from actions import ActionRecents, Action
from face_tagger import compareFaces
from photo_scanner import PhotoScanner
from storage import Storage
from UI.landmarks_widget import LandmarksWidget
from UI.tagger_widget import TaggerWidget
from UI.widgets.photo_grid import PhotoGrid
import qtawesome as qta


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


class MainWindow(QMainWindow, PhotoScanner):
    galleryTaggingHandler = Signal(object)
    galleryLandmarksHandler = Signal(object)

    def __init__(self):
        super().__init__()
        self.storage = None
        self.menuRecents = None
        self.menuGallery = None
        self.menuFile = None
        self.viewer = None
        self.statusbar = None
        self.menubar = None
        self.progressBar = None
        self.widgets_layout = None
        self.central_layout = None
        self.central_widget = None

        self.actionGalleryOpen = Action(self, "Open Gallery", "fa.folder-open")
        self.actionGalleryOpen.setOnClickEvent(self.openPhotoGalleryFolder)

        self.threadpool = QThreadPool()

        self.taggingFaceForm = TaggerWidget()
        self.landmarksFaceForm = LandmarksWidget()
        self.storage = Storage()

        self.setupUi(self)

    def setupUi(self, main_window):
        icon = qta.icon("fa.picture-o")
        main_window.setWindowIcon(icon)
        main_window.setWindowTitle(tr("Photo Tagger"))
        self.central_widget = QWidget(main_window)
        self.central_layout = QHBoxLayout(self.central_widget)
        self.widgets_layout = QVBoxLayout()

        self.viewer = PhotoGrid(self.central_widget)
        self.viewer.setClickEvent(self.onActivePhotoClicked)
        self.viewer.setDoubleClickEvent(self.onActivePhotoDoubleClicked)
        self.viewer.setContextTagEvent(self.onContextMenuTagClicked)
        self.viewer.setContextLandmarksEvent(self.onContextMenuLandmarksClicked)
        self.viewer.setContexMovePhotosEvent(self.onContextMenuMovePhotosClicked)
        self.viewer.setContexCopyPhotosEvent(self.onContextMenuCopyPhotosClicked)
        self.widgets_layout.addWidget(self.viewer)

        self.progressBar = QProgressBar(self.central_widget)
        self.progressBar.setValue(0)
        self.progressBar.hide()
        self.widgets_layout.addWidget(self.progressBar)

        self.central_layout.addLayout(self.widgets_layout)

        main_window.setCentralWidget(self.central_widget)

        # Menu creation
        self.createMenus(main_window)
        self.appendFileRecents()

        # Statusbar creation
        self.statusbar = QStatusBar(main_window)
        main_window.setStatusBar(self.statusbar)

        QMetaObject.connectSlotsByName(main_window)
        self.galleryTaggingHandler.connect(self.taggingFaceForm.onFaceTaggerRequest)
        self.taggingFaceForm.taggerMessageHandler.connect(self.onCompareFaceMessage)

        self.galleryLandmarksHandler.connect(self.landmarksFaceForm.onFaceLandmarksRequest)

    def createMenus(self, main_window):
        self.menubar = QMenuBar(main_window)
        self.menuFile = QMenu(self.menubar)
        self.menuFile.setTitle(tr("File"))
        self.menubar.addAction(self.menuFile.menuAction())
        self.menuFile.addAction(self.actionGalleryOpen)
        self.menuRecents = QMenu(self.menuFile)
        self.menuRecents.setTitle(tr("Open Recents"))

        self.actionGalleryOpen.setToolTip(tr("Open Gallery"))
        self.actionGalleryOpen.setShortcut(tr("Ctrl+O"))

        self.menuFile.addMenu(self.menuRecents)
        main_window.setMenuBar(self.menubar)

    def appendFileRecents(self):
        recents = self.storage.fetchGalleries()
        for recent in recents:
            action = ActionRecents(self, recent[0])
            action.setCallback(self.startScanningThread)
            self.menuRecents.addAction(action)

    def logger(self, tag, message):
        self.statusbar.showMessage("{0} {1}".format(tag, message))

    def onActivePhotoClicked(self, event, photo):
        self.logger("Working image at: ", photo.tags())

    def onActivePhotoDoubleClicked(self, event, photo):
        pass

    def onContextMenuTagClicked(self, event, photo):
        self.galleryTaggingHandler.emit(photo)
        self.taggingFaceForm.show()

    def onContextMenuLandmarksClicked(self, event, photo):
        self.galleryLandmarksHandler.emit(photo)
        self.landmarksFaceForm.show()

    def onContextMenuMovePhotosClicked(self, event, known_photo):
        new_path = QFileDialog.getExistingDirectory(self, 'Choose new destination')
        if new_path:
            for photo in self.viewer.photos():
                if photo == known_photo:
                    photo.moveFile(new_path)

    def onContextMenuCopyPhotosClicked(self, event, known_photo):
        new_path = QFileDialog.getExistingDirectory(self, 'Choose new destination')
        if new_path:
            for photo in self.viewer.photos():
                if photo == known_photo:
                    photo.copyFile(new_path)

    def openPhotoGalleryFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open gallery')
        if folder:
            self.startScanningThread(folder)
            self.logger("Working gallery at: ", folder)

    def savePhotoTags(self, values):
        self.storage.updateAll(values)

    def onCompareFaceMessage(self, known_photo):
        for photo in self.viewer.photos():
            if compareFaces(known_photo.encodings(), photo.encodings()):
                photo.writeTags(self.savePhotoTags, known_photo.tags())
