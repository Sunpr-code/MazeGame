# ====== UI 弹窗模块 ======
import tkinter as tk
from tkinter import messagebox, simpledialog
from src.difficulty import DIFFICULTY_CONFIG

def get_difficulty(title="🎯 选择难度"):
    root = tk.Tk()
    root.withdraw()

    diff_names = list(DIFFICULTY_CONFIG.keys())
    options = []
    for i, name in enumerate(diff_names, 1):
        config = DIFFICULTY_CONFIG[name]
        desc = f"{config['desc']} | 提示{config['hint_time']}秒"
        options.append(f"{i}. {name} - {desc}")

    while True:
        try:
            choice = simpledialog.askstring(
                title,
                f"请选择难度等级：\n\n" + "\n".join(options) +
                f"\n\n请输入数字 (1-{len(diff_names)})：",
                initialvalue="2"
            )
            if choice is None:
                root.destroy()
                return None
            idx = int(choice.strip()) - 1
            if 0 <= idx < len(diff_names):
                selected = diff_names[idx]
                root.destroy()
                return selected
            messagebox.showwarning("无效选择", f"请输入 1-{len(diff_names)} 之间的数字！")
        except ValueError:
            messagebox.showerror("输入错误", "请输入有效的数字！")

def show_rules(max_walls, hint_time, hint_cooldown):
    root = tk.Tk()
    root.withdraw()
    rules = f"""
🎯 迷宫游戏规则

目标：找到出口（E）

⚠️ 死亡机制：
撞墙 {max_walls} 次 → 游戏结束 💀

🔍 提示系统（按 H 激活）：
• 激活后显示 {hint_time} 秒方向指引
• 冷却时间 {hint_cooldown} 秒

操作说明：
WASD / 方向键 - 移动
H - 激活提示
R - 重新选择难度
Q - 退出游戏
"""
    messagebox.showinfo("🎯 迷宫游戏 - 规则说明", rules)
    root.destroy()

def show_wall_warning(wall_count, max_walls):
    root = tk.Tk()
    root.withdraw()
    remaining = max_walls - wall_count
    message = f"🧱 撞墙了！\n\n剩余撞墙次数：{remaining}/{max_walls}"
    if remaining <= 2:
        message += "\n\n⚠️ 警告：撞墙次数即将用完！"
    messagebox.showwarning("🧱 撞墙了！", message)
    root.destroy()

def show_death(steps, size, wall_count, max_walls):
    root = tk.Tk()
    root.withdraw()
    message = f"""
💀 你死了！
撞墙次数已达上限（{max_walls} 次）！
迷宫大小：{size}×{size}
已走步数：{steps}
撞墙次数：{wall_count}/{max_walls}
游戏结束...
"""
    result = messagebox.askyesno("💀 游戏结束", message + "\n\n是否重新开始？")
    root.destroy()
    return result

def show_win(steps, size, wall_count, hint_uses):
    root = tk.Tk()
    root.withdraw()
    message = f"""
🎉 恭喜通关！
成功走出 {size}×{size} 迷宫！
步数：{steps}
撞墙次数：{wall_count} 次
使用提示次数：{hint_uses} 次
太棒了！👏
"""
    result = messagebox.askyesno("🎉 恭喜通关！", message + "\n\n是否再来一局？")
    root.destroy()
    return result
