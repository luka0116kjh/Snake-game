import pygame
import random
import sys

WIDTH, HEIGHT = 600, 600 
CELL = 20 
FPS = 8 

BG = (0, 150, 0)
SNAKE_HEAD = (255, 255, 255)  # 머리 흰색
SNAKE_BODY = (0, 0, 0)        # 몸통 검정
FOOD = (200, 0, 0) 
TEXT = (200, 200, 200) 
WALL = (0, 120, 255) 
WALL_THICK = 4 

<<<<<<< HEAD
=======
<<<<<<< HEAD
=======
FOOD = (200, 0, 0) # 사과 크기
TEXT = (200, 200, 200) #글자 크기

WALL = (0, 120, 255)          # 벽 파란색
WALL_THICK = 4                # 벽 두께

# 랜덤 위치 선정
>>>>>>> 8057b09 (luka: 코드 일정부분 수정정)
>>>>>>> ce28048c654914bf5d10dea27d057fe109a8c8e1
def rand_pos():
    return (
        random.randrange(0, WIDTH, CELL),
        random.randrange(0, HEIGHT, CELL)
    )

def draw_walls(screen):
    pygame.draw.rect(screen, WALL, (0, 0, WIDTH, WALL_THICK))
    pygame.draw.rect(screen, WALL, (0, HEIGHT - WALL_THICK, WIDTH, WALL_THICK))
    pygame.draw.rect(screen, WALL, (0, 0, WALL_THICK, HEIGHT))
    pygame.draw.rect(screen, WALL, (WIDTH - WALL_THICK, 0, WALL_THICK, HEIGHT))

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Reverse Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24) 

    head = (WIDTH // 2, HEIGHT // 2)

    # 초기 상태
    snake = [
        head,
        (head[0] - CELL, head[1]),
        (head[0] - 2 * CELL, head[1]),
        (head[0] - 3 * CELL, head[1]),
        (head[0] - 4 * CELL, head[1]),
        (head[0] - 5 * CELL, head[1]),
    ]

    dx, dy = (0, 0) # 초기 이동 방향 없음
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
                    # 방향키 조작 (반대 방향 이동 제한)
                    if event.key == pygame.K_UP and dy != CELL:
                        dx, dy = (0, -CELL)
                    elif event.key == pygame.K_DOWN and dy != -CELL:
                        dx, dy = (0, CELL)
                    elif event.key == pygame.K_LEFT and dx != CELL:
                        dx, dy = (-CELL, 0)
                    elif event.key == pygame.K_RIGHT and dx != -CELL:
                        dx, dy = (CELL, 0)

        if not game_over and (dx, dy) != (0, 0): # 이동 방향이 설정된 경우에만 이동
            head_x, head_y = snake[0]
            new_head = (head_x + dx, head_y + dy)

            # 벽 충돌 체크
            if new_head[0] < 0 or new_head[0] >= WIDTH or new_head[1] < 0 or new_head[1] >= HEIGHT:
                game_over = True
            # 몸통 충돌 체크
            elif new_head in snake:
                game_over = True
            else:
                snake.insert(0, new_head)

                if new_head == food:
                    score += 1
                    #[핵심 수정 부분]
                    snake.reverse()    # 1. 뱀의 몸통 순서를 뒤집음 (꼬리가 머리가 됨)
                    # 2. 새로운 이동 방향을 꼬리에서 머리 방향으로 설정
                    new_head_x, new_head_y = snake[0]
                    neck_x, neck_y = snake[1]
                    # 새로운 이동 방향을 설정
                    dx = new_head_x - neck_x
                    dy = new_head_y - neck_y

                    while True:
                        food = rand_pos()
                        if food not in snake:
                            break
                else:
                    snake.pop()
    
        screen.fill(BG)
        draw_walls(screen)
        pygame.draw.rect(screen, FOOD, (food[0], food[1], CELL, CELL))

        for i, (x, y) in enumerate(snake): 
            color = SNAKE_HEAD if i == 0 else SNAKE_BODY
            pygame.draw.rect(screen, color, (x, y, CELL, CELL))

        screen.blit(font.render(f"Score: {score}", True, TEXT), (15, 15))

        if game_over:
            screen.blit(font.render("GAME OVER (R: restart, Q: quit)", True, TEXT), (60, HEIGHT // 2))

        pygame.display.flip()

if __name__ == "__main__":
    main()