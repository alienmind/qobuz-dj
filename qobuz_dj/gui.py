import os
import re
import sys

from PySide6.QtCore import QByteArray, QProcess, Qt
from PySide6.QtGui import QColor, QFont, QTextCharFormat, QTextCursor
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPlainTextEdit,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class ConsoleWidget(QPlainTextEdit):
    """
    A custom QPlainTextEdit that acts as a terminal console.
    """

    def __init__(self, parent=None):
        super().__init__(parent)
        self.setReadOnly(True)
        self.setBackgroundVisible(False)
        self.setStyleSheet("background-color: black; color: white;")
        self.setFont(QFont("Courier New", 10))

        # ANSI color regex
        self.ansi_regex = re.compile(r"\x1b\[([0-9;]*)m")

        self.color_map = {
            "30": QColor("black"),
            "31": QColor("red"),
            "32": QColor("green"),
            "33": QColor("yellow"),
            "34": QColor("blue"),
            "35": QColor("magenta"),
            "36": QColor("cyan"),
            "37": QColor("white"),
            "90": QColor("gray"),
            "91": QColor("lightred"),
            "92": QColor("lightgreen"),
            "93": QColor("lightyellow"),
            "94": QColor("lightblue"),
            "95": QColor("lightmagenta"),
            "96": QColor("lightcyan"),
            "97": QColor("white"),
        }

    def append_ansi(self, text):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.End)

        parts = self.ansi_regex.split(text)
        current_format = QTextCharFormat()

        for i, part in enumerate(parts):
            if i % 2 == 0:
                # Regular text
                if part:
                    cursor.insertText(part, current_format)
            else:
                # ANSI code
                codes = part.split(";")
                for code in codes:
                    if code == "0" or not code:
                        current_format = QTextCharFormat()
                    elif code in self.color_map:
                        current_format.setForeground(self.color_map[code])
                    elif code == "1":
                        current_format.setFontWeight(QFont.Bold)

        self.setTextCursor(cursor)
        self.ensureCursorVisible()

    def keyPressEvent(self, event):
        # Forward key events to the MainWindow's QProcess
        main_win = self.window()
        if hasattr(main_win, "send_input"):
            key = event.text()
            if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                key = "\n"

            if key:
                main_win.send_input(key)
        # We don't call super().keyPressEvent(event) to keep it read-only


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("qobuz-dj GUI")
        self.resize(900, 700)

        self.process = QProcess(self)
        self.process.setProcessChannelMode(QProcess.MergedChannels)
        self.process.readyReadStandardOutput.connect(self.read_output)

        self.init_ui()

    def init_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Mode Buttons
        mode_layout = QHBoxLayout()
        modes = [
            ("DJ Mode", "dj"),
            ("Download", "dl"),
            ("Sanitize", "sz"),
            ("Lucky", "lucky"),
            ("Interactive", "fun"),
        ]

        for name, cmd in modes:
            btn = QPushButton(name)
            btn.clicked.connect(lambda checked, c=cmd: self.run_command(c))
            mode_layout.addWidget(btn)

        main_layout.addLayout(mode_layout)

        # Input Field Layer
        input_layout = QHBoxLayout()
        input_layout.addWidget(QLabel("Source / Arguments:"))
        self.source_input = QLineEdit()
        self.source_input.setPlaceholderText("Enter URL, keywords, or folder path...")
        input_layout.addWidget(self.source_input)

        self.browse_btn = QPushButton("Browse Folder")
        self.browse_btn.clicked.connect(self.browse_folder)
        input_layout.addWidget(self.browse_btn)

        main_layout.addLayout(input_layout)

        # Console
        self.console = ConsoleWidget()
        main_layout.addWidget(self.console)

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Directory to Sanitize")
        if folder:
            self.source_input.setText(folder)

    def run_command(self, cmd):
        if self.process.state() != QProcess.NotRunning:
            self.console.append_ansi("\x1b[31mProcess already running...\x1b[0m\n")
            return

        args_text = self.source_input.text().strip()
        cli_args = [cmd]
        if args_text:
            # Simple split for multiple args, though URLs usually don't have spaces
            # For complex paths with spaces, we rely on QProcess handling list args correctly
            if cmd == "sz":
                cli_args.append(args_text)
            else:
                # For lucky or dl, might be multiple URLs or keywords
                cli_args.extend(args_text.split())

        self.console.append_ansi(
            f"\x1b[32mRunning: qobuz-dj {' '.join(cli_args)}\x1b[0m\n"
        )

        if getattr(sys, "frozen", False):
            program = os.path.join(os.path.dirname(sys.executable), "qobuz-dj")
            if os.name == "nt":
                program += ".exe"
            # Fallback for dev if not found
            if not os.path.exists(program):
                program = "qobuz-dj"
        else:
            program = "uv"
            cli_args = ["run", "qobuz-dj"] + cli_args

        self.process.start(program, cli_args)

    def read_output(self):
        data = self.process.readAllStandardOutput()
        text = str(QByteArray(data), "utf-8", errors="replace")
        self.console.append_ansi(text)

    def send_input(self, text):
        if self.process.state() == QProcess.Running:
            self.process.write(text.encode("utf-8"))


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
