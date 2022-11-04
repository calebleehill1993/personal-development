################################################################################
# ATOM PACKAGES
# Hydrogen 2.16.3
# atom-beautify 0.33.4
#
# Python Version 3.9.5
# IPython3 Kernel
################################################################################

# Python Data Analysis Library (Derived from "panel data")
import pandas as pd # Version 1.2.4

# Reading in CSV files
ufo = pd.read_csv('http://bit.ly/uforeports')
ufo.head()

# Find the null values
ufo.isnull()

# Drop the null values
ufo.dropna(how='any').head()

# Fill the null values
ufo['Shape Reported'].fillna(value='VARIOUS').tail()

# Selecting specific columns
ufo['Colors Reported']

# What are the dimensions?
ufo.shape

# What are the columns?
ufo.columns

# Remove Rows (axis=0)
ufo.drop([0, 1, 2, 3], axis=0)
ufo.head()

# Remove columns (axis=1)
# Inplace replaces the DataFrame
ufo.drop(['Colors Reported'], axis=1, inplace=True)
ufo.head()

# Reading tables vs CSV
drinks = pd.read_table('http://bit.ly/drinksbycountry', sep=',')
drinks.head()

# We can do groupby aggregations
drinks.groupby('continent').beer_servings.mean()
drinks.groupby('continent').beer_servings.agg(['count', 'min', 'max', 'mean'])

# Plotting groups
drinks.groupby('continent').mean().plot(kind='bar')
# If wasn't using the IPython Kernel I'd have to show the plot.
# matplotlib.pyplot.show()

# Movies table
movies = pd.read_csv('http://bit.ly/imdbratings')
movies.head()

# Filtering DataFrames
movies.loc[movies.duration >= 200, 'genre']

# Filtering by multiple conditions
movies.loc[(movies.duration >= 200) & (movies.genre == 'Drama'), :]

# Counting values
movies.genre.value_counts()
movies.genre.value_counts(normalize=True)

# Getting unique values
movies.genre.unique()
movies.genre.nunique()

# Counting by multiple categories
pd.crosstab(movies.genre, movies.content_rating)

# Plotting histograms
movies.duration.plot(kind='hist')

# Plotting counts by category
movies.genre.value_counts().plot(kind='bar')

# Gives overview of numerical columns
movies.describe()

# Changing the index
movies.set_index('title')

# .loc
ufo.loc[:, ['City', 'State']]

# .iloc
ufo.iloc[:, [0, 3]]

# Exporting Table as .csv
ufo.iloc[0:9, :].to_csv('ufo.csv')

# Exporting Table as Pickle
ufo.iloc[0:9, :].to_pickle('ufo.pkl')

# Creating a DataFrame
df = pd.DataFrame({'ID': [100, 101, 102, 103], 'quality':['good', 'very good', 'good', 'excellent']})
df

# Sorting by a string is alphabetical
df.sort_values('quality')

# We can create the ordering.
# We can use the CategoricalDtype as a way of telling the DataFrame what categories
# there are.
df['quality'] = df.quality.astype(pd.api.types.CategoricalDtype(categories=['good', 'very good', 'excellent'], ordered=True))
df.sort_values('quality')
df.quality
df.loc[df.quality > 'good']

# Talked very briefly about Machine Learning using LogisticRegression
# and training sets on Kaggle Data set about the Titanic

# Getting a random sample from a DataFrame
ufo.sample(n=3, random_state=42)

# Getting Dummy Variables for modeling
train = pd.read_csv('http://bit.ly/kaggletrain')
train.head()
pd.get_dummies(train, columns=['Sex', 'Embarked'], drop_first=True)
