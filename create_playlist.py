import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pandas as pd
import math
from datetime import date
import yaml

with open("credentials.yaml", "r") as stream:
    
    try:
        credentials = yaml.safe_load(stream)
    except yaml.YAMLError as exc:
        print(exc)

SPOTIFY_CLIENT_ID = credentials["SPOTIFY_CLIENT_ID"]
SPOTIFY_CLIENT_SECRET = credentials["SPOTIFY_CLIENT_SECRET"]
SPOTIFY_REDIRECT_URI = credentials["SPOTIFY_REDIRECT_URI"]
USER = credentials["SPOTIFY_USER"]
today = date.today()

#create SP scope and auth objects
sp_modify_playlist = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, 
                                                               client_secret=SPOTIFY_CLIENT_SECRET, 
                                                               redirect_uri=SPOTIFY_REDIRECT_URI, 
                                                               scope="playlist-modify-private"))
sp_read_library = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_CLIENT_ID, 
                                                            client_secret=SPOTIFY_CLIENT_SECRET, 
                                                            redirect_uri=SPOTIFY_REDIRECT_URI, 
                                                            scope="user-library-read"))
#returns list of URIs of songs from saved albums from dictionary response
def albums_uri_list(dict):
    df = pd.DataFrame(dict)
    return_list = []
    for items1 in df['items']:
        for items2 in items1['album']['tracks']['items']:
            return_list.append(items2['uri'])
    return return_list

#returns list of URIs of songs from saved songs from dictionary response
def song_uri_list(dict):
    df = pd.DataFrame(dict)
    return_list= []
    for items1 in df['items']:
        return_list.append(items1['track']['uri'])
    return return_list


def find_all_songs(loop_run_count, api_call):
    all_songs_uris = []

    for i in range(loop_run_count):
        offset_value = i*50
        response = api_call(limit=50, offset=offset_value)
        if api_call == sp_read_library.current_user_saved_albums:
            all_songs_uris += albums_uri_list(response)
        else:
            all_songs_uris +=song_uri_list(response)
    return list(set(all_songs_uris))
    



#get a count of albums saved from library
album_count = sp_read_library.current_user_saved_albums()['total']
song_count = sp_read_library.current_user_saved_tracks()['total']
#empty list to be populated with all the song uris in each saved album
all_songs_uris = []
# number of times loop should run for albums
album_count_limit = math.ceil(album_count/50)
song_count_limit = math.ceil(song_count/50)


#list of songs from liked songs and saved albums
all_saved_songs = find_all_songs(song_count_limit,sp_read_library.current_user_saved_tracks)
all_album_songs = find_all_songs(album_count_limit,sp_read_library.current_user_saved_albums)

#iteration values
all_songs_flattened= all_saved_songs + all_album_songs
all_songs_limit = math.floor(len(all_songs_flattened)/100)

#create playlist with current date and get response for playlist ID as reference to add to later
make_playlist_response = sp_modify_playlist.user_playlist_create(user = USER, name= 'All songs updated ' + today.strftime("%m/%d/%Y"), public = False)






#go through every 100th until last iteration where the list won't be a full 100 songs. Playlist add track is limited to 100 per request
for i in range(all_songs_limit):
    index = i*100
    sp_modify_playlist.user_playlist_add_tracks(user = USER, playlist_id=make_playlist_response['id'], tracks=all_songs_flattened[index:index+100])

#for the last increment that doesn't add up to 100, start at the previous increment to end
list_start_position = 100*(all_songs_limit)
sp_modify_playlist.user_playlist_add_tracks(user = USER, playlist_id=make_playlist_response['id'], tracks=all_songs_flattened[list_start_position:])



