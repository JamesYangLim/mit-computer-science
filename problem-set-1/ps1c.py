
# annual_salary = float(input("What is your annual salary? "))

annual_salary = 10000

total_cost = 1000000
semi_annual_raise = 0.07

months_per_year = 12
investment_return = 0.04
portion_down_payment = 0.25

down_payment = portion_down_payment * total_cost
monthly_salary = annual_salary / months_per_year

lower_bound = 0
upper_bound = 10000
mid = 0

savings_offset = 100
target_month_count = 36

steps = 0
current_savings = 0
portion_saved = 0.0

while(100 < abs(current_savings - down_payment)):

    temp_annual_salary = annual_salary
    temp_monthly_salary = monthly_salary

    steps = steps + 1

    mid = int((upper_bound - lower_bound) / 2) + lower_bound
    portion_saved = mid / 10000.0

    # print(mid)
    # print(portion_saved)

    current_savings = 0
    monthly_saved = portion_saved * temp_monthly_salary

    for iMonth in range(target_month_count):

        if (iMonth % 6 == 0):
            temp_annual_salary += (temp_annual_salary * semi_annual_raise)
            temp_monthly_salary = temp_annual_salary / months_per_year
            monthly_saved = portion_saved * temp_monthly_salary

        monthly_investment_return = (investment_return * current_savings) / months_per_year
        current_savings = current_savings + monthly_saved + monthly_investment_return


    # print(current_savings)

    if (current_savings < down_payment):
        lower_bound = mid
    else:
        upper_bound = mid

    if (upper_bound - lower_bound == 1):
        print("It is not possible to pay the down payment in three years.")
        break
    
    # print("lower_bound:", lower_bound, "upper_bound:", upper_bound)
    assert(lower_bound < upper_bound)

print("Best savings rate:", portion_saved)
print("Steps in bisection search:", steps)
print("Savings:", current_savings)
print("Down payment:", down_payment)

