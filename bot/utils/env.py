import os
import sys

from dotenv import load_dotenv

try:
    load_dotenv()

    BOT_TOKEN = os.environ["BOT_TOKEN"]
    FILES_CHAT = os.environ["FILES_CHAT"]
    ADMIN_ID = os.environ["ADMIN_ID"]

    DB_PATH = os.environ["DB_PATH"]

    SPOTIFY_CLIENT_ID = os.environ["SPOTIFY_CLIENT_ID"]
    SPOTIFY_CLIENT_SECRET = os.environ["SPOTIFY_CLIENT_SECRET"]

    DEEZER_ARL = os.environ["DEEZER_ARL"]

    SOUNDCLOUD_CLIENT_ID = os.environ["SOUNDCLOUD_CLIENT_ID"]

    GENIUS_CLIENT_ACCESS = os.environ["GENIUS_CLIENT_ACCESS"]

except KeyError as e:
    print("Can't parse environment", e)
    sys.exit(1)
