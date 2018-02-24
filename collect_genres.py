#!/usr/bin/python3

import json
from os import path
import sys

if path.exists('genre-map.json'):
    if input(
            'This will override catagorized genres.\n' + 
            'Enter "y" to continue, or anything else to abort: '
    ) != 'y':
        print('Aborted.')
        sys.exit(1)

with open('user-genres.json', 'r') as f:
    user_genres = json.loads(f.read())

all_genres = []
for genres in user_genres.values():
    all_genres.extend(genres)

with open('genre-map.json', 'w') as f:
    f.write(
        json.dumps(
            {'u': sorted(list(set(all_genres)))},
            sort_keys=True,
            indent=4,
            separators=(',', ': '),
        )
    )

print('Successfully wrote to genre-map.json')