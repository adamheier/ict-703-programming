''' 
Task: An income tax calculator with the following tax laws:
1. All taxpayers are charged a flat tax rate of 20%
2. All taxpayers are allowed a $10,000 standard deduction
3. For each dependent, a taxpayer is allowed an additional $3,000 deduction.
4. Gross income must be entered to the nearest cent.
5. The income tax is expressed as a decimal number.
Another part of analysis determines what information the user will have to provide. In this case, the user inputs are gross income and number of dependents. The program calculates the income tax based on the inputs and the tax law and then displays the income tax. Below is the proposed output. Characters in italics indicate user inputs. The proram prints the rest.


Pseudocode: 
Dependent deduction = 3000
Standard deduction = 10000
1. User enters their gross income and number of dependents.
2. Count number of dependents. Deduct sum of dependent deduction from gross income.
3. Deduct standard deduction from the result of step 2.
4. Charge a flat tax rate of 20% on the result of step 3.
5. If the tax < 0, set tax to 0.
Print the tax as a decimal number.
'''

print ("Welcome to the Income Tax Calculator")
gross_income = float(input("Please enter your gross income: "))
num_dependents = int(input("Please enter the number of dependents: "))

def calculate_income_tax(gross_income, num_dependents):
    standard_deduction = 10000
    dependent_deduction = 3000
    flat_tax_rate = 0.20

    total_dependent_deduction = num_dependents * dependent_deduction
    total_deductions = standard_deduction + total_dependent_deduction
    net_income = gross_income - total_deductions
    income_tax = net_income * flat_tax_rate
    if income_tax < 0:
        income_tax = 0
    return standard_deduction, total_dependent_deduction, total_deductions, net_income, income_tax

standard_deduction, total_dependent_deduction, total_deductions, net_income, income_tax = calculate_income_tax(gross_income, num_dependents)

print("Standard deduction:", standard_deduction)
print("Dependent deduction:", total_dependent_deduction)
print("Total deductions:", total_deductions)
print("Net income:", net_income)
print("Income tax:", income_tax)


