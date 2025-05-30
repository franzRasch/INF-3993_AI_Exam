import random

MOVES = ["rock", "paper", "scissors"]


def get_ai_move() -> str:
    """Get the AI's move in the game.

    Returns:
        str: The AI's move.
    """
    return random.choice(MOVES)


def determine_result(user_move: str, ai_move: str) -> str:
    """Determine the result of a rock-paper-scissors game.

    Args:
        user_move (str): The user's move.
        ai_move (str): The AI's move.

    Returns:
        str: The result of the game.
    """
    if user_move == ai_move:
        return "draw"
    if (
        (user_move == "rock" and ai_move == "scissors")
        or (user_move == "paper" and ai_move == "rock")
        or (user_move == "scissors" and ai_move == "paper")
    ):
        return "win"

    return "lose"
