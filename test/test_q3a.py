import util
import util_lab_7 as lab7

SHARED_ROWS_HINT = (
    "Your board's 3 rows are all the same list (they have the same id), so changing a cell in one row changes that "
    "cell in every row! This is what happens with [[\"\"] * 3] * 3: the outer * 3 makes 3 references to ONE row "
    "list, just like foods2 in Part 1 is an alias of foods. Make a new list for each row instead, e.g. with a loop "
    "that appends [\"\"] * 3 to the board three times.")


def make_empty_board():
  """Return the make_empty_board function defined in src/q3.py"""
  return util.get_student_function("q3", "make_empty_board", "Part 3a")


def test_make_empty_board_is_defined():
  make_empty_board()


def test_make_empty_board_takes_no_parameters():
  util.check_parameter_count(make_empty_board(), 0, "it always makes the same empty board")


def test_make_empty_board_has_a_docstring():
  make_empty_board()
  util.check_has_docstring("q3", "make_empty_board")


def test_make_empty_board_returns_instead_of_printing(capsys):
  util.check_returns_instead_of_printing(capsys, make_empty_board())


def test_make_empty_board_returns_3_rows_of_3_empty_strings():
  board = util.call(make_empty_board())
  explanation = "An empty board is a list of 3 rows, where each row is a list of 3 empty strings (\"\")."
  cells = [cell for row in board for cell in row] if isinstance(board, list) and all(isinstance(r, list) for r in board) else []
  if any(cell in [" ", None] for cell in cells):
    explanation += "\nHINT: an empty cell is the empty string \"\" (quotes with nothing between them), not a space or None."
  util.check_returned("make_empty_board()", board, lab7.make_empty_board(), explanation)


def test_make_empty_board_rows_are_different_lists():
  board = util.call(make_empty_board())
  ids = [id(row) for row in board]
  if len(set(ids)) < len(ids):
    board[0][0] = "X"
    assert False, (
        f"Setting board[0][0] = \"X\" on the board returned by make_empty_board() should only change the top left "
        f"cell, but your board became\n{lab7.show_board(board)}\nHINT: {SHARED_ROWS_HINT}")


def test_make_empty_board_makes_a_new_board_each_time():
  first = util.call(make_empty_board())
  first[0][0] = "X"
  second = util.call(make_empty_board())
  assert second == lab7.make_empty_board(), (
      f"After changing a cell of one board returned by make_empty_board(), calling make_empty_board() again should "
      f"return a new, empty board, but it returned\n{lab7.show_board(second)}\n"
      f"HINT: make the board inside the function, so that each call makes a new board. (Don't return a board that "
      f"was made outside the function.)")


def test_shared_rows_are_explained():
  lab7.check_explanation(
      "q3", lambda words: words & {"row", "rows", "list", "lists", "board"} and words & {
          "same", "alias", "aliases", "refer", "refers", "reference", "references", "id", "ids", "copy", "copies",
          "share", "shared", "point", "points", "object", "objects"},
      "Part 3a asks you to explain, in a comment in src/q3.py, why [[\"\"] * 3] * 3 would NOT work as an empty "
      "board. (Try it in a REPL as the README shows: what happens when you change one cell?) Explain what is "
      "wrong with the rows of that board.")


def test_q3_has_no_print_calls():
  lab7.check_no_print_calls("q3", "make_empty_board, is_occupied, board_state and board_to_str")
