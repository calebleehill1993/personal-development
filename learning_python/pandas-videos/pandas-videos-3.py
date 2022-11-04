import pandas as pd
pd.__version__

# Video #35 - Top 25 pandas tricks

pd.show_versions()

# Rename columns

drinks.head()

drinks.loc[::-1]

drinks.loc[::-1].reset_index()

drinks.loc[:, ::-1]

drinks.select_dtypes(include=['number', 'object']).dtypes

# This is used to convert dtypes to numerics where we coerce the errors into na.
# Then we fill the na as 0. So any errors in the conversion will result in 0.
pd.to_numeric(df.col_three, errors='coerce').fillna(0)

# reducing dataframe size: Use categories and read in only what you need.

# This is a library that gets a list of file names following a pattern
from glob import glob

# This will grab all the of the stocks csvs
stock_files = sorted(glob('data/stocks*.csv'))

pd.concat((pd.read_csv(file for file in stock_files)))
pd.concat((pd.read_csv(file for file in stock_files)), ignore_index=True)

# For columns
pd.concat((pd.read_csv(file for file in stock_files)), axis='columns')

# to DataFrame from clipboard
df = pd.read_clipboard()
df

# Split DataFrame into 2 parts
movies_1 = movies.sample(frac=0.75, random_state=1234)
movies_2 = movies.drop(movies_1.index)

# Filter by multiple categaries
movies[(movies.genre == 'Action') |
        (movies.genre == 'Drama') |
        (movies.genre == 'Western')].head()

# Better way
movies[movies.genre.isin(['Action', 'Drama', 'Western'])].head()

# Exclude
movies[~movies.genre.isin(['Action', 'Drama', 'Western'])].head()

# 3 Largest
movies[movies.genre.isin(counts.nlargest(3).index)].head()

# Missing values
ufo.isna().sum()

ufo.isna().mean()

ufo.dropna(axis='columns').head()

# If more than 10% are missing we'll drop that column
ufo.dropna(thresh=len(ufo)*0.9, axis='columns').head()

# Split string into multiple columns
df.name.str.split(' ', expand=True)

df.pivot_table(index='Something', columns='Somthing', values='Something', aggfunc='mean', margins=True)

# Turn countinuous data into categorical
pd.cut(titanic.Age, bins=[0, 18, 25, 99], labels=['child', 'young adult', 'adult']).head(10)

import pandas_profiling

pandas_profiling.ProfileReport(df)















# Video #34 - 5 new changes in pandas you need to know about (older)

# ix has been deprecated.

drinks = pd.read_csv('http://bit.ly/drinksbycountry', index_col='country')
drinks

drinks.loc['Angola', 'spirit_servings']

drinks.iloc[4, 1]

# Deprecated
drinks.ix['Angola', 1]

# Alternatives
drinks.loc['Angola', drinks.columns[1]]
drinks.iloc[drinks.index.get_loc('Angola'), 1]

drinks.loc[drinks.index[4], 'spirit_servings']

# Aliases have been added for is null and notnull

ufo = pd.read_csv('http://bit.ly/uforeports')
ufo.head()

ufo.isnull()
ufo.notnull()

# Dropping na rather than null. Both work, but standardized names.
ufo.dropna().head()

# Recommended that we use na.
ufo.isna()
ufo.notna()

# Drop now accepts "index" and "columns"
ufo.drop([0, 1], axis=0).head()
ufo.drop([0, 1], axis='index').head()

ufo.drop(index=[0, 1]).head()

ufo.drop(columns=['City', 'State'])

# rename and reindex now accepts "axis" keyword

ufo.rename(columns={'City': 'CITY', 'State': 'STATE'})

ufo.rename({'City': 'CITY', 'State': 'STATE'}, axis='columns').head()

ufo.rename(str.upper, axis='columns').head()

df = pd.DataFrame({'ID': [100, 101, 102, 103],
                    'quality': ['good', 'very good', 'good', 'excellent']})

from pandas.api.types import CategoricalDtype
quality_cat = CategoricalDtype(['good', 'very good', 'excellent'], ordered=True)
df['quality'] = df.quality.astype(quality_cat)

df.quality
