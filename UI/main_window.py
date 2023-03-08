import os.path

import qtawesome as qta
from PySide6.QtCore import (QCoreApplication, QMetaObject, Signal, QThreadPool)
from PySide6.QtWidgets import (QHBoxLayout, QMenuBar,
                               QProgressBar, QStatusBar,
                               QVBoxLayout, QWidget, QMainWindow, QMenu, QFileDialog)

from UI.landmarks_widget import LandmarksWidget
from UI.tagger_widget import TaggerWidget
from UI.widgets.photo_grid import PhotoGrid
from actions import ActionRecents, Action
from face_tagger import compareFaces
from photo_scanner import PhotoScanner
from storage import Storage


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


class MainWindow(QMainWindow, PhotoScanner):
    galleryTaggingHandler = Signal(object)
    galleryLandmarksHandler = Signal(object)

    def __init__(self):
        super().__init__()
        self.menuFaces = None
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

        self.actionShowFacesCropped = Action(self, "Show faces cropped", "mdi.face-recognition")
        self.actionSaveFacesCropped = Action(self, "Export faces cropped", "fa.save")
        self.actionReloadAllFaces = Action(self, "Reload faces gallery", "mdi.reload")

        self.actionShowFacesCropped.setOnClickEvent(self.onShowFacesCropped)
        self.actionSaveFacesCropped.setOnClickEvent(self.onSaveFacesCropped)
        self.actionReloadAllFaces.setOnClickEvent(self.onReloadAllFaces)

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
        self.viewer.setContexCropFacesEvent(self.onContextMenuCropFacesClicked)
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

        self.menuFaces = QMenu(self.menubar)
        self.menuFaces.setTitle(tr("Faces"))
        self.menubar.addAction(self.menuFaces.menuAction())
        self.menuFaces.addAction(self.actionShowFacesCropped)
        self.menuFaces.addAction(self.actionSaveFacesCropped)
        self.menuFaces.addAction(self.actionReloadAllFaces)

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

    def showMessage(self, message):
        self.statusbar.showMessage(message)

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

        def updatePath(file, folder, new_folder):
            self.storage.updateFolderPath((new_folder, folder, file))

        new_path = QFileDialog.getExistingDirectory(self, 'Choose new folder destination')
        if new_path:
            for photo in self.viewer.photos():
                if photo == known_photo:
                    photo.moveFile(updatePath, new_path)

    def onContextMenuCropFacesClicked(self, event, known_photo):
        pass

    def onShowFacesCropped(self):
        for photo in self.viewer.photos():
            thumb = photo.cropFace()
            if thumb:
                thumb = thumb.scaled(128, 128)
                photo.setPixmap(thumb)

    def onSaveFacesCropped(self):
        new_folder = QFileDialog.getExistingDirectory(self, 'Choose photo set destination')
        if new_folder:
            for photo in self.viewer.photos():
                new_path = os.path.join(new_folder, photo.fileName())
                face = photo.cropFace()
                if face:
                    print(face.width())
                    if face.width() >= 180:
                        face.scaled(256, 256).save(new_path)

    def onReloadAllFaces(self):
        pass

    def openPhotoGalleryFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open gallery')
        if folder:
            self.startScanningThread(folder)
            self.logger("Working gallery at: ", folder)

    def onCompareFaceMessage(self, known_photo):

        def updatePhotoTags(tags, folder, file):
            self.storage.updateAllTags((tags, folder, file))

        matches = []
        for photo in self.viewer.photos():
            if compareFaces(known_photo.encodings(), photo.encodings()):
                matches.append(photo)

        for photo in matches:
            photo.writeTags(updatePhotoTags, known_photo.tags())

        self.logger("Total faces matches ", str(len(matches)))
