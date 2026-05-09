; Inno Setup script for PngTiny
; Requires Inno Setup 6+: https://jrsoftware.org/isinfo.php

#define MyAppName "PngTiny"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "PngTiny"
#define MyAppExeName "pngtiny.exe"

[Setup]
AppId={{A8F3C9E2-5B7D-4A1E-9C3F-8D2E6B7A9F1C}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=.\dist\installer
OutputBaseFilename=PngTiny_Setup_{#MyAppVersion}
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
ArchitecturesInstallIn64BitMode=x64compatible
PrivilegesRequired=admin
SetupIconFile=icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimp"; MessagesFile: "ChineseSimplified.isl"

[CustomMessages]
; Chinese Simplified custom messages
chinesesimp.AppName=PngTiny
chinesesimp.LaunchAfterInstall=安装完成后启动 PngTiny

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{#MyAppName} 设置"; Filename: "{app}\{#MyAppExeName}"; Parameters: "--settings"
Name: "{group}\卸载 {#MyAppName}"; Filename: "{uninstallexe}"

[Registry]
; Register right-click context menu for PNG files
; Primary: classic .png\shell path (most compatible, used by 7-Zip/WinRAR/VSCode)
Root: HKCR; Subkey: ".png\shell\PngTinyCompress"; ValueType: string; ValueName: ""; ValueData: "使用 PngTiny 压缩"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".png\shell\PngTinyCompress"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".png\shell\PngTinyCompress\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey
; Fallback: SystemFileAssociations (Windows 8+), ensures menu shows even if .png is unassociated
Root: HKCR; Subkey: "SystemFileAssociations\.png\shell\PngTinyCompress"; ValueType: string; ValueName: ""; ValueData: "使用 PngTiny 压缩"; Flags: uninsdeletekey
Root: HKCR; Subkey: "SystemFileAssociations\.png\shell\PngTinyCompress"; ValueType: string; ValueName: "Icon"; ValueData: "{app}\{#MyAppExeName}"; Flags: uninsdeletekey
Root: HKCR; Subkey: "SystemFileAssociations\.png\shell\PngTinyCompress\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "启动 {#MyAppName}"; Flags: nowait postinstall skipifsilent
