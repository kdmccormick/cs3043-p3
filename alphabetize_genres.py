#!/usr/bin/python3

import json

with open('genre-map.json', 'r') as f:
    genre_map = json.loads(f.read())

sorted_genre_map = {k: sorted(v) for k, v in genre_map.items()}

with open('genre-map.json', 'w') as f:
    f.write(
        json.dumps(
            sorted_genre_map,
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )
    )