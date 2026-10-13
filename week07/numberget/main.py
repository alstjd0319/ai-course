import flet as ft
import sys
import os

# 1. 로직 레이어를 불러오기 위한 경로 설정
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), ".")))
from src.logic.game_logic import GuessGame

def main(page: ft.Page):
    page.title = "숫자 맞추기 게임"
    # page.window_width, height 등은 가이드라인에 따라 제거
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    # 2. [Logic Layer] 인스턴스 생성
    game = GuessGame()

    # 3. [UI Layer] 기존 스타일의 요소들
    value = ft.TextField(label="숫자 입력 (1-100)", value="", width=200)
    result = ft.Text(value="", size=20, weight=ft.FontWeight.BOLD)
    notice = ft.Text(value="", color=ft.Colors.RED)
    items = ft.ListView(expand=True, spacing=4)
    
    attempt_text = ft.Text(value="현재 시도 횟수: 0회", size=16)
    restart_button = ft.Button("새 게임 시작", visible=False)

    # 4. [Event Handlers]
    
    def on_guess(e):
        nonlocal game
        notice.value = "" 
        
        # [Validation]
        try:
            user_input = value.value.strip()
            if not user_input:
                raise ValueError("숫자를 입력해주세요.")
            
            num = int(user_input)
            if not (1 <= num <= 100):
                raise ValueError("1~100 사이의 숫자만 입력 가능합니다.")
        except ValueError as err:
            notice.value = str(err)
            page.update()
            return

        # [Logic]
        res_msg = game.check_guess(num)
        status = game.get_status()

        # [UI Update] 한글 메시지 변환 로직 추가 ⭐
        # 영어 메시지를 한글로 맵핑합니다.
        msg_map = {
            "Too High": "더 작습니다 ↓",   # 입력값이 정답보다 크면, 정답은 더 작음
            "Too Low": "더 큽니다 ↑",      # 입력값이 정답보다 작으면, 정답은 더 큼
            "Correct": "🎉 정답입니다!"
        }
        
        # 매핑된 한글 메시지 가져오기 (없을 경우 대비하여 기본값 설정)
        display_msg = msg_map.get(res_msg, res_msg)

        result.value = display_msg
        result.color = ft.Colors.BLUE if res_msg != "Correct" else ft.Colors.GREEN
        
        attempt_text.value = f"현재 시도 횟수: {status['attempts']}회"
        
        # 기록 추가 (한글 메시지로 기록)
        items.controls.append(ft.Text(f"입력: {num} -> {display_msg}"))
        
        if res_msg == "Correct":
            # 정답 시 상세 결과 출력
            result.value = f"🎉 정답입니다! ({status['attempts']}번 만에 성공!)"
            restart_button.visible = True
            value.disabled = True
        
        value.value = "" 
        page.update()

    def on_reset(e):
        game.reset()
        result.value = ""
        notice.value = ""
        attempt_text.value = "현재 시도 횟수: 0회"
        items.controls.clear()
        value.value = ""
        value.disabled = False
        restart_button.visible = False
        page.update()

    # 이벤트 바인딩
    restart_button.on_click = on_reset
    value.on_submit = on_guess
    
    # 5. [Layout]
    page.add(
        ft.Column(
            controls=[
                ft.Text("Number Guessing Game", size=28, weight=ft.FontWeight.BOLD),
                attempt_text,
                ft.Row([value, ft.Button("확인", on_click=on_guess)], alignment=ft.MainAxisAlignment.CENTER),
                result,
                notice,
                ft.Divider(),
                ft.Text("시도 기록", weight=ft.FontWeight.BOLD),
                items,
                restart_button,
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.run(main)
