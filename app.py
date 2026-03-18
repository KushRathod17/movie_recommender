import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ─── Page config (must be first Streamlit call) ───────────────────────────────
st.set_page_config(
    page_title="CineMatch — Movie Recommender",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── Cinematic CSS ────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:wght@300;400;500&display=swap');

/* ── Global reset ── */
html, body, .stApp {
    background-color: #0a0a0f !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif;
}

/* ── Hide Streamlit chrome ── */
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2rem 3rem 4rem; max-width: 1400px; }

/* ── Hero title ── */
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3rem, 8vw, 6rem);
    letter-spacing: 0.04em;
    line-height: 1;
    background: linear-gradient(135deg, #ff3b3b 0%, #ff8c42 60%, #ffd166 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0;
}
.hero-sub {
    font-size: 1rem;
    color: #7a7870;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    margin-top: 0.3rem;
    margin-bottom: 2.5rem;
}

/* ── Select box ── */
.stSelectbox label { color: #7a7870 !important; font-size: 0.8rem !important; letter-spacing: 0.1em; text-transform: uppercase; }
.stSelectbox > div > div {
    background-color: #14141e !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 10px !important;
    color: #e8e6e0 !important;
}

/* ── Primary button ── */
.stButton > button {
    background: linear-gradient(135deg, #ff3b3b, #c0392b) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.95rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    cursor: pointer !important;
    transition: opacity 0.2s, transform 0.15s !important;
    width: 100% !important;
}
.stButton > button:hover { opacity: 0.88 !important; transform: translateY(-1px) !important; }

/* ── Movie card ── */
.movie-card {
    background: #14141e;
    border: 1px solid #1e1e2e;
    border-radius: 14px;
    overflow: hidden;
    transition: transform 0.25s, border-color 0.25s, box-shadow 0.25s;
    height: 100%;
}
.movie-card:hover {
    transform: translateY(-6px);
    border-color: #ff3b3b55;
    box-shadow: 0 12px 40px rgba(255, 59, 59, 0.15);
}
.movie-card img { width: 100%; border-radius: 0; display: block; }
.movie-card-body { padding: 0.9rem 1rem 1rem; }
.movie-card-title {
    font-family: 'DM Sans', sans-serif;
    font-weight: 500;
    font-size: 0.92rem;
    color: #e8e6e0;
    margin-bottom: 0.25rem;
    line-height: 1.3;
    white-space: nowrap;
    overflow: hidden;
    text-overflow: ellipsis;
}
.movie-card-meta { font-size: 0.78rem; color: #7a7870; margin-bottom: 0.4rem; }
.movie-card-genres { display: flex; flex-wrap: wrap; gap: 4px; margin-bottom: 0.6rem; }
.genre-tag {
    background: #1e1e2e;
    color: #a09e98;
    border-radius: 20px;
    padding: 2px 9px;
    font-size: 0.7rem;
    letter-spacing: 0.05em;
    border: 1px solid #2a2a38;
}
.movie-card-overview {
    font-size: 0.78rem;
    color: #5a5850;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 0.75rem;
}

/* ── Trailer link button ── */
.trailer-btn {
    display: inline-block;
    background: transparent;
    border: 1px solid #2a2a38;
    color: #a09e98 !important;
    border-radius: 8px;
    padding: 5px 14px;
    font-size: 0.78rem;
    text-decoration: none !important;
    transition: border-color 0.2s, color 0.2s;
    letter-spacing: 0.05em;
}
.trailer-btn:hover { border-color: #ff3b3b; color: #ff3b3b !important; }

/* ── Section headers ── */
.section-label {
    font-size: 0.75rem;
    color: #7a7870;
    text-transform: uppercase;
    letter-spacing: 0.15em;
    margin-bottom: 1rem;
    padding-bottom: 0.5rem;
    border-bottom: 1px solid #1e1e2e;
}

/* ── Sidebar ── */
section[data-testid="stSidebar"] {
    background-color: #0d0d15 !important;
    border-right: 1px solid #1e1e2e !important;
}
section[data-testid="stSidebar"] .stSelectbox label,
section[data-testid="stSidebar"] p,
section[data-testid="stSidebar"] label { color: #7a7870 !important; font-size: 0.8rem !important; }
section[data-testid="stSidebar"] h3 { color: #e8e6e0 !important; font-size: 0.85rem !important; font-weight: 500 !important; letter-spacing: 0.1em !important; text-transform: uppercase !important; }

/* ── History pill buttons ── */
.stButton.hist-btn > button {
    background: #14141e !important;
    border: 1px solid #2a2a38 !important;
    border-radius: 20px !important;
    padding: 0.3rem 1rem !important;
    font-size: 0.78rem !important;
    color: #a09e98 !important;
    text-transform: none !important;
    letter-spacing: 0 !important;
    width: auto !important;
}

/* ── Divider ── */
hr { border-color: #1e1e2e !important; }

/* ── Success / info messages ── */
.stSuccess, .stInfo { background: #14141e !important; border-color: #2a2a38 !important; }
</style>
""", unsafe_allow_html=True)

# ─── API key ──────────────────────────────────────────────────────────────────
my_api_key = st.secrets["tmdb_key"]

# ─── Session state init ───────────────────────────────────────────────────────
if 'watchlist' not in st.session_state:
    st.session_state.watchlist = []
if 'search_history' not in st.session_state:
    st.session_state.search_history = []
if 'recommendations' not in st.session_state:
    st.session_state.recommendations = []
if 'last_movie' not in st.session_state:
    st.session_state.last_movie = None

# ─── TMDB fetch ───────────────────────────────────────────────────────────────
def fetch_details(movie_id):
    try:
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={my_api_key}&language=en-US"
        data = requests.get(url, timeout=5).json()

        poster = ("https://image.tmdb.org/t/p/w500" + data['poster_path']
                  if data.get('poster_path')
                  else "https://via.placeholder.com/500x750?text=No+Image")

        rating   = round(data.get('vote_average', 0), 1)
        year     = data.get('release_date', 'N/A')[:4]
        overview = data.get('overview', 'No description available.')
        genres   = [g['name'] for g in data.get('genres', [])][:3]
        runtime  = data.get('runtime', 0)
        runtime_str = f"{runtime // 60}h {runtime % 60}m" if runtime else "N/A"

        # Trailer
        vdata = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={my_api_key}&language=en-US",
            timeout=5
        ).json()
        trailer_url = next(
            (f"https://www.youtube.com/watch?v={v['key']}"
             for v in vdata.get('results', [])
             if v['type'] == 'Trailer' and v['site'] == 'YouTube'),
            f"https://www.youtube.com/results?search_query={data.get('title', '')}+official+trailer"
        )

        return {
            "title":    data.get('title', 'Unknown'),
            "poster":   poster,
            "rating":   rating,
            "year":     year,
            "overview": overview,
            "genres":   genres,
            "runtime":  runtime_str,
            "trailer":  trailer_url,
        }
    except Exception:
        return {
            "title": "Unknown", "poster": "https://via.placeholder.com/500x750?text=Error",
            "rating": 0, "year": "N/A", "overview": "", "genres": [], "runtime": "N/A",
            "trailer": "https://www.youtube.com",
        }

# ─── Recommend logic ──────────────────────────────────────────────────────────
def recommend(movie, genre_filter="All", num=5):
    idx       = movies[movies['title'] == movie].index[0]
    distances = similarity[idx]
    movie_list = sorted(enumerate(distances), key=lambda x: x[1], reverse=True)[1:]

    results = []
    for i, _ in movie_list:
        if len(results) >= num:
            break
        movie_id = movies.iloc[i].movie_id
        details  = fetch_details(movie_id)
        if genre_filter != "All" and genre_filter not in details['genres']:
            continue
        results.append(details)
    return results

# ─── Data loading ─────────────────────────────────────────────────────────────
movies_dict = pickle.load(open('movies.pkl', 'rb'))
movies      = pd.DataFrame(movies_dict)

def load_similarity(base_name):
    if os.path.exists(base_name):
        return pickle.load(open(base_name, 'rb'))
    data, n = b"", 1
    while True:
        part = f"{base_name}.part{n}"
        try:
            data += open(part, 'rb').read()
            n += 1
        except FileNotFoundError:
            break
    return pickle.loads(data) if data else None

similarity = load_similarity('similarity.pkl')

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛 Filters")
    genre_filter = st.selectbox(
        "Genre",
        ["All", "Action", "Comedy", "Drama", "Horror", "Romance",
         "Thriller", "Science Fiction", "Animation", "Crime", "Adventure"],
    )
    num_recs = st.slider("Results", min_value=3, max_value=10, value=5)

    st.markdown("---")

    # Search history
    if st.session_state.search_history:
        st.markdown("### 🕐 Recent Searches")
        for past_movie in st.session_state.search_history:
            if st.button(f"↩ {past_movie}", key=f"hist_{past_movie}"):
                st.session_state.last_movie  = past_movie
                st.session_state.recommendations = recommend(past_movie, genre_filter, num_recs)
        if st.button("Clear history", key="clear_hist"):
            st.session_state.search_history = []
            st.rerun()

    st.markdown("---")

    # Watchlist count
    wl_count = len(st.session_state.watchlist)
    st.markdown(f"### 📋 Watchlist ({wl_count})")
    if wl_count == 0:
        st.caption("Nothing saved yet.")
    if wl_count > 0 and st.button("🗑 Clear Watchlist"):
        st.session_state.watchlist = []
        st.rerun()

# ─── Hero header ──────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">CineMatch</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Discover your next favourite film</div>', unsafe_allow_html=True)

# ─── Search bar ───────────────────────────────────────────────────────────────
col_sel, col_btn = st.columns([4, 1])
with col_sel:
    selected_movie = st.selectbox(
        "Pick a movie you love",
        movies['title'].values,
        label_visibility="collapsed",
    )
with col_btn:
    search_clicked = st.button("Find Movies")

# ─── Trigger recommendation ───────────────────────────────────────────────────
if search_clicked:
    with st.spinner("Finding movies you'll love..."):
        recs = recommend(selected_movie, genre_filter, num_recs)
    st.session_state.recommendations = recs
    st.session_state.last_movie      = selected_movie

    # Update search history
    if selected_movie in st.session_state.search_history:
        st.session_state.search_history.remove(selected_movie)
    st.session_state.search_history.insert(0, selected_movie)
    st.session_state.search_history = st.session_state.search_history[:10]

# ─── Display recommendations ─────────────────────────────────────────────────
if st.session_state.recommendations:
    st.markdown(f'<div class="section-label">Because you liked &nbsp;<strong style="color:#e8e6e0">{st.session_state.last_movie}</strong></div>', unsafe_allow_html=True)

    cols = st.columns(len(st.session_state.recommendations))
    for col, movie in zip(cols, st.session_state.recommendations):
        with col:
            # Build genre tags HTML
            tags_html = "".join(f'<span class="genre-tag">{g}</span>' for g in movie['genres'])
            in_watchlist = any(m['title'] == movie['title'] for m in st.session_state.watchlist)

            st.markdown(f"""
            <div class="movie-card">
                <img src="{movie['poster']}" alt="{movie['title']}"/>
                <div class="movie-card-body">
                    <div class="movie-card-title">{movie['title']}</div>
                    <div class="movie-card-meta">
                        {movie['year']} &nbsp;·&nbsp; ⭐ {movie['rating']} &nbsp;·&nbsp; 🕐 {movie['runtime']}
                    </div>
                    <div class="movie-card-genres">{tags_html}</div>
                    <div class="movie-card-overview">{movie['overview']}</div>
                    <a href="{movie['trailer']}" target="_blank" class="trailer-btn">▶ Trailer</a>
                </div>
            </div>
            """, unsafe_allow_html=True)

            # Watchlist button below card
            btn_label = "✓ Saved" if in_watchlist else "+ Watchlist"
            if st.button(btn_label, key=f"wl_{movie['title']}"):
                if not in_watchlist:
                    st.session_state.watchlist.append(movie)
                    st.rerun()

# ─── Watchlist section ────────────────────────────────────────────────────────
if st.session_state.watchlist:
    st.markdown("---")
    st.markdown('<div class="section-label">My Watchlist</div>', unsafe_allow_html=True)
    wl_cols = st.columns(min(len(st.session_state.watchlist), 5))
    for wc, wm in zip(wl_cols, st.session_state.watchlist):
        with wc:
            st.image(wm['poster'], use_container_width=True)
            st.caption(f"**{wm['title']}**  \n{wm['year']} · ⭐ {wm['rating']}")
