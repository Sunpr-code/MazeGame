# 🏰 迷宫探险 (Maze Explorer)

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/Pygame-2.6.1-green.svg)](https://www.pygame.org/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Release](https://img.shields.io/badge/Release-v1.0-orange.svg)](https://github.com/yourusername/maze-game/releases)

> 一个用 Python + Pygame 开发的随机迷宫探险游戏。支持难度选择、撞墙死亡机制、智能提示系统！

---

## 🎮 游戏截图

<div align='center'><img src="./屏幕截图 2026-08-28 175903.png" style="width:400px;" /></div>


---

## ✨ 功能特点

| 功能 | 说明 |
|------|------|
| 🗺️ **随机迷宫** | 使用 DFS 算法生成，**保证有解** |
| 🎯 **5 种难度** | 简单 ~ 地狱，适配不同水平玩家 |
| 💀 **死亡机制** | 撞墙次数用完即死，紧张刺激 |
| 🔍 **智能提示** | 按 H 激活，显示方向指引（计时 + 冷却） |
| 👣 **路径记忆** | 走过的路会留下标记，防止绕圈 |
| 📱 **自适应窗口** | 自动适配屏幕大小（11×11 ~ 81×81） |
| 📦 **独立 EXE** | 无需 Python 环境，双击即玩 |
| 🎨 **精美 UI** | 彩色图形界面，流畅 60FPS |

---

## 🎯 操作说明

| 按键 | 功能 |
|:----:|------|
| `W` / `↑` | 向上移动 |
| `S` / `↓` | 向下移动 |
| `A` / `←` | 向左移动 |
| `D` / `→` | 向右移动 |
| `H` | 激活提示（显示方向指引） |
| `R` | 重新选择难度 |
| `Q` | 退出游戏 |

---

## 🎯 难度配置

| 难度 | 迷宫大小 | 撞墙上限 | 提示持续 | 提示冷却 | 适合人群 |
|:----:|:--------:|:--------:|:--------:|:--------:|----------|
| 简单 | 11×11 | 5 次 | 30 秒 | 10 秒 | 新手入门 |
| 普通 | 21×21 | 8 次 | 25 秒 | 12 秒 | 休闲娱乐 ⭐ |
| 困难 | 31×31 | 12 次 | 20 秒 | 15 秒 | 挑战自我 |
| 专家 | 51×51 | 8 次 | 15 秒 | 18 秒 | 硬核玩家 |
| 地狱 | 81×81 | 5 次 | 10 秒 | 20 秒 | 极限挑战 ⚠️ |

---

## 📦 安装与运行

### 🔹 方式一：直接运行 EXE（推荐）

1. 前往 [Releases](https://github.com/Sunpr-code/maze-game/releases) 下载 `maze.exe`
2. 双击运行，无需安装任何环境

### 🔹 方式二：运行 Python 源码

```bash
# 1. 克隆仓库
git clone https://github.com/yourusername/maze-game.git
cd maze-game

# 2. 安装依赖
pip install pygame

# 3. 运行游戏
python maze.py
