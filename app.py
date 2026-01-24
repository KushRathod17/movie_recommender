import streamlit as st
import pickle
import pandas as pd
import requests
import os


my_api_key = "50e3ca3a2b11ecdf6cc63be05babd425"  


def fetch_details(movie_id):
    try:
       
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={my_api_key}&language=en-US"
        response = requests.get(url, timeout=5)
        data = response.json()
        
  
        if data.get('poster_path'):
            poster = "https://image.tmdb.org/t/p/w500/" + data['poster_path']
        else:
            poster = "https://via.placeholder.com/500x750?text=No+Image"

      
        rating = round(data.get('vote_average', 0), 1)
        release_date = data.get('release_date', "N/A")
        year = release_date.split("-")[0] if release_date else "N/A"
        title = data.get('title', "Movie")

        url_videos = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={my_api_key}&language=en-US"
        data_videos = requests.get(url_videos, timeout=5).json()
        
        trailer_url = ""
       
        for video in data_videos.get('results', []):
            if video['type'] == "Trailer" and video['site'] == "YouTube":
                trailer_url = f"https://www.youtube.com/watch?v={video['key']}"
                break
        
        if not trailer_url:
            trailer_url = f"https://www.youtube.com/results?search_query={title}+official+trailer"

        return poster, rating, year, trailer_url

    except:
    
        return "https://via.placeholder.com/500x750?text=Error", 0, "N/A", "https://www.youtube.com"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    
    rec_data = [] # List to store all movie details
    
    for i in movie_list:
        movie_id = movies.iloc[i[0]].movie_id
        title = movies.iloc[i[0]].title
        
        # Fetch all the rich data
        poster, rating, year, trailer = fetch_details(movie_id)
        
        rec_data.append({
            "title": title,
            "poster": poster,
            "rating": rating,
            "year": year,
            "trailer": trailer
        })
        
    return rec_data

movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)

def load_data(base_name):
   
    if os.path.exists(base_name):
        return pickle.load(open(base_name, 'rb'))
    
    # If not, glue the split parts together (deployment)
    combined_data = b""
    part_num = 1
    while True:
        part_name = f"{base_name}.part{part_num}"
        try:
            with open(part_name, 'rb') as f:
                combined_data += f.read()
            part_num += 1
        except FileNotFoundError:
            break
            
    if not combined_data:
        return None 
        
    return pickle.loads(combined_data)

similarity = load_data('similarity.pkl')

st.title("Movie Recommender System")

selected_movie_name = st.selectbox(
    'Choose a movie to recommend',
    movies['title'].values
)

if st.button('Recommend'):
    recommendations = recommend(selected_movie_name)
    
   
    cols = st.columns(5)
    
    for col, movie in zip(cols, recommendations):
        with col:
            # Display Title & Year
            st.markdown(f"**{movie['title']}**")
            st.caption(f"({movie['year']})")
            
            # Display Image
            st.image(movie['poster'])
            
            # Display Rating
            st.markdown(f"⭐ **{movie['rating']}/10**")
            
            # Display Trailer Button
            st.link_button("▶ Watch Trailer", movie['trailer'])
