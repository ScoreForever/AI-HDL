# Windows / TeX Live 可编辑报告

本包已随附中文和西文字体，使用 fonts/ 内的字体文件加载。无需安装 Noto 或 DejaVu 字体。正文与已完成 FSM 复验的最终报告一致。

1. 将整个 ZIP 解压到一个新目录，保留 fonts/、figures/ 与 report.tex 的相对位置。
2. 在包含 report.tex 的目录打开 PowerShell，执行 `./build.cmd`。
3. 编辑 report.tex 后再次运行同一命令。PDF 输出为 Lab1_Report_team01.pdf。

也可在 VSCode 中使用“打开文件夹”打开此目录，保留 .vscode/settings.json，运行 LaTeX Workshop 的 XeLaTeX twice recipe。必须使用 XeLaTeX。无需 Bash 或 Pandoc；不要复制旧包的 build.sh 或字体设置到本包。

如需添加成员信息，在私有本地副本修改 `\author{team01}`。旧包中已修改的正文可复制到本包 `\begin{document}` 后的对应位置，保留本包导言区和 fonts/ 文件夹。

字体许可在 fonts/ 中。此次字体修复已在 Linux XeLaTeX 下完成实际编译；Windows build.cmd 提供对应的两次编译命令。其他 TeX 宏包使用 TeX Live 环境中的版本。

服务器原图仍可按 server-summary.png、server-winograd-log.png、server-winograd-wave.png、server-cordic-log.png、server-cordic-wave.png、server-fsm-recheck.png、server-bonus-log.png 放入 figures/，重新编译即可插入。现有图片为本地真实波形。
