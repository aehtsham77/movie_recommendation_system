# movie_recommendation_system
Trained on TMDB Data Set from Kaggle which contains information about 5000 movies.
#Importing Libraries
import pandas as pd
import numpy as np
import ast
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import pickle

#Loading Data Sets 
credits = pd.read_csv('D:\\Movies Recommndation System\\soft files\\tmdb_5000_credits.csv')
movies = pd.read_csv('D:\\Movies Recommndation System\\soft files\\tmdb_5000_movies.csv')

#Preprocessing of data files
movie = movies.merge(credits, left_on  = 'title', right_on = 'title')
movie= movie[['movie_id', 'title', 'overview', 'genres', 'popularity', 'keywords', 'cast', 'crew']]

#function used for removal of unwanted things
def convert(obj):
    L = []
    for i in ast.literal_eval(obj):
        L.append(i['name'])
    return L
#preprocessing
movie['genres'] = movie['genres'].apply(convert)
movie['keywords'] = movie['keywords'].apply(convert)
movie['cast'] = movie['cast'].apply(lambda x:[i['name'] for i in ast.literal_eval(x)[:3]])
movie['crew'] = movie['crew'].apply(lambda x:[i['name'] for i in ast.literal_eval(x) if i['job'] == 'Director'])
movie['tags'] = movie['genres'] + movie['keywords'] + movie['cast'] + movie['crew']

movie = movie [['movie_id', 'title', 'overview','tags']]
movie['tags'] = movie['tags'].apply(lambda x: " ".join(x)) #to remove the commas
movie['tags'] = movie['tags'].apply(lambda x: x.lower())  #to lower the text

#Main Code
tfi = TfidfVectorizer(stop_words='english')
tfi_matrix = tfi.fit_transform(movie['tags'])


cosine_sim = cosine_similarity(tfi_matrix, tfi_matrix)

def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movie[movie['title'] == title] .index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse= True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movies['title'].iloc[movie_indices]

#using pickle for exporting the file
with open('movie_data.pkl', 'wb') as file:
    pickle.dump((movie, cosine_sim), file)
