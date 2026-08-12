'''Write a program that creates a list of 100 random numbers and then print out the amount
of odd and even numbers.'''

from random import randint

numbers = [randint(1,100) for _ in range(100)]

even = []
odd = []

for i in numbers:
    if (i % 2 == 0):
        even.append(i)
    else:
        odd.append(i)

print(f'Amount even numbers: {len(even)} -> the sum is {sum(even)}')
print(f'Amount odd numbers: {len(odd)} -> the sum is {sum(odd)}')

