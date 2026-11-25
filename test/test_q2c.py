import ast
import util
import util_lab_7 as lab7

INVERTED_HINT = "Your function kept the strings that are NOT numeric. Check the condition you use to choose the strings."
INTS_HINT = "Return the numeric strings themselves (e.g. \"123\"), not numbers made from them (e.g. 123)."
PARENTHESES_HINT = ("Your function kept every string. Remember to *call* the isnumeric method, with parentheses: "
                    "text.isnumeric(). Without them, `if text.isnumeric:` is always true.")
NOT_DIGITS_HINT = ("isnumeric() is only True when every character in the string is a digit, so strings with a "
                   "decimal point, a minus sign or a space (and the empty string) are not numeric.")


def only_numeric():
  """Return the only_numeric function defined in src/q2.py"""
  return util.get_student_function("q2", "only_numeric", "Part 2c")


def check(strings, expected, explanation, hint=None):
  mistakes = [([s for s in strings if not s.isnumeric()], INVERTED_HINT),
              ([int(s) for s in expected], INTS_HINT), (strings, PARENTHESES_HINT)]
  if len(expected) > 1:
    mistakes += [(expected[:1], lab7.RETURN_IN_LOOP_HINT), (expected[1:], lab7.SKIPPED_ITEM_HINT),
                 (expected[:-1], lab7.SKIPPED_ITEM_HINT)]
  lab7.check_new_list(only_numeric(), strings, expected, explanation,
                      [(wrong, h) for wrong, h in mistakes if wrong != expected], hint,
                      modified_hint=lab7.REMOVE_WHILE_LOOPING_HINT)


def test_only_numeric_is_defined():
  only_numeric()


def test_only_numeric_takes_one_parameter():
  util.check_parameter_count(only_numeric(), 1, "the list of strings")


def test_only_numeric_has_a_docstring():
  only_numeric()
  util.check_has_docstring("q2", "only_numeric")


def test_only_numeric_returns_instead_of_printing(capsys):
  util.check_returns_instead_of_printing(capsys, only_numeric(), ["1", "a"])


def test_only_numeric_keeps_numeric_strings():
  check(["123", "abc", "456", "0"], ["123", "456", "0"], "Only \"123\", \"456\" and \"0\" are numeric.")
  check(["one", "two", "3", "4five"], ["3"], "Only \"3\" is numeric (\"4five\" has letters in it).")


def test_only_numeric_keeps_the_order_and_duplicates():
  check(["9", "x", "1", "9"], ["9", "1", "9"], "The numeric strings must stay in the same order, and a string that "
        "appears twice must be kept twice.")


def test_only_numeric_with_strings_next_to_each_other_to_remove():
  check(["a", "b", "1", "c", "d", "2"], ["1", "2"], "Only \"1\" and \"2\" are numeric.")


def test_decimals_negatives_and_spaces_are_not_numeric():
  check(["78.9", "-5", " 7", ""], [], "None of these strings are numeric.", NOT_DIGITS_HINT)


def test_only_numeric_when_every_string_is_numeric():
  check(["123", "456"], ["123", "456"], "Every string is numeric, so they are all kept (in a new list).")


def test_only_numeric_of_empty_list():
  check([], [], "An empty list has no numeric strings, so the result is an empty list.")


def test_only_numeric_uses_isnumeric():
  definition = util.find_function_def("q2", "only_numeric")
  assert definition is not None, "Define a function named only_numeric in src/q2.py, as described in Part 2c of the README."
  uses = [node for node in ast.walk(definition) if isinstance(node, ast.Attribute) and node.attr == "isnumeric"]
  assert uses != [], (
      "only_numeric should use the isnumeric method to check each string, as described in Part 2c of the README.")


def test_only_numeric_uses_a_loop():
  lab7.check_uses_loop("q2", "only_numeric", "Part 2c")


def test_only_numeric_has_a_traversal_pattern_comment():
  lab7.check_pattern_comment("q2", "only_numeric", "filter", "Part 2c")
