#!/usr/bin/python3

import json

with open('parent-genres.tsv', 'r') as f:
    parent_genres = {
        line.split('\t')[0]: line.split('\t')[1]
        for line in f.read().splitlines()
    }

with open('user-parent-genres.json', 'r') as f:
    user_parent_genres = json.loads(f.read())

with open('genre-indicators.tsv', 'r') as f:
    genre_indicators = {
        parent_genres[line.split('\t')[0]]:
            (int(line.split('\t')[1]), int(line.split('\t')[2]))
        for line in f.read().splitlines()
    }

with open('parent-genre-song-counts.tsv') as f:
    genre_total_counts = {
        line.split('\t')[0]: float(line.split('\t')[1])
        for line in f.read().splitlines()
    }

genre_total_counts.pop('uncategorized')
total_genre_total_counts = sum(genre_total_counts.values())
genre_avg_proportions = {
    g: c / total_genre_total_counts
    for g, c in genre_total_counts.items()
}

for user, genre_rates in user_parent_genres.items():
    genre_rates.pop('uncategorized')
    genre_avg_deviations = {
        g: (((gr - genre_avg_proportions[g]) / genre_avg_proportions[g]) if gr else 0)
        for g, gr in genre_rates.items()
    }
    male_score = sum(gd * genre_indicators[g][0] for g, gd in genre_avg_deviations.items())
    town_score = sum(gd * genre_indicators[g][1] for g, gd in genre_avg_deviations.items())
    print('user = {0} ; male score = {1:.2f} ; town score = {2:.2f}'.format(
        user, male_score, town_score
    ))
