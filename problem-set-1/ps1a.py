
annual_salary = float(input("What is your annual salary? "))
portion_saved = float(input("What is the portion of the salary you saved? "))
total_cost = float(input("What is the cost of your dream house? "))

months_per_year = 12
investment_return = 0.04
portion_down_payment = 0.25

down_payment = portion_down_payment * total_cost
monthly_salary = annual_salary / months_per_year
monthly_saved = portion_saved * monthly_salary

current_savings = 0

month_count = 1;
while(current_savings < down_payment):
    monthly_investment_return = (investment_return * current_savings) / months_per_year
    current_savings = current_savings + monthly_saved + monthly_investment_return
    month_count = month_count + 1

print("Number of months", month_count)