# 简介

- [简介](#简介)
- [配置](#配置)
- [选择 Python 解释器](#选择-python-解释器)
- [包的安装和使用](#包的安装和使用)
  - [创建虚拟环境](#创建虚拟环境)
    - [安装特定版本的包](#安装特定版本的包)
- [Debug](#debug)

2021-02-20, 11:43
***

VS Code 支持 Python，各种扩展程序使得 VS Code 成为一个高效而简单的 Python IDE。

下面按照如下流程介绍如何在 VS Code 中使用 Python：
- 为 VSCode 安装 Python 扩展
- 安装 Python 3
- 编写、运行、调试 Python "Hello World" 程序
- 安装 packages
- 编写绘图脚本


# 配置
除了 VS Code，还需要安装：
- Python 扩展
- Python 3

# 选择 Python 解释器
Python 是一种解释型语言，要运行 Python 代码、获得 IntelliSense 支持，必须告诉 VS Code 使用哪个解释器。

使用 `Python: Select Interpreter` 命令检索并选择合适的解释器。

或者使用状态栏的 **Select Python Environment** 选项选择解释器。

![](images/2019-11-23-15-07-06.png)


# 包的安装和使用
在 Python，工具包一般通过 [PyPI](https://pypi.org/) 安装。

## 创建虚拟环境
一般不建议将工具包安装在 global 解释器环境，使用 project-specific 包含 global 解释器副本的虚拟环境。这样，安装的工具包都在当前项目中，这样可以很好的避免包冲突的问题。

创建虚拟环境的方式：
Windows
```
py -3 -m venv .venv
```
创建成功后，会出现弹窗，提示选择虚拟环境为解释器：

![](images/2019-11-23-15-25-51.png)



安装包流程：
1. 通过 **Terminal: Create New Integrated Terminal** (``Ctrl+Shift+` ``) 打开终端




2. 

```py
# Don't use with Anaconda distributions because they include matplotlib already.

# macOS
python3 -m pip install matplotlib

# Windows (may require elevation)
python -m pip install matplotlib

# Linux (Debian)
apt-get install python3-tk
python3 -m pip install matplotlib
```
### 安装特定版本的包
```py
pip install --force-reinstall pytest==5.0.1
```

# Debug

不同图标的含义：
- continue (F5)
- step over (F10)
- step into (F11)
- step out (Shift+F11)
- restart (Ctrl+Shift+F5)
- stop (Shift+F5)

![](images/2020-01-09-22-18-01.png)

