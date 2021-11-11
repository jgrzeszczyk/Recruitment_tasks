from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.QtCore import QThread


class Worker(QObject):
    def __init__(self, func, **kwargs):
        super().__init__()
        self.func = func
        self.func_kwargs = kwargs

    finished = pyqtSignal()

    def run(self):
        """Long-running task."""
        self.func(self.func_kwargs)
        self.finished.emit()


class CustomThread:
    def __init__(self, worker):
        self.thread = QThread()
        self.worker = worker

    def run_task(self):
        """Threading to avoid GUI freezing"""
        # Move worker to the thread
        self.worker.moveToThread(self.thread)
        # Connect signals and slots
        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        # Start the thread
        self.thread.start()