import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image
from datetime import datetime
import base64

# Authentication credentials
USER_CREDENTIALS = {
    "admin": "admin",
    "user1": "moviefan"
}

# Authentication function
def authenticate(username, password):
    return USER_CREDENTIALS.get(username) == password

# Session state initialization
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a7929155a13f1d72c8b721ee864c3299&language=en-US"
    response = requests.get(url)
    data = response.json()
    
    poster_url = "https://image.tmdb.org/t/p/w500" + data['poster_path'] if 'poster_path' in data and data['poster_path'] else "https://via.placeholder.com/500x750?text=No+Image"
    genre = ", ".join([g["name"] for g in data.get("genres", [])]) if "genres" in data else "Unknown Genre"
    duration = f"{data.get('runtime', 'N/A')} min"
    
    return poster_url, genre, duration

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    recommended_movies = []
    recommended_movies_posters = []
    recommended_movies_genres = []
    recommended_movies_durations = []
    
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        poster, genre, duration = fetch_movie_details(movie_id)
        
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(poster)
        recommended_movies_genres.append(genre)
        recommended_movies_durations.append(duration)
    
    return recommended_movies, recommended_movies_posters, recommended_movies_genres, recommended_movies_durations

def get_greeting():
    hour = datetime.utcnow().hour
    if hour < 12:
        return "Good Afternoon"
    elif hour < 18:
        return "Good afternoon"
    else:
        return "Good evening"

def fetch_trending_movies():
    url = "https://api.themoviedb.org/3/trending/movie/week?api_key=a7929155a13f1d72c8b721ee864c3299"
    response = requests.get(url)
    data = response.json()
    if "results" not in data:
        return [], []
    movies = data["results"][:5]
    trending_titles = [movie.get("title", "Unknown") for movie in movies]
    trending_posters = [fetch_movie_details(movie["id"])[0] if "id" in movie else "https://via.placeholder.com/500x750?text=No+Image" for movie in movies]
    return trending_titles, trending_posters

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

hide_st_style="""
<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>
"""
st.markdown(hide_st_style, unsafe_allow_html=True)

img = Image.open("Bingyfi.png")
st.image(img, width=100)

def set_bg_image(image_path):
    with open(image_path, "rb") as img_file:
        encoded = base64.b64encode(img_file.read()).decode()
    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

set_bg_image("bg.jpg")

# Authentication System
if not st.session_state.logged_in:
    st.title("Login to Bingyfi")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        if authenticate(username, password):
            st.session_state.logged_in = True
            st.session_state.username = username
            st.success("Login successful!")
            st.rerun()
        else:
            st.error("Invalid credentials. Try again.")
else:
    greeting = get_greeting()
    st.title(f"{greeting}, {st.session_state.username}!")
    
    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
    
    st.header("Trending Movies")
    trending_titles, trending_posters = fetch_trending_movies()
    if trending_titles:
        cols = st.columns(len(trending_titles))
        for i, col in enumerate(cols):
            with col:
                st.text(trending_titles[i])
                st.image(trending_posters[i])
    else:
        st.warning("No trending movies available.")
    
    st.header("Movie Recommendation System")
    st.text("Enter the name of the movie you like")
    selected_movie_name = st.selectbox('Search your movie', movies['title'].values)
    if st.button('Recommend'):
        names, posters, genres, durations = recommend(selected_movie_name)
        cols = st.columns(len(names))
        for i, col in enumerate(cols):
            with col:
                st.text(names[i])
                st.image(posters[i])
                st.write(f"*Genre:* {genres[i]}")
                st.write(f"*Duration:* {durations[i]}")

# Streamlit Footer
st.markdown("""
    <div style="text-align: center; padding: 10px; font-size: 14px;">
        Made with ❤ by DesDevelopers | In Illuminati 2025 
    </div>
""", unsafe_allow_html=True)
