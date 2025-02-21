import streamlit as st
import pickle
import pandas as pd
import requests
from PIL import Image




def fetch_poster(movie_id):
    response = requests.get(
        f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=a7929155a13f1d72c8b721ee864c3299&language=en-US"
    )
    data = response.json()

    if 'poster_path' in data and data['poster_path']:  # Check if key exists
        return "https://image.tmdb.org/t/p/w500" + data['poster_path']
    else:
        return "https://via.placeholder.com/500x750?text=No+Image"



def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x:x[1])[1:6]

    recommended_movies= []
    recommended_movies_posters = []
    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        #fetch_poster(i[0])
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters


movies_dict= pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))

#removal of footer
hide_st_style="""
<style> #MainMenu {visibility: hidden;} footer {visibility: hidden;} </style>
"""

st.markdown(hide_st_style, unsafe_allow_html=True)


img = Image.open("Bingyfi.png")
st.image(
    img ,
    width=100,
)


def set_bg_image(image_url):
    bg_style = f"""
    <style>
    .stApp {{
        background-image: url("{"bg.jpg"}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(bg_style, unsafe_allow_html=True)

# Call the function with your image URL
set_bg_image("bg.jpg")






st.text("Enter the name of the movie you like")

selected_movie_name = st.selectbox(
    '   Search your movie',
    movies['title'].values)

if st.button('Recommend'):
    names,posters = recommend(selected_movie_name)

    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(names[0])
        st.image(posters[0])

    with col2:
        st.text(names[1])
        st.image(posters[1])

    with col3:
        st.text(names[2])
        st.image(posters[2])

    with col4:
        st.text(names[3])
        st.image(posters[3])

    with col5:
        st.text(names[4])
        st.image(posters[4])



#https://api.themoviedb.org/3/movie/65?api_key=<<api_key>>&language=en-US
