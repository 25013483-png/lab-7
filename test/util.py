"""General purpose helpers for testing student lab code.

Nothing in this file should be specific to one lab; lab-specific helpers
belong in util_lab_N.py"""

import ast
import contextlib
import copy
import difflib
import importlib
import inspect
import io
import pytest
import runpy
import signal
import tokenize
import traceback
from pathlib import Path

from conftest import InputCalledDuringTest

SRC_DIR = Path(__file__).resolve().parent.parent / "src"

# How long student code may run before it is assumed to be stuck in an infinite loop
TIME_LIMIT_SECONDS = 2


class TookTooLong(BaseException):
  """Raised when student code runs for longer than TIME_LIMIT_SECONDS. (It is a
     BaseException so that an `except Exception:` in student code can't catch it)"""


@contextlib.contextmanager
def time_limit(seconds=TIME_LIMIT_SECONDS):
  """Raise TookTooLong in the code inside this `with` block if it runs for longer than seconds"""
  if not hasattr(signal, "setitimer"):  # e.g. Windows, which has no timer signal
    yield
    return

  def _timeout(signum, frame):
    raise TookTooLong()

  previous_handler = signal.signal(signal.SIGALRM, _timeout)
  signal.setitimer(signal.ITIMER_REAL, seconds)
  try:
    yield
  finally:
    signal.setitimer(signal.ITIMER_REAL, 0)
    signal.signal(signal.SIGALRM, previous_handler)


def describe_too_long(what, exc):
  """Explain that student code (described by what, e.g. 'count(3)') never finished"""
  frame = _src_frame(exc)
  return (
      f"{what} did not finish within {TIME_LIMIT_SECONDS} seconds, so it is probably stuck in an infinite loop." +
      (f"\n  It was running line {frame.lineno} of src/{Path(frame.filename).name}: {frame.line}" if frame else "") +
      "\nHINT: check that every loop eventually stops. For a while loop, make sure the variables in its condition "
      "change each time through the loop (e.g. that you add 1 to the index), so that the condition eventually becomes False.")


# ---------------------------------------------------------------------------
# Loading student code


def read_source(module_name):
  """Return the text of src/<module_name>.py"""
  return (SRC_DIR / f"{module_name}.py").read_text()


def parse_source(module_name):
  """Parse src/<module_name>.py so tests can check how it is written"""
  try:
    return ast.parse(read_source(module_name))
  except SyntaxError as e:
    message = (
        f"Python can't understand the code in src/{module_name}.py, so it could not be checked.\n"
        f"  {type(e).__name__}: {e.msg} (line {e.lineno} of src/{module_name}.py)\n"
        f"Run `python src/{module_name}.py` in the terminal to see more details about the error.")
  pytest.fail(message, pytrace=False)


def _src_frame(exc):
  """Return the last traceback frame of exc that is in the student's src/ folder (or None)"""
  for frame in reversed(traceback.extract_tb(exc.__traceback__)):
    if Path(frame.filename).resolve().parent == SRC_DIR:
      return frame
  return None


def _line_in_src(exc):
  """Describe where in the student's src/ files an exception happened, e.g. 'line 4 of src/q2.py'"""
  frame = _src_frame(exc)
  return f"line {frame.lineno} of src/{Path(frame.filename).name}" if frame else None


def describe_error(exc):
  """Describe an exception raised by student code, including the line of code that raised it"""
  frame = _src_frame(exc)
  if isinstance(exc, AssertionError):
    description = "  AssertionError (an assert statement was False)" + (f": {exc}" if str(exc) else "")
  else:
    description = f"  {type(exc).__name__}: {exc}"
  if frame:
    description += f"\n  at line {frame.lineno} of src/{Path(frame.filename).name}: {frame.line}"
  return description


def import_student_module(module_name, input_advice=None):
  """Import src/<module_name>.py. If the file can't be imported, fail the current
     test with a short explanation (rather than stopping the whole test run).
     input_advice (optional) replaces the advice given if the file calls input() when imported"""
  # pytest.fail is called after the except blocks so that the original error
  # isn't also printed as part of the test output
  try:
    with time_limit():
      return importlib.import_module(module_name)
  except TookTooLong as e:
    message = describe_too_long(f"Importing src/{module_name}.py", e)
  except SyntaxError as e:
    # e.filename may be a different file (e.g. q3.py imports a q2.py with a typo)
    filename = Path(e.filename).name if e.filename else f"{module_name}.py"
    message = (
        f"Python can't understand the code in src/{filename}, so it could not be tested.\n"
        f"  {type(e).__name__}: {e.msg} (line {e.lineno} of src/{filename})\n"
        f"Run `python src/{filename}` in the terminal to see more details about the error.")
  except InputCalledDuringTest as e:
    where = _line_in_src(e)
    message = (
        f"src/{module_name}.py (or a file it imports) calls input() as soon as it is imported" +
        (f" (at {where})" if where else "") + ".\n" +
        (input_advice or "Code that runs when a file is imported should only define functions. To try out your "
         "functions, call them from scratchpad.py instead."))
  except Exception as e:
    message = (
        f"src/{module_name}.py crashed while it was being imported, so it could not be tested.\n" +
        describe_error(e) + "\n"
        f"Run `python src/{module_name}.py` in the terminal to see the full error.")
  pytest.fail(message, pytrace=False)


def get_student_function(module_name, function_name, readme_part):
  """Return the function named function_name from src/<module_name>.py, or fail
     the current test with a helpful message if it doesn't exist"""
  module = import_student_module(module_name)
  function = getattr(module, function_name, None)
  if callable(function):
    return function

  message = f"Define a function named {function_name} in src/{module_name}.py, as described in {readme_part} of the README."
  defined = [name for name, value in vars(module).items() if inspect.isfunction(value)]
  close = difflib.get_close_matches(function_name, defined, n=1)
  if close:
    message += f"\nYou defined a function named {close[0]}. Check the spelling: the name must be exactly {function_name}"
  pytest.fail(message, pytrace=False)


def get_student_variable(module_name, variable_name, readme_part):
  """Return the value of the variable named variable_name in src/<module_name>.py, or fail
     the current test with a helpful message if it doesn't exist"""
  module = import_student_module(module_name)
  if hasattr(module, variable_name):
    return getattr(module, variable_name)

  message = f"Create a variable named {variable_name} in src/{module_name}.py, as described in {readme_part} of the README."
  defined = [name for name in vars(module) if not name.startswith("__")]
  close = difflib.get_close_matches(variable_name, defined, n=1)
  if close:
    message += f"\nYou created a variable named {close[0]}. Check the spelling: the name must be exactly {variable_name}"
  pytest.fail(message, pytrace=False)


# ---------------------------------------------------------------------------
# Calling student code


def describe_call(function, *args):
  """Describe a function call as it would be written in Python, e.g. "area(3, 4)" """
  return f"{function.__name__}({', '.join(repr(a) for a in args)})"


def call(function, *args, hints=None):
  """Call a student's function and return the result. If it crashes, fail the
     current test with a description of the error and the line that caused it.
     hints (optional) maps exception types to extra advice, e.g. {TypeError: "..."}"""
  try:
    with time_limit():
      return function(*args)
  except InputCalledDuringTest:
    raise
  except TookTooLong as e:
    message = describe_too_long(describe_call(function, *args), e)
  except Exception as e:
    message = f"{describe_call(function, *args)} crashed with an error:\n" + describe_error(e)
    for exception_type, hint in (hints or {}).items():
      if isinstance(e, exception_type):
        message += f"\nHINT: {hint}"
        break
  pytest.fail(message, pytrace=False)


def call_without_modifying(function, *args, hints=None, modified_hint=None):
  """Call a student's function (like call) and return the result, but also fail the current
     test if the function changed any of its arguments (e.g. added to or removed from a list
     that was passed to it). modified_hint (optional) is extra advice if it did"""
  call_text = describe_call(function, *args)  # before the call, in case the arguments change
  originals = copy.deepcopy(args)
  result = call(function, *args, hints=hints)
  for position, (before, after) in enumerate(zip(originals, args), start=1):
    if before != after:
      pytest.fail(
          f"{call_text} changed its argument{f' #{position}' if len(args) > 1 else ''}. Before the call it was\n"
          f"    {before!r}\n  and after the call it was\n    {after!r}\n"
          f"A PURE function must not change the values (e.g. lists) passed to it. Build and return a new value "
          f"instead." + (f"\nHINT: {modified_hint}" if modified_hint else ""),
          pytrace=False)
  return result


def check_raises(function, args, exception_type, reason, message=None, hints=None, returned_hint=None):
  """Fail with a helpful message unless calling function(*args) raises exception_type (e.g. ValueError).
     reason says why the error should be raised, e.g. 'the position is already occupied'.
     message (optional) is the exact message the exception must have.
     hints (optional) maps other exception types to extra advice.
     returned_hint (optional) is extra advice if the function returns instead"""
  call_text = describe_call(function, *args)
  name = exception_type.__name__
  try:
    with time_limit():
      result = function(*args)
  except TookTooLong as e:
    failure = describe_too_long(call_text, e)
  except exception_type as e:
    if message is None or str(e) == message:
      return
    failure = (f"{call_text} raised {a_or_an(name)} because {reason}, which is correct, but its message is wrong.\n" +
               compare_strings(message, str(e), "Yours") +
               f"\nHINT: put the message in the parentheses when you raise the error, e.g. raise {name}({message!r})")
  except InputCalledDuringTest:
    raise
  except Exception as e:
    hint = next((hint for exception_type, hint in (hints or {}).items() if isinstance(e, exception_type)), None)
    failure = (f"{call_text} should raise {a_or_an(name)} because {reason}, but it crashed with a different error "
               f"instead:\n" + describe_error(e) + (f"\nHINT: {hint}" if hint else ""))
  else:
    failure = (f"{call_text} should raise {a_or_an(name)} because {reason}, but it returned {result!r} instead." +
               (f"\nHINT: {returned_hint}" if returned_hint else ""))
  pytest.fail(failure, pytrace=False)


def mock_input(monkeypatch, answers, too_many_message=None):
  """Make input() return each of answers in turn, and echo the prompt and answer
     like a terminal would. Returns a list that collects every prompt given to input().
     too_many_message (optional) explains what is wrong if input() is called more
     than len(answers) times."""
  prompts = []

  def _input(prompt=""):
    if len(prompts) >= len(answers):
      pytest.fail(
          too_many_message or
          f"Your code asked for input {len(prompts) + 1} times, but the test only expected it to ask "
          f"{len(answers)} time{'s' if len(answers) != 1 else ''} (the user's answers were {answers}).",
          pytrace=False)
    prompts.append(prompt)
    answer = answers[len(prompts) - 1]
    print(prompt + answer)
    return answer

  monkeypatch.setattr("builtins.input", _input)
  return prompts


class StopScript(BaseException):
  """A fake input() function can raise this to stop a program that is being run by
     run_script_with_input (e.g. once a test has seen all it needs to). It is a
     BaseException so that an `except Exception:` in student code can't catch it"""


def run_script(module_name, monkeypatch, capsys, answers, too_many_message=None):
  """Run src/<module_name>.py as a program (i.e. with __name__ == "__main__"), as
     if the user typed each of answers when asked for input.
     Returns (everything the program printed, list of prompts given to input())"""
  prompts = mock_input(monkeypatch, answers, too_many_message)
  output = run_script_with_input(module_name, monkeypatch, capsys, None, f"when the user entered {', '.join(answers)}")
  return output, prompts


def run_script_with_input(module_name, monkeypatch, capsys, fake_input, description, hints=None):
  """Run src/<module_name>.py as a program (i.e. with __name__ == "__main__"), using
     fake_input (if it isn't None) in place of input(). fake_input may raise StopScript to
     end the program early. description says what the user did, for messages
     (e.g. 'when the user entered 3').
     hints (optional) maps exception types to extra advice if the program crashes (or to a function
     that returns the advice for a particular exception, or None).
     Returns everything the program printed (including anything fake_input printed)"""
  if fake_input is not None:
    monkeypatch.setattr("builtins.input", fake_input)
  # pytest.fail is called after the except blocks so that the original error
  # isn't also printed as part of the test output
  try:
    with time_limit():
      runpy.run_path(str(SRC_DIR / f"{module_name}.py"), run_name="__main__")
    return capsys.readouterr().out
  except StopScript:
    return capsys.readouterr().out
  except TookTooLong as e:
    message = describe_too_long(f"src/{module_name}.py ({description})", e)
  except SyntaxError as e:
    # e.filename may be a different file (e.g. the script imports a file with a typo)
    filename = Path(e.filename).name if e.filename else f"{module_name}.py"
    message = (
        f"Python can't understand the code in src/{filename}, so src/{module_name}.py could not be run.\n"
        f"  {type(e).__name__}: {e.msg} (line {e.lineno} of src/{filename})\n"
        f"Run `python src/{filename}` in the terminal to see more details about the error.")
  except Exception as e:
    message = f"src/{module_name}.py crashed {description}:\n" + describe_error(e) + "\n"
    frame = _src_frame(e)
    if isinstance(e, AssertionError) and frame and Path(frame.filename).name != f"{module_name}.py":
      message += (
          f"HINT: an assert statement in src/{Path(frame.filename).name} failed, which usually means src/{module_name}.py "
          f"passed an invalid value to one of your functions. Check the values you pass to the functions you call "
          f"(and that you call functions with parentheses, e.g. prompt() not prompt).\n")
    for exception_type, hint in (hints or {}).items():
      if isinstance(e, exception_type):
        hint = hint(e) if callable(hint) else hint
        message += f"HINT: {hint}\n" if hint else ""
        break
    message += f"Run `python src/{module_name}.py` to see the full error."
  pytest.fail(message, pytrace=False)


# ---------------------------------------------------------------------------
# Checking results


def check_parameter_count(function, count, description):
  """Fail with a helpful message if function doesn't take exactly count parameters"""
  params = inspect.signature(function).parameters
  if len(params) != count:
    pytest.fail(
        f"{function.__name__} must have exactly {count} parameter{'s' if count != 1 else ''} ({description}), "
        f"but yours has {len(params)}: def {function.__name__}({', '.join(params)}):",
        pytrace=False)


def check_returned(call, actual, expected, explanation=""):
  """Compare the value a student function returned with the expected value.
     call is a description of the call, like 'is_leapyear(1900)'.
     explanation (optional) says why expected is correct."""
  if actual == expected and type(actual) == type(expected):
    return

  why = f"\n{explanation}" if explanation else ""

  if actual is None:
    pytest.fail(none_returned_hint(call) + why, pytrace=False)

  if type(actual) != type(expected):
    pytest.fail(
        f"{call} returned {actual!r} ({a_or_an(type(actual).__name__)}), but it should return "
        f"{expected!r} ({a_or_an(type(expected).__name__)})." +
        (" Note that True and False must not have quotes around them." if isinstance(expected, bool) else "") +
        why,
        pytrace=False)

  if isinstance(expected, str):
    pytest.fail(f"{call} returned the wrong string.{why}\n" + compare_text(expected, actual, "Returned"),
                pytrace=False)

  pytest.fail(f"{call} returned {actual!r}, but it should return {expected!r}.{why}", pytrace=False)


def compare_strings(expected, actual, actual_label="Returned"):
  """Show two one-line strings one above the other, with a ^ under the first
     character that differs (so the difference can be seen without colours)"""
  first_difference = next(
      (i for i, (e, a) in enumerate(zip(repr(expected), repr(actual))) if e != a),
      min(len(repr(expected)), len(repr(actual))))
  label_width = max(len("Expected"), len(actual_label))
  result = (f"  {'Expected':<{label_width}}: {expected!r}\n"
            f"  {actual_label:<{label_width}}: {actual!r}\n"
            f"  {' ' * (label_width + 2)}{' ' * first_difference}^ first difference")
  if actual.lower() == expected.lower():
    result += "\nHINT: the only difference is upper/lower case letters."
  elif actual.strip() == expected.strip():
    result += "\nHINT: the only difference is spaces or newlines (\\n) at the start or end."
  return result


def compare_text(expected, actual, actual_label="Returned"):
  """Compare two strings that may have several lines. Shows both (if they are
     short), then the first line that is different, with a ^ under the first
     character that differs. Newlines are shown as \\n."""
  if "\n" not in expected.rstrip("\n") and "\n" not in actual.rstrip("\n"):
    return compare_strings(expected, actual, actual_label)

  expected_lines = expected.splitlines(keepends=True)
  actual_lines = actual.splitlines(keepends=True)
  result = ""
  if len(expected_lines) <= 12 and len(actual_lines) <= 12:
    result += "  Expected:\n" + "".join(f"    {line!r}\n" for line in expected_lines)
    result += f"  {actual_label}:\n" + "".join(f"    {line!r}\n" for line in actual_lines)
  else:
    result += f"  Expected {len(expected_lines)} lines; {actual_label.lower()} {len(actual_lines)} lines\n"

  for line_number, (e, a) in enumerate(zip(expected_lines, actual_lines), start=1):
    if e != a:
      return result + f"First difference is on line {line_number}:\n" + compare_strings(e, a, actual_label)
  if len(actual_lines) < len(expected_lines):
    return result + (f"Lines {len(actual_lines) + 1} onwards are missing. The first missing line is:\n"
                     f"    {expected_lines[len(actual_lines)]!r}")
  return result + (f"There are extra lines after line {len(expected_lines)}. The first extra line is:\n"
                   f"    {actual_lines[len(expected_lines)]!r}")


def a_or_an(word):
  """Put 'a' or 'an' in front of word, e.g. 'an int', 'a str'"""
  return f"{'an' if word[0] in 'aeiou' else 'a'} {word}"


def none_returned_hint(call):
  return (f"{call} returned None. This usually means your function has no `return` statement for this case, "
          f"or uses print() where it should use return.")


def check_returns_instead_of_printing(capsys, function, *args):
  """Fail with a helpful message if calling function prints something or returns None"""
  call_text = describe_call(function, *args)
  result = call(function, *args)
  printed = capsys.readouterr().out
  if printed != "":
    pytest.fail(
        f"{call_text} printed {printed.strip()!r}. This function must *return* its result instead of printing it. "
        f"(Use print() in scratchpad.py to display what your functions return.)",
        pytrace=False)
  if result is None:
    pytest.fail(none_returned_hint(call_text), pytrace=False)
  return result


def check_raises_assertion_error(function, args, reason, hints=None, returned_hint=None):
  """Fail with a helpful message unless calling function(*args) fails an assert statement.
     reason says why the arguments are invalid, e.g. 'the width is negative'.
     hints (optional) maps other exception types to extra advice.
     returned_hint (optional) is extra advice if the function returns instead"""
  call_text = describe_call(function, *args)
  try:
    with time_limit():
      result = function(*args)
  except TookTooLong as e:
    message = describe_too_long(call_text, e)
  except AssertionError as e:
    # For a recursive function, the assert should fail in the first call, not after several recursive calls
    depth = sum(1 for frame in traceback.extract_tb(e.__traceback__) if frame.name == function.__name__)
    if depth <= 1:
      return
    message = (f"{call_text} should fail an assert statement right away because {reason}. Your function did fail "
               f"an assert, but only after calling itself {depth - 1} more time{'s' if depth > 2 else ''}:\n" +
               describe_error(e) + "\nHINT: check the arguments with assert statements at the start of your function.")
  except InputCalledDuringTest:
    raise
  except Exception as e:
    hint = next((hint for exception_type, hint in (hints or {}).items() if isinstance(e, exception_type)),
                "put an assert statement at the start of your function to check its arguments before using them.")
    message = (f"{call_text} should fail an assert statement because {reason}, "
               f"but it crashed with a different error instead:\n" + describe_error(e) + f"\nHINT: {hint}")
  else:
    message = f"{call_text} should fail an assert statement because {reason}, but it returned {result!r} instead."
    if returned_hint:
      message += f"\nHINT: {returned_hint}"
  pytest.fail(message, pytrace=False)


# ---------------------------------------------------------------------------
# Checking how student code is written


def find_print_calls(module_name):
  """Return the line numbers of all print() calls in src/<module_name>.py. Comments, and
     print() calls inside an `if __name__ == "__main__":` block (which only run when the
     file is run directly, e.g. for debugging), are ignored"""
  tree = parse_source(module_name)
  in_main_guard = set()
  for node in ast.walk(tree):
    if is_main_guard(node):
      for statement in node.body:  # not node.orelse, which runs when the file is imported
        in_main_guard.update(ast.walk(statement))
  return [node.lineno for node in ast.walk(tree) if node not in in_main_guard and is_call_to(node, "print")]


def find_calls(tree, function_name):
  """Return the line numbers of all calls to function_name in tree (a module or
     function parsed with ast). Matches both name(...) and module.name(...)"""
  return [node.lineno for node in ast.walk(tree) if is_call_to(node, function_name)]


def is_call_to(node, function_name):
  """Return True if node (parsed with ast) is a call to function_name, i.e. name(...) or module.name(...)"""
  return isinstance(node, ast.Call) and (
      (isinstance(node.func, ast.Name) and node.func.id == function_name) or
      (isinstance(node.func, ast.Attribute) and node.func.attr == function_name))


def find_assignments(tree, variable_name):
  """Return the values (parsed with ast) assigned to variable_name in tree, e.g. the
     `foods[:]` in `copy = foods[:]`"""
  values = []
  for node in ast.walk(tree):
    if isinstance(node, ast.Assign) and any(isinstance(t, ast.Name) and t.id == variable_name for t in node.targets):
      values.append(node.value)
    elif isinstance(node, (ast.AnnAssign, ast.AugAssign)) and isinstance(node.target, ast.Name) and \
        node.target.id == variable_name and node.value is not None:
      values.append(node.value)
  return values


def find_method_calls(tree, method_name):
  """Return the calls (parsed with ast) to a method named method_name in tree, e.g. foods.append("spam")"""
  return [
      node for node in ast.walk(tree)
      if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == method_name
  ]


def receiver_name(call):
  """Return the name of the variable a method is called on (e.g. 'foods' for foods.append("spam")),
     or None if it isn't called on a variable"""
  return call.func.value.id if isinstance(call.func.value, ast.Name) else None


def find_del_targets(tree):
  """Return everything (parsed with ast) deleted by a del statement in tree, e.g. the `copy[0]` in `del copy[0]`"""
  return [target for node in ast.walk(tree) if isinstance(node, ast.Delete) for target in node.targets]


def is_slice_of(node, variable_name):
  """Return True if node (parsed with ast) is a slice of variable_name, e.g. foods[1:] or foods[:]"""
  return (isinstance(node, ast.Subscript) and isinstance(node.slice, ast.Slice) and isinstance(node.value, ast.Name) and
          node.value.id == variable_name)


def comments_above(module_name, function_name):
  """Return the text of the comment lines directly above the def line of function_name in
     src/<module_name>.py (blank lines between the comments and the def are allowed), or
     None if the function isn't defined"""
  definition = find_function_def(module_name, function_name)
  if definition is None:
    return None
  lines = read_source(module_name).splitlines()
  first_line = min([definition.lineno] + [d.lineno for d in definition.decorator_list])
  index = first_line - 2  # the line above the def, counting from 0
  while index >= 0 and lines[index].strip() == "":
    index -= 1
  comments = []
  while index >= 0 and lines[index].strip().startswith("#"):
    comments.insert(0, lines[index].strip().lstrip("#").strip())
    index -= 1
  return "\n".join(comments)


def find_comment_blocks(module_name):
  """Return the comments in src/<module_name>.py, with one string for each group of comment lines
     that are next to each other (without the #s). Strings on a line of their own (e.g. a
     \"\"\" ... \"\"\" explanation) are included too"""
  tree = parse_source(module_name)  # fails with a helpful message if the file has a syntax error
  blocks, last_line = [], None
  for token in tokenize.generate_tokens(io.StringIO(read_source(module_name)).readline):
    if token.type == tokenize.COMMENT:
      text = token.string.lstrip("#").strip()
      if last_line is not None and token.start[0] == last_line + 1:
        blocks[-1] += "\n" + text
      else:
        blocks.append(text)
      last_line = token.start[0]
  blocks += [
      node.value.value for node in ast.walk(tree)
      if isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)
  ]
  return blocks


def find_function_def(module_name, function_name):
  """Return the ast definition of function_name in src/<module_name>.py, or None"""
  for node in ast.walk(parse_source(module_name)):
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name:
      return node
  return None


def calls_itself(module_name, function_name):
  """Return True if function_name in src/<module_name>.py contains a call to itself (i.e. is recursive)"""
  definition = find_function_def(module_name, function_name)
  return definition is not None and find_calls(definition, function_name) != []


def find_while_loops(tree):
  """Return the line numbers of all while loops in tree (a module or function parsed with ast)"""
  return sorted(node.lineno for node in ast.walk(tree) if isinstance(node, ast.While))


def find_for_loops(tree):
  """Return the line numbers of all for loops in tree (a module or function parsed with ast),
     including the `for` in comprehensions like [c for c in text]"""
  return sorted(
      node.lineno for node in ast.walk(tree) if isinstance(
          node, (ast.For, ast.AsyncFor, ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)))


def imported_modules(module_name):
  """Return the set of module names imported by src/<module_name>.py"""
  tree = parse_source(module_name)
  names = set()
  for node in ast.walk(tree):
    if isinstance(node, ast.Import):
      names.update(alias.name for alias in node.names)
    elif isinstance(node, ast.ImportFrom) and node.module:
      names.add(node.module)
  return names


def defined_function_names(module_name):
  """Return the names of all functions defined in src/<module_name>.py"""
  tree = parse_source(module_name)
  return [node.name for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))]


def is_main_guard(node):
  """Return True if node (parsed with ast) is an `if __name__ == "__main__":` statement"""
  if isinstance(node, ast.If) and isinstance(node.test, ast.Compare) and len(node.test.comparators) == 1:
    sides = [node.test.left, node.test.comparators[0]]
    names = [s.id for s in sides if isinstance(s, ast.Name)]
    strings = [s.value for s in sides if isinstance(s, ast.Constant)]
    return isinstance(node.test.ops[0], ast.Eq) and names == ["__name__"] and strings == ["__main__"]
  return False


def has_main_guard(module_name):
  """Return True if src/<module_name>.py has an `if __name__ == "__main__":` statement"""
  return any(is_main_guard(node) for node in ast.walk(parse_source(module_name)))


def check_has_docstring(module_name, function_name):
  """Fail with a helpful message if function_name in src/<module_name>.py has no docstring"""
  tree = parse_source(module_name)
  definitions = [
      node for node in ast.walk(tree) if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)) and node.name == function_name
  ]
  if definitions == [] or ast.get_docstring(definitions[0]):
    return
  definition = definitions[0]

  message = (
      f"Add a docstring to {function_name} in src/{module_name}.py. A docstring is a string in triple quotes "
      f'(""" ... """) on the first line *inside* the function that describes what the function does.')
  # A common mistake is to put the docstring (or a comment) just above the def line
  body = tree.body
  for i, node in enumerate(body):
    if node is definition and i > 0 and isinstance(body[i - 1], ast.Expr) and isinstance(
        body[i - 1].value, ast.Constant) and isinstance(body[i - 1].value.value, str):
      message += f"\nHINT: it looks like you put a docstring above the `def {function_name}` line. Move it below that line (and indent it)."
  pytest.fail(message, pytrace=False)


# ---------------------------------------------------------------------------
# Older helpers, kept for labs whose tests still use them


def red(s):
  return "\033[0;91m" + s + "\033[39m\033[49m"  #"\033[0m"


def green(s):
  return "\033[0;92m" + s + "\033[39m\033[49m"  #"\033[0m"


def purple(s):
  return "\033[0;95m" + s + "\033[39m\033[49m"  #"\033[0m"


def show_ws(s):
  """Render spaces as a visible middle dot so space differences (e.g. missing
     trailing spaces) are obvious even without color support"""
  return s.replace(' ', '·')


def trimlines(str):
  """Remove empty rows at the end of text so trailing blank lines don't cause
     spurious differences. Line widths are left untouched so real trailing
     space mismatches between truth and test remain visible in diff()"""
  lines = str.split("\n")
  lines.reverse()
  first_non_empty_line_idx = 0
  for line in lines:
    if line.strip() != "":
      break
    first_non_empty_line_idx += 1
  lines = lines[first_non_empty_line_idx:]
  lines.reverse()

  return "\n".join(lines)


def output_is_equivalent(truth, test, trim=False):
  if trim:
    truth = trimlines(truth)
    test = trimlines(test)
  return truth == test


def diff(truth, test):
  truth = trimlines(truth)
  test = trimlines(test)

  test = test.split("\n")
  d = ""
  y = 0
  for line in truth.split("\n"):

    # Truth drawing has more rows than test drawing
    if y >= len(test):
      d += purple(show_ws(line) + "↵")
    else:
      x = 0
      for expected in line:
        # truth line continues beyond end of test line: the remaining
        # expected characters (including this one) were never typed
        if x >= len(test[y]):
          d += purple(show_ws(line[x:])) + red("↵")
          x = len(line)
          break
        else:
          yours = test[y][x]
          if yours == expected:
            d += green(show_ws(expected))
          elif yours != ' ':
            # show what was actually typed; a colored space would be invisible
            d += red(show_ws(yours))
          else:
            d += purple(show_ws(expected))
        x += 1

      # test line continues beyond end of truth line: the extra
      # characters (including the one at x) were unexpected
      if x < len(test[y]):
        d += purple("↵") + red(show_ws(test[y][x:]) + "↵")
      elif x == len(test[y]):
        d += green("↵")

    d += "\n"

    y += 1

  # Test drawing has more rows than truth drawing
  if y < len(test):
    d += red("↵\n".join(show_ws(l) for l in test[y:]) + "↵\n")

  return d


def format_message(msg, expected, yours):
  theDiff = ""
  try:
    theDiff = diff(expected, yours)
  except Exception:
    print(traceback.format_exc())

  return f"{msg}\nExpected: (↵ represents end of line; · represents a space)\n" + show_ws(expected).replace(
      '\n', '↵\n'
  ) + f"\nBut got:\n" + show_ws(yours).replace("\n", "↵\n") + (
      f"\nDifference: ({green('green')}=correct; {purple('purple')}=expected but missing; {red('red')}=unexpected)\n{theDiff}"
      if theDiff else "")


def mock_input_func(answers):
  i = 0

  def _in(p):
    nonlocal i
    try:
      r = answers[i]
      print(p + r)
    except IndexError:
      pytest.fail(
          f"Your code asked for input more than {len(answers)} times, but the test only expected it to ask "
          f"{len(answers)} times (the user's answers were {answers}).",
          pytrace=False)
    i += 1
    return r

  return _in


def expect_assertion_error(f, fname, argnum, argtypestr):
  try:
    f()
  except AssertionError as e:
    return
  except Exception:
    pass
  assert False, f"The {fname} function must raise an AssertionError if the {argnum} argument {argtypestr}"


def assert_assertion_message_equals(f, msg, argnum, argtypestr):
  with pytest.raises(AssertionError) as err:
    f()

  assert msg == str(
      err.value
  ), f"The raised error must have the message '{msg}' when the {argnum} argument {argtypestr}"
