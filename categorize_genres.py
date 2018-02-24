#!/usr/bin/python3

import json
from collections import defaultdict
import sys
from os import system

with open('parent-genres.txt', 'r') as f:
    parent_genres = {
        line.split(':')[0]: line.split(':')[1]
        for line in f.read().splitlines()
    }

def open_in_chrome(url):
    system('google-chrome "{0}" > /dev/null 2>&1'.format(url))

offset = -1
while offset < 0:
    try:
        offset = int(input('Enter offset: '))
    except ValueError:
        continue
    else:
        break

while True:
    print ('====================================')
    print('Parent genres:')
    for code, pg_string in sorted(parent_genres.items(), key=lambda t: t[0]):
        print('    ' + code + ' - ' + pg_string)
    with open('genre-map.json', 'r') as f:
        genre_map = defaultdict(lambda: [], json.loads(f.read()))
    print('Other options:')
    print('    q - quit')
    print('    ? - Search information about genre')
    print('There are {0} uncategorized genres.'.format(
        len(genre_map['u'])
    ))
    if not genre_map['u']:
        sys.exit(0)
    if offset >= len(genre_map['u']):
        print('Offset exceeds number of uncategorized genres.')
        print('Run this script again with a lower offset.')
        sys.exit(0)
    genre = genre_map['u'][offset]
    while True:
        pg_code = input('Enter code to categorize "{0}": '.format(
            genre
        ))
        if pg_code == 'q':
            sys.exit(0)
        elif pg_code == '?':
            open_in_chrome('http://everynoise.com/everynoise1d.cgi?root={0}&scope=all'.format(
                genre.replace(' ', '%20')
            ))
            open_in_chrome('http://google.com/search?q={0}+genre'.format(
                genre.replace(' ', '+')
            ))
        elif pg_code in parent_genres:
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
