"""Main window with file list, progress bar, and compression worker."""

import os

# Minimum imports for class definitions — the rest are lazy-imported
# inside functions to avoid triggering Qt DLL loading during module import.
from PySide6.QtCore import QThread, Signal, QObject
from PySide6.QtWidgets import QMainWindow

from compressor import compress_png, resolve_output_path, format_size
from settings import load_settings


STATUS_PENDING = "等待中"
STATUS_WORKING = "处理中..."
STATUS_OK = "完成"
STATUS_FAIL = "失败"


class CompressWorker(QObject):
    """Runs compression in a background thread, emitting signals per file."""

    file_done = Signal(int, object)  # index, result dict
    all_done = Signal()

    def __init__(self, files: list, settings: dict):
        super().__init__()
        self.files = files
        self.settings = settings

    def run(self):
        for i, filepath in enumerate(self.files):
            if not os.path.isfile(filepath):
                self.file_done.emit(
                    i,
                    {
                        "success": False,
                        "original_size": 0,
                        "compressed_size": 0,
                        "error": "文件不存在",
                        "output_path": "",
                    },
                )
                continue

            output_path = resolve_output_path(filepath, self.settings)

            result = compress_png(
                filepath,
                output_path,
                quality_min=self.settings["quality_min"],
                quality_max=self.settings["quality_max"],
                preserve_date=self.settings.get("preserve_date", True),
            )
            result["output_path"] = output_path
            self.file_done.emit(i, result)

        self.all_done.emit()


class MainWindow(QMainWindow):
    def __init__(self, files: list, icon=None):
        super().__init__()
        self.files = files
        self.settings = load_settings()
        self.results = [None] * len(files)
        self._running = True
        if icon:
            self.setWindowIcon(icon)
        self._setup_ui()
        self._start_compression()

    def _setup_ui(self):
        from PySide6.QtWidgets import (
            QWidget, QVBoxLayout, QHBoxLayout, QTableWidget,
            QTableWidgetItem, QProgressBar, QLabel, QPushButton,
            QHeaderView, QAbstractItemView,
        )
        from PySide6.QtGui import QFont

        self.setWindowTitle("PngTiny")
        self.resize(780, 500)

        # Center on screen
        screen = self.screen().availableGeometry()
        self.move(
            (screen.width() - self.width()) // 2,
            (screen.height() - self.height()) // 2,
        )

        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(12)

        # --- Header ---
        header_layout = QHBoxLayout()
        title = QLabel("PngTiny")
        title_font = QFont()
        title_font.setPointSize(14)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)

        header_layout.addStretch()

        btn_settings = QPushButton("设置")
        btn_settings.setFixedWidth(80)
        btn_settings.clicked.connect(self._open_settings)
        header_layout.addWidget(btn_settings)
        layout.addLayout(header_layout)

        # --- File table ---
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["文件名", "状态", "原大小", "压缩后"])
        self.table.setRowCount(len(self.files))
        self.table.setSelectionMode(QAbstractItemView.NoSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.table.verticalHeader().setVisible(False)

        header = self.table.horizontalHeader()
        header.setStretchLastSection(False)
        header.setSectionResizeMode(0, QHeaderView.Stretch)
        header.setSectionResizeMode(1, QHeaderView.Fixed)
        header.setSectionResizeMode(2, QHeaderView.Fixed)
        header.setSectionResizeMode(3, QHeaderView.Fixed)
        self.table.setColumnWidth(1, 90)
        self.table.setColumnWidth(2, 110)
        self.table.setColumnWidth(3, 130)

        # Populate filenames and set pending status
        for i, fp in enumerate(self.files):
            name_item = QTableWidgetItem(os.path.basename(fp))
            name_item.setToolTip(fp)
            self.table.setItem(i, 0, name_item)
            self.table.setItem(i, 1, QTableWidgetItem(STATUS_PENDING))

        layout.addWidget(self.table)

        # --- Progress bar ---
        self.progress_bar = QProgressBar()
        self.progress_bar.setMaximum(len(self.files))
        self.progress_bar.setValue(0)
        self.progress_bar.setTextVisible(True)
        self.progress_bar.setFormat("%v / %m")
        layout.addWidget(self.progress_bar)

        # --- Stats ---
        stats_layout = QHBoxLayout()
        self.stats_label = QLabel("准备中...")
        stats_layout.addWidget(self.stats_label)
        stats_layout.addStretch()

        self.close_btn = QPushButton("关闭")
        self.close_btn.setFixedWidth(80)
        self.close_btn.setEnabled(False)
        self.close_btn.clicked.connect(self.close)
        stats_layout.addWidget(self.close_btn)
        layout.addLayout(stats_layout)

    def _start_compression(self):
        self.thread = QThread()
        self.worker = CompressWorker(self.files, self.settings)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.file_done.connect(self._on_file_done)
        self.worker.all_done.connect(self._on_all_done)
        self.worker.all_done.connect(self.thread.quit)
        self.worker.all_done.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_file_done(self, index: int, result: dict):
        from PySide6.QtWidgets import QTableWidgetItem
        from PySide6.QtGui import QColor

        self.results[index] = result

        # Update status column
        if result["success"]:
            status_item = QTableWidgetItem(STATUS_OK)
            status_item.setForeground(QColor("#27ae60"))
        else:
            status_item = QTableWidgetItem(STATUS_FAIL)
            status_item.setForeground(QColor("#e74c3c"))
            status_item.setToolTip(result.get("error", ""))
        self.table.setItem(index, 1, status_item)

        # Original size
        self.table.setItem(
            index, 2, QTableWidgetItem(format_size(result["original_size"]))
        )

        # Compressed size + ratio
        if result["success"]:
            saved = result["original_size"] - result["compressed_size"]
            ratio = (saved / result["original_size"]) * 100
            detail = (
                f"{format_size(result['compressed_size'])} "
                f"(-{ratio:.0f}%)"
            )
            item = QTableWidgetItem(detail)
            item.setForeground(QColor("#27ae60"))
        else:
            item = QTableWidgetItem(result.get("error", "—"))
            item.setForeground(QColor("#e74c3c"))
        self.table.setItem(index, 3, item)

        # Update progress
        completed = sum(1 for r in self.results if r is not None)
        self.progress_bar.setValue(completed)

        # Update stats
        total_orig = sum(
            r["original_size"] for r in self.results if r is not None and r["success"]
        )
        total_comp = sum(
            r["compressed_size"] for r in self.results if r is not None and r["success"]
        )
        success_count = sum(1 for r in self.results if r is not None and r["success"])
        if total_orig > 0:
            saved = total_orig - total_comp
            self.stats_label.setText(
                f"已完成 {completed}/{len(self.files)}  |  "
                f"成功 {success_count} 个  |  "
                f"共节省 {format_size(saved)}"
            )

    def _on_all_done(self):
        self._running = False
        completed = sum(1 for r in self.results if r is not None)
        success_count = sum(1 for r in self.results if r is not None and r["success"])
        self.close_btn.setEnabled(True)
        self.progress_bar.setFormat(
            f"完成 — {success_count}/{completed} 个文件压缩成功"
        )

        if self.settings.get("open_folder_after") and success_count > 0:
            first_output = None
            for r in self.results:
                if r and r.get("output_path"):
                    first_output = r["output_path"]
                    break
            if first_output:
                os.startfile(os.path.dirname(first_output))

    def _open_settings(self):
        from settings_window import SettingsWindow

        dlg = SettingsWindow(self.settings, self)
        if dlg.exec():
            self.settings = dlg.get_settings()

    def closeEvent(self, event):
        from PySide6.QtWidgets import QMessageBox

        if self._running:
            reply = QMessageBox.question(
                self,
                "确认",
                "压缩正在进行中，确定要退出吗？",
                QMessageBox.Yes | QMessageBox.No,
                QMessageBox.No,
            )
            if reply == QMessageBox.Yes:
                self._running = False
                try:
                    self.thread.quit()
                    self.thread.wait(2000)
                except RuntimeError:
                    pass
                event.accept()
            else:
                event.ignore()
        else:
            event.accept()


def launch_gui(files: list, icon_path: str = None):
    """Entry point called from main.py.

    icon_path is a file path string — QIcon is created AFTER QApplication
    because Qt image codecs require an initialized QApplication.
    """
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QIcon

    app = QApplication.instance()
    if not app:
        app = QApplication([])

    # QApplication must exist before creating QIcon
    icon = None
    if icon_path:
        icon = QIcon(icon_path)
        app.setWindowIcon(icon)

    window = MainWindow(files, icon)
    window.show()
    app.exec()
