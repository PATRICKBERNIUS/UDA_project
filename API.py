from fastapi import FastAPI
from pydantic import BaseModel
import os

os.environ["TOKENIZERS_PARALLELISM"] = "false"

# ✅ Import ONLY your pipeline function
from playlist_pipeline import (
    get_playlist_data,
    get_lyrics,
    analyze_sentiment
)

app = FastAPI(title="Playlist Sentiment API", version="1.0")


class PlaylistRequest(BaseModel):
    playlist_url: str
    model: str = "vader"


@app.get("/")
def home():
    return {"status": "API is running"}


@app.post("/analyze_playlist")
def analyze_api(request: PlaylistRequest):

    songs_df = get_playlist_data(request.playlist_url)
    lyrics_df = get_lyrics(songs_df)
    analyzed_df = analyze_sentiment(lyrics_df, request.model)

    return {
        "model": request.model,
        "rows": len(analyzed_df),
        "results": analyzed_df.to_dict(orient="records")
    }
