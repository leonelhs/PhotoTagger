import shutil

from PySide6.QtCore import (QCoreApplication, QMetaObject, Signal, QThreadPool)
from PySide6.QtGui import QPainter, QColor
from PySide6.QtWidgets import (QHBoxLayout, QMenuBar,
                               QProgressBar, QStatusBar,
                               QVBoxLayout, QWidget, QMainWindow, QMenu, QFileDialog)

from tagger import compareFaces, processMetadata
from FileFilter import FileFilter
from Actions import ActionRecents, Action
from PhotoScanner import PhotoScanner
from Storage import Storage
from UI.Tagging import Tagging
from UI.widgets.PhotoGrid import PhotoGrid


def get_line(array):
    for i in range(0, len(array), 2):
        yield array[i:i + 2]


def tr(label):
    return QCoreApplication.translate("MainWindow", label, None)


def drawFaceLandmarks(face):
    painter = QPainter(face.__thumbnail)
    painter.setPen(QColor(255, 255, 0))
    for marks in face.__landmarks:
        for positions in marks:
            for position in get_line(marks[positions]):
                if len(position) > 1:
                    painter.drawLine(*position[0], *position[1])


class MainWindow(QMainWindow, PhotoScanner):
    galleryHandler = Signal(object)

    def __init__(self):
        super().__init__()
        self.storage = None
        self.menuRecents = None
        self.menuGallery = None
        self.menuFile = None
        self.thumbnailGrid = None
        self.statusbar = None
        self.menubar = None
        self.progressBar = None
        self.widgets_layout = None
        self.central_layout = None
        self.central_widget = None

        self.actionGalleryOpen = Action(self, "Open Gallery", "fa.folder-open")
        self.actionGalleryOpen.setOnClickEvent(self.openGalleryFolder)

        self.threadpool = QThreadPool()

        self.tagFaceForm = Tagging()
        self.storage = Storage()

        self.setupUi(self)

    def setupUi(self, main_window):
        main_window.setWindowTitle(tr("Photo Tagger"))
        self.central_widget = QWidget(main_window)
        self.central_layout = QHBoxLayout(self.central_widget)
        self.widgets_layout = QVBoxLayout()

        self.thumbnailGrid = PhotoGrid(self.central_widget)
        self.thumbnailGrid.setClickEvent(self.onActivePhotoClicked)
        self.thumbnailGrid.setDoubleClickEvent(self.onActivePhotoDoubleClicked)
        self.thumbnailGrid.setContextTagEvent(self.onContextMenuTagClicked)
        self.thumbnailGrid.setContextLandmarksEvent(self.onContextMenuLandmarksClicked)
        self.thumbnailGrid.setContextNewGalleryEvent(self.onContextMenuNewGalleryClicked)
        self.widgets_layout.addWidget(self.thumbnailGrid)

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
        self.galleryHandler.connect(self.tagFaceForm.onGalleryHandlerMessage)
        self.tagFaceForm.taggerHandler.connect(self.onTaggerHandlerMessage)

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

    def populateThumbnails(self, folder):
        if self.storage.exists(folder):
            face_list = self.storage.fetchAllFaces(folder)
            self.thumbnailGrid.populate_grid(face_list)
            return True
        return False

    def appendFileRecents(self):
        recents = self.storage.fetchGalleries()
        for recent in recents:
            action = ActionRecents(self, recent[0])
            action.setCallback(self.populateThumbnails)
            self.menuRecents.addAction(action)

    def logger(self, tag, message):
        self.statusbar.showMessage("{0} {1}".format(tag, message))

    def onActivePhotoClicked(self, event, face):
        self.logger("Working image at: ", face.tags)

    def onActivePhotoDoubleClicked(self, event, face):
        pass

    def onContextMenuTagClicked(self, event, face):
        self.galleryHandler.emit(face)
        self.tagFaceForm.show()

    def onContextMenuLandmarksClicked(self, event, face):
        image = tagger.imageOpen(face.path)
        face.__thumbnail = image.toqpixmap()
        drawFaceLandmarks(face)
        self.galleryHandler.emit(face)
        self.tagFaceForm.show()

    def onContextMenuNewGalleryClicked(self, event, face):
        tagged_list = []
        new_gallery_path = QFileDialog.getExistingDirectory(self, 'Open gallery')
        if new_gallery_path:
            for tagged_face in self.storage.fetchAllFaces():
                if tagged_face.tags == face.tags:
                    tagged_list.append(tagged_face)
            for tagged_face in tagged_list:
                shutil.move(tagged_face.__file, new_gallery_path)

    def openGalleryFolder(self):
        folder = QFileDialog.getExistingDirectory(self, 'Open gallery')
        if folder:
            if not self.populateThumbnails(folder):
                self.startScanningThread(folder)
            self.logger("Working gallery at: ", folder)

    def onTaggerHandlerMessage(self, known_face):
        tagged = []
        for unknown_face in self.storage.fetchAllFaces(known_face.folder):
            if compareFaces(known_face.__encodings, unknown_face.__encodings):
                unknown_face.tags = known_face.tags
                tagged.append(unknown_face)
        self.thumbnailGrid.populate_grid(tagged)
        to_tag = [(face.tags, face.folder, face.file) for face in tagged]
        self.storage.updateAll(to_tag)

    def executeScanningWork(self, folder, progress_callback):
        imageList = FileFilter(folder)
        for image in imageList():
            metadata = processMetadata(image.pop("path"))
            imageList.append(image, metadata)
            progress_callback.emit(imageList.progress())
        self.storage.saveGallery(folder, imageList.values())
        return folder

    def trackScanningProgress(self, progress):
        self.progressBar.setValue(progress)
        self.logger("Scanning gallery completed: ", progress)

    def scanningDone(self, folder):
        self.logger("encode ", " done")
        self.populateThumbnails(folder)

    def scanningComplete(self):
        self.progressBar.hide()
        self.logger("Scanning complete ", "Done")