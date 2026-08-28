# ====== 主入口 ======
import pygame
import sys
import time
from src.config import COLORS
from src.game_state import GameState
from src.renderer import Renderer
from src.ui import get_difficulty, show_rules, show_win, show_death
from src.difficulty import DIFFICULTY_CONFIG

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
        return True
    return False

def main():
    print("🎯 迷宫游戏启动！")

    difficulty = get_difficulty()
    if difficulty is None:
        print("用户取消，退出游戏")
        return

    pygame.init()
    clock = pygame.time.Clock()

    state = GameState(difficulty)
    renderer = Renderer(state)

    show_rules(state.max_walls, state.hint_duration, state.hint_cooldown)

    running = True
    last_time = time.time()

    while running:
        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        state.update_timers(dt)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_r:
                    if rechoose_difficulty(state, renderer):
                        pass
                elif event.key == pygame.K_h:
                    if state.activate_hint():
                        print(f"🔍 提示激活！持续 {state.hint_duration} 秒")
                    else:
                        if state.hint_cooldown_timer > 0:
                            print(f"⏳ 冷却中 {int(state.hint_cooldown_timer)}s")
                        elif state.hint_timer > 0:
                            print(f"🔍 已激活 {int(state.hint_timer)}s")
                elif event.key in (pygame.K_w, pygame.K_UP):
                    state.move_player(0, -1)
                elif event.key in (pygame.K_s, pygame.K_DOWN):
                    state.move_player(0, 1)
                elif event.key in (pygame.K_a, pygame.K_LEFT):
                    state.move_player(-1, 0)
                elif event.key in (pygame.K_d, pygame.K_RIGHT):
                    state.move_player(1, 0)

        renderer.draw()
        clock.tick(60)

        if state.waiting_for_popup:
            state.waiting_for_popup = False
            if state.popup_type == 'win':
                if show_win(state.steps, state.rows, state.wall_hits, state.hint_uses):
                    state.reset()
                    renderer.__init__(state)
                else:
                    running = False
            elif state.popup_type == 'death':
                if show_death(state.steps, state.rows, state.wall_hits, state.max_walls):
                    state.reset()
                    renderer.__init__(state)
                else:
                    running = False

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
