"""PngTiny — PNG compression tool."""

import os
import sys
import traceback
from pathlib import Path

from compressor import compress_png, resolve_output_path, format_size
from settings import load_settings


def _show_error(title: str, text: str):
    """Show a Windows message box. Does NOT depend on PySide6."""
    try:
        import ctypes
        ctypes.windll.user32.MessageBoxW(0, text, title, 0x10)
    except Exception:
        pass


def get_icon_path() -> str:
    """Get path to icon.ico (works in both dev and PyInstaller-frozen modes)."""
    if getattr(sys, "frozen", False):
        return str(Path(sys._MEIPASS) / "icon.ico")
    return str(Path(__file__).parent / "icon.ico")


def run_cli(png_files: list):
    """Compress files from the command line (no GUI)."""
    settings = load_settings()
    total_original = 0
    total_compressed = 0
    success_count = 0

    for filepath in png_files:
        filename = os.path.basename(filepath)
        output_path = resolve_output_path(filepath, settings)

        print(f"压缩中: {filename} ... ", end="", flush=True)

        result = compress_png(
            filepath,
            output_path,
            quality_min=settings["quality_min"],
            quality_max=settings["quality_max"],
            preserve_date=settings.get("preserve_date", True),
        )

        if result["success"]:
            saved = result["original_size"] - result["compressed_size"]
            ratio = (saved / result["original_size"]) * 100
            print(
                f"[OK] {format_size(result['original_size'])} -> "
                f"{format_size(result['compressed_size'])} ({ratio:.0f}%)"
            )
            total_original += result["original_size"]
            total_compressed += result["compressed_size"]
            success_count += 1
        else:
            print(f"[FAIL] {result['error']}")

    if success_count > 0:
        total_saved = total_original - total_compressed
        print(f"\n压缩完成: {success_count}/{len(png_files)} 个文件")
        print(f"共节省: {format_size(total_saved)}")


def _has_gui() -> bool:
    try:
        import PySide6  # noqa: F401
        return True
    except ImportError:
        return False


def _has_display() -> bool:
    """Check if a graphical display is available (session has a desktop)."""
    if sys.platform == "win32":
        try:
            import ctypes
            return ctypes.windll.user32.GetDesktopWindow() != 0
        except Exception:
            return True
    return bool(os.environ.get("DISPLAY"))


def _open_settings_gui():
    from PySide6.QtWidgets import QApplication
    from PySide6.QtGui import QIcon
    from settings_window import SettingsWindow
    from settings import save_settings

    app = QApplication.instance() or QApplication([])
    app.setWindowIcon(QIcon(get_icon_path()))
    settings = load_settings()
    dlg = SettingsWindow(settings)
    if dlg.exec():
        save_settings(dlg.get_settings())


def main():
    args = sys.argv[1:]

    # --cli flag: force CLI mode
    force_cli = "--cli" in args
    if force_cli:
        args = [a for a in args if a != "--cli"]

    # --settings flag: open settings window only
    if "--settings" in args:
        _open_settings_gui()
        return

    # Collect valid PNG files from arguments
    png_files = []
    for arg in args:
        arg = arg.strip('"')
        if arg.lower().endswith(".png") and os.path.isfile(arg):
            png_files.append(os.path.abspath(arg))

    if png_files:
        if _has_gui() and not force_cli and _has_display():
            from main_window import launch_gui
            # Pass icon_path as string — QIcon must be created AFTER QApplication
            launch_gui(png_files, get_icon_path())
        else:
            run_cli(png_files)
    else:
        if _has_gui() and _has_display():
            _open_settings_gui()
        else:
            print("PngTiny — PNG 压缩工具")
            print("用法: python main.py <png文件> [更多png文件...]")
            print("或右键 PNG 文件选择 '使用 PngTiny 压缩'")
            print("可选:")
            print("  --settings   打开设置")
            print("  --cli        强制命令行模式")


def _main_safe():
    """Wrap main() with crash logging and user-visible error reporting."""
    try:
        main()
    except Exception:
        tb = traceback.format_exc()
        _show_error("PngTiny 启动失败", f"程序发生未预期的错误：\n\n{tb[-400:]}")


if __name__ == "__main__":
    _main_safe()
