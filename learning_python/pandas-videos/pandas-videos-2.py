import pandas as pd
import numpy as np

# Video #33 - 4 new time-saving tricks in pandas

df = pd.DataFrame([[12, 25, 2017, 10], [1, 15, 2018, 11]],
            columns=['month', 'day', 'year', 'hour'])
df
# Uses the names to create the series.
pd.to_datetime(df)

pd.to_datetime(df[['month', 'day', 'year']])

drinks = pd.read_csv('http://bit.ly/drinksbycountry')
drinks.head()
drinks.dtypes

# New way to change dtypes
drinks = pd.read_csv('http://bit.ly/drinksbycountry', dtype={'continent': 'category'})
drinks.dtypes

# Convert the data type of multiple columns at once
drinks = pd.read_csv('http://bit.ly/drinksbycountry')
drinks = drinks.astype({'beer_servings': 'float', 'spirit_servings': 'float'})
drinks.dtypes

drinks.groupby('continent').beer_servings.mean()

drinks.groupby('continent').beer_servings.agg(['mean', 'min', 'max'])

drinks.beer_servings.agg(['mean', 'min', 'max'])

drinks.agg(['mean', 'min', 'max'])

drinks.describe()

# Pandas cheat sheet.
















# Video #32 - How do I merge DataFrames in pandas?

df1.append(df2) # Stacking vertically
pd.concat([df1, df2])
pd.merge([df1, df2])
df1.join(df2)

# We join the tables together on the following
pd.merge(movies, ratings, left_on='m_id', right_on='movie_id')

# If it's an index we would do
# Uses the index from the right DataFrame
pd.merge(movies, ratings, left_index=True, right_on='movie_id')

# Both tables have indexes we want to join on
pd.merge(movies, ratings, left_index=True, right_index=True)

# We've been doing an inner join
# There are 4 different types
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














# Video #31 - How do I use the MultiIndex in pandas?

stocks = pd.read_csv('http://bit.ly/smallstocks')
stocks

stocks.index
stocks.groupby('Symbol').Close.mean()

ser = stocks.groupby(['Symbol', 'Date']).Close.mean()
# Two dimensional index.
ser.index

# Change to a DataFrame
ser.unstack()

df = stocks.pivot_table(values='Close', index='Symbol', columns='Date')

ser.loc['AAPL', '2016-10-03']

ser.loc[:, '2016-10-03']

stocks.set_index(['Symbol', 'Date'], inplace=True)
stocks.sort_index(inplace=True)
stocks
stocks.loc['AAPL']
# What rows (index), what columns
stocks.loc[('AAPL', '2016-10-03'), 'Close']

stocks.loc[(['AAPL', 'MSFT'], '2016-10-03'), 'Close']

stocks.loc[('AAPL', ['2016-10-03', '2016-10-04']), :]

stocks.loc[(slice(None), ['2016-10-03', '2016-10-04']), :]

close = pd.read_csv('http://bit.ly/smallstocks', usecols=[0, 1, 3], index_col=['Symbol', 'Date'])
volume = pd.read_csv('http://bit.ly/smallstocks', usecols=[0, 2, 3], index_col=['Symbol', 'Date'])
close
volume

# Merge them together
both = pd.merge(close, volume, left_index=True, right_index=True)
both.sort_index()

# Tidy Data - Each variable has it's own column......

both.reset_index()















# Video #30 How do I apply a function to a pandas Series or DataFrame?

train = pd.read_csv('http://bit.ly/kaggletrain')
train.head()

train['Sex-num'] = train.Sex.map({'female': 0, 'male': 1})
train.loc[0:4, ['Sex', 'Sex-num']]

# Length of each string in the Name column.
train['name_length'] = train.Name.apply(len)
train.loc[0:4, ['Name', 'name_length']]

# Let's round the Fare column
train['Fare_ceil'] = train.Fare.apply(np.ceil)
train.loc[0:4, ['Fare', 'Fare_ceil']]

def get_element(my_list, position):
    return my_list[position]

# This is a list of strings
train.Name.str.split(',').apply(lambda x: x[0]).head()

drinks = pd.read_csv('http://bit.ly/drinksbycountry')
drinks.head()

drinks.loc[:, 'beer_servings':'wine_servings'].apply(np.argmax, axis=1)

drinks.loc[:, 'beer_servings':'wine_servings'] = drinks.loc[:, 'beer_servings':'wine_servings'].applymap(float)
drinks.head()









# Video #29 How do I create a pandas DataFrame from another object?
df = pd.DataFrame({'id':[100, 101, 102], 'color':['red', 'blue', 'red']}, columns=['id', 'color'], index=['a', 'b', 'c'])

pd.DataFrame([[100, 'red'], [101, 'blue'], [102, 'red']], columns=['id', 'color'])

# From numpy array
arr = np.random.rand(4, 2)
arr
pd.DataFrame(arr, columns=['one', 'two'])

# Let's create a DataFrame or 10 rows
pd.DataFrame({'student':np.arange(100, 110, 1), 'test':np.random.randint(60, 101, 10)}).set_index('student')

s = pd.Series(['round', 'square'], index=['c', 'b'], name='shape')

pd.concat([df, s], axis=1)










# Video #28 How do I change display options in pandas?

drinks = pd.read_csv('http://bit.ly/drinksbycountry')
drinks

#pandas.get_option
pd.get_option('display.max_rows')
pd.set_option('display.max_rows', None)

drinks
pd.reset_option('display.max_rows')

pd.get_option('display.max_columns')

train = pd.read_csv('http://bit.ly/kaggletrain')
train.head()

# Show the first 50 characters
pd.get_option('display.max_colwidth')
pd.set_option('display.max_colwidth', 1000)
train.head()

pd.get_option('display.precision')
pd.set_option('display.precision', 2)
train.head()

drinks.head()
drinks['x'] = drinks.wine_servings * 1000
drinks['y'] = drinks.total_litres_of_pure_alcohol * 1000
drinks.head()

# This is format strings in Python generally
pd.set_option('display.float_format', '{:,}'.format)
drinks.head()

pd.describe_option('rows')

pd.reset_option('all')








# Video #27 How do I avoid a SettingWithCopyWarning in pandas?

movies = pd.read_csv('http://bit.ly/imdbratings')
movies.head()
movies.content_rating.isnull().sum()
movies[movies.content_rating.isnull()]

movies.content_rating.value_counts()

movies.loc[movies.content_rating == 'NOT RATED', 'content_rating'] = np.nan

# It's still 3.
movies.content_rating.isnull().sum()

# Let's focus on movies with a a high star rating.
top_movies = movies.loc[movies.star_rating >= 9, :].copy()
top_movies.head()

# Is it a copy or are we changing both the main table and the copy?
top_movies.loc[0, 'duration'] = 150

top_movies.head()












# Video #26 How do I find a remove duplicate rows in pandas

user_cols = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
users = pd.read_table('http://bit.ly/movieusers', sep='|', header=None, names=user_cols)

users.shape
# Returns a true if the value has already been seen in the series.
users.zip_code.duplicated()

# If an entire row has been duplicated it is true.
users.duplicated()

users.loc[users.zip_code.duplicated(keep='last'), :]
users.loc[users.zip_code.duplicated(keep='first'), :]
# Mark all duplicates as true
users.loc[users.zip_code.duplicated(keep=False), :]

users.drop_duplicates(keep=False).shape

# Only consider certain columns
users.drop_duplicates(subset=['age', 'zip_code'], inplace=True)
users.shape




# Video #25 How do I work with dates and times in pandas?
ufo = pd.read_csv('http://bit.ly/uforeports')
ufo.head()

ufo.dtypes

ufo.Time.str.slice(-5, -3).astype(int).head()

ufo['Time'] = pd.to_datetime(ufo.Time)
ufo.dtypes
ufo.Time.dt.hour
ufo.Time.dt.dayofyear

# pandas.Series.dt documentation has more info.

# This is a timestamp
ts = pd.to_datetime('1/1/1999')
ufo.loc[ufo.Time >= ts, :].head()

# We can do math with pandas.
ufo.Time.max() - ufo.Time.min()

ufo['Year'] = ufo.Time.dt.year

ufo.head()
ufo.Year.value_counts().sort_index().plot()
