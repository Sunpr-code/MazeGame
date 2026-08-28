# ====== 渲染模块 ======
import pygame
from src.config import COLORS, calculate_cell_size
from src.pathfinder import get_next_direction

class Renderer:
    def __init__(self, state):
        self.state = state
        self.cell_size = calculate_cell_size(state.rows, state.cols)
        self.width = state.cols * self.cell_size
        self.height = state.rows * self.cell_size + 60

        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption(f"{state.difficulty} - {state.rows}×{state.rows} 迷宫")

        font_size = max(14, min(24, self.cell_size // 2))
        self.font = pygame.font.Font(None, font_size)
        self.small_font = pygame.font.Font(None, max(10, font_size - 4))

    def draw(self):
        self.screen.fill(COLORS['bg'])
        self._draw_maze()
        self._draw_visited_path()
        self._draw_exit()
        self._draw_hint()
        self._draw_player()
        self._draw_ui()
        pygame.display.flip()

    def _draw_maze(self):
        for row in range(self.state.rows):
            for col in range(self.state.cols):
                x = col * self.cell_size
                y = row * self.cell_size
                color = COLORS['wall'] if self.state.maze[row][col] == '#' else COLORS['path']
                pygame.draw.rect(self.screen, color, (x, y, self.cell_size, self.cell_size))

    def _draw_visited_path(self):
        if len(self.state.visited_path) <= 1:
            return
        for idx, (px, py) in enumerate(self.state.visited_path[:-1]):
            x = px * self.cell_size + self.cell_size // 2
            y = py * self.cell_size + self.cell_size // 2
            radius = max(2, self.cell_size // 6)
            alpha = int(50 + 30 * (idx / max(1, len(self.state.visited_path))))
            alpha = min(80, alpha)
            surf = pygame.Surface((self.cell_size, self.cell_size), pygame.SRCALPHA)
            pygame.draw.circle(surf, (255, 200, 80, alpha),
                              (self.cell_size//2, self.cell_size//2), radius)
            self.screen.blit(surf, (px * self.cell_size, py * self.cell_size))

    def _draw_player(self):
        cx = self.state.player_x * self.cell_size + self.cell_size // 2
        cy = self.state.player_y * self.cell_size + self.cell_size // 2
        radius = max(2, self.cell_size // 2 - 4)

        glow = pygame.Surface((self.cell_size * 2, self.cell_size * 2), pygame.SRCALPHA)
        for i in range(3, 0, -1):
            alpha = 30 + i * 20
            pygame.draw.circle(glow, (255, 200, 50, alpha),
                              (self.cell_size, self.cell_size), radius + i * 4)
        self.screen.blit(glow, (cx - self.cell_size, cy - self.cell_size))

        pygame.draw.circle(self.screen, COLORS['player'], (cx, cy), radius)
        pygame.draw.circle(self.screen, (180, 140, 30), (cx, cy), max(1, radius // 3), 2)

    def _draw_exit(self):
        cx = self.state.exit_x * self.cell_size + self.cell_size // 2
        cy = self.state.exit_y * self.cell_size + self.cell_size // 2
        radius = max(2, self.cell_size // 2 - 4)

        pulse = abs(pygame.time.get_ticks() % 1000 - 500) / 500
        glow_radius = radius + int(4 * pulse)

        glow = pygame.Surface((self.cell_size * 2, self.cell_size * 2), pygame.SRCALPHA)
        for i in range(4, 0, -1):
            alpha = int(30 * pulse * (i / 4))
            pygame.draw.circle(glow, (50, 255, 50, alpha),
                              (self.cell_size, self.cell_size), glow_radius + i * 4)
        self.screen.blit(glow, (cx - self.cell_size, cy - self.cell_size))

        pygame.draw.circle(self.screen, COLORS['exit'], (cx, cy), radius)
        pygame.draw.circle(self.screen, (20, 150, 20), (cx, cy), max(1, radius // 3), 2)

        if self.cell_size >= 16:
            e_text = self.small_font.render("E", True, (255, 255, 255))
            self.screen.blit(e_text, e_text.get_rect(center=(cx, cy)))

    def _draw_hint(self):
        if not self.state.show_hint or self.state.game_won or self.state.game_over:
            return
        if self.state.hint_cooldown_timer > 0 or self.state.hint_timer <= 0:
            return

        hint_dir = get_next_direction(
            self.state.maze,
            (self.state.player_x, self.state.player_y),
            (self.state.exit_x, self.state.exit_y),
            self.state.visited_path
        )
        if hint_dir is None:
            return

        dx_map = {'↑': (0, -1), '↓': (0, 1), '←': (-1, 0), '→': (1, 0)}
        if hint_dir in dx_map:
            dx, dy = dx_map[hint_dir]
            cx, cy = self.state.player_x + dx, self.state.player_y + dy
            if cx < 0 or cx >= self.state.cols or cy < 0 or cy >= self.state.rows:
                return
            if self.state.maze[cy][cx] == '#':
                return

        cx = self.state.player_x * self.cell_size + self.cell_size // 2
        cy = self.state.player_y * self.cell_size + self.cell_size // 2

        arrow_len = max(10, self.cell_size // 2)
        arrow_w = max(5, self.cell_size // 4)

        if hint_dir == '↑':
            tip = (cx, cy - arrow_len)
            base_left = (cx - arrow_w, cy + arrow_w//2)
            base_right = (cx + arrow_w, cy + arrow_w//2)
        elif hint_dir == '↓':
            tip = (cx, cy + arrow_len)
            base_left = (cx - arrow_w, cy - arrow_w//2)
            base_right = (cx + arrow_w, cy - arrow_w//2)
        elif hint_dir == '←':
            tip = (cx - arrow_len, cy)
            base_left = (cx + arrow_w//2, cy - arrow_w)
            base_right = (cx + arrow_w//2, cy + arrow_w)
        elif hint_dir == '→':
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
            glow_surf = pygame.Surface((self.cell_size * 2, self.cell_size * 2), pygame.SRCALPHA)
            glow_points = [(p[0] - cx + self.cell_size, p[1] - cy + self.cell_size) for p in points]
            pygame.draw.polygon(glow_surf, (255, 255, 50, alpha_glow // (5 - size + 1)), glow_points, size * 2)
            self.screen.blit(glow_surf, (cx - self.cell_size, cy - self.cell_size))

        arrow_surf = pygame.Surface((self.cell_size * 2, self.cell_size * 2), pygame.SRCALPHA)
        arrow_points = [(p[0] - cx + self.cell_size, p[1] - cy + self.cell_size) for p in points]
        pygame.draw.polygon(arrow_surf, (255, 255, 50, alpha_main), arrow_points)
        pygame.draw.polygon(arrow_surf, (200, 200, 0, min(255, alpha_main + 30)), arrow_points, 2)
        self.screen.blit(arrow_surf, (cx - self.cell_size, cy - self.cell_size))

        time_text = self.small_font.render(f"{int(self.state.hint_timer)}s", True, (255, 255, 255))
        time_x = cx + arrow_len + 8
        time_y = cy - 8
        bg_rect = pygame.Rect(time_x - 3, time_y - 3, 24, 18)
        pygame.draw.rect(self.screen, (0, 0, 0, 180), bg_rect)
        self.screen.blit(time_text, (time_x, time_y))

    def _draw_ui(self):
        ui_y = self.state.rows * self.cell_size
        ui_bg = pygame.Surface((self.width, 60))
        ui_bg.set_alpha(220)
        ui_bg.fill(COLORS['ui_bg'])
        self.screen.blit(ui_bg, (0, ui_y))
        pygame.draw.line(self.screen, (60, 60, 80), (0, ui_y), (self.width, ui_y), 2)

        step_text = self.font.render(f"Steps: {self.state.steps}", True, (255, 255, 255))
        self.screen.blit(step_text, (5, ui_y + 18))

        remaining = self.state.max_walls - self.state.wall_hits
        if remaining <= 2:
            wall_color = COLORS['danger']
        elif remaining <= 4:
            wall_color = COLORS['progress_warn']
        else:
            wall_color = COLORS['progress_good']
        wall_text = self.font.render(f"❤️ {remaining}/{self.state.max_walls}", True, wall_color)
        self.screen.blit(wall_text, (120, ui_y + 18))

        if self.cell_size >= 8:
            path_text = self.small_font.render(f"最短:{self.state.path_len}", True, (180, 180, 200))
            self.screen.blit(path_text, (200, ui_y + 20))

        if self.state.show_hint:
            if self.state.hint_cooldown_timer > 0:
                status = f"⏳{int(self.state.hint_cooldown_timer)}s"
                color = COLORS['hint_cooldown']
            elif self.state.hint_timer > 0:
                status = f"🔍{int(self.state.hint_timer)}s"
                color = COLORS['hint_ready']
            else:
                status = "🔍Ready"
                color = COLORS['hint_ready']
            hint_text = self.small_font.render(status, True, color)
            self.screen.blit(hint_text, (310, ui_y + 20))
            use_text = self.small_font.render(f"x{self.state.hint_uses}", True, (180, 180, 200))
            self.screen.blit(use_text, (390, ui_y + 20))
        else:
            hint_text = self.small_font.render("Hint:OFF", True, (150, 150, 150))
            self.screen.blit(hint_text, (310, ui_y + 20))

        diff_text = self.small_font.render(self.state.difficulty, True, (180, 180, 200))
        self.screen.blit(diff_text, (self.width - 160, ui_y + 20))
        tip_text = self.small_font.render("H R Q", True, (180, 180, 200))
        self.screen.blit(tip_text, (self.width - 60, ui_y + 20))

        if self.state.game_over:
            over_text = self.font.render("GAME OVER", True, (255, 50, 50))
            self.screen.blit(over_text, over_text.get_rect(center=(self.width // 2, ui_y + 30)))
        elif self.state.game_won:
            win_text = self.font.render("YOU WIN!", True, (255, 215, 0))
            self.screen.blit(win_text, win_text.get_rect(center=(self.width // 2, ui_y + 30)))
