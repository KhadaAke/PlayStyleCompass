# List of platform IDs
"""
Pc(94)
Mac(17)
Mobile (123, 96)
Nintendo ( 21, 52, 157)
Xbox (32)
PlayStation (22, 19)
Linux (152)
Browser (140)
Wii (36)
"""

import os
from dotenv import load_dotenv

load_dotenv()

platform_ids = ['94', '17', '123', '96', '21', '52', '32', '22', '152', '140', '36', '157', '19']

genres = [
    'Action', 'Adventure', 'Role-Playing', 'Strategy', 'Sports', 'Shooter',
    'Simulation', 'Puzzle', 'Horror', 'MMORPG', 'MOBA', 'Driving/Racing'
]

platforms = [
    'PC', 'PlayStation', 'Xbox', 'Nintendo', 'Android', 'iPhone',
    'Mac', 'Linux', 'Wii', 'Browser'
]

API_KEY = str(os.getenv('GBAPI_KEY'))

BASE_URL = 'https://www.giantbomb.com/api/'

headers = {
    "User-Agent": "PlayStyleCompass/1.0",
}