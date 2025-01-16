import pandas
import numpy as np
import streamlit as st
import pickle
with open('C:\\Users\\MUHAMMAD AEHTSHAM\\Documents\\movie_data.pkl', 'rb') as file:
    movie, cosine_sim = pickle.load(file)
    
def get_recommendations(title, cosine_sim=cosine_sim):
    try:
        idx = movie[movie['title'] == title].index[0]
    except IndexError:
        return pd.DataFrame()

    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]
    movie_indices = [i[0] for i in sim_scores]
    return movie.iloc[movie_indices][['title', 'movie_id']]

    
st.title("Movie Recommendations")
st.header("What's Your Favourite Movie")

st.sidebar.title("Enter you details")
name = st.sidebar.text_input("Name")
email = st.sidebar.text_input("Email")
message = st.sidebar.text_input("contact no: ")
if st.sidebar.button("submit"):
    st.success("Your details have been entered")

selected_movie =st.selectbox("Select a Movie", movie['title'].values)
if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    if not recommendations.empty:
        st.write(" Top 10 Recommended Movies:")
        num_recommendations = len(recommendations)
        num_columns = 5 

        for i in range(0, num_recommendations, num_columns):
            cols = st.columns(num_columns)
            for col, j in zip(cols, range(i, i + num_columns)):
                if j < num_recommendations:
                    movie_title = recommendations.iloc[j]['title']
                    movie_id = recommendations.iloc[j]['movie_id']
                    with col:
                        st.write(movie_title)
    else:
        st.error("No recommendations found. Please try another movie.")

