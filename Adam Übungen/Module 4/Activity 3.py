'''Develop pseudo code and a program that does the following: 
Print the total of all odd numbers in the following list list1 = [2,3,4,5,6,4,8,9,9,8,34,32,33,37,78,79]'''

'''list1 has odd and even numbers.
odd_counter = 0
For all the number in list 1:
    If the number is odd += 1
    Else the number is even = skip counter
print the total odd numbers'''



list1 = [2,3,4,5,6,4,8,9,9,8,34,32,33,37,78,79]
odd_counter = 0
for i in list1:
    if  (i % 2 != 0):
        odd_counter += 1
    else:
        continue
print("The total odd numbers in the list are:", odd_counter)