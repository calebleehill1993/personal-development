import numpy as np
from matplotlib import pyplot as plt

# Just taking a high Idaho Estimate (About the National Average)
ANNUAL_HOMEOWNER_INSURANCE = 1200

def annual_pmi(loan_amount, rate):
    return loan_amount * rate

def annual_property_tax(market_value, tax_rate):
    return market_value * tax_rate

def annual_property_maintenance(square_feet):
    return square_feet

def mortgage(principle, i, years):
    monthly_i = i / 12
    months = years * 12

    return (principle * monthly_i * (1 + monthly_i)**months) / ((1 + monthly_i)**months - 1)

def total_interest_paid(principle, i, payment):
    monthly_i = i / 12
    total_interest_paid = 0
    months = 0

    if principle * monthly_i >= payment:
        return 99999999999999999

    current_principle = principle
    while current_principle > 0:
        current_interest = current_principle * monthly_i
        paid_on_principle = payment - current_interest
        total_interest_paid += current_interest
        current_principle -= paid_on_principle
        months += 1

    return {'total_interest': total_interest_paid, 'months': months}

x = np.array([i for i in range(10000, 1000001, 10000)])
y = mortgage(x, .06, 30)

# plt.plot(x, mortgage(x, .06, 30), label='30 years at 6%')
# plt.plot(x, mortgage(x, .04, 30), label='30 years at 4%')
# plt.plot(x, mortgage(x, .06, 15), label='15 years at 6%')
# plt.plot(x, mortgage(x, .04, 15), label='15 years at 4%')
# plt.legend()
# plt.show()

# print(total_interest_paid(400000, .06, mortgage(400000, .06, 30)))

# Basic example of how paying more on your mortgage saves you money
# principle = 400000
# i = .06
# years = 30
# minimum_payment = mortgage(principle, i, years)
#
# x = np.array([minimum_payment * j / 100 for j in range(100, 301)])
# plt.plot(x, np.array([total_interest_paid(principle, i, x_i)['total_interest'] for x_i in x]))
# plt.show()

# Paying more on mortgage has diminishing returns over time and the ammount over the minimum payment
# principle = 400000
# i = .03
# years = 30
# minimum_payment = mortgage(principle, i, years)
#
# x = np.array([j / 100 for j in range(100, 301)])
# plt.plot(x, np.array([(principle + total_interest_paid(principle, i, minimum_payment * x_i)['total_interest']) / principle for x_i in x]))
#
# principle = 400000
# i = .06
# years = 30
# minimum_payment = mortgage(principle, i, years)
#
# x = np.array([j / 100 for j in range(100, 301)])
# plt.plot(x, np.array([(principle + total_interest_paid(principle, i, minimum_payment * x_i)['total_interest']) / principle for x_i in x]))
#
#
# plt.show()




# As the interest rate increases, how does the ammount paid increase?
# principle = 400000
# years = 30
#
# x = np.array([i / 1000 for i in range(1, 101)])
# plt.plot(x, np.array([(principle + total_interest_paid(principle, x_i, mortgage(principle, x_i, years))['total_interest']) / principle for x_i in x]))
#
#
# plt.show()

print(annual_property_tax(400000, .0059))
print(annual_property_maintenance(2000))
print()
