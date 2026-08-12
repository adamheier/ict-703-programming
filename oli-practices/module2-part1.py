'''Workshop Module 2 Part 1'''
import unittest

class tax_office:

    def calculate_tax(self, gross_income, number_dependents):
        deductions = 10000 + number_dependents * 3000
        net_income = gross_income - deductions
        tax = net_income * 0.2
        return tax, deductions, net_income

    def __init__(self, name):
        self.name = name


def get_float(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")


def get_non_negative_int(prompt):
    while True:
        try:
            value = int(input(prompt))
            if value < 0:
                print("Please enter a non-negative number.")
            else:
                return value
        except ValueError:
            print("Invalid input. Please enter a whole number.")

class TestTaxOffice(unittest.TestCase):

    def setUp(self):
        self.office = tax_office("Test Office")

    def test_0_dependents_10000(self):
        tax, _, _ = self.office.calculate_tax(10000, 0)
        self.assertAlmostEqual(tax, 0)

    def test_1_dependent_10000(self):
        tax, _, _ = self.office.calculate_tax(10000, 1)
        self.assertAlmostEqual(tax, -600)

    def test_2_dependents_10000(self):
        tax, _, _ = self.office.calculate_tax(10000, 2)
        self.assertAlmostEqual(tax, -1200)

    def test_0_dependents_20000(self):
        tax, _, _ = self.office.calculate_tax(20000, 0)
        self.assertAlmostEqual(tax, 2000)

    def test_1_dependent_20000(self):
        tax, _, _ = self.office.calculate_tax(20000, 1)
        self.assertAlmostEqual(tax, 1400)

    def test_2_dependents_20000(self):
        tax, _, _ = self.office.calculate_tax(20000, 2)
        self.assertAlmostEqual(tax, 800)


if __name__ == "__main__":
    office = tax_office("Tax Office")

    print("=== Tax Calculator ===")
    gross_income = get_float("Enter gross income: ")
    number_dependents = get_non_negative_int("Enter number of dependents: ")

    tax, deductions, net_income = office.calculate_tax(gross_income, number_dependents)

    print("\n--- Tax Summary ---")
    print(f"  Gross Income:      ${gross_income:,.2f}")
    print(f"  Deductions:        ${deductions:,.2f}")
    print(f"  Net Income:        ${net_income:,.2f}")
    print(f"  Tax (20%):         ${tax:,.2f}")
    print(f"  Take-home Pay:     ${gross_income - tax:,.2f}")
