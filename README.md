# string-calculator
Given a String of a mathematical expression, can I solve it without making use of functions like Python's eval?

I'm using Poetry for my package.

Poetry installation instructions are here: https://python-poetry.org/docs/#installing-with-pipx  

Git clone the following repo: https://github.com/N-A-B-S/string-calculator  
cd into the directory  
poetry install  
poetry run python string_calculator.py  

I didn't implement a good way to change the expression you want to run so...

1. Open the string_calculator.py file
2. Change the expression on line 142
3. Save and exit
4. Re-run script.

If you want to run the tests to prove the test cases:
1. poetry run pytest

