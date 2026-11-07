# AI-HDL：Lab 1

2026-11-07 已重新核对官方文件并复跑全部测试。最新下载与提交操作见 [最终交付与操作步骤](docs/最终交付与操作步骤.md)。

课程：[Lab 1 作业说明](https://aiarchpku.com/2026Fall/project/la1.html)。
已实现三项必做任务和 2D Winograd Bonus。说明与报告均为中文。

## 从 GitHub 获取和使用

不需要访问云环境目录。在 GitHub 仓库首页可以直接打开下面的文件：

- [实验报告 PDF](dist/Lab1_Report_team01.pdf)：查看设计、测试结果和波形。文件页可预览，也可点击 **Download raw file** 下载。
- [提交包 ZIP](dist/Lab1_Report_team01.zip)：打开文件页后点击 **Download raw file** 下载。只包含 PDF 和七个实现 RTL，不含 TB 或仿真临时文件。
- [中文交接说明](docs/交接说明.md)：先看“提交人仍需完成”和“服务器交接”，包含后续操作和原课程服务器命令。

如要下载全部源码与脚本，点击仓库首页 **Code → Download ZIP**，解压后阅读本 README。整个仓库的下载包用于开发，课程提交应使用 `dist/` 内专门生成的作业包。

当前文件已填写 team01 ，公开版不含个人信息。若修改报告，可用 `python3 scripts/package.py --team team01` 重新生成报告和压缩包。服务器 VCS/Verdi 复验尚未执行，组长上传课程网也尚未完成。

## 文件位置与本地复现

- [交接说明：已完成、待完成、服务器复验与提交步骤](docs/交接说明.md)
- [实验报告源稿](docs/Lab1_Report_team01.md)
- [已有验证日志](docs/validation/README.md)
- 源码在 `lab1/`，复现脚本在 `scripts/`，报告 PDF 和提交压缩包在 `dist/`。

在现有隔离环境 checkout `/workspace/AI-HDL` 中工作，无需另建 worktree。

```sh
cd /workspace/AI-HDL
bash scripts/setup_iverilog.sh
python3 scripts/verify.py
python3 scripts/extended.py
python3 scripts/plot_waves.py
bash scripts/setup_report.sh
python3 scripts/package.py  # 默认 team01；真实组号通过 --team team01 等传入
```

安装使用 Debian 官方 HTTPS 软件包和 SHA256 校验，不需要管理员权限。
仿真脚本可通过 IVERILOG、IVL、VVP 环境变量覆盖工具路径。
`package.py` 需要 Pandoc、XeLaTeX 和 Noto Serif CJK SC 字体。
图片脚本需要 matplotlib，测试脚本本身仅用 Python 标准库。

`lab1/{winograd,cordic,fsm}/run` 与课程 TB 保持原样；`NO_FSDB` 是原 TB 已有的条件编译开关。
Icarus 的执行结果不等于 VCS/Verdi 已复验，也未声称完成综合或板级验证。
`build/` 内日志、VCD 和扩展测试中间文件用于复查，不进入提交包。
