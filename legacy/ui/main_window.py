from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QPushButton, QTextEdit, QFileDialog, QComboBox, QHBoxLayout, QCheckBox
)
from app.core.scanner import storm_mode, snipe_mode
from PyQt5.QtCore import QThread, pyqtSignal
from PyQt5.QtWidgets import QMessageBox
import re
import datetime
import os

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
            results = storm_mode(self.urls, log_callback=self.log.emit)
            if not results:
                self.log.emit("🔍 No obvious redirection found.")
                self.output.emit("❌ No vulns found while storming.")
            else:
                for url, payload in results:
                    self.log.emit(f"⚠️ Potential vuln: {url} with payload `{payload}`")
                vuln_urls = list(set(url for url, _ in results))
                vuln_urls_str = "\n".join(vuln_urls)
                self.output.emit("💡 Potential vulns found on these URLs:")
                self.output.emit(vuln_urls_str)
                self.output.emit("💡 Run Snipe mode on these URLs to confirm details.")
        elif self.mode == "Snipe":
            results = snipe_mode(self.urls, log_callback=self.log.emit)
            if not results:
                self.log.emit("🔎 No confirmed vulns found.")
                self.output.emit("❌ No confirmed vulns found in snipe mode.")
            else:
                for url, payload, loc in results:
                    self.output.emit(f"🎯 Confirmed vuln: {url} -> `{loc}` via `{payload}`")
        self.log.emit("✅ Scan finished.\n")

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("StormSniper 🌪️🎯")
        self.setGeometry(900, 600, 900, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        main_layout = QVBoxLayout()
        self.central_widget.setLayout(main_layout)

        # Mode Selector
        self.mode_selector = QComboBox()
        self.mode_selector.addItems(["Storm", "Snipe"])
        main_layout.addWidget(QLabel("Select Mode:"))
        main_layout.addWidget(self.mode_selector)

        # URL Input
        main_layout.addWidget(QLabel("Enter URLs (one per line):"))
        self.url_input = QTextEdit()
        main_layout.addWidget(self.url_input)

        # Upload Button
        self.upload_button = QPushButton("📂 Load URLs from .txt")
        self.upload_button.clicked.connect(self.load_urls)
        main_layout.addWidget(self.upload_button)

        # Run Button
        self.run_button = QPushButton("🚀 Run Scan")
        self.run_button.clicked.connect(self.run_scan)
        main_layout.addWidget(self.run_button)

        # Snipe These URLs Button
        self.snipe_button = QPushButton("🎯 Snipe Vulnerable URLs")
        self.snipe_button.clicked.connect(self.snipe_these_urls)
        self.snipe_button.setEnabled(False)
        main_layout.addWidget(self.snipe_button)

        # Save Log Toggle & Save Button
        save_layout = QHBoxLayout()
        self.save_log_toggle = QCheckBox("💾 Enable Log Saving")
        save_layout.addWidget(self.save_log_toggle)

        self.save_logs_button = QPushButton("💾 Save Logs Now")
        self.save_logs_button.clicked.connect(self.save_logs_to_file)
        save_layout.addWidget(self.save_logs_button)
        self.save_logs_button.setText("💾 Dump Logs")
        self.save_logs_button.setEnabled(False)  # start disabled

        # connect toggle to enabling/disabling dump button
        self.save_log_toggle.stateChanged.connect(self.toggle_save_logs_button)


        main_layout.addLayout(save_layout)

        # Horizontal layout for Output and Log
        output_log_layout = QHBoxLayout()
        main_layout.addLayout(output_log_layout)

        # Output Area
        output_layout = QVBoxLayout()
        output_layout.addWidget(QLabel("📜 Output:"))
        self.output = QTextEdit()
        self.output.setReadOnly(True)
        output_layout.addWidget(self.output)
        output_log_layout.addLayout(output_layout, 2)

        # Log Area
        log_layout = QVBoxLayout()
        log_layout.addWidget(QLabel("📝 Log:"))
        self.log_box = QTextEdit()
        self.log_box.setReadOnly(True)
        log_layout.addWidget(self.log_box)
        output_log_layout.addLayout(log_layout, 1)

        # Store last storm results URLs here
        self.last_storm_urls = []

        # Buffers to store session logs if saving is enabled
        self._session_logs = []
        self._session_output = []

        # Connect log and output appenders to buffer
        self.log_box.textChanged.connect(self.buffer_logs)
        self.output.textChanged.connect(self.buffer_output)

    def buffer_logs(self):
        if self.save_log_toggle.isChecked():
            text = self.log_box.toPlainText()
            self._session_logs = text.splitlines()
        else:
            self._session_logs = []

    def buffer_output(self):
        if self.save_log_toggle.isChecked():
            text = self.output.toPlainText()
            self._session_output = text.splitlines()
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
            self.output.append("⚠️ no urls provided :3")
            return

        self.output.append(f"▶️ running scan in {mode} mode on {len(urls)} urls...\n")

        self.scan_thread = ScanThread(mode, urls)
        self.scan_thread.log.connect(self.log_box.append)      
        self.scan_thread.output.connect(self.handle_output)    
        self.scan_thread.start()
        self.snipe_button.setEnabled(False)

    def handle_output(self, text):
        self.output.append(text)

        if text.startswith("💡 Potential vulns found on these URLs:"):
            self.last_storm_urls = []
            self.snipe_button.setEnabled(True)
            return

        if not self.snipe_button.isEnabled():
            return

        if text.startswith("💡 Run Snipe mode"):
            return

        line = text.strip()
        url_pattern = re.compile(
            r'^(https?://(?:[a-zA-Z0-9\-._~:/?#@!$&\'()*+,;=%]+))$'
        )

        if line and url_pattern.match(line):
            self.last_storm_urls.append(line)

    def snipe_these_urls(self):
        if not self.last_storm_urls:
            self.output.append("⚠️ no storm urls found to snipe :3")
            return

        self.mode_selector.setCurrentText("Snipe")
        self.url_input.setText("\n".join(self.last_storm_urls))
        self.output.append(f"▶️ loaded {len(self.last_storm_urls)} urls from storm results for snipe mode.\n")
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
        enabled = state == 2  # 2 means checked in Qt
        self.save_logs_button.setEnabled(enabled)
    
    def closeEvent(self, event):
        if self.save_log_toggle.isChecked():
            reply = QMessageBox.question(
                self,
                "Save Logs?",
                "You have log saving enabled. Do you want to dump the logs before exiting?",
                QMessageBox.Yes | QMessageBox.No | QMessageBox.Cancel,
                QMessageBox.Yes
            )

            if reply == QMessageBox.Yes:
                self.save_logs_to_file()
                event.accept()
            elif reply == QMessageBox.No:
                event.accept()
            else:  # Cancel
                event.ignore()
        else:
            event.accept()


