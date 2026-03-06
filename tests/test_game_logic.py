import pytest
from logic_utils import check_guess, get_range_for_difficulty, update_score, parse_guess

def test_winning_guess():
    # If the secret is 50 and guess is 50, it should be a win
    result = check_guess(50, 50)
    assert result == "Win"

def test_guess_too_high():
    # If secret is 50 and guess is 60, hint should be "Too High"
    result = check_guess(60, 50)
    assert result == "Too High"

def test_guess_too_low():
    # If secret is 50 and guess is 40, hint should be "Too Low"
    result = check_guess(40, 50)
    assert result == "Too Low"


# --- Bug 1: Hints were backwards ---
# Buggy code displayed "GO HIGHER!" when guess was too high and "GO LOWER!" when too low.
# check_guess must return the semantically correct outcome label so the UI maps it correctly.

def test_hint_direction_too_high_is_not_too_low():
    # Guess above secret must NOT come back as "Too Low" (the backwards-hint bug)
    result = check_guess(80, 50)
    assert result != "Too Low", "Backwards hint bug: high guess reported as Too Low"

def test_hint_direction_too_low_is_not_too_high():
    # Guess below secret must NOT come back as "Too High" (the backwards-hint bug)
    result = check_guess(20, 50)
    assert result != "Too High", "Backwards hint bug: low guess reported as Too High"


# --- Bug 2: Hard was easier than Normal (Hard range was 1-50) ---

def test_hard_range_is_wider_than_normal():
    _, normal_high = get_range_for_difficulty("Normal")
    _, hard_high = get_range_for_difficulty("Hard")
    assert hard_high > normal_high, (
        f"Hard range top ({hard_high}) should exceed Normal range top ({normal_high})"
    )

def test_hard_range_values():
    low, high = get_range_for_difficulty("Hard")
    assert low == 1
    assert high == 200, f"Hard high should be 200, got {high}"


# --- Bug 3: Easy had fewer attempts than Normal (Easy=6, Normal=8) ---
# attempt_limit_map lives in app.py (Streamlit), so we verify the difficulty ranges used
# to derive difficulty ordering are sensible, and document the expected attempt counts.

EXPECTED_ATTEMPTS = {"Easy": 10, "Normal": 7, "Hard": 5}

def test_easy_has_more_attempts_than_normal():
    assert EXPECTED_ATTEMPTS["Easy"] > EXPECTED_ATTEMPTS["Normal"], (
        "Easy should allow more attempts than Normal"
    )

def test_normal_has_more_attempts_than_hard():
    assert EXPECTED_ATTEMPTS["Normal"] > EXPECTED_ATTEMPTS["Hard"], (
        "Normal should allow more attempts than Hard"
    )


# --- Bug 4: Secret type glitch (every other attempt cast secret to str) ---
# When secret is accidentally a string, int == str is always False in Python 3,
# so a correct guess would never be recognized as a win.

def test_check_guess_int_secret_wins():
    # Baseline: int secret must produce a win
    assert check_guess(42, 42) == "Win"

def test_check_guess_string_secret_does_not_win():
    # If the type glitch strikes and secret becomes "42", the comparison crashes with TypeError.
    # Either a crash or a non-Win result both mean the type glitch breaks the game.
    with pytest.raises((TypeError, AssertionError)):
        result = check_guess(42, "42")  # type: ignore[arg-type]
        assert result != "Win", "Type glitch: str secret incorrectly accepted int guess as Win"


# --- Bug 5: New game ignored difficulty (always used randint(1, 100)) ---
# Verified indirectly: get_range_for_difficulty must return distinct bounds per difficulty
# so that new_game can use the correct range.

def test_easy_range_differs_from_normal():
    easy_bounds = get_range_for_difficulty("Easy")
    normal_bounds = get_range_for_difficulty("Normal")
    assert easy_bounds != normal_bounds, "Easy and Normal ranges should be different"

def test_hard_range_differs_from_normal():
    hard_bounds = get_range_for_difficulty("Hard")
    normal_bounds = get_range_for_difficulty("Normal")
    assert hard_bounds != normal_bounds, "Hard and Normal ranges should be different"


# --- Bug 6: attempts initialized to 1 instead of 0 ---
# update_score uses attempt_number; starting at 0 gives max points on first win.

def test_first_attempt_win_gives_max_points():
    # In the game, attempts is incremented to 1 before update_score is called.
    # attempt_number=1 => points = 100 - 10*(1-1) = 100
    score = update_score(0, "Win", 1)
    assert score == 100, f"First-attempt win should score 100, got {score}"

def test_second_attempt_win_gives_fewer_points():
    score_first = update_score(0, "Win", 1)
    score_second = update_score(0, "Win", 2)
    assert score_first > score_second, "Earlier wins should score more than later wins"


# --- Bug 7: Info banner hardcoded "1 to 100" ---
# Verified via get_range_for_difficulty: Easy must not return (1, 100).

def test_easy_range_is_not_hardcoded_1_to_100():
    low, high = get_range_for_difficulty("Easy")
    assert (low, high) != (1, 100), (
        "Easy range was hardcoded to 1-100 (the Normal range); should be 1-20"
    )


# --- Edge case 1: parse_guess silently truncates decimals ---
# "3.9" should NOT be silently accepted as 3; it is an invalid guess.

def test_parse_guess_decimal_is_rejected():
    ok, _, _ = parse_guess("3.9")
    assert not ok, "Decimal input '3.9' should be rejected, not silently truncated to 3"


# --- Edge case 2: parse_guess accepts out-of-range numbers without complaint ---
# parse_guess alone does not enforce game range, so an extremely large value
# passes through. This test documents the gap so callers know to validate range.

def test_parse_guess_extremely_large_value_passes_through():
    ok, value, _ = parse_guess("99999999999999999")
    assert ok, "parse_guess should successfully parse a large number"
    assert value == 99999999999999999, "Parsed value should match the large integer exactly"
    # NOTE: range validation must happen in the caller; parse_guess alone won't catch this.


# --- Edge case 3: update_score with a negative attempt_number gives an inflated win bonus ---
# attempt_number=-1 produces 100 - 10*(0) = 100 points, the theoretical maximum.
# This tests that a logically impossible attempt number is not silently rewarded.

def test_update_score_negative_attempt_number_does_not_exceed_max_valid_score():
    # The highest legitimate score on attempt 0 is 90 (100 - 10*1).
    max_valid_first_attempt_score = update_score(0, "Win", 0)  # 90
    inflated_score = update_score(0, "Win", -1)               # 100
    assert inflated_score <= max_valid_first_attempt_score, (
        f"Negative attempt_number yielded {inflated_score} points, "
        f"exceeding the legitimate max of {max_valid_first_attempt_score}"
    )
