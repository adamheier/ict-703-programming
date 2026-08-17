'''Develop pseudo code and a program that does the following: 
Count the vowels in a given string and then print out how many of each vowel (a, e, i, o, u)'''

text = input("Please enter a string: ")

chars = list(text)

a = 0
e = 0
i = 0
o = 0
u = 0

for char in chars:
    if (char == "a"):
        a += 1
    elif (char == "e"):
        e += 1
    elif (char == "i"):
        i += 1
    elif (char == "o"):
        o += 1
    elif (char == "u"):
        u += 1
    else:
        continue

sum = a + e + i + o + u

print(f"The amount of vowels are: a = {a}, e = {e}, i = {i}, o = {o}, u = {u}")
print(f"The total amount of vowels is: {sum}")