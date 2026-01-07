import pygame
import random
import sys

WIDTH, HEIGHT = 600,600 # 화면 크기
CELL = 20 # 셀크기(스네이크 크기)
FPS = 8 # 스네이크 속도 

BG = (0, 150, 0)

SNAKE_HEAD = (255, 255, 255)  #  머리 흰색
SNAKE_BODY = (0, 0, 0)        # 몸통 검정

FOOD = (200, 0, 0) # 사과 크기
TEXT = (200, 200, 200) #글자 크기

WALL = (0, 120, 255)          # 벽 파란색
WALL_THICK = 4                # 벽 두께

# 랜덤 위치 선정
def rand_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )

def draw_walls(screen):
    # 화면 테두리에 파란 벽 그리기
    pygame.draw.rect(screen, WALL, (0, 0, WIDTH, WALL_THICK))                      # 위
    pygame.draw.rect(screen, WALL, (0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK))    # 아래
    pygame.draw.rect(screen, WALL, (0, 0, WALL_THICK, HEIGHT))                     # 왼
    pygame.draw.rect(screen, WALL, (WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT))    # 오

# 뱀의 초기 상태
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    head = (WIDTH // 2, HEIGHT // 2)

    snake = [
        head,
        (head[0] - CELL, head[1]),
        (head[0] - 2 * CELL, head[1]),
        (head[0] - 3 * CELL, head[1]),
        (head[0] - 4 * CELL, head[1]),
        (head[0] - 5 * CELL, head[1]),
    ]

    dx, dy = (0, 0)
    food = rand_pos()
    score = 0
    game_over = False

    while True:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if game_over:
                    if event.key == pygame.K_r:
                        main()
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                else:
                    if event.key == pygame.K_UP and dy != CELL:
                        dx, dy = (0, -CELL)
                    elif event.key == pygame.K_DOWN and dy != -CELL:
                        dx, dy = (0, CELL)
                    elif event.key == pygame.K_LEFT and dx != CELL:
                        dx, dy = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and dx != -CELL:
                        dx, dy = (CELL, 0)

        if not game_over and (dx, dy) != (0, 0):
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)

            # 벽 충돌(기존 그대로: 화면 밖으로 나가면 게임오버)
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
                game_over = True

            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)

                if new_head == food:
                    score += 1
                    while True:
                        food = rand_pos()
                        if food not in snake:
                            break
                else:
                    snake.pop()

        screen.fill(BG)

        # 벽 표시
        draw_walls(screen)

        pygame.draw.rect(screen, FOOD, (food[0], food[1], CELL, CELL))

        # 뱀: 머리 흰색, 나머지 검정
        for i, (x, y) in enumerate(snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))

        screen.blit(font.render(f"Score: {score}", True, TEXT), (10, 10))

        if game_over:
            screen.blit(font.render("GAME OVER  (R: restart, Q: quit)", True, TEXT), (60, HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    main()
