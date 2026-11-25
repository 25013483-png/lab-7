import ast
import pytest
import util
import util_lab_7 as lab7


def variable(name):
  """Return the value of the variable named name in src/q1.py"""
  return util.get_student_variable("q1", name, "Part 1")


def code():
  """Return src/q1.py parsed with ast"""
  return util.parse_source("q1")


def assigned(name):
  """Return the last value (parsed with ast) assigned to the variable name in src/q1.py, or None"""
  values = util.find_assignments(code(), name)
  return values[-1] if values else None


def is_index_of(node, variable_name):
  """Return True if node (parsed with ast) is an index of variable_name (not a slice), e.g. foods[1]"""
  return (isinstance(node, ast.Subscript) and not isinstance(node.slice, ast.Slice) and
          isinstance(node.value, ast.Name) and node.value.id == variable_name)


def foods():
  value = variable("foods")
  assert isinstance(value, list), f"foods must be a list, but yours is {value!r} ({util.a_or_an(type(value).__name__)})."
  module = util.import_student_module("q1")
  assert getattr(module, "copy", None) is not value, (
      "copy refers to the same list as foods (it is an alias, not a copy), so removing items from copy in steps 12 "
      "and 13 also removes them from foods! `copy = foods` makes an alias; use a slice to make a copy (step 8).")
  return value


def method_calls(method_name):
  """Return the names of the variables that method_name is called on in src/q1.py"""
  return [util.receiver_name(call) for call in util.find_method_calls(code(), method_name)]


# Steps 1 to 4: create and change the foods list
def test_foods_is_a_list_of_strings():
  items = foods()
  not_strings = [item for item in items if not isinstance(item, str)]
  assert not_strings == [], (
      f"Every item in the foods list should be a food (a string), but foods contains {not_strings[0]!r}. "
      f"Remember to put quotes around each food, e.g. \"pizza\".")


def test_foods_has_at_least_5_foods_plus_2_spams():
  items = foods()
  assert len(items) >= 7, (
      f"foods should start with at least 5 foods (step 1). Steps 3 and 4 then add 2 more items, so it should end up "
      f"with at least 7 items, but yours has {len(items)}: {items!r}")


def test_first_food_is_updated_to_spam():
  items = foods()
  assert items[0] == "spam", f"The first item in foods should be updated to \"spam\" (step 2), but foods is {items!r}"
  updates = [t for node in ast.walk(code()) if isinstance(node, ast.Assign) for t in node.targets
             if is_index_of(t, "foods")]
  assert updates != [], (
      "Step 2 asks you to *update* the first item of foods, using an assignment with an index, "
      "e.g. foods[0] = \"spam\".")


def test_spam_is_appended():
  items = foods()
  assert "foods" in method_calls("append"), "Use the append method to add \"spam\" to the end of foods (step 3), e.g. foods.append(\"spam\")."
  assert items[-1] == "spam", f"The last item in foods should be \"spam\" (step 3), but foods is {items!r}"


def test_spam_is_inserted_as_the_third_item():
  items = foods()
  inserts = [call for call in util.find_method_calls(code(), "insert") if util.receiver_name(call) == "foods"]
  assert inserts != [], "Use the insert method to add \"spam\" as the third item of foods (step 4), e.g. foods.insert(..., \"spam\")."
  message = f"The third item in foods should be \"spam\" (step 4), but foods is {items!r}"
  if items[2] != "spam" and len(items) > 3 and items[3] == "spam":
    message += "\nHINT: you inserted \"spam\" as the fourth item. " + lab7.INDEX_HINT
  assert items[2] == "spam", message


# Steps 5 to 9: indexes, slices and list comprehensions
def test_second():
  items, second = foods(), variable("second")
  hint = f"\nHINT: {lab7.INDEX_HINT}" if second == items[0] or second == items[2] else ""
  assert second == items[1], f"second should be the second item of foods ({items[1]!r}), but it is {second!r}.{hint}"
  assert is_index_of(assigned("second"), "foods"), (
      "Use an index of the foods list to set second (step 5), rather than typing the value yourself.")


def test_second_last():
  items, second_last = foods(), variable("second_last")
  message = f"second_last should be the second-last item of foods ({items[-2]!r}), but it is {second_last!r}."
  if isinstance(second_last, list):
    message += ("\nHINT: second_last should be one item (a string), not a list. Use an index (e.g. foods[...]) rather "
                "than a slice (e.g. foods[...:...]).")
  elif second_last == items[-1]:
    message += "\nHINT: " + lab7.INDEX_HINT
  elif second_last == items[-3]:
    message += ("\nHINT: steps 2 to 4 change foods, so the steps must be done in the order given in the README. "
                "Did you set second_last before \"spam\" was appended to foods (step 3)?")
  assert second_last == items[-2], message
  assert is_index_of(assigned("second_last"), "foods"), (
      "Use an index of the foods list to set second_last (step 6), rather than typing the value yourself. "
      "(Remember that negative indexes count from the end of the list.)")


def test_all_but_first():
  items, all_but_first = foods(), variable("all_but_first")
  message = f"all_but_first should be every item of foods except the first:\n    {items[1:]!r}\nbut it is\n    {all_but_first!r}"
  if all_but_first == items[2:]:
    message += "\nHINT: a slice starts at the index *before* the colon: " + lab7.INDEX_HINT
  assert all_but_first == items[1:], message
  assert util.is_slice_of(assigned("all_but_first"), "foods"), "Use a slice of foods to set all_but_first (step 7), e.g. foods[...:...]"


def test_copy_is_a_copy_made_with_a_slice():
  items, copy = foods(), variable("copy")
  assert isinstance(copy, list), f"copy should be a list, but yours is {copy!r} ({util.a_or_an(type(copy).__name__)})."
  assert copy is not items, (
      "copy must be a *copy* of foods (a new list with the same items), but your copy refers to the same list as "
      "foods (they have the same id). `copy = foods` makes copy an alias of foods; use a slice to make a copy (step 8).")
  assert util.is_slice_of(assigned("copy"), "foods"), (
      "Use a slice of foods to make the copy (step 8). (A slice with no start or end index includes every item.)")


def test_no_spam():
  items, no_spam = foods(), variable("no_spam")
  expected = [item for item in items if item != "spam"]
  message = f"no_spam should be every item of foods except \"spam\":\n    {expected!r}\nbut it is\n    {no_spam!r}"
  if isinstance(no_spam, list) and no_spam != [] and all(isinstance(item, bool) for item in no_spam):
    message += ("\nHINT: your list contains True and False. In a list comprehension, the value to put in the new list "
                "goes first and the condition goes at the end: [item for item in items if <condition>]")
  elif isinstance(no_spam, list) and "spam" in no_spam:
    message += "\nHINT: use a condition (`if ...`) at the end of your list comprehension to leave out \"spam\"."
  assert no_spam == expected, message
  assert isinstance(assigned("no_spam"), ast.ListComp), (
      "Use a list comprehension to set no_spam (step 9), e.g. [... for ... in foods if ...]")


# Steps 10 to 15: aliases, remove and del
def test_foods2_is_an_alias_of_foods():
  items, foods2 = foods(), variable("foods2")
  assert foods2 is items, (
      "foods2 must be an *alias* of foods: another name for the very same list (with the same id). " +
      ("Your foods2 has the same items as foods but is a different list (a copy). " if foods2 == items else "") +
      "To make an alias, assign foods to foods2 (step 10).")


def test_remove_and_del_are_used_on_copy():
  removes, dels = method_calls("remove"), [t for t in util.find_del_targets(code()) if isinstance(t, ast.Subscript)]
  assert "foods" not in removes and not any(is_index_of(t, "foods") for t in dels), (
      "Steps 12 and 13 ask you to remove items from copy, not from foods. (Step 15 only asks you to *explain* what "
      "would happen if you removed them from foods.)")
  assert "copy" in removes, "Use the remove method to remove the first \"spam\" from copy (step 12), e.g. copy.remove(...)"
  assert any(is_index_of(t, "copy") for t in dels), "Use a del statement to remove the first item from copy (step 13), e.g. del copy[...]"


def test_copy_after_remove_and_del():
  items, copy = foods(), variable("copy")
  expected = items[2:]
  message = (f"After removing the first \"spam\" (step 12) and then the first item (step 13), copy should be\n"
             f"    {expected!r}\nbut it is\n    {copy!r}")
  swapped = items[1:]
  swapped.remove("spam")
  if copy == swapped:
    message += "\nHINT: did you do step 13 (del) before step 12 (remove)? Do them in the order given in the README."
  elif copy == items[1:]:
    message += "\nHINT: it looks like only one item was removed from copy. Check that you did both steps 12 and 13."
  assert copy == expected, message


def test_ids_are_explained():
  lab7.check_explanation(
      "q1", lambda words: words & {"id", "ids", "identity"},
      "Step 11 asks you to look at the ids of foods, foods2, copy and no_spam (e.g. with the id function) and to "
      "explain, in a comment in src/q1.py, which of them refer to the same list and why. Mention the ids in your "
      "explanation.")


def test_remove_and_del_are_explained():
  lab7.check_explanation(
      "q1", lambda words: "remove" in words and "del" in words,
      "Step 14 asks you to explain, in a comment in src/q1.py, the difference between the remove method and a del "
      "statement. Mention both remove and del in your explanation.")


def test_foods2_is_explained():
  lab7.check_explanation(
      "q1", lambda words: "foods2" in words and words & {
          "remove", "removed", "removing", "del", "delete", "deleted", "deleting", "change", "changes", "changed",
          "affect", "affects", "affected"},
      "Step 15 asks you to explain, in a comment in src/q1.py, what would happen to foods2 if you did the remove and "
      "del operations on foods instead of copy. Mention foods2 in your explanation.")


# Step 16: print each item with its index
def test_items_are_printed_with_their_indexes(monkeypatch, capsys):
  items = foods()
  assert util.find_for_loops(code()) != [], "Use a for loop to print each item of foods with its index (step 16)."
  output, _ = util.run_script("q1", monkeypatch, capsys, [])
  lines = output.splitlines()
  for index, item in enumerate(items):
    if not any(str(index) in line and item in line for line in lines):
      pytest.fail(
          f"Step 16 asks you to print each item of foods along with its index, but q1.py didn't print a line with "
          f"both the index {index} and the item {item!r} at that index. It printed:\n" +
          "".join(f"    {line}\n" for line in lines[-12:]) +
          "HINT: loop over the indexes with `for index in range(len(foods)):` and print both index and foods[index].",
          pytrace=False)


# Steps 17 to 19: split and lists of lists
def test_row_is_made_with_split():
  row = variable("row")
  message = f"row should be ['X', 'O', 'X'], but it is {row!r}."
  if row == ["X|O|X"]:
    message += "\nHINT: pass the character to split on to the split method, e.g. text.split(\"|\")"
  assert row == ["X", "O", "X"], message
  assert method_calls("split") != [], "Use the split method to make row (step 17)."


def test_tictactoe_board_is_3_by_3():
  board = variable("tictactoe_board")
  message = f"tictactoe_board should be a list of 3 lists (the rows), each containing 3 strings, but it is\n{lab7.show_board(board)}"
  assert isinstance(board, list) and len(board) == 3, message
  if any(isinstance(row, str) for row in board):
    message += "\nHINT: each row must be a list of 3 strings (e.g. [\"X\", \"O\", \"\"]), not one string."
  assert all(isinstance(row, list) and len(row) == 3 for row in board), message
  cells = [cell for row in board for cell in row]
  bad = [cell for cell in cells if cell not in ["X", "O", ""]]
  hint = ("\nHINT: an empty cell is the empty string \"\" (quotes with nothing between them), not a space or None."
          if any(cell in [" ", None] for cell in bad) else "")
  assert bad == [], f"Each cell of tictactoe_board must be \"X\", \"O\" or \"\", but your board contains {bad[0]!r}.{hint}"


def test_middle_cell():
  board, middle_cell = variable("tictactoe_board"), variable("middle_cell")
  value = assigned("middle_cell")
  assert isinstance(value, ast.Subscript) and is_index_of(value.value, "tictactoe_board"), (
      "Use indexing to set middle_cell to the middle cell of tictactoe_board (step 19). You need two indexes: one "
      "to choose the row, then one to choose the cell in that row, e.g. tictactoe_board[...][...]")
  indexes = [value.value.slice, value.slice]
  if all(isinstance(i, ast.Constant) for i in indexes):
    assert all(i.value in [1, -2] for i in indexes), (
        f"middle_cell should be the cell in the middle of the board (the middle row, middle column), but you used "
        f"tictactoe_board[{indexes[0].value}][{indexes[1].value}].\nHINT: {lab7.INDEX_HINT}")
  assert middle_cell == board[1][1], f"middle_cell should be {board[1][1]!r}, but it is {middle_cell!r}."
