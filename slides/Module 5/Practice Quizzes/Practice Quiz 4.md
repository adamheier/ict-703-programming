# Assessment 1 Practice Quiz 4
25 TOTAL POINTS

---

### Question 1 (1 point)
Which is a valid Python variable name?

- [ ] _score
- [ ] 2nd_score
- [ ] second-score
- [ ] return

---

### Question 2 (1 point)
What is printed?

```python
n = 4
while n > 0:
    print(n)
    n = n - 1
```

- [ ] 4 3 2 1
- [ ] 4 3 2 1 0
- [ ] 1 2 3 4
- [ ] Error

---

### Question 3 (1 point)
What is the data type of `None`?

- [ ] int
- [ ] str
- [ ] bool
- [ ] NoneType

---

### Question 4 (1 point)
Suppose `word = "keyboard"`. What is the value of `word[5]`?

- [ ] o
- [ ] a
- [ ] r
- [ ] d

---

### Question 5 (1 point)
What is stored in `colors`?

```python
colors = ["red", "green"]
colors.insert(1, "blue")
```

- [ ] ["red", "green", "blue"]
- [ ] ["red", "blue", "green"]
- [ ] ["blue", "red", "green"]
- [ ] Error

---

### Question 6 (1 point)
Which exception is raised?

```python
x = "5" + 5
```

- [ ] TypeError
- [ ] ValueError
- [ ] NameError
- [ ] SyntaxError

---

### Question 7 (1 point)
Suppose `xs = "0123456789"`, which slice produces `"1357"`?

- [ ] xs[1:8:2]
- [ ] xs[8:1:-2]
- [ ] xs[1::2]
- [ ] xs[2:8:2]

---

### Question 8 (1 point) — Extended Answer
What error (if any) will the following code produce? Please provide a brief explanation.

```python
try:
    n = int("3.5")
except ValueError:
    print("first")
except TypeError:
    print("second")
```

*(Write your answer here)*

---

### Question 9 (2 points)
What error (if any) will the following code produce?

```python
temperature = 20
unit = "C"
message = "Temperature: " + temperature + unit
print(message)
```

**Question 9.1 (1 point)** — What error (if any) will the code produce? Please provide a brief explanation.

*(Write your answer here)*

**Question 9.2 (1 point)** — Provide a correct program.

*(Write your answer here)*

---

### Question 10 (1 point)
Complete the program which prints all numbers from 1 to 20 that are NOT divisible by 5.

```python
# Print all numbers from 1 to 20 that are not divisible by 5
for i in range(1, 21):
    # Complete the condition
    if ___________________:
        print(i)
```

*(Write your answer here)*

---

### Question 11 (1 point)
What is stored in `result`?

```python
word = "sunshine"
result = word[1:5]
```

*(Write your answer here)*

---

### Question 12 (2 points)
Write a Python program that calculates and prints how many of the numbers from 1 to 20 are even.

*(Write your answer here)*

---

### Question 13 (5 points)
The next five questions refer to the following Python program. Write the exact output or value in each answer box.

```python
temps = [15, 22, 8, 30, 19]
warm_days = []
total_temp = 0

for temp in temps:
    total_temp = total_temp + temp
    if temp >= 20:
        warm_days.append(temp)

coldest_warm = warm_days[0]
```

**Question 13.1 (1 point)** — How many times does the loop execute?

**Question 13.2 (1 point)** — What is the value of `total_temp` after the loop?

**Question 13.3 (1 point)** — What is the final value of `warm_days`?

**Question 13.4 (1 point)** — What value is stored in `coldest_warm`?

**Question 13.5 (1 point)** — What is the length of `warm_days`?

---

### Question 14 (2 points)
Complete the missing parts of the program.

The following program should ask the user to enter some text and count the number of **uppercase letters** in it.

```python
text = input("Enter text: ")
count = 0

for character in text:
    if ______________________________:
        count = ______________________________

print("Number of uppercase letters:", count)
```

**Question 14.1 (1 point)** — Fill in the first blank

**Question 14.2 (1 point)** — Fill in the second blank

---

### Question 15 (4 points)
The next four questions refer to the following Python program.

```python
values = [10, 20, 30]
index = 0

while index <= len(values):
    print(values[index])
    index = index + 1
```

**Question 15.1 (1 point)** — Which line causes the first error, and at what value of `index`?

**Question 15.2 (1 point)** — Why does that line fail?

**Question 15.3 (1 point)** — After correcting the `while` line to `while index < len(values):`, what is printed?

**Question 15.4 (1 point)** — How could this loop be rewritten using a `for` loop instead, to avoid this type of bug entirely?

---

> [!success]- Answer Key (click to expand)
>
> **Q1.** `_score` — `2nd_score` starts with a digit, `second-score` contains a hyphen, and `return` is a reserved keyword.
>
> **Q2.** 4 3 2 1 — the loop prints `n` then decrements; it stops as soon as `n` is no longer greater than 0, so 0 is never printed.
>
> **Q3.** NoneType
>
> **Q4.** a — `word = "keyboard"` → k(0) e(1) y(2) b(3) o(4) a(5) r(6) d(7), so `word[5]` is `"a"`.
>
> **Q5.** `["red", "blue", "green"]` — `.insert(1, "blue")` inserts `"blue"` at index 1, shifting `"green"` right.
>
> **Q6.** TypeError — `can only concatenate str (not "int") to str`; a string and an int cannot be combined with `+`.
>
> **Q7.** `xs[1:8:2]` — starts at index 1, steps forward by 2, stopping before index 8: indices 1, 3, 5, 7 → `"1357"`.
>
> **Q8.** `int("3.5")` raises a `ValueError` because `"3.5"` is not a valid integer literal (it contains a decimal point). This **is** caught by `except ValueError`, so `"first"` is printed.
>
> **Q9.1.** `TypeError: can only concatenate str (not "int") to str`. `temperature` is an int and cannot be directly concatenated to a string with `+`.
>
> **Q9.2.**
> ```python
> temperature = 20
> unit = "C"
> message = "Temperature: " + str(temperature) + unit
> print(message)
> ```
>
> **Q10.** `i % 5 != 0`
>
> **Q11.** `"unsh"` — `word = "sunshine"` → s(0) u(1) n(2) s(3) h(4) i(5) n(6) e(7), so `word[1:5]` is indices 1–4: `"unsh"`.
>
> **Q12.**
> ```python
> count = 0
> for i in range(1, 21):
>     if i % 2 == 0:
>         count = count + 1
> print(count)
> ```
> Output: `10`
>
> **Q13.1.** 5 (the loop runs once per item in `temps`)
>
> **Q13.2.** 94 (15 + 22 + 8 + 30 + 19)
>
> **Q13.3.** `[22, 30, 19]` (15 and 8 are excluded because they're below 20)
>
> **Q13.4.** 22
>
> **Q13.5.** 3
>
> **Q14.1.** `character.isupper()`
>
> **Q14.2.** `count + 1`
>
> **Q15.1.** The line `print(values[index])`, when `index` is 3.
>
> **Q15.2.** `IndexError` — `values` only has indices 0–2 (3 elements), but the `while` condition allows `index` to reach 3, and `values[3]` doesn't exist.
>
> **Q15.3.** `10`, `20`, `30` (each on its own line), and the loop ends without error.
>
> **Q15.4.**
> ```python
> for value in values:
>     print(value)
> ```
