[[English](README.md) | [简体中文](README.zh-CN.md)]

# PngTiny

PngTiny is a local PNG compression tool for Windows.

It provides a simple workflow similar to some online image compression tools, but without requiring image uploads, accounts, or API keys. It is useful for reducing PNG file size before using images in websites, apps, documents, or game assets.

Current version: `v1.0.0`

## Highlights

- Compress PNG files locally on Windows
- Use from the Windows right-click menu
- Process single or multiple PNG files
- Show compression progress in a lightweight desktop window
- Adjust compression quality and output location
- Run from either the desktop UI or command line

## Download and Use

Build a Windows executable with PyInstaller, then create an installer with Inno Setup:

```powershell
pyinstaller pngtiny.spec
ISCC.exe installer.iss
```

After installation, right-click a PNG file and choose:

```text
使用 PngTiny 压缩
```

PngTiny is intended for Windows 10 / 11 desktop use. Compression runs on your computer and does not require network upload.

## Run from Source

Recommended environment:

- Windows 10 / 11
- Python 3.11 or later

Install dependencies:

```powershell
python -m pip install -r requirements.txt
```

Open settings:

```powershell
python main.py --settings
```

Compress with the desktop UI:

```powershell
python main.py image.png
```

Compress from the command line:

```powershell
python main.py --cli image.png
```

## Basic Workflow

1. Install PngTiny or run it from source.
2. Adjust quality and output settings if needed.
3. Right-click PNG files and choose `使用 PngTiny 压缩`.
4. Wait for the compression window to finish.
5. Use the compressed PNG files in your project.

## Third-Party Components

PngTiny uses `pngquant` for PNG compression and `PySide6` for the desktop interface.

See [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md) for details.

## License

Review the licenses of bundled third-party components before redistributing binaries.
