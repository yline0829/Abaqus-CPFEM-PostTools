# Abaqus-CPFEM-PostTools

[English](README.md) | **简体中文**

[![Latest Release](https://img.shields.io/github/v/release/yline0829/Abaqus-CPFEM-PostTools?display_name=tag&sort=semver)](https://github.com/yline0829/Abaqus-CPFEM-PostTools/releases/latest)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
![Windows](https://img.shields.io/badge/Windows-supported-0078D6?logo=windows&logoColor=white)
![Linux](https://img.shields.io/badge/Linux-supported-FCC624?logo=linux&logoColor=black)

面向 **Abaqus/CPFEM** 的跨平台后处理工具集，主要用于大型 ODB 选择性读取、ParaView 可视化、晶粒尺度场分析、GND 演化、摩擦时历数据提取以及 PEEQCP 重构。

> 本项目与 Dassault Systèmes 无关联。读取和写入 ODB 需要用户本机已安装并获得合法许可的 Abaqus；本仓库不分发 Abaqus 库、可执行文件或其他商业软件组件。

## 下载

普通用户建议直接从 **GitHub Releases** 下载最新打包版本：

**[下载最新版本](https://github.com/yline0829/Abaqus-CPFEM-PostTools/releases/latest)**

当前提供：

- **Windows — Abaqus Data Exporter 数据导出器**
- **Windows — Abaqus CPFEM Postprocess 后处理工具**
- **Linux — 两个工具的整合版本**

仓库本身主要用于源码维护；普通用户使用的 ZIP 包统一通过 **Releases** 发布。

## 项目概览

目前工具集包含两个互补的小程序：

| 程序 | 主要用途 |
|---|---|
| **Abaqus Data Exporter** | 选择性 ODB → VTU/PVD 导出、ParaView 场变量、GrainID、Initial IPF、Mises、GND 差值、晶粒极值分析以及 History/Curve 数据 |
| **Abaqus CPFEM Postprocess** | RP 时历数据提取，以及基于物理时间匹配的 PEEQCP 逐帧重构、目标帧保存与写回 |

## 软件截图

### 1. Abaqus Data Exporter 数据导出器

可选择 ODB、实例、晶粒区域、分析步、帧以及需要导出的场变量。支持多分析步的 ParaView 时间序列导出，不需要把整个大型 ODB 全部转换。

<p align="center">
  <img src="docs/images/data-exporter.png" width="95%" alt="Abaqus 数据导出器">
</p>

### 2. Abaqus CPFEM Postprocess

用于 RP 时历数据以及 PEEQCP 重构。PEEQCP 仍然遍历全部存储帧进行累积，但只保存选定的物理状态，用于后续对比或写回 ODB。

<p align="center">
  <img src="docs/images/cpfem-postprocess.png" width="72%" alt="Abaqus CPFEM 后处理">
</p>

### 3. ParaView — 重构 PEEQCP

导出的 PVD/VTU 可以直接在 ParaView 中打开。下面示例显示摩擦/CPFEM 模型中的重构 PEEQCP 场。

<p align="center">
  <img src="docs/images/paraview-peeqcp.png" width="95%" alt="ParaView PEEQCP 云图">
</p>

### 4. ParaView — 初始晶体学取向

Data Exporter 可以根据 INP 中每个晶粒 Material 的 Euler 角重构初始晶粒取向，并输出与 HCP-Ti IPF 相关的 ParaView 场变量。

<p align="center">
  <img src="docs/images/paraview-initial-ipf.png" width="95%" alt="ParaView 初始 IPF">
</p>

## 功能

### Abaqus Data Exporter

- ODB → **VTU/PVD** 选择性导出，用于 ParaView
- 面向大型 ODB：只读取选定实例、集合、分析步、帧和场变量
- `GrainID` 重构和 `<所有晶粒>` 虚拟集合
- 计算并导出 **von Mises 应力**
- 根据 INP 中各晶粒 Material 的 Euler 角生成 **Initial HCP-Ti IPF**
- 场变量极值 / 晶粒关联分析
- Top-N 或极值区间晶粒单独导出
- History / Curve 时历 CSV 导出
- 基于 `gnd_field.dat` 与 `SDV11–SDV28` 的 **18 个滑移系 GND 演化**
- 以首次滑动帧或前一分析步末帧为基准的滑动阶段 GND 增量

### Abaqus CPFEM Postprocess

- RP 时历提取：`U1/U2`、`RF1/RF2`、`CF1/CF2`、COF
- 根据 `Fp = SDV1–SDV9` 进行逐帧 PEEQCP 重构
- 目标状态保存：
  - 下压 / 法向加载分析步：首帧 + 末帧
  - 每个摩擦循环：按 StepTime 取 **T0/T25/T50/T75/T100**
- 如果目标 StepTime 没有恰好对应输出帧，则自动匹配最接近的真实 ODB Frame
- 可将 PEEQCP 写回这些目标帧
- Linux 版本支持实时进度日志和计算/写回完成提示

## 仓库结构

```text
src/
  data_exporter/
    backend/     # Abaqus-Python ODB 后端
    windows/     # PowerShell/WPF 界面
    linux/       # Python/Tk 界面
  postprocess/
    backend/     # History + PEEQCP 后端
    windows/     # PowerShell 界面
    linux/       # Python/Tk 界面
packaging/linux/ # Linux 桌面安装/卸载脚本
scripts/         # Release 打包脚本
docs/            # 方法和安装说明
examples/        # 小型、非专有示例文件
```

## 运行要求

- 已获得合法许可并安装的 Abaqus，且能够使用 `odbAccess`
- 可执行 Abaqus 命令，例如 `abaqus` 或 `abq2024`
- ParaView，用于 VTU/PVD 可视化
- Windows：Windows PowerShell / WPF
- Linux GUI：Python 3 + Tkinter

如果 Linux 中的 Abaqus 通过 Singularity/Apptainer 容器运行，可以在软件的 **Abaqus command** 中填写完整命令前缀，例如：

```bash
singularity exec /path/to/abaqus2024.sif /opt/run_abaqus.sh
```

软件会自动在后面追加 `python <backend.py> ...`，因此不需要再手动添加 `cae -mesa`。

## 重要模型假设

部分 CPFEM 功能与当前 UMAT 的变量定义直接相关，并不是 Abaqus 通用定义。

当前 GND 映射假设：

- `SDV11–SDV28` 为 18 个滑移系的 GND 密度
- `gnd_field.dat` 第 1 列为 Abaqus element label
- 第 2–10 列为 9 个初始 GND / Burgers 方向密度
- 每个方向平均分配到对应的两个滑移系

使用其他 UMAT 前，请先阅读 [GND 映射说明](docs/gnd_mapping.md) 并确认 SDV 定义一致。

PEEQCP 重构假设 `SDV1–SDV9` 按当前文档中的 Fortran 列主序保存 `Fp`。详细方法见 [PEEQCP 方法说明](docs/peeqcp.md)。

## 安装说明

- [Windows 安装说明](docs/install-windows.md)
- [Linux 安装说明](docs/install-linux.md)

普通用户建议直接下载 **Releases** 中的打包文件。

## 构建 Release 包

在普通 Python 3 环境运行：

```bash
python scripts/build_release.py
```

生成的 ZIP 将写入 `dist/`，该目录不会提交到 Git。

## 开发状态

当前为首个公开源码版本 `v0.1.0`。项目最初来源于内部科研后处理工作流，目前正在逐步泛化和完善。

如果遇到 Abaqus 版本兼容、特定单元类型、场变量映射或工作流问题，欢迎通过 GitHub **Issues** 提交。

## 许可证

MIT License，详见 [LICENSE](LICENSE)。
