#!/usr/bin/python

import json

with open('parent-genres.txt', 'r') as f:
    parent_genres = {
        line.split(':')[0]: line.split(':')[1]
        for line in f.read().splitlines()
    }

with open('user-genres.json', 'r') as f:
    user_genres = json.loads(f.read())

with open('genre-map.json', 'r') as f:
    genre_map = json.loads(f.read())

reverse_genre_map = {
    sg: parent_genres[pg] for pg in genre_map for sg in genre_map[pg]
}

user_summed_genres = {}
for username, genre_rates in user_genres.items():
    summed_genres = {pg: 0 for pg in parent_genres.values()}
    for genre, rate in genre_rates.items():
        parent_genre = reverse_genre_map[genre]
        summed_genres[parent_genre] += rate
    user_summed_genres[username] = summed_genres

with open('user-parent-genres.json', 'w') as f:
    f.write(
        json.dumps(
            user_summed_genres,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )
    )