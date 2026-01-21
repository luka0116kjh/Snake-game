# Snake Game (Pygame)

Python + Pygame으로 만든 스네이크 게임입니다.  
기본 스네이크 규칙에 더해 **사과를 먹는 순간 뱀이 뒤집히는(Reverse)** 특수 규칙을 구현했습니다.

---

## 🛠 Tech Stack
- Python
- Pygame

---

## 🎮 How to Play
- 방향키(↑ ↓ ← →)로 이동
- 사과를 먹으면 점수 증가 + 몸 길이 증가
- 벽 또는 자기 몸통에 부딪히면 게임 오버

---

## ✨ Special Feature: Reverse Snake
사과를 먹는 순간 `snake.reverse()`가 실행되어 **기존 꼬리가 머리가 되는 효과**가 발생합니다.

- 사과 획득 시 뱀의 리스트를 뒤집어 꼬리가 머리가 되도록 처리
- 뒤집힌 직후에도 이동 방향이 자연스럽게 이어지도록  
  **머리-목(0번, 1번 인덱스) 기준으로 dx/dy를 재계산**
- Reverse 이후에도 충돌 판정이 정상 동작하도록 로직 보완

---

## 🎨 UI / Colors
- Snake Head: **White**
- Snake Body: **Black**
- Wall: **Blue**
- Food(Apple): **Red**

---

## ⌨ Controls
- **Arrow Keys**: Move
- **R**: Restart
- **Q / ESC**: Quit

> 참고: `R` 재시작 로직은 개선 중이며, `main()`을 중첩 호출할 때 크래시가 발생할 수 있어 구조 수정 예정입니다.

---

## 🏁 Win Condition
- 뱀이 보드의 모든 칸을 채우면 **YOU WIN!** 출력

---

## ⚡ Difficulty (Speed Up)
- 사과를 **5개 먹을 때마다 속도 +1**
  - 예: `food_eaten % 5 == 0` → `speed += 1`

---

## ▶ Run
```bash
pip install pygame
python main.py
