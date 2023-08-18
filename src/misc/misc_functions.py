"""
The misc_functions module contains misc functions used in different parts
of the application.
"""

from constants import BASE_URL, headers, API_KEY

import requests
import json
import sqlite3

def fetch_game_ids_by_platforms(platform_ids, api_key):
    """
    Fetches game IDs for multiple platform IDs and returns a set of all fetched game IDs.
    """
    all_game_ids = set()

    for platform_id in platform_ids:
        url = f'{BASE_URL}games/?api_key={api_key}&format=json&platforms={platform_id}&limit=5'
        response = requests.get(url, headers=headers)
        game_ids = [result['id'] for result in response.json()['results']]
        all_game_ids.update(game_ids)

    return all_game_ids

def fetch_game_data(game_id):
    """Fetch game data from Giant Bomb API"""
    url = f'{BASE_URL}game/{game_id}/?api_key={API_KEY}&format=json'
    response = requests.get(url, headers=headers)
    return response.json()

def parse_game_data(game_id):
    """Parses the game data fetched using the provided game ID and extracts relevant information."""
    game_data = fetch_game_data(game_id)
    
    title = game_data['results']['name']
    description = game_data['results']['deck']
    
    genre_names = [genre['name'] for genre in game_data['results'].get('genres', [])]
    genres = ", ".join(genre_names) if genre_names else None
    
    platform_names = [platform['name'] for platform in game_data['results']['platforms']]
    platforms = ", ".join(platform_names)
    
    theme_names = [theme['name'] for theme in game_data['results'].get('themes', [])]
    themes = ", ".join(theme_names) if theme_names else None
    
    return title, description, genres, platforms, themes

def create_games_data_db(game_ids):
    """Inserts game data into a SQLite database using the provided game IDs."""
    with sqlite3.connect('games_data.db') as db_connection:
        cursor = db_connection.cursor()

        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            genres TEXT,  
            platforms TEXT,
            themes TEXT
        );
        '''
        cursor.execute(create_table_sql)
        db_connection.commit()

        for game_id in game_ids:
            title, description, genres, platforms, themes = parse_game_data(game_id)
            
            sql = "INSERT INTO Games (title, description, genres, platforms, themes) VALUES (?, ?, ?, ?, ?)"
            values = (title, description, genres, platforms, themes)
            cursor.execute(sql, values)
            db_connection.commit()
