本目录日志已于 2026-11-07 重新运行验证并刷新；数值结果与上一轮一致。详见 `../最终交付与操作步骤.md`。

# 本地验证记录

这些日志来自完成作业时实际执行的 Icarus Verilog 12.0 仿真，随云环境快照保留，本次复制到仓库供 GitHub 阅读。它们不是服务器 VCS/Verdi 运行记录。

- winograd-simulation.log：课程原始测试 10 PASS，ALL PASS。
- cordic-simulation.log：课程原始测试 10 PASS，ALL PASS。
- fsm-simulation.log：课程原始测试 3 项 PASS，ALL PASS。
- stream1.log：2400 周期，1861 个有效输出一致。
- stream2.log：1200 周期，928 个有效输出一致。
- angles.log：1568 个输入，最大绝对误差 1。
- fsm_grid.log：36 组延迟组合及运行中复位。

对应的 compile.log 记录编译警告，未隐去无显式 timescale 的提示。

重跑课程测试：`python3 scripts/verify.py`；扩展测试：`python3 scripts/extended.py`。新日志会输出到 build/，不会自动覆盖本目录已存档的证据。
