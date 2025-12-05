---
title: "Song Scraping and Lyric Sentiment Analysis"
format: gfm
jupyter: python3
---



This project attempted to scrape song data from public apple music playlists, perform sentiment analysis using several different methods, and reorder said playlist from happiest to saddest, plotting the results and providing a dataframe of the songs in their new order. Uses Genius's API to extract lyrics.


```{python}
import pandas as pd
from bs4 import BeautifulSoup
import requests


url = "https://music.apple.com/us/playlist/best-of-the-best/pl.u-XkD0YzMfDYd17j9"


#test url
boston_url = "https://music.apple.com/us/playlist/boston/pl.u-r2yBJJ4FPkKMbNm"


#function to extract the id from the url
def extract_id(playlist_url): 
    splits = playlist_url.split('/') #splitting on /
    id = splits[-1] #taking last group
    return id


#json request header
url2 = "https://amp-api.music.apple.com/v1/catalog/us/playlists/pl.u-XkD0YzMfDYd17j9?art%5Burl%5D=f&extend=editorialArtwork%2CeditorialVideo%2Coffers%2CseoDescription%2CseoTitle%2CtrackCount&fields%5Balbums%5D=name%2Cartwork%2CplayParams%2Curl&fields%5Bapple-curators%5D=name%2Curl&fields%5Bartists%5D=name%2Cartwork%2Curl&fields%5Bcurators%5D=name%2Curl&fields%5Bsongs%5D=name%2CartistName%2CcuratorName%2CcomposerName%2Cartwork%2CplayParams%2CcontentRating%2CalbumName%2Curl%2CdurationInMillis%2CaudioTraits%2CextendedAssetUrls&format%5Bresources%5D=map&include=tracks%2Ccurator&include%5Bmusic-videos%5D=artists&include%5Bsongs%5D=artists&l=en-US&limit%5Btracks%5D=300&limit%5Bview.featured-artists%5D=15&limit%5Bview.more-by-curator%5D=15&omit%5Bresource%5D=autos&platform=web&views=featured-artists%2Cmore-by-curator"


#public url
base_url = f"https://amp-api.music.apple.com/v1/catalog/us/playlists/{id}"

#ending for request 
query = "?art%5Burl%5D=f&extend=editorialArtwork%2CeditorialVideo%2Coffers%2CseoDescription%2CseoTitle%2CtrackCount&fields%5Balbums%5D=name%2Cartwork%2CplayParams%2Curl&fields%5Bapple-curators%5D=name%2Curl&fields%5Bartists%5D=name%2Cartwork%2Curl&fields%5Bcurators%5D=name%2Curl&fields%5Bsongs%5D=name%2CartistName%2CcuratorName%2CcomposerName%2Cartwork%2CplayParams%2CcontentRating%2CalbumName%2Curl%2CdurationInMillis%2CaudioTraits%2CextendedAssetUrls&format%5Bresources%5D=map&include=tracks%2Ccurator&include%5Bmusic-videos%5D=artists&include%5Bsongs%5D=artists&l=en-US&limit%5Btracks%5D=300&limit%5Bview.featured-artists%5D=15&limit%5Bview.more-by-curator%5D=15&omit%5Bresource%5D=autos&platform=web&views=featured-artists%2Cmore-by-curator"








headers = {"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNzYyNTM4NTI0LCJleHAiOjE3Njk3OTYxMjQsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.2fpk1NEdRGBhrWjhjDJfeVWQyfa005cJYQ0Ye37GeD08vuyZvVA1xOc0JiePTEa9FLHa1HZjLd3n5F0CYUqLTw",
            "Media-User-Token": "AvxHFN2PzpRpIkzuoGPn9VeW7Hdx1Y5a8LLLsfVgOEiSBYJcUGycxXIjlw7eno8fDsWek35uL65oj+CZI9eY76CFQPx4QpkR31qMNGKjEHBYhhgfLdBlYQb4APuPFYJ45NJvSGT9A+jxFG+wQNYtQupM9JdrT4i64PV3XxKjwqhb+MFp1o9iy9BXVLTTDttyztXnZJbI6aV1s8hgURZWnT6FhdOtjzTkTRHiNcuO0CwT+VnvKw==",
            "Referer": "https://music.apple.com/",
            "Origin": "https://music.apple.com"}


#st.markdown("In your playlist, click the three dots at the top of the screen. Click 'copy link' (share → copy, if on mobile). Paste that link below.")

r = requests.get(url, headers=headers)
r2 = requests.get(url2, headers=headers)


```



```{python}
#testing if function works on different playlists
boston_url = "https://music.apple.com/us/playlist/boston/pl.u-r2yBJJ4FPkKMbNm"

def extract_id(playlist_url):
    splits = playlist_url.split('/')
    id = splits[-1]
    return id


id = extract_id(boston_url)

base_url = f"https://amp-api.music.apple.com/v1/catalog/us/playlists/{id}"

json_url = base_url + query
boston_url = requests.get(json_url, headers=headers)
```





```{python}
import json
import re

#parsing json
data = r2.json()

#song data is nested here
song_data = data['resources']['songs']

#extracts all the names of the songs
songs_list = [song['attributes']['name'] for song in song_data.values()]
#removes parentheses and strops spaces
songs_list = [re.sub(r"\(.+\)", '', s).strip() for s in songs_list]


#extracting artist names
artist_list = [artist['attributes']['artistName'] for artist in song_data.values()]


#creating dataframe
df = pd.DataFrame({
    "song": songs_list, 
    "artist": artist_list})


#creating dictionary for searching
songs_dict = dict(zip(songs_list, artist_list))
songs_dict
```





```{python}
#genius API key
client_access_token = "_sYrfS9alifx52SESlKPx5_gIqlcwL-gIjRTzXqylKxLUh0oGz5Ekjrcd4yTvbvS"


import lyricsgenius
LyricsGenius = lyricsgenius.Genius(client_access_token, timeout=15, sleep_time=1, retries=3)

#test
song = LyricsGenius.search_song("Primetime", "JAY-Z")
lyrics = song.lyrics
lyrics
```








```{python}
import time
from tqdm import tqdm


all_lyrics = []
for song, artist in tqdm(songs_dict.items()): #for each song and artist
    artist_search = re.split('&|,', artist) #if multiple artists, take the first
    search = LyricsGenius.search_song(song, artist_search[0].strip()) #search through genius
    if search is None:
        print(f"No lyrics for {search}")
        continue #continue if no lyrics found
    lyrics = search.lyrics
    all_lyrics.append({'lyrics': lyrics,
                        'song': song,
                        'artist': artist}) 
    time.sleep(0.5)
all_lyrics
```






```{python}
from joblib import dump, load
#dump(all_lyrics, 'all_lyrics.joblib')
```


```{python}
lyrics_saved = load('all_lyrics.joblib')
lyrics_saved
```

```{python}
lyrics_df = pd.DataFrame(lyrics_saved)
lyrics_df

```




```{python}
#cleaning lyrics 

lyrics_df['lyrics'] = (
    lyrics_df['lyrics'].str.replace(r'\n', ' ', regex=True) #removes new line symbol
    .str.replace(r'([a-z])([A-Z])', '\\1 \\2', regex=True) #ensures spaces between words
    .str.replace(r'\[.*?\]', ' ', regex=True) #removes brackets
    .str.replace(r'^.*Lyrics ', '', regex=True) #removes everything before and including lyrics headers
    .str.replace(r'\u2005', '', regex=True) #removes this pattern which sometimes appears within lyrics
)
lyrics_df
```


Trying different sentiment analysis methods:



```{python}
#textblob method
from tqdm import tqdm
import textblob
from textblob.sentiments import NaiveBayesAnalyzer
import nltk

classss = [] 
pos = []
neg = []

for i in tqdm(lyrics_df['lyrics']): #loop through lyrics
  output = textblob.TextBlob(i, analyzer=NaiveBayesAnalyzer()).sentiment

  classss.append(output[0])
  pos.append(output[1])
  neg.append(output[2])


blob_lyrics_df = lyrics_df.copy()

blob_lyrics_df['classification'] = classss
blob_lyrics_df['pos'] = pos
blob_lyrics_df['neg'] = neg

blob_lyrics_df
```








```{python}
#transformers method
from tqdm import tqdm
from transformers import pipeline
import torch


trans_lyrics_df = lyrics_df.copy()

trans_list = []

sentiment_analysis = pipeline('sentiment-analysis', model='siebert/sentiment-roberta-large-english', 
truncation=True, 
max_length=512)

for i in tqdm(trans_lyrics_df['lyrics']):
  text = i
  result = sentiment_analysis(text)
  trans_list.append((result[0]['label'], result[0]['score']))


trans_lyrics_df[['label', 'score']] = trans_list

trans_lyrics_df
```






```{python}
#VADER method

from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

vader = SentimentIntensityAnalyzer()

vader_polars = []

for i in tqdm(lyrics_df['lyrics']):
  statement = i
  vader_polars.append(vader.polarity_scores(statement).get('compound'))

vader_songs_df = lyrics_df.copy()
vader_songs_df['sentiment'] = vader_polars

vader_songs_df
```








```{python}
#detecting emotion from lyrics


classifier = pipeline("text-classification", model='bhadresh-savani/distilbert-base-uncased-emotion', return_all_scores=True, truncation=True, 
max_length=512)



emotions = []

for pred in tqdm(lyrics_df['lyrics']):
    prediction = classifier(str(pred))
    top_emote = max(prediction[0], key=lambda x:x['score']) #taking the most confident emotion
    emotions.append(top_emote)


emote_df = lyrics_df.copy()
emotions_scores = pd.DataFrame(emotions)
emote_df[['emotion', 'score']] = emotions_scores[['label', 'score']]
emote_df
```





```{python}
#detecting genre from lyrics

from transformers import pipeline

classifier = pipeline("text-classification", model="Veucci/lyrics-to-genre",
truncation=True, 
max_length=512)

result = classifier(lyrics_df['lyrics'][8])

print(result)


genres = []

for g in tqdm(lyrics_df['lyrics']):
    prediction = classifier(str(g))
    genres.append(prediction[0])


genres_df = lyrics_df.copy()
genres_scores = pd.DataFrame(genres)
genres_df[['label', 'score']] = genres_scores
genres_df

```



Reordering and plotting playlist from happiest to saddest

```{python}
import plotly.express as px

#for model outputs that are all on a positive scale, flips the sign to represent negative sentiment
def convert_to_neg(df):
  df['score'] = df['score'].where(df['label'] == 'POSITIVE', -df['score']) #if label is positive, keep as is, else reverse the sign
  return df




#ranking songs by VADER sentiment
vader_sorted = vader_songs_df.sort_values(by='sentiment', ascending=False)

#plotting songs from most to least positive
vader_fig = px.line(vader_sorted,
    x='song',
    y='sentiment',
    title='VADER Rankings')
vader_fig.show()




#sorting textblob sentiment
blob_sorted = blob_lyrics_df.sort_values(by='pos', ascending=False)

#plotting songs from most to least positive
blob_vid = px.line(blob_sorted,
    x='song',
    y='pos',
    title='Blob Rankings')
blob_vid.show()





#converting negative sentiment values to negative
tsfdf = convert_to_neg(trans_lyrics_df)

#sorting transformer sentiment output
trans_sorted = tsfdf.sort_values(by='score', ascending=False)

#plotting songs from most to least positive
trans_fig = px.line(trans_sorted,
    x='song',
    y='score',
    title='Transformer Rankings')
trans_fig.show()
```




Creating functions and pipeline for different playlists:

```{python}
from tqdm import tqdm

#this function takes in a public apple music playlist link and extracts the song name and artist

def get_playlist_data(playlist_url):

    playlist_id = extract_id(playlist_url=playlist_url)

    #public url
    base_url = f"https://amp-api.music.apple.com/v1/catalog/us/playlists/{playlist_id}"

    #ending for request 
    query = "?art%5Burl%5D=f&extend=editorialArtwork%2CeditorialVideo%2Coffers%2CseoDescription%2CseoTitle%2CtrackCount&fields%5Balbums%5D=name%2Cartwork%2CplayParams%2Curl&fields%5Bapple-curators%5D=name%2Curl&fields%5Bartists%5D=name%2Cartwork%2Curl&fields%5Bcurators%5D=name%2Curl&fields%5Bsongs%5D=name%2CartistName%2CcuratorName%2CcomposerName%2Cartwork%2CplayParams%2CcontentRating%2CalbumName%2Curl%2CdurationInMillis%2CaudioTraits%2CextendedAssetUrls&format%5Bresources%5D=map&include=tracks%2Ccurator&include%5Bmusic-videos%5D=artists&include%5Bsongs%5D=artists&l=en-US&limit%5Btracks%5D=300&limit%5Bview.featured-artists%5D=15&limit%5Bview.more-by-curator%5D=15&omit%5Bresource%5D=autos&platform=web&views=featured-artists%2Cmore-by-curator"


    full_url = base_url + query
    
    r = requests.get(full_url, headers=headers)

    data = r.json()
#
    song_data = data['resources']['songs']

    songs_list = [song['attributes']['name'] for song in song_data.values()]
    songs_list = [re.sub(r"\(.+\)", '', s).strip() for s in songs_list]

    artist_list = [artist['attributes']['artistName'] for artist in song_data.values()]

    df = pd.DataFrame({
    "song": songs_list, 
    "artist": artist_list})

    return df



#this function gets the lyrics for each song

def get_lyrics(df):

    songs_dict = dict(zip(df['song'], df['artist']))

    client_access_token = "_sYrfS9alifx52SESlKPx5_gIqlcwL-gIjRTzXqylKxLUh0oGz5Ekjrcd4yTvbvS"

    import lyricsgenius
    LyricsGenius = lyricsgenius.Genius(client_access_token, timeout=15, sleep_time=1, retries=3)

    import time
    all_lyrics = []
    for song, artist in tqdm(songs_dict.items()):
        artist_search = re.split('&|,', artist)
        search = LyricsGenius.search_song(song, artist_search[0].strip())
        if search is None:
            print(f"No lyrics for {search}")
            continue
        lyrics = search.lyrics
        all_lyrics.append({'lyrics': lyrics,
                            'song': song,
                            'artist': artist})
        time.sleep(0.5)

    lyrics_df = pd.DataFrame(all_lyrics)


    lyrics_df['lyrics'] = (
    lyrics_df['lyrics'].str.replace(r'\n', ' ', regex=True) #removes new line symbol
    .str.replace(r'([a-z])([A-Z])', '\\1 \\2', regex=True) #ensures spaces between words
    .str.replace(r'\[.*?\]', ' ', regex=True) #removes brackets
    .str.replace(r'^.*Lyrics ', '', regex=True) #removes everything before and including lyrics headers
    .str.replace(r'\u2005', '', regex=True) #removes this pattern which sometimes appears within lyrics
)

    return lyrics_df


```



```{python}
#vader function
def vader_sentiment(df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    vader = SentimentIntensityAnalyzer()

    vader_polars = []

    for i in tqdm(df['lyrics']):
        vader_polars.append(vader.polarity_scores(i).get('compound'))

    vader_songs_df = df.copy()
    vader_songs_df['sentiment'] = vader_polars

    return vader_songs_df


#textblob function
def texblob_sentiment(df):

    import textblob
    from textblob.sentiments import NaiveBayesAnalyzer
    import nltk

    classss = [] 
    pos = []
    neg = []

    for i in tqdm(df['lyrics']): #loop through lyrics
        output = textblob.TextBlob(i, analyzer=NaiveBayesAnalyzer()).sentiment

        classss.append(output[0])
        pos.append(output[1])
        neg.append(output[2])


    blob_lyrics_df = df.copy()

    blob_lyrics_df['classification'] = classss
    blob_lyrics_df['pos'] = pos
    blob_lyrics_df['neg'] = neg

    return blob_lyrics_df


#transformer function
def transformer_sentiment(df):
    from transformers import pipeline
    import torch


    trans_list = []

    sentiment_analysis = pipeline('sentiment-analysis', model='siebert/sentiment-roberta-large-english', 
    truncation=True, 
    max_length=512)

    for i in tqdm(df['lyrics']):
        result = sentiment_analysis(i)
        trans_list.append((result[0]['label'], result[0]['score']))

    trans_lyrics_df = df.copy()

    trans_lyrics_df[['label', 'score']] = trans_list

    return trans_lyrics_df
```



```{python}
#based on model choice, performs sentiment analysis on lyrics
def analyze_sentiment(lyrics_df, model='vader'):

    if model.lower() == 'vader':
        return vader_sentiment(lyrics_df)
    if model.lower() == 'textblob':
        return texblob_sentiment(lyrics_df)
    if model.lower() == 'transformer':
        return transformer_sentiment(lyrics_df)
    else:
        print("Model must be 'vader', 'textblob', or 'transformer'.")
```



```{python}

#reorders and plots playlist from happiest to saddest
def rank_and_plot(df, model):

    import plotly.express as px


    if model.lower() == 'vader':
        vader_sorted = df.sort_values(by='sentiment', ascending=False)

    #plotting songs from most to least positive
        vader_fig = px.line(vader_sorted,
        x='song',
        y='sentiment',
        title='VADER Rankings')
        return vader_fig, vader_sorted

    elif model.lower() == 'textblob':
        blob_sorted = df.sort_values(by='pos', ascending=False)

        #plotting songs from most to least positive
        blob_fig = px.line(blob_sorted,
            x='song',
            y='pos',
            title='Blob Rankings')
        return blob_fig, blob_sorted

    else:
        tsfdf = convert_to_neg(df)

        #sorting transformer sentiment output
        trans_sorted = tsfdf.sort_values(by='score', ascending=False)

        #plotting songs from most to least positive
        trans_fig = px.line(trans_sorted,
            x='song',
            y='score',
            title='Transformer Rankings')
        return trans_fig, trans_sorted
```



```{python}
#full pipeline
def analyze_playlist(playlist_url, model='vader'):

    #converts to negative signs if needed
    def convert_to_neg(df):
        df['score'] = df['score'].where(df['label'] == 'POSITIVE', -df['score']) #if label is positive, keep as is, else reverse the sign
        return df

    #for extracting id from playlist url
    def extract_id(playlist_url): 
        splits = playlist_url.split('/') #splitting on /
        id = splits[-1] #taking last group
        return id
    
    songs_df = get_playlist_data(playlist_url) #finds song data
    lyrics_df = get_lyrics(songs_df) #gets lyrics
    analyzed_df = analyze_sentiment(lyrics_df, model) #sentiment analysis 
    fig, sorted_df = rank_and_plot(analyzed_df, model) #ranking and plotting
    return fig, sorted_df


```



```{python}
test_url = "https://music.apple.com/us/playlist/best-of-the-best/pl.u-XkD0YzMfDYd17j9"

fig, sorted_df = analyze_playlist(test_url, model='textblob')
fig.show()
display(sorted_df)
```


```{python}
fig
sorted_df

```