from PySide6.QtCore import (QCoreApplication, QMetaObject, Signal, QThreadPool)
from PySide6.QtWidgets import (QHBoxLayout, QMenuBar,
                               QProgressBar, QStatusBar,
                               QVBoxLayout, QWidget, QMainWindow, QMenu, QFileDialog)

from Actions import ActionRecents, Action
from FaceTagger import compareFaces
from PhotoScanner import PhotoScanner
from Reopen import Reopen
from UI.TaggerWidget import TaggerWidget
from UI.widgets.PhotoGrid import PhotoGrid


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


class MainWindow(QMainWindow, PhotoScanner):
    taggerHandler = Signal(object)

    def __init__(self):
        super().__init__()
        self.reopen = None
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
        self.reopen = Reopen()

        self.setupUi(self)

    def setupUi(self, main_window):
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
        self.taggerHandler.connect(self.taggingFaceForm.onFaceTaggerRequest)
        self.taggingFaceForm.taggerHandler.connect(self.onCompareFaceMessage)

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
        recents = self.reopen.fetchRecents()
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
        self.taggerHandler.emit(photo)
        self.taggingFaceForm.show()

    def onContextMenuLandmarksClicked(self, event, photo):
        big_photo = photo.getOriginalPhoto()
        big_photo.drawFaceLandmarks()
        self.taggerHandler.emit(big_photo)
        self.taggingFaceForm.show()

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
            self.reopen.appendRecents(folder)
            self.startScanningThread(folder)
            self.logger("Working gallery at: ", folder)

    def onCompareFaceMessage(self, known_photo):
        for photo in self.viewer.photos():
            if compareFaces(known_photo.encodings(), photo.encodings()):
                photo.setTags(known_photo.tags())
                photo.saveTags(known_photo.tags())
