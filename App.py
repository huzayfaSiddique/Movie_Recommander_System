import streamlit as st
import pandas as pd
import pickle
import requests

def fetch_poster(movie_id):
        response = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=bdb0d2357012e1b98da662ca19e0671d&language=en-US"
        )
        response.raise_for_status()
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return "https://image.tmdb.org/t/p/w500/" + poster_path
        else:
            return "https://via.placeholder.com/500x750?text=No+Poster+Found"
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:10]

    recommended_movies = []
    recommended_posters = []

    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))

    return recommended_movies, recommended_posters
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


st.title('Movie Recommender System')

option = st.selectbox(
    'Write movie name for recommendations:',
    movies['title'].values
)

if st.button('Recommend'):
    recommended_movies, recommended_posters = recommend(option)

    cols = st.columns(5)
    for col, name, poster in zip(cols, recommended_movies, recommended_posters):
        with col:
            st.image(poster, use_container_width=True)
            st.markdown(f"**🎞 {name}**", unsafe_allow_html=True)
