# -*- coding: utf-8 -*-
"""Project 2 EDA.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1rfw24shLkbVUDoEWcvUxD_9MA2SRyrSg
"""

pip install plotly

"""***IMPORTS***"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.io.json import json_normalize
import ast
import plotly.express as px
import plotly.graph_objects as go

#from google.colab import files
#uploaded = files.upload()
#import io
#print(uploaded.keys())
#credits = pd.read_csv(io.BytesIO(uploaded['TMDB-credits.csv']))
#movies = pd.read_csv(io.BytesIO(uploaded['TMDB-movies.csv']))

credits = pd.read_csv("TMDB-credits.csv")
movies = pd.read_csv("TMDB-movies.csv")

"""***FEATURE DICTIONARY***

The first file contains the following features:
--------------------------------------------------------------------

movie_id: A unique identifier for each movie.

cast: The name of lead and supporting actors.

crew: The name of Director, Editor, Composer, Writer etc.

--------------------------------------------------------------------

The second file contains the following features:
--------------------------------------------------------------------

budget: The budget in which the movie was made.

genre: The genre of the movie, Action, Comedy ,Thriller etc.

homepage: A link to the homepage of the movie.

id: This is infact the movie_id as in the first dataset.

keywords: The keywords or tags related to the movie.

original_language: The language in which the movie was made.

original_title: The title of the movie before translation or adaptation.

overview: A brief description of the movie.

popularity: A numeric quantity specifying the movie popularity.

production_companies: The production house of the movie.

production_countries: The country in which it was produced.

release_date: The date on which it was released.

revenue: The worldwide revenue generated by the movie.

runtime: The running time of the movie in minutes.

status: "Released" or "Rumored".

tagline: Movie's tagline.

title - Title of the movie.

vote_average - average ratings the movie recieved.

vote_count - the count of votes recieved.
"""

# Rename title feature to avoid errors in dataset merge
credits.columns = ['id','title2','cast','crew']

"""***FEATURE ANALYSIS AND DATA CLEANING***"""

# Dataset combination
data = movies.merge(credits,on='id')

# Remove the extra title feature
del data['title2']

data.shape

data.isnull().sum().sort_values(ascending=False)

del data['homepage']
del data['release_date']

data.shape

data.info()

"""***OUTLIER ANALYSIS AND INITIAL DATA OBSERVATIONS***"""

print(data.describe())

print("Number of no budget movies: ", data[data.budget == 0].shape[0])
cleanedBudget = data[data.budget != 0]
print("Number of no budget movies: ", cleanedBudget[cleanedBudget.budget == 0].shape[0])
budgetSorted = cleanedBudget.sort_values('budget', ascending=False)
#print(budgetSorted[['title','budget']].tail(35))
budgetSorted.drop(budgetSorted.tail(35).index,inplace=True) # drop last 38 rows
print("Movies costed less than $10,000 are removed.")
#print(budgetSorted.budget.mean()) # old mean budget = 30 million   new nean budget 37 million
print("\n\nBUDGET MAX OUTLIER CHECK (250 to 380 million dollars)\n")
print(budgetSorted[['title','budget']].head(10))
print("\nAverage cost for a movie production is approximately 37 million dollars.")
print("\nPirates of the Caribbean: On Stranger Tides spent 380 million dollars for production.")
print("\n\nLOWEST BUDGET MOVIES\n")
print(budgetSorted[['title','budget', 'revenue']].tail())
print("\nParanormal Activity revenued 193 million dollars out of 15 thousand dollars budget.")

print("Number of no revenue movies: ", data[data.revenue == 0].shape[0])
cleanedRevenue = data[data.revenue != 0]
print("Number of no revenue movies: ", cleanedRevenue[cleanedRevenue.revenue == 0].shape[0])
print(cleanedRevenue.revenue.mean())
revenueSorted = cleanedRevenue.sort_values('revenue', ascending=False)
print("\n\nREVENUE MAX OUTLIER CHECK (1 to 2.8 billion dollars)\n")
print(revenueSorted[['title','revenue']].head(10))
print("\nAverage revenue from a movie is approximately 117 million dollars.")
print("\nAvatar revenued 2 billion 787 million dollars with only 237 million dollars investment.")

runtimeSorted = data.sort_values('runtime', ascending=False)
runtimeSorted.drop(runtimeSorted.tail(38).index,inplace=True)
print("Movies shorter than 25 minutes are removed.")
print("\n\nTHE LONGEST MOVIES\n")
print(runtimeSorted[['title', 'runtime']].head())
print("\n\nTHE SHORTEST MOVIES\n")
print(runtimeSorted[['title', 'runtime']].tail())
print("\n\nA movie runtime average is an hour and 46 minutes.\n")

"""***HISTOGRAMS***"""

data.hist(column=['budget', 'revenue', 'runtime', 'vote_count', 'vote_average'], figsize=(16,16))
plt.show()

"""***DATA TRANSFORMATIONS***"""

def jsonToList(column, data):  
  data[column] = data[column].fillna('[]').apply(ast.literal_eval)
  data[column] = data[column].apply(lambda x: [i['name'] for i in x] if isinstance(x, list) else [])

def convertToDir(column, data):
    data[column] = data[column].fillna('[]').apply(ast.literal_eval)
    data[column] = data[column].apply(lambda x: [i['name']  for i in x if i['job'] == "Director"] if isinstance(x, list) else [])

jsonToList('genres', data)
jsonToList('production_companies', data)
jsonToList('production_countries', data)
jsonToList('spoken_languages', data)
jsonToList('keywords', data)
jsonToList('cast', data)
convertToDir('crew', data)

data.rename(columns={'crew': 'Director'}, inplace=True)

data['profit'] = data['revenue'] - data['budget']
data['profit_rate'] = data['profit'] / data['budget']

data.head()

"""***VISUALIZATIONS***"""

print("\n\n          Fitting a line...")

fig = px.scatter(data, x="budget", y="revenue", trendline="ols", title="Relationship between Budget and Revenue",color_discrete_sequence=['#30F1E3'])
fig.update_layout(xaxis_title="Budget", 
                 yaxis_title="Revenue")
fig.show()

print("\n\n As expected, budget and revenue positively correlates to each other. \n")
print(" Relationship is almost 1 to 1. \n")

px.histogram(data[data['vote_count'] < 5000],x='vote_count',
             title='Distribution of Vote Counts', color_discrete_sequence=['#1B5D00'])

fig = px.bar(data.sort_values(by="vote_count", ascending=False).iloc[:20][::-1],
             x="vote_count", y="title", orientation='h', title="Most Voted Movies", color_discrete_sequence=['#1B5D00'])
fig.show()

fig = px.histogram(data,x='vote_average',title='Rating Distribution',color_discrete_sequence=['#DE9547'])
fig.update_layout(xaxis_title="Vote Average", 
                 yaxis_title="Numbers")

fig.show()

print("There is a left skew on vote averages.\n")

def common10(data, column):
    temp_data = data.apply(lambda x: pd.Series(x[column], dtype='object'),axis=1).stack().reset_index(level=1, drop=True)
    a = temp_data.value_counts().reset_index()
    a.rename(columns={0: 'Value'})
    fig = px.bar(a.iloc[:10][::-1], x=0, y='index', orientation='v', title="Top 10 {}".format(column),color_discrete_sequence=['#3065F1 '])
    fig.show()

def profitable10(data, column):
    temp_data = data.apply(lambda x: pd.Series(x[column], dtype='object'),axis=1).stack().reset_index(level=1, drop=True)
    a = temp_data.value_counts().reset_index()
    a.rename(columns={0: 'Value'})
    fig = px.bar(a.iloc[:10][::-1], x=0, y='index', orientation='v', title="Top 10 {}".format(column),color_discrete_sequence=['#D1371F '])
    fig.show()

common10(data, 'genres')

common10(data, 'cast')

common10(data, 'keywords')

print("\n\n      MOST PROFITABLES\n")
most_profit_movies = data.sort_values(by="profit", ascending=False).head(200)
profitable10( most_profit_movies, 'genres')

profitable10( most_profit_movies, 'keywords')

profitable10( most_profit_movies, 'spoken_languages')

profitable10( most_profit_movies, 'cast')

common10( most_profit_movies, 'keywords')

corr_matrix=data.corr()
corr_matrix["profit"].sort_values(ascending=False)

fig, ax = plt.subplots(figsize=(19,12));
new = data[['revenue','budget', 'runtime', 'vote_average', 'popularity']].copy()
new = new.corr()
sns.heatmap(new, ax=ax);
ax.set_title('Correlation Matrix');

pd.reset_option('display.max_rows')

"""***CONCLUSIONS***

1 - Profit of the movie is mostly impacted by the vote counts.

2 - Longer runtime tends to increase profit.

3 - Rating of the movie affects the profit very little.

4 - Budget and Revenue has almost 1 to 1 correlation.

5 - Only 35 movies are costed less than $10,000 (Excluding no budget outliers)

6 - Average cost for a movie production is approximately 37 million dollars.

7 - Pirates of the Caribbean: On Stranger Tides spent 380 million dollars for production.

8 - Paranormal Activity revenued 193 million dollars out of 15 thousand dollars budget.

9 - Average revenue from a movie is approximately 117 million dollars.

10 - Avatar revenued 2 billion 787 million dollars with only 237 million dollars investment.

11 - A movie runtime average is an hour and 46 minutes.

12 - Most of the movies are budgeted between \$100,000 to \$40,000,000$

13 - Most of the movies take 70 minutes to 130 minutes.

14 - Most of the movies are rated 5 to 7.8 .

15 - Most of the movies are voted less than 1,300 times.

16 - Inception is rated nearly 14,000 times

17 - Drama is by far the most common genre. Almost 1 in 2 movies has the genre drama.

18 - Samuel L. Jackson is the most common actor with 67 movies followed by Robert Deniro with 57 movies

19 - Most common keywords are the "woman director", "independent film" and "during credits stinger".

20 - Most profitable genres by far are the "adventure" and "action".

21 - Most profitable keyword is "duringcreditsstinger".

22 - English spoken movies are almost 10 times more profitable than the second most profitable spoken language (French).

23 - Stan Lee and John Ratzenberger are the most profitable actors.
"""