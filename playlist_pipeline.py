from tqdm import tqdm
import pandas as pd
import re
import requests
import time
import lyricsgenius
from tqdm import tqdm
import plotly.express as px



headers = {"user-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36",
            "Authorization": "Bearer eyJhbGciOiJFUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IldlYlBsYXlLaWQifQ.eyJpc3MiOiJBTVBXZWJQbGF5IiwiaWF0IjoxNzYyNTM4NTI0LCJleHAiOjE3Njk3OTYxMjQsInJvb3RfaHR0cHNfb3JpZ2luIjpbImFwcGxlLmNvbSJdfQ.2fpk1NEdRGBhrWjhjDJfeVWQyfa005cJYQ0Ye37GeD08vuyZvVA1xOc0JiePTEa9FLHa1HZjLd3n5F0CYUqLTw",
            "Media-User-Token": "AvxHFN2PzpRpIkzuoGPn9VeW7Hdx1Y5a8LLLsfVgOEiSBYJcUGycxXIjlw7eno8fDsWek35uL65oj+CZI9eY76CFQPx4QpkR31qMNGKjEHBYhhgfLdBlYQb4APuPFYJ45NJvSGT9A+jxFG+wQNYtQupM9JdrT4i64PV3XxKjwqhb+MFp1o9iy9BXVLTTDttyztXnZJbI6aV1s8hgURZWnT6FhdOtjzTkTRHiNcuO0CwT+VnvKw==",
            "Referer": "https://music.apple.com/",
            "Origin": "https://music.apple.com"}




def convert_to_neg(df):
        df['score'] = df['score'].where(df['label'] == 'POSITIVE', -df['score']) #if label is positive, keep as is, else reverse the sign
        return df

def extract_id(playlist_url): 
    splits = playlist_url.split('/') #splitting on /
    id = splits[-1] #taking last group
    return id





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





def vader_sentiment(df):
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    vader = SentimentIntensityAnalyzer()

    vader_polars = []

    for i in tqdm(df['lyrics']):
        vader_polars.append(vader.polarity_scores(i).get('compound'))

    vader_songs_df = df.copy()
    vader_songs_df['sentiment'] = vader_polars

    return vader_songs_df



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






def analyze_sentiment(lyrics_df, model='vader'):

    if model.lower() == 'vader':
        return vader_sentiment(lyrics_df)
    if model.lower() == 'textblob':
        return texblob_sentiment(lyrics_df)
    if model.lower() == 'transformer':
        return transformer_sentiment(lyrics_df)
    else:
        print("Model must be 'vader', 'textblob', or 'transformer'.")





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





def analyze_playlist(playlist_url, model='vader'):

    def convert_to_neg(df):
        df['score'] = df['score'].where(df['label'] == 'POSITIVE', -df['score']) #if label is positive, keep as is, else reverse the sign
        return df

    def extract_id(playlist_url): 
        splits = playlist_url.split('/') #splitting on /
        id = splits[-1] #taking last group
        return id
    
    songs_df = get_playlist_data(playlist_url)
    lyrics_df = get_lyrics(songs_df)
    analyzed_df = analyze_sentiment(lyrics_df, model)
    fig, sorted_df = rank_and_plot(analyzed_df, model)
    return fig, sorted_df