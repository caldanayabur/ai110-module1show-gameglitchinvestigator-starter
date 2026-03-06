# FIX: Refactored game logic functions into logic_utils.py using Copilot Agent mode
def get_range_for_difficulty(difficulty: str):
    """
    Return the inclusive range (low, high) of numbers for a given difficulty level.
    
    Args:
        difficulty (str): The difficulty level. Supported values are "Easy", "Normal", and "Hard".
    
    Returns:
        tuple: A tuple of two integers (low, high) representing the inclusive range.
               - "Easy": (1, 20)
               - "Normal": (1, 100)
               - "Hard": (1, 200)
               - Default/Unknown: (1, 100)
    
    Examples:
        >>> get_range_for_difficulty("Easy")
        (1, 20)
        >>> get_range_for_difficulty("Hard")
        (1, 200)
        >>> get_range_for_difficulty("Unknown")
        (1, 100)
    """
    if difficulty == "Easy":
        return 1, 20
    if difficulty == "Normal":
        return 1, 100
    if difficulty == "Hard":
        return 1, 200
    return 1, 100


def parse_guess(raw: str):
    """
    Parse and validate a user's guess input.

    Args:
        raw (str): The raw input string from the user.
    Returns:
        tuple: A tuple containing:
            - bool: True if the guess is valid, False otherwise.
            - int or None: The parsed integer value if valid, None if invalid.
            - str or None: An error message if invalid, None if valid.
    Raises:
        None: Does not raise exceptions; returns error messages instead.
    Examples:
        >>> parse_guess("42")
        (True, 42, None)
        >>> parse_guess("")
        (False, None, "Enter a guess.")
        >>> parse_guess("3.14")
        (False, None, "Enter a whole number.")
        >>> parse_guess("abc")
        (False, None, "That is not a number.")
    """
    if not raw:
        return False, None, "Enter a guess."

    try:
        if "." in raw:
            return False, None, "Enter a whole number."
        value = int(raw)
    except ValueError:
        return False, None, "That is not a number."

    return True, value, None


def check_guess(guess: int, secret: int) -> str:
    """
    Compare a guess against the secret number and return feedback.
    
    Args:
        guess (int): The number guessed by the player.
        secret (int): The correct secret number to match against.
    
    Returns:
        str: "Win" if guess equals secret, "Too High" if guess is greater than secret,
             or "Too Low" if guess is less than secret.
    """
    if guess == secret:
        return "Win"
    if guess > secret:
        return "Too High"
    return "Too Low"


def update_score(current_score: int, outcome: str, attempt_number: int) -> int:
    """
    Updates the player's score based on the game outcome and attempt number.

    Args:
        current_score (int): The player's current score before the update.
        outcome (str): The result of the game attempt. Possible values are:
            - "Win": Player guessed correctly
            - "Too High": Player's guess was too high
            - "Too Low": Player's guess was too low
        attempt_number (int): The current attempt number (1-indexed).
    Returns:
        int: The updated score after applying the outcome modifier.
    Scoring rules:
        - "Win": Awards 100 - (10 * attempts_after_first), minimum 10 points
        - "Too High": Awards 5 points if attempt_number is even, otherwise deducts 5 points
        - "Too Low": Deducts 5 points
        - Any other outcome: Returns current_score unchanged
    """
    if outcome == "Win":
        points = 100 - 10 * max(attempt_number - 1, 0)
        if points < 10:
            points = 10
        return current_score + points

    if outcome == "Too High":
        if attempt_number % 2 == 0:
            return current_score + 5
        return current_score - 5

    if outcome == "Too Low":
        return current_score - 5

    return current_score


HIGH_SCORE_FILE = "high_score.txt"


def load_high_score(filepath: str = HIGH_SCORE_FILE) -> int:
    """
    Load the high score from a file.
    
    Reads the high score value from the specified file. If the file does not exist
    or contains invalid data, returns 0 as the default high score.
    
    Args:
        filepath (str): The path to the file containing the high score.
                       Defaults to HIGH_SCORE_FILE constant.
    
    Returns:
        int: The high score as an integer. Returns 0 if the file is not found
             or the file contents cannot be converted to an integer.
    """
    try:
        with open(filepath, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def reset_high_score(filepath: str = HIGH_SCORE_FILE) -> None:
    """
    Reset the high score to 0 by writing to the high score file.
    
    Args:
        filepath (str): The path to the file where the high score is stored.
                       Defaults to HIGH_SCORE_FILE constant.
    
    Returns:
        None
    """
    with open(filepath, "w") as f:
        f.write("0")


def save_high_score(score: int, filepath: str = HIGH_SCORE_FILE) -> bool:
    """
    Save a high score to a file if it exceeds the current best score.
    
    Args:
        score (int): The score to potentially save as the new high score.
        filepath (str): The path to the file where the high score is stored.
                       Defaults to HIGH_SCORE_FILE.
    
    Returns:
        bool: True if the score was saved (score exceeded current best),
              False otherwise.
    """
    current_best = load_high_score(filepath)
    if score > current_best:
        with open(filepath, "w") as f:
            f.write(str(score))
        return True
    return False
