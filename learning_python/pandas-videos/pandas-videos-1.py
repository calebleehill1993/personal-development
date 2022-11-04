import pandas as pd

# Video #24 - How do I create dummy variables in pandas?

# Dummy variables would be like male is 0 female is 1

train = pd.read_csv('http://bit.ly/kaggletrain')
train.head()
# Dummy for sex columns
train['Sex_male'] = train.Sex.map({'female':0, 'male':1})
train.head()

# Generally we use k-1 dummy variables
pd.get_dummies(train.Sex, prefix='Sex').iloc[:, 1:]

train.Embarked.value_counts()
embarked_dummies = pd.get_dummies(train.Embarked, prefix='Embarked').iloc[:, 1:]

train = pd.concat([train, embarked_dummies], axis=1)
train.head()

# This is the way
pd.get_dummies(train, columns=['Sex', 'Embarked'], drop_first=True)








# Video #23 - More questions

# How do I read pandas docs (just google the name of the function)

ufo = pd.read_csv('http://bit.ly/uforeports')
ufo.head()
ufo.isnull().head()
pd.isnull(ufo).head()

# Label Based indexing. Inclusive
# Why is loc different?
# It wouldn't make sense for loc to have City through Time to get
# City through State.
ufo.loc[:, 'City':'State']
ufo.loc[0:4, :]

# Pandas is built on Numpy
# iloc uses the same logic as Numpy
# Numpy likely does it because range() does it.
ufo.iloc[0:4, :]
ufo.values[0:4, :]

# Random Sampling
ufo.sample(n=3, random_state=42)

train = ufo.sample(frac=0.75, random_state=99)

test = ufo.loc[~ufo.index.isin(train.index), :]







# Video #22 - How do I use pandas with sciket-learn to create Kaggle submissions?

# Kaggle is a place for competitive machine learning

# Data our model will learn from
train = pd.read_csv('http://bit.ly/kaggletrain')
train.head()
feature_cols = ['Pclass', 'Parch']
X = train.loc[:, feature_cols]
X.shape
# Target
y = train.Survived
y.shape

from sklearn.linear_model import LogisticRegression
logreg = LogisticRegression()
logreg.fit(X, y)

test = pd.read_csv('http://bit.ly/kaggletest')
test.head()
X_new = test.loc[:, feature_cols]
X_new.shape
new_pred_class = logreg.predict(X_new)

test.PassengerId
new_pred_class

pd.DataFrame({'PassengerId': test.PassengerId, 'Survived': new_pred_class}).set_index('PassengerId').to_csv('sub.csv')

# Save DataFrame to disk (We will pickle it)
train.to_pickle('train.pkl')
pd.read_pickle('train.pkl')




# Video #21 - How do I make my pandas DataFrame smaller and faster?

drinks = pd.read_csv('http://bit.ly/drinksbycountry')

# object type is just a reference to an object
# We don't know exactly how much data is in each object, just how much
# the actual DataFrame
drinks.info()

# This is the true memory size
drinks.info(memory_usage='deep')
# This is the memory in bytes
drinks.memory_usage(deep=True)

drinks.memory_usage(deep=True).sum()

# Maybe I can store ints to reference the strings
sorted(drinks.continent.unique())

drinks.continent.head()

# Convert to categary type
drinks['continent'] = drinks.continent.astype('category')
drinks.dtypes
# It's storing them as ints
drinks.continent.head()
# cat is the way to access category info and methods
drinks.continent.cat.codes.head()

drinks.memory_usage(deep=True)
# Country gets bigger because we have all unique countries and so we're storing
# both all the strings and all the ints and it is more.
drinks['country'] = drinks.country.astype('category')
drinks.memory_usage(deep=True)

# Category dtypes speed up computations when compared with strings.
df = pd.DataFrame({'ID': [100, 101, 102, 103], 'quality':['good', 'very good', 'good', 'excellent']})
df
df.sort_values('quality')
# We can create the ordering.
# We can use the CategoricalDtype as a way of telling the DataFrame what categories
# there are.
df['quality'] = df.quality.astype(pd.api.types.CategoricalDtype(categories=['good', 'very good', 'excellent'], ordered=True))
df.sort_values('quality')
df.quality
df.loc[df.quality > 'good'

]


# Video #20 - When should I use the "inplace" paramketer?

ufo = pd.read_csv('http://bit.ly/uforeports')
ufo.shape
ufo.head()
ufo.drop('City', axis=1).head()
ufo.head()
# We have to say inplace if we want to change the base DataFrame.
ufo.drop('City', axis=1, inplace=True)
# Now it's gone.
ufo.head()
ufo.dropna(how='any').shape
# You could do an assignment statement
ufo = ufo.set_index('Time')
ufo.head()
# What's the difference? Inplace sounds better, but there really doesn't seem
# to be a difference that is for sure. just use whichever is better.
ufo.fillna(method='bfill').tail()
ufo.fillna(method='ffill').tail()








# Video # 19 - How do I select multiple rows and columns from a pandas DataFrame
ufo = pd.read_csv('http://bit.ly/uforeprots')
ufo.head(3)

ufo.loc[0:2, :]

ufo.loc[:, ['City', 'State']]
ufo.loc[0:2, 'City':'State']
ufo.head(3).drop('Time', axis=1)

ufo[ufo.City=='Oakland'].State
ufo.loc[ufo.City=='Oakland', 'State']

# Integer Position
ufo.iloc[:, [0, 3]]
# iloc is exclusive.
ufo.iloc[:, 0:4]
# Again exclusive
ufo.iloc[0:3, :]

ufo[['City', 'State']]
ufo[0:2]

drinks = pd.read_csv('http://bit.ly/drinksbycountry', index_col='country')
drinks.head()
# ix is depricated
drinks.ix['Albania', 0]




# Video 18 - What do I need to know about the padnas index part 2
drinks = pd.read_csav('http://bit.ly/drinksbycountry')

drinks.head()
# Series also have an index
drinks.continent.head()

drinks.set_index('country', inplace=True)
drinks.head()
drinks.continent.head()
drinks.continent.value_counts()['Africa']
drinks.continent.value_counts().sort_index()

# Created DataFrame
people = pd.Series([3000000, 85000], index=['Albania', 'Andorra'], name='population')
people

# This worked by index. It matched the index of each of the DataFrames
drinks.beer_servings * people

# Aligned by index
pd.concat([drinks, people], axis=1).head()


# Video #17 - What do I need to know about the pandas index?

drinks = pd.read_csv('http://bit.ly/drinksbycountry')
drinks.head()

# Sometimes called the row labels
drinks.index

# Index isn't part of the DataFrame
drinks.shape

pd.read_table('http://bit.ly/movieusers', header=None, sep='|').head()

drinks[drinks.continent=='South America']
# You can use index like this.
drinks.loc[23, 'beer_servings']
drinks.set_index('country', inplace=True)
drinks.head()
drinks.columns
drinks.shape
drinks.loc['Brazil', 'beer_servings']
# You don't have to have a name for the index.
drinks.index.name = None
drinks.head()
# Moving back into a column
drinks.index.name = 'country'
drinks.reset_index(inplace=True)
drinks.head()
# Describe is a DataFrame
drinks.describe()

drinks.describe().columns
drinks.describe().index
drinks.describe().loc['25%', 'beer_servings']


# How do I handle missing values in pandas

ufo = pd.read_csv('http://bit.ly/uforeports')
ufo.tail()
ufo.isnull().tail() # True if the value is missing
ufo.notnull().tail() # The opposite

# Axis determines the direction we are summing (columns or rows)
ufo.isnull().sum(axis=0) # Sum will convert bools to 1 or 0 and then sum.

pd.Series([True, False, True]).sum()

ufo[ufo.City.isnull()]

# There is not only one option for what to do with null values.
# We could just drop the rows that are null.
ufo.shaped
# Drop a row if any values are null.
ufo.dropna(how='any', inplace=False).shape

ufo.dropna(how='all').shape

# Subset determines what columns we are looking at.
ufo.dropna(subset=['City', 'Shape Reported'], how='any').shape

# By default missing values are not included
ufo['Shape Reported'].value_counts(dropna=False)

ufo['Shape Reported'].fillna(value='VARIOUS', inplace=True)
