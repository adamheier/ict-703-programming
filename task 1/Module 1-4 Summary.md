# ICT703 Programming — Summary Modules 1–4

> **Note on sources:** This summary is built from the topic slide PDFs and workshop instruction PDFs in `slides/Module 2` through `slides/Module 4`, cross-checked against the practice code in `practices-adam/` and `practices-oli/`. **No slide PDFs exist for Module 1** in this vault (the `slides/Module 1` folder is empty) — that section below is reconstructed from cross-references in the Module 2 workshop ("In Module 1, we showed how to write algorithms in ordinary English") and from your earliest practice files (`hello.py`, `pseudo.py`). If you have the original Module 1 slides elsewhere, let me know and I'll fold in anything missing.

---

## Module 1 — Introduction to Programming & Algorithmic Thinking *(reconstructed)*

### Topics covered
- **What a program is**: a sequence of instructions the computer executes step by step (the *sequence* control flow, later joined by *iteration*, *selection*, and *abstraction* in Module 3/4).
- **Algorithms in plain English**: describing a solution as a numbered list of steps before writing any code.
- **Pseudocode**: a stylised, language-independent way of writing an algorithm (`if condition then action`, `for each item do action`, etc.) — used throughout the course before implementing in Python.
- **Basic Python I/O**:
  - `print()` to display output.
  - `input()` to collect text from the user (always returns a `str`).
  - String concatenation with `+`.
  - Multi-line/triple-quoted strings (`'''...'''`) for docstrings/comments.
- **Basic control flow with `if` / `elif` / `else` and simple loops** used to sort items into categories (the classic "M&M sorting" and "lollies sorting" pattern) — this pattern is referenced again in the Module 4 workshop ("Expand the **M&M program**..."), confirming it originates in Module 1.

### Workshop tasks & solutions

**Task: Hello World / greeting program**
Print a greeting, then greet the user and a friend by name.

```python
# Greet the user
print("Hello World!")

name = input("What is your name? ")
print("Hello " + name + ", how are you today?")

friend_name = input("What is your friend's name? ")
print("Hello " + friend_name + " and " + name + ", how are you two today?")

# A second greeting using a docstring as a comment block
'''Happy Birthday!'''
name = input("What is your name: ")
print("Happy Birthday " + name + "!")
```

**Task: Sort M&Ms into bowls by colour, discarding blue ones**
> *I have a jar of M&Ms (red, green, yellow, blue, brown). Sort them into their colours but throw away the blue ones.*

```python
def sort_mms(mms):
    """Sort M&Ms by colour into separate bowls; blue M&Ms are discarded."""
    red_bowl = []
    green_bowl = []
    yellow_bowl = []
    brown_bowl = []

    for mm in mms:
        if mm == 'blue':
            continue  # blue M&Ms are thrown away, not sorted
        elif mm == 'red':
            red_bowl.append(mm)
        elif mm == 'green':
            green_bowl.append(mm)
        elif mm == 'yellow':
            yellow_bowl.append(mm)
        elif mm == 'brown':
            brown_bowl.append(mm)

    return red_bowl, green_bowl, yellow_bowl, brown_bowl


mms = ['red', 'green', 'blue', 'yellow', 'brown', 'blue', 'green', 'red', 'yellow', 'brown']
red, green, yellow, brown = sort_mms(mms)
print("Red M&M's:", red)
print("Green M&M's:", green)
print("Yellow M&M's:", yellow)
print("Brown M&M's:", brown)

# Extension: print the number of different M&M colours in the bowl
print("Number of different M&M colours in the bowl:", len(set(mms)))
```

**Task: Sort lollies into 3 preference piles (pseudocode + program)**
> *pile1 = cherry (favourite), pile2 = berry, pile3 = orange (least favourite).*

Pseudocode:
```
For every lollie in the jar:
    if lollie is cherry: put on pile1
    elif lollie is berry: put on pile2
    else (lollie is orange): put on pile3
```

```python
def sort_lollies(lollies):
    """Sort lollies into 3 piles based on preference (cherry > berry > orange)."""
    pile1 = []  # favourite: cherry
    pile2 = []  # medium: berry
    pile3 = []  # least favourite: orange

    for lollie in lollies:
        if lollie == 'cherry':
            pile1.append(lollie)
        elif lollie == 'berry':
            pile2.append(lollie)
        else:  # orange
            pile3.append(lollie)

    return pile1, pile2, pile3


lollies = ['orange', 'berry', 'cherry', 'orange', 'berry', 'cherry', 'cherry', 'berry', 'cherry', 'cherry']
pile1, pile2, pile3 = sort_lollies(lollies)
print("Pile 1 (Cherry):", pile1)
print("Pile 2 (Berry):", pile2)
print("Pile 3 (Orange):", pile3)
```

---

## Module 2 — Software Development, Python Data Types, Documentation

### Topic 1: Software Development
- **Software development** = the process of planning and organising a program.
- **Waterfall model** (sequential phases, each verified before moving on): Customer request → Analysis → Design → Implementation → Integration → Maintenance.
  - Programs rarely work correctly the first time — **testing** is essential.
  - Cost of fixing a bug rises steeply the later it's found: **Maintenance accounts for ~68%** of total lifecycle cost, vs. ~8% each for Analysis/Design/Implementation/Integration.
- **Agile model**: iterative & incremental — each cycle (Plan → Build → Test → Review → Deploy) delivers a small working increment quickly, rather than one long sequential pass.
  - Key Agile principles: early & continuous delivery, welcome changing requirements, daily collaboration between business and developers, working software as the primary measure of progress, simplicity, self-organising teams.
  - **Waterfall** is process-centric/command-and-control; **Agile** is people-centric/leadership-and-collaboration, favours self-organising teams and object-oriented technology.

### Topic 2: Python Data Types
- **Data types** in Python: `str` (text), `int` (whole numbers), `float` (decimals), `bool` (True/False), `list`, `set`, `dict`, and more.
- A **data type** = a set of values + the operations you can perform on them. A **literal** is how a value looks in code (e.g. `"Hi"`, `3.14`, `-1`).
- **Integers (`int`)**: whole numbers, written without commas; Python's range is limited only by memory.
- **Floats (`float`)**: represent real numbers with finite precision (~16 significant digits); can be written in decimal (`3.78`) or scientific notation (`3.78e0`).
- **String literals**: enclosed in `'...'` or `"..."`; `''`/`""` is the empty string; triple quotes (`'''...'''`/`"""..."""`) allow multi-line strings.
- **String concatenation**: joining strings with `+` (e.g. `"Hi " + "there"`).
- **Variables**: associate a name with a value via `<name> = <expression>`.
  - Naming rules: cannot be a reserved word (`if`, `def`, `import`, ...), must start with a letter or `_`, can contain letters/digits/`_`, are case-sensitive.
  - Convention: `camelCase` for variables (e.g. `interestRate`), `ALL_CAPS` for constants (e.g. `TAX_RATE`).
- **Expressions & arithmetic operators**: `-` (negation), `**` (exponent), `*`, `/`, `//` (quotient), `%` (remainder/modulus), `+`, `-`.
  - **Precedence**: `**` highest → unary `-` → `*`, `/`, `%` → `+`, `-` → `=` lowest. Equal-precedence ops evaluate left-to-right, except `**` and `=` which are right-associative. Use `()` to override order.
  - **Mixed-mode arithmetic**: if both operands are the same numeric type, the result is that type; if types differ, the result is the more general type (e.g. `3 / 4` → `0`, but `3 / 4.0` → `0.75`... actually in Python 3, `/` always returns `float`; `//` returns the floored/integer-style result).
- **Type conversion functions**: `int(...)`, `float(...)`, `str(...)`.
  - `input()` always returns a `str` — must convert with `int()`/`float()` before doing arithmetic.
  - `int()` **truncates** a float (`int(6.75)` → `6`), it does **not** round; use `round()` to round (`round(6.75)` → `7`).
  - Concatenating a string with a number directly raises `TypeError` — convert the number with `str()` first: `'$' + str(profit)`.
  - Python is a **strongly typed** language: it never silently converts between unrelated types.

### Topic 3: Documentation
- **Comments**: text the interpreter ignores but that documents the code for programmers.
  - **Docstrings**: multi-line strings (`'''...'''`) typically placed at the top of a program/function to describe its purpose, author, and date.
  - **End-of-line comments**: start with `#` and run to the end of the line, e.g. `RATE = 0.85  # Conversion rate CAD→USD`.
- Good practice: state the program's purpose up top, comment each variable's purpose, comment before major code blocks, and explain any tricky logic.
- **All submitted work must contain comments** — this is an explicit course requirement.

### Workshop tasks & solutions

**Task 1: Income Tax Calculator** (full software-development cycle: request → analysis → design → implementation → testing)

Tax rules: flat 20% tax rate, $10,000 standard deduction, $3,000 deduction per dependent, negative tax should still be reported as a negative number here (Module 3 later adds the "clamp to 0" rule).

Pseudocode:
```
CONSTANT dependent_deduction = 3000
CONSTANT standard_deduction = 10000
1. Ask the user for gross income and number of dependents.
2. total_deductions = standard_deduction + (number_of_dependents * dependent_deduction)
3. net_income = gross_income - total_deductions
4. income_tax = net_income * 0.20
5. Print income_tax
```

```python
"""
Program: income_tax_calculator.py
Purpose: Computes income tax given gross income and number of dependents,
         using a flat 20% tax rate, $10,000 standard deduction and $3,000
         deduction per dependent.
"""

STANDARD_DEDUCTION = 10000
DEPENDENT_DEDUCTION = 3000
FLAT_TAX_RATE = 0.20

gross_income = float(input("Enter the gross income: "))
number_of_dependents = int(input("Enter the number of dependents: "))

total_deductions = STANDARD_DEDUCTION + number_of_dependents * DEPENDENT_DEDUCTION
net_income = gross_income - total_deductions
income_tax = net_income * FLAT_TAX_RATE

print("The income tax is $" + str(income_tax))
```

Test table from the workshop (all pass with this implementation):

| Dependents | Gross Income | Expected Tax |
|---|---|---|
| 0 | 10000 | 0 |
| 1 | 10000 | -600 |
| 2 | 10000 | -1200 |
| 0 | 20000 | 2000 |
| 1 | 20000 | 1400 |
| 2 | 20000 | 800 |
| 3 | 150000 | 26200.0 |

**Task 2 (Workshop Part 2), Activity 1: Conversion**

```python
# a) String to number
number_as_text = input("Enter a number as text: ")
number = float(number_as_text)
print(f"You entered '{number_as_text}', converted to the number {number}")

# b) Number to string
value = float(input("Enter a number: "))
value_as_text = str(value)
print(f"The number {value} as a string is '{value_as_text}' (type: {type(value_as_text).__name__})")

# c) Two numbers -> all arithmetic results
a = float(input("Enter the first number: "))
b = float(input("Enter the second number: "))
print(f"Sum: {a + b}")
print(f"Difference: {a - b}")
print(f"Product: {a * b}")
print(f"Division: {a / b}")
print(f"Quotient: {a // b}")
print(f"Remainder: {a % b}")
print(f"Exponentiation: {a ** b}")
```

**Task 2, Activity 2: Banking (5 transactions)**

```python
print("Hello and welcome to the banking program")

balance = float(input("Please enter your starting balance: "))
print("Starting balance:", balance)

deposit_1 = float(input("Deposit 1 amount: "))
balance += deposit_1
print("Deposit 1:", deposit_1, "-> Running balance:", balance)

deposit_2 = float(input("Deposit 2 amount: "))
balance += deposit_2
print("Deposit 2:", deposit_2, "-> Running balance:", balance)

deposit_3 = float(input("Deposit 3 amount: "))
balance += deposit_3
print("Deposit 3:", deposit_3, "-> Running balance:", balance)

withdrawal_1 = float(input("Withdrawal 1 amount: "))
balance -= withdrawal_1
print("Withdrawal 1:", withdrawal_1, "-> Running balance:", balance)

withdrawal_2 = float(input("Withdrawal 2 amount: "))
balance -= withdrawal_2
print("Withdrawal 2:", withdrawal_2, "-> Running balance:", balance)

print("Final balance:", balance)
```

**Task 3 (Workshop Part 3): Print Formatting, Circle Area, Name Reversed, Print a List, File Extension, n+nn+nnn, Docstrings**

```python
# 1. Print Formatting — reproduce the exact stepped-indentation output
print("Twinkle, twinkle, little star,\n\tHow I wonder what you are!"
      "\n\t\tUp above the world so high,\n\t\tLike a diamond in the sky."
      "\nTwinkle, twinkle, little star,\n\tHow I wonder what you are")

# 2. Area of a Circle
import math
r = float(input("r = "))
print(f"Area = {math.pi * r ** 2}")

# 3. Name Reversed
first_name = input("Enter your first name: ")
last_name = input("Enter your last name: ")
print(f"{last_name} {first_name}")

# 4. Print a list from comma-separated input
raw_numbers = input("Enter comma-separated numbers: ")
number_list = []
for item in raw_numbers.split(","):
    number_list.append(float(item.strip()))
print(number_list)

# 5. File Extension
filename = input("Enter filename: ")
if "." in filename:
    extension = filename.split(".")[-1]
else:
    extension = ""
print(extension)

# 6. Compute n + nn + nnn
n = int(input("Enter an integer n: "))
nn = int(str(n) * 2)
nnn = int(str(n) * 3)
print(f"n + nn + nnn = {n + nn + nnn}")

# 7. Docstrings of built-in functions
for func in (print, len, input, int, str, float):
    print(f"--- {func.__name__} ---")
    print(func.__doc__)
    print()
```

---

## Module 3 — Iteration, Selection, Boolean Logic

### Topic 1: Iteration
- **Iteration** = repeating an action ("doing things many times"). Each repetition is a **pass**.
- **Definite/bounded iteration** (`for` loop): repeats a known/fixed number of times.
  - `for <variable> in range(<n>):` — the loop header, followed by an **indented** loop body.
  - `range(n)` counts from `0` to `n-1` — a common **off-by-one error** is forgetting this.
  - `range(start, stop)` counts from `start` to `stop-1`.
  - `range(start, stop, step)` — a third argument sets the step size; a **negative step** counts down.
  - You can traverse (loop over) any sequence directly: a list, a string, etc. — `for character in "Hi there!":`.
- **Indefinite/unbounded iteration** (`while` loop): repeats until a **continuation condition** becomes false.
  - Syntax: `while <condition>: <statements>`.
  - Also called an **entry-controlled loop** — the condition is checked *before* each pass, so the body can run zero or more times.
  - Improper use can cause an **infinite loop**; `Ctrl+C` halts a hung loop during testing.
  - A `while` loop can replace any `for` loop (used for count control) but needs manual initialisation and manual incrementing of the loop variable.
  - Common `while`-loop bugs: incorrectly initialised loop control variable, failing to update it inside the loop, failing to test it correctly.

### Topic 2: Selection
- **Selection statements** let a program make choices based on a **condition**.
- **One-way (`if`)**: `if <condition>: <statements>` — runs only if the condition is true.
- **Two-way (`if`/`else`)**: runs one branch or the other, never both.
- **Multi-way (`if`/`elif`/`else`)**: tests conditions in order, running the first branch whose condition is true; `else` is the default/fallback.
- Testing tip: exercise **every branch** of a selection statement, and test compound Boolean conditions with data covering all combinations of operand values.
- The `random` module (`import random`, `random.randint(a, b)`) generates random integers between `a` and `b` inclusive — used for games, simulations, etc.

### Topic 3: Boolean Logic
- **Boolean type**: `True` / `False`.
- **Comparison operators**: `==`, `!=`, `<`, `>`, `<=`, `>=` — all return a `bool`.
- **Logical operators**: `and` (both must be true), `or` (at least one must be true), `not` (inverts).
  - Truth tables: `A and B` is true only if both are true; `A or B` is true if at least one is true; `not A` flips `A`.
  - **Precedence**: `not` binds tighter than `and`, which binds tighter than `or` — so `not A and B` ≠ `not (A and B)`.
  - Full precedence order (highest→lowest): `**` → unary `-` → `*`,`/`,`%` → `+`,`-` → comparisons → `not` → `and` → `or` → `=`.
- **Short-circuit evaluation**: `A and B` stops evaluating as soon as `A` is false (result is already known); `A or B` stops as soon as `A` is true. This lets you safely guard against errors, e.g. `count > 0 and total // count > 10` avoids a division by zero when `count` is `0`.

### Workshop tasks & solutions

**Task 1 (Workshop), Activity 1: Predict loop output**

```python
for count in range(5):
    print(count, end=" ")
# Output: 0 1 2 3 4

for count in range(5):
    print(count + 1, end=" ")
# Output: 1 2 3 4 5

for count in range(1, 4):
    print(count, end=" ")
# Output: 1 2 3

for count in range(1, 6, 2):
    print(count, end=" ")
# Output: 1 3 5

for count in range(6, 1, -1):
    print(count, end=" ")
# Output: 6 5 4 3 2
```

**Activity 2: Loops and strings**

```python
text = input("Enter a string: ")
for character in text:
    print(character)
```

**Activity 3: Logic 1** (with `x = 3`, `y = 5`)

```python
x = 3
y = 5
print(x == y)          # False
print(x > y - 3)       # True   (3 > 2)
print(x <= y - 2)      # True   (3 <= 3)
print(x == y or x > 2) # True   (False or True)
print(x != 6 and y > 10)  # False  (True and False)
print(x > 0 and x < 100)  # True   (True and True)
```

**Activity 4: For to While**

```python
# for count in range(100): print(count)
count = 0
while count < 100:
    print(count)
    count += 1

# for count in range(1, 101): print(count)
count = 1
while count <= 100:
    print(count)
    count += 1

# for count in range(100, 0, -1): print(count)
count = 100
while count > 0:
    print(count)
    count -= 1
```

**Activity 5: Tax Calculator enhancements**

```python
"""
Enhances the Module 2 tax calculator:
a) captures invalid (non-numeric) input,
b) clamps any negative tax to 0,
c) replaces the flat rate with a progressive/tiered system:
   - $0–$19,999: no tax
   - $20,000–$49,999: 10% on the amount above $20,000
   - over $49,999: flat 20% on the whole income
"""

def get_float_safe(prompt):
    """Repeatedly prompt until the user enters a valid number."""
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def calculate_progressive_tax(income):
    """Return the tax owed under the progressive tax rules."""
    if income <= 19999:
        tax = 0
    elif income <= 49999:
        tax = (income - 20000) * 0.10
    else:
        tax = income * 0.20

    if tax < 0:
        tax = 0
    return tax


gross_income = get_float_safe("Enter your gross income: ")
tax = calculate_progressive_tax(gross_income)
print(f"The income tax is ${tax:.2f}")
```

**Task 2 (Workshop Part 2), Activity 1: Rock Paper Scissors (Part A + Part B, 5 rounds with score)**

```python
from random import randint

CHOICES = {1: "Rock", 2: "Paper", 3: "Scissors"}
wins = 0
losses = 0
ties = 0

for round_number in range(1, 6):  # Part B: repeat 5 times
    computer_choice = CHOICES[randint(1, 3)]

    player_pick = int(input("Choose 1) Rock  2) Paper  3) Scissors: "))
    player_choice = CHOICES[player_pick]

    print(f"You chose {player_choice}, the computer chose {computer_choice}")

    if player_choice == computer_choice:
        print("It's a tie!")
        ties += 1
    elif (player_choice == "Rock" and computer_choice == "Scissors") or \
         (player_choice == "Paper" and computer_choice == "Rock") or \
         (player_choice == "Scissors" and computer_choice == "Paper"):
        print("You win this round!")
        wins += 1
    else:
        print("The computer wins this round!")
        losses += 1

print(f"\nFinal score — Wins: {wins}, Losses: {losses}, Ties: {ties}")
if wins > losses:
    print("You won the game!")
elif wins < losses:
    print("The computer won the game!")
else:
    print("It's an overall tie!")
```

**Activity 2: MattsBank gets Sophisticated**

```python
name = input("Enter your name: ")
account_number = input("Enter your account number: ")
balance = float(input("Enter your starting balance: "))

while True:
    command = input("Command (deposit, withdraw, balance, stop): ").strip().lower()

    if command == "deposit":
        amount = float(input("Amount to deposit: "))
        balance += amount
        print(f"Deposit successful. New balance: ${balance:.2f}")
    elif command == "withdraw":
        amount = float(input("Amount to withdraw: "))
        if amount > balance:
            print(f"Insufficient funds. Current balance: ${balance:.2f}")
        else:
            balance -= amount
            print(f"Withdrawal successful. New balance: ${balance:.2f}")
    elif command == "balance":
        print(f"Current balance: ${balance:.2f}")
    elif command == "stop":
        print(f"Thank you, {name}. Final balance: ${balance:.2f}. Goodbye!")
        break
    else:
        print("Invalid command. Please try again.")
```

---

## Module 4 — Strings & Lists

### Topic 1: Strings
- A **string is a data structure**: an ordered sequence of characters. `len(s)` gives its length (character count).
- **String operators**:
  - `+` concatenates two strings.
  - `*` repeats a string (`"Bee " * 3` → `"Bee Bee Bee "`).
  - `[x]` (**subscript operator**) accesses the character at index `x` (0-based). Negative indices count from the end (`s[-1]` = last character).
  - `[x:y]` (**slicing**) returns a substring from index `x` up to (not including) `y`.
  - `in` / `not in` test membership (a substring can be searched for, not just a single character).
- Indexing out of range raises `IndexError`.
- **String methods** (call as `<string>.<method>(...)`; methods **return a new string/value** — they never modify the original string):
  - `upper()`, `lower()`, `capitalize()`, `title()`, `swapcase()`
  - `find(sub)` / `index(sub)` — position of a substring (`find` returns `-1` if not found; `index` raises an error)
  - `replace(old, new)` — replace occurrences
  - `split(sep)` — split into a **list** of substrings (default separator: whitespace)
  - `strip()` / `lstrip()` / `rstrip()` — remove leading/trailing whitespace (or specified characters)
  - `count(sub)` — count non-overlapping occurrences
  - Boolean-test methods: `isalpha()`, `isdigit()`, `isalnum()`, `isupper()`, `islower()`, `isspace()`, etc.

### Topic 2: Lists
- A **list** stores multiple values, is great when you don't know the amount of data up front, **can contain duplicates**, and is written as `[value1, value2, ...]`; `[]` is an empty list.
- A string can be thought of as a special case of a list (a list of characters).
- **Access & slicing**: same subscript/slice syntax as strings — `list[0]`, `list[1:3]`.
- **List methods** (these **do** mutate the list in place, unlike string methods):
  - `append(x)` — add `x` to the end
  - `insert(i, x)` — add `x` at position `i`
  - `remove(x)` — remove the first item equal to `x`
  - `pop([i])` — remove and return the item at position `i` (default: the last item)
  - `clear()` — remove all items
  - `index(x)` — position of the first item equal to `x`
  - `count(x)` — number of items equal to `x`
  - `sort()` / `reverse()` — sort / reverse in place
  - `extend(iterable)` — append all items from another iterable
  - `copy()` — return a shallow copy

### Workshop tasks & solutions

**Activity 1: Strings**

```python
inputString = "Python rules!"

# a) Length
print(len(inputString))            # 13

# b) List of words
print(inputString.split())         # ['Python', 'rules!']

# c) Uppercase
print(inputString.upper())         # PYTHON RULES!

# d) The 10th character (index 9, since indexing starts at 0)
print(inputString[9])              # l

# e) Position of the substring "rule"
print(inputString.find("rule"))    # 7

# f) Replace the first "!" with a "?"
print(inputString.replace("!", "?", 1))   # Python rules?
```

**Challenge 1: make it robust for any string (e.g. `"Hello World"`, which has no `"!"` and no `"rule"`)**

```python
def analyze_string(inputString):
    """Run the Activity 1 operations on inputString, handling short/mismatched strings safely."""
    print(f"\nInput: '{inputString}'")
    print("Length:", len(inputString))
    print("Words:", inputString.split())
    print("Uppercase:", inputString.upper())

    if len(inputString) >= 10:
        print("10th character:", inputString[9])
    else:
        print("10th character: (string is shorter than 10 characters)")

    position = inputString.find("rule")
    if position != -1:
        print("Position of 'rule':", position)
    else:
        print("'rule' not found in string")

    print("After replace:", inputString.replace("!", "?", 1))


analyze_string("Python rules!")
analyze_string("Hello World")
```

**Challenge 2: reverse a string**

```python
original = input("Enter a string: ")
reversed_string = original[::-1]
print("Original:", original)
print("Reversed:", reversed_string)
```

**Activity 2: Lists and Accumulators**

```python
# a) Expand the M&M program to also print the number of DIFFERENT colours
mms = ['red', 'green', 'blue', 'yellow', 'brown', 'blue', 'green', 'red', 'yellow', 'brown']
red, green, yellow, brown = [], [], [], []

for mm in mms:
    if mm == 'blue':
        continue  # blue M&Ms are discarded
    elif mm == 'red':
        red.append(mm)
    elif mm == 'green':
        green.append(mm)
    elif mm == 'yellow':
        yellow.append(mm)
    elif mm == 'brown':
        brown.append(mm)

print("Red:", red, "Green:", green, "Yellow:", yellow, "Brown:", brown)
print("Number of different M&M colours in the bowl:", len(set(mms)))


# b) 100 random numbers -> count odds and evens
# Pseudocode:
#   1. Generate a list of 100 random numbers.
#   2. For each number, check if it's even or odd and increment the matching counter.
from random import randint

numbers = [randint(1, 100) for _ in range(100)]
even_count = 0
odd_count = 0
for number in numbers:
    if number % 2 == 0:
        even_count += 1
    else:
        odd_count += 1
print(f"Even numbers: {even_count}, Odd numbers: {odd_count}")


# c) Enhance b) to also sum the odd numbers
odd_sum = 0
odd_count = 0
even_count = 0
for number in numbers:
    if number % 2 == 0:
        even_count += 1
    else:
        odd_count += 1
        odd_sum += number
print(f"Even: {even_count}, Odd: {odd_count}, Sum of odd numbers: {odd_sum}")
```

**Activity 3: Lists and Summing**

Pseudocode:
```
total = 0
For every number in list1:
    If the number is odd:
        add it to total
Print total
```

```python
list1 = [2, 3, 4, 5, 6, 4, 8, 9, 9, 8, 34, 32, 33, 37, 78, 79]
total = 0
for number in list1:
    if number % 2 != 0:
        total += number
print("Total of all odd numbers in the list:", total)   # 175
```

**Activity 4: Counting Vowels**

Pseudocode:
```
For every character in the string:
    If character is a vowel (a, e, i, o, u):
        increment that vowel's counter
Print all five counters
```

```python
text = input("Enter a string: ")
counts = {"a": 0, "e": 0, "i": 0, "o": 0, "u": 0}

for character in text.lower():
    if character in counts:
        counts[character] += 1

print(f"a={counts['a']}, e={counts['e']}, i={counts['i']}, o={counts['o']}, u={counts['u']}")
print("Total vowels:", sum(counts.values()))
```
