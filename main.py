import pygame
import random
import sys

# 기본 설정
WIDTH, HEIGHT = 600, 600   # 화면 크기
CELL = 20                  # 한 칸(뱀/사과) 크기
FPS = 8                    # 기본 속도

# 색상 설정
BG = (0, 150, 0)           # 배경(초록)
BG_PATTERN = (0, 170, 0)   # 배경 무늬용 연한 초록
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

def draw_background_pattern(screen):
    for x in range(0, WIDTH, CELL):
        for y in range(0, HEIGHT, CELL):
            if (x // CELL + y // CELL) % 2 == 0:
                pygame.draw.rect(screen, BG_PATTERN, (x, y, CELL, CELL))


def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Go Snake Game")
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("consolas", 24)

    total_cells = (WIDTH // CELL) * (HEIGHT // CELL)
    FOOD_LIMIT_MS = 30000

    while True:  # [수정] 게임 재시작을 위한 외부 루프
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
        last_dx, last_dy = (CELL, 0) # [수정] 마지막 이동 방향(초기엔 오른쪽을 보고 있음)
        
        food = rand_pos()       # 사과 위치
        score = 0
        food_eaten = 0
        speed = FPS
        
        game_over = False
        game_won = False

        # 시간 제한 관련
        last_food_ticks = None  # None으로 시작 (첫 이동 시 타이머 시작)

        running = True
        while running:  # [수정] 현재 게임 세션 루프
            clock.tick(speed)

            # 이벤트 처리
            direction_changed = False # [수정] 한 프레임에 한 번만 방향 전환 허용

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    # 게임 종료/승리 상태: 재시작 or 종료
                    if game_over or game_won:
                        if event.key == pygame.K_r:
                            running = False  # 루프 탈출 -> 외부 루프(재시작)로 이동
                        if event.key in (pygame.K_q, pygame.K_ESCAPE):
                            pygame.quit()
                            sys.exit()
                    else:
                        # 방향키 입력(반대 방향 즉시 전환 방지 + 프레임 당 1회 제한)
                        if not direction_changed:
                            # 현재 움직이는 방향(last_dx, last_dy)을 기준으로 반대 방향 체크
                            if event.key == pygame.K_UP and last_dy != CELL:
                                dx, dy = 0, -CELL
                                direction_changed = True
                            elif event.key == pygame.K_DOWN and last_dy != -CELL:
                                dx, dy = 0, CELL
                                direction_changed = True
                            elif event.key == pygame.K_LEFT and last_dx != CELL:
                                dx, dy = -CELL, 0
                                direction_changed = True
                            elif event.key == pygame.K_RIGHT and last_dx != -CELL:
                                dx, dy = CELL, 0
                                direction_changed = True

            # 이동/충돌 처리
            if not game_over and not game_won and (dx, dy) != (0, 0):
                # 첫 이동 시 타이머 시작
                if last_food_ticks is None:
                    last_food_ticks = pygame.time.get_ticks()
                
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
                        # 사과를 먹으면 타이머 리셋
                        last_food_ticks = pygame.time.get_ticks()

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
                    
                        # [수정] 방향이 바뀌었으므로 last_dx, last_dy도 업데이트
                        last_dx, last_dy = dx, dy 

                        # 뱀 위에 겹치지 않는 위치로 사과 재생성
                        while True:
                            food = rand_pos()
                            if food not in snake:
                                break
                    else:
                        # 사과를 안 먹었으면 꼬리 한 칸 제거(길이 유지)
                        snake.pop()
                    
                # [수정] 성공적으로 이동했으므로 last_dx, last_dy 갱신
                last_dx, last_dy = dx, dy

            # [특수 규칙] 30초 시간 초과 체크
            if not game_over and not game_won and last_food_ticks is not None:
                current_time = pygame.time.get_ticks()
                if current_time - last_food_ticks > FOOD_LIMIT_MS:
                    game_over = True

            # 화면
            screen.fill(BG)
            draw_background_pattern(screen)  # 배경 무늬
            draw_walls(screen)               # 벽은 제일 위


            # 사과
            pygame.draw.rect(screen, FOOD, (food[0], food[1], CELL, CELL))

            # 뱀(머리/몸통 색 구분)
            for i, (x, y) in enumerate(snake):
                color = SNAKE_HEAD if i == 0 else SNAKE_BODY
                pygame.draw.rect(screen, color, (x, y, CELL, CELL))

            # 점수 표시
            screen.blit(font.render(f"Score: {score}", True, TEXT), (15, 15))
            
            # 남은 시간 표시 (게임 시작 전부터 표시)
            if not game_over and not game_won:
                if last_food_ticks is None:
                    # 게임 시작 전: 30초 표시
                    time_left = FOOD_LIMIT_MS // 1000
                else:
                    # 게임 진행 중: 실제 남은 시간 계산
                    time_left = max(0, (FOOD_LIMIT_MS - (pygame.time.get_ticks() - last_food_ticks)) // 1000)
                timer_text = font.render(f"Timer: {time_left}s", True, (255, 0, 0)) # 빨강 텍스트
                screen.blit(timer_text, (15, 45))

            # 안내 문구
            if game_over:
                screen.blit(font.render("GAME OVER (R: restart, Q: quit)", True, TEXT), (60, HEIGHT // 2))
            if game_won:
                screen.blit(font.render("이걸 이기네.. (R: restart, Q: quit)", True, TEXT), (70, HEIGHT // 2))

            pygame.display.flip()

if __name__ == "__main__": 
    main()