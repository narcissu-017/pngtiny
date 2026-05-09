[[English](README.md) | [简体中文](README.zh-CN.md)]

# PngTiny

PngTiny 是一款 Windows 本地 PNG 图片压缩工具。

它提供类似某些图片压缩网站的简单使用流程，但不需要上传图片、不需要账号，也不需要 API Key。适合在图片用于网站、应用、文档或游戏素材之前，先减小 PNG 文件体积。

当前版本：`v1.0.0`

## 主要特点

- 在 Windows 本机压缩 PNG 图片
- 支持通过右键菜单快速使用
- 支持单文件和多文件处理
- 使用轻量桌面窗口显示压缩进度
- 可调整压缩质量和输出位置
- 支持桌面界面和命令行两种用法

## 下载和使用

可以使用 PyInstaller 构建 Windows 可执行文件，再用 Inno Setup 生成安装器：

```powershell
pyinstaller pngtiny.spec
ISCC.exe installer.iss
```

安装后，右键 PNG 文件并选择：

```text
使用 PngTiny 压缩
```

PngTiny 面向 Windows 10 / 11 桌面环境。压缩过程在本机完成，不需要网络上传。

## 从源码运行

推荐环境：

- Windows 10 / 11
- Python 3.11 或更高版本

安装依赖：

```powershell
python -m pip install -r requirements.txt
```

打开设置窗口：

```powershell
python main.py --settings
```

使用桌面界面压缩：

```powershell
python main.py image.png
```

使用命令行压缩：

```powershell
python main.py --cli image.png
```

## 基本流程

1. 安装 PngTiny，或从源码运行。
2. 按需要调整压缩质量和输出位置。
3. 右键 PNG 文件并选择 `使用 PngTiny 压缩`。
4. 等待压缩窗口完成处理。
5. 在项目中使用压缩后的 PNG 文件。

## 第三方组件

PngTiny 使用 `pngquant` 进行 PNG 压缩，使用 `PySide6` 构建桌面界面。

详情见 [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)。

## 许可证

重新分发二进制文件前，请确认所包含第三方组件的许可证要求。
