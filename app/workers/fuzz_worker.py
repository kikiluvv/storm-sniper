from PyQt5.QtCore import QThread, pyqtSignal
from app.core.storm import storm_mode
from app.core.snipe import snipe_mode

class ScanThread(QThread):
    log = pyqtSignal(str)
    output = pyqtSignal(str)

    def __init__(self, mode, urls):
        super().__init__()
        self.mode = mode
        self.urls = urls

    def run(self):
        self.log.emit(f"🌀 Starting scan in {self.mode} mode...")
        if self.mode == "Storm":
            results, summary = storm_mode(self.urls, log_callback=self.log.emit)
            self.output.emit(summary)
        elif self.mode == "Snipe":
            results, summary = snipe_mode(self.urls, log_callback=self.log.emit)
            self.output.emit(summary)
        self.log.emit("✅ Scan finished.\n")


