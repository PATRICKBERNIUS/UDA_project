import streamlit as st
import pandas as pd
import requests
import re
import time
import lyricsgenius
from tqdm import tqdm
import plotly.express as px

# Configure page
st.set_page_config(
    page_title="Playlist Sentiment Analyzer",
    page_icon="🎵",
    layout="wide"
)

# ============================================================
# CONFIGURATION
# ============================================================

GENIUS_TOKEN = st.secrets["GENIUS_TOKEN"]

headers = {
    "user-Agent": "Mozilla/5.0",
    "Authorization": st.secrets["Authorization"],
    "Media-User-Token": st.secrets["Media_User_Token"],
    "Referer": "https://music.apple.com/",
    "Origin": "https://music.apple.com"
}

# ============================================================
# HELPER FUNCTIONS
# ============================================================

def extract_id(playlist_url):
    return playlist_url.rstrip('/').split('/')[-1]

def get_playlist_data(playlist_url):
    playlist_id = extract_id(playlist_url)
    base_url = f"https://amp-api.music.apple.com/v1/catalog/us/playlists/{playlist_id}"
    query = "?art%5Burl%5D=f&extend=editorialArtwork%2CeditorialVideo&fields%5Balbums%5D=name%2Cartwork&fields%5Bartists%5D=name%2Cartwork&fields%5Bsongs%5D=name%2CartistName%2CalbumName%2Curl%2CdurationInMillis&format%5Bresources%5D=map&include=tracks&l=en-US&limit%5Btracks%5D=300"
    
    r = requests.get(base_url + query, headers=headers)
    r.raise_for_status()
    data = r.json()
    
    song_data = data['resources']['songs']
    songs_list = [re.sub(r"\(.+\)", '', s['attributes']['name']).strip() 
                  for s in song_data.values()]
    artist_list = [s['attributes']['artistName'] for s in song_data.values()]
    
    return pd.DataFrame({"song": songs_list, "artist": artist_list})

def get_lyrics(df):
    songs_dict = dict(zip(df['song'], df['artist']))
    LyricsGenius = lyricsgenius.Genius(GENIUS_TOKEN, timeout=15, sleep_time=1, retries=3)
    
    all_lyrics = []
    progress_bar = st.progress(0)
    total = len(songs_dict)
    
    for idx, (song, artist) in enumerate(songs_dict.items(), 1):
        progress_bar.progress(idx / total)
        artist_search = re.split('&|,', artist)[0].strip()
        
        try:
            search = LyricsGenius.search_song(song, artist_search)
            lyrics = search.lyrics if search else ""
        except:
            lyrics = ""
        
        all_lyrics.append({'lyrics': lyrics, 'song': song, 'artist': artist})
        time.sleep(0.5)
    
    lyrics_df = pd.DataFrame(all_lyrics)
    lyrics_df['lyrics'] = (
        lyrics_df['lyrics']
        .str.replace(r'\n', ' ', regex=True)
        .str.replace(r'([a-z])([A-Z])', r'\1 \2', regex=True)
        .str.replace(r'\[.*?\]', ' ', regex=True)
        .str.replace(r'^.*Lyrics ', '', regex=True)
        .str.replace(r'\u2005', '', regex=True)
    )
    
    return lyrics_df

def vader_sentiment(df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    vader = SentimentIntensityAnalyzer()
    
    progress_bar = st.progress(0)
    vader_polars = []
    
    for idx, lyrics in enumerate(df['lyrics'], 1):
        progress_bar.progress(idx / len(df))
        vader_polars.append(vader.polarity_scores(lyrics).get('compound'))
    
    df = df.copy()
    df['sentiment'] = vader_polars
    return df

def textblob_sentiment(df):
    import textblob
    from textblob.sentiments import NaiveBayesAnalyzer
    
    progress_bar = st.progress(0)
    classss, pos, neg = [], [], []
    
    for idx, lyrics in enumerate(df['lyrics'], 1):
        progress_bar.progress(idx / len(df))
        output = textblob.TextBlob(lyrics, analyzer=NaiveBayesAnalyzer()).sentiment
        classss.append(output[0])
        pos.append(output[1])
        neg.append(output[2])
    
    df = df.copy()
    df['classification'] = classss
    df['pos'] = pos
    df['neg'] = neg
    return df

def transformer_sentiment(df):
    from transformers import pipeline
    
    sentiment_analysis = pipeline(
        'sentiment-analysis',
        model='siebert/sentiment-roberta-large-english',
        truncation=True,
        max_length=512
    )
    
    progress_bar = st.progress(0)
    trans_list = []
    
    for idx, lyrics in enumerate(df['lyrics'], 1):
        progress_bar.progress(idx / len(df))
        result = sentiment_analysis(lyrics)
        trans_list.append((result[0]['label'], result[0]['score']))
    
    df = df.copy()
    df[['label', 'score']] = trans_list
    return df

def analyze_sentiment(lyrics_df, model='vader'):
    if model.lower() == 'vader':
        return vader_sentiment(lyrics_df)
    elif model.lower() == 'textblob':
        return textblob_sentiment(lyrics_df)
    elif model.lower() == 'transformer':
        return transformer_sentiment(lyrics_df)
    else:
        raise ValueError("Invalid model")

def convert_to_neg(df):
    df = df.copy()
    df['score'] = df['score'].where(df['label'] == 'POSITIVE', -df['score'])
    return df

def rank_and_plot(df, model):
    if model.lower() == 'vader':
        sorted_df = df.sort_values(by='sentiment', ascending=False)
        fig = px.line(sorted_df, x='song', y='sentiment', title='VADER Rankings')
        return fig, sorted_df
    
    elif model.lower() == 'textblob':
        sorted_df = df.sort_values(by='pos', ascending=False)
        fig = px.line(sorted_df, x='song', y='pos', title='TextBlob Rankings')
        return fig, sorted_df
    
    else:  # transformer
        df = convert_to_neg(df)
        sorted_df = df.sort_values(by='score', ascending=False)
        fig = px.line(sorted_df, x='song', y='score', title='Transformer Rankings')
        return fig, sorted_df

# ============================================================
# STREAMLIT UI
# ============================================================

# Initialize session state
if 'lyrics_df' not in st.session_state:
    st.session_state.lyrics_df = None
if 'current_url' not in st.session_state:
    st.session_state.current_url = None

st.title("🎵 Playlist Sentiment Analyzer")
st.markdown("""
Analyze the sentiment of songs in your Apple Music playlist and reorder them from most to least positive!

**How to use:**
1. Open your Apple Music playlist
2. Click the three dots (⋯) → Share → Copy Link
3. Paste the link below
4. Choose a sentiment analysis model
5. Click "Analyze Playlist"
""")

# Input
playlist_url = st.text_input(
    "Apple Music Playlist URL:",
    placeholder="https://music.apple.com/us/playlist/...",
    value="https://music.apple.com/us/playlist/boston/pl.u-r2yBJJ4FPkKMbNm"
)

model_choice = st.selectbox(
    "Choose Sentiment Model:",
    ["VADER", "TextBlob", "Transformer"],
    help="VADER: Fast, good for social media text\nTextBlob: Classic NLP approach\nTransformer: Most accurate but slowest"
)

# Analyze button - only fetches lyrics if URL changed
if st.button("🚀 Analyze Playlist", type="primary"):
    if not playlist_url:
        st.error("Please enter a playlist URL!")
    else:
        try:
            # Only fetch lyrics if URL changed
            if st.session_state.current_url != playlist_url:
                with st.spinner("Fetching playlist songs and lyrics..."):
                    songs_df = get_playlist_data(playlist_url)
                    st.session_state.lyrics_df = get_lyrics(songs_df)
                    st.session_state.current_url = playlist_url
            
            # Run sentiment analysis on cached lyrics
            with st.spinner(f"Analyzing sentiment with {model_choice}..."):
                analyzed_df = analyze_sentiment(st.session_state.lyrics_df, model=model_choice.lower())
                fig, sorted_df = rank_and_plot(analyzed_df, model_choice.lower())
            
            st.success("✅ Analysis complete!")
            
            # Display results
            st.subheader("📊 Sentiment Rankings")
            st.plotly_chart(fig, use_container_width=True)
            
            st.subheader("📋 Ranked Songs")
            st.dataframe(sorted_df, use_container_width=True)
            
            # Download button
            csv = sorted_df.to_csv(index=False).encode('utf-8')
            st.download_button(
                "⬇️ Download Results as CSV",
                csv,
                "ranked_playlist.csv",
                "text/csv",
                key='download-csv'
            )
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.info("Make sure your playlist URL is correct and public!")

