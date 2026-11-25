# Lab 7 - Lists

## Setup

1. Click the "**Use this template**" button near the top of this repository on GitHub
2. Set the following properties on the GitHub repository, then click "Create repository":
    - **Owner**: your GitHub username (NOT the course organization)
    - **Name**: csd110-26f-lab-7
    - **Visibility**: Private
3. In your new repository, go to Settings -> Collaborators, and add your instructor as a collaborator.
4. Create a branch named `lab-7` on which to do your lab work
5. Create a Codespace on that branch, and open it (give it a few minutes to initialize)
6. In your Codespace terminal, verify your setup using `gh lab setup-check`

### Required Reading 

It is assumed that you have watched all lecture videos and completed readings and practice exercises up to the end of Chapter 10 (not including Chapter 4) in the course textbook.  If you have not done so yet, you should! 

### Reflections

As you are working on your lab, help yourself remember important things by taking notes in `reflections.md`. Record notes about anything you think important to remember, any problems you encountered and how you resolved them, and any remaining questions you may still have.

> **NOTE**: `reflections.md` is a 'markdown' file.  Markdown is a markup language that has simple syntax for adding formatting to plain text documents. See [this documentation on GitHub](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) to learn how to format text in a markdown file.

### AI Use

> **IMPORTANT**: ***Failure to include an accurate AI Use Statement as described below may result in a lab grade deduction of up to 100% depending on your instructor's evaluation of how well you understand the code you submit***

You MAY use AI as a LEARNING AID to help you understand topics you are needing extra help with.
You may NOT use AI to do your work for you or to avoid having to think and learn on your own.

#### AI Use Statement

**Whether or not you use AI**, you MUST include an AI Use Statement in your `reflections.md` document that indicates clearly:

- Which specific AI tools you used in the completion of this lab (or an explicit statement that you did not use any AI tools).
- Links to or copies of **ALL** AI chats you had related to this assignment. 

> **IMPORTANT:** if sharing a link, do NOT simply copy the URL from your browser; you MUST click the **Share** button and create a public link.

Examples:
- I used ChatGPT to help me better understand the lab requirements.  Below are links to my ChatGPT chats.
- I used Claude to give me examples of statements vs expressions in Python.  Below are links to my conversation.
- I did not use any AI tools to complete this lab.

### Running your code

#### From the terminal

1. Open the terminal (View -> Terminal)
2. Enter a command like the following `python path/to/script.py`.  For example, to run the `q1.py` script in the `src` folder, run `python src/q1.py`.

#### Using the debugger

1. Open the Python file you want to run
2. Open the 'Run and Debug' panel (right side, right-arrow icon with bug in lower left corner). 
3. Make sure the "Python Debugger: Current File" configuration is selected in the dropdown at the top of the panel.
4. Click the green arrow button to run the currently opened Python file

### Testing your code

A set of tests have been prepared for this lab that will help you determine if your code is correct or not.

#### Running tests 

| Task | Command | Example |
|------|---------|---------|
| Run all tests | `pytest` | `pytest` |
| Stop at the first failing test while working | `pytest -x` | `pytest -x` |
| Run one test file | `pytest <path_to_file>` | `pytest test/test_q1.py` |
| Run one test function | `pytest <path_to_file>::<function_name>` | `pytest test/test_q2a.py::test_list_product_of_several_numbers` | 

While working, use `pytest -x` to focus on one failure at a time. Fix that issue and run the same command again to continue through the tests. Once the tests are passing this way, run `pytest` to check the entire lab.

#### Reading test output

The output of the tests will give you an indication of which tests passed or failed. For any failed tests, you will also see messages that should help you determine why the test failed.

Here are some tips for dealing with failing tests:

1. The name of the test itself usually gives a clue as to what the test is checking (e.g. `test_list_product_of_several_numbers`).
2. Read the message under the test name. It usually says which function call was tested, what your function returned, what it should have returned, and why.
3. When a string is wrong, the message shows the "Expected" and "Returned" values one above the other, with a `^` under the first character that is different.
4. If a line starting with `src/` appears in the output, it shows the line in **your** code where the problem happened.
5. If a test says your code "did not finish", it is probably stuck in an infinite loop: check that the condition of each `while` loop eventually becomes `False`.
6. The tests for each part are in order, starting with the simplest. Fix the first failing test before worrying about later ones. Often fixing one test fixes other failing tests as well.
7. When working on a failing test, run just that test (see above) so you can focus on its output without having to wade through the output of all the other tests.

#### Passing tests does not guarantee correctness

If all the tests passed, you can be reasonably sure that your code is correct, **BUT PASSING ALL TESTS DOES NOT NECESSARILY MEAN YOU WILL GET 100%** because some grades are assigned to non-coding tasks, and it is sometimes possible to create incorrect programs that do pass the tests.

## Instructions

### Overview

In this lab you will practice using lists in Python programs.  You will start with some simple list operations and list-based functions.  You will then work toward building a working tic tac toe game.

> **IMPORTANT**: You are expected to use meaningful names for all functions and variables, and you must document all functions with appropriate docstrings as discussed in class.  Failing to do so may result in a lower grade.

### Part 1 - List basics

In this part you will write some simple code involving lists. Place your answers in `q1.py`.

1. Create a variable named `foods` that contains a list of at least 5 different food items (strings)
2. Update the first item in the `foods` list to be "spam"
3. Use the `append` method to add "spam" to the end of the `foods` list
4. Use the `insert` method to add "spam" as the **third** element in the `foods` list
5. In a variable named `second`, store the second item from the `foods` list
6. In a variable named `second_last`, store the second-last item from the `foods` list
7. In a variable named `all_but_first`, **use a slice** to store all but the first item from the `foods` list
8. In a variable named `copy`, **use a slice** to store a copy of the entire `foods` list
9. In a variable named `no_spam`, use a **list comprehension** to create a new list that contains all the items from the `foods` list except `"spam"`
10. Create a variable named `foods2` that is an **alias** of the `foods` variable
11. Use the `id` function (e.g., in the Debug Console while paused in your debugger) to look at the ids of the `foods`, `foods2`, `copy`, and `no_spam` lists. In a comment, explain which of them refer to the same list and why
12. Using the `remove` method, remove the first instance of `"spam"` from the `copy` list
13. Using a `del` statement, remove the first item from the `copy` list
14. In a comment, explain the difference between the `remove` method and a `del` statement
15. In a comment, explain what would happen to `foods2` if you did the above `remove` and `del` operations on the `foods` list instead of the `copy` list
16. Using a `for` loop, print each item in the `foods` list along with its index (i.e., print both the index and the item for each item in the list). **HINT**: Use `range(len(yourvariablehere))` or the [`enumerate`](https://book.pythontips.com/en/latest/enumerate.html#enumerate) function to loop over the indexes of a sequence instead of the values in the sequence.
17. Use the string `split` method to create a list named `row` from the string `"X|O|X"`. (I.e., split the string `"X|O|X"` on the pipe character `|`.)
18. Create a variable named `tictactoe_board` that contains a 3x3 list of lists representing a tic tac toe board. (I.e., the main list contains three lists, each representing one row of the board; each row list contains three string elements, either `"X"`, `"O"`, or an empty string `""`.)
19. Finally, in a variable named `middle_cell`, use indexing to store the value in the middle cell of the `tictactoe_board`


### Part 2 - List traversals

In this part you will make functions that traverse lists using each of the three common loop traversal patterns: map, filter, and reduce.

> **IMPORTANT:** Use appropriate variable names, docstrings, and code comments

In `q2.py`...

#### Part 2a - Calculate the product of a list of numbers
1. Create a **PURE** function named `list_product` which takes a list of numbers and returns the product of all the numbers in the list. **NOTE**: In order for a function that accepts a list to remain pure, it must not modify the list in any way.
2. The function has 1 parameter which is assumed to be a list of numbers (you may state this as a precondition in your docstring).
3. The function returns the product of the numbers in the list. If the list is empty, the function returns `1`
4. In a comment above the function header, identify which traversal pattern is being employed in this function (map, filter, or reduce)

> **Examples:**
> ```python
> list_product([1, 2, 3, 4])         # returns 24
> list_product([3.0, 4.0])           # returns 12.0
> list_product([10, 0.5, 2, -0.2])   # returns -2.0
> list_product([10])                 # returns 10
> list_product([])                   # returns 1
> ```

#### Part 2b - Calculate the roots of a list of numbers
1. Create a **PURE** function named `list_roots` which takes a list of numbers and returns a new list containing the square roots of each number in the input list
2. The function has 1 parameter which is assumed to be a list of **non-negative** numbers (i.e., 0 or greater) (you may state this as a precondition in your docstring).
3. The function returns a new list containing the square roots of each number in the input list 
4. In a comment above the function header, identify which traversal pattern is being employed in this function (map, filter, or reduce)
5. **CHALLENGE:** (not graded) In a comment show a one-line implementation of the function using a list comprehension
6. **CHALLENGE:** (not graded) Python has some [built-in higher-order functions](https://book.pythontips.com/en/latest/map_filter.html) that implement the common traversal patterns. In another comment, show a one-line implementation of this function using the appropriate built-in function. HINT: youwill need to use the `list` function to convert the result of the built-in function into a list.

> **Examples:**
> ```python
> list_roots([4, 9, 16])         # returns [2.0, 3.0, 4.0]
> list_roots([1, 2.25, 0.25])    # returns [1.0, 1.5, 0.5]
> list_roots([0])                # returns [0.0]
> list_roots([])                 # returns []
> ```

#### Part 2c - Remove non-numeric strings
1. Create a **PURE** function named `only_numeric` which takes a list of strings and returns a new list containing only those strings that are numeric
2. The function has 1 parameter which is assumed to be a list of strings (you may state this as a precondition in your docstring).
3. The function returns a new list containing only those strings from the input list that are numeric (i.e., strings for which the `isnumeric` method returns `True`)
4. In a comment above the function header, identify which traversal pattern is being employed in this function (map, filter, or reduce)
5. **CHALLENGE:** (not graded) In a comment show a one-line implementation of the function using a list comprehension
6. **CHALLENGE:** (not graded) Python has some built-in higher-order functions that implement the common traversal patterns. In another comment, show a one-line implementation of this function using the appropriate built-in function.

> **Examples:**
> ```python
> only_numeric(["123", "abc", "456", "0"])       # returns ["123", "456", "0"]
> only_numeric(["one", "two", "3", "4five"])     # returns ["3"]
> only_numeric(["78.9", "-5", " 7", ""])         # returns [] ("." "-" and " " are not numeric characters)
> only_numeric([])                               # returns []
> ```

### Part 3 - Tic Tac Toe utilities

In Part 4 you will build a tic tac toe game. In this part, you will implement some functions that will help you build that game.

In Part 1 you created a data structure for representing tic tac toe boards. Namely, a 3x3 list of lists containing either "X", "O", or the empty string.  In this part you will create some functions that operate on such list representations of tic tac toe boards.

> **IMPORTANT:** Use appropriate variable names, docstrings, and code comments

#### Part 3a - Create an empty board
1. Create a **PURE** function named `make_empty_board` which takes no parameters and returns a new empty tic tac toe board (i.e., a 3x3 list of lists containing 3 rows of 3 empty strings each)
2. In a comment, explain why `[[""] * 3] * 3` would NOT work as an empty board. Try it in a REPL:
   ```python
   >>> board = [[""] * 3] * 3   # Make the board
   >>> board                    # View the board to see that it looks correct
   >>> board[0][0] = "X"        # Try setting the top left cell to "X"
   >>> board                    # What happened? Why?
   ```

#### Part 3b - Checking if a position is already occupied

1. Create a **PURE** function named `is_occupied` which takes a tic tac toe board and a position (row and column). It returns `True` if the position is already occupied (i.e., contains `"X"` or `"O"`) and `False` otherwise.
2. The function has 2 parameters:
   1. A 3x3 list of lists representing a tic tac toe board as described above (you may state this as a precondition in your docstring.)
   2. A 2-element list of integers representing the row and column of the position, respectively. (I.e., the first element is the row index and the second element is the column index. Both indices are 0-based, so they must be either 0, 1, or 2.)
3. The function returns `True` if the given position is already occupied (i.e., contains `"X"` or `"O"`) and `False` otherwise
4. Use assertion statement(s) in your function to verify the following about the position parameter:
   1. It is a list
   2. It contains exactly 2 elements
   3. Both the row and column indices are either 0, 1, or 2

> **Examples:**
> ```python
> board = [["X", "O", ""],
>          ["", "X", "O"],
>          ["O", "", "X"]]
> is_occupied(board, [0, 0])   # returns True
> is_occupied(board, [0, 2])   # returns False
> is_occupied(board, [2, 1])   # returns False
> is_occupied(board, [1, 2])   # returns True
> is_occupied(board, "11")    # AssertionError (the position is not a list)
> is_occupied(board, [0])      # AssertionError (the position does not have exactly 2 elements)
> is_occupied(board, [3, 0])   # AssertionError (row index 3 is out of range)
> ```

#### Part 3c - Placing a symbol on the board
1. Create a function named `place` which takes a tic tac toe board, a position (row and column), and a symbol ("X" or "O") and places that symbol at the specified position on the board
2. The function has 3 parameters:
   1. A 3x3 list of lists representing a tic tac toe board as described above (you may state this as a precondition in your docstring.)
   2. A position (a 2-element list of row and column indices), as described in Part 3b
   3. A string representing the symbol to place at the specified position
3. Use an assertion statement in your function to verify that the symbol parameter is either "X" or "O"
4. The function must raise a ValueError with the message "Position already occupied" if the given position is already occupied. (Yes, you should use the `is_occupied` function you created above to help you with this.)
5. The function does NOT return any value; it simply places the symbol at the specified position on the board.
6. In a comment above the function header, explain why this function can NOT be considered a pure function.

> **NOTE:** You may wonder why you should bother with the ValueError check here given that you have the `is_occupied` function. Of course, you can (and should) always check that the given position is not already occupied before trying to set it; writing your code otherwise would be a semantic error. The reason to have this check here is that if you make the mistake of forgetting to check before calling `place`, this function will raise a helpful error rather than silently overwriting an existing value on the board and allowing the game to proceed in a corrupted state.

#### Part 3d - Check the board state

1. Create a **PURE** function named `board_state` which takes a tic tac toe board and returns the winner of the game if there is one, "Draw" if the game is a draw, or the empty string if there is no winner yet.
2. The function has 1 parameter which is assumed to be a 3x3 list of lists representing a tic tac toe board (you may state this as a precondition in your docstring).
3. The function returns:
   1. "X" if player X has won
   2. "O" if player O has won
   3. "Draw" if the game is a draw (i.e., all positions are occupied and there is no winner)
   4. The empty string `""` if there is no winner yet and there are still unoccupied positions on the board

> **Examples:**
> ```python
> board_state([["X", "O", ""],
>              ["", "X", ""],
>              ["", "", "O"]])     # returns "" (no winner yet, and there are still empty cells)
> 
> board_state([["O", "X", ""],
>              ["O", "X", ""],
>              ["", "X", "O"]])    # returns "X" (X has the middle column)
> 
> board_state([["X", "", "O"],
>              ["X", "O", ""],
>              ["O", "", "X"]])    # returns "O" (O has the diagonal from bottom-left to top-right)
> 
> board_state([["X", "O", "X"],
>              ["X", "O", "O"],
>              ["O", "X", "X"]])   # returns "Draw" (the board is full and nobody won)
> 
> board_state([["X", "X", "X"],
>              ["O", "O", "X"],
>              ["O", "X", "O"]])   # returns "X" (a full board with a winner is NOT a draw)
> ```

#### Part 3e - Converting a board list to a string

In this part you will create a function that converts a tic tac toe board list into a readable string format. Specifically, your function should return a string that looks like this:

```
   | O | X 
---+---+---
   | X | O 
---+---+---
 X |   | O 
```

> **IMPORTANT:** Note the spaces in the output above.  Each cell is 3 characters wide (the X/O or an empty space surrounded by one space on either side), so every row ends with a space. Rows are separated by newline characters (`\n`), and there is NO newline at the end of the string.

1. Create a **PURE** function named `board_to_str` which takes a 3x3 tic tac toe board (a list of lists) and returns a string representing the board in the format shown above
2. The function has 1 parameter which is assumed to be a 3x3 list of lists representing a tic tac toe board (you may state this as a precondition in your docstring).
3. The function returns a string representing the board in the format shown above

### Part 4 - Tic Tac Toe game

In this part you will create a working tic tac toe game that two players can play against each other from the terminal. You will use the functions you created in Part 3 to help you build this game.

Here is a basic outline of how the game should work:
- Start with an empty board; player X goes first
- Repeatedly:
   - Display the current board
   - Prompt the current player to enter their move (row and column)
   - Update the board with the player's move
   - If there is a winner or a draw, display the final board and announce the result, then end the game
   - Otherwise, switch to the other player and continue

You are free to implement the game in any way you see fit, as long as it meets the requirements below.

Do your work for this part in `q4.py`.

#### Requirements
1. The game must use (`import`) the functions you created in Part 3 to manage the game, check for wins/draws, and format the board for display
2. You must use a `__main__` guard that calls a parameterless `tictactoe()` function to start the game when the script is run directly
3. For full marks, make the app as robust and user-friendly as possible. For example:
   - Validate user input to ensure that the entered row and column are valid integers between 0 and 2
   - Ensure that players cannot place their symbol in an already occupied position (you should use your `is_occupied` function for this)
   - Handle any other potential errors gracefully, providing helpful error messages to the players. (E.g. ensure the user enters valid positions, re-prompt on blank inputs, etc.)
4. **CHALLENGE:** (not graded) Enhance the game to allow players to play multiple rounds, keeping track of the score across rounds, allow players to choose to play again or exit after each round, etc.

## Reflect

Did you take notes in `reflections.md` as you worked? (See the [Reflections](#reflections) instructions above.) You should!

Did you document your AI usage adequately? (See the [AI Use](#ai-use) instructions above.) You must!

## Submission

1. **Test** your code to verify that it is working as expected (see the [Testing your code](#testing-your-code) section above).
2. **Review** your code to ensure that you are using appropriate names, comments, and docstrings
3. **Commit** all changes in your lab files with meaningful commit messages.
4. **Push** your commits to GitHub
5. **Verify** that the code on GitHub is correct
6. Create a **Pull request** using your lab branch as the 'compare' branch and the main branch as the 'base'
7. Navigate to the "Files Changed" tab of your pull request, and **copy the URL** to this page into the lab folder on the LMS.

## Rubric

See the rubric attached to this lab in the LMS

### Automatic limits:

Your grade will be limited to a maximum of 79% for any of the following:
- Missing / inadequate [AI Use Statement](#ai-use)
- Missing / inadequate [Reflections](#reflections)
- Incorrect lab [Setup](#setup)
