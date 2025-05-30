import random

MOVES = ["rock", "paper", "scissors"]

def get_ai_move():
    return random.choice(MOVES)

def determine_result(user_move: str, ai_move: str) -> str:
    if user_move == ai_move:
        return "draw"
    elif (user_move == "rock" and ai_move == "scissors") or \
         (user_move == "paper" and ai_move == "rock") or \
         (user_move == "scissors" and ai_move == "paper"):
        return "win"
    else:
        return "lose"
