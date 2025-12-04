import streamlit as st

# Configure Streamlit to use a wide layout
st.set_page_config(page_title="Lyrics Analyzer", layout="wide")
import requests
import pandas as pd
import re
import time
import lyricsgenius
import plotly.express as px

# ---------------------------
# INITIAL SESSION STATE
# ---------------------------
if "df_songs" not in st.session_state:
    st.session_state.df_songs = None
if "df_lyrics" not in st.session_state:
    st.session_state.df_lyrics = None
if "df_sent" not in st.session_state:
    st.session_state.df_sent = None
if "last_model" not in st.session_state:
    st.session_state.last_model = None


# ---------------------------
# HELPERS
# ---------------------------
def extract_id(playlist_url: str) -> str:
    return playlist_url.rstrip("/").split("/")[-1]


query = (
    "?art%5Burl%5D=f&extend=editorialArtwork%2CeditorialVideo"
    "&fields%5Balbums%5D=name%2Cartwork"
    "&fields%5Bartists%5D=name%2Cartwork"
    "&fields%5Bsongs%5D=name%2CartistName%2CalbumName%2Curl%2CdurationInMillis"
    "&format%5Bresources%5D=map&include=tracks"
    "&l=en-US&limit%5Btracks%5D=300"
)

headers = {
    "user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)",
    "Authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNzYyNTM4NTI0LCJleHAiOjE3Njk3OTYxMjQsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.2fpk1NEdRGBhrWjhjDJfeVWQyfa005cJYQ0Ye37GeD08vuyZvVA1xOc0JiePTEa9FLHa1HZjLd3n5F0CYUqLTw",
    "Media-User-Token": "AvxHFN2PzpRpIkzuoGPn9VeW7Hdx1Y5a8LLLsfVgOEiSBYJcUGycxXIjlw7eno8fDsWek35uL65oj+CZI9eY76CFQPx4QpkR31qMNGKjEHBYhhgfLdBlYQb4APuPFYJ45NJvSGT9A+jxFG+wQNYtQupM9JdrT4i64PV3XxKjwqhb+MFp1o9iy9BXVLTTDttyztXnZJbI6aV1s8hgURZWnT6FhdOtjzTkTRHiNcuO0CwT+VnvKw==",
    "Referer": "https://music.apple.com/",
    "Origin": "https://music.apple.com"
}


def fetch_playlist(playlist_url: str):
    playlist_id = extract_id(playlist_url)
    url = f"https://amp-api.music.apple.com/v1/catalog/us/playlists/{playlist_id}{query}"

    r = requests.get(url, headers=headers)
    r.raise_for_status()
    data = r.json()

    songs_json = data.get("resources", {}).get("songs", {})
    if not songs_json:
        raise ValueError("Playlist not found or Apple token expired.")

    songs = [
        re.sub(r"\(.+\)", "", s["attributes"]["name"]).strip()
        for s in songs_json.values()
    ]
    artists = [s["attributes"]["artistName"] for s in songs_json.values()]

    df = pd.DataFrame({"song": songs, "artist": artists})
    return df, dict(zip(songs, artists))


def fetch_lyrics_for_songs(songs_dict: dict, token: str):
    genius = lyricsgenius.Genius(token, timeout=15, sleep_time=1, retries=3)

    results = []
    progress = st.progress(0)
    total = max(len(songs_dict), 1)

    for i, (song, artist) in enumerate(songs_dict.items(), start=1):
        progress.progress(i / total)

        main_artist = re.split("&|,", artist)[0].strip()

        try:
            found = genius.search_song(song, main_artist)
            lyrics = found.lyrics if found else ""
        except Exception:
            lyrics = ""

        results.append({"song": song, "artist": artist, "lyrics": lyrics})
        time.sleep(0.2)

    df = pd.DataFrame(results)

    df["lyrics"] = (
        df["lyrics"]
        .str.replace(r"\n", " ", regex=True)
        .str.replace(r"([a-z])([A-Z])", r"\1 \2", regex=True)
        .str.replace(r"\[.*?\]", " ", regex=True)
        .str.replace(r"^.*Lyrics ", "", regex=True)
        .str.replace(r"\u2005", "", regex=True)
    )

    return df


# ---------------------------
# SENTIMENT MODELS
# ---------------------------
def compute_textblob_sentiment(df):
    from textblob import TextBlob
    from textblob.sentiments import NaiveBayesAnalyzer

    df = df.copy()
    total = len(df)
    prog = st.progress(0)

    tb_class, tb_pos, tb_neg = [], [], []

    for i, lyr in enumerate(df["lyrics"], start=1):
        if not lyr:
            tb_class.append(None)
            tb_pos.append(0)
            tb_neg.append(0)
        else:
            s = TextBlob(lyr, analyzer=NaiveBayesAnalyzer()).sentiment
            tb_class.append(s.classification)
            tb_pos.append(getattr(s, "p_pos", s[1]))
            tb_neg.append(getattr(s, "p_neg", s[2]))

        prog.progress(i / total)

    df["tb_class"] = tb_class
    df["tb_pos"] = tb_pos
    df["tb_neg"] = tb_neg
    return df


def compute_vader_sentiment(df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer
    analyzer = SentimentIntensityAnalyzer()

    df = df.copy()
    total = len(df)
    prog = st.progress(0)

    scores = []
    for i, text in enumerate(df["lyrics"], start=1):
        scores.append(0 if not text else analyzer.polarity_scores(text)["compound"])
        prog.progress(i / total)

    df["vader"] = scores
    return df


def compute_transformer_sentiment(df):
    from transformers import pipeline
    pipe = pipeline(
        "sentiment-analysis",
        model="siebert/sentiment-roberta-large-english",
        truncation=True,
        max_length=512,
    )

    df = df.copy()
    total = len(df)
    prog = st.progress(0)

    labels, scores = [], []
    for i, text in enumerate(df["lyrics"], start=1):
        if not text:
            labels.append("NEUTRAL")
            scores.append(0)
        else:
            out = pipe(text)[0]
            labels.append(out["label"])
            scores.append(out.get("score", 0))

        prog.progress(i / total)

    df["trans_label"] = labels
    df["trans_score"] = scores
    df["trans_signed"] = df.apply(
        lambda r: r["trans_score"] if r["trans_label"] == "POSITIVE" else -r["trans_score"],
        axis=1,
    )
    return df


# ---------------------------
# PLOTS
# ---------------------------
def plot_blob(df):
    df_sorted = df.sort_values("tb_pos", ascending=False)
    return px.line(df_sorted, x="song", y="tb_pos", title="TextBlob Rankings")


def plot_vader(df):
    df_sorted = df.sort_values("vader", ascending=False)
    return px.line(df_sorted, x="song", y="vader", title="VADER Sentiment Rankings")


def plot_transformer(df):
    df_sorted = df.sort_values("trans_signed", ascending=False)
    return px.line(df_sorted, x="song", y="trans_signed", title="Transformer Sentiment Rankings")


# ---------------------------
# MAIN APP
# ---------------------------
def main():
    st.title("🎵 Simple Lyrics & Sentiment Analyzer")
    st.markdown("In your playlist, click the three dots at the top of the screen. Click 'copy link' (share → copy, if on mobile). Paste that link below.")

    playlist_url = st.text_input(
        "Apple Music Playlist URL:",
        value="https://music.apple.com/us/playlist/boston/pl.u-r2yBJJ4FPkKMbNm",
    )

    genius_token = "_sYrfS9alifx52SESlKPx5_gIqlcwL-gIjRTzXqylKxLUh0oGz5Ekjrcd4yTvbvS"

    # Load songs + lyrics
    if st.button("Load Playlist & Lyrics"):
        try:
            with st.spinner("Fetching playlist songs..."):
                df_songs, song_map = fetch_playlist(playlist_url)
                st.session_state.df_songs = df_songs

            with st.spinner("Fetching lyrics (this may take a bit)..."):
                df_lyrics = fetch_lyrics_for_songs(song_map, genius_token)
                st.session_state.df_lyrics = df_lyrics

            st.success("Lyrics loaded successfully!")

        except Exception as e:
            st.error(f"Error loading playlist: {e}")

    if st.session_state.df_lyrics is not None:
        st.write("### Lyrics Loaded")
        st.dataframe(st.session_state.df_lyrics, use_container_width=True)

    # ---------------------------
    # SENTIMENT ANALYSIS
    # ---------------------------
    st.markdown("---")
    st.subheader("Sentiment Analysis")

    model_choice = st.selectbox(
        "Choose a sentiment model:",
        ["TextBlob (NaiveBayes)", "VADER", "Transformer"],
    )

    if st.button("Run Sentiment Analysis"):
        df_base = st.session_state.df_lyrics.copy()

        if model_choice == "TextBlob (NaiveBayes)":
            df_sent = compute_textblob_sentiment(df_base)
        elif model_choice == "VADER":
            df_sent = compute_vader_sentiment(df_base)
        else:
            df_sent = compute_transformer_sentiment(df_base)

        st.session_state.df_sent = df_sent
        st.session_state.last_model = model_choice
        st.success("Sentiment analysis complete!")

    # ---------------------------
    # PERSISTENT DISPLAY
    # ---------------------------
    if st.session_state.df_sent is not None:
        df_sent = st.session_state.df_sent
        model_used = st.session_state.last_model

        st.write(f"### {model_used} Output")
        st.dataframe(df_sent, use_container_width=True)

        if model_used == "TextBlob (NaiveBayes)":
            fig = plot_blob(df_sent)
        elif model_used == "VADER":
            fig = plot_vader(df_sent)
        else:
            fig = plot_transformer(df_sent)

        st.plotly_chart(fig, use_container_width=True)

        # Sentiment CSV download
        st.download_button(
            "Download sentiment results as CSV",
            df_sent.to_csv(index=False).encode("utf-8"),
            "sentiment_results.csv",
            "text/csv",
        )

        # Reordered playlist download
        if model_used == "TextBlob (NaiveBayes)":
            col = "tb_pos"
        elif model_used == "VADER":
            col = "vader"
        else:
            col = "trans_signed"

        df_sorted = df_sent.sort_values(col, ascending=False)[["song", "artist"]]

        st.download_button(
            "⬇️ Download Reordered Playlist (Based on Sentiment)",
            df_sorted.to_csv(index=False).encode("utf-8"),
            "reordered_playlist.csv",
            "text/csv",
        )


if __name__ == "__main__":
    main()
