# Assessment 1 Practice Quiz 3
25 TOTAL POINTS

---

### Question 1 (1 point)
Which is a valid Python variable name?

- [ ] my_var
- [ ] 3var
- [ ] my var
- [ ] True

---

### Question 2 (1 point)
What is printed?

```python
y = 3
if y == 3:
    print("X")
print("Y")
```

- [ ] X only
- [ ] Y only
- [ ] X and Y (on separate lines)
- [ ] Error

---

### Question 3 (1 point)
What is the data type of `"42"`?

- [ ] int
- [ ] float
- [ ] str
- [ ] bool

---

### Question 4 (1 point)
Suppose `word = "Programming"`. What is the value of `word[4]`?

- [ ] g
- [ ] r
- [ ] a
- [ ] m

---

### Question 5 (1 point)
What is stored in `nums`?

```python
nums = [5, 10, 15]
nums.pop()
```

- [ ] [5, 10, 15]
- [ ] [5, 10]
- [ ] [15]
- [ ] Error

---

### Question 6 (1 point)
Which exception is raised?

```python
d = {"a": 1}
print(d["b"])
```

- [ ] KeyError
- [ ] IndexError
- [ ] TypeError
- [ ] NameError

---

### Question 7 (1 point)
Suppose `xs = "abcdefghij"`, which slice produces `"jihgf"`?

- [ ] xs[9:4:-1]
- [ ] xs[4:9:-1]
- [ ] xs[9:4]
- [ ] xs[9::-1]

---

### Question 8 (1 point) — Extended Answer
What error (if any) will the following code produce? Please provide a brief explanation.

```python
try:
    z = [1, 2, 3][5]
except IndexError:
    print("first")
else:
    print("second")
```

*(Write your answer here)*

---

### Question 9 (2 points)
What error (if any) will the following code produce?

```python
age = "25"
years_to_go = 10
future_age = age + years_to_go
print(future_age)
```

**Question 9.1 (1 point)** — What error (if any) will the code produce? Please provide a brief explanation.

*(Write your answer here)*

**Question 9.2 (1 point)** — Provide a correct program.

*(Write your answer here)*

---

### Question 10 (1 point)
Complete the program which prints all numbers divisible by 3 from 1 to 15.

```python
# Print all numbers divisible by 3 from 1 to 15
for i in range(1, 16):
    # Complete the condition
    if ___________________:
        print(i)
```

*(Write your answer here)*

---

### Question 11 (1 point)
What is stored in `result`?

```python
word = "javascript"
result = word[2:6]
```

*(Write your answer here)*

---

### Question 12 (2 points)
Write a Python program that calculates and prints the average of the numbers from 1 to 6.

*(Write your answer here)*

---

### Question 13 (5 points)
The next five questions refer to the following Python program. Write the exact output or value in each answer box.

```python
items = ["pen", "book", "eraser", "bag"]
short_items = []
total_chars = 0

for item in items:
    total_chars = total_chars + len(item)
    if len(item) <= 4:
        short_items.append(item)

last_short = short_items[-1]
```

**Question 13.1 (1 point)** — How many times does the loop execute?

**Question 13.2 (1 point)** — What is the value of `total_chars` after the loop?

**Question 13.3 (1 point)** — What is the final value of `short_items`?

**Question 13.4 (1 point)** — What value is stored in `last_short`?

**Question 13.5 (1 point)** — What is the length of `short_items`?

---

### Question 14 (2 points)
Complete the missing parts of the program.

The following program should ask the user to enter some text and count the number of **digits** in it.

```python
text = input("Enter text: ")
count = 0

for character in text:
    if ______________________________:
        count = ______________________________

print("Number of digits:", count)
```

**Question 14.1 (1 point)** — Fill in the first blank

**Question 14.2 (1 point)** — Fill in the second blank

---

### Question 15 (4 points)
The next four questions refer to the following Python program.

```python
numbers = [12, 24, 36]
total = 0

for num in numbers:
    total = total + num

print(Total)
```

**Question 15.1 (1 point)** — Which line causes the first error?

**Question 15.2 (1 point)** — Why does the last line fail?

**Question 15.3 (1 point)** — After correcting the last line to `print(total)`, what is printed?

**Question 15.4 (1 point)** — How could the loop body be rewritten using an augmented assignment operator?

---

> [!success]- Answer Key (click to expand)
>
> **Q1.** `my_var` — `3var` starts with a digit, `"my var"` contains a space, and `True` is a reserved keyword.
>
> **Q2.** X and Y (on separate lines) — `print("Y")` is not indented, so it always runs after the `if` block, regardless of the condition.
>
> **Q3.** str
>
> **Q4.** r — `word = "Programming"` → P(0) r(1) o(2) g(3) r(4) a(5) m(6) m(7) i(8) n(9) g(10), so `word[4]` is `"r"`.
>
> **Q5.** `[5, 10]` — `.pop()` with no argument removes and returns the *last* element.
>
> **Q6.** KeyError — the key `"b"` does not exist in the dictionary.
>
> **Q7.** `xs[9:4:-1]` — starts at index 9, steps backward by 1, stopping before index 4: indices 9, 8, 7, 6, 5 → `"jihgf"`.
>
> **Q8.** `[1, 2, 3][5]` raises an `IndexError` (the list only has indices 0–2). This error **is** caught by `except IndexError`, so `"first"` is printed. No crash occurs.
>
> **Q9.1.** `TypeError: can only concatenate str (not "int") to str`. `age` is a string and `years_to_go` is an int, so `+` cannot combine them directly.
>
> **Q9.2.**
> ```python
> age = "25"
> years_to_go = 10
> future_age = int(age) + years_to_go
> print(future_age)
> ```
>
> **Q10.** `i % 3 == 0`
>
> **Q11.** `"vasc"` — `word = "javascript"` → j(0) a(1) v(2) a(3) s(4) c(5) r(6) i(7) p(8) t(9), so `word[2:6]` is indices 2–5: `"vasc"`.
>
> **Q12.**
> ```python
> total = 0
> for i in range(1, 7):
>     total = total + i
> average = total / 6
> print(average)
> ```
> Output: `3.5`
>
> **Q13.1.** 4 (the loop runs once per item in `items`)
>
> **Q13.2.** 16 — lengths: pen=3, book=4, eraser=6, bag=3 → 3+4+6+3 = 16
>
> **Q13.3.** `["pen", "book", "bag"]` (eraser has 6 letters, which is longer than 4, so it's excluded)
>
> **Q13.4.** `"bag"`
>
> **Q13.5.** 3
>
> **Q14.1.** `character.isdigit()`
>
> **Q14.2.** `count + 1`
>
> **Q15.1.** The last line (`print(Total)`)
>
> **Q15.2.** `NameError: name 'Total' is not defined`. Python is case-sensitive — the variable was created as `total` (lowercase), not `Total`.
>
> **Q15.3.** `72` (12 + 24 + 36)
>
> **Q15.4.** `total += num`
