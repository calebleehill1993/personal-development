import pandas as pd
import numpy as np
import matplotlib

# This will help with displaying more columns rather than having ...
desired_width = 320
pd.set_option('display.width', desired_width)
np.set_printoptions(linewidth=desired_width)
pd.set_option('display.max_columns', 10)




# How do I explore a pandas Series?

# movies = pd.read_csv('http://bit.ly/imdbratings')
# print(movies.head())
# print(movies.dtypes)
# print(movies.genre.describe())
# print(movies.genre.value_counts(normalize=True))
# print(movies.genre.unique())
# print(movies.genre.nunique())
# print(pd.crosstab(movies.genre, movies.content_rating))
# print(movies.duration.mean())
#
# movies.duration.plot(kind='hist')
# matplotlib.pyplot.show()
# movies.genre.value_counts().plot(kind='bar')
# matplotlib.pyplot.show()


# How to change dtype of pandas series

# drinks = pd.read_csv('http://bit.ly/drinksbycountry')
#
# print(drinks.head())
# print(drinks.dtypes)
# drinks['beer_servings'] = drinks.beer_servings.astype(float)
# print(drinks.dtypes)

# # Convert dtypes while reading in
# drinks = pd.read_csv('http://bit.ly/drinksbycountry', dtype={'beer_servings': float})
#
# orders = pd.read_table('http://bit.ly/chiporders')
# # Object is string.
# print(orders.item_price.str.replace('$', '').astype(float).mean())
#
# # Converting bool to int so we can do some kind of math on it
# print(orders.item_name.str.contains('Chicken').astype(int).head())

# When should I use a "grouppby" in pandas?

# drinks = pd.read_csv('http://bit.ly/drinksbycountry')
#
# print(drinks)
# print(drinks.groupby('continent').beer_servings.mean())
# print(drinks.groupby('continent').beer_servings.agg(['count', 'min', 'max', 'mean']))
# print(drinks.groupby('continent').mean())
#
# drinks.groupby('continent').mean().plot(kind='bar')
# matplotlib.pyplot.show()


# How do I use string methods in pandas?

# orders = pd.read_table('http://bit.ly/chiporders')
# print(orders.head())
# print(orders.item_name.str.upper())
# print(orders[orders.item_name.str.contains('Chicken')])
#
# print(orders.choice_description.str.replace('[\[\]]', ''))





# ufo = pd.read_csv('http://bit.ly/uforeports', usecols=['City', 'State'])
# # read in the first number of rows
# ufo = pd.read_csv('http://bit.ly/uforeports', nrows=3)
#
# for c in ufo.City:
#     print(c)
#
# for index, row in ufo.iterrows():
#     print(index, row.City, row.State)
#
# drinks = pd.read_csv('http://bit.ly/drinksbycountry')
#
# print(drinks.dtypes)
#
# # What if we only want a certain data type?
# print(drinks.select_dtypes(include=[np.number]).head())
#
# print(drinks.head())
#
# print(drinks.describe(include=['object']))


# How do I apply multiple filter criteria to a pandas DataFrame

# movies = pd.read_csv('http://bit.ly/imdbratings')
#
# print(movies.head())
#
# # We have to use parenthesis and & or | for filtering pandas.
# print(movies[(movies.duration >= 200) & (movies.genre == 'Drama')])
#
# print(movies[movies.genre.isin(['Crime', 'Drama', 'Action'])])


# How do I filter rows of a pandas DataFrame by column value?

# movies = pd.read_csv('http://bit.ly/imdbratings')
#
# # We want to filter by duration
# booleans = []
# for length in movies.duration:
#     if length >= 200:
#         booleans.append(True)
#     else:
#         booleans.append(False)
#
# print(booleans[0:5])
#
# # Convert to series
# is_long = pd.Series(booleans)
#
# is_long = movies.duration >= 200
#
# # Shows when duration is long
# print(movies.loc[movies.duration >= 200, 'genre']) # what rows, what columns. Powerful stuff.



# How do I sort a pandas DataFrame or Series
#
# movies = pd.read_csv('http://bit.ly/imdbratings')
#
# # New version (relative to the video time)
# print(movies['title'].sort_values(ascending=False)) # does not change the dataframe
#
# # inplace=True replaces the df values
# print(movies.sort_values('duration', ascending=False))
#
# movies.sort_values(['content_rating', 'duration']) # Sort by content_rating then by duration



# How do I remove columns from a pandas DataFrame?

# ufo = pd.read_csv('http://bit.ly/uforeports')
#
# # Get rid of colors_reported
# ufo.drop(['Colors Reported', 'City', 'State'], axis=1, inplace=True)
#
# print(ufo.head())
#
# # remove rows
# ufo.drop([0, 1] , axis=0, inplace=True)
# print(ufo.head())



# How do I rename columns in a pndas DataFrame?

# ufo = pd.read_csv('http://bit.ly/uforeports')
# print(ufo.head())
# print(ufo.columns)
# ufo.rename(columns={'Colors Reported': 'Colors_Reported', 'Shape Reported': 'Shape_Reported'}, inplace=True)
# print(ufo.columns)
# ufo_cols = ['city', 'colors reported', 'shape reported', 'state', 'time']
# ufo.columns = ufo_cols
# print(ufo.columns)
#
# ufo = pd.read_csv('http://bit.ly/uforeports', names=ufo_cols, header=0) # Replaces row own names with ufo_cols
#
# ufo.columns = ufo.columns.str.replace(' ', '_')
#
# print(ufo.columns)



# Why do some pandas commands end with parentheses, and other commands don't?

# methods vs attributes (does it do something or store something?

# movies = pd.read_csv('http://bit.ly/imdbratings')
#
# print(movies.head())
# print(movies.describe(include=['object']))
# print(movies.shape)
# print(movies.dtypes)
#
# type(movies)


# How do I select a pandas Series from a DataFrame

# ufo = pd.read_csv('http://bit.ly/uforeports')
# print(type(ufo))
# print(ufo.head())
# print(ufo['City']) # case sensitive
# print(ufo.City) # This also works
# print(ufo['Colors Reported']) # Can't use dot notation for this.
#
# ufo['Location'] = ufo.City + ', ' + ufo.State
#
# print(ufo.head())

# orders = pd.read_table('http://bit.ly/chiporders') # Assumes tab separation
#
# user_columns = ['user_id', 'age', 'gender', 'occupation', 'zip_code']
# users = pd.read_table('http://bit.ly/movieusers', sep='|', header=None, names=user_columns)
# print(users)