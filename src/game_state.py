# ====== 游戏状态管理 ======
import time
from difficulty import DIFFICULTY_CONFIG
from maze_gen import generate_solvable_maze, shortest_path_length
from ui import show_wall_warning

class GameState:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.config = DIFFICULTY_CONFIG[difficulty]

        self.rows = self.config['size']
        self.cols = self.config['size']
        self.max_walls = self.config['max_walls']
        self.extra_paths = self.config['extra_paths']
        self.hint_duration = self.config['hint_time']
        self.hint_cooldown = self.config['hint_cooldown']

        self.maze = None
        self.path_len = 0
        self.player_x = 1
        self.player_y = 1
        self.exit_x = self.rows - 2
        self.exit_y = self.cols - 2
        self.steps = 0
        self.wall_hits = 0
        self.game_won = False
        self.game_over = False
        self.waiting_for_popup = False
        self.popup_type = None

        self.show_hint = False
        self.hint_direction = None
        self.hint_active = False
        self.hint_timer = 0
        self.hint_cooldown_timer = 0
        self.hint_uses = 0

        self.visited_path = [(1, 1)]
        self._generate_maze()

    def _generate_maze(self):
        print(f"正在生成 {self.difficulty} 迷宫...")
        start = time.time()
        self.maze = generate_solvable_maze(self.rows, self.cols, self.extra_paths)
        self.path_len = shortest_path_length(self.maze, (1, 1), (self.rows-2, self.cols-2))
        print(f"生成完成！最短路径: {self.path_len} 步")

    def reset(self):
        self.player_x, self.player_y = 1, 1
        self.steps = 0
        self.wall_hits = 0
        self.game_won = False
        self.game_over = False
        self.waiting_for_popup = False
        self.popup_type = None
        self.show_hint = False
        self.hint_direction = None
        self.hint_active = False
        self.hint_timer = 0
        self.hint_cooldown_timer = 0
        self.hint_uses = 0
        self.visited_path = [(1, 1)]
        self._generate_maze()

    def move_player(self, dx, dy):
        if self.game_won or self.game_over:
            return

        new_x = self.player_x + dx
        new_y = self.player_y + dy

        if new_x < 0 or new_x >= self.cols or new_y < 0 or new_y >= self.rows:
            return

        if self.maze[new_y][new_x] == '#':
            self.wall_hits += 1
            if self.wall_hits >= self.max_walls:
                self.game_over = True
                self.waiting_for_popup = True
                self.popup_type = 'death'
                return
            show_wall_warning(self.wall_hits, self.max_walls)
            return

        self.player_x, self.player_y = new_x, new_y
        self.steps += 1

        if (self.player_x, self.player_y) not in self.visited_path:
            self.visited_path.append((self.player_x, self.player_y))
        if len(self.visited_path) > 100:
            self.visited_path = self.visited_path[-100:]

        if self.player_x == self.exit_x and self.player_y == self.exit_y:
            self.game_won = True
            self.waiting_for_popup = True
            self.popup_type = 'win'

    def activate_hint(self):
        if not self.show_hint:
            self.show_hint = True
            self.hint_active = True
            self.hint_timer = self.hint_duration
            self.hint_uses += 1
            return True
        else:
            if self.hint_cooldown_timer > 0 or self.hint_timer > 0:
                return False
            self.hint_active = True
            self.hint_timer = self.hint_duration
            self.hint_uses += 1
            return True

    def update_timers(self, dt):
        if self.show_hint:
            if self.hint_cooldown_timer > 0:
                self.hint_cooldown_timer -= dt
                if self.hint_cooldown_timer < 0:
                    self.hint_cooldown_timer = 0
            elif self.hint_active and self.hint_timer > 0:
                self.hint_timer -= dt
                if self.hint_timer <= 0:
                    self.hint_timer = 0
                    self.hint_active = False
                    self.hint_direction = None
                    self.hint_cooldown_timer = self.hint_cooldown

    def get_remaining_walls(self):
        return self.max_walls - self.wall_hits
