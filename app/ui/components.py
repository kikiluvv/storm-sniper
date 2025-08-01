from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QLabel, QPushButton, QTextEdit,
    QComboBox, QHBoxLayout, QCheckBox, QFrame
)
from PyQt5.QtCore import Qt

def setup_ui(self):
    self.setStyleSheet("""
        QWidget {
            background-color: #1e1e1e;
            color: #d4d4d4;
            font-family: 'Segoe UI', sans-serif;
            font-size: 10pt;
        }

        QLabel {
            color: #dcdcdc;
        }

        QComboBox, QTextEdit, QLineEdit {
            background-color: #2d2d2d;
            color: #ffffff;
            border: 1px solid #3c3c3c;
            border-radius: 6px;
            padding: 6px;
        }

        QComboBox QAbstractItemView {
            background-color: #252526;
            color: #ffffff;
            selection-background-color: #007acc;
        }

        QPushButton {
            background-color: #007acc;
            color: #ffffff;
            border: none;
            border-radius: 6px;
            padding: 8px;
        }

        QPushButton:hover {
            background-color: #005f9e;
        }

        QPushButton:disabled {
            background-color: #333333;
            color: #888888;
        }

        QCheckBox {
            padding: 4px;
        }

        QFrame {
            background-color: #1e1e1e;
        }
    """)

    self.central_widget = QWidget()
    self.setCentralWidget(self.central_widget)

    main_layout = QVBoxLayout()
    main_layout.setSpacing(12)
    main_layout.setContentsMargins(20, 20, 20, 20)
    self.central_widget.setLayout(main_layout)

    # 🧠 Title
    title = QLabel("StormSniper v0.0.2")
    title.setAlignment(Qt.AlignCenter)
    title.setStyleSheet("font-size: 16pt; font-weight: bold; margin-bottom: 12px;")
    main_layout.addWidget(title)

    # 🔧 Mode selection
    mode_row = QHBoxLayout()
    mode_label = QLabel("Mode:")
    self.mode_selector = QComboBox()
    self.mode_selector.addItems(["Storm", "Snipe"])
    mode_row.addWidget(mode_label)
    mode_row.addWidget(self.mode_selector)
    main_layout.addLayout(mode_row)

    # 🌐 URL input with load button on same line
    url_input_label_row = QHBoxLayout()
    url_label = QLabel("Target URL(s):")
    self.upload_button = QPushButton("Load URL List")
    url_input_label_row.addWidget(url_label)
    url_input_label_row.addStretch()
    url_input_label_row.addWidget(self.upload_button)
    main_layout.addLayout(url_input_label_row)

    self.url_input = QTextEdit()
    main_layout.addWidget(self.url_input)

    # 🚀 Action Buttons side-by-side and centered
    action_buttons_row = QHBoxLayout()
    self.run_button = QPushButton("Initiate Scan")
    self.snipe_button = QPushButton("Snipe Vulnerables")
    self.snipe_button.setEnabled(False)
    action_buttons_row.addStretch()
    action_buttons_row.addWidget(self.run_button)
    action_buttons_row.addWidget(self.snipe_button)
    action_buttons_row.addStretch()
    main_layout.addLayout(action_buttons_row)

    # 🧾 Logging controls
    save_layout = QVBoxLayout()
    self.save_log_toggle = QCheckBox("Enable Logging")
    
    button_row = QHBoxLayout()
    self.save_logs_button = QPushButton("Dump Logs")
    self.save_logs_button.setEnabled(False)
    button_row.addWidget(self.save_logs_button)
    button_row.addStretch()  
     
    save_layout.addWidget(self.save_log_toggle)
    save_layout.addLayout(button_row)
    main_layout.addLayout(save_layout)

    # ─ Divider line
    divider = QFrame()
    divider.setFrameShape(QFrame.HLine)
    divider.setFrameShadow(QFrame.Sunken)
    divider.setStyleSheet("margin-top: 12px; margin-bottom: 12px; border-top: 1px solid #3c3c3c;")
    main_layout.addWidget(divider)

    # 🖥️ Output / Log side-by-side
    output_log_layout = QHBoxLayout()
    main_layout.addLayout(output_log_layout)

    # ✉️ Output Summary 
    output_layout = QVBoxLayout()
    output_label = QLabel("Output Summary:")
    output_layout.addWidget(output_label)

    self.output = QTextEdit()
    self.output.setReadOnly(True)
    output_layout.addWidget(self.output)
    output_log_layout.addLayout(output_layout, 2)

    # 📜 Log 
    log_layout = QVBoxLayout()
    log_label = QLabel("Log:")
    log_layout.addWidget(log_label)

    self.log_box = QTextEdit()
    self.log_box.setReadOnly(True)
    log_layout.addWidget(self.log_box)
    output_log_layout.addLayout(log_layout, 1)
