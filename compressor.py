"""PNG compression engine using pngquant."""

import os
import sys
import shutil
import subprocess
from pathlib import Path
from typing import Optional


def get_pngquant_path() -> Optional[str]:
    """Locate pngquant executable (bundled or system PATH)."""
    if getattr(sys, "frozen", False):
        app_dir = Path(sys._MEIPASS)
    else:
        app_dir = Path(__file__).parent

    for candidate in [
        app_dir / "pngquant.exe",
        app_dir / "bin" / "pngquant.exe",
    ]:
        if candidate.exists():
            return str(candidate)

    system_path = shutil.which("pngquant")
    if system_path:
        return system_path

    return None


def is_apng(filepath: str) -> bool:
    """Detect animated PNG by scanning for the acTL chunk."""
    try:
        with open(filepath, "rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n":
                return False
            while True:
                length_bytes = f.read(4)
                if len(length_bytes) < 4:
                    break
                length = int.from_bytes(length_bytes, "big")
                chunk_type = f.read(4).decode("ascii", errors="replace")
                if chunk_type == "acTL":
                    return True
                if chunk_type == "IDAT":
                    return False
                f.seek(length + 4, 1)
    except Exception:
        pass
    return False


def resolve_output_path(input_path: str, settings: dict) -> str:
    """Determine output path based on settings, with collision avoidance."""
    file_dir = os.path.dirname(input_path)
    filename = os.path.basename(input_path)
    name, ext = os.path.splitext(filename)

    if settings.get("save_mode") == "custom_folder" and settings.get("custom_folder"):
        output_dir = settings["custom_folder"]
        output_name = filename
        base_name = name
        suffix = ""
    else:
        output_dir = file_dir
        base_name = name
        suffix = settings.get("suffix", "-min")
        output_name = f"{name}{suffix}{ext}"

    output_path = os.path.join(output_dir, output_name)

    if not settings.get("overwrite", False):
        counter = 1
        while os.path.exists(output_path):
            if suffix:
                new_name = f"{base_name}{suffix}_{counter}{ext}"
            else:
                new_name = f"{base_name}_{counter}{ext}"
            output_path = os.path.join(output_dir, new_name)
            counter += 1

    return output_path


def _exit_code_message(code: int) -> str:
    messages = {
        1: "不是有效的 PNG 文件",
        2: "pngquant 参数错误",
        25: "无法解码此 PNG 文件（文件可能已损坏）",
        98: "无法写入输出文件（检查目标文件夹权限）",
        99: "图片颜色过于丰富，在此质量范围下无法压缩。请尝试降低质量标准",
    }
    return messages.get(code, f"压缩失败 (退出码: {code})")


def compress_png(
    input_path: str,
    output_path: str,
    quality_min: int = 60,
    quality_max: int = 80,
    preserve_date: bool = True,
) -> dict:
    """
    Compress a single PNG file.

    Returns dict: {success, original_size, compressed_size, error}
    """
    pngquant = get_pngquant_path()
    original_size = os.path.getsize(input_path)

    if not pngquant:
        return {
            "success": False,
            "original_size": original_size,
            "compressed_size": 0,
            "error": "找不到 pngquant，请确认已正确安装",
        }

    if is_apng(input_path):
        return {
            "success": False,
            "original_size": original_size,
            "compressed_size": 0,
            "error": "不支持动画 PNG (APNG)",
        }

    # Preserve original file timestamps
    original_stat = os.stat(input_path) if preserve_date else None

    # Create output directory if needed
    output_dir = os.path.dirname(output_path)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)

    creationflags = subprocess.CREATE_NO_WINDOW if sys.platform == "win32" else 0

    try:
        result = subprocess.run(
            [
                pngquant,
                f"--quality={quality_min}-{quality_max}",
                "--force",
                "--output", output_path,
                "--", input_path,
            ],
            capture_output=True,
            text=True,
            creationflags=creationflags,
            timeout=60,
        )

        if result.returncode == 0 and os.path.exists(output_path):
            compressed_size = os.path.getsize(output_path)

            if preserve_date and original_stat:
                os.utime(output_path, (original_stat.st_atime, original_stat.st_mtime))

            return {
                "success": True,
                "original_size": original_size,
                "compressed_size": compressed_size,
                "error": None,
            }
        else:
            error_msg = result.stderr.strip() if result.stderr else _exit_code_message(result.returncode)
            return {
                "success": False,
                "original_size": original_size,
                "compressed_size": 0,
                "error": error_msg,
            }
    except subprocess.TimeoutExpired:
        return {
            "success": False,
            "original_size": original_size,
            "compressed_size": 0,
            "error": "压缩超时",
        }
    except Exception as e:
        return {
            "success": False,
            "original_size": original_size,
            "compressed_size": 0,
            "error": str(e),
        }


def format_size(size_bytes: int) -> str:
    """Human-readable file size."""
    if size_bytes >= 1024 * 1024:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
    elif size_bytes >= 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes} B"
