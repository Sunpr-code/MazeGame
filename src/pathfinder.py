# ====== 寻路算法（BFS） ======

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

def get_next_direction(maze, start, end, visited_path):
    """
    智能寻路：优先走新路，必要时允许走回头路
    三级降级策略
    """
    rows, cols = len(maze), len(maze[0])

    # 方法1：避开走过的路
    visited1 = [[False]*cols for _ in range(rows)]
    for (px, py) in visited_path[:-1]:
        visited1[px][py] = True
    result1 = bfs_find_path(maze, start, end, visited1)
    if result1 is not None:
        return result1

    # 方法2：只避开最近5步
    visited2 = [[False]*cols for _ in range(rows)]
    recent_len = min(5, len(visited_path))
    for (px, py) in visited_path[-recent_len:]:
        visited2[px][py] = True
    result2 = bfs_find_path(maze, start, end, visited2)
    if result2 is not None:
        return result2

    # 方法3：完全不带记忆
    visited3 = [[False]*cols for _ in range(rows)]
    return bfs_find_path(maze, start, end, visited3)
