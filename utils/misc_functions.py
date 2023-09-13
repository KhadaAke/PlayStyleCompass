"""
The misc_functions module contains misc functions used in different parts
of the application.
"""

from constants import BASE_URL, headers, API_KEY

import requests
import json
import sqlite3
from datetime import datetime
from bs4 import BeautifulSoup


def fetch_game_ids_by_platforms(platform_ids, api_key):
    """
    Fetches game IDs for multiple platform IDs and returns a set of all fetched game IDs.
    """
    all_game_ids = set()

    current_date = datetime.now().date()

    for platform_id in platform_ids:
        url = f'{BASE_URL}games/?api_key={api_key}&format=json&platforms={platform_id}&filter=original_release_date:|{current_date}&sort=original_release_date:desc&limit=50'
        response = requests.get(url, headers=headers)

        if response.status_code == 200:
            game_ids = [result['id'] for result in response.json()['results']]
            all_game_ids.update(game_ids)

    return all_game_ids

def fetch_game_data(game_id):
    """Fetch game data from Giant Bomb API"""
    url = f'{BASE_URL}game/{game_id}/?api_key={API_KEY}&format=json'
    response = requests.get(url, headers=headers)
    return response.json()

def extract_overview_content(data):
    """Extract overview content from game data."""
    if 'description' in data and data['description']:
        soup = BeautifulSoup(data['description'], 'html.parser')

        overview_tag = soup.find('h2', string='Overview')
        
        if overview_tag:
            overview_content = []

            current_element = overview_tag.find_next_sibling()
            while current_element and current_element.name != 'h2':
                if current_element.name == 'p':
                    overview_content.append(current_element.get_text())
                current_element = current_element.find_next_sibling()

            overview_text = '\n'.join(overview_content)

            return overview_text
    
    return None

def parse_game_data(game_id):
    """Parses the game data fetched using the provided game ID and extracts relevant information."""
    game_data = fetch_game_data(game_id)['results']

    title = game_data['name']

    description = game_data['deck']

    overview = extract_overview_content(game_data)
    
    genre_names = [genre['name'] for genre in game_data.get('genres', [])]
    genres = ", ".join(genre_names) if genre_names else None
    
    platform_names = [platform['name'] for platform in game_data['platforms']]
    platforms = ", ".join(platform_names) if platform_names else None
    
    theme_names = [theme['name'] for theme in game_data.get('themes', [])]
    themes = ", ".join(theme_names) if theme_names else None
    
    image_url = game_data['image'].get('small_url', None)
    image = 'https://i.ibb.co/HnJFgmy/default-psc.jpg' if image_url and 'default' in image_url else image_url
    
    release_date = game_data['original_release_date'] if game_data['original_release_date'] is not None else game_data['expected_release_year']

    if 'developers' in game_data and isinstance(game_data['developers'], list):
        developer_names = [developer['name'] for developer in game_data['developers']]
        developers = ", ".join(developer_names) if developer_names else None
    else:
        developers = None

    return title, description, overview, genres, platforms, themes, image, release_date, developers

def create_games_data_db(game_ids):
    """Inserts game data into a SQLite database using the provided game IDs."""
    with sqlite3.connect('games_data.db') as db_connection:
        cursor = db_connection.cursor()

        create_table_sql = '''
        CREATE TABLE IF NOT EXISTS Games (
            id INTEGER PRIMARY KEY,
            title TEXT,
            description TEXT,
            overview TEXT,
            genres TEXT,  
            platforms TEXT,
            themes TEXT,
            image TEXT,
            release_date TEXT,
            developers TEXT
        );
        '''
        cursor.execute(create_table_sql)
        db_connection.commit()

        for game_id in game_ids:
            title, description, overview, genres, platforms, themes, image, release_date, developers = parse_game_data(game_id)
            
            sql = "INSERT INTO Games (title, description, overview, genres, platforms, themes, image, release_date, developers) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)"
            values = (title, description, overview, genres, platforms, themes, image, release_date, developers)
            cursor.execute(sql, values)
            db_connection.commit()

        # Remove duplicates based on the title
        remove_duplicates_sql = '''
        DELETE FROM Games
        WHERE rowid NOT IN (
            SELECT MIN(rowid)
            FROM Games
            GROUP BY title
        );
        '''
        cursor.execute(remove_duplicates_sql)
        db_connection.commit()
