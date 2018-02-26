#!/bin/bash
echo -n "Enter username: "
read username

echo $username > usernames.txt

./scrape_spotify.py && ./categorize_user_genres.py && ./guess_user_demographics.py
