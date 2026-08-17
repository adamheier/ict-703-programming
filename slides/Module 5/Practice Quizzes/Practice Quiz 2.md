# Assessment 1 Practice Quiz 2
25 TOTAL POINTS

---

### Question 1 (1 point)
Which is a valid Python variable name?

- [ ] 2total
- [x] total_2
- [ ] total-2
- [ ] class

---

### Question 2 (1 point)
What is printed?

```python
x = 7
if x > 10:
    print("A")
elif x > 5:
    print("B")
else:
    print("C")
```

- [ ] A
- [x] B
- [ ] C
- [ ] Nothing

---

### Question 3 (1 point)
What is the data type of `True`?

- [ ] int
- [ ] float
- [ ] str
- [x] bool

---

### Question 4 (1 point)
Suppose `word = "Coding"`. What is the value of `word[2]`?

- [ ] C
- [ ] o
- [x] d
- [ ] n

---

### Question 5 (1 point)
What is stored in `fruits`?

```python
fruits = ["apple", "banana", "cherry"]
fruits.remove("banana")
```

- [ ] ["apple", "banana", "cherry"]
- [x] ["apple", "cherry"]
- [ ] ["banana"]
- [ ] Error

---

### Question 6 (1 point)
Which exception is raised?

```python
numbers = [1, 2, 3]
print(numbers[5])
```

- [x] IndexError
- [ ] KeyError
- [ ] TypeError
- [ ] ValueError

---

### Question 7 (1 point)
Suppose `xs = "0123456789"`, which slice produces `"8642"`?

- [x] xs[8:0:-2]
- [ ] xs[0:8:2]
- [ ] xs[8::-2]
- [ ] xs[2:8:2]

---

### Question 8 (1 point) — Extended Answer
What error (if any) will the following code produce? Please provide a brief explanation.

```python
try:
    y = 10 / 0
except ValueError:
    print("first")
else:
    print("second")
```

*(Write your answer here)*

---

### Question 9 (2 points)
What error (if any) will the following code produce?

```python
score1 = "85"
score2 = 90
total_score = score1 + score2
print(total_score)
```

**Question 9.1 (1 point)** — What error (if any) will the code produce? Please provide a brief explanation.

*(Write your answer here)*

**Question 9.2 (1 point)** — Provide a correct program.

*(Write your answer here)*

---

### Question 10 (1 point)
Complete the program which prints all odd numbers from 1 to 10.

```python
# Print all odd numbers from 1 to 10
for i in range(1, 11):
    # Complete the condition
    if ___________________:
        print(i)
```

*(Write your answer here)*

---

### Question 11 (1 point)
What is stored in `result`?

```python
word = "abcdef"
result = word[::-1]
```

*(Write your answer here)*

---

### Question 12 (2 points)
Write a Python program that calculates and prints the product of the numbers from 1 to 4 (i.e. 1×2×3×4).

*(Write your answer here)*

---

### Question 13 (5 points)
The next five questions refer to the following Python program. Write the exact output or value in each answer box.

```python
scores = [55, 82, 91, 40]
passed = []
total_points = 0

for score in scores:
    total_points = total_points + score
    if score >= 50:
        passed.append(score)

first_pass = passed[0]
```

**Question 13.1 (1 point)** — How many times does the loop execute?

**Question 13.2 (1 point)** — What is the value of `total_points` after the loop?

**Question 13.3 (1 point)** — What is the final value of `passed`?

**Question 13.4 (1 point)** — What value is stored in `first_pass`?

**Question 13.5 (1 point)** — What is the length of `passed`?

---

### Question 14 (2 points)
Complete the missing parts of the program.

The following program should ask the user to enter a word and count the number of **vowels** in the word. You may assume the user enters only lowercase letters (a–z).

```python
word = input("Enter a word: ")
count = 0

for character in word:
    if ______________________________:
        count = ______________________________

print("Number of vowels:", count)
```

**Question 14.1 (1 point)** — Fill in the first blank

**Question 14.2 (1 point)** — Fill in the second blank

---

### Question 15 (4 points)
The next four questions refer to the following Python program.

```python
values = [5, 10, 15]
total = "0"

for value in values:
    total = total + value

print(values[3])
```

**Question 15.1 (1 point)** — Which line causes the first error?

**Question 15.2 (1 point)** — Why does line 5 fail?

**Question 15.3 (1 point)** — After correcting line 2 to `total = 0`, what error occurs next?

**Question 15.4 (1 point)** — How should the last line be corrected to print the last item?

---

> [!success]- Answer Key (click to expand)
>
> **Q1.** `total_2` — `2total` starts with a digit, `total-2` contains a hyphen, and `class` is a reserved keyword. All three are invalid.
>
> **Q2.** B — `x = 7` is not greater than 10, but it is greater than 5, so the `elif` branch runs.
>
> **Q3.** bool
>
> **Q4.** d — `word = "Coding"` → indices: C(0) o(1) d(2) i(3) n(4) g(5), so `word[2]` is `"d"`.
>
> **Q5.** `["apple", "cherry"]` — `.remove("banana")` deletes the first matching value.
>
> **Q6.** IndexError — the list only has indices 0–2; index 5 doesn't exist.
>
> **Q7.** `xs[8:0:-2]` — starts at index 8, steps backward by 2, stopping before index 0: indices 8, 6, 4, 2 → `"8642"`.
>
> **Q8.** The code raises a `ZeroDivisionError` (division by zero). This is **not** caught by `except ValueError`, so the program crashes with an unhandled `ZeroDivisionError`. Neither "first" nor "second" is printed.
>
> **Q9.1.** `TypeError: can only concatenate str (not "int") to str`. `score1` is a string and `score2` is an int, so `+` cannot combine them directly.
>
> **Q9.2.**
> ```python
> score1 = "85"
> score2 = 90
> total_score = int(score1) + score2
> print(total_score)
> ```
>
> **Q10.** `i % 2 != 0` (equivalently `i % 2 == 1`)
>
> **Q11.** `"fedcba"`
>
> **Q12.**
> ```python
> product = 1
> for i in range(1, 5):
>     product = product * i
> print(product)
> ```
> Output: `24`
>
> **Q13.1.** 4 (the loop runs once per item in `scores`)
>
> **Q13.2.** 268 (55 + 82 + 91 + 40)
>
> **Q13.3.** `[55, 82, 91]` (40 is excluded because it's below 50)
>
> **Q13.4.** 55
>
> **Q13.5.** 3
>
> **Q14.1.** `character in "aeiou"`
>
> **Q14.2.** `count + 1`
>
> **Q15.1.** Line 5 (`total = total + value`)
>
> **Q15.2.** `total` is a string (`"0"`) and `value` is an int; Python cannot add a `str` and an `int` with `+`, raising a `TypeError`.
>
> **Q15.3.** `IndexError` — `values` only has indices 0–2 (3 elements), but `values[3]` tries to access a fourth element that doesn't exist.
>
> **Q15.4.** `print(values[-1])` (or `print(values[2])`)
