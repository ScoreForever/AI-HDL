# V2 可编辑报告：使用说明

此目录为新版本，旧版 docs/ 和 dist/ 报告未被替换。

**状态：正文和 PDF 已生成，服务器原截图待嵌入。当前不是可直接提交版本。**
聊天中的七张截图已由 AI 读取并在正文逐项分析，但未作为可读取的文件提供到执行环境。因此 PDF 七处保留明确的待插图框，未伪造截图。现有三张 figures/*.png 是此前本地真实 VCD 绘图，来源已在正文区分。

## 文件

- `report.tex`：可直接编辑并编译的独立 LaTeX 源文件。
- `report.md`：更易阅读、编辑的正文源稿。
- `header.tex`：Markdown 转 TeX 时加入的宏；生成的 report.tex 已内含它。
- `Lab1_Report_team01.pdf`：当前编译的 PDF（待嵌图稿）。
- `figures/`：本地波形和预留的截图位置。
- `rtl/`：与已验证版本逐字节一致的七个实现文件，供最终本地打包。
- `build.sh`：编译脚本；默认不覆盖 TeX。
- `package_submission.py`：最终精简打包脚本；缺截图时拒绝打包。

## 两种编辑方式，选一种

### 直接编辑 TeX（推荐）

修改 `report.tex` 中的段落、表格、公式，然后运行：

```sh
bash build.sh
```

也可不使用脚本，在此目录连续运行两次：

```sh
xelatex -interaction=nonstopmode -halt-on-error -jobname=Lab1_Report_team01 report.tex
xelatex -interaction=nonstopmode -halt-on-error -jobname=Lab1_Report_team01 report.tex
```

**直接修改 TeX 后不要运行 `build.sh --from-md`，否则会由 Markdown 重新生成并覆盖 TeX 改动。**

### 编辑 Markdown

修改 report.md，若需修改截图宏则修改 header.tex，然后运行：

```sh
bash build.sh --from-md
```

该操作重新生成 report.tex 再编译两次 PDF。应选择一个文件作为正文主版本，避免双向编辑不一致。

## 编译环境

使用 TeX Live 或 MiKTeX，编译器选 XeLaTeX，需 xeCJK/中文字体、DejaVu Serif、DejaVu Sans Mono、Noto Serif CJK SC；重新从 Markdown 生成 TeX 另需 Pandoc。当前云环境已经成功编译。

也可把 report.tex 和整个 figures 文件夹上传到私有 Overleaf 项目，将主文档设为 report.tex、编译器设为 XeLaTeX。若环境缺指定字体，安装这些字体，或在 TeX 导言区将 mainfont/monofont/CJKmainfont 改为环境已有字体并检查排版。Windows 本地可用 TeXstudio 调用 XeLaTeX；无需运行 Bash 脚本。

## 七张服务器截图如何插入

先用本机图片工具在图片像素上裁去或覆盖账号、学号、主机名、个人目录，然后导出新的 PNG。不要只使用 LaTeX 白框遮住原图，这可能保留可提取的个人信息。请保留 PASS、时间轴、信号名及 FSM 崩溃行；裁剪隐私不能删除不利证据。

将处理后的图片按下列名字放入 figures/：

1. `server-bonus-log.png`：2D 编译及 928 组输出通过截图。
2. `server-summary.png`：三项自动验证汇总，裁去首行提示符和末行个人路径。
3. `server-cordic-wave.png`：CORDIC Verdi 波形，去掉包含账号路径的标题/源码栏。
4. `server-winograd-log.png`：Winograd 十组 PASS 日志。
5. `server-fsm-log.png`：FSM 编译和仿真截图，保留 Segmentation fault 与 ALL PASS。
6. `server-cordic-log.png`：CORDIC 十角度 PASS 日志。
7. `server-winograd-wave.png`：Winograd Verdi 波形，去掉个人路径。

重新编译后，图片自动替换对应待插图框。还需将报告关于“原图未收到”的证据说明和提交差距改为实际完成状态，并检查图中字是否可读；可将较长截图拆为局部，保留完整证据文件在本地。

## 本地补充个人信息

仅在私有本地副本中，在 TeX 的 `\maketitle` 之前设置 `\author{...}`（建议放在 `\date{...}` 前）。成员姓名和学号也可以在正文加入表格。填写后重新编译。不要将含个人信息的源稿、PDF、截图或 ZIP 推送到公开仓库。

## FSM 异常补查

用户截图在编译阶段出现 cfs_ident_exec Segmentation fault，之后功能测试 ALL PASS。新报告如实保留。建议使用新解压目录复验，并在 FSM run 目录执行：

```sh
make rerun > rerun-console.log 2>&1
status=$?
printf 'make_exit_code=%s\n' "$status" > exit-status.txt
```

保留 compile.log、simulation.log、rerun-console.log、exit-status.txt；检查所有日志中的 Segmentation fault、core dumped、Error、Fatal。即使 make 退出为 0，也要检查工具子进程异常。如持续出现，请助教检查工具环境，勿修改 TB 来规避。将实际复验结果写入新版报告；不能直接删除已有异常记录而不解释处理结果。

## 最终打包

完成插图、异常补查、身份信息和正文状态更新，编译并人工检查 PDF 后：

```sh
python3 package_submission.py
```

生成 submission/Lab1_Report_team01.zip，仅含 PDF 和七个实现 .v。源稿、图片、TB、日志都不进入该 ZIP。脚本检查图片齐备和占位文本，但不能替代人工检查，更不能自动认定 FSM 工具异常已解决。
