from flask import Flask, request, render_template, Response
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from operator import itemgetter
import requests

app = Flask(__name__)

# Replace with your Spotify API credentials
cid = 'ecb42b03924a473eac366b5d16f2b65f'
secret = 'fbddb37fb3e843bea5b87ed537ab0e7c'

# Initialize the Spotify client
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

@app.route("/")
def home():
    return render_template("firstpage.html")

@app.route("/library")
def library():
    return render_template("thirdpage.html")

@app.route('/TopSongs', methods=['GET', 'POST'])
def get_top_songs():
    if request.method == 'POST':
        search_option = request.form.get('search_option')
        search_query = request.form.get('search_query')
    else:
        search_option = 'artist'
        search_query = ''

    track_name = []
    artist_name = []
    cover_url = []
    audio_preview_url = []

    if search_option == 'artist':
        track_results = sp.search(q=f'artist:{search_query}', type='track', limit=50)
    else:
        track_results = sp.search(q=f'year:{search_query}', type='track', limit=50)

    for t in track_results['tracks']['items']:
        track_name.append(t['name'])
        artist_name.append(t['artists'][0]['name'])
        cover_url.append(t['album']['images'][0]['url'])
        audio_preview_url.append(t['preview_url'])

    # Create a list of (popularity, track) tuples
    tracks_with_popularity = list(zip(range(len(track_results['tracks']['items'])), zip(track_name, artist_name, cover_url, audio_preview_url)))

    # Sort tracks by popularity in descending order
    sorted_tracks = sorted(tracks_with_popularity, key=itemgetter(0), reverse=True)

    # Generate HTML for the top 10 songs by popularity
    top_songs_html = ''
    for i, (popularity, (track, artist, cover_url, audio_preview_url)) in enumerate(sorted_tracks[:10]):
        if audio_preview_url is not None:
            top_songs_html += f"""
                <p>{i+1}. {track} by {artist}</p>
                <img src="{cover_url}" alt="Cover Art" width="200" height="200" style="margin-left: 5%">
                <button class="play-button">Play</button>
                <audio>
                    <source src="/proxy_audio?url={audio_preview_url}" type="audio/mpeg">
                    Your browser does not support the audio element.
                </audio>
            """
        else:
            top_songs_html += f"""
                <p>{i+1}. {track} by {artist}</p>
                <img src="{cover_url}" alt="Cover Art" width="200" height="200" style="margin-left: 5%">
                <p>No audio preview available</p>
            """

    return render_template('index.html', search_option=search_option, search_query=search_query, top_songs=top_songs_html)

@app.route('/proxy_audio', methods=['GET'])
def proxy_audio():
    audio_url = request.args.get('url')
    if not audio_url:
        return Response(status=400)

    # Fetch the audio data from Spotify and serve it as a response
    audio_data = requests.get(audio_url).content
    return Response(audio_data, content_type='audio/mpeg')

if __name__ == "__main__":
    app.run()
