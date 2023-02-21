from abc import abstractmethod

from ScanWorker import ScanWorker


class PhotoScanner:

    def __init__(self):
        self.threadpool = None
        self.progressBar = None

    def startScanningThread(self, folder):
        worker = ScanWorker(self.executeScanningWork, folder)
        worker.signals.result.connect(self.scanningDone)
        worker.signals.finished.connect(self.scanningComplete)
        worker.signals.progress.connect(self.trackScanningProgress)
        self.progressBar.show()
        self.progressBar.setValue(0)
        self.threadpool.start(worker)

    @abstractmethod
    def executeScanningWork(self, folder, progress_callback):
        pass

    @abstractmethod
    def logger(self, param, progress):
        pass

    @abstractmethod
    def trackScanningProgress(self, progress):
        pass

    @abstractmethod
    def scanningDone(self, folder):
        pass

    @abstractmethod
    def scanningComplete(self):
        pass
