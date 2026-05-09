; Chinese Simplified language file for Inno Setup 6.5+
; Based on Default.isl format.

[LangOptions]
LanguageName=简体中文
LanguageID=$0804
LanguageCodePage=0

[Messages]

; *** Application titles
SetupAppTitle=安装程序
SetupWindowTitle=安装 - [name]
UninstallAppTitle=卸载程序
UninstallAppFullTitle=%1 卸载程序

; *** Misc. common
ButtonBack=< 上一步(&B)
ButtonNext=下一步(&N) >
ButtonInstall=安装(&I)
ButtonOK=确定
ButtonCancel=取消
ButtonYes=是(&Y)
ButtonNo=否(&N)
ButtonFinish=完成(&F)
ButtonBrowse=浏览(&B)...
ButtonWizardBrowse=浏览(&R)...

; *** Welcome page
WelcomeLabel1=欢迎使用 [name] 安装向导
WelcomeLabel2=本程序将在您的电脑上安装 [name]。%n%n建议在继续安装之前关闭所有其他应用程序。

; *** License page
WizardLicense=许可协议
LicenseLabel=在继续安装之前，请阅读以下重要信息。
LicenseLabel3=请阅读以下许可协议。您必须接受协议才能继续安装。
LicenseAccepted=我接受协议(&A)
LicenseNotAccepted=我不接受协议(&D)

; *** Directory page
WizardSelectDir=选择目标位置
SelectDirDesc=应将 [name] 安装到何处？
SelectDirLabel3=安装程序将把 [name] 安装到以下文件夹中。
SelectDirBrowseLabel=点击"下一步"继续。如需选择其他文件夹，请点击"浏览"。
DiskSpaceMBLabel=至少需要 [mb] MB 的可用磁盘空间。

; *** Program group page
WizardSelectProgramGroup=选择开始菜单文件夹
SelectStartMenuFolderDesc=应将程序的快捷方式放在何处？
SelectStartMenuFolderLabel3=安装程序将在以下开始菜单文件夹中创建程序的快捷方式。
SelectStartMenuFolderBrowseLabel=点击"下一步"继续。如需选择其他文件夹，请点击"浏览"。
NoProgramGroupCheck2=不要创建开始菜单文件夹(&D)
MustEnterGroupName=请输入文件夹名称。

; *** Ready page
WizardReady=准备安装
ReadyLabel1=安装程序已准备就绪，将开始在您的电脑上安装 [name]。
ReadyLabel2a=点击"安装"继续安装。
ReadyLabel2b=点击"安装"继续安装。%n%n以下为您的安装设置摘要：
ReadyMemoUserInfo=用户信息:
ReadyMemoDir=目标位置:
ReadyMemoType=安装类型:
ReadyMemoComponents=选定组件:
ReadyMemoGroup=开始菜单文件夹:
ReadyMemoTasks=附加任务:
ClickInstall=点击"安装"开始安装。

; *** Installing page
WizardInstalling=正在安装
InstallingLabel=请稍候，安装程序正在将 [name] 安装到您的电脑上。

; *** Setup completed page
FinishedHeadingLabel=[name] 安装完成
FinishedLabel=安装程序已在您的电脑上完成 [name] 的安装。应用程序可通过已创建的快捷方式启动。%n%n点击"完成"退出安装程序。
FinishedLabelNoIcons=安装程序已在您的电脑上完成 [name] 的安装。%n%n点击"完成"退出安装程序。
ClickFinish=点击"完成"退出安装程序。

; *** Uninstaller messages
ConfirmUninstall=您确定要完全卸载 %1 及其所有组件吗？
UninstallStatusLabel=请稍候，正在卸载 %1……
UninstalledAll=%1 已成功从您的电脑中卸载。%n%n点击"完成"退出。
UninstalledMost=%1 卸载完成。%n%n部分组件未能删除，您可以手动删除。%n%n点击"完成"退出。
UninstalledAndNeedsRestart=要完成 %1 的卸载，必须重新启动电脑。%n%n是否立即重新启动？
UninstallDataCorrupted=文件"%s"损坏，无法卸载。%n请重新安装程序后重试。

; *** Setup status messages
StatusCreateDirs=创建目录……
StatusExtractFiles=解压文件……
StatusCreateIcons=创建快捷方式……
StatusCreateUninstaller=创建卸载程序……
StatusRegistry=写入注册表……
StatusInstallDone=安装完成
StatusRunProgram=启动程序……
StatusRollback=正在回滚更改……
StatusUninstalling=正在卸载 %1……
StatusUninstallDone=卸载完成
StatusFinishErrors=安装程序未能完成安装。请修正以下问题并重试:

; *** Other
PrivilegesRequiredOverrideTitle=需要管理员权限
PrivilegesRequiredOverrideInstruction=安装程序需要管理员权限才能继续。
RunEntryExec=运行 %1
RunEntryShellExec=运行 %1
DiskSpaceMB=%1 需要至少 %2 MB 的磁盘空间。%n%n请释放一些磁盘空间后重试。
AboutSetupTitle=关于安装程序
AboutSetupMessage=%1 版本 %2%n%nCopyright (C) 1997-2026 Jordan Russell.%nPortions Copyright (C) 2000-2026 Martijn Laan.%n%nhttps://www.innosetup.com
HelpTextNote=本安装程序使用了 Inno Setup，如有问题请参考其帮助文档: %1
