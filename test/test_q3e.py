import util
import util_lab_7 as lab7

NEWLINE_AT_END_HINT = "There should be no newline (\\n) at the end of the string: only between the lines."
TRAILING_SPACE_HINT = ("Each cell is 3 characters wide, including the last cell of each row, so every row ends with a "
                       "space (e.g. \" X | O | X \").")
EMPTY_CELL_HINT = ("An empty cell must also be 3 characters wide (3 spaces). Your empty cells are only 2 spaces wide: "
                   "the empty string \"\" between two spaces is just \"  \".")
MODIFIED_HINT = ("Don't change the board (e.g. by replacing \"\" with \" \") to make it easier to display. Build the "
                 "string from the cells instead, e.g. using \" \" for a cell that is \"\".")


def board_to_str():
  """Return the board_to_str function defined in src/q3.py"""
  return util.get_student_function("q3", "board_to_str", "Part 3e")


def strip_lines(text):
  return "\n".join(line.rstrip() for line in text.strip("\n").split("\n"))


def check(rows, explanation):
  board = lab7.board_from_string(rows)
  expected = lab7.board_to_str(board)
  call_text = util.describe_call(board_to_str(), board)
  actual = util.call_without_modifying(board_to_str(), board, modified_hint=MODIFIED_HINT)
  if isinstance(actual, str) and actual != expected:
    two_wide = "\n---+---+---\n".join("|".join(f" {cell} " for cell in row) for row in board)
    if actual.rstrip("\n") == expected:
      explanation += f"\nHINT: {NEWLINE_AT_END_HINT}"
    elif actual == two_wide or actual.rstrip("\n") == two_wide:
      explanation += f"\nHINT: {EMPTY_CELL_HINT}"
    elif strip_lines(actual) == strip_lines(expected):
      explanation += f"\nHINT: {TRAILING_SPACE_HINT}"
  util.check_returned(call_text, actual, expected, explanation)


def test_board_to_str_is_defined():
  board_to_str()


def test_board_to_str_takes_one_parameter():
  util.check_parameter_count(board_to_str(), 1, "the board")


def test_board_to_str_has_a_docstring():
  board_to_str()
  util.check_has_docstring("q3", "board_to_str")


def test_board_to_str_returns_instead_of_printing(capsys):
  util.check_returns_instead_of_printing(capsys, board_to_str(), lab7.board_from_string("XO_/_X_/__O"))


def test_board_to_str_of_a_full_board():
  check("XOX/OXO/OXO", "Each cell is the symbol with a space on either side, cells are separated by |, and rows "
        "are separated by a line of ---+---+---.")


def test_board_to_str_of_the_readme_example():
  check("_OX/_XO/X_O", "This is the example board in Part 3e of the README. An empty cell is 3 spaces wide.")


def test_board_to_str_of_an_empty_board():
  check("___/___/___", "Every cell of an empty board is 3 spaces.")


def test_board_to_str_of_a_partly_full_board():
  check("X__/_O_/__X", "Each cell is 3 characters wide, including the empty ones.")
