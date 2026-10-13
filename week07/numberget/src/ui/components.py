import flet as ft

class GameUIComponents:
    def __init__(self, on_submit, on_restart):
        self.on_submit = on_submit
        self.on_restart = on_restart
        
        # 1. Header
        self.title = ft.Text("숫자 맞추기 게임", size=32, weight=ft.FontWeight.BOLD)
        
        # 2. Status Panel (Attempts)
        self.attempt_text = ft.Text("현재 시도 횟수: 0회", size=20)
        
        # 3. Input Area
        self.input_field = ft.TextField(
            label="1~100 사이의 숫자 입력",
            width=300,
            text_align=ft.TextAlign.CENTER,
            on_submit=self.on_submit  # 엔터키 지원
        )
        self.submit_button = ft.ElevatedButton("확인", on_click=self.on_submit)
        
        # 4. History List
        self.history_list = ft.ListView(
            expand=True,
            spacing=10,
            padding=10,
        )
        self.history_container = ft.Column(
            controls=[
                ft.Text("시도 기록", size=18, weight=ft.FontWeight.W_600),
                ft.Container(
                    content=self.history_list,
                    height=200,
                    border=ft.border.all(1, ft.colors.OUTLINE),
                    border_radius=10,
                )
            ]
        )
        
        # 5. Result/Control Panel
        self.result_text = ft.Text("", size=22, color=ft.colors.BLUE_ACCENT, weight=ft.FontWeight.BOLD)
        self.restart_button = ft.ElevatedButton(
            "새 게임 시작", 
            icon=ft.icons.RESTART_ALT, 
            on_click=self.on_restart,
            visible=False  # 처음에는 숨김
        )

    def get_main_layout(self):
        """전체 레이아웃을 반환합니다."""
        return ft.Column(
            controls=[
                self.title,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                self.attempt_text,
                ft.Divider(height=10, color=ft.colors.TRANSPARENT),
                ft.Row(
                    [self.input_field, self.submit_button],
                    alignment=ft.MainAxisAlignment.CENTER
                ),
                self.result_text,
                self.restart_button,
                ft.Divider(height=20, color=ft.colors.TRANSPARENT),
                self.history_container
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            scroll=ft.ScrollMode.AUTO
        )
