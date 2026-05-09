"""Settings dialog for save location, quality, and behavior options."""

from PySide6.QtGui import QIcon
from PySide6.QtWidgets import (
    QDialog,
    QVBoxLayout,
    QHBoxLayout,
    QGroupBox,
    QRadioButton,
    QLineEdit,
    QSpinBox,
    QCheckBox,
    QPushButton,
    QLabel,
    QFileDialog,
    QDialogButtonBox,
    QButtonGroup,
    QWidget,
)
from PySide6.QtCore import Qt

from settings import save_settings


class SettingsWindow(QDialog):
    def __init__(self, settings: dict, parent=None):
        super().__init__(parent)
        self.settings = dict(settings)
        self.setWindowTitle("PngTiny 设置")
        self.setMinimumWidth(460)
        # Inherit parent's window icon or use app default
        if parent and parent.windowIcon():
            self.setWindowIcon(parent.windowIcon())
        self._setup_ui()
        self._load_values()

    def _setup_ui(self):
        layout = QVBoxLayout(self)
        layout.setSpacing(16)

        # --- Save location group ---
        save_group = QGroupBox("保存位置")
        save_layout = QVBoxLayout(save_group)

        self.btn_suffix = QRadioButton("源文件夹 + 文件名后缀")
        self.btn_custom = QRadioButton("统一保存到指定文件夹")
        btn_group = QButtonGroup(self)
        btn_group.addButton(self.btn_suffix)
        btn_group.addButton(self.btn_custom)
        btn_group.setExclusive(True)

        save_layout.addWidget(self.btn_suffix)

        # Suffix row
        suffix_row = QHBoxLayout()
        suffix_row.addWidget(QLabel("后缀名:"))
        self.suffix_input = QLineEdit()
        self.suffix_input.setFixedWidth(120)
        self.suffix_input.setPlaceholderText("-min")
        suffix_row.addWidget(self.suffix_input)
        suffix_row.addStretch()
        save_layout.addLayout(suffix_row)

        save_layout.addWidget(self.btn_custom)

        # Custom folder row
        folder_row = QHBoxLayout()
        folder_row.addWidget(QLabel("目标文件夹:"))
        self.folder_input = QLineEdit()
        self.folder_input.setPlaceholderText("选择文件夹...")
        folder_row.addWidget(self.folder_input)
        btn_browse = QPushButton("浏览...")
        btn_browse.setFixedWidth(70)
        btn_browse.clicked.connect(self._browse_folder)
        folder_row.addWidget(btn_browse)
        save_layout.addLayout(folder_row)

        self.btn_suffix.toggled.connect(self._on_save_mode_changed)
        self.btn_custom.toggled.connect(self._on_save_mode_changed)
        layout.addWidget(save_group)

        # --- Quality group ---
        quality_group = QGroupBox("压缩质量 (pngquant)")
        quality_layout = QHBoxLayout(quality_group)

        quality_layout.addWidget(QLabel("最小:"))
        self.quality_min = QSpinBox()
        self.quality_min.setRange(0, 100)
        self.quality_min.setSuffix("%")
        quality_layout.addWidget(self.quality_min)

        quality_layout.addSpacing(16)

        quality_layout.addWidget(QLabel("最大:"))
        self.quality_max = QSpinBox()
        self.quality_max.setRange(0, 100)
        self.quality_max.setSuffix("%")
        quality_layout.addWidget(self.quality_max)

        quality_layout.addStretch()

        tip = QLabel("数值越低压缩率越高，质量损失越大。建议 60-80。")
        tip.setStyleSheet("color: #888; font-size: 11px;")
        quality_layout.addWidget(tip)
        layout.addWidget(quality_group)

        # --- Options group ---
        options_group = QGroupBox("其他选项")
        options_layout = QVBoxLayout(options_group)

        self.chk_overwrite = QCheckBox("覆盖原文件（不生成新文件）")
        self.chk_preserve_date = QCheckBox("保留原文件修改日期")
        self.chk_open_folder = QCheckBox("压缩完成后打开目标文件夹")

        options_layout.addWidget(self.chk_overwrite)
        options_layout.addWidget(self.chk_preserve_date)
        options_layout.addWidget(self.chk_open_folder)
        layout.addWidget(options_group)

        # --- Buttons ---
        button_box = QDialogButtonBox(
            QDialogButtonBox.Ok | QDialogButtonBox.Cancel
        )
        button_box.accepted.connect(self._on_save)
        button_box.rejected.connect(self.reject)
        layout.addWidget(button_box)

    def _load_values(self):
        s = self.settings
        if s.get("save_mode") == "custom_folder":
            self.btn_custom.setChecked(True)
        else:
            self.btn_suffix.setChecked(True)

        self.suffix_input.setText(s.get("suffix", "-min"))
        self.folder_input.setText(s.get("custom_folder", ""))
        self.quality_min.setValue(s.get("quality_min", 60))
        self.quality_max.setValue(s.get("quality_max", 80))
        self.chk_overwrite.setChecked(s.get("overwrite", False))
        self.chk_preserve_date.setChecked(s.get("preserve_date", True))
        self.chk_open_folder.setChecked(s.get("open_folder_after", False))

        self._on_save_mode_changed()

    def _on_save_mode_changed(self):
        is_suffix = self.btn_suffix.isChecked()
        self.suffix_input.setEnabled(is_suffix)
        self.folder_input.setEnabled(not is_suffix)

    def _browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "选择保存文件夹")
        if folder:
            self.folder_input.setText(folder)

    def _on_save(self):
        s = self.settings
        s["save_mode"] = "suffix" if self.btn_suffix.isChecked() else "custom_folder"
        s["suffix"] = self.suffix_input.text().strip() or "-min"
        s["custom_folder"] = self.folder_input.text().strip()
        s["quality_min"] = self.quality_min.value()
        s["quality_max"] = self.quality_max.value()
        s["overwrite"] = self.chk_overwrite.isChecked()
        s["preserve_date"] = self.chk_preserve_date.isChecked()
        s["open_folder_after"] = self.chk_open_folder.isChecked()

        if s["save_mode"] == "custom_folder" and not s["custom_folder"]:
            self.folder_input.setFocus()
            return

        save_settings(s)
        self.accept()

    def get_settings(self) -> dict:
        return self.settings
