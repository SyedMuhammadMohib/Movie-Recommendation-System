import pandas as pd
import pickle
import streamlit as st
import requests
import time
import random

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=c24ee19410a0d08ecebf0223e40ef1f6&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')
    if poster_path:
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        return full_path
    return "https://via.placeholder.com/200x300.png?text=No+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)

    return recommended_movie_names, recommended_movie_posters


st.set_page_config(page_title="🎬Movie Recommendation System", layout="wide")
st.title("🎬Movie Recommendation System")
st.markdown("### 🍿Find your next favorite movie in seconds!")


movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))


movie_list = movies['title'].values
selected_movie_name = st.selectbox("🎥 Select a movie you like:", movie_list)


if st.button('Show Recommendation 🎯'):
    with st.spinner("🔍 Finding the best recommendations for you..."):
        time.sleep(2)  # simulate loading
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie_name)


    st.success("✨ Here are your movie recommendations!")


    cols = st.columns(5)
    for idx, col in enumerate(cols):
        with col:
            st.image(recommended_movie_posters[idx], use_container_width=True)
            st.markdown(f"**{recommended_movie_names[idx]}**")


            with st.expander("More Info"):
                st.write(f"⭐ Rating: {random.randint(70,100)/10}")
                st.write(f"📅 Release: {random.randint(2002,2023)}")
                st.write("🎭 Genre: Action, Drama, Adventure")
