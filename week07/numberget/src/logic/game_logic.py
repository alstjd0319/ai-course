import random
from typing import List, Tuple, Optional

class GuessGame:
    def __init__(self):
        self.target_number: Optional[int] = None
        self.attempts: int = 0
        self.history: List[Tuple[int, str]] = []
        self.is_game_over: bool = False
        self.reset()

    def reset(self) -> None:
        """게임 상태를 초기화합니다."""
        self.target_number = random.randint(1, 100)
        self.attempts = 0
        self.history = []
        self.is_game_over = False

    def check_guess(self, guess: int) -> str:
        """
        사용자의 추측을 확인하고 결과를 반환합니다.
        결과값: "Too High", "Too Low", "Correct"
        """
        if self.is_game_over:
            return "Game is already over. Please restart."

        self.attempts += 1
        
        if guess < self.target_number:
            result = "Too Low"
        elif guess > self.target_number:
            result = "Too High"
        else:
            result = "Correct"
            self.is_game_over = True

        self.history.append((guess, result))
        return result

    def get_status(self) -> dict:
        """현재 게임의 상태 정보를 반환합니다."""
        return {
            "attempts": self.attempts,
            "history": self.history,
            "is_game_over": self.is_game_over,
            "correct_answer": self.target_number if self.is_game_over else None
        }
