import pygame
import random
import sys

# 기본 설정
WIDTH, HEIGHT = 600, 600   # 화면 크기
CELL = 20                  # 한 칸(뱀/사과) 크기
FPS = 8                    # 기본 속도

# 색상 설정
BG = (0, 150, 0)           # 배경(초록)
SNAKE_HEAD = (255, 255, 255)  # 뱀 머리(흰색)
SNAKE_BODY = (0, 0, 0)        # 뱀 몸통(검정)
FOOD = (200, 0, 0)            # 사과(빨강)
TEXT = (200, 200, 200)        # 텍스트(회색)
WALL = (0, 120, 255)          # 벽(파랑)
WALL_THICK = 4                # 벽 두께(px)

def rand_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )

def draw_walls(screen):
    pygame.draw.rect(screen, WALL, (0, 0, WIDTH, WALL_THICK))                        # 위
    pygame.draw.rect(screen, WALL, (0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK))      # 아래
    pygame.draw.rect(screen, WALL, (0, 0, WALL_THICK, HEIGHT))                       # 왼쪽
    pygame.draw.rect(screen, WALL, (WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT))      # 오른쪽

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    # 뱀 초기 상태
    head = (WIDTH // 2, HEIGHT // 2)
    snake = [
        head,
        (head[0] - CELL, head[1]),
        (head[0] - 2 * CELL, head[1]),
        (head[0] - 3 * CELL, head[1]),
        (head[0] - 4 * CELL, head[1]),
        (head[0] - 5 * CELL, head[1]),
    ]

    
    dx, dy = (0, 0)         # 이동 방향(처음엔 정지)
    food = rand_pos()       # 사과 위치
    score = 0
    food_eaten = 0
    speed = FPS
    total_cells = (WIDTH // CELL) * (HEIGHT // CELL)
    game_over = False
    game_won = False

    # 메인 게임 루프
    while True:
        clock.tick(speed)

        # 이벤트 처리
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                # 게임 종료/승리 상태: 재시작 or 종료
                if game_over or game_won:
                    if event.key == pygame.K_r:
                        main()
                    if event.key in (pygame.K_q, pygame.K_ESCAPE):
                        pygame.quit()
                        sys.exit()
                else:
                    # 방향키 입력(반대 방향 즉시 전환 방지)
                    if event.key == pygame.K_UP and dy != CELL:
                        dx, dy = (0, -CELL)
                    elif event.key == pygame.K_DOWN and dy != -CELL:
                        dx, dy = (0, CELL)
                    elif event.key == pygame.K_LEFT and dx != CELL:
                        dx, dy = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and dx != -CELL:
                        dx, dy = (CELL, 0)

        # 이동/충돌 처리
        if not game_over and not game_won and (dx, dy) != (0, 0):
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)

            # 벽 충돌
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
                game_over = True

            # 몸통 충돌
            elif new_head in snake:
                game_over = True

            else:
                snake.insert(0, new_head)

                # 사과를 먹었을 때
                if new_head == food:
                    score += 1
                    food_eaten += 1

                    # 5개마다 속도 증가
                    if food_eaten % 5 == 0:
                        speed += 1

                    # 화면을 다 채우면 승리
                    if len(snake) == total_cells:
                        game_won = True

                    # [특수 규칙] 사과를 먹으면 뱀 방향이 뒤집힘(꼬리가 머리가 됨)
                    snake.reverse()
                    new_head_x, new_head_y = snake[0]
                    neck_x, neck_y = snake[1]
                    dx = new_head_x - neck_x
                    dy = new_head_y - neck_y

                    # 뱀 위에 겹치지 않는 위치로 사과 재생성
                    while True:
                        food = rand_pos()
                        if food not in snake:
                            break
                else:
                    # 사과를 안 먹었으면 꼬리 한 칸 제거(길이 유지)
                    snake.pop()

        # 화면
        screen.fill(BG)
        draw_walls(screen)

        # 사과
        pygame.draw.rect(screen, FOOD, (food[0], food[1], CELL, CELL))

        # 뱀(머리/몸통 색 구분)
        for i, (x, y) in enumerate(snake):
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))

        # 점수
        screen.blit(font.render(f"Score: {score}", True, TEXT), (15, 15))

        # 안내 문구
        if game_over:
            screen.blit(font.render("GAME OVER (R: restart, Q: quit)", True, TEXT), (60, HEIGHT // 2))
        if game_won:
            screen.blit(font.render("YOU WIN! (R: restart, Q: quit)", True, TEXT), (70, HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__": 
    main() 
