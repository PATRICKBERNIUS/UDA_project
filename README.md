# Song Scraping and Lyric Sentiment Analysis


This project attempted to scrape song data from public apple music
playlists, perform sentiment analysis using several different methods,
and reorder said playlist from happiest to saddest, plotting the results
and providing a dataframe of the songs in their new order. Uses Genius’s
API to extract lyrics.

``` python
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

    {'Have a Cigar': 'Pink Floyd',
     'In the Flesh?': 'Pink Floyd',
     'Hey You': 'Pink Floyd',
     'Paranoid Android': 'Radiohead',
     'Subterranean Homesick Alien': 'Radiohead',
     'Karma Police': 'Radiohead',
     'Street Spirit': 'Radiohead',
     'Feasting On the Flowers': 'Red Hot Chili Peppers',
     'Jigsaw Falling Into Place': 'Radiohead',
     'sdp interlude': 'Travis Scott',
     'Pick Up the Phone': 'Lupe Fiasco',
     'Cadence': 'The Long Faces',
     'Pink Ocean': 'The Voidz',
     'Hun43rd': 'A$AP Rocky',
     'Reborn': 'KIDS SEE GHOSTS',
     'Self Care': 'Mac Miller',
     'Get Em High': 'Kanye West',
     'Family Business': 'Kanye West',
     'Losing My Religion': 'R.E.M.',
     'One': 'Metallica',
     'We Major': 'Kanye West',
     'Gone': 'Kanye West',
     'Devil In a New Dress': 'Kanye West',
     'Linger': 'The Cranberries',
     'Soundtrack 2 My Life': 'Kid Cudi',
     'Make Her Say': 'Kid Cudi',
     'No One Knows': 'Queens of the Stone Age',
     "The Sky Is Fallin'": 'Queens of the Stone Age',
     'Go with the Flow': 'Queens of the Stone Age',
     'Forgot About Dre': 'Dr. Dre',
     'Mr. Rager': 'Kid Cudi',
     'Kool On': 'The Roots',
     'Lighthouse': 'The Roots',
     'Fast Lane': 'Bad Meets Evil',
     'Swimming Pools  [Extended Version]': 'Kendrick Lamar',
     'Soul Food': 'Logic',
     'Under Pressure': 'Logic',
     'Alright': 'Logic',
     'u': 'Kendrick Lamar',
     'Pound Cake / Paris Morton Music 2': 'Drake',
     'Company': 'Drake',
     'You & The 6': 'Drake',
     'Feel No Ways': 'Drake',
     'Digital Dash': 'Drake & Future',
     'Diamonds Dancing': 'Drake & Future',
     'Scholarships': 'Drake & Future',
     'Primetime': 'JAY-Z & Kanye West',
     'Scentless Apprentice': 'Nirvana',
     'Rape Me': 'Nirvana',
     "I'm Still Standing": 'Taron Egerton',
     'Stan': 'Eminem',
     'Baptized in Fire': 'Kid Cudi',
     'Blood On the Leaves': 'Kanye West',
     'Flexicution': 'Logic',
     'The Man Who Sold the World': 'Nirvana',
     'Without Me': 'Eminem',
     'Stargazer': 'Rainbow',
     'Never Change': 'JAY-Z',
     'Song Cry': 'JAY-Z',
     'Hey Jude': 'The Beatles',
     'You Never Give Me Your Money': 'The Beatles',
     'Paranoid': 'Kanye West',
     'Ghost Town': 'Kanye West',
     'Father Stretch My Hands, Pt. 1': 'Kanye West',
     'Saint Pablo': 'Kanye West',
     '151 Rum': 'JID',
     'Just What I Am': 'Kid Cudi',
     'Sunflower': 'Post Malone & Swae Lee',
     'I Wonder': 'Kanye West',
     '90210': 'Travis Scott',
     'Nightcrawler': 'Travis Scott',
     'Oh! Darling': 'The Beatles',
     'Throw Away': 'Future',
     'Good News': 'Mac Miller',
     'Everybody': 'Mac Miller',
     'Not The Same Anymore': 'The Strokes',
     'Ode To The Mets': 'The Strokes',
     "Truth Doesn't Make a Noise": 'The White Stripes',
     'Rooster': 'Alice In Chains',
     'Let It Be': 'The Beatles',
     'I Appear Missing': 'Queens of the Stone Age',
     'Beach Life-In-Death': 'Car Seat Headrest',
     'Bodys': 'Car Seat Headrest',
     'Un-Reborn Again': 'Queens of the Stone Age',
     'Believe What I Say': 'Kanye West',
     'The Bronze': 'Queens of the Stone Age',
     'Eleanor Rigby': 'The Beatles',
     'Doomsday': 'MF DOOM',
     'On Time': 'Metro Boomin & John Legend',
     'Superhero': 'Metro Boomin, Future & Chris Brown',
     'Too Many Nights': 'Metro Boomin & Future',
     'Us and Them': 'Pink Floyd',
     'Any Colour You Like': 'Pink Floyd',
     'Belize': 'Danger Mouse & Black Thought',
     'Like That': 'Future, Metro Boomin & Kendrick Lamar',
     'Square Wave': 'The Voidz',
     'The Emptiness Machine': 'LINKIN PARK',
     'Heartbeat': 'Childish Gambino',
     'Matches': 'Mac Miller',
     'Red Dot Music': 'Mac Miller',
     'Donald Trump': 'Mac Miller',
     'Kick, Push': 'Lupe Fiasco',
     'Killing In the Name': 'Rage Against the Machine',
     'Breaking the Law': 'Judas Priest',
     'Snow': 'Red Hot Chili Peppers',
     '505': 'Arctic Monkeys',
     'Chonkyfire': 'Outkast',
     'Hard to Explain': 'The Strokes',
     'Nutshell': 'Alice In Chains',
     'Superstar': 'Lupe Fiasco',
     'C.R.E.A.M.': 'Wu-Tang Clan',
     'Man in the Box': 'Alice In Chains',
     '3030': 'Deltron 3030',
     'You Only Live Once': 'The Strokes',
     'Automatic Stop': 'The Strokes',
     'Just Like Heaven': 'The Cure',
     'Pictures of You': 'The Cure',
     'The Show Goes On': 'Lupe Fiasco',
     'Black': 'Pearl Jam',
     'Times Like These': 'Foo Fighters',
     'Battle Scars': 'Lupe Fiasco & Guy Sebastian',
     'For Whom the Bell Tolls': 'Metallica',
     'Kashmir': 'Led Zeppelin',
     'Ten Years Gone': 'Led Zeppelin',
     'Rock and Roll': 'Led Zeppelin',
     'Stairway to Heaven': 'Led Zeppelin',
     'When the Levee Breaks': 'Led Zeppelin',
     'Dazed and Confused': 'Led Zeppelin',
     'Somewhere I Belong': 'LINKIN PARK',
     'IFHY': 'Tyler, The Creator',
     'Hotel California': 'Eagles',
     "I Can't Tell You Why": 'Eagles',
     'Desperado': 'Eagles',
     'N.Y. State of Mind': 'Nas',
     'One Love': 'Nas',
     'Do I Wanna Know?': 'Arctic Monkeys',
     'Mayonaise': 'The Smashing Pumpkins',
     "War Pigs / Luke's Wall": 'Black Sabbath',
     'Well I Wonder': 'The Smiths',
     "I Know It's Over": 'The Smiths',
     'How Soon Is Now?': 'The Smiths',
     'Shot You Down': 'Isaiah Rashad',
     'Hitch a Ride': 'Boston',
     'Otherside': 'Red Hot Chili Peppers',
     'Californication': 'Red Hot Chili Peppers',
     'F*****G YOUNG / PERFECT': 'Tyler, The Creator',
     'Plug In Baby': 'Muse',
     'L$D': 'A$AP Rocky',
     'Jukebox Joints': 'A$AP Rocky'}

``` python
#lyrics_df = pd.DataFrame(lyrics_saved)
lyrics_df = pd.DataFrame(all_lyrics)
lyrics_df.head()
```

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|  | lyrics | song | artist |
|----|----|----|----|
| 0 | \[Instrumental Intro\]\n\n\[Verse 1: Roy Harper\]\\.. | Have a Cigar | Pink Floyd |
| 1 | \[Intro: Richard Wright\]\n...we came in?\n\n\[Ve... | In the Flesh? | Pink Floyd |
| 2 | \[Instrumental Intro\]\n\n\[Verse 1: David Gilmou... | Hey You | Pink Floyd |
| 3 | \[Part I\]\n\[Verse 1\]\nPlease could you stop the... | Paranoid Android | Radiohead |
| 4 | \[Verse 1\]\nThe breath of the morning, I keep f... | Subterranean Homesick Alien | Radiohead |

</div>

Trying different sentiment analysis methods:

``` python
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

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|  | lyrics | song | artist | sentiment |
|----|----|----|----|----|
| 0 | Come in here, dear boy, have a cigar You'... | Have a Cigar | Pink Floyd | 0.9727 |
| 1 | ...we came in? So you thought you might l... | In the Flesh? | Pink Floyd | -0.7398 |
| 2 | Hey, you Out there in the cold, getting l... | Hey You | Pink Floyd | 0.6652 |
| 3 | Please could you stop the noise? I'm tryin... | Paranoid Android | Radiohead | 0.9890 |
| 4 | The breath of the morning, I keep forgettin'... | Subterranean Homesick Alien | Radiohead | -0.9758 |
| ... | ... | ... | ... | ... |
| 141 | How long, how long will I slide? Well, separ... | Otherside | Red Hot Chili Peppers | 0.8856 |
| 142 | Psychic spies from China try to steal your m... | Californication | Red Hot Chili Peppers | 0.9768 |
| 143 | I've exposed your lies, baby The underneath'... | Plug In Baby | Muse | -0.9238 |
| 144 | Uh Uh I know I dream about her all day (U... | L\$D | A\$AP Rocky | 0.9939 |
| 145 | And I'm a man of my word, that I got noth... | Jukebox Joints | A\$AP Rocky | 0.9971 |

<p>146 rows × 4 columns</p>
</div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|  | lyrics | song | artist | emotion | score |
|----|----|----|----|----|----|
| 0 | Come in here, dear boy, have a cigar You'... | Have a Cigar | Pink Floyd | joy | 0.998559 |
| 1 | ...we came in? So you thought you might l... | In the Flesh? | Pink Floyd | love | 0.976635 |
| 2 | Hey, you Out there in the cold, getting l... | Hey You | Pink Floyd | sadness | 0.595291 |
| 3 | Please could you stop the noise? I'm tryin... | Paranoid Android | Radiohead | fear | 0.989243 |
| 4 | The breath of the morning, I keep forgettin'... | Subterranean Homesick Alien | Radiohead | fear | 0.928234 |
| ... | ... | ... | ... | ... | ... |
| 141 | How long, how long will I slide? Well, separ... | Otherside | Red Hot Chili Peppers | anger | 0.689661 |
| 142 | Psychic spies from China try to steal your m... | Californication | Red Hot Chili Peppers | joy | 0.901904 |
| 143 | I've exposed your lies, baby The underneath'... | Plug In Baby | Muse | sadness | 0.853856 |
| 144 | Uh Uh I know I dream about her all day (U... | L\$D | A\$AP Rocky | sadness | 0.996708 |
| 145 | And I'm a man of my word, that I got noth... | Jukebox Joints | A\$AP Rocky | sadness | 0.729435 |

<p>146 rows × 5 columns</p>
</div>

Reordering and plotting playlist from happiest to saddest

Creating functions and pipeline for different playlists:

``` python
test_url = "https://music.apple.com/us/playlist/best-of-the-best/pl.u-XkD0YzMfDYd17j9"

fig, sorted_df = analyze_playlist(test_url, model='textblob')
fig.show()
display(sorted_df)
```

    Searching for "Have a Cigar" by Pink Floyd...
    Done.

    Searching for "In the Flesh?" by Pink Floyd...
    Done.

    Searching for "Hey You" by Pink Floyd...
    Done.

    Searching for "Paranoid Android" by Radiohead...
    Done.

    Searching for "Subterranean Homesick Alien" by Radiohead...
    Done.

    Searching for "Karma Police" by Radiohead...
    Done.

    Searching for "Street Spirit" by Radiohead...
    Done.

    Searching for "Feasting On the Flowers" by Red Hot Chili Peppers...
    Done.

    Searching for "Jigsaw Falling Into Place" by Radiohead...
    Done.

    Searching for "sdp interlude" by Travis Scott...
    Done.

    Searching for "Pick Up the Phone" by Lupe Fiasco...
    Done.

    Searching for "Cadence" by The Long Faces...
    Done.

    Searching for "Pink Ocean" by The Voidz...
    Done.

    Searching for "Hun43rd" by A$AP Rocky...
    Done.

    Searching for "Reborn" by KIDS SEE GHOSTS...
    Done.

    Searching for "Self Care" by Mac Miller...
    Done.

    Searching for "Get Em High" by Kanye West...
    Done.

    Searching for "Family Business" by Kanye West...
    Done.

    Searching for "Losing My Religion" by R.E.M....
    Done.

    Searching for "One" by Metallica...
    Done.

    Searching for "We Major" by Kanye West...
    Done.

    Searching for "Gone" by Kanye West...
    Done.

    Searching for "Devil In a New Dress" by Kanye West...
    Done.

    Searching for "Linger" by The Cranberries...
    Done.

    Searching for "Soundtrack 2 My Life" by Kid Cudi...
    Done.

    Searching for "Make Her Say" by Kid Cudi...
    Done.

    Searching for "No One Knows" by Queens of the Stone Age...
    Done.

    Searching for "The Sky Is Fallin'" by Queens of the Stone Age...
    Done.

    Searching for "Go with the Flow" by Queens of the Stone Age...
    Done.

    Searching for "Forgot About Dre" by Dr. Dre...
    Done.

    Searching for "Mr. Rager" by Kid Cudi...
    Done.

    Searching for "Kool On" by The Roots...
    Done.

    Searching for "Lighthouse" by The Roots...
    Done.

    Searching for "Fast Lane" by Bad Meets Evil...
    Done.

    Searching for "Swimming Pools  [Extended Version]" by Kendrick Lamar...
    Done.

    Searching for "Soul Food" by Logic...
    Done.

    Searching for "Under Pressure" by Logic...
    Done.

    Searching for "Alright" by Logic...
    Done.

    Searching for "u" by Kendrick Lamar...
    Done.

    Searching for "Pound Cake / Paris Morton Music 2" by Drake...
    Done.

    Searching for "Company" by Drake...
    Done.

    Searching for "You & The 6" by Drake...
    Done.

    Searching for "Feel No Ways" by Drake...
    Done.

    Searching for "Digital Dash" by Drake...
    Done.

    Searching for "Diamonds Dancing" by Drake...
    Done.

    Searching for "Scholarships" by Drake...
    Done.

    Searching for "Primetime" by JAY-Z...
    Done.

    Searching for "Scentless Apprentice" by Nirvana...
    Done.

    Searching for "Rape Me" by Nirvana...
    Done.

    Searching for "I'm Still Standing" by Taron Egerton...
    Done.

    Searching for "Stan" by Eminem...
    Done.

    Searching for "Baptized in Fire" by Kid Cudi...
    Done.

    Searching for "Blood On the Leaves" by Kanye West...
    Done.

    Searching for "Flexicution" by Logic...
    Done.

    Searching for "The Man Who Sold the World" by Nirvana...
    Done.

    Searching for "Without Me" by Eminem...
    Done.

    Searching for "Stargazer" by Rainbow...
    Done.

    Searching for "Never Change" by JAY-Z...
    Done.

    Searching for "Song Cry" by JAY-Z...
    Done.

    Searching for "Hey Jude" by The Beatles...
    Done.

    Searching for "You Never Give Me Your Money" by The Beatles...
    Done.

    Searching for "Paranoid" by Kanye West...
    Done.

    Searching for "Ghost Town" by Kanye West...
    Done.

    Searching for "Father Stretch My Hands, Pt. 1" by Kanye West...
    Done.

    Searching for "Saint Pablo" by Kanye West...
    Done.

    Searching for "151 Rum" by JID...
    Done.

    Searching for "Just What I Am" by Kid Cudi...
    Done.

    Searching for "Sunflower" by Post Malone...
    Done.

    Searching for "I Wonder" by Kanye West...
    Done.

    Searching for "90210" by Travis Scott...
    Done.

    Searching for "Nightcrawler" by Travis Scott...
    Done.

    Searching for "Oh! Darling" by The Beatles...
    Done.

    Searching for "Throw Away" by Future...
    Done.

    Searching for "Good News" by Mac Miller...
    Done.

    Searching for "Everybody" by Mac Miller...
    Done.

    Searching for "Not The Same Anymore" by The Strokes...
    Done.

    Searching for "Ode To The Mets" by The Strokes...
    Done.

    Searching for "Truth Doesn't Make a Noise" by The White Stripes...
    Done.

    Searching for "Rooster" by Alice In Chains...
    Done.

    Searching for "Let It Be" by The Beatles...
    Done.

    Searching for "I Appear Missing" by Queens of the Stone Age...
    Done.

    Searching for "Beach Life-In-Death" by Car Seat Headrest...
    Done.

    Searching for "Bodys" by Car Seat Headrest...
    Done.

    Searching for "Un-Reborn Again" by Queens of the Stone Age...
    Done.

    Searching for "Believe What I Say" by Kanye West...
    Done.

    Searching for "The Bronze" by Queens of the Stone Age...
    Done.

    Searching for "Eleanor Rigby" by The Beatles...
    Done.

    Searching for "Doomsday" by MF DOOM...
    Done.

    Searching for "On Time" by Metro Boomin...
    Done.

    Searching for "Superhero" by Metro Boomin...
    Done.

    Searching for "Too Many Nights" by Metro Boomin...
    Done.

    Searching for "Us and Them" by Pink Floyd...
    Done.

    Searching for "Any Colour You Like" by Pink Floyd...

    Specified song does not contain lyrics. Rejecting.
    No lyrics for None
    Searching for "Belize" by Danger Mouse...
    Done.

    Searching for "Like That" by Future...
    Done.

    Searching for "Square Wave" by The Voidz...
    Done.

    Searching for "The Emptiness Machine" by LINKIN PARK...
    Done.

    Searching for "Heartbeat" by Childish Gambino...
    Done.

    Searching for "Matches" by Mac Miller...
    Done.

    Searching for "Red Dot Music" by Mac Miller...
    Done.

    Searching for "Donald Trump" by Mac Miller...
    Done.

    Searching for "Kick, Push" by Lupe Fiasco...
    Done.

    Searching for "Killing In the Name" by Rage Against the Machine...
    Done.

    Searching for "Breaking the Law" by Judas Priest...
    Done.

    Searching for "Snow" by Red Hot Chili Peppers...
    Done.

    Searching for "505" by Arctic Monkeys...
    Done.

    Searching for "Chonkyfire" by Outkast...
    Done.

    Searching for "Hard to Explain" by The Strokes...
    Done.

    Searching for "Nutshell" by Alice In Chains...
    Done.

    Searching for "Superstar" by Lupe Fiasco...
    Done.

    Searching for "C.R.E.A.M." by Wu-Tang Clan...
    Done.

    Searching for "Man in the Box" by Alice In Chains...
    Done.

    Searching for "3030" by Deltron 3030...
    Done.

    Searching for "You Only Live Once" by The Strokes...
    Done.

    Searching for "Automatic Stop" by The Strokes...
    Done.

    Searching for "Just Like Heaven" by The Cure...
    Done.

    Searching for "Pictures of You" by The Cure...
    Done.

    Searching for "The Show Goes On" by Lupe Fiasco...
    Done.

    Searching for "Black" by Pearl Jam...
    Done.

    Searching for "Times Like These" by Foo Fighters...
    Done.

    Searching for "Battle Scars" by Lupe Fiasco...
    Done.

    Searching for "For Whom the Bell Tolls" by Metallica...
    Done.

    Searching for "Kashmir" by Led Zeppelin...
    Done.

    Searching for "Ten Years Gone" by Led Zeppelin...
    Done.

    Searching for "Rock and Roll" by Led Zeppelin...
    Done.

    Searching for "Stairway to Heaven" by Led Zeppelin...
    Done.

    Searching for "When the Levee Breaks" by Led Zeppelin...
    Done.

    Searching for "Dazed and Confused" by Led Zeppelin...
    Done.

    Searching for "Somewhere I Belong" by LINKIN PARK...
    Done.

    Searching for "IFHY" by Tyler...
    Done.

    Searching for "Hotel California" by Eagles...
    Done.

    Searching for "I Can't Tell You Why" by Eagles...
    Done.

    Searching for "Desperado" by Eagles...
    Done.

    Searching for "N.Y. State of Mind" by Nas...
    Done.

    Searching for "One Love" by Nas...
    Done.

    Searching for "Do I Wanna Know?" by Arctic Monkeys...
    Done.

    Searching for "Mayonaise" by The Smashing Pumpkins...
    Done.

    Searching for "War Pigs / Luke's Wall" by Black Sabbath...

    No results found for: 'War Pigs / Luke's Wall Black Sabbath'
    No lyrics for None
    Searching for "Well I Wonder" by The Smiths...
    Done.

    Searching for "I Know It's Over" by The Smiths...
    Done.

    Searching for "How Soon Is Now?" by The Smiths...
    Done.

    Searching for "Shot You Down" by Isaiah Rashad...
    Done.

    Searching for "Hitch a Ride" by Boston...
    Done.

    Searching for "Otherside" by Red Hot Chili Peppers...
    Done.

    Searching for "Californication" by Red Hot Chili Peppers...
    Done.

    Searching for "F*****G YOUNG / PERFECT" by Tyler...

    No results found for: 'F*****G YOUNG / PERFECT Tyler'
    No lyrics for None
    Searching for "Plug In Baby" by Muse...
    Done.

    Searching for "L$D" by A$AP Rocky...
    Done.

    Searching for "Jukebox Joints" by A$AP Rocky...
    Done.

<div>            <script src="https://cdnjs.cloudflare.com/ajax/libs/mathjax/2.7.5/MathJax.js?config=TeX-AMS-MML_SVG"></script><script type="text/javascript">if (window.MathJax && window.MathJax.Hub && window.MathJax.Hub.Config) {window.MathJax.Hub.Config({SVG: {font: "STIX-Web"}});}</script>                <script type="text/javascript">window.PlotlyConfig = {MathJaxConfig: 'local'};</script>
        <script charset="utf-8" src="https://cdn.plot.ly/plotly-3.3.0.min.js" integrity="sha256-bO3dS6yCpk9aK4gUpNELtCiDeSYvGYnK7jFI58NQnHI=" crossorigin="anonymous"></script>                <div id="c56c8aba-546d-48af-bb64-f2dd9ced9920" class="plotly-graph-div" style="height:525px; width:100%;"></div>            <script type="text/javascript">                window.PLOTLYENV=window.PLOTLYENV || {};                                if (document.getElementById("c56c8aba-546d-48af-bb64-f2dd9ced9920")) {                    Plotly.newPlot(                        "c56c8aba-546d-48af-bb64-f2dd9ced9920",                        [{"hovertemplate":"song=%{x}\u003cbr\u003epos=%{y}\u003cextra\u003e\u003c\u002fextra\u003e","legendgroup":"","line":{"color":"#636efa","dash":"solid"},"marker":{"symbol":"circle"},"mode":"lines","name":"","orientation":"v","showlegend":false,"x":["u","3030","Under Pressure","Pound Cake \u002f Paris Morton Music 2","Soul Food","Snow","Desperado","Feasting On the Flowers","Square Wave","Superstar","Devil In a New Dress","Kool On","N.Y. State of Mind","Never Change","C.R.E.A.M.","Kick, Push","Mayonaise","Hitch a Ride","Pictures of You","Soundtrack 2 My Life","Beach Life-In-Death","Chonkyfire","Alright","IFHY","L$D","Jukebox Joints","Stairway to Heaven","Saint Pablo","Lighthouse","Baptized in Fire","Family Business","Gone","The Show Goes On","I Know It's Over","Belize","Believe What I Say","Losing My Religion","Stargazer","Californication","You & The 6","Just Like Heaven","Scholarships","Matches","Street Spirit","Ten Years Gone","Kashmir","Us and Them","Primetime","Forgot About Dre","For Whom the Bell Tolls","151 Rum","Nutshell","Without Me","Hun43rd","Stan","Times Like These","I Wonder","Good News","I'm Still Standing","One","Let It Be","Do I Wanna Know?","Ghost Town","Dazed and Confused","I Appear Missing","Blood On the Leaves","No One Knows","Rooster","Song Cry","Fast Lane","One Love","Swimming Pools  [Extended Version]","Hey You","We Major","Scentless Apprentice","Eleanor Rigby","How Soon Is Now?","Shot You Down","Un-Reborn Again","Reborn","Get Em High","Linger","Superhero","Go with the Flow","You Only Live Once","Paranoid","Hotel California","Hard to Explain","Company","Oh! Darling","I Can't Tell You Why","Otherside","Not The Same Anymore","Paranoid Android","You Never Give Me Your Money","Pink Ocean","Well I Wonder","In the Flesh?","Pick Up the Phone","Father Stretch My Hands, Pt. 1","Sunflower","Like That","Have a Cigar","Automatic Stop","Cadence","Man in the Box","Hey Jude","Somewhere I Belong","Plug In Baby","Mr. Rager","Rape Me","Battle Scars","Truth Doesn't Make a Noise","Doomsday","Everybody","Subterranean Homesick Alien","Black","Red Dot Music","The Man Who Sold the World","Killing In the Name","The Emptiness Machine","505","Breaking the Law","Bodys","On Time","Self Care","When the Levee Breaks","Flexicution","Diamonds Dancing","Rock and Roll","Donald Trump","90210","Throw Away","The Bronze","Nightcrawler","Jigsaw Falling Into Place","Feel No Ways","sdp interlude","The Sky Is Fallin'","Heartbeat","Karma Police","Ode To The Mets","Make Her Say","Just What I Am","Too Many Nights","Digital Dash"],"xaxis":"x","y":{"dtype":"f8","bdata":"Ov3\u002f\u002f\u002f\u002f\u002f7z+j0\u002f\u002f\u002f\u002f\u002f\u002fvPwfb\u002ff\u002f\u002f\u002f+8\u002f4Baf\u002f\u002f\u002f\u002f7z8Ph63+\u002f\u002f\u002fvP3Uv4fj\u002f\u002f+8\u002fQsSF8\u002f\u002f\u002f7z9yB+vs\u002f\u002f\u002fvP4MeeOf\u002f\u002f+8\u002fb86G1f\u002f\u002f7z+al0nN\u002f\u002f\u002fvP79\u002fHLD\u002f\u002f+8\u002ftdkelv\u002f\u002f7z9TfqWG\u002f\u002f\u002fvPz9q5Ln+\u002f+8\u002fCGrIxPz\u002f7z8l7FI0+v\u002fvP3o9CJ75\u002f+8\u002fC8xIOvn\u002f7z\u002fXiq3W9\u002f\u002fvP\u002fnORg3z\u002f+8\u002f6R78S\u002fH\u002f7z8f9K428f\u002fvP2dN9Sbx\u002f+8\u002fch13+uX\u002f7z9NL+I+5f\u002fvP0RGtLna\u002f+8\u002fV3N8K9b\u002f7z9cg4vruf\u002fvP50z9Ced\u002f+8\u002fjUOyspn\u002f7z8b1WN1lP\u002fvP8nZUyeO\u002f+8\u002fjIZsZ2H\u002f7z9HeeLLMv\u002fvP7SDbkDZ\u002fu8\u002fX1x82rP+7z8DzpEuqf7vP6F4HgYo\u002fu8\u002f6KP60Bv+7z8IW+Fm9f3vP7TjFOC\u002f\u002fe8\u002fFR0m7YT97z\u002fZyvVCvfzvPzMO8ziC++8\u002fcPyJLCr77z8t\u002fE7Y8vbvPzyrJy3M9u8\u002f8BFCzST17z9xT3qHa\u002fTvP+soQwmV8+8\u002fa5nA0dny7z\u002fM3YBTTfLvP1KZyqWK7O8\u002fU6C1L7Tr7z9WPVPl3+nvP9w1VfkE4+8\u002f3Ch5osXh7z8r\u002fzBZbdzvP\u002f6gdSBg2+8\u002f8DkQXPvW7z821paYvtDvP\u002fKU32hXzO8\u002fF7echVy37z+LPjfVsLTvPzMI6UXCsO8\u002f96HPY+Kh7z9wqRXhNp3vP+u5hhhshO8\u002fxTvNdW1l7z8lRAZDyk\u002fvPzSqIQLtPu8\u002fskqZ0YQG7z9yfh1GygHvP8J1rKKf\u002f+4\u002f9sPil53k7j9lut6I1eLuP2qb79uwuu4\u002fqhEeXnOt7j8jl4Uf5aPuP5BWAcMace4\u002fSy9tR5Iu7j\u002fvfJ1AhB\u002fuP\u002fn4XV+1\u002fu0\u002f3R1ZIpjO7T8cTLIfPGPtPye94Zp8Puw\u002f8c\u002fkWHYS7D\u002fhn0WVWPbrPxHWs6\u002frbus\u002fQvGKPDdk6z+QNLtxElPrP\u002fkcLFqqT+s\u002fnnDpMagC6j\u002f\u002fEjyvBkPpP9wErHt\u002fIuk\u002fQVuQ5dFj6D8y8ncuxjPoP+YqsZa8dOY\u002fGuupG0v75T8X5ZcD2\u002fnlP+GutAy2DuQ\u002fviyD6YgD5D\u002fzISgDCuzjPwduwy\u002fNQ+M\u002fkyZlGuIY4z8PJA9ZThPjP\u002f\u002fggslLqOI\u002faWTUyhFM4T+iVGza6u3gPwFihVQejuA\u002fHSG3iQrb3z\u002f4TvyEM+rdP\u002fktEMxYct0\u002fY3EGQq\u002f53D\u002f1z7ewRY7XP6iHRm+eQ9U\u002fu9f4frZw0j+Af3lecfHMP\u002fUFQk7\u002fGss\u002fCxgl15xfyj8Xirh3dGrIP7CgjaWaqLs\u002f0lIkuGjFtj\u002f+HxU2A1e0P2eppVGw7q8\u002ftuFAA0J+rz8xInPk9bKtPxmVbedvWag\u002fR8d\u002fMyGmpj+XudmPnsmhP2TE6aVHT6E\u002fUabiE828oD+MHHXrVTCgP8M64X0iSpI\u002fF+LL3j4DjT82m66vvSGMP+dRgCi1e4c\u002faT\u002f\u002fH4z0fT+UUG9oSad5P5G\u002f3z6AlHE\u002fKJ4QGTWQYT\u002fmmAk1rihVP+OqoRvWbTM\u002f199ZJQNjKT\u002fmDu2gR\u002fPoPg=="},"yaxis":"y","type":"scatter"}],                        {"template":{"data":{"histogram2dcontour":[{"type":"histogram2dcontour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"choropleth":[{"type":"choropleth","colorbar":{"outlinewidth":0,"ticks":""}}],"histogram2d":[{"type":"histogram2d","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"heatmap":[{"type":"heatmap","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"contourcarpet":[{"type":"contourcarpet","colorbar":{"outlinewidth":0,"ticks":""}}],"contour":[{"type":"contour","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"surface":[{"type":"surface","colorbar":{"outlinewidth":0,"ticks":""},"colorscale":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]]}],"mesh3d":[{"type":"mesh3d","colorbar":{"outlinewidth":0,"ticks":""}}],"scatter":[{"fillpattern":{"fillmode":"overlay","size":10,"solidity":0.2},"type":"scatter"}],"parcoords":[{"type":"parcoords","line":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolargl":[{"type":"scatterpolargl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"bar":[{"error_x":{"color":"#2a3f5f"},"error_y":{"color":"#2a3f5f"},"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"bar"}],"scattergeo":[{"type":"scattergeo","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterpolar":[{"type":"scatterpolar","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"histogram":[{"marker":{"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"histogram"}],"scattergl":[{"type":"scattergl","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatter3d":[{"type":"scatter3d","line":{"colorbar":{"outlinewidth":0,"ticks":""}},"marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermap":[{"type":"scattermap","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattermapbox":[{"type":"scattermapbox","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scatterternary":[{"type":"scatterternary","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"scattercarpet":[{"type":"scattercarpet","marker":{"colorbar":{"outlinewidth":0,"ticks":""}}}],"carpet":[{"aaxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"baxis":{"endlinecolor":"#2a3f5f","gridcolor":"white","linecolor":"white","minorgridcolor":"white","startlinecolor":"#2a3f5f"},"type":"carpet"}],"table":[{"cells":{"fill":{"color":"#EBF0F8"},"line":{"color":"white"}},"header":{"fill":{"color":"#C8D4E3"},"line":{"color":"white"}},"type":"table"}],"barpolar":[{"marker":{"line":{"color":"#E5ECF6","width":0.5},"pattern":{"fillmode":"overlay","size":10,"solidity":0.2}},"type":"barpolar"}],"pie":[{"automargin":true,"type":"pie"}]},"layout":{"autotypenumbers":"strict","colorway":["#636efa","#EF553B","#00cc96","#ab63fa","#FFA15A","#19d3f3","#FF6692","#B6E880","#FF97FF","#FECB52"],"font":{"color":"#2a3f5f"},"hovermode":"closest","hoverlabel":{"align":"left"},"paper_bgcolor":"white","plot_bgcolor":"#E5ECF6","polar":{"bgcolor":"#E5ECF6","angularaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"radialaxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"ternary":{"bgcolor":"#E5ECF6","aaxis":{"gridcolor":"white","linecolor":"white","ticks":""},"baxis":{"gridcolor":"white","linecolor":"white","ticks":""},"caxis":{"gridcolor":"white","linecolor":"white","ticks":""}},"coloraxis":{"colorbar":{"outlinewidth":0,"ticks":""}},"colorscale":{"sequential":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"sequentialminus":[[0.0,"#0d0887"],[0.1111111111111111,"#46039f"],[0.2222222222222222,"#7201a8"],[0.3333333333333333,"#9c179e"],[0.4444444444444444,"#bd3786"],[0.5555555555555556,"#d8576b"],[0.6666666666666666,"#ed7953"],[0.7777777777777778,"#fb9f3a"],[0.8888888888888888,"#fdca26"],[1.0,"#f0f921"]],"diverging":[[0,"#8e0152"],[0.1,"#c51b7d"],[0.2,"#de77ae"],[0.3,"#f1b6da"],[0.4,"#fde0ef"],[0.5,"#f7f7f7"],[0.6,"#e6f5d0"],[0.7,"#b8e186"],[0.8,"#7fbc41"],[0.9,"#4d9221"],[1,"#276419"]]},"xaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"yaxis":{"gridcolor":"white","linecolor":"white","ticks":"","title":{"standoff":15},"zerolinecolor":"white","automargin":true,"zerolinewidth":2},"scene":{"xaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"yaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2},"zaxis":{"backgroundcolor":"#E5ECF6","gridcolor":"white","linecolor":"white","showbackground":true,"ticks":"","zerolinecolor":"white","gridwidth":2}},"shapedefaults":{"line":{"color":"#2a3f5f"}},"annotationdefaults":{"arrowcolor":"#2a3f5f","arrowhead":0,"arrowwidth":1},"geo":{"bgcolor":"white","landcolor":"#E5ECF6","subunitcolor":"white","showland":true,"showlakes":true,"lakecolor":"white"},"title":{"x":0.05},"mapbox":{"style":"light"},"margin":{"b":0,"l":0,"r":0,"t":30}}},"xaxis":{"anchor":"y","domain":[0.0,1.0],"title":{"text":"song"}},"yaxis":{"anchor":"x","domain":[0.0,1.0],"title":{"text":"pos"}},"legend":{"tracegroupgap":0},"title":{"text":"Blob Rankings"}},                        {"responsive": true}                    ).then(function(){
                            &#10;var gd = document.getElementById('c56c8aba-546d-48af-bb64-f2dd9ced9920');
var x = new MutationObserver(function (mutations, observer) {{
        var display = window.getComputedStyle(gd).display;
        if (!display || display === 'none') {{
            console.log([gd, 'removed!']);
            Plotly.purge(gd);
            observer.disconnect();
        }}
}});
&#10;// Listen for the removal of the full notebook cells
var notebookContainer = gd.closest('#notebook-container');
if (notebookContainer) {{
    x.observe(notebookContainer, {childList: true});
}}
&#10;// Listen for the clearing of the current output cell
var outputEl = gd.closest('.output');
if (outputEl) {{
    x.observe(outputEl, {childList: true});
}}
&#10;                        })                };            </script>        </div>

<div>
<style scoped>
    .dataframe tbody tr th:only-of-type {
        vertical-align: middle;
    }
&#10;    .dataframe tbody tr th {
        vertical-align: top;
    }
&#10;    .dataframe thead th {
        text-align: right;
    }
</style>

|  | lyrics | song | artist | classification | pos | neg |
|----|----|----|----|----|----|----|
| 38 | Ah! Ah! Ah! Loving you is complicated ... | u | Kendrick Lamar | pos | 1.000000 | 5.409459e-14 |
| 111 | Calling Apollo 9, calling Apollo 9 What is y... | 3030 | Deltron 3030 | pos | 1.000000 | 1.204027e-12 |
| 36 | Thug 'round—from a—from a—thug 'round—onc... | Under Pressure | Logic | pos | 1.000000 | 1.563086e-11 |
| 39 | Good God Almighty—like back in the old da... | Pound Cake / Paris Morton Music 2 | Drake | pos | 1.000000 | 7.051626e-10 |
| 35 | Goddamn, goddamn, conversations with legends... | Soul Food | Logic | pos | 1.000000 | 2.462722e-09 |
| ... | ... | ... | ... | ... | ... | ... |
| 76 | Up on his horse, up on his horse Not gonna w... | Ode To The Mets | The Strokes | neg | 0.002144 | 9.978560e-01 |
| 25 | Kid Cudi I Make Her Say (Oh, oh oh oh) (Oh, oh... | Make Her Say | Kid Cudi | neg | 0.001291 | 9.987086e-01 |
| 66 | I'm just what you made, God, not many I trus... | Just What I Am | Kid Cudi | neg | 0.000296 | 9.997035e-01 |
| 90 | Honorable C.N.O.T.E Metr o Keep the bitch... | Too Many Nights | Metro Boomin & Future | neg | 0.000194 | 9.998063e-01 |
| 43 | ( Metro Boomin want some more, nigga ) Rolli... | Digital Dash | Drake & Future | neg | 0.000012 | 9.999881e-01 |

<p>146 rows × 6 columns</p>
</div>
