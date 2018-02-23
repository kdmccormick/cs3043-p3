#!/usr/bin/python3

import json
import requests
from collections import defaultdict

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
    response = requests.get(url=base_url, headers=headers)
    if response.status_code != 200:
        print_error(response, 'User', username)
        continue
    playlists = response_items(response, 'items')
    for i, playlist in enumerate(playlists):
        print_progress(1, 'Playlist', i, playlists, playlist['name'])
        response = requests.get(
            url=(playlist['href'] + '/tracks'),
            headers=headers,
        )
        if response.status_code != 200:
            print_error(response, 'Playlist', playlist['name'])
            continue
        tracks = response_items(response, 'items')
        genre_counts = defaultdict(lambda: 0)
        for j, track in enumerate(tracks):
            print_progress(2, 'Track', j, tracks, track['track']['name'])
            artist = track['track']['album']['artists'][0]
            response = requests.get(url=artist['href'], headers=headers)
            if response.status_code != 200:
                print_error(response, 'Artist', artist['name'])
                continue
            genres = response_items(response, 'genres')
            for genre in genres:
                genre_counts[genre] += 1 / float(len(genres))
    total_counts = sum(count for genre, count in genre_counts.items())
    for genre, count in genre_counts.items():
        genre_rates[username][genre] = count / total_counts

for username in usernames:
    print(username)
    pairs = sorted(
        genre_rates[username].items(),
        key=lambda pair: pair[1],
        reverse=True,
    )
    for genre, rate in pairs:
        print('    ' + genre.ljust(24) + "{0:.2f}%".format(rate * 100).rjust(6))
