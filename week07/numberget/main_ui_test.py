import flet as ft
from src.ui.components import GameUIComponents

def main(page: ft.Page):
    page.title = "Number Guessing Game"
    page.window_width = 400
    page.window_height = 600
    page.window_resizable = False
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER
    page.theme_mode = ft.ThemeMode.LIGHT

    # Mock functions for testing UI layout only
    def mock_submit(e):
        print("Submit clicked")

    def mock_restart(e):
        print("Restart clicked")

    # Initialize UI components
    ui = GameUIComponents(on_submit=mock_submit, on_restart=mock_restart)
    
    # Add components to page
    page.add(ui.get_main_layout())

if __name__ == "__main__":
    ft.app(target=main)
