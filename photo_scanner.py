from abc import abstractmethod

from face_tagger import getMetadata
from file_filter import FileFilter
from scan_worker import ScanWorker


class PhotoScanner:

    def __init__(self):
        self.storage = None
        self.viewer = None
        self.threadpool = None
        self.progressBar = None

    def startScanningThread(self, folder):
        worker = ScanWorker(self.executeScanningWork, folder)
        worker.signals.result.connect(self.scanningDone)
        worker.signals.finished.connect(self.scanningComplete)
        worker.signals.progress.connect(self.trackScanningProgress)
        self.progressBar.setValue(0)
        self.threadpool.start(worker)

    def executeScanningWork(self, folder, progress_callback):
        self.progressBar.show()
        if not self.storage.exists(folder):
            imageList = FileFilter(folder)
            for image in imageList():
                metadata = getMetadata(image["path"])
                if metadata:
                    imageList.append(image, metadata)
                    progress_callback.emit(imageList.progress())
            metadataList = imageList.metadataList()
            self.storage.saveGallery(folder, metadataList)
            return metadataList
        else:
            return self.storage.fetchAllFaces(folder)

    def trackScanningProgress(self, progress):
        self.progressBar.setValue(progress)
        self.logger("Scanning gallery progress: ", progress)

    def scanningDone(self, metadata):
        self.logger("encode ", " done")
        self.viewer.drawPhotos(metadata)

    def scanningComplete(self):
        self.progressBar.hide()
        self.logger("Scanning complete ", "Done")

    @abstractmethod
    def logger(self, param, progress):
        pass
