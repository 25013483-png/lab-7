import util
import util_lab_7 as lab7


def board_state():
  """Return the board_state function defined in src/q3.py"""
  return util.get_student_function("q3", "board_state", "Part 3d")


def check(rows, explanation):
  """Check board_state for the board described by rows (see lab7.board_from_string)"""
  board = lab7.board_from_string(rows)
  expected = lab7.board_state(board)
  call_text = util.describe_call(board_state(), board)
  actual = util.call_without_modifying(board_state(), board)
  explanation = f"For the board\n{lab7.show_board(board)}\n{explanation}"
  empty_lines = [line for line in lab7.winning_lines(board) if line == ["", "", ""]]
  if expected in ["X", "O"] and actual == "" and empty_lines:
    explanation += f"\nHINT: {lab7.EMPTY_LINE_HINT}"
  elif expected == "" and actual == "Draw":
    explanation += f"\nHINT: {lab7.DRAW_TOO_SOON_HINT}"
  elif expected in ["X", "O"] and actual == "Draw":
    explanation += f"\nHINT: {lab7.WINNER_FIRST_HINT}"
  elif expected in ["X", "O"] and actual in ["X", "O", ""]:
    explanation += "\nHINT: check that your function checks all 8 lines: 3 rows, 3 columns and 2 diagonals."
  util.check_returned(call_text, actual, expected, explanation)


def test_board_state_is_defined():
  board_state()


def test_board_state_takes_one_parameter():
  util.check_parameter_count(board_state(), 1, "the board")


def test_board_state_has_a_docstring():
  board_state()
  util.check_has_docstring("q3", "board_state")


def test_board_state_returns_instead_of_printing(capsys):
  util.check_returns_instead_of_printing(capsys, board_state(), lab7.board_from_string("XXX/OO_/___"))


def test_empty_board_has_no_winner_yet():
  check("___/___/___", "Nobody has won yet, and there are empty cells, so the game isn't over: return \"\".")


def test_partly_full_board_with_no_winner_yet():
  check("XO_/_X_/__O", "Nobody has won yet, and there are empty cells, so the game isn't over: return \"\".")
  check("XOX/___/___", "Nobody has won yet (a line must have 3 of the SAME symbol), so return \"\".")
  check("XOX/OXO/OX_", "Nobody has won yet, and there is still one empty cell, so return \"\".")


def test_x_wins_with_a_row():
  for rows, row in [("XXX/OO_/___", "top"), ("OO_/XXX/___", "middle"), ("OO_/___/XXX", "bottom")]:
    check(rows, f"X has the whole {row} row, so X wins.")


def test_x_wins_with_a_column():
  for rows, column in [("XO_/XO_/X__", "left"), ("OX_/OX_/_X_", "middle"), ("O_X/O_X/__X", "right")]:
    check(rows, f"X has the whole {column} column, so X wins.")


def test_x_wins_with_a_diagonal():
  check("XO_/OX_/__X", "X has the diagonal from the top left to the bottom right, so X wins.")
  check("O_X/OX_/X__", "X has the diagonal from the bottom left to the top right, so X wins.")


def test_o_wins_with_a_row():
  for rows, row in [("OOO/XX_/X__", "top"), ("XX_/OOO/__X", "middle"), ("XX_/_X_/OOO", "bottom")]:
    check(rows, f"O has the whole {row} row, so O wins.")


def test_o_wins_with_a_column():
  for rows, column in [("OX_/OX_/O_X", "left"), ("XOX/_O_/XO_", "middle"), ("X_O/X_O/_XO", "right")]:
    check(rows, f"O has the whole {column} column, so O wins.")


def test_o_wins_with_a_diagonal():
  check("OX_/XO_/X_O", "O has the diagonal from the top left to the bottom right, so O wins.")
  check("X_O/XO_/O_X", "O has the diagonal from the bottom left to the top right, so O wins.")


def test_win_after_an_empty_line():
  check("___/XXX/OO_", "X has the whole middle row, so X wins (even though the top row is empty).")
  check("_XO/_XO/__O", "O has the whole right column, so O wins (even though the left column is empty).")


def test_full_board_with_no_winner_is_a_draw():
  check("XOX/XOO/OXX", "Every cell is occupied and nobody has won, so it's a draw.")
  check("OXO/XXO/XOX", "Every cell is occupied and nobody has won, so it's a draw.")


def test_full_board_with_a_winner_is_not_a_draw():
  check("XXX/OOX/OXO", "Every cell is occupied, but X has the top row, so X wins (it is not a draw).")
  check("XOX/OXO/OXX", "Every cell is occupied, but X has a diagonal, so X wins (it is not a draw).")
