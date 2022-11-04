import pandas as pd
import numpy as np

# Things I learned this week
# 1. * df.apply
# 2. display options for pandas
# 3. how to copy DataFrames correctly
# 4. * joining tables
# 5. * pd.cut
# 6. * df.pivot_table
# 7. splitting a string column into multiple columns
# 8. * Reading several csv files into one DataFrame using glob library
# 9. filling na values

ufo = pd.read_csv('http://bit.ly/uforeports')
drinks = pd.read_csv('http://bit.ly/drinksbycountry')
movies = pd.read_csv('http://bit.ly/imdbratings')
train = pd.read_csv('http://bit.ly/kaggletrain')

# Formatting DataFrames for display
pd.set_option('display.max_rows', None)
pd.set_option('display.max_colwidth', 1000)
pd.set_option('display.float_format', '{:.2f}'.format)
pd.reset_option('all')

# Applying functions to all rows
train['name_length'] = train.Name.apply(len)

# Copying a DataFrame the right way
top_movies = movies.loc[movies.star_rating >= 9, :].copy()


# Joins in pandas
A = pd.DataFrame({'color': ['green', 'yellow', 'red'], 'num': [1, 2, 3]})
B = pd.DataFrame({'color': ['green', 'yellow', 'pink'], 'size': ['S', 'M', 'L']})

A
B

# Merge on matching color
# Inner is default and must be found in both tables
pd.merge(A, B, how='inner')

# All keys are included
pd.merge(A, B, how='outer')

# Include everything from left
pd.merge(A, B, how='left')

# Include everything from right
pd.merge(A, B, how='right')


train.loc[train.Age == 18].head()
# By default the bins are exclusive of the left and inclusive or the right.
# We can change that to be inclusive of the left and exclusive of the right.
train['age_group'] = pd.cut(train.Age, bins=[0, 18, 25, 99], labels=['child', 'young adult', 'adult'], include_lowest=True, right=False)

train.pivot_table(index='Sex', columns='Pclass', values='Fare', aggfunc='mean', margins=True)

train.Name.str.split(',', expand=True)

# This is a library that gets a list of file names following a pattern
from glob import glob

# This will grab all the of the stocks csvs
stock_files = sorted(glob('stocks/*.csv'))
stock_files

faang_stocks = pd.concat((pd.read_csv(file) for file in stock_files), ignore_index=True)
faang_stocks.head()

# This is used to convert dtypes to numerics where we coerce the errors into na.
# Then we fill the na as 0. So any errors in the conversion will result in 0.
pd.to_numeric(df.col_three, errors='coerce').fillna(0)
