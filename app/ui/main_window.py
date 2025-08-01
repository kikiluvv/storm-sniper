from PyQt5.QtWidgets import QMainWindow, QFileDialog, QMessageBox
from app.ui.components import setup_ui
from app.workers.fuzz_worker import ScanThread
import datetime, os, re
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StormSniper 🌪️🎯")
        self.setGeometry(900, 600, 900, 600)
        setup_ui(self)
        self.last_storm_urls = []
        self._session_logs = []
        self._session_output = []
        font = QFont("System")  
        self.log_box.setFont(font)
        self.output.setFont(font)
        self.log_box.textChanged.connect(self.buffer_logs)
        self.output.textChanged.connect(self.buffer_output)
        self.upload_button.clicked.connect(self.load_urls)
        self.run_button.clicked.connect(self.run_scan)
        self.snipe_button.clicked.connect(self.snipe_these_urls)
        self.save_logs_button.clicked.connect(self.save_logs_to_file)
        self.save_log_toggle.stateChanged.connect(self.toggle_save_logs_button)

    def buffer_logs(self):
        if self.save_log_toggle.isChecked():
            self._session_logs = self.log_box.toPlainText().splitlines()
        else:
            self._session_logs = []

    def buffer_output(self):
        if self.save_log_toggle.isChecked():
            self._session_output = self.output.toPlainText().splitlines()
        else:
            self._session_output = []

    def load_urls(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open URL File", "", "Text Files (*.txt)")
        if file_path:
            with open(file_path, 'r') as f:
                lines = [line.strip() for line in f if line.strip()]
                self.url_input.setText("\n".join(lines))

    def run_scan(self):
        mode = self.mode_selector.currentText()
        urls = [line.strip() for line in self.url_input.toPlainText().splitlines() if line.strip()]
        if not urls:
            self.output.append("no urls provided :3")
            return

        self.last_storm_urls = []

        self.output.append(f"🌀 running scan in {mode} mode on {len(urls)} urls...\n")

        self.scan_thread = ScanThread(mode, urls)
        self.scan_thread.log.connect(self.log_box.append)
        self.scan_thread.output.connect(self.handle_output)
        self.scan_thread.start()

        self.snipe_button.setEnabled(False)

    def handle_output(self, text):
        self.output.append(text)
        self.log_box.append(text)

        if "potential vuln" in text.lower():
            self.snipe_button.setEnabled(True)

        for line in text.strip().splitlines():
            urls = re.findall(r'https?://[^\s]+', line)
            for url in urls:
                self.last_storm_urls.append(url)


    def snipe_these_urls(self):
        if not self.last_storm_urls:
            self.output.append("⚠️ no storm urls found to snipe :3")
            return

        self.mode_selector.setCurrentText("Snipe")
        self.url_input.setText("\n".join(self.last_storm_urls))
        self.output.append(f"🌀 loaded {len(self.last_storm_urls)} urls from storm results for snipe mode.\n")
        self.snipe_button.setEnabled(False)
        self.run_scan()

    def save_logs_to_file(self):
        now = datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"stormsniper-log-{now}.txt"
        folder = QFileDialog.getExistingDirectory(self, "select folder to save log, uwu")
        if not folder:
            self.output.append("⚠️ save cancelled, owo")
            return

        full_path = os.path.join(folder, filename)
        with open(full_path, "w", encoding="utf-8") as f:
            f.write("=== stormsniper scan log ===\n\n")
            f.write("📝 Log:\n")
            f.write("\n".join(self._session_logs))
            f.write("\n\n📜 Output:\n")
            f.write("\n".join(self._session_output))
        self.output.append(f"💾 log saved to {full_path} owo~")

    def toggle_save_logs_button(self, state):
        self.save_logs_button.setEnabled(state == 2)

    def closeEvent(self, event):
        if self.save_log_toggle.isChecked():
            reply = QMessageBox.question(
                self, "Save Logs?",
                "You have log saving enabled. Do you want to dump the logs before exiting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )
            if reply == QMessageBox.Yes:
                self.save_logs_to_file()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()
