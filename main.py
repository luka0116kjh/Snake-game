import json
import random
import sys
from pathlib import Path

import pygame


WIDTH, HEIGHT = 720, 640
CELL = 20
GRID_WIDTH = WIDTH // CELL
GRID_HEIGHT = HEIGHT // CELL

START_SPEED = 8
MAX_SPEED = 18
FOOD_LIMIT_MS = 30000
SPECIAL_FOOD_MS = 9000
HIGH_SCORE_FILE = Path(__file__).with_name("high_score.json")

BG = (20, 36, 32)
BG_ALT = (24, 46, 41)
PANEL = (12, 18, 22)
GRID_LINE = (32, 58, 51)
TEXT = (230, 238, 232)
MUTED = (150, 168, 158)
ACCENT = (88, 214, 141)
WARN = (255, 190, 80)
DANGER = (237, 87, 87)
SNAKE_HEAD = (242, 246, 245)
SNAKE_BODY = (25, 192, 122)
SNAKE_BODY_ALT = (16, 145, 96)
FOOD_NORMAL = (236, 68, 68)
FOOD_GOLD = (255, 212, 72)
FOOD_SLOW = (89, 183, 255)
OBSTACLE = (87, 98, 109)
SHADOW = (3, 7, 8)


TEXTS = {
    "en": {
        "title": "SNAKE UPGRADE",
        "score": "Score",
        "best": "Best",
        "level": "Level",
        "speed": "Speed",
        "timer": "Food timer",
        "combo": "combo",
        "start_line_1": "Eat food before the timer ends",
        "start_line_2": "Food reverses the snake",
        "start_line_3": "Gold gives bonus, blue slows speed",
        "start_line_4": "Press SPACE to start",
        "language_hint": "Press K for Korean",
        "paused": "PAUSED",
        "resume": "Press SPACE to resume",
        "restart_quit": "R restarts, ESC quits",
        "game_over": "GAME OVER",
        "win": "YOU WIN",
        "restart": "Press R to restart",
        "wall_crash": "Wall crash",
        "self_crash": "Self crash",
        "obstacle_crash": "Obstacle crash",
        "timer_expired": "Food timer expired",
        "board_cleared": "Board cleared",
        "gold": "Gold +50",
        "slow": "Blue slows",
    },
    "ko": {
        "title": "스네이크 업그레이드",
        "score": "점수",
        "best": "최고",
        "level": "레벨",
        "speed": "속도",
        "timer": "제한 시간",
        "combo": "콤보",
        "start_line_1": "시간 안에 먹이를 먹으세요",
        "start_line_2": "먹이를 먹으면 뱀의 방향이 뒤집힙니다",
        "start_line_3": "금색은 보너스, 파란색은 감속 효과",
        "start_line_4": "SPACE 키로 시작",
        "language_hint": "K 키로 영어 전환",
        "paused": "일시정지",
        "resume": "SPACE 키로 계속",
        "restart_quit": "R 재시작, ESC 종료",
        "game_over": "게임 오버",
        "win": "승리!",
        "restart": "R 키로 다시 시작",
        "wall_crash": "벽에 부딪혔습니다",
        "self_crash": "몸에 부딪혔습니다",
        "obstacle_crash": "장애물에 부딪혔습니다",
        "timer_expired": "제한 시간이 끝났습니다",
        "board_cleared": "보드를 모두 채웠습니다",
        "gold": "금색 +50",
        "slow": "파란색 감속",
    },
}


DIRS = {
    pygame.K_UP: (0, -CELL),
    pygame.K_w: (0, -CELL),
    pygame.K_DOWN: (0, CELL),
    pygame.K_s: (0, CELL),
    pygame.K_LEFT: (-CELL, 0),
    pygame.K_a: (-CELL, 0),
    pygame.K_RIGHT: (CELL, 0),
    pygame.K_d: (CELL, 0),
}


def tr(game, key):
    return TEXTS[game["language"]][key]


def make_fonts():
    font_names = ["malgungothic", "gulim", "consolas"]
    return (
        pygame.font.SysFont(font_names, 44, bold=True),
        pygame.font.SysFont(font_names, 24, bold=True),
        pygame.font.SysFont(font_names, 18),
    )


def grid_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL),
    )


def load_high_score():
    try:
        with HIGH_SCORE_FILE.open("r", encoding="utf-8") as file:
            data = json.load(file)
        return int(data.get("high_score", 0))
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return 0


def save_high_score(score):
    try:
        with HIGH_SCORE_FILE.open("w", encoding="utf-8") as file:
            json.dump({"high_score": score}, file)
    except OSError:
        pass


def draw_text(screen, font, text, color, pos, center=False):
    surface = font.render(text, True, color)
    rect = surface.get_rect()
    if center:
        rect.center = pos
    else:
        rect.topleft = pos
    screen.blit(surface, rect)
    return rect


def draw_cell(screen, pos, color, radius=5, inset=2):
    x, y = pos
    rect = pygame.Rect(x + inset, y + inset, CELL - inset * 2, CELL - inset * 2)
    pygame.draw.rect(screen, SHADOW, rect.move(2, 2), border_radius=radius)
    pygame.draw.rect(screen, color, rect, border_radius=radius)


def draw_background(screen):
    screen.fill(BG)
    for x in range(0, WIDTH, CELL):
        for y in range(0, HEIGHT, CELL):
            if (x // CELL + y // CELL) % 2 == 0:
                pygame.draw.rect(screen, BG_ALT, (x, y, CELL, CELL))
    for x in range(0, WIDTH, CELL * 2):
        pygame.draw.line(screen, GRID_LINE, (x, 0), (x, HEIGHT))
    for y in range(0, HEIGHT, CELL * 2):
        pygame.draw.line(screen, GRID_LINE, (0, y), (WIDTH, y))


def draw_hud(screen, font, small_font, game, time_left):
    pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, 54))
    draw_text(screen, font, f"{tr(game, 'score')} {game['score']}", TEXT, (16, 13))
    draw_text(screen, small_font, f"{tr(game, 'best')} {game['high_score']}", MUTED, (150, 18))
    draw_text(screen, small_font, f"{tr(game, 'level')} {game['level']}", MUTED, (260, 18))
    draw_text(screen, small_font, f"{tr(game, 'speed')} {game['speed']}", MUTED, (350, 18))

    timer_color = DANGER if time_left <= 7 else WARN if time_left <= 12 else TEXT
    draw_text(screen, small_font, f"{tr(game, 'timer')} {time_left}s", timer_color, (450, 18))
    if game["combo"] > 1:
        draw_text(screen, small_font, f"x{game['combo']} {tr(game, 'combo')}", ACCENT, (610, 18))


def make_obstacles(snake, food, count):
    blocked = set(snake)
    if food:
        blocked.add(food)

    obstacles = set()
    center_safe = {
        (WIDTH // 2 + x * CELL, HEIGHT // 2 + y * CELL)
        for x in range(-3, 4)
        for y in range(-3, 4)
    }

    attempts = 0
    while len(obstacles) < count and attempts < 2000:
        attempts += 1
        pos = grid_pos()
        if pos not in blocked and pos not in center_safe:
            obstacles.add(pos)
    return obstacles


def spawn_food(snake, obstacles, forbidden=None):
    forbidden = forbidden or set()
    blocked = set(snake) | set(obstacles) | set(forbidden)
    if len(blocked) >= GRID_WIDTH * GRID_HEIGHT:
        return None

    while True:
        pos = grid_pos()
        if pos not in blocked:
            return pos


def new_game(high_score, language="en"):
    head = (WIDTH // 2, HEIGHT // 2)
    snake = [
        head,
        (head[0] - CELL, head[1]),
        (head[0] - 2 * CELL, head[1]),
        (head[0] - 3 * CELL, head[1]),
    ]
    food = spawn_food(snake, set())
    obstacles = make_obstacles(snake, food, 8)

    return {
        "snake": snake,
        "dx": CELL,
        "dy": 0,
        "next_dx": CELL,
        "next_dy": 0,
        "food": food,
        "special_food": None,
        "special_kind": None,
        "special_until": 0,
        "obstacles": obstacles,
        "score": 0,
        "high_score": high_score,
        "level": 1,
        "speed": START_SPEED,
        "food_eaten": 0,
        "combo": 0,
        "last_food_ticks": pygame.time.get_ticks(),
        "state": "start",
        "message": "",
        "language": language,
    }


def reverse_snake(game):
    snake = game["snake"]
    if len(snake) < 2:
        return

    snake.reverse()
    head_x, head_y = snake[0]
    neck_x, neck_y = snake[1]
    game["dx"] = head_x - neck_x
    game["dy"] = head_y - neck_y
    game["next_dx"] = game["dx"]
    game["next_dy"] = game["dy"]


def add_obstacles_for_level(game):
    target_count = 8 + (game["level"] - 1) * 3
    if len(game["obstacles"]) >= target_count:
        return

    new_obstacles = make_obstacles(
        game["snake"],
        game["food"],
        target_count - len(game["obstacles"]),
    )
    game["obstacles"].update(new_obstacles)


def maybe_spawn_special(game, now):
    if game["special_food"] and now > game["special_until"]:
        game["special_food"] = None
        game["special_kind"] = None

    if game["special_food"] is None and game["food_eaten"] > 0 and game["food_eaten"] % 4 == 0:
        if random.random() < 0.35:
            game["special_kind"] = random.choice(("gold", "slow"))
            game["special_food"] = spawn_food(
                game["snake"],
                game["obstacles"],
                {game["food"]},
            )
            game["special_until"] = now + SPECIAL_FOOD_MS


def update_level_and_speed(game):
    game["level"] = 1 + game["food_eaten"] // 5
    game["speed"] = min(MAX_SPEED, START_SPEED + game["level"] - 1)
    add_obstacles_for_level(game)


def finish_game(game, message):
    game["state"] = "game_over"
    game["message"] = message
    if game["score"] > game["high_score"]:
        game["high_score"] = game["score"]
        save_high_score(game["high_score"])


def eat_normal_food(game, now):
    game["combo"] += 1
    gained = 10 + max(0, game["combo"] - 1) * 2
    game["score"] += gained
    game["food_eaten"] += 1
    game["last_food_ticks"] = now

    reverse_snake(game)
    update_level_and_speed(game)
    game["food"] = spawn_food(game["snake"], game["obstacles"], {game["special_food"]})
    if game["food"] is None:
        game["state"] = "win"
        game["message"] = "board_cleared"
    maybe_spawn_special(game, now)


def eat_special_food(game, now):
    kind = game["special_kind"]
    if kind == "gold":
        game["score"] += 50
        game["combo"] += 2
    elif kind == "slow":
        game["score"] += 20
        game["speed"] = max(START_SPEED, game["speed"] - 3)
        if len(game["snake"]) > 4:
            game["snake"].pop()

    game["special_food"] = None
    game["special_kind"] = None
    game["special_until"] = 0
    game["last_food_ticks"] = now


def move_snake(game):
    now = pygame.time.get_ticks()
    game["dx"] = game["next_dx"]
    game["dy"] = game["next_dy"]

    head_x, head_y = game["snake"][0]
    new_head = (head_x + game["dx"], head_y + game["dy"])

    if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
        finish_game(game, "wall_crash")
        return

    will_eat_normal = new_head == game["food"]
    will_eat_special = new_head == game["special_food"]
    body_to_check = game["snake"] if will_eat_normal or will_eat_special else game["snake"][:-1]

    if new_head in body_to_check:
        finish_game(game, "self_crash")
        return
    if new_head in game["obstacles"]:
        finish_game(game, "obstacle_crash")
        return

    game["snake"].insert(0, new_head)

    if will_eat_normal:
        eat_normal_food(game, now)
    elif will_eat_special:
        eat_special_food(game, now)
    else:
        game["snake"].pop()

    if game["state"] == "playing" and now - game["last_food_ticks"] > FOOD_LIMIT_MS:
        finish_game(game, "timer_expired")
        return

    if game["state"] == "playing":
        maybe_spawn_special(game, now)


def handle_direction(game, key):
    if key not in DIRS:
        return

    dx, dy = DIRS[key]
    if (dx, dy) == (-game["dx"], -game["dy"]):
        return

    game["next_dx"] = dx
    game["next_dy"] = dy


def draw_snake(screen, snake):
    for i, pos in enumerate(reversed(snake)):
        original_index = len(snake) - 1 - i
        if original_index == 0:
            color = SNAKE_HEAD
        elif original_index % 2 == 0:
            color = SNAKE_BODY
        else:
            color = SNAKE_BODY_ALT
        draw_cell(screen, pos, color)

    head_x, head_y = snake[0]
    eye_size = 4
    pygame.draw.circle(screen, PANEL, (head_x + 7, head_y + 7), eye_size)
    pygame.draw.circle(screen, PANEL, (head_x + 13, head_y + 7), eye_size)


def draw_food(screen, food, special_food, special_kind):
    if food:
        draw_cell(screen, food, FOOD_NORMAL, radius=9, inset=3)

    if special_food:
        color = FOOD_GOLD if special_kind == "gold" else FOOD_SLOW
        draw_cell(screen, special_food, color, radius=10, inset=1)
        x, y = special_food
        pygame.draw.circle(screen, TEXT, (x + CELL // 2, y + CELL // 2), 3)


def draw_obstacles(screen, obstacles):
    for pos in obstacles:
        draw_cell(screen, pos, OBSTACLE, radius=3, inset=1)


def draw_overlay(screen, title_font, font, small_font, title, lines):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 165))
    screen.blit(overlay, (0, 0))

    box = pygame.Rect(80, 150, WIDTH - 160, 300)
    pygame.draw.rect(screen, PANEL, box, border_radius=8)
    pygame.draw.rect(screen, ACCENT, box, width=2, border_radius=8)
    draw_text(screen, title_font, title, TEXT, (WIDTH // 2, 205), center=True)

    y = 260
    for line in lines:
        color = ACCENT if line.startswith(("Press", "SPACE", "K", "R")) else MUTED
        draw_text(screen, small_font if len(line) > 34 else font, line, color, (WIDTH // 2, y), center=True)
        y += 34


def draw_game(screen, fonts, game):
    title_font, font, small_font = fonts
    now = pygame.time.get_ticks()
    time_left = max(0, (FOOD_LIMIT_MS - (now - game["last_food_ticks"])) // 1000)

    draw_background(screen)
    draw_obstacles(screen, game["obstacles"])
    draw_food(screen, game["food"], game["special_food"], game["special_kind"])
    draw_snake(screen, game["snake"])
    draw_hud(
        screen,
        font,
        small_font,
        game,
        time_left,
    )

    if game["special_food"]:
        remaining = max(0, (game["special_until"] - now) // 1000)
        kind = tr(game, "gold") if game["special_kind"] == "gold" else tr(game, "slow")
        draw_text(screen, small_font, f"{kind} ({remaining}s)", TEXT, (16, HEIGHT - 30))

    if game["state"] == "start":
        draw_overlay(
            screen,
            title_font,
            font,
            small_font,
            tr(game, "title"),
            [
                tr(game, "start_line_1"),
                tr(game, "start_line_2"),
                tr(game, "start_line_3"),
                tr(game, "start_line_4"),
                tr(game, "language_hint"),
            ],
        )
    elif game["state"] == "paused":
        draw_overlay(
            screen,
            title_font,
            font,
            small_font,
            tr(game, "paused"),
            [tr(game, "resume"), tr(game, "restart_quit"), tr(game, "language_hint")],
        )
    elif game["state"] == "game_over":
        draw_overlay(
            screen,
            title_font,
            font,
            small_font,
            tr(game, "game_over"),
            [
                tr(game, game["message"]),
                f"{tr(game, 'score')} {game['score']}  {tr(game, 'best')} {game['high_score']}",
                tr(game, "restart"),
            ],
        )
    elif game["state"] == "win":
        draw_overlay(
            screen,
            title_font,
            font,
            small_font,
            tr(game, "win"),
            [
                f"{tr(game, 'score')} {game['score']}  {tr(game, 'best')} {game['high_score']}",
                tr(game, "restart"),
            ],
        )


def main():
    pygame.init()
    pygame.display.set_caption("Snake Upgrade")
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    fonts = make_fonts()

    game = new_game(load_high_score())

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key in (pygame.K_ESCAPE, pygame.K_q):
                    pygame.quit()
                    sys.exit()

                if event.key == pygame.K_r:
                    game = new_game(game["high_score"], game["language"])
                elif event.key == pygame.K_k:
                    game["language"] = "ko" if game["language"] == "en" else "en"
                elif event.key == pygame.K_SPACE:
                    if game["state"] == "start":
                        game["state"] = "playing"
                        game["last_food_ticks"] = pygame.time.get_ticks()
                    elif game["state"] == "playing":
                        game["state"] = "paused"
                    elif game["state"] == "paused":
                        game["state"] = "playing"
                        game["last_food_ticks"] = pygame.time.get_ticks()
                elif game["state"] == "playing":
                    handle_direction(game, event.key)

        if game["state"] == "playing":
            move_snake(game)

        draw_game(screen, fonts, game)
        pygame.display.flip()
        clock.tick(game["speed"])


if __name__ == "__main__":
    main()
