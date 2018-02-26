#!/usr/bin/python3

import json

with open('parent-genres.tsv', 'r') as f:
    parent_genre_codes = [
        line.split('\t')[0]
        for line in f.read().splitlines()
    ]

with open('genre-map.json', 'r') as f:
    genre_map = json.loads(f.read())

already_categorized = set()

for pgc in parent_genre_codes:
    in_genre = set(genre_map[pgc])
    genre_map[pgc] = sorted(list(in_genre - already_categorized))
    already_categorized = already_categorized | set(genre_map[pgc])

with open('genre-map.json', 'w') as f:
    f.write(
        json.dumps(
            genre_map,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )
    )