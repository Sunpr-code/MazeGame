import pygame
import sys
import tkinter as tk
from tkinter import messagebox, simpledialog
import random
import time

# ====== 难度配置 ======
DIFFICULTY_CONFIG = {
    '简单': {
        'size': 11, 
        'max_walls': 5, 
        'extra_paths': 8, 
        'desc': '11×11，允许撞墙5次',
        'hint_time': 30,
        'hint_cooldown': 10
    },
    '普通': {
        'size': 21, 
        'max_walls': 8, 
        'extra_paths': 15, 
        'desc': '21×21，允许撞墙8次',
        'hint_time': 25,
        'hint_cooldown': 12
    },
    '困难': {
        'size': 31, 
        'max_walls': 12, 
        'extra_paths': 25, 
        'desc': '31×31，允许撞墙12次',
        'hint_time': 20,
        'hint_cooldown': 15
    },
    '专家': {
        'size': 51, 
        'max_walls': 8, 
        'extra_paths': 40, 
        'desc': '51×51，允许撞墙8次',
        'hint_time': 15,
        'hint_cooldown': 18
    },
    '地狱': {
        'size': 81, 
        'max_walls': 5, 
        'extra_paths': 60, 
        'desc': '81×81，允许撞墙5次',
        'hint_time': 10,
        'hint_cooldown': 20
    }
}

def get_difficulty(title="🎯 选择难度"):
    root = tk.Tk()
    root.withdraw()
    
    diff_names = list(DIFFICULTY_CONFIG.keys())
    options = []
    for i, name in enumerate(diff_names, 1):
        config = DIFFICULTY_CONFIG[name]
        desc = f"{config['desc']} | 提示{config['hint_time']}秒"
        options.append(f"{i}. {name} - {desc}")
    
    options_str = "\n".join(options)
    
    while True:
        try:
            choice = simpledialog.askstring(
                title,
                f"请选择难度等级：\n\n{options_str}\n\n请输入数字 (1-{len(diff_names)})：",
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
• 智能避让已走过的路

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

# ====== 迷宫生成 ======
def generate_maze(rows, cols):
    maze = [['#' for _ in range(cols)] for _ in range(rows)]
    stack = [(1, 1)]
    maze[1][1] = '.'
    dirs = [(-2, 0), (2, 0), (0, -2), (0, 2)]
    
    while stack:
        x, y = stack[-1]
        random.shuffle(dirs)
        moved = False
        for dx, dy in dirs:
            nx, ny = x + dx, y + dy
            if 1 <= nx < rows-1 and 1 <= ny < cols-1 and maze[nx][ny] == '#':
                maze[x + dx//2][y + dy//2] = '.'
                maze[nx][ny] = '.'
                stack.append((nx, ny))
                moved = True
                break
        if not moved:
            stack.pop()
    return maze

def add_extra_paths(maze, rows, cols, extra_count):
    candidates = []
    for r in range(1, rows-1):
        for c in range(1, cols-1):
            if maze[r][c] == '#':
                paths = 0
                if maze[r-1][c] == '.': paths += 1
                if maze[r+1][c] == '.': paths += 1
                if maze[r][c-1] == '.': paths += 1
                if maze[r][c+1] == '.': paths += 1
                if paths >= 2:
                    candidates.append((r, c))
    
    random.shuffle(candidates)
    for i in range(min(extra_count, len(candidates))):
        r, c = candidates[i]
        maze[r][c] = '.'
    return maze

def has_solution(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False]*cols for _ in range(rows)]
    queue = [(start[0], start[1])]
    visited[start[0]][start[1]] = True
    dirs = [(0,1), (0,-1), (1,0), (-1,0)]
    
    while queue:
        x, y = queue.pop(0)
        if (x, y) == end:
            return True
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny] and maze[nx][ny] == '.':
                    visited[nx][ny] = True
                    queue.append((nx, ny))
    return False

def generate_solvable_maze(rows, cols, extra_paths=20):
    for attempt in range(100):
        maze = generate_maze(rows, cols)
        maze[1][1] = '.'
        maze[rows-2][cols-2] = '.'
        maze = add_extra_paths(maze, rows, cols, extra_paths)
        if has_solution(maze, (1, 1), (rows-2, cols-2)):
            return maze
    
    maze = [['#' for _ in range(cols)] for _ in range(rows)]
    for i in range(1, rows-1):
        maze[i][1] = '.'
        maze[i][cols-2] = '.'
    for j in range(1, cols-1):
        maze[1][j] = '.'
        maze[rows-2][j] = '.'
    maze[1][1] = '.'
    maze[rows-2][cols-2] = '.'
    return maze

# ====== 修复版：智能寻路 ======
def get_next_direction(maze, start, end, visited_path):
    """智能寻路：优先走新路，必要时允许走回头路"""
    rows, cols = len(maze), len(maze[0])
    
    # 方法1：避开走过的路（探索模式）
    visited1 = [[False]*cols for _ in range(rows)]
    for (px, py) in visited_path[:-1]:  # 不包括当前位置
        visited1[px][py] = True
    
    result1 = bfs_find_path(maze, start, end, visited1)
    if result1 is not None:
        return result1
    
    # 方法2：如果探索模式找不到，允许走回头路（逃生模式）
    visited2 = [[False]*cols for _ in range(rows)]
    # 只标记最近的几个位置，防止死循环
    recent_len = min(5, len(visited_path))
    for (px, py) in visited_path[-recent_len:]:
        visited2[px][py] = True
    
    result2 = bfs_find_path(maze, start, end, visited2)
    if result2 is not None:
        return result2
    
    # 方法3：完全不带记忆（最后手段）
    visited3 = [[False]*cols for _ in range(rows)]
    return bfs_find_path(maze, start, end, visited3)

def bfs_find_path(maze, start, end, visited):
    """BFS寻路，返回第一步方向"""
    rows, cols = len(maze), len(maze[0])
    queue = [(start[0], start[1], None)]
    visited[start[0]][start[1]] = True
    
    dirs = [(-1, 0, '↑'), (1, 0, '↓'), (0, -1, '←'), (0, 1, '→')]
    
    while queue:
        x, y, first_dir = queue.pop(0)
        
        if (x, y) == end:
            return first_dir
        
        for dx, dy, label in dirs:
            nx, ny = x + dx, y + dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny] and maze[nx][ny] == '.':
                    visited[nx][ny] = True
                    next_dir = label if first_dir is None else first_dir
                    queue.append((nx, ny, next_dir))
    
    return None

def shortest_path_length(maze, start, end):
    rows, cols = len(maze), len(maze[0])
    visited = [[False]*cols for _ in range(rows)]
    queue = [(start[0], start[1], 0)]
    visited[start[0]][start[1]] = True
    dirs = [(0,1), (0,-1), (1,0), (-1,0)]
    
    while queue:
        x, y, dist = queue.pop(0)
        if (x, y) == end:
            return dist
        for dx, dy in dirs:
            nx, ny = x+dx, y+dy
            if 0 <= nx < rows and 0 <= ny < cols:
                if not visited[nx][ny] and maze[nx][ny] == '.':
                    visited[nx][ny] = True
                    queue.append((nx, ny, dist+1))
    return -1

def calculate_cell_size(rows, cols):
    import ctypes
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

# ====== 全局变量 ======
pygame.init()
clock = pygame.time.Clock()

def init_game(difficulty):
    global ROWS, COLS, MAX_WALLS, EXTRA_PATHS, CELL_SIZE
    global WINDOW_WIDTH, WINDOW_HEIGHT, screen
    global maze, path_len, player_x, player_y, exit_x, exit_y
    global steps, wall_hits, game_won, game_over, waiting_for_popup, popup_type
    global show_hint, hint_direction, hint_timer, hint_cooldown_timer
    global hint_active, hint_uses, HINT_DURATION, HINT_COOLDOWN
    global visited_path
    
    config = DIFFICULTY_CONFIG[difficulty]
    ROWS = config['size']
    COLS = config['size']
    MAX_WALLS = config['max_walls']
    EXTRA_PATHS = config['extra_paths']
    HINT_DURATION = config['hint_time']
    HINT_COOLDOWN = config['hint_cooldown']
    
    print(f"难度: {difficulty}")
    print(f"迷宫大小: {ROWS}×{ROWS}")
    print(f"最大撞墙次数: {MAX_WALLS}")
    print(f"提示持续时间: {HINT_DURATION}秒")
    print(f"提示冷却: {HINT_COOLDOWN}秒")
    
    CELL_SIZE = calculate_cell_size(ROWS, COLS)
    WINDOW_WIDTH = COLS * CELL_SIZE
    WINDOW_HEIGHT = ROWS * CELL_SIZE + 60
    
    print(f"格子大小: {CELL_SIZE}px")
    print(f"窗口尺寸: {WINDOW_WIDTH}×{WINDOW_HEIGHT}")
    
    screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
    pygame.display.set_caption(f"{difficulty} - {ROWS}×{ROWS} 迷宫")
    
    print("正在生成迷宫...")
    start_time = time.time()
    maze = generate_solvable_maze(ROWS, COLS, EXTRA_PATHS)
    gen_time = time.time() - start_time
    
    player_x, player_y = 1, 1
    exit_x, exit_y = ROWS - 2, COLS - 2
    steps = 0
    wall_hits = 0
    game_won = False
    game_over = False
    waiting_for_popup = False
    popup_type = None
    show_hint = False
    hint_direction = None
    hint_active = False
    hint_timer = 0
    hint_cooldown_timer = 0
    hint_uses = 0
    visited_path = [(player_x, player_y)]
    
    path_len = shortest_path_length(maze, (1, 1), (ROWS-2, COLS-2))
    pygame.display.set_caption(f"{difficulty} - {ROWS}×{ROWS} 迷宫 (最短:{path_len}步)")
    
    print(f"迷宫生成完成！用时: {gen_time:.2f}秒")
    print(f"最短路径长度: {path_len} 步")
    print("-" * 40)
    
    return screen

def reset_game():
    global maze, player_x, player_y, steps, game_won, game_over
    global exit_x, exit_y, path_len, wall_hits, waiting_for_popup, popup_type
    global show_hint, hint_direction, hint_timer, hint_cooldown_timer
    global hint_active, hint_uses, visited_path
    
    print(f"正在生成新 {difficulty} 迷宫...")
    start_time = time.time()
    maze = generate_solvable_maze(ROWS, COLS, EXTRA_PATHS)
    gen_time = time.time() - start_time
    
    player_x, player_y = 1, 1
    exit_x, exit_y = ROWS - 2, COLS - 2
    steps = 0
    wall_hits = 0
    game_won = False
    game_over = False
    waiting_for_popup = False
    popup_type = None
    show_hint = False
    hint_direction = None
    hint_active = False
    hint_timer = 0
    hint_cooldown_timer = 0
    hint_uses = 0
    visited_path = [(player_x, player_y)]
    
    path_len = shortest_path_length(maze, (1, 1), (ROWS-2, COLS-2))
    pygame.display.set_caption(f"{difficulty} - {ROWS}×{ROWS} 迷宫 (最短:{path_len}步)")
    print(f"新迷宫生成完成！用时: {gen_time:.2f}秒，最短: {path_len}步")

def rechoose_difficulty():
    global difficulty, screen
    new_diff = get_difficulty("🎯 重新选择难度")
    if new_diff is not None:
        difficulty = new_diff
        screen = init_game(difficulty)
        show_rules(MAX_WALLS, HINT_DURATION, HINT_COOLDOWN)
        return True
    return False

print("🎯 迷宫游戏启动！")

difficulty = get_difficulty()
if difficulty is None:
    print("用户取消，退出游戏")
    sys.exit()

screen = init_game(difficulty)
show_rules(MAX_WALLS, HINT_DURATION, HINT_COOLDOWN)

# ====== 颜色 ======
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

font_size = max(14, min(24, CELL_SIZE // 2))
font = pygame.font.Font(None, font_size)
small_font = pygame.font.Font(None, max(10, font_size - 4))

# ====== 状态变量 ======
show_hint = False
hint_direction = None
hint_active = False
hint_timer = 0
hint_cooldown_timer = 0
hint_uses = 0
visited_path = [(1, 1)]

def draw_maze():
    for row in range(ROWS):
        for col in range(COLS):
            x = col * CELL_SIZE
            y = row * CELL_SIZE
            color = COLORS['wall'] if maze[row][col] == '#' else COLORS['path']
            pygame.draw.rect(screen, color, (x, y, CELL_SIZE, CELL_SIZE))

def draw_visited_path():
    """绘制走过的路径"""
    if len(visited_path) <= 1:
        return
    
    for idx, (px, py) in enumerate(visited_path[:-1]):
        x = px * CELL_SIZE + CELL_SIZE // 2
        y = py * CELL_SIZE + CELL_SIZE // 2
        radius = max(2, CELL_SIZE // 6)
        
        # 渐变色：新走的路更亮
        alpha = int(50 + 30 * (idx / max(1, len(visited_path))))
        alpha = min(80, alpha)
        
        surf = pygame.Surface((CELL_SIZE, CELL_SIZE), pygame.SRCALPHA)
        pygame.draw.circle(surf, (255, 200, 80, alpha), 
                          (CELL_SIZE//2, CELL_SIZE//2), radius)
        screen.blit(surf, (px * CELL_SIZE, py * CELL_SIZE))

def draw_player():
    cx = player_x * CELL_SIZE + CELL_SIZE // 2
    cy = player_y * CELL_SIZE + CELL_SIZE // 2
    radius = max(2, CELL_SIZE // 2 - 4)
    
    glow = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
    for i in range(3, 0, -1):
        alpha = 30 + i * 20
        pygame.draw.circle(glow, (255, 200, 50, alpha),
                          (CELL_SIZE, CELL_SIZE), radius + i * 4)
    screen.blit(glow, (cx - CELL_SIZE, cy - CELL_SIZE))
    
    pygame.draw.circle(screen, COLORS['player'], (cx, cy), radius)
    pygame.draw.circle(screen, (180, 140, 30), (cx, cy), max(1, radius // 3), 2)

def draw_exit():
    cx = exit_x * CELL_SIZE + CELL_SIZE // 2
    cy = exit_y * CELL_SIZE + CELL_SIZE // 2
    radius = max(2, CELL_SIZE // 2 - 4)
    
    pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
    glow_radius = radius + int(4 * pulse)
    
    glow = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
    for i in range(4, 0, -1):
        alpha = int(30 * pulse * (i / 4))
        pygame.draw.circle(glow, (50, 255, 50, alpha),
                          (CELL_SIZE, CELL_SIZE), glow_radius + i * 4)
    screen.blit(glow, (cx - CELL_SIZE, cy - CELL_SIZE))
    
    pygame.draw.circle(screen, COLORS['exit'], (cx, cy), radius)
    pygame.draw.circle(screen, (20, 150, 20), (cx, cy), max(1, radius // 3), 2)
    
    if CELL_SIZE >= 16:
        e_text = small_font.render("E", True, (255, 255, 255))
        screen.blit(e_text, e_text.get_rect(center=(cx, cy)))

def draw_hint():
    global hint_timer, hint_active, hint_direction, show_hint
    
    if not show_hint or game_won or game_over:
        return
    
    if hint_cooldown_timer > 0:
        return
    
    if hint_timer <= 0:
        return
    
    # 使用智能寻路
    hint_direction = get_next_direction(maze, (player_x, player_y), (exit_x, exit_y), visited_path)
    
    if hint_direction is None:
        return
    
    # 验证方向
    dx_map = {'↑': (0, -1), '↓': (0, 1), '←': (-1, 0), '→': (1, 0)}
    if hint_direction in dx_map:
        dx, dy = dx_map[hint_direction]
        check_x, check_y = player_x + dx, player_y + dy
        if check_x < 0 or check_x >= COLS or check_y < 0 or check_y >= ROWS:
            return
        if maze[check_y][check_x] == '#':
            return
    
    cx = player_x * CELL_SIZE + CELL_SIZE // 2
    cy = player_y * CELL_SIZE + CELL_SIZE // 2
    
    arrow_len = max(10, CELL_SIZE // 2)
    arrow_w = max(5, CELL_SIZE // 4)
    
    if hint_direction == '↑':
        tip = (cx, cy - arrow_len)
        base_left = (cx - arrow_w, cy + arrow_w//2)
        base_right = (cx + arrow_w, cy + arrow_w//2)
    elif hint_direction == '↓':
        tip = (cx, cy + arrow_len)
        base_left = (cx - arrow_w, cy - arrow_w//2)
        base_right = (cx + arrow_w, cy - arrow_w//2)
    elif hint_direction == '←':
        tip = (cx - arrow_len, cy)
        base_left = (cx + arrow_w//2, cy - arrow_w)
        base_right = (cx + arrow_w//2, cy + arrow_w)
    elif hint_direction == '→':
        tip = (cx + arrow_len, cy)
        base_left = (cx - arrow_w//2, cy - arrow_w)
        base_right = (cx - arrow_w//2, cy + arrow_w)
    else:
        return
    
    blink = abs(pygame.time.get_ticks() % 400 - 200) / 200
    alpha_main = int(180 + 75 * blink)
    alpha_glow = int(60 + 40 * blink)
    
    points = [tip, base_left, base_right]
    
    for size in range(4, 0, -1):
        glow_surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
        glow_points = [(p[0] - cx + CELL_SIZE, p[1] - cy + CELL_SIZE) for p in points]
        pygame.draw.polygon(glow_surf, (255, 255, 50, alpha_glow // (5 - size + 1)), glow_points, size * 2)
        screen.blit(glow_surf, (cx - CELL_SIZE, cy - CELL_SIZE))
    
    arrow_surf = pygame.Surface((CELL_SIZE * 2, CELL_SIZE * 2), pygame.SRCALPHA)
    arrow_points = [(p[0] - cx + CELL_SIZE, p[1] - cy + CELL_SIZE) for p in points]
    pygame.draw.polygon(arrow_surf, (255, 255, 50, alpha_main), arrow_points)
    pygame.draw.polygon(arrow_surf, (200, 200, 0, min(255, alpha_main + 30)), arrow_points, 2)
    screen.blit(arrow_surf, (cx - CELL_SIZE, cy - CELL_SIZE))
    
    time_text = small_font.render(f"{int(hint_timer)}s", True, (255, 255, 255))
    time_x = cx + arrow_len + 8
    time_y = cy - 8
    
    bg_rect = pygame.Rect(time_x - 3, time_y - 3, 24, 18)
    pygame.draw.rect(screen, (0, 0, 0, 180), bg_rect)
    screen.blit(time_text, (time_x, time_y))

def draw_ui():
    global hint_timer, hint_active, hint_cooldown_timer, show_hint, hint_uses
    
    ui_y = ROWS * CELL_SIZE
    ui_bg = pygame.Surface((WINDOW_WIDTH, 60))
    ui_bg.set_alpha(220)
    ui_bg.fill(COLORS['ui_bg'])
    screen.blit(ui_bg, (0, ui_y))
    
    pygame.draw.line(screen, (60, 60, 80), (0, ui_y), (WINDOW_WIDTH, ui_y), 2)
    
    step_text = font.render(f"Steps: {steps}", True, (255, 255, 255))
    screen.blit(step_text, (5, ui_y + 18))
    
    remaining = MAX_WALLS - wall_hits
    if remaining <= 2:
        wall_color = COLORS['danger']
    elif remaining <= 4:
        wall_color = COLORS['progress_warn']
    else:
        wall_color = COLORS['progress_good']
    
    wall_text = font.render(f"❤️ {remaining}/{MAX_WALLS}", True, wall_color)
    screen.blit(wall_text, (120, ui_y + 18))
    
    if CELL_SIZE >= 8:
        path_text = small_font.render(f"最短:{path_len}", True, (180, 180, 200))
        screen.blit(path_text, (200, ui_y + 20))
    
    if show_hint:
        if hint_cooldown_timer > 0:
            status = f"⏳{int(hint_cooldown_timer)}s"
            color = COLORS['hint_cooldown']
        elif hint_timer > 0:
            status = f"🔍{int(hint_timer)}s"
            color = COLORS['hint_ready']
        else:
            status = "🔍Ready"
            color = COLORS['hint_ready']
        
        hint_text = small_font.render(status, True, color)
        screen.blit(hint_text, (310, ui_y + 20))
        
        use_text = small_font.render(f"x{hint_uses}", True, (180, 180, 200))
        screen.blit(use_text, (390, ui_y + 20))
    else:
        hint_text = small_font.render("Hint:OFF", True, (150, 150, 150))
        screen.blit(hint_text, (310, ui_y + 20))
    
    diff_text = small_font.render(difficulty, True, (180, 180, 200))
    screen.blit(diff_text, (WINDOW_WIDTH - 160, ui_y + 20))
    
    tip_text = small_font.render("H R Q", True, (180, 180, 200))
    screen.blit(tip_text, (WINDOW_WIDTH - 60, ui_y + 20))
    
    if game_over:
        over_text = font.render("GAME OVER", True, (255, 50, 50))
        screen.blit(over_text, over_text.get_rect(center=(WINDOW_WIDTH // 2, ui_y + 30)))
    elif game_won:
        win_text = font.render("YOU WIN!", True, (255, 215, 0))
        screen.blit(win_text, win_text.get_rect(center=(WINDOW_WIDTH // 2, ui_y + 30)))

def move_player(dx, dy):
    global player_x, player_y, steps, game_won, game_over
    global wall_hits, waiting_for_popup, popup_type, visited_path
    
    if game_won or game_over:
        return
    
    new_x, new_y = player_x + dx, player_y + dy
    
    if new_x < 0 or new_x >= COLS or new_y < 0 or new_y >= ROWS:
        return
    
    if maze[new_y][new_x] == '#':
        wall_hits += 1
        pygame.display.set_caption(f"{difficulty} - {ROWS}×{ROWS} 迷宫 (撞墙:{wall_hits}/{MAX_WALLS})")
        
        if wall_hits >= MAX_WALLS:
            game_over = True
            waiting_for_popup = True
            popup_type = 'death'
            return
        
        show_wall_warning(wall_hits, MAX_WALLS)
        return
    
    player_x, player_y = new_x, new_y
    steps += 1
    
    # 只记录最近的位置，避免路径列表过长
    if (player_x, player_y) not in visited_path:
        visited_path.append((player_x, player_y))
    
    # 限制路径列表长度（只保留最近100步）
    if len(visited_path) > 100:
        visited_path = visited_path[-100:]
    
    if player_x == exit_x and player_y == exit_y:
        game_won = True
        waiting_for_popup = True
        popup_type = 'win'

# ====== 主循环 ======
running = True
last_time = time.time()

while running:
    current_time = time.time()
    dt = current_time - last_time
    last_time = current_time
    
    if show_hint:
        if hint_cooldown_timer > 0:
            hint_cooldown_timer -= dt
            if hint_cooldown_timer < 0:
                hint_cooldown_timer = 0
        elif hint_active and hint_timer > 0:
            hint_timer -= dt
            if hint_timer <= 0:
                hint_timer = 0
                hint_active = False
                hint_direction = None
                hint_cooldown_timer = HINT_COOLDOWN
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                running = False
            elif event.key == pygame.K_r:
                if rechoose_difficulty():
                    font_size = max(14, min(24, CELL_SIZE // 2))
                    font = pygame.font.Font(None, font_size)
                    small_font = pygame.font.Font(None, max(10, font_size - 4))
            elif event.key == pygame.K_h:
                if not show_hint:
                    show_hint = True
                    hint_active = True
                    hint_timer = HINT_DURATION
                    hint_uses += 1
                    print(f"🔍 提示激活！持续 {HINT_DURATION} 秒")
                else:
                    if hint_cooldown_timer > 0:
                        print(f"⏳ 冷却中 {int(hint_cooldown_timer)}s")
                    elif hint_timer > 0:
                        print(f"🔍 已激活 {int(hint_timer)}s")
                    else:
                        hint_active = True
                        hint_timer = HINT_DURATION
                        hint_uses += 1
                        print(f"🔍 提示激活！持续 {HINT_DURATION} 秒")
            elif event.key in (pygame.K_w, pygame.K_UP):
                move_player(0, -1)
            elif event.key in (pygame.K_s, pygame.K_DOWN):
                move_player(0, 1)
            elif event.key in (pygame.K_a, pygame.K_LEFT):
                move_player(-1, 0)
            elif event.key in (pygame.K_d, pygame.K_RIGHT):
                move_player(1, 0)
    
    screen.fill(COLORS['bg'])
    draw_maze()
    draw_visited_path()
    draw_exit()
    draw_hint()
    draw_player()
    draw_ui()
    pygame.display.flip()
    clock.tick(60)
    
    if waiting_for_popup:
        waiting_for_popup = False
        if popup_type == 'win':
            if show_win(steps, ROWS, wall_hits, hint_uses):
                reset_game()
            else:
                running = False
        elif popup_type == 'death':
            if show_death(steps, ROWS, wall_hits, MAX_WALLS):
                reset_game()
            else:
                running = False

pygame.quit()
sys.exit()
