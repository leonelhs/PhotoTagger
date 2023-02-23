from abc import abstractmethod

from FaceTagger import getMetadata
from FileFilter import FileFilter
from ScanWorker import ScanWorker


class PhotoScanner:

    def __init__(self):
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
        imageList = FileFilter(folder)
        for image in imageList():
            metadata = getMetadata(image["path"])
            if metadata:
                imageList.append(image, metadata)
                progress_callback.emit(imageList.progress())
        return imageList.metadataList()

    def trackScanningProgress(self, progress):
        self.progressBar.setValue(progress)
        self.logger("Scanning gallery completed: ", progress)

    def scanningDone(self, metadata):
        self.logger("encode ", " done")
        self.viewer.drawPhotos(metadata)

    def scanningComplete(self):
        self.progressBar.hide()
        self.logger("Scanning complete ", "Done")

    @abstractmethod
    def logger(self, param, progress):
        pass
