from flask import Flask, request, render_template
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import itemgetter

app = Flask(__name__)

cid = 'ecb42b03924a473eac366b5d16f2b65f'
secret = 'fbddb37fb3e843bea5b87ed537ab0e7c'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route("/")
def home():
    return render_template("firstpage.html")

@app.route("/plans")
def plans1():
    return render_template("secondpage.html")

@app.route("/library")
def library1():
    return render_template("thirdpage.html")

@app.route('/TopSongs', methods=['GET', 'POST'])
def get_top_songs():
    if request.method == 'POST':
        search_option = request.form.get('search_option')
        search_query = request.form.get('search_query')
    else:
        search_option = 'artist'
        search_query = ''

    artist_name = []
    track_name = []
    popularity = []
    track_id = []

    if search_option == 'artist':
        track_results = sp.search(q=f'artist:{search_query}', type='track', limit=50)
    else:
        track_results = sp.search(q=f'year:{search_query}', type='track', limit=50)

    for i, t in enumerate(track_results['tracks']['items']):
        artist_name.append(t['artists'][0]['name'])
        track_name.append(t['name'])
        track_id.append(t['id'])
        popularity.append(t['popularity'])

    # Create a list of (popularity, track) tuples
    tracks_with_popularity = list(zip(popularity, zip(track_name, artist_name)))

    # Sort tracks by popularity in descending order
    sorted_tracks = sorted(tracks_with_popularity, key=itemgetter(0), reverse=True)

    # Generate HTML for the top 10 songs by popularity
    top_songs_html = ''
    for i, (popularity, (track, artist)) in enumerate(sorted_tracks[:10]):
        top_songs_html += f"<p>{i+1}. {track} by {artist}</p>"

    return render_template('index.html', search_option=search_option, search_query=search_query, top_songs=top_songs_html)

if __name__ == "__main__":
    app.run()
