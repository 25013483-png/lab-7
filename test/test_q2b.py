import math
import util
import util_lab_7 as lab7

SQUARED_HINT = "Your function squared the numbers. Use math.sqrt(...) (or ** 0.5) to get the square root."


def list_roots():
  """Return the list_roots function defined in src/q2.py"""
  return util.get_student_function("q2", "list_roots", "Part 2b")


def check(numbers, explanation):
  expected = [math.sqrt(number) for number in numbers]
  mistakes = [([number**2 for number in numbers], SQUARED_HINT)]
  if len(numbers) > 1:
    mistakes += [(expected[:1], lab7.RETURN_IN_LOOP_HINT), (expected[1:], lab7.SKIPPED_ITEM_HINT),
                 (expected[:-1], lab7.SKIPPED_ITEM_HINT)]
  lab7.check_new_list(list_roots(), numbers, expected, explanation, mistakes,
                      modified_hint="Don't put the square roots into the list you were given; append them to a new list.")


def test_list_roots_is_defined():
  list_roots()


def test_list_roots_takes_one_parameter():
  util.check_parameter_count(list_roots(), 1, "the list of numbers")


def test_list_roots_has_a_docstring():
  list_roots()
  util.check_has_docstring("q2", "list_roots")


def test_list_roots_returns_instead_of_printing(capsys):
  util.check_returns_instead_of_printing(capsys, list_roots(), [4, 9])


def test_list_roots_of_perfect_squares():
  check([4, 9, 16], "The square roots of 4, 9 and 16 are 2.0, 3.0 and 4.0.")
  check([49], "The square root of 49 is 7.0.")


def test_list_roots_of_other_numbers():
  check([1, 2.25, 0.25], "The square roots of 1, 2.25 and 0.25 are 1.0, 1.5 and 0.5.")
  check([2, 10], "The square roots of 2 and 10 are about 1.414 and 3.162.")


def test_list_roots_of_zero():
  check([0], "The square root of 0 is 0.0.")


def test_list_roots_of_empty_list():
  check([], "An empty list has no numbers, so the list of their square roots is empty too.")


def test_list_roots_uses_a_loop():
  lab7.check_uses_loop("q2", "list_roots", "Part 2b")


def test_list_roots_has_a_traversal_pattern_comment():
  lab7.check_pattern_comment("q2", "list_roots", "map", "Part 2b")
