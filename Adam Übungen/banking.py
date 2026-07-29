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

'''
print ("Hello and welcome to the banking program")
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

print("Hello and welcome to the banking program")
starting_balance = float(input("Please enter your starting balance: "))

anzahl = int(input("Wie viele Transaktionen möchtest du durchführen? "))

running_balance = starting_balance
transaktionen = []  # speichert (typ, betrag, saldo_danach) für jede Transaktion

for i in range(anzahl):
    typ = input(f"Transaktion {i + 1}: Einzahlung oder Abhebung? (e/a): ").strip().lower()
    betrag = float(input(f"Transaktion {i + 1}: Betrag: "))

    if typ == "e":
        running_balance += betrag
        transaktionen.append(("Einzahlung", betrag, running_balance))
    elif typ == "a":
        running_balance -= betrag
        transaktionen.append(("Abhebung", betrag, running_balance))
    else:
        print("Ungültige Eingabe, Transaktion wird übersprungen.")

print("Starting balance:", starting_balance)
for typ, betrag, saldo in transaktionen:
    print(f"{typ}: {betrag}  Running Balance: {saldo}")
print("Final balance:", running_balance)
