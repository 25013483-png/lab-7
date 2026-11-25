"""Helpers specific to lab 7 (lists and tic tac toe)"""

import ast
import math
import re
import pytest
import util

# ---------------------------------------------------------------------------
# Common mistakes

RETURN_IN_LOOP_HINT = ("Your function seems to stop after looking at only the first item. Check that your `return` "
                       "statement is *after* the loop (not indented inside it), so the loop can go through the "
                       "whole list first.")
SKIPPED_ITEM_HINT = ("Your function seems to skip the first or last item of the list. If you loop over indexes, "
                     "use `range(len(...))`, which goes from 0 up to (but not including) the length of the list.")
MAP_OBJECT_HINT = ("map() and filter() don't return a list. Wrap them in list(...) to get one, e.g. "
                   "list(map(...)), or use a loop or list comprehension instead.")
NEW_LIST_HINT = ("Your function returned the same list that was passed to it, not a new list. Start with an empty "
                 "list (e.g. `result = []`) and append the items you want to it.")
REMOVE_WHILE_LOOPING_HINT = (
    "Removing items from a list while you are looping over it also makes the loop skip items. Instead, start with "
    "an empty list and append the items you want to keep to it.")
INDEX_HINT = ("Remember that list indexes start at 0: the first item is at index 0, the second at index 1, and so on. "
              "Negative indexes count from the end: the last item is at index -1.")

# ---------------------------------------------------------------------------
# Part 2: traversal patterns

PATTERNS = {
    "map": "builds a new list by doing the same thing to every item",
    "filter": "builds a new list that keeps only some of the items",
    "reduce": "combines all of the items into a single value",
}


def check_pattern_comment(module_name, function_name, pattern, readme_part):
  """Check that the comment directly above `def function_name` says which traversal pattern it uses"""
  comments = util.comments_above(module_name, function_name)
  if comments is None:
    pytest.fail(f"Define a function named {function_name} in src/{module_name}.py, as described in {readme_part} of the README.",
                pytrace=False)
  words = set(re.findall(r"[a-z]+", comments.lower()))
  mentioned = [p for p in PATTERNS if p in words]
  if pattern in mentioned and len(mentioned) < len(PATTERNS):
    return

  explanation = "\nThe three patterns are:\n" + "".join(f"  - {p}: {meaning}\n" for p, meaning in PATTERNS.items())
  if comments == "":
    message = (f"Add a comment (a line starting with #) directly above the `def {function_name}` line that says which "
               f"traversal pattern (map, filter, or reduce) {function_name} uses, as described in {readme_part} of "
               f"the README.")
    definition = util.find_function_def(module_name, function_name)
    docstring = (ast.get_docstring(definition) or "").lower()
    if any(p in docstring for p in PATTERNS):
      message += "\nHINT: you mentioned the pattern in your docstring. The README asks for a comment *above* the def line."
  elif mentioned == []:
    message = (f"The comment above `def {function_name}` should say which traversal pattern (map, filter, or reduce) "
               f"{function_name} uses, but it doesn't mention any of them. The comment is:\n    {comments}")
  elif len(mentioned) == len(PATTERNS):
    message = (f"The comment above `def {function_name}` mentions all three traversal patterns. Say which ONE "
               f"pattern {function_name} uses. The comment is:\n    {comments}")
  else:
    message = (f"The comment above `def {function_name}` doesn't name the traversal pattern that {function_name} "
               f"uses. The comment is:\n    {comments}\nThink about what {function_name} does with the items of the list.")
  pytest.fail(message + explanation.rstrip(), pytrace=False)


EXPLANATION_NOTE = "(The tests can only check that your explanation is there: your instructor will read it.)"


def check_explanation(module_name, matches, missing_message):
  """Check that src/<module_name>.py has a comment that explains something. matches(words) is True
     if a comment with that set of (lower case) words is about the right thing. Comment lines that
     copy the README's instructions (e.g. "In a comment, explain ...") don't count"""
  too_short = False
  for block in util.find_comment_blocks(module_name):
    block = "\n".join(line for line in block.splitlines() if "in a comment" not in line.lower())
    words = re.findall(r"[a-z0-9_]+", block.lower())
    if matches(set(words)):
      if len(words) >= 6:
        return
      too_short = True
  hint = ("\nHINT: you have a comment about this, but it is very short. Explain in a sentence or two."
          if too_short else "")
  pytest.fail(f"{missing_message}{hint}\n{EXPLANATION_NOTE}", pytrace=False)


def check_uses_loop(module_name, function_name, readme_part):
  """Check that function_name traverses its list with a loop (a for loop, while loop or list comprehension)"""
  definition = util.find_function_def(module_name, function_name)
  if definition is None:
    pytest.fail(f"Define a function named {function_name} in src/{module_name}.py, as described in {readme_part} of the README.",
                pytrace=False)
  if util.find_for_loops(definition) + util.find_while_loops(definition) == []:
    pytest.fail(
        f"{function_name} must use a loop (or a list comprehension) to go through the list: Part 2 is about "
        f"practising the loop traversal patterns. (Put any one-line version using built-in functions like map() "
        f"or filter() in a comment, as the CHALLENGE in {readme_part} of the README says.)",
        pytrace=False)


def same_items(actual, expected):
  """Return True if the lists actual and expected have equal items (floats only need to be very close)"""
  if not isinstance(actual, list) or len(actual) != len(expected):
    return False
  for a, e in zip(actual, expected):
    if isinstance(e, float) and isinstance(a, (int, float)) and not isinstance(a, bool):
      if not math.isclose(a, e):
        return False
    elif a != e or type(a) != type(e):
      return False
  return True


def check_new_list(function, argument, expected, explanation, mistakes=(), hint=None, modified_hint=None):
  """Check that function(argument) returns a NEW list equal to expected, without changing argument.
     mistakes (optional) is a list of (wrong answer, hint) pairs: if the function returns one of
     the wrong answers, the matching hint is shown instead of hint"""
  call_text = util.describe_call(function, argument)
  actual = util.call_without_modifying(function, argument, modified_hint=modified_hint)
  if same_items(actual, expected):
    if actual is argument:
      pytest.fail(f"{call_text} returned the list that was passed to it.\nHINT: {NEW_LIST_HINT}", pytrace=False)
    return
  if type(actual).__name__ in ["map", "filter", "generator"]:
    hint = MAP_OBJECT_HINT
  else:
    hint = next((h for wrong, h in mistakes if same_items(actual, wrong)), hint)
  util.check_returned(call_text, actual, expected, explanation + (f"\nHINT: {hint}" if hint else ""))
  # check_returned allows e.g. [2, 3] for [2.0, 3.0]; anything else that gets here is wrong
  pytest.fail(f"{call_text} returned {actual!r}, but it should return {expected!r}.\n{explanation}" +
              (f"\nHINT: {hint}" if hint else ""),
              pytrace=False)


def check_no_print_calls(module_name, what):
  lines = util.find_print_calls(module_name)
  assert lines == [], (
      f"src/{module_name}.py calls print() on line(s) {', '.join(map(str, lines))}. {what} should return "
      f"{'their results' if ' ' in what else 'its result'}, not print {'them' if ' ' in what else 'it'}. "
      f"(Do your experimenting in scratchpad.py, or inside an `if __name__ == \"__main__\":` block at the end of the file.)")


# ---------------------------------------------------------------------------
# Part 3: tic tac toe boards


def make_empty_board():
  """The correct answer for make_empty_board"""
  return [["", "", ""] for _ in range(3)]


def winning_lines(board):
  """Return the 8 lines (3 rows, 3 columns and 2 diagonals) of board"""
  rows = [list(row) for row in board]
  columns = [[board[r][c] for r in range(3)] for c in range(3)]
  diagonals = [[board[i][i] for i in range(3)], [board[2 - i][i] for i in range(3)]]
  return rows + columns + diagonals


def board_state(board):
  """The correct answer for board_state"""
  for line in winning_lines(board):
    if line[0] != "" and line.count(line[0]) == 3:
      return line[0]
  if all(cell != "" for row in board for cell in row):
    return "Draw"
  return ""


def board_to_str(board):
  """The correct answer for board_to_str"""
  return "\n---+---+---\n".join("|".join(f" {cell or ' '} " for cell in row) for row in board)


def show_board(board):
  """Show a board as a Python list of lists with one row per line, for messages"""
  if not (isinstance(board, list) and len(board) == 3 and all(isinstance(row, list) for row in board)):
    return f"    {board!r}"
  return "    [" + ",\n     ".join(repr(row) for row in board) + "]"


def board_from_string(text):
  """Make a board from a string like 'XO_/_X_/__O' (rows separated by /, _ for an empty cell)"""
  return [["" if cell == "_" else cell for cell in row] for row in text.split("/")]


EMPTY_LINE_HINT = (
    "Three empty cells in a row are not a win! If you check whether the three cells of a line are equal, also check "
    "that they aren't empty (\"\"). Otherwise your function may return \"\" for an empty row before it gets to "
    "check the other rows, columns and diagonals.")
DRAW_TOO_SOON_HINT = ("It's only a draw when there is no winner AND every cell is occupied. While there are still empty "
                      "cells (and no winner) the game isn't over yet, so return \"\".")
WINNER_FIRST_HINT = ("A full board can still have a winner (e.g. when the last move completes a line). Check for a "
                     "winner first, and only return \"Draw\" if there isn't one.")
ROW_COLUMN_HINT = ("The first element of the position is the ROW (which inner list) and the second is the COLUMN "
                   "(which item in that row), so position [r, c] is board[r][c].")


# ---------------------------------------------------------------------------
# Part 4: playing the game


def q3_function(name, reference):  # only used for board_to_str
  """Return the student's function from q3 if it exists (so the game is checked against what the
     student's own functions produce), otherwise the reference version"""
  try:
    import q3
    function = getattr(q3, name)
    if isinstance(function(make_empty_board()), str):
      return function
  except Exception:
    pass
  return reference


def split_separators(module_name):
  """Return the separators that src/<module_name>.py splits strings on (" " for split() with no argument)"""
  separators = set()
  for call in util.find_method_calls(util.parse_source(module_name), "split"):
    if call.args == []:
      separators.add(" ")
    elif isinstance(call.args[0], ast.Constant) and isinstance(call.args[0].value, str):
      separators.add(call.args[0].value)
  return separators


class Move:
  """Something the players type in place of a move: `separate` when the game asks for the row
     and column separately, and `together` (with {sep} for the separator) when it asks for both at once"""

  def __init__(self, separate, together, description):
    self.separate = separate
    self.together = together
    self.description = description


ASKS_ROW = re.compile(r"\brows?\b", re.IGNORECASE)
ASKS_COLUMN = re.compile(r"\bcol(umn)?s?\b", re.IGNORECASE)
ASKS_MOVE = re.compile(r"\b(rows?|col(umn)?s?|moves?|positions?|cells?|spots?|squares?)\b", re.IGNORECASE)
ASKS_AGAIN = re.compile(r"\b(again|another|continue|quit|exit)\b", re.IGNORECASE)


class GamePlayer:
  """A fake input() that plays tic tac toe. Each item of moves is a (row, column) pair or a Move.
     It answers a prompt that asks for a row (or a column) with just that number, and any other
     prompt with the row and column together (e.g. "1 2"), using the separator the game splits on.
     If stop is True, the game is stopped (with util.StopScript) when it asks for input after
     all the moves have been made."""

  def __init__(self, moves, capsys, separator, guessed, stop):
    self.moves = list(moves)
    self.capsys = capsys
    self.separator = separator
    self.guessed = guessed  # True if we don't know the separator the game expects between the row and column
    self.used_separator = False  # True once the row and column have been typed together
    self.stop = stop
    self.transcript = ""
    self.given = set()  # which parts ("row", "column") of the current move have been typed
    self.stopped = False
    self.extra_prompts = 0

  def __call__(self, prompt=""):
    self.transcript += self.capsys.readouterr().out
    lines = [line for line in (self.transcript + str(prompt)).splitlines() if line.strip() != ""]
    context = str(prompt) if str(prompt).strip() else (lines[-1] if lines else "")

    if self.moves == []:
      if self.stop:
        self.stopped = True
        raise util.StopScript()
      self.extra_prompts += 1
      if ASKS_MOVE.search(context) and not ASKS_AGAIN.search(context) or self.extra_prompts > 2:
        self.fail("The game asked for another move after it should have ended.")
      return self.type(prompt, "n")  # e.g. "Play again?"

    move = self.moves[0]
    asks_row, asks_column = bool(ASKS_ROW.search(context)), bool(ASKS_COLUMN.search(context))
    if asks_row != asks_column:  # the game asks for the row and column separately
      part = "row" if asks_row else "column"
      if isinstance(move, Move):
        self.moves.pop(0)
        return self.type(prompt, move.separate)
      self.given.add(part)
      if self.given == {"row", "column"}:
        self.moves.pop(0)
        self.given = set()
      return self.type(prompt, str(move[0] if part == "row" else move[1]))

    self.moves.pop(0)
    self.given = set()
    self.used_separator = True
    if isinstance(move, Move):
      return self.type(prompt, move.together.format(sep=self.separator))
    return self.type(prompt, f"{move[0]}{self.separator}{move[1]}")

  def type(self, prompt, answer):
    """Echo the prompt and answer like a terminal would, and return answer"""
    self.transcript += f"{prompt}{answer}\n"
    return answer

  def fail(self, problem):
    if self.guessed and self.used_separator:
      pytest.skip("These tests could not work out how your game reads the players' moves, so they could not play "
                  "it. That's OK: your instructor will play your game to check it.")
    if self.transcript.strip() == "":
      pytest.fail("When src/q4.py was run, it didn't print anything or ask for any input, so the game could not be "
                  "played. Check that your `if __name__ == \"__main__\":` block calls tictactoe(), and that tictactoe "
                  "displays the board and asks the players for their moves.", pytrace=False)
    pytest.fail(f"{problem}\n{describe_game(self.transcript, self.separator)}", pytrace=False)


HOW_MOVES_ARE_TYPED = (
    "(The tests play your game by answering each prompt that asks for a row or a column with that number (0 to 2), "
    "and any other prompt with the row and column together, separated by {sep!r}.)")


def describe_game(transcript, separator=" "):
  lines = transcript.splitlines()
  shown = lines[-40:]
  return (("Here is the end of the game:\n" if len(lines) > len(shown) else "Here is the game:\n") +
          "".join(f"    {line}\n" for line in shown) + HOW_MOVES_ARE_TYPED.format(sep=separator))


def value_error_hint(error):
  if str(error) == "Position already occupied":
    return ("Before calling place(), check that the position is empty with is_occupied(), and ask the player again if "
            "it isn't.")
  if "int()" in str(error):
    return ("Before converting what the player typed to an int, check that it is a whole number (e.g. with "
            ".isdigit()), and ask the player again if it isn't.")
  return None


GAME_CRASH_HINTS = {
    ValueError: value_error_hint,
    IndexError: ("Check that the player typed a row and a column, and that each is 0, 1 or 2, before using them. "
                 "(If you split what they typed, check how many parts there are first: e.g. an empty answer has none.)"),
}


def play(monkeypatch, capsys, moves, stop=False):
  """Run src/q4.py, with the players typing moves (see GamePlayer). Returns (everything the
     game printed, the GamePlayer)"""
  separators = split_separators("q4")
  separator = " " if separators in [set(), {" "}] else sorted(separators - {" "})[0]
  player = GamePlayer(moves, capsys, separator, guessed=separators == set(), stop=stop)
  described = ", ".join(str(list(m)) if isinstance(m, tuple) else m.description for m in moves)
  output = util.run_script_with_input("q4", monkeypatch, capsys, player, f"when the players' moves were {described}",
                                      hints=GAME_CRASH_HINTS)
  player.transcript += output
  return player.transcript, player


def check_game_result(monkeypatch, capsys, moves, final_board, result_pattern, result_description):
  """Play a whole game and check that it shows the final board and announces the result"""
  transcript, player = play(monkeypatch, capsys, moves)
  if player.moves != []:
    next_move = player.moves[0]
    player.fail(f"The game ended before all the moves were made (the next move was "
                f"{list(next_move) if isinstance(next_move, tuple) else next_move.description}).")
  shown = q3_function("board_to_str", board_to_str)(final_board)
  if shown not in transcript:
    player.fail("At the end of the game, display the final board (using board_to_str). The final board should be:\n" +
                "".join(f"    {line}\n" for line in shown.splitlines()).rstrip())
  ending = transcript[transcript.rindex(shown) + len(shown):]
  if not re.search(result_pattern, ending, re.IGNORECASE):
    player.fail(f"After displaying the final board, the game should announce the result: {result_description}.")
