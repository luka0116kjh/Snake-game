import pygame
import random
import sys

WIDTH, HEIGHT = 600, 600
CELL = 20
FPS = 10

BG = (0, 150, 0)
SNAKE = (0, 0, 0)
FOOD = (200, 0, 0)
TEXT = (255, 255, 255)

def rand_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )
# 뱀의 초기 상태
def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Snake")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    # 뱀상태 (머리 + 꼬리 4개)
    head = (WIDTH // 2, HEIGHT // 2)

    # 꼬리 4개를 왼쪽으로 붙여서 시작
    snake = [
        head,
        (head[0] - CELL, head[1]),
        (head[0] - 2 * CELL, head[1]),
        (head[0] - 3 * CELL, head[1]),
        (head[0] - 4 * CELL, head[1]),
    ]

    dx, dy = (0, 0)   # 처음엔 움직이지 않음
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
                        main()  # 재시작
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                else:
                    # 방향키
                    if event.key == pygame.K_UP and dy != CELL:
                        dx, dy = (0, -CELL)
                    elif event.key == pygame.K_DOWN and dy != -CELL:
                        dx, dy = (0, CELL)
                    elif event.key == pygame.K_LEFT and dx != CELL:
                        dx, dy = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and dx != -CELL:
                        dx, dy = (CELL, 0)

        # 게임 진행 중중
        if not game_over and (dx, dy) != (0, 0):
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)

            # 벽 충돌
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
                game_over = True

            # 자기 몸 충돌
            elif new_head in snake:
                game_over = True

            else:
                # 머리 추가
                snake.insert(0, new_head)

                # 먹이 먹으면 길이 유지
                if new_head == food:
                    score += 1
                    # 먹이가 뱀 위에 생성되지 않게
                    while True:
                        food = rand_pos()
                        if food not in snake:
                            break
                else:
                    # 안 먹었으면 꼬리 제거
                    snake.pop()

        screen.fill(BG)

        # 먹이
        pygame.draw.rect(screen, FOOD, (food[0], food[1], CELL, CELL))

        # 뱀
        for x, y in snake:
            pygame.draw.rect(screen, SNAKE, (x, y, CELL, CELL))

        # 점수
        screen.blit(font.render(f"Score: {score}", True, TEXT), (10, 10))

        # 게임오버 메시지
        if game_over:
            screen.blit(font.render("GAME OVER  (R: restart, Q: quit)", True, TEXT), (60, HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    main()
