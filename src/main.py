# ====== 主入口 ======
import pygame
import sys
import time
from config import COLORS
from game_state import GameState
from renderer import Renderer
from ui import get_difficulty, show_rules, show_win, show_death
from difficulty import DIFFICULTY_CONFIG

def rechoose_difficulty(state, renderer):
    from ui import get_difficulty, show_rules
    new_diff = get_difficulty("🎯 重新选择难度")
    if new_diff is not None:
        state.difficulty = new_diff
        state.config = DIFFICULTY_CONFIG[new_diff]
        state.rows = state.config['size']
        state.cols = state.config['size']
        state.max_walls = state.config['max_walls']
        state.extra_paths = state.config['extra_paths']
        state.hint_duration = state.config['hint_time']
        state.hint_cooldown = state.config['hint_cooldown']
        state.exit_x = state.rows - 2
        state.exit_y = state.cols - 2
        state.visited_path = [(1, 1)]
        state._generate_maze()
        state.player_x, state.player_y = 1, 1
        state.steps = 0
        state.wall_hits = 0
        state.game_won = False
        state.game_over = False
        state.waiting_for_popup = False
        state.show_hint = False
        state.hint_active = False
        state.hint_timer = 0
        state.hint_cooldown_timer = 0
        state.hint_uses = 0

        renderer.cell_size = renderer.calculate_cell_size(state.rows, state.cols)
        renderer.width = state.cols * renderer.cell_size
        renderer.height = state.rows * renderer.cell_size + 60
        renderer.screen = pygame.display.set_mode((renderer.width, renderer.height))
        pygame.display.set_caption(f"{state.difficulty} - {state.rows}×{state.rows} 迷宫")
        show_rules(state.max_walls, state.hint_duration, state.hint_cooldown)
        return
