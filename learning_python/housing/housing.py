import pandas as pd
# https://fred.stlouisfed.org/series/MSPUS
housing = pd.read_csv('data/median_house_prices_us.csv', names=['date', 'price'], header=0)
# https://fred.stlouisfed.org/series/MEFAINUSA646N
income = pd.read_csv('data/median_income_us_by_year.csv', names=['date', 'income'], header=0)

size = pd.read_csv('data/median_house_size.csv', names=['date', 'size'], header=0)

housing.head()
income.head()
size.head()

housing_income = pd.merge(pd.merge(housing, income), size, how='left')

housing_income.head()

housing_income.dropna(how='any').head()

housing_income['price_to_income'] = housing_income.price / housing_income.income
housing_income['price_per_sqft'] = housing_income.price / housing_income['size']
housing_income['ppsf_to_income'] = housing_income.iloc[-1, 3] * housing_income.price_per_sqft / housing_income.income
housing_income['year'] = pd.DatetimeIndex(housing_income.date).year


housing_income.plot(x='year', y='price_to_income')

housing_income.plot(x='year', y='price')
housing_income.plot(x='year', y='income')
housing_income.dropna(how='any').plot(x='year', y='size')
housing_income.dropna(how='any').plot(x='year', y='price_per_sqft')
# How many annual incomes to purchase a home with the median sqft from this year.
housing_income.dropna(how='any').plot(x='year', y='ppsf_to_income')
