# ====== 迷宫生成算法（DFS） ======
import random

def generate_maze(rows, cols):
    """DFS生成迷宫"""
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
    """随机打通额外的墙"""
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
    """BFS检查迷宫是否有解"""
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
    """生成保证有解的迷宫"""
    for _ in range(100):
        maze = generate_maze(rows, cols)
        maze[1][1] = '.'
        maze[rows-2][cols-2] = '.'
        maze = add_extra_paths(maze, rows, cols, extra_paths)
        if has_solution(maze, (1, 1), (rows-2, cols-2)):
            return maze

    # 降级方案
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

def shortest_path_length(maze, start, end):
    """计算最短路径长度"""
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
