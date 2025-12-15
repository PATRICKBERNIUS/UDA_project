# Song Scraping and Lyric Sentiment Analysis


## Overview

This project scrapes song data from public Apple Music playlists,
performs sentiment analysis using several different methods (VADER,
TextBlob, and Transformer models), and reorders playlists from happiest
to saddest songs. The project uses the Genius API to extract lyrics and
provides visualizations of sentiment rankings.

## Usage Pipeline

The project includes a complete pipeline function that handles all steps
from playlist URL to sentiment-ranked resul Creating functions and
pipeline for different playlists:

### Example Usage

``` python
test_url = "https://music.apple.com/us/playlist/best-of-the-best/pl.u-XkD0YzMfDYd17j9"

# Run the complete analysis pipeline
fig, sorted_df = analyze_playlist(test_url, model='textblob')
```

### Results Visualization

![Sentiment ranking](sentiment_ranking.png)
