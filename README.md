# Snake Game (Pygame)

Python + Pygame으로 만든 스네이크 게임입니다.  
사과를 먹는 순간 **뱀이 뒤집히는(Reverse)** 특수 규칙이 있습니다.

## Features
- 방향키로 이동
- 사과 먹으면 길이 증가 + 점수 증가
- **사과 먹을 때 `snake.reverse()` (꼬리가 머리로)**
- *가짜 사과 먹었을떄 잠시 멈춰진다(1초) 제작중*
- 머리 흰색 / 몸통 검정 / 벽 파란색 / 사과 빨간색
- **사과 5개마다 속도 +1**
- 벽/몸통 충돌 시 Game Over
- 보드 전체를 채우면 Win
- **R**: 재시작, **Q/ESC**: 종료  
  - 재시작 로직은 개선 중(`main()` 중첩 호출 크래시 가능)

## Run
```bash
pip install pygame
python main.py
