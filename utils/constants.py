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

platform_ids = [
    "94",
    "17",
    "123",
    "96",
    "21",
    "52",
    "32",
    "22",
    "152",
    "140",
    "36",
    "157",
    "19",
    "176",
    "146",
]

genres = [
    "Action",
    "Adventure",
    "Role-Playing",
    "Strategy",
    "Sports",
    "Shooter",
    "Simulation",
    "Puzzle",
    "Horror",
    "MMORPG",
    "MOBA",
    "Driving/Racing",
    "Fighting",
    "Anime",
    "Platformer",
]

all_themes = [
    "Fantasy",
    "Anime",
    "Comedy",
    "Crime",
    "Cyberpunk",
    "Horror",
    "Medieval",
    "Sci-Fi",
    "Superhero",
    "Motorsports",
    "Martial Arts",
]

all_platforms = [
    "PC",
    "PlayStation",
    "PlayStation 4",
    "PlayStation 5",
    "Xbox",
    "Nintendo",
    "Android",
    "iPhone",
    "Mac",
    "Linux",
    "Wii",
    "Browser",
]

game_ids_to_add = [
    "3030-85645",
    "3030-85432",
    "3030-89473",
    "3030-82375",
    "3030-72597",
    "3030-86375",
    "3030-75881",
    "3030-88561",
    "3030-48190",
    "3030-41484",
    "3030-73982",
    "3030-24024",
    "3030-80641",
    "3030-49998",
    "3030-56725",
    "3030-36765",
    "3030-38456",
    "3030-37030",
    "3030-80643",
    "3030-74787",
    "3030-55211",
    "3030-25462",
    "3030-73727",
    "3030-89729",
    "3030-85645",
    "3030-81387",
    "3030-89239",
    "3030-83940",
    "3030-32327",
    "3030-82842",
    "3030-86145",
]

franchises_ids_to_add = [
    "3025-82",
    "3025-6",
    "3025-38",
    "3025-609",
    "3025-282",
    "3025-7",
    "3025-2",
    "3025-397",
    "3025-267",
    "3025-1495",
    "3025-244",
    "3025-174",
    "3025-194",
    "3025-51",
]

API_KEY = str(os.getenv("GBAPI_KEY"))
GOOGLE_API_KEY = str(os.getenv("GOOGLE_API_KEY"))

BASE_URL = "https://www.giantbomb.com/api/"

headers = {
    "User-Agent": "PlayStyleCompass/1.0",
}
