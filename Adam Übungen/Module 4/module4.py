'''

inputString = input("Please enter a string: ")

print(len(inputString))
print(inputString.split("i"))
print(inputString.upper())
print(inputString[9])
print(inputString.find("rule"))

'''








'''
inputString = input("Please enter a string: ")
reversedString = inputString[::-1]
print("Original string:", inputString)
print("Reversed string:", reversedString)
'''


'''Write a program that creates a list of 100 random numbers and then print out the amount of odd and even numbers.'''

import random

l = []
even = 0
even_sum = 0
odd = 0
odd_sum = 0

for i in range(100):
    l.append(random.randint(1, 99))
print(l)

for random_number in l:
    if random_number % 2 == 0:
        even += 1
        even_sum += random_number
    else:
        odd += 1
        odd_sum += random_number

print("The amount of even numbers is:" , even, "The amount of odd numbers is:", odd)
print("The sum of even numbers is:" , even_sum, "The sum of odd numbers is:", odd_sum)
