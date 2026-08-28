# ====== 配置、常量、颜色 ======
import pygame
import ctypes

# 颜色
COLORS = {
    'wall': (30, 30, 50),
    'path': (180, 180, 160),
    'player': (255, 200, 50),
    'exit': (50, 200, 50),
    'bg': (20, 20, 35),
    'ui_bg': (15, 15, 30),
    'danger': (255, 50, 50),
    'progress_good': (50, 255, 50),
    'progress_warn': (255, 200, 50),
    'hint_arrow': (255, 255, 50),
    'hint_ready': (100, 255, 100),
    'hint_cooldown': (255, 100, 100),
}

def calculate_cell_size(rows, cols):
    """根据迷宫大小自动计算格子尺寸"""
    user32 = ctypes.windll.user32
    screen_width = user32.GetSystemMetrics(0)
    screen_height = user32.GetSystemMetrics(1)

    margin = 40
    ui_height = 70
    max_width = screen_width - margin * 2
    max_height = screen_height - margin * 2 - ui_height

    cell_w = max_width // cols
    cell_h = max_height // rows
    cell_size = min(cell_w, cell_h)

    if cell_size < 4:
        cell_size = 4
    if rows >= 50:
        cell_size = min(cell_size, 12)
    if rows >= 70:
        cell_size = min(cell_size, 9)
    if rows >= 81:
        cell_size = min(cell_size, 7)
    if cell_size > 60:
        cell_size = 60

    return max(4, cell_size)
