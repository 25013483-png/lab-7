import pytest


class InputCalledDuringTest(Exception):
  pass


@pytest.fixture(autouse=True)
def block_input(monkeypatch):
  """Replace input() so that code which asks for input fails with a clear
     message instead of pytest's confusing 'reading from stdin' error.
     (Tests that need input provide their own input() with util.mock_input)"""

  def _input(prompt=""):
    raise InputCalledDuringTest(
        "Your code called input() during a test that does not provide any input. "
        "Only the functions and programs that the README says should ask the user for input may call input(). "
        "If you added code to try out your functions, move it into scratchpad.py.")

  monkeypatch.setattr("builtins.input", _input)
