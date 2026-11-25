import util
import util_lab_7 as lab7

VALID_HINT = ("This move is valid (an empty position, and the symbol \"X\" or \"O\"), so it should not fail an assert "
              "statement or raise an error. Check the conditions in your assert statement and your use of is_occupied.")
SYMBOL_TYPE_HINT = "Check the symbol with an assert statement at the start of your function, before using it."
POSITION_HINT = ("Call is_occupied(board, position) before using the position to index the board: its assert "
                 "statements check that the position is valid.")


def place():
  """Return the place function defined in src/q3.py"""
  return util.get_student_function("q3", "place", "Part 3c")


def check_place(board, position, symbol, explanation):
  """Call place(board, position, symbol) and check that it changed board to expected"""
  expected = [row[:] for row in board]
  expected[position[0]][position[1]] = symbol
  before = lab7.show_board(board)
  call_text = util.describe_call(place(), board, position, symbol)
  result = util.call(place(), board, position, symbol, hints={AssertionError: VALID_HINT, ValueError: VALID_HINT})
  if board == expected:
    assert result is None, (
        f"{call_text} placed the symbol correctly, but it also returned {result!r}. place should change the board "
        f"it is given and NOT return anything (see Part 3c of the README).")
    return
  message = f"After {call_text} the board should be\n{lab7.show_board(expected)}\nbut it is\n{lab7.show_board(board)}\n{explanation}"
  if result == expected:
    message += ("\nHINT: your function returned a new board with the symbol on it, but it must change the board "
                "it is given instead (which is why place is not a pure function).")
  elif lab7.show_board(board) == before:
    message += "\nHINT: place must change the board it is given (which is why place is not a pure function)."
  elif board[position[1]][position[0]] == symbol:
    message += f"\nHINT: {lab7.ROW_COLUMN_HINT}"
  assert False, message


def test_place_is_defined():
  place()


def test_place_takes_three_parameters():
  util.check_parameter_count(place(), 3, "the board, the position, and the symbol to place")


def test_place_has_a_docstring():
  place()
  util.check_has_docstring("q3", "place")


def test_place_puts_the_symbol_on_the_board():
  check_place(lab7.make_empty_board(), [1, 2], "O", "Row 1, column 2 is the right-hand cell of the middle row.")
  check_place(lab7.make_empty_board(), [0, 0], "X", "Row 0, column 0 is the top left cell.")


def test_place_several_symbols():
  board = lab7.make_empty_board()
  for position, symbol in [([1, 2], "O"), ([0, 0], "X"), ([2, 1], "X"), ([1, 1], "O"), ([2, 0], "O")]:
    check_place(board, position, symbol, "Each call to place should add one symbol to the board, and leave the "
                "rest of the board as it was.")


def test_invalid_symbol_fails_assert():
  for symbol, reason in [("A", "\"A\" is not \"X\" or \"O\""), ("", "the symbol is empty"),
                         ("x", "the symbol must be an upper case \"X\""), ("XO", "\"XO\" is not \"X\" or \"O\""),
                         (1, "1 is not \"X\" or \"O\"")]:
    util.check_raises_assertion_error(place(), (lab7.make_empty_board(), [0, 0], symbol), reason,
                                      hints={TypeError: SYMBOL_TYPE_HINT})


def test_invalid_position_fails_assert():
  for position, reason in [([3, 0], "the row index 3 is not 0, 1 or 2"), ([0], "the position needs 2 elements"),
                           ([-1, 0], "the row index -1 is not 0, 1 or 2")]:
    util.check_raises_assertion_error(place(), (lab7.make_empty_board(), position, "X"), reason,
                                      hints={IndexError: POSITION_HINT, TypeError: POSITION_HINT},
                                      returned_hint=POSITION_HINT)


def test_placing_on_an_occupied_position_raises_value_error():
  for symbol in ["O", "X"]:
    board = lab7.board_from_string("X__/___/___")
    util.check_raises(place(), (board, [0, 0], symbol), ValueError, "position [0, 0] is already occupied",
                      message="Position already occupied",
                      hints={AssertionError: "Use `raise ValueError(\"Position already occupied\")` for an occupied "
                             "position, rather than an assert statement."},
                      returned_hint="Use is_occupied to check the position first, and `raise ValueError(...)` if it "
                      "is occupied.")
    assert board == lab7.board_from_string("X__/___/___"), (
        f"place(board, [0, 0], {symbol!r}) correctly raised a ValueError because [0, 0] is occupied, but it changed "
        f"the board first:\n{lab7.show_board(board)}\nHINT: check whether the position is occupied *before* "
        f"placing the symbol.")


def test_place_uses_is_occupied():
  definition = util.find_function_def("q3", "place")
  assert definition is not None, "Define a function named place in src/q3.py, as described in Part 3c of the README."
  assert util.find_calls(definition, "is_occupied") != [], (
      "place should call your is_occupied function to check whether the position is already occupied "
      "(see Part 3c of the README).")


def test_place_has_a_comment_saying_why_it_is_not_pure():
  comments = util.comments_above("q3", "place")
  assert comments is not None, "Define a function named place in src/q3.py, as described in Part 3c of the README."
  assert comments.strip() != "", (
      "Add a comment (lines starting with #) directly above the `def place` line that explains why place can NOT "
      "be considered a pure function (see Part 3c of the README).")
