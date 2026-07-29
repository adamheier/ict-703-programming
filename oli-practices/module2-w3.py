'''Workshop Module 2 Part 3'''
import math

def print_formatted_poem():
    """Print the Twinkle Twinkle Little Star poem, one phrase per line."""
    poem = (
        "Twinkle, twinkle, little star,\n"
        "How I wonder what you are!\n"
        "Up above the world so high,\n"
        "Like a diamond in the sky.\n"
        "Twinkle, twinkle, little star,\n"
        "How I wonder what you are"
    )
    print(poem)

def circle_area(radius):
    """Return the area of a circle given its radius."""
    return math.pi * radius ** 2

def reverse_name(first, last):
    """Return the name in 'last first' order."""
    return f"{last} {first}"

def comma_string_to_list(s):
    """Convert a comma-separated string of values into a list of stripped strings."""
    return [x.strip() for x in s.split(",")]

def file_extension(filename):
    """Return the file extension of filename, or an empty string if none."""
    return filename.rsplit(".", 1)[-1] if "." in filename else ""

def n_nn_nnn(n):
    """Return the sum of n, nn (n repeated twice), and nnn (n repeated three times)."""
    nn = int(str(n) * 2)
    nnn = int(str(n) * 3)
    return n + nn + nnn

def print_docstrings():
    """Print the name and docstring of a selection of Python built-in functions."""
    for fn in (print, len, range, input, int, str, float, list, dict, type):
        print(f"--- {fn.__name__} ---")
        print(fn.__doc__)
        print()


if __name__ == "__main__":

    print("=== Exercise 1: Print Formatting ===")
    print_formatted_poem()

    print("\n=== Exercise 2: Area of a Circle ===")
    r = float(input("Enter radius: "))
    print(f"r = {r}")
    print(f"Area = {circle_area(r)}")

    print("\n=== Exercise 3: Name Reversed ===")
    first = input("Enter first name: ")
    last = input("Enter last name: ")
    print(reverse_name(first, last))

    print("\n=== Exercise 4: Print a List ===")
    raw = input("Enter comma-separated numbers: ")
    print(comma_string_to_list(raw))

    print("\n=== Exercise 5: File Extension ===")
    filename = input("Enter filename: ")
    print(file_extension(filename))

    print("\n=== Exercise 6: Compute n+nn+nnn ===")
    n = int(input("Enter an integer n: "))
    print(f"n+nn+nnn = {n_nn_nnn(n)}")

    print("\n=== Exercise 7: Docstrings ===")
    print_docstrings()
