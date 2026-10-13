import pytest
import sys
import os

# 프로젝트 루트를 path에 추가하여 src 모듈을 찾을 수 있게 함
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../")))

from src.logic.game_logic import GuessGame

def test_game_initialization():
    game = GuessGame()
    assert game.attempts == 0
    assert len(game.history) == 0
    assert game.is_game_over is False
    assert 1 <= game.target_number <= 100

def test_game_too_low():
    game = GuessGame()
    # 정답을 확실히 높게 만들기 위해 강제로 설정 (테스트 용도)
    game.target_number = 50
    
    result = game.check_guess(30)
    
    assert result == "Too Low"
    assert game.attempts == 1
    assert (30, "Too Low") in game.history

def test_game_too_high():
    game = GuessGame()
    game.target_number = 50
    
    result = game.check_guess(70)
    
    assert result == "Too High"
    assert game.attempts == 1
    assert (70, "Too High") in game.history

def test_game_correct():
    game = GuessGame()
    game.target_number = 50
    
    result = game.check_guess(50)
    
    assert result == "Correct"
    assert game.attempts == 1
    assert game.is_game_over is True
    
    status = game.get_status()
    assert status["attempts"] == 1
    assert status["is_game_over"] is True
    assert status["correct_answer"] == 50

def test_game_reset():
    game = GuessGame()
    game.target_number = 50
    game.check_guess(50) # 게임 종료 상태로 만듦
    
    assert game.is_game_over is True
    
    game.reset()
    
    assert game.attempts == 0
    assert len(game.history) == 0
    assert game.is_game_over is False
    assert 1 <= game.target_number <= 100

def test_check_guess_after_game_over():
    game = GuessGame()
    game.target_number = 50
    game.check_guess(50) # 종료
    
    result = game.check_guess(10)
    assert result == "Game is already over. Please restart."
    assert game.attempts == 1 # 종료 전 시도만 카운트됨 (로직 설계에 따름)
