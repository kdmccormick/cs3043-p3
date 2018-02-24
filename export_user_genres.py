#!/usr/bin/python3

import json

with open('user-parent-genres.json', 'r') as f:
    user_parent_genres = json.loads(f.read())

user_parent_genres_list = sorted(user_parent_genres.items(), key=lambda a: a[0].lower())

lines = []
for user, genre_rates_dict in user_parent_genres_list:
    genre_rates_dict.pop('uncategorized')
    genre_rates_list = sorted(genre_rates_dict.items(), key=lambda a: a[0])
    genre_rates_strs = ['{0:.04f}'.format(a[1]) for a in genre_rates_list]
    lines.append(user + '\t' + '\t'.join(genre_rates_strs))

with open('user-parent-genres.tsv', 'w') as f:
    f.write('\n'.join(lines))
