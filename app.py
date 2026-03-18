import streamlit as st
import pickle
import pandas as pd
import requests
import os

# ─── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="CineMatch",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ─── CSS ──────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Bebas+Neue&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

html, body, .stApp {
    background-color: #0a0a0f !important;
    color: #e8e6e0 !important;
    font-family: 'DM Sans', sans-serif;
}
#MainMenu, footer, header { visibility: hidden; }
.block-container { padding: 2.5rem 3rem 5rem; max-width: 1300px; }

/* Hero */
.hero-title {
    font-family: 'Bebas Neue', sans-serif;
    font-size: clamp(3.5rem, 7vw, 6rem);
    letter-spacing: 0.05em;
    line-height: 1;
    background: linear-gradient(120deg, #ff3b3b 0%, #ff7043 55%, #ffd166 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}
.hero-sub {
    font-size: 0.82rem;
    color: #555048;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    margin-top: 0.2rem;
    margin-bottom: 2.5rem;
}

/* Selectbox */
.stSelectbox label { color: #555048 !important; font-size: 0.78rem !important; letter-spacing: 0.1em; text-transform: uppercase; }
.stSelectbox > div > div {
    background-color: #13131c !important;
    border: 1px solid #222230 !important;
    border-radius: 10px !important;
    color: #e8e6e0 !important;
}

/* All Streamlit buttons — small pill style */
div[data-testid="stButton"] > button {
    background: transparent !important;
    color: #8a8880 !important;
    border: 1px solid #252535 !important;
    border-radius: 8px !important;
    padding: 0.3rem 1rem !important;
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.75rem !important;
    font-weight: 400 !important;
    letter-spacing: 0.05em !important;
    text-transform: none !important;
    width: 100% !important;
    transition: border-color 0.2s, color 0.2s !important;
}
div[data-testid="stButton"] > button:hover {
    border-color: #ff3b3b88 !important;
    color: #ff7043 !important;
    background: #ff3b3b0a !important;
}
div[data-testid="stButton"] > button:disabled {
    border-color: #ff3b3b44 !important;
    color: #ff6b6b !important;
    opacity: 1 !important;
}

/* The single "Recommend" button — make it stand out */
.recommend-btn div[data-testid="stButton"] > button {
    background: linear-gradient(135deg, #ff3b3b, #c0392b) !important;
    color: #fff !important;
    border: none !important;
    font-size: 0.88rem !important;
    padding: 0.6rem 1rem !important;
    letter-spacing: 0.1em !important;
    text-transform: uppercase !important;
}

/* Movie card */
.movie-card {
    background: #13131c;
    border: 1px solid #1c1c28;
    border-radius: 14px;
    overflow: hidden;
    transition: transform 0.25s ease, box-shadow 0.25s ease, border-color 0.25s ease;
    margin-bottom: 4px;
}
.movie-card:hover {
    transform: translateY(-6px);
    box-shadow: 0 14px 44px rgba(255,59,59,0.1);
    border-color: #ff3b3b33;
}
.movie-card img {
    width: 100%;
    aspect-ratio: 2/3;
    object-fit: cover;
    display: block;
}
.card-body { padding: 12px 13px 14px; }
.card-title {
    font-weight: 500;
    font-size: 0.88rem;
    color: #e8e6e0;
    margin-bottom: 4px;
    line-height: 1.3;
    display: -webkit-box;
    -webkit-line-clamp: 2;
    -webkit-box-orient: vertical;
    overflow: hidden;
    min-height: 2.2em;
}
.card-meta { font-size: 0.72rem; color: #555048; margin-bottom: 7px; }
.card-genres { display: flex; flex-wrap: wrap; gap: 3px; margin-bottom: 8px; }
.genre-pill {
    background: #1c1c28;
    color: #6a6860;
    border: 1px solid #252535;
    border-radius: 20px;
    padding: 1px 8px;
    font-size: 0.66rem;
}
.card-overview {
    font-size: 0.73rem;
    color: #42403a;
    font-style: italic;
    line-height: 1.5;
    display: -webkit-box;
    -webkit-line-clamp: 3;
    -webkit-box-orient: vertical;
    overflow: hidden;
    margin-bottom: 10px;
    min-height: 3.3em;
}
.btn-trailer {
    display: block;
    text-align: center;
    background: transparent;
    border: 1px solid #252535;
    color: #6a6860 !important;
    border-radius: 8px;
    padding: 5px 0;
    font-size: 0.73rem;
    text-decoration: none !important;
    transition: border-color 0.2s, color 0.2s;
    margin-bottom: 6px;
}
.btn-trailer:hover { border-color: #ff3b3b; color: #ff7043 !important; }

/* Section label */
.section-label {
    font-size: 0.72rem;
    color: #555048;
    text-transform: uppercase;
    letter-spacing: 0.18em;
    padding-bottom: 10px;
    border-bottom: 1px solid #1c1c28;
    margin-bottom: 1rem;
}
.section-label strong { color: #c8c6c0; }

/* Sidebar */
section[data-testid="stSidebar"] {
    background-color: #0d0d15 !important;
    border-right: 1px solid #1c1c28 !important;
}
section[data-testid="stSidebar"] h3 {
    color: #e8e6e0 !important;
    font-size: 0.78rem !important;
    font-weight: 500 !important;
    letter-spacing: 0.14em !important;
    text-transform: uppercase !important;
}
section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] p { color: #555048 !important; font-size: 0.78rem !important; }

hr { border-color: #1c1c28 !important; margin: 2rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ─── API Key ──────────────────────────────────────────────────────────────────
my_api_key = st.secrets["tmdb_key"]

# ─── Session State ────────────────────────────────────────────────────────────
for key, default in [
    ('watchlist', []),
    ('search_history', []),
    ('recommendations', []),
    ('last_movie', None),
]:
    if key not in st.session_state:
        st.session_state[key] = default

# ─── TMDB Fetch ───────────────────────────────────────────────────────────────
def fetch_details(movie_id):
    try:
        data = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={my_api_key}&language=en-US",
            timeout=5
        ).json()

        poster = ("https://image.tmdb.org/t/p/w500" + data['poster_path']
                  if data.get('poster_path')
                  else "https://via.placeholder.com/500x750/13131c/555048?text=No+Poster")

        year     = data.get('release_date', 'N/A')[:4]
        rating   = round(data.get('vote_average', 0), 1)
        overview = data.get('overview', '')
        genres   = [g['name'] for g in data.get('genres', [])][:3]
        rt       = data.get('runtime', 0)
        runtime  = f"{rt//60}h {rt%60}m" if rt else "N/A"

        vdata = requests.get(
            f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={my_api_key}&language=en-US",
            timeout=5
        ).json()
        trailer = next(
            (f"https://www.youtube.com/watch?v={v['key']}"
             for v in vdata.get('results', [])
             if v['type'] == 'Trailer' and v['site'] == 'YouTube'),
            f"https://www.youtube.com/results?search_query={data.get('title', '')}+trailer"
        )

        return dict(
            title=data.get('title', 'Unknown'),
            poster=poster, year=year, rating=rating,
            overview=overview, genres=genres,
            runtime=runtime, trailer=trailer,
        )
    except Exception:
        return dict(
            title='Unknown',
            poster='https://via.placeholder.com/500x750/13131c/555048?text=Error',
            year='N/A', rating=0, overview='', genres=[], runtime='N/A',
            trailer='https://www.youtube.com',
        )

# ─── Recommend ────────────────────────────────────────────────────────────────
def recommend(movie, genre_filter="All", num=5):
    idx      = movies[movies['title'] == movie].index[0]
    ranked   = sorted(enumerate(similarity[idx]), key=lambda x: x[1], reverse=True)[1:]
    results  = []
    for i, _ in ranked:
        if len(results) >= num:
            break
        details = fetch_details(int(movies.iloc[i].movie_id))
        if genre_filter != "All" and genre_filter not in details['genres']:
            continue
        results.append(details)
    return results

# ─── Load Data ────────────────────────────────────────────────────────────────
movies = pd.DataFrame(pickle.load(open('movies.pkl', 'rb')))

def load_similarity(base):
    if os.path.exists(base):
        return pickle.load(open(base, 'rb'))
    raw, n = b"", 1
    while True:
        try:
            raw += open(f"{base}.part{n}", 'rb').read(); n += 1
        except FileNotFoundError:
            break
    return pickle.loads(raw) if raw else None

similarity = load_similarity('similarity.pkl')

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 🎛 Filters")
    genre_filter = st.selectbox("Genre", [
        "All", "Action", "Comedy", "Drama", "Horror", "Romance",
        "Thriller", "Science Fiction", "Animation", "Crime", "Adventure", "Fantasy",
    ])
    num_recs = st.slider("Results", 3, 10, 5)

    st.markdown("---")

    if st.session_state.search_history:
        st.markdown("### 🕐 Recent")
        for past in st.session_state.search_history:
            if st.button(f"↩ {past}", key=f"h_{past}"):
                with st.spinner("Loading..."):
                    st.session_state.recommendations = recommend(past, genre_filter, num_recs)
                    st.session_state.last_movie = past
        if st.button("✕ Clear history", key="clrhist"):
            st.session_state.search_history = []
            st.rerun()

    st.markdown("---")
    wl = st.session_state.watchlist
    st.markdown(f"### 📋 Watchlist ({len(wl)})")
    if not wl:
        st.caption("Nothing saved yet.")
    else:
        if st.button("🗑 Clear all", key="clrwl"):
            st.session_state.watchlist = []
            st.rerun()

# ─── Hero ─────────────────────────────────────────────────────────────────────
st.markdown('<div class="hero-title">CineMatch</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Discover your next favourite film</div>', unsafe_allow_html=True)

# ─── Search Row ───────────────────────────────────────────────────────────────
c1, c2 = st.columns([5, 1])
with c1:
    selected = st.selectbox("movie", movies['title'].values, label_visibility="collapsed")
with c2:
    st.markdown('<div class="recommend-btn">', unsafe_allow_html=True)
    go = st.button("Recommend ›")
    st.markdown('</div>', unsafe_allow_html=True)

# ─── Trigger ──────────────────────────────────────────────────────────────────
if go:
    with st.spinner("Finding movies you'll love…"):
        recs = recommend(selected, genre_filter, num_recs)
    st.session_state.recommendations = recs
    st.session_state.last_movie = selected
    hist = st.session_state.search_history
    if selected in hist:
        hist.remove(selected)
    hist.insert(0, selected)
    st.session_state.search_history = hist[:10]

# ─── Results ──────────────────────────────────────────────────────────────────
recs = st.session_state.recommendations
if recs:
    lm = st.session_state.last_movie
    st.markdown(f'<div class="section-label">Because you liked &nbsp;<strong>{lm}</strong></div>', unsafe_allow_html=True)

    # Render in rows of 5
    for row_start in range(0, len(recs), 5):
        row = recs[row_start:row_start + 5]
        cols = st.columns(5)

        for col, movie in zip(cols, row):
            with col:
                in_wl     = any(m['title'] == movie['title'] for m in st.session_state.watchlist)
                tags_html = "".join(f'<span class="genre-pill">{g}</span>' for g in movie['genres'])

                # HTML card (poster + info + trailer link)
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{movie['poster']}" alt="{movie['title']}" loading="lazy"/>
                    <div class="card-body">
                        <div class="card-title">{movie['title']}</div>
                        <div class="card-meta">{movie['year']} &nbsp;·&nbsp; ⭐ {movie['rating']} &nbsp;·&nbsp; {movie['runtime']}</div>
                        <div class="card-genres">{tags_html}</div>
                        <div class="card-overview">{movie['overview'] or 'No description available.'}</div>
                        <a href="{movie['trailer']}" target="_blank" class="btn-trailer">▶ Watch Trailer</a>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                # Watchlist button — kept outside card HTML so Streamlit handles state
                if not in_wl:
                    if st.button("+ Watchlist", key=f"wl_{row_start}_{movie['title']}"):
                        st.session_state.watchlist.append(movie)
                        st.rerun()
                else:
                    st.button("✓ Saved", key=f"sv_{row_start}_{movie['title']}", disabled=True)

# ─── Watchlist ────────────────────────────────────────────────────────────────
wl = st.session_state.watchlist
if wl:
    st.markdown("---")
    st.markdown('<div class="section-label">My Watchlist</div>', unsafe_allow_html=True)
    wl_cols = st.columns(min(len(wl), 8))
    for wc, wm in zip(wl_cols, wl):
        with wc:
            st.image(wm['poster'], use_container_width=True)
            st.caption(f"**{wm['title']}**  \n{wm['year']} · ⭐ {wm['rating']}")
