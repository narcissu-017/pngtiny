"""Register / unregister Windows right-click context menu for PNG files."""

import os
import sys
import winreg


MENU_NAME = "使用 PngTiny 压缩"
REG_PATH = r".png\shell\PngTinyCompress"


def get_exe_path() -> str:
    """Get the path to the executable for the registry command."""
    if getattr(sys, "frozen", False):
        return sys.executable
    else:
        # Development mode — use python to run main.py
        python_exe = sys.executable
        script_path = os.path.join(os.path.dirname(__file__), "main.py")
        return f'"{python_exe}" "{script_path}"'


def is_registered() -> bool:
    """Check if the right-click menu is already registered."""
    try:
        key = winreg.OpenKey(
            winreg.HKEY_CLASSES_ROOT, REG_PATH, 0, winreg.KEY_READ
        )
        winreg.CloseKey(key)
        return True
    except FileNotFoundError:
        return False


def register():
    """Add right-click menu entry for all file types."""
    try:
        # Create the shell menu key
        key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, REG_PATH)
        winreg.SetValueEx(key, "", 0, winreg.REG_SZ, MENU_NAME)
        winreg.SetValueEx(key, "Icon", 0, winreg.REG_SZ, get_exe_path())
        winreg.CloseKey(key)

        # Create the command subkey
        cmd_path = f"{REG_PATH}\\command"
        cmd_key = winreg.CreateKey(winreg.HKEY_CLASSES_ROOT, cmd_path)
        winreg.SetValueEx(
            cmd_key, "", 0, winreg.REG_SZ, f'{get_exe_path()} "%1"'
        )
        winreg.CloseKey(cmd_key)

        print(f"已注册右键菜单: {MENU_NAME}")
        return True
    except PermissionError:
        print("权限不足，请以管理员身份运行此命令")
        return False
    except Exception as e:
        print(f"注册失败: {e}")
        return False


def unregister():
    """Remove the right-click menu entry."""
    try:
        cmd_path = f"{REG_PATH}\\command"
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, cmd_path)
        winreg.DeleteKey(winreg.HKEY_CLASSES_ROOT, REG_PATH)
        print("已移除右键菜单")
        return True
    except FileNotFoundError:
        print("右键菜单未注册")
        return True
    except PermissionError:
        print("权限不足，请以管理员身份运行此命令")
        return False
    except Exception as e:
        print(f"移除失败: {e}")
        return False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="PngTiny 右键菜单管理")
    parser.add_argument(
        "action",
        choices=["install", "uninstall", "status"],
        help="install: 注册右键菜单 | uninstall: 移除右键菜单 | status: 查看状态",
    )
    args = parser.parse_args()

    if args.action == "install":
        register()
    elif args.action == "uninstall":
        unregister()
    elif args.action == "status":
        if is_registered():
            print("右键菜单已注册")
        else:
            print("右键菜单未注册")
