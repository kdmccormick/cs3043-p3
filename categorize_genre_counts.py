#!/usr/bin/python3

import json

with open('parent-genres.tsv', 'r') as f:
    parent_genres = {
        line.split('\t')[0]: line.split('\t')[1]
        for line in f.read().splitlines()
    }

with open('genre-map.json', 'r') as f:
    genre_map = json.loads(f.read())

reverse_genre_map = {
    sg: parent_genres[pg] for pg in genre_map for sg in genre_map[pg]
}

with open('genre-song-counts.tsv', 'r') as f:
    genre_song_counts = {
        line.split('\t')[0]: float(line.split('\t')[1])
        for line in f.read().splitlines()
    }

parent_genre_song_counts = {pg: 0.0 for pg in parent_genres.values()}

for genre, count in genre_song_counts.items():
    if not genre in reverse_genre_map:
        print('Warning: {0} not in genre map'.format(genre))
        continue
    parent_genre_song_counts[reverse_genre_map[genre]] += count

parent_genre_song_counts_list = sorted(
    parent_genre_song_counts.items(),
    key=lambda x: x[0],
)
parent_genre_song_counts_str = '\n'.join(
    '{0}\t{1:.2f}'.format(pg, count)
    for pg, count in parent_genre_song_counts_list
)

with open('parent-genre-song-counts.tsv', 'w') as f:
    f.write(parent_genre_song_counts_str)