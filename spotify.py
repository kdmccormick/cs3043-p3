#!/usr/bin/python3

import json
import requests
from collections import defaultdict
import signal
import sys

interrupted = False
def signal_handler(signal, frame):
    global interrupted
    if interrupted:
        sys.exit(1)
    else:
        print('==========================================')
        print(' Interrupted! Will quit after this user.')
        print(' Interrupt again to quit immediately.')
        print('==========================================')
        interrupted = True

signal.signal(signal.SIGINT, signal_handler)

def print_progress(indent, item_type, index, items, item):
    print(
        ('    ' * indent) +
        item_type + ' ({0}/{1}): {2}'.format(index + 1, len(items), item)
    )

def print_error(response, item_type, item):
    print(
        'Error! Got status={0} for {1}={2}'.format(
            response.status_code, item_type, item,
        )
    )

def response_items(response, items_field_name):
    return json.loads(response.content.decode())[items_field_name]

with open('token.txt', 'r') as f:
    token = f.read()

with open('usernames.txt', 'r') as f:
    s = f.read()
usernames = s.splitlines()
usernames = [un for un in usernames if not un.startswith('#')]

genre_rates = { username: defaultdict(lambda: 0) for username in usernames }

for k, username in enumerate(usernames):
    print_progress(0, 'User', k, usernames, username)
    base_url = 'https://api.spotify.com/v1/users/' + username + '/playlists'
    headers = {
        'Authorization': 'Bearer ' + token,
        'Accept': 'application/json',
    }
    response = requests.get(
        url=base_url,
        headers=headers,
        params={'limit': 50, 'fields': 'items(name,href)'},
    )
    if response.status_code != 200:
        print_error(response, 'User', username)
        continue
    playlists = response_items(response, 'items')
    if not playlists:
        continue
    artist_counts = defaultdict(lambda: 0)
    for i, playlist in enumerate(playlists):
        print_progress(1, 'Playlist', i, playlists, playlist['name'])
        tracks = []
        offset = 0
        while True:
            response = requests.get(
                url=(playlist['href'] + '/tracks'),
                headers=headers,
                params={
                    'limit': 100,
                    'offset': offset,
                    'fields': 'items(track(name,album(artists(name,id))))',
                },
            )
            if response.status_code != 200:
                print_error(response, 'Playlist', playlist['name'])
                break
            these_tracks = response_items(response, 'items')
            tracks.extend(these_tracks)
            if len(these_tracks) < 100:
                break
            else:
                offset += 100
        if not tracks:
            continue
        for j, track in enumerate(tracks):
            #print_progress(2, 'Track', j, tracks, track['track']['name'])
            artists = track['track']['album']['artists']
            if not artists:
                continue
            artist = artists[0]
            artist_counts[artist['id']] += 1
            '''
            response = requests.get(
                url=artist['href'],
                headers=headers,
                params={'fields': 'items(name,genres)'},
            )
            if response.status_code != 200:
                print_error(response, 'Artist', artist['name'])
                continue
            genres = response_items(response, 'genres')
            for genre in genres:
                genre_counts[genre] += 1 / float(len(genres))
            '''

    genre_counts = defaultdict(lambda: 0)
    artist_ids = list(artist_counts.keys())
    if not artist_ids:
        continue
    for request_ix in range(len(artist_ids) // 50 + 1):
        these_artist_ids = artist_ids[request_ix * 50 : (request_ix + 1) * 50]
        response = requests.get(
            url='https://api.spotify.com/v1/artists',
            headers=headers,
            params={'ids': ','.join(these_artist_ids).encode('utf8')},
        )
        if response.status_code != 200:
            print('Error! Failed to get artist genres. Aborting.')
            print('these_artist_ids=' + str(these_artist_ids))
            sys.exit(1)
        artists = response_items(response, 'artists')
        for artist in artists:
            for genre in artist['genres']:
                genre_counts[genre] += artist_counts[artist['id']] / float(len(artist['genres']))

    total_counts = sum(count for genre, count in genre_counts.items())
    genre_rates = defaultdict(lambda: 0)
    for genre, count in genre_counts.items():
        genre_rates[genre] = count / total_counts
    try:
        with open('user-genres.json', 'r') as f:
            saved_user_genre_rates = json.loads(f.read())
    except:
        saved_user_genre_rates = {}

    saved_user_genre_rates[username] = genre_rates
    with open('user-genres.json', 'w') as f:
        f.write(
            json.dumps(
                saved_user_genre_rates,
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            ),
        )
    print('Wrote data to file.')

    if interrupted:
        break
