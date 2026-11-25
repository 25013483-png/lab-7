import ast
import sys
import pytest
import util
import util_lab_7 as lab7
from util_lab_7 import Move

PART_3_FUNCTIONS = ["make_empty_board", "is_occupied", "place", "board_state", "board_to_str"]
X_WINS = r"\bX\b.*\b(wins?|won|winner)\b|\b(wins?|won|winner)\b.*\bX\b"
O_WINS = r"\bO\b.*\b(wins?|won|winner)\b|\b(wins?|won|winner)\b.*\bO\b"
DRAW = r"\b(draw|tie)\b"


def tictactoe():
  """Return the tictactoe function defined in src/q4.py"""
  return util.get_student_function("q4", "tictactoe", "Part 4")


def check_asks_again(monkeypatch, capsys, moves, problem):
  """Play moves, then check that the game asks for another move (rather than crashing or ending)"""
  transcript, player = lab7.play(monkeypatch, capsys, moves, stop=True)
  if not player.stopped:
    player.fail(f"{problem} The game should tell the player what is wrong and ask them again, but it ended instead.")
  return transcript, player


# How the program is written
def test_importing_q4_does_not_start_the_game(capsys):
  sys.modules.pop("q4", None)
  util.import_student_module(
      "q4", input_advice="Put the code that starts the game inside your `if __name__ == \"__main__\":` block.")
  printed = capsys.readouterr().out
  assert printed == "", (
      f"When src/q4.py is imported it should not start the game, but it printed:\n{printed}\n"
      f"Put the code that starts the game inside your `if __name__ == \"__main__\":` block.")


def test_q4_imports_q3():
  assert "q3" in util.imported_modules("q4"), (
      "src/q4.py must import the functions you wrote in src/q3.py (e.g. `from q3 import ...`), as described in "
      "Part 4 of the README.")


def test_q4_does_not_copy_q3_functions():
  copied = [name for name in PART_3_FUNCTIONS if name in util.defined_function_names("q4")]
  assert copied == [], (
      f"src/q4.py should not contain its own definition of {', '.join(copied)}. "
      f"Delete it and import the function from src/q3.py instead!")


def test_tictactoe_is_defined():
  tictactoe()


def test_tictactoe_takes_no_parameters():
  util.check_parameter_count(tictactoe(), 0, "Part 4 of the README says it is parameterless")


def test_main_guard_calls_tictactoe():
  tree = util.parse_source("q4")
  guards = [node for node in ast.walk(tree) if util.is_main_guard(node)]
  assert guards != [], (
      "src/q4.py must use a main guard (`if __name__ == \"__main__\":`) that calls tictactoe() to start the game, "
      "as described in Part 4 of the README.")
  assert any(util.find_calls(ast.Module(body=guard.body, type_ignores=[]), "tictactoe") for guard in guards), (
      "Your `if __name__ == \"__main__\":` block should call tictactoe() to start the game.")


def test_q4_uses_the_part_3_functions():
  tree = util.parse_source("q4")
  needed = {"make_empty_board": "start with an empty board", "place": "put each player's symbol on the board",
            "board_state": "check for a win or a draw", "board_to_str": "display the board"}
  missing = [f"{name} (to {why})" for name, why in needed.items() if util.find_calls(tree, name) == []]
  assert missing == [], (
      "The game must use the functions you wrote in Part 3, but src/q4.py doesn't call:\n" +
      "".join(f"  - {name}\n" for name in missing))


def test_q4_uses_is_occupied():
  assert util.find_calls(util.parse_source("q4"), "is_occupied") != [], (
      "Use is_occupied to check that a player isn't trying to use an occupied position (see requirement 3 in "
      "Part 4 of the README), so you can ask them again instead of letting place() raise a ValueError.")


# Playing the game
def test_game_shows_the_empty_board_before_the_first_move(monkeypatch, capsys):
  transcript, player = lab7.play(monkeypatch, capsys, [], stop=True)
  if not player.stopped:
    player.fail("The game ended without asking for a move.")
  shown = lab7.q3_function("board_to_str", lab7.board_to_str)(lab7.make_empty_board())
  if shown not in transcript:
    player.fail("Before asking for the first move, the game should display the empty board (using board_to_str).")


def test_x_can_win(monkeypatch, capsys):
  lab7.check_game_result(monkeypatch, capsys, [(0, 0), (1, 0), (0, 1), (1, 1), (0, 2)],
                         lab7.board_from_string("XXX/OO_/___"), X_WINS, "X wins")


def test_o_can_win(monkeypatch, capsys):
  lab7.check_game_result(monkeypatch, capsys, [(0, 0), (1, 1), (0, 1), (0, 2), (2, 2), (2, 0)],
                         lab7.board_from_string("XXO/_O_/O_X"), O_WINS, "O wins")


def test_game_can_be_a_draw(monkeypatch, capsys):
  lab7.check_game_result(monkeypatch, capsys, [(0, 0), (0, 1), (0, 2), (1, 1), (1, 0), (1, 2), (2, 1), (2, 0), (2, 2)],
                         lab7.board_from_string("XOX/XOO/OXX"), DRAW, "it's a draw")


def test_win_with_the_last_move_is_not_a_draw(monkeypatch, capsys):
  lab7.check_game_result(monkeypatch, capsys, [(0, 2), (0, 1), (0, 0), (1, 0), (2, 1), (1, 2), (1, 1), (2, 0), (2, 2)],
                         lab7.board_from_string("XOX/OXO/OXX"), X_WINS, "X wins (the board is full, but X has a line)")


def test_occupied_position_is_rejected(monkeypatch, capsys):
  transcript, player = check_asks_again(monkeypatch, capsys, [(0, 0), (0, 0)],
                                        "Player O tried to move to [0, 0], which X already occupies.")
  overwritten = lab7.q3_function("board_to_str", lab7.board_to_str)(lab7.board_from_string("O__/___/___"))
  if overwritten in transcript:
    player.fail("Player O was allowed to replace X's symbol at [0, 0].")


def test_invalid_moves_are_rejected(monkeypatch, capsys):
  for move, problem in [(Move("abc", "abc", "abc"), "The player typed abc, which is not a number."),
                        (Move("", "", "(blank)"), "The player didn't type anything (just pressed Enter)."),
                        (Move("3", "3{sep}1", "3, 1"), "The player typed 3 for the row, which is not 0, 1 or 2."),
                        (Move("-1", "-1{sep}0", "-1, 0"), "The player typed -1 for the row, which is not 0, 1 or 2.")]:
    check_asks_again(monkeypatch, capsys, [move], problem)
