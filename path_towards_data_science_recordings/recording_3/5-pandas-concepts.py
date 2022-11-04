################################################################################
# 5 Things I learned this week
# 1. df.apply
# 2. pd.cut
# 3. df.pivot_table
# 4. joining tables
# 5. Reading several csv files into one DataFrame using glob library
################################################################################

################################################################################
# ATOM PACKAGES
# Hydrogen 2.16.3
# atom-beautify 0.33.4
#
# Python Version 3.9.5
# IPython3 Kernel
################################################################################

################################################################################
# IMPORTS
import pandas as pd # Version 1.2.4
import numpy as np # Version 1.20.3
import seaborn as sns # Version 0.11.2
from glob import glob # Python Standard Library Package for file finding
################################################################################

# Titanic dataset from Kaggle
titanic = pd.read_csv('http://bit.ly/kaggletrain')
titanic.head()

# 1. df.apply()

# $1 in 1912 is $29.81 in 2022 adjusted for inflation
titanic['2022Fare'] = titanic.Fare.apply(lambda x: round(x * 29.81, 2))
titanic.head()


# 2. pd.cut() to group continuous columns

# By default the bins are exclusive of the left and inclusive or the right.
# We can change that to be inclusive of the left and exclusive of the right.
titanic['AgeGroup'] = pd.cut(titanic.Age, bins=[0, 18, 30, 99], labels=['child', 'young adult', 'adult'], include_lowest=True, right=False)
titanic.head()


# 3. Pivot tables
titanic.pivot_table(index='Sex', columns='Pclass', values='2022Fare', aggfunc='mean', margins=True)
titanic.pivot_table(index='Sex', columns='AgeGroup', values='2022Fare', aggfunc='mean', margins=True)

# 4. Joins in pandas
A = pd.DataFrame({'color': ['green', 'yellow', 'red'], 'num': [1, 2, 3]})
B = pd.DataFrame({'Color': ['green', 'yellow', 'pink'], 'size': ['S', 'M', 'L']})
A
B

# Merge on matching color
# Inner is default and must be found in both tables
pd.merge(A, B, how='inner', left_on='color', right_on='Color')

# All keys are included
pd.merge(A, B, how='outer', left_on='color', right_on='Color')

# Include everything from left
pd.merge(A, B, how='left', left_on='color', right_on='Color')

# Include everything from right
pd.merge(A, B, how='right', left_on='color', right_on='Color')


# 5. Reading several csv files into one DataFrame using glob library

# This will grab all the of the stock csv files
stock_files = sorted(glob('stocks/*.csv'))
stock_files

# concatenating all the CSVs as they are read in.
faang_stocks = pd.concat((pd.read_csv(file) for file in stock_files), ignore_index=True)
faang_stocks
sns.lineplot(x='Date', y='Close', data=faang_stocks, hue='Company')
