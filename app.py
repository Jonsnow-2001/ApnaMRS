import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

# Page configuration
st.set_page_config(page_title="Apna Movie Recommender", layout="wide", initial_sidebar_state="auto")

# File & URL setup
file_id = "1h7GXUyodqVrJnbDOCFkJKjMFjG6bjUj7"
url = f"https://drive.google.com/uc?id={file_id}"
local_path = "similarity.pkl"

# Load data: movies_dict
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies_list = pd.DataFrame(movies_dict)

# Cache similarity loading
@st.cache_resource
def load_similarity():
    if not os.path.exists(local_path):
        gdown.download(url, local_path, quiet=False)
    with open(local_path, 'rb') as f:
        return pickle.load(f)

similarity = load_similarity()

# Cache poster fetching
@st.cache_data(show_spinner=False)
def fetch_poster(movie_id):
    response = requests.get(
        f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=60a49e9e17e90231e64df24a912b7442&language=en-US')
    data = response.json()
    return "http://image.tmdb.org/t/p/w500/" + data['poster_path']

# Movie recommendation logic
def recommend(movie_name):
    movie_index = movies_list[movies_list['title'] == movie_name].index[0]
    distances = similarity[movie_index]
    rec_movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]

    new_rec_movies_list = []
    rec_movies_posters = []

    for i in rec_movies_list:
        movie_id = movies_list.iloc[i[0]].movie_id
        new_rec_movies_list.append(movies_list.iloc[i[0]].title)
        rec_movies_posters.append(fetch_poster(movie_id))

    return new_rec_movies_list, rec_movies_posters

# Custom CSS
st.markdown("""
    <style>
        .custom-label {
            font-size: 22px;
            font-weight: 600;
        }
        div[data-baseweb="select"] > div {
            font-size: 18px;
        }
        button[kind="primary"] {
            font-size: 18px !important;
            font-weight: 600 !important;
        }
        .movie-title {
            font-size: 22px;
            font-weight: 500;
            text-align: center;
            height: 2em;
            overflow: hidden;
            white-space: nowrap;
            text-overflow: ellipsis;
        }
        .movie-poster {
            transition: transform 0.3s ease;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        }
        .movie-poster:hover {
            transform: scale(1.05);
            box-shadow: 0 6px 12px rgba(0,0,0,0.3);
        }
        .stImage {
            display: flex;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Title
st.title('🎬 Apna Movie Recommender ')

# Spacer
st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

# Movie select box
st.markdown('<div class="custom-label">Select the movie name to recommend similar movies:</div>', unsafe_allow_html=True)
selected_movie_name = st.selectbox("Select a movie", movies_list['title'].values, label_visibility="collapsed")


# Recommend button
if st.button("🎯 Recommend"):
    with st.spinner("Recommending movies..."):
        movies, posters = recommend(selected_movie_name)

        # Spacer between rows
        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

        row1 = st.columns(5)
        for i in range(5):
            with row1[i]:
                st.markdown(f"<div class='movie-title'>{movies[i]}</div>", unsafe_allow_html=True)
                st.markdown(f"<img src='{posters[i]}' class='movie-poster' width='100%'>", unsafe_allow_html=True)

        st.markdown("<div style='margin-top: 30px;'></div>", unsafe_allow_html=True)

        row2 = st.columns(5)
        for i in range(5, 10):
            with row2[i % 5]:
                st.markdown(f"<div class='movie-title'>{movies[i]}</div>", unsafe_allow_html=True)
                st.markdown(f"<img src='{posters[i]}' class='movie-poster' width='100%'>", unsafe_allow_html=True)
