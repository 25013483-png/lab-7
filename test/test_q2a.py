import pytest
import util
import util_lab_7 as lab7

SUM_HINT = "Your function added the numbers together. It should multiply them (use * rather than +)."
START_AT_ZERO_HINT = ("Anything multiplied by 0 is 0, so if you start your product at 0 it stays 0. Start it at 1 "
                      "instead (multiplying by 1 doesn't change a number).")
FLOAT_START_HINT = "Start your product at the int 1, not the float 1.0, so that a list of ints gives an int."
MODIFIED_HINT = "Don't remove items from the list (e.g. with pop()) to go through it. Loop over it instead."


def list_product():
  """Return the list_product function defined in src/q2.py"""
  return util.get_student_function("q2", "list_product", "Part 2a")


def product(numbers):
  result = 1
  for number in numbers:
    result *= number
  return result


def check(numbers, expected, explanation):
  call_text = util.describe_call(list_product(), numbers)
  actual = util.call_without_modifying(list_product(), numbers, modified_hint=MODIFIED_HINT)
  mistakes = []
  if len(numbers) > 1:
    mistakes += [(numbers[0], lab7.RETURN_IN_LOOP_HINT), (sum(numbers), SUM_HINT),
                 (product(numbers[1:]), lab7.SKIPPED_ITEM_HINT), (product(numbers[:-1]), lab7.SKIPPED_ITEM_HINT)]
  if numbers != [] and 0 not in numbers:
    mistakes.append((0, START_AT_ZERO_HINT))
  if isinstance(actual, float) and isinstance(expected, int) and actual == expected:
    hint = FLOAT_START_HINT
  else:
    hint = next((h for wrong, h in mistakes if actual == wrong and wrong != expected), None)
  util.check_returned(call_text, actual, expected, explanation + (f"\nHINT: {hint}" if hint else ""))


def test_list_product_is_defined():
  list_product()


def test_list_product_takes_one_parameter():
  util.check_parameter_count(list_product(), 1, "the list of numbers")


def test_list_product_has_a_docstring():
  list_product()
  util.check_has_docstring("q2", "list_product")


def test_list_product_returns_instead_of_printing(capsys):
  util.check_returns_instead_of_printing(capsys, list_product(), [2, 3])


def test_list_product_of_several_numbers():
  check([1, 2, 3, 4], 24, "1 * 2 * 3 * 4 is 24.")
  check([5, 6, 7], 210, "5 * 6 * 7 is 210.")
  check([2, 5], 10, "2 * 5 is 10.")


def test_list_product_of_floats():
  check([3.0, 4.0], 12.0, "3.0 * 4.0 is 12.0.")
  check([10, 0.5, 2, -0.5], -5.0, "10 * 0.5 * 2 * -0.5 is -5.0.")


def test_list_product_of_negative_numbers():
  check([-2, 3], -6, "-2 * 3 is -6.")
  check([-2, -3, -1], -6, "-2 * -3 * -1 is -6.")


def test_list_product_with_a_zero():
  check([5, 0, 7], 0, "Anything multiplied by 0 is 0.")


def test_list_product_of_one_number():
  check([10], 10, "The product of a list with one number is that number.")
  check([-4], -4, "The product of a list with one number is that number.")


def test_list_product_of_empty_list():
  check([], 1, "The product of an empty list is 1 (see Part 2a of the README). 1 is to multiplying what 0 is to "
        "adding: multiplying by 1 changes nothing, so it is the right starting value for a product.")


def test_list_product_uses_a_loop():
  lab7.check_uses_loop("q2", "list_product", "Part 2a")


def test_list_product_has_a_traversal_pattern_comment():
  lab7.check_pattern_comment("q2", "list_product", "reduce", "Part 2a")


def test_q2_has_no_print_calls():
  lab7.check_no_print_calls("q2", "list_product, list_roots and only_numeric")
