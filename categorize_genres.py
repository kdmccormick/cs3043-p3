#!/usr/bin/python3

import json
from collections import defaultdict
import sys

with open('parent-genres.txt', 'r') as f:
    parent_genres = {
        line.split(':')[0]: line.split(':')[1]
        for line in f.read().splitlines()
    }

while True:
    print ('====================================')
    print('Parent genres:')
    for code, pg_string in sorted(parent_genres.items(), key=lambda t: t[0]):
        print('    ' + code + ' - ' + pg_string)
    with open('genre-map.json', 'r') as f:
        genre_map = defaultdict(lambda: [], json.loads(f.read()))
    print('There are {0} uncategorized genres.'.format(
        len(genre_map['u'])
    ))
    print('Enter "q" to quit.')
    genre = genre_map['u'][0]
    while True:
        pg_code = input('Enter code to categorize "{0}": '.format(
            genre
        ))
        if pg_code == 'q':
            sys.exit(0)
        if pg_code in parent_genres:
            break
    genre_map['u'].remove(genre)
    genre_map[pg_code].append(genre)
    with open('genre-map.json', 'w') as f:
        f.write(
            json.dumps(
                dict(genre_map),
                sort_keys=True,
                indent=4,
                separators=(',', ': '),
            )
        )
    print('Successfully categorized under "{0}".'.format(
        parent_genres[pg_code]
    ))
