Movie Recommender System

A content-based movie recommendation system built using Python and Streamlit.

This project was developed to suggest movies to users based on similarities in plot, genre, cast, and crew. It uses a dataset of over 5000 movies and applies cosine similarity to find the best matches.

How It Works
The system analyzes the metadata of the movie selected by the user. It processes information such as the movie overview, genre, keywords, cast, and director to create tags. These tags are then vectorized, and the system calculates the similarity distance between them to recommend the top 5 most similar movies.

Key Features
- Simple user interface built with Streamlit.
- Provides 5 movie recommendations with posters.
- Displays release year, star ratings, and cast information.
- Includes a direct link to watch the movie trailer on YouTube.

Tech Stack
- Python
- Streamlit (Web App Framework)
- Pandas (Data Analysis)
- Scikit-learn (Machine Learning/Similarity calculation)
- TMDB API (Real-time posters and movie details)

How to Run
1. Clone the repository.
2. Install the required libraries:
   pip install -r requirements.txt
3. Run the application:
   streamlit run app.py
