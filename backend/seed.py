#!/usr/bin/env python3
"""
Database Seeding Script for Terminal Quiz Master V2.
Safely seeds at least 15 questions per difficulty level (Basic, Intermediate, Advanced)
and demo users without duplicate insertions.
"""

import sys
import os

# Add backend directory to sys.path so app imports resolve
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app.database import SessionLocal, engine, Base
from app.models.question import Question
from app.models.user import User
from app.models.quiz_attempt import QuizAttempt
from app.auth.security import hash_password

QUESTIONS_DATA = [
    # ═══════════════════════════════════════════════════════════════════════════
    # BASIC LEVEL (15 Questions)
    # Topics: Variables, Data Types, Operators, Strings, Input, If-Else, Loops
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "b01",
        "difficulty_level": "basic",
        "topic": "Variables & Data Types",
        "question_text": "Which of the following is NOT a valid Python data type?",
        "option_a": "int",
        "option_b": "str",
        "option_c": "char",
        "option_d": "float",
        "correct_answer": "char",
        "explanation": "Python does not have a built-in `char` type. Individual characters are represented as strings of length 1 using the `str` type.",
        "code_snippet": None,
    },
    {
        "id": "b02",
        "difficulty_level": "basic",
        "topic": "Variables & Data Types",
        "question_text": "What will `type(3.14)` return in Python?",
        "option_a": "<class 'int'>",
        "option_b": "<class 'float'>",
        "option_c": "<class 'decimal'>",
        "option_d": "<class 'double'>",
        "correct_answer": "<class 'float'>",
        "explanation": "3.14 is a floating-point literal, so Python represents it as a `float` type. Python does not have `double` primitives.",
        "code_snippet": "print(type(3.14))  # <class 'float'>",
    },
    {
        "id": "b03",
        "difficulty_level": "basic",
        "topic": "Strings",
        "question_text": "What is the output of `\"Hello\"[1]` in Python?",
        "option_a": "H",
        "option_b": "e",
        "option_c": "He",
        "option_d": "Hello",
        "correct_answer": "e",
        "explanation": "Python strings use zero-based indexing. Index 0 is 'H', index 1 is 'e', and so on.",
        "code_snippet": "print(\"Hello\"[1])  # e",
    },
    {
        "id": "b04",
        "difficulty_level": "basic",
        "topic": "Strings",
        "question_text": "Which method converts a string to all uppercase letters?",
        "option_a": ".upper()",
        "option_b": ".toUpper()",
        "option_c": ".capitalize()",
        "option_d": ".toUpperCase()",
        "correct_answer": ".upper()",
        "explanation": "The `.upper()` method returns a copy of the string with all characters converted to uppercase.",
        "code_snippet": "text = \"hello\"\nprint(text.upper())  # HELLO",
    },
    {
        "id": "b05",
        "difficulty_level": "basic",
        "topic": "Operators",
        "question_text": "What does the `//` operator do in Python?",
        "option_a": "Regular division",
        "option_b": "Modulo (remainder)",
        "option_c": "Floor division",
        "option_d": "Exponentiation",
        "correct_answer": "Floor division",
        "explanation": "`//` performs floor division — it divides and rounds down to the nearest integer. For example, 7 // 2 = 3.",
        "code_snippet": "print(7 // 2)   # 3\nprint(7 / 2)    # 3.5",
    },
    {
        "id": "b06",
        "difficulty_level": "basic",
        "topic": "Conditions",
        "question_text": "What is the correct syntax to check if `x` is equal to 10 in Python?",
        "option_a": "if x = 10:",
        "option_b": "if x == 10:",
        "option_c": "if x === 10:",
        "option_d": "if x.equals(10):",
        "correct_answer": "if x == 10:",
        "explanation": "Python uses `==` for equality comparison. A single `=` is assignment, and `===` does not exist in Python.",
        "code_snippet": "x = 10\nif x == 10:\n    print(\"Yes!\")",
    },
    {
        "id": "b07",
        "difficulty_level": "basic",
        "topic": "Loops",
        "question_text": "How many times does the following loop print \"Hello\"?\nfor i in range(3):\n    print(\"Hello\")",
        "option_a": "2",
        "option_b": "3",
        "option_c": "4",
        "option_d": "0",
        "correct_answer": "3",
        "explanation": "`range(3)` generates the sequence [0, 1, 2], which contains 3 values. The loop runs 3 times.",
        "code_snippet": "for i in range(3):\n    print(\"Hello\")\n# Prints \"Hello\" 3 times",
    },
    {
        "id": "b08",
        "difficulty_level": "basic",
        "topic": "Variables & Data Types",
        "question_text": "Which of the following creates a boolean value in Python?",
        "option_a": "x = 1",
        "option_b": "x = True",
        "option_c": "x = \"true\"",
        "option_d": "x = Boolean(1)",
        "correct_answer": "x = True",
        "explanation": "Python booleans are capitalized keywords: `True` and `False`.",
        "code_snippet": "x = True\nprint(type(x))  # <class 'bool'>",
    },
    {
        "id": "b09",
        "difficulty_level": "basic",
        "topic": "Strings",
        "question_text": "What does `len(\"Python\")` return?",
        "option_a": "5",
        "option_b": "6",
        "option_c": "7",
        "option_d": "Error",
        "correct_answer": "6",
        "explanation": "The `len()` function returns the number of characters in a string. 'Python' contains 6 characters.",
        "code_snippet": "print(len(\"Python\"))  # 6",
    },
    {
        "id": "b10",
        "difficulty_level": "basic",
        "topic": "Conditions",
        "question_text": "What keyword is used for an alternative condition in Python?",
        "option_a": "else if",
        "option_b": "elsif",
        "option_c": "elif",
        "option_d": "elseif",
        "correct_answer": "elif",
        "explanation": "Python uses `elif` (short for 'else if') for chaining conditional branches.",
        "code_snippet": "score = 75\nif score >= 90:\n    print(\"A\")\nelif score >= 75:\n    print(\"B\")\nelse:\n    print(\"C\")",
    },
    {
        "id": "b11",
        "difficulty_level": "basic",
        "topic": "Input & Type Conversion",
        "question_text": "What data type does the built-in `input()` function always return in Python 3?",
        "option_a": "int",
        "option_b": "str",
        "option_c": "float",
        "option_d": "depends on user input",
        "correct_answer": "str",
        "explanation": "In Python 3, `input()` always returns the entered data as a string (`str`). You must explicitly convert it using `int()` or `float()` if needed.",
        "code_snippet": "val = input(\"Enter: \")\nprint(type(val))  # <class 'str'>",
    },
    {
        "id": "b12",
        "difficulty_level": "basic",
        "topic": "Input & Type Conversion",
        "question_text": "What will `int(\"42\") + 8` evaluate to?",
        "option_a": "\"428\"",
        "option_b": "50",
        "option_c": "TypeError",
        "option_d": "42.8",
        "correct_answer": "50",
        "explanation": "`int(\"42\")` converts the string \"42\" to integer 42, then 42 + 8 = 50.",
        "code_snippet": "result = int(\"42\") + 8\nprint(result)  # 50",
    },
    {
        "id": "b13",
        "difficulty_level": "basic",
        "topic": "Operators",
        "question_text": "What is the result of `2 ** 3` in Python?",
        "option_a": "6",
        "option_b": "8",
        "option_c": "9",
        "option_d": "5",
        "correct_answer": "8",
        "explanation": "The `**` operator represents exponentiation in Python: 2 ** 3 = 2³ = 8.",
        "code_snippet": "print(2 ** 3)  # 8",
    },
    {
        "id": "b14",
        "difficulty_level": "basic",
        "topic": "Loops",
        "question_text": "What statement terminates the current loop immediately?",
        "option_a": "continue",
        "option_b": "break",
        "option_c": "pass",
        "option_d": "stop",
        "correct_answer": "break",
        "explanation": "`break` terminates the nearest enclosing loop immediately. `continue` skips to the next iteration, and `pass` is a null statement.",
        "code_snippet": "for i in range(5):\n    if i == 2:\n        break\nprint(i)  # 2",
    },
    {
        "id": "b15",
        "difficulty_level": "basic",
        "topic": "Loops",
        "question_text": "What will be the output of `while count < 3` when starting with `count = 0` and incrementing by 1 each time?",
        "option_a": "0 1 2",
        "option_b": "0 1 2 3",
        "option_c": "1 2 3",
        "option_d": "Infinite loop",
        "correct_answer": "0 1 2",
        "explanation": "The while loop runs for count = 0, 1, 2. When count reaches 3, the condition `count < 3` evaluates to False and the loop exits.",
        "code_snippet": "count = 0\nwhile count < 3:\n    print(count, end=' ')\n    count += 1\n# Output: 0 1 2",
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # INTERMEDIATE LEVEL (15 Questions)
    # Topics: Functions, Lists, Tuples, Dictionaries, Nested Loops, Exceptions, OOP
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "i01",
        "difficulty_level": "intermediate",
        "topic": "Functions",
        "question_text": "What is the output of the following code?",
        "option_a": "5",
        "option_b": "10",
        "option_c": "15",
        "option_d": "None",
        "correct_answer": "10",
        "explanation": "`*args` allows a function to accept any number of positional arguments packed as a tuple. Here, sum((2, 3, 5)) = 10.",
        "code_snippet": "def total(*args):\n    return sum(args)\n\nprint(total(2, 3, 5))",
    },
    {
        "id": "i02",
        "difficulty_level": "intermediate",
        "topic": "Lists",
        "question_text": "What does the following list comprehension produce?\n[x**2 for x in range(1, 5)]",
        "option_a": "[1, 4, 9, 16]",
        "option_b": "[1, 4, 9, 16, 25]",
        "option_c": "[0, 1, 4, 9]",
        "option_d": "[2, 4, 6, 8]",
        "correct_answer": "[1, 4, 9, 16]",
        "explanation": "`range(1, 5)` generates 1, 2, 3, 4. Squaring each yields [1, 4, 9, 16].",
        "code_snippet": "result = [x**2 for x in range(1, 5)]\nprint(result)  # [1, 4, 9, 16]",
    },
    {
        "id": "i03",
        "difficulty_level": "intermediate",
        "topic": "Dictionaries",
        "question_text": "What is the output of `d.get(\"z\", 99)` when `d = {\"a\": 1, \"b\": 2}`?",
        "option_a": "1",
        "option_b": "2",
        "option_c": "99",
        "option_d": "KeyError",
        "correct_answer": "99",
        "explanation": "`dict.get(key, default)` returns the provided default value (99) if the key is not present, avoiding a KeyError.",
        "code_snippet": "d = {\"a\": 1, \"b\": 2}\nprint(d.get(\"z\", 99))  # 99",
    },
    {
        "id": "i04",
        "difficulty_level": "intermediate",
        "topic": "Functions",
        "question_text": "What is a lambda function in Python?",
        "option_a": "A function that runs asynchronously",
        "option_b": "An anonymous, single-expression function",
        "option_c": "A function that can only take one argument",
        "option_d": "A built-in function for list operations",
        "correct_answer": "An anonymous, single-expression function",
        "explanation": "Lambda functions are small, anonymous functions defined with the `lambda` keyword that consist of a single expression.",
        "code_snippet": "double = lambda x: x * 2\nprint(double(5))  # 10",
    },
    {
        "id": "i05",
        "difficulty_level": "intermediate",
        "topic": "Exceptions",
        "question_text": "Which block always runs whether an exception occurs or not?",
        "option_a": "except",
        "option_b": "else",
        "option_c": "finally",
        "option_d": "catch",
        "correct_answer": "finally",
        "explanation": "The `finally` block always executes after `try` and `except` blocks, making it ideal for cleanup operations.",
        "code_snippet": "try:\n    x = 1 / 0\nexcept ZeroDivisionError:\n    print(\"Error\")\nfinally:\n    print(\"Always runs\")",
    },
    {
        "id": "i06",
        "difficulty_level": "intermediate",
        "topic": "Lists",
        "question_text": "What is the difference between `append()` and `extend()` on a list?",
        "option_a": "They are identical",
        "option_b": "append() adds a single element; extend() adds all elements from an iterable",
        "option_c": "extend() adds a single element; append() adds all elements",
        "option_d": "append() creates a new list; extend() modifies in place",
        "correct_answer": "append() adds a single element; extend() adds all elements from an iterable",
        "explanation": "`append()` adds its argument as a single element. `extend()` unpacks the iterable and adds its elements individually.",
        "code_snippet": "a = [1, 2]\na.append([3, 4])  # [1, 2, [3, 4]]\nb = [1, 2]\nb.extend([3, 4])  # [1, 2, 3, 4]",
    },
    {
        "id": "i07",
        "difficulty_level": "intermediate",
        "topic": "OOP Basics",
        "question_text": "What is the primary purpose of Python's `__init__` method?",
        "option_a": "It destroys an object when done",
        "option_b": "It initializes the object's attributes when an instance is created",
        "option_c": "It defines class-level constants",
        "option_d": "It must return the class instance explicitly",
        "correct_answer": "It initializes the object's attributes when an instance is created",
        "explanation": "`__init__` is the instance initializer (constructor) invoked automatically when an instance of a class is created.",
        "code_snippet": "class Dog:\n    def __init__(self, name):\n        self.name = name\n\nd = Dog(\"Rex\")\nprint(d.name)  # Rex",
    },
    {
        "id": "i08",
        "difficulty_level": "intermediate",
        "topic": "Dictionaries",
        "question_text": "What does `dict.items()` return?",
        "option_a": "A list of all keys",
        "option_b": "A list of all values",
        "option_c": "A view of (key, value) tuples",
        "option_d": "A sorted dictionary",
        "correct_answer": "A view of (key, value) tuples",
        "explanation": "`dict.items()` returns a dynamic dict_items view of (key, value) pairs.",
        "code_snippet": "d = {\"x\": 1, \"y\": 2}\nfor k, v in d.items():\n    print(k, v)",
    },
    {
        "id": "i09",
        "difficulty_level": "intermediate",
        "topic": "Functions",
        "question_text": "What is the output of the following code?",
        "option_a": "5",
        "option_b": "10",
        "option_c": "0",
        "option_d": "Error",
        "correct_answer": "10",
        "explanation": "Default parameters take effect when the caller omits that argument: multiply(5) uses factor=2, producing 5 * 2 = 10.",
        "code_snippet": "def multiply(x, factor=2):\n    return x * factor\n\nprint(multiply(5))",
    },
    {
        "id": "i10",
        "difficulty_level": "intermediate",
        "topic": "Nested Loops",
        "question_text": "How many times does `print(\"*\")` execute in the following code?\nfor i in range(3):\n    for j in range(2):\n        print(\"*\")",
        "option_a": "3",
        "option_b": "2",
        "option_c": "6",
        "option_d": "5",
        "correct_answer": "6",
        "explanation": "The outer loop runs 3 times; for each iteration, the inner loop executes 2 times. 3 * 2 = 6 iterations total.",
        "code_snippet": "for i in range(3):\n    for j in range(2):\n        print(\"*\")\n# 6 times",
    },
    {
        "id": "i11",
        "difficulty_level": "intermediate",
        "topic": "Tuples & Sets",
        "question_text": "What is the primary difference between a list and a tuple in Python?",
        "option_a": "Lists are immutable; tuples are mutable",
        "option_b": "Lists are mutable; tuples are immutable",
        "option_c": "Tuples cannot contain different data types",
        "option_d": "Lists cannot be iterated over",
        "correct_answer": "Lists are mutable; tuples are immutable",
        "explanation": "Tuples are immutable sequences whose contents cannot be modified after creation, while lists can be altered in-place.",
        "code_snippet": "my_tuple = (1, 2, 3)\n# my_tuple[0] = 99 -> Raises TypeError",
    },
    {
        "id": "i12",
        "difficulty_level": "intermediate",
        "topic": "Tuples & Sets",
        "question_text": "What is the output of `len(set([1, 2, 2, 3, 3, 3]))`?",
        "option_a": "6",
        "option_b": "3",
        "option_c": "1",
        "option_d": "TypeError",
        "correct_answer": "3",
        "explanation": "Sets in Python automatically eliminate duplicates. The unique elements are {1, 2, 3}, so the length is 3.",
        "code_snippet": "s = set([1, 2, 2, 3, 3, 3])\nprint(len(s))  # 3",
    },
    {
        "id": "i13",
        "difficulty_level": "intermediate",
        "topic": "List Methods",
        "question_text": "What does `numbers.pop()` do when called with no arguments on a non-empty list?",
        "option_a": "Removes and returns the first element",
        "option_b": "Removes and returns the last element",
        "option_c": "Deletes the entire list",
        "option_d": "Reverses the list in place",
        "correct_answer": "Removes and returns the last element",
        "explanation": "By default, `list.pop()` removes and returns the last item in the list (index -1).",
        "code_snippet": "nums = [10, 20, 30]\nval = nums.pop()\nprint(val, nums)  # 30 [10, 20]",
    },
    {
        "id": "i14",
        "difficulty_level": "intermediate",
        "topic": "Exceptions",
        "question_text": "What block in a `try-except` statement executes only if NO exceptions were raised in the try block?",
        "option_a": "finally",
        "option_b": "else",
        "option_c": "catch",
        "option_d": "then",
        "correct_answer": "else",
        "explanation": "The `else` clause in exception handling runs exclusively when the `try` block completes successfully without any exceptions.",
        "code_snippet": "try:\n    x = 10 / 2\nexcept ZeroDivisionError:\n    print('fail')\nelse:\n    print('success')  # This runs",
    },
    {
        "id": "i15",
        "difficulty_level": "intermediate",
        "topic": "OOP Basics",
        "question_text": "What does the `self` parameter represent in an instance method?",
        "option_a": "The class definition itself",
        "option_b": "The current instance of the class",
        "option_c": "A pointer to the parent class",
        "option_d": "A global singleton instance",
        "correct_answer": "The current instance of the class",
        "explanation": "`self` explicitly refers to the specific instance upon which the method is called, allowing access to its attributes.",
        "code_snippet": "class Player:\n    def set_name(self, name):\n        self.name = name",
    },

    # ═══════════════════════════════════════════════════════════════════════════
    # ADVANCED LEVEL (15 Questions)
    # Topics: Recursion, Advanced OOP, Algorithms, Generators, Decorators, Output
    # ═══════════════════════════════════════════════════════════════════════════
    {
        "id": "a01",
        "difficulty_level": "advanced",
        "topic": "OOP",
        "question_text": "What is the output of the following code?",
        "option_a": "Animal speaks\nDog barks",
        "option_b": "Dog barks\nAnimal speaks",
        "option_c": "Dog barks",
        "option_d": "Error",
        "correct_answer": "Dog barks",
        "explanation": "Python uses method resolution order (MRO). Because `Dog` overrides `speak()`, calling `d.speak()` executes `Dog.speak` directly.",
        "code_snippet": "class Animal:\n    def speak(self):\n        print(\"Animal speaks\")\n\nclass Dog(Animal):\n    def speak(self):\n        print(\"Dog barks\")\n\nd = Dog()\nd.speak()",
    },
    {
        "id": "a02",
        "difficulty_level": "advanced",
        "topic": "Recursion",
        "question_text": "What is the return value of `factorial(4)` given this code?",
        "option_a": "8",
        "option_b": "16",
        "option_c": "24",
        "option_d": "12",
        "correct_answer": "24",
        "explanation": "factorial(4) = 4 * 3 * 2 * 1 = 24. The base case factorial(0) returns 1.",
        "code_snippet": "def factorial(n):\n    if n == 0:\n        return 1\n    return n * factorial(n - 1)\n\nprint(factorial(4))  # 24",
    },
    {
        "id": "a03",
        "difficulty_level": "advanced",
        "topic": "Generators",
        "question_text": "What keyword turns a function into a generator in Python?",
        "option_a": "return",
        "option_b": "yield",
        "option_c": "async",
        "option_d": "generate",
        "correct_answer": "yield",
        "explanation": "`yield` pauses the function execution, preserves its local state, and yields a value back to the iterator.",
        "code_snippet": "def count_up(n):\n    for i in range(n):\n        yield i\n\nfor x in count_up(3):\n    print(x)  # 0, 1, 2",
    },
    {
        "id": "a04",
        "difficulty_level": "advanced",
        "topic": "Decorators",
        "question_text": "What does a Python decorator do?",
        "option_a": "It adds CSS styling to output",
        "option_b": "It wraps a function to modify or extend its behavior without changing its code",
        "option_c": "It creates a new class method",
        "option_d": "It compiles Python to native code for speed",
        "correct_answer": "It wraps a function to modify or extend its behavior without changing its code",
        "explanation": "A decorator is a callable that takes a function as argument and returns an augmented wrapper function.",
        "code_snippet": "def my_decorator(func):\n    def wrapper():\n        print(\"Before\")\n        func()\n        print(\"After\")\n    return wrapper\n\n@my_decorator\ndef greet():\n    print(\"Hello!\")",
    },
    {
        "id": "a05",
        "difficulty_level": "advanced",
        "topic": "Data Structures",
        "question_text": "What is the time complexity of inserting at the beginning of a standard Python list?",
        "option_a": "O(1)",
        "option_b": "O(log n)",
        "option_c": "O(n)",
        "option_d": "O(n²)",
        "correct_answer": "O(n)",
        "explanation": "Inserting at index 0 requires shifting all n existing elements one slot to the right in memory, making it O(n). For O(1), use `collections.deque`.",
        "code_snippet": "my_list = [1, 2, 3]\nmy_list.insert(0, 0)  # O(n)",
    },
    {
        "id": "a06",
        "difficulty_level": "advanced",
        "topic": "OOP",
        "question_text": "What does `super()` do in Python?",
        "option_a": "Creates a superuser account",
        "option_b": "Returns the parent class and allows calling its methods",
        "option_c": "Runs the program with elevated privileges",
        "option_d": "Converts a class to a superclass",
        "correct_answer": "Returns the parent class and allows calling its methods",
        "explanation": "`super()` returns a proxy object delegating method calls to a parent or sibling class based on MRO.",
        "code_snippet": "class Dog(Animal):\n    def __init__(self, name, breed):\n        super().__init__(name)\n        self.breed = breed",
    },
    {
        "id": "a07",
        "difficulty_level": "advanced",
        "topic": "Algorithms",
        "question_text": "What is the average time complexity of Python's built-in `sorted()` function?",
        "option_a": "O(n)",
        "option_b": "O(n log n)",
        "option_c": "O(n²)",
        "option_d": "O(log n)",
        "correct_answer": "O(n log n)",
        "explanation": "Python's `sorted()` uses Timsort (hybrid of merge sort and insertion sort), with O(n log n) average and worst-case complexity.",
        "code_snippet": "data = [3, 1, 4, 1, 5]\nsorted_data = sorted(data)  # O(n log n)",
    },
    {
        "id": "a08",
        "difficulty_level": "advanced",
        "topic": "Generators",
        "question_text": "What is the output of the following code?",
        "option_a": "[0, 1, 4, 9, 16]",
        "option_b": "<generator object>",
        "option_c": "(0, 1, 4, 9, 16)",
        "option_d": "[0, 1, 2, 3, 4]",
        "correct_answer": "<generator object>",
        "explanation": "Parentheses `()` create a generator expression rather than a tuple or list. Elements are evaluated lazily on demand.",
        "code_snippet": "gen = (x**2 for x in range(5))\nprint(gen)\n# <generator object <genexpr> at 0x...>",
    },
    {
        "id": "a09",
        "difficulty_level": "advanced",
        "topic": "Decorators",
        "question_text": "Which built-in decorator makes a method belong to the class rather than instances?",
        "option_a": "@staticmethod",
        "option_b": "@classmethod",
        "option_c": "@property",
        "option_d": "@abstractmethod",
        "correct_answer": "@classmethod",
        "explanation": "`@classmethod` passes the class object (`cls`) as the first implicit argument instead of the instance (`self`).",
        "code_snippet": "class MyClass:\n    count = 0\n    @classmethod\n    def inc(cls):\n        cls.count += 1",
    },
    {
        "id": "a10",
        "difficulty_level": "advanced",
        "topic": "Complex Output",
        "question_text": "What is the output of this Python code?",
        "option_a": "[1, 2, 3]",
        "option_b": "[1, 2, 3, 4]",
        "option_c": "[1, 2, 3]\n[1, 2, 3, 4]",
        "option_d": "Error",
        "correct_answer": "[1, 2, 3]\n[1, 2, 3, 4]",
        "explanation": "Python passes mutable objects like lists by assignment (reference). `add_item` mutates the original list in place.",
        "code_snippet": "def add_item(lst, item):\n    print(lst)\n    lst.append(item)\n\na = [1, 2, 3]\nadd_item(a, 4)\nprint(a)",
    },
    {
        "id": "a11",
        "difficulty_level": "advanced",
        "topic": "Algorithms & Data Structures",
        "question_text": "What is the average lookup time complexity of a key in a Python `dict`?",
        "option_a": "O(1)",
        "option_b": "O(log n)",
        "option_c": "O(n)",
        "option_d": "O(n log n)",
        "correct_answer": "O(1)",
        "explanation": "Python dictionaries are implemented using hash tables, giving them an average-case key lookup complexity of O(1).",
        "code_snippet": "d = {'key': 'val'}\n# Lookup d['key'] is O(1) on average",
    },
    {
        "id": "a12",
        "difficulty_level": "advanced",
        "topic": "Advanced OOP",
        "question_text": "What is the Method Resolution Order (MRO) algorithm used in Python 3?",
        "option_a": "Depth-First Search (DFS)",
        "option_b": "Breadth-First Search (BFS)",
        "option_c": "C3 Superconcurrency Linearization",
        "option_d": "Dijkstra Linearization",
        "correct_answer": "C3 Superconcurrency Linearization",
        "explanation": "Python uses the C3 linearization algorithm to determine method resolution order in multiple inheritance hierarchies.",
        "code_snippet": "class A: pass\nclass B(A): pass\nprint(B.__mro__)",
    },
    {
        "id": "a13",
        "difficulty_level": "advanced",
        "topic": "Generators & Iterators",
        "question_text": "What exception does an iterator raise when there are no further items available in `next()`?",
        "option_a": "IndexError",
        "option_b": "StopIteration",
        "option_c": "KeyError",
        "option_d": "GeneratorExit",
        "correct_answer": "StopIteration",
        "explanation": "When an iterator is exhausted, calling `next(iterator)` raises a `StopIteration` exception, which `for` loops catch to terminate.",
        "code_snippet": "it = iter([1])\nnext(it)  # 1\n# next(it) -> raises StopIteration",
    },
    {
        "id": "a14",
        "difficulty_level": "advanced",
        "topic": "Problem-Solving",
        "question_text": "What is the output of the following mutable default argument snippet?",
        "option_a": "[1]\n[1]",
        "option_b": "[1]\n[1, 2]",
        "option_c": "[1]\n[2]",
        "option_d": "TypeError",
        "correct_answer": "[1]\n[1, 2]",
        "explanation": "Default parameter values are evaluated once at function definition time. The list `items` is shared across calls.",
        "code_snippet": "def append_to(element, items=[]):\n    items.append(element)\n    return items\n\nprint(append_to(1))\nprint(append_to(2))",
    },
    {
        "id": "a15",
        "difficulty_level": "advanced",
        "topic": "Problem-Solving",
        "question_text": "What is the difference between `is` and `==` in Python?",
        "option_a": "`is` compares values; `==` compares memory identities",
        "option_b": "`is` compares memory identities; `==` compares equality of values",
        "option_c": "They are completely interchangeable aliases",
        "option_d": "`is` is used only for strings; `==` is for numbers",
        "correct_answer": "`is` compares memory identities; `==` compares equality of values",
        "explanation": "`is` checks if two references point to the exact same object in memory (`id(a) == id(b)`), while `==` checks value equality.",
        "code_snippet": "a = [1, 2]\nb = [1, 2]\nprint(a == b)  # True (equal values)\nprint(a is b)  # False (distinct objects)",
    },
]

DEMO_USERS = [
    {"username": "SakuraCoder", "email": "sakura@example.com", "total_xp": 2840},
    {"username": "PyroNinja", "email": "pyro@example.com", "total_xp": 2610},
    {"username": "QuantumDev", "email": "quantum@example.com", "total_xp": 2380},
    {"username": "CodeSamurai", "email": "samurai@example.com", "total_xp": 2100},
    {"username": "AlgoBeast", "email": "beast@example.com", "total_xp": 1920},
    {"username": "DataWizard", "email": "wizard@example.com", "total_xp": 1750},
    {"username": "ByteHunter", "email": "hunter@example.com", "total_xp": 1590},
    {"username": "SyntaxStorm", "email": "storm@example.com", "total_xp": 1340},
]


def seed_database():
    """Seed questions and demo users idempotently."""
    print("🌱 Initializing database schema...")
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()

    try:
        # Seed Questions
        print(f"📚 Seeding {len(QUESTIONS_DATA)} questions...")
        inserted_q = 0
        updated_q = 0

        for q_data in QUESTIONS_DATA:
            existing = db.query(Question).filter(Question.id == q_data["id"]).first()
            if not existing:
                q = Question(**q_data, is_active=True)
                db.add(q)
                inserted_q += 1
            else:
                # Update fields if changed
                for k, v in q_data.items():
                    setattr(existing, k, v)
                updated_q += 1

        db.commit()
        print(f"✅ Questions: {inserted_q} new inserted, {updated_q} verified/updated.")

        # Seed Demo Users
        print(f"👥 Seeding {len(DEMO_USERS)} leaderboard demo users...")
        inserted_u = 0
        default_hashed_pwd = hash_password("QuizMaster2026!")

        for u_data in DEMO_USERS:
            existing_user = db.query(User).filter(User.username == u_data["username"]).first()
            if not existing_user:
                user = User(
                    username=u_data["username"],
                    email=u_data["email"],
                    hashed_password=default_hashed_pwd,
                    total_xp=u_data["total_xp"],
                )
                db.add(user)
                inserted_u += 1

        db.commit()
        print(f"✅ Demo Users: {inserted_u} inserted.")

        # Verify Counts
        basic_count = db.query(Question).filter(Question.difficulty_level == "basic").count()
        inter_count = db.query(Question).filter(Question.difficulty_level == "intermediate").count()
        adv_count = db.query(Question).filter(Question.difficulty_level == "advanced").count()
        total_users = db.query(User).count()

        print("-" * 50)
        print(f"🎉 Database Seeding Summary:")
        print(f"  • Basic Questions:        {basic_count}")
        print(f"  • Intermediate Questions: {inter_count}")
        print(f"  • Advanced Questions:     {adv_count}")
        print(f"  • Total Questions:        {basic_count + inter_count + adv_count}")
        print(f"  • Total Users:            {total_users}")
        print("-" * 50)

    except Exception as e:
        db.rollback()
        print(f"❌ Error seeding database: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
