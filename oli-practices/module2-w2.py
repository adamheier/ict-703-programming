'''Workshop Module 2 Part 2'''

import sys
import tty
import termios


def get_key():
    fd = sys.stdin.fileno()
    old = termios.tcgetattr(fd)
    try:
        tty.setraw(fd)
        return sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old)


class atm_machine:

    def __init__(self, name, starting_balance):
        self.name = name
        self.balance = starting_balance

    def deposit(self, amount):
        self.balance += amount
        print(f"  Deposit:    +${amount:,.2f}  |  Balance: ${self.balance:,.2f}")

    def withdraw(self, amount):
        self.balance -= amount
        print(f"  Withdrawal: -${amount:,.2f}  |  Balance: ${self.balance:,.2f}")

    def statement(self):
        print(f"  Final Balance: ${self.balance:,.2f}")


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    print("== ATM Statement ==")
    print("Hallo Oli, I'm your ATM and am showing your bank statement\n")

    starting_balance = get_float("Enter your balance to start with: ")
    atm = atm_machine("ATM Machine", starting_balance)
    print(f"  Starting Balance:   ${starting_balance:,.2f}\n")

    while True:
        print("What would you like to do?  [d] Deposit  [w] Withdraw  [q] Quit")
        choice = get_key()
        print(choice)

        match choice:
            case "d":
                atm.deposit(get_float("  Amount to deposit: "))
            case "w":
                atm.withdraw(get_float("  Amount to withdraw: "))
            case "q":
                break
            case _:
                print("  Invalid choice. Please press d, w, or q.\n")
                continue
        print()

    print()
    atm.statement()
