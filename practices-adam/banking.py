'''
1. Conversion
For the tasks below make sure you gather the input with explanation and provide the output with
explanation.
a) Write a program that takes the input as a string and converts it to a number.
b) Write a program that takes a number and converts it to a string
c) Write a program that takes 2 numbers and outputs the sum, difference, product, division,
quotient, remainder, exponentiation.
2. Banking
Write a program that asks for the user’s bank balance and then does 5 transactions (3 deposits
and 2 withdrawals) – asking the user each time.
Print out a statement of the account (beginning balance, each transaction with a running balance
and the final balance.
'''

'''
PseudoCode:

Greet User
Ask the starting balance
Ask Deposit 1
Ask Deposit 2
Ask Deposit 3
Ask Withdrawal 1
Ask Withdrawal 2

Print a statement showing the starting balance, then all the transactions with a running balance.
'''


'''print ("Hello and welcome to the banking program")
starting_balance = float(input("Please enter your starting balance: "))

deposit_1 = float(input("Please enter your first deposit amount: "))
deposit_2 = float(input("Please enter your second deposit amount: "))
deposit_3 = float(input("Please enter your third deposit amount: "))
withdrawal_1 = float(input("Please enter your first withdrawal amount: "))
withdrawal_2 = float(input("Please enter your second withdrawal amount: "))



print ("Starting balance", starting_balance)
print ("Deposit 1", deposit_1, "Running Balance: ", starting_balance + deposit_1)
print ("Deposit 2", deposit_2, "Running Balance: ", starting_balance + deposit_1 + deposit_2)
print ("Deposit 3", deposit_3, "Running Balance: ", starting_balance + deposit_1 + deposit_2 + deposit_3)
print ("Withdrawal 1", withdrawal_1, "Running Balance: ", starting_balance + deposit_1 + deposit_2 + deposit_3 - withdrawal_1)
print ("Withdrawal 2", withdrawal_2, "Running Balance: ", starting_balance + deposit_1 + deposit_2 + deposit_3 - withdrawal_1 - withdrawal_2)
'''

'''Enhance the bank program from module 2. Start by asking the person’s name, account number
and starting balance as before. Then repeatedly ask the user for their command. They can ask to
“deposit”, “withdraw”, “balance” or “stop”. For the first 2 you need to then ask the amount and
update the balance. Keep asking until the person says “stop”.'''

print ("Hello and welcome to the banking program")

user_name = str(input("Please enter your name: "))
account_number = int(input("Please enter your account number: "))
starting_balance = float(input("Please enter your starting balance: "))
while True:
    command = str(input("Please enter your command (deposit, withdraw, balance, stop)"))
    if command == "deposit":
        deposit_amount = float(input("Please enter the amount to deposit: "))
        starting_balance += deposit_amount
        print("Your new balance is: ", starting_balance)
    elif command == "withdraw":
        withdrawal_amount == ""

















    command = str(input("Please enter your command (deposit, withdraw, balance, stop): "))
    if command == "deposit":
        deposit_amount = float(input("Please enter the amount to deposit: "))
        starting_balance += deposit_amount
        print ("Deposit successful. New balance: ", starting_balance)
    elif command == "withdraw":
        withdrawal_amount = float(input("Please enter the amount to withdraw: "))
        if withdrawal_amount > starting_balance:
            print ("Insufficient funds. Current balance: ", starting_balance)
        else:
            starting_balance -= withdrawal_amount
            print ("Withdrawal successful. New balance: ", starting_balance)
    elif command == "balance":
        print ("Current balance: ", starting_balance)
    elif command == "stop":
        print ("Thank you for using the banking program. Goodbye!")
        break
    else:
        print ("Invalid command. Please try again.")