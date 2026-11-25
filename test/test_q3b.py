import util
import util_lab_7 as lab7

BOARD = lab7.board_from_string("XO_/_XO/O__")
VALID_POSITION_HINT = ("This position is valid (a list of 2 indexes that are each 0, 1 or 2), so it should not fail "
                       "an assert statement. Check the conditions in your assert statements.")
TYPE_HINT = ("Check that the position is a list with an assert statement (e.g. `assert type(position) == list`) "
             "*before* using it.")
CHECK_FIRST_HINT = "Check the position with assert statements at the start of your function, *before* using it to index the board."
NEGATIVE_HINT = ("Python allows negative indexes (board[-1] is the last row), so using -1 doesn't crash. But -1 isn't "
                 "a valid row or column for a tic tac toe position, so your assert statements must check that each "
                 "index is 0, 1 or 2.")


def is_occupied():
  """Return the is_occupied function defined in src/q3.py"""
  return util.get_student_function("q3", "is_occupied", "Part 3b")


def check(board, position, expected, explanation):
  call_text = util.describe_call(is_occupied(), board, position)
  actual = util.call_without_modifying(is_occupied(), board, position,
                                       hints={AssertionError: VALID_POSITION_HINT})
  row, column = position
  if actual == (board[column][row] != "") and actual != expected:
    explanation += f"\nHINT: {lab7.ROW_COLUMN_HINT}"
  elif isinstance(actual, str):
    explanation += "\nHINT: return True or False, not the contents of the cell."
  util.check_returned(call_text, actual, expected, explanation)


def check_assert(position, reason, returned_hint=None):
  util.check_raises_assertion_error(is_occupied(), (lab7.make_empty_board(), position), reason,
                                    hints={TypeError: TYPE_HINT, IndexError: CHECK_FIRST_HINT},
                                    returned_hint=returned_hint)


def test_is_occupied_is_defined():
  is_occupied()


def test_is_occupied_takes_two_parameters():
  util.check_parameter_count(is_occupied(), 2, "the board, and the position to check")


def test_is_occupied_has_a_docstring():
  is_occupied()
  util.check_has_docstring("q3", "is_occupied")


def test_is_occupied_returns_instead_of_printing(capsys):
  util.check_returns_instead_of_printing(capsys, is_occupied(), lab7.make_empty_board(), [0, 0])


def test_nothing_is_occupied_on_an_empty_board():
  for row in range(3):
    for column in range(3):
      check(lab7.make_empty_board(), [row, column], False, "Every cell of an empty board is empty.")


def test_everything_is_occupied_on_a_full_board():
  board = lab7.board_from_string("XOX/OXO/OXO")
  for row in range(3):
    for column in range(3):
      check(board, [row, column], True, "Every cell of a full board is occupied.")


def test_is_occupied_on_a_partly_full_board():
  for position, expected in [([0, 0], True), ([0, 2], False), ([1, 1], True), ([2, 1], False), ([1, 2], True),
                             ([2, 0], True), ([1, 0], False)]:
    row, column = position
    check(BOARD, position, expected,
          f"Row {row}, column {column} of the board contains {BOARD[row][column]!r}.\n{lab7.show_board(BOARD)}")


def test_position_that_is_not_a_list_fails_assert():
  check_assert((1, 1), "the position (1, 1) is a tuple, not a list",
               "(1, 1) has 2 valid indexes, so only a check that the position is a list (e.g. "
               "`assert type(position) == list`) can catch it.")
  check_assert("11", "the position \"11\" is a string, not a list")
  check_assert(4, "the position 4 is an int, not a list")


def test_position_with_wrong_number_of_elements_fails_assert():
  check_assert([1], "the position has only 1 element (it needs a row and a column)")
  check_assert([0, 1, 2], "the position has 3 elements (it needs just a row and a column)")
  check_assert([], "the position is empty (it needs a row and a column)")


def test_position_out_of_range_fails_assert():
  check_assert([3, 0], "the row index 3 is not 0, 1 or 2")
  check_assert([0, 3], "the column index 3 is not 0, 1 or 2")


def test_negative_position_fails_assert():
  check_assert([-1, 0], "the row index -1 is not 0, 1 or 2", NEGATIVE_HINT)
  check_assert([0, -1], "the column index -1 is not 0, 1 or 2", NEGATIVE_HINT)
