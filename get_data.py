from datetime import datetime
import spotify, youtube
import pandas as pd

def get_track_data(q, youtube_item = None, spotify_item = None):
    raw_data = {}
    raw_data['q'] = q
    if not youtube_item:
        raw_data['youtube'] = youtube.search_track(q)
    else:
        raw_data['youtube'] = youtube_item
    if not spotify_item:
        raw_data['spotify'] = spotify.search_track(q)
    else:
        raw_data['spotify'] = spotify_item
    return raw_data

filename = f"data/results_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.csv"
print("The data wil be saved in " + filename)
print("Type \"exit\" to stop and save ")
print("--")

q = ""
rows = pd.DataFrame(columns=['q', 'youtube', 'spotify'])
while q != "exit":
    if q != "exit" and len (q) > 5 :
        if "/playlist/" in q:
            tracks = spotify.get_playlist(q)['tracks']['items']
            for track in tracks:
                row = {}
                q = track['track']['artists'][0]['name'] + " - " + track['track']['name']
                raw_data = get_track_data(q, spotify_item=track)
                row[0] = raw_data
                row = pd.DataFrame(row).T
                rows = pd.concat([rows, row], ignore_index=True)
                print(rows)
                if len(rows) > 0:
                    rows.to_csv(filename)
        else:
            row = {}
            row[0] = get_track_data(q)
            row = pd.DataFrame(row).T
            rows = pd.concat([rows, row], ignore_index=True)
            rows.to_csv(filename)
        print(rows)
    q =  input("Enter a track name or a Spotify playlist link: ")
