import requests
import json
import time
import os
import base64

# --- CONFIG --- #
CLIENT_ID = "ceb2d377d74d4f71be398bca71f06aab"
CLIENT_SECRET = "27cf316152084829aae4eaa0caeb715e"
REFRESH_TOKEN = "AQBpmJu1wPZqpU_FKOTg3zbynhCW7IGtTMd_zP6QUPVCkN2O-RTn0pB4SDJ3ko0w4eCXN8t6v-g6a_Iwiv2wU3zlhxdBz4yi2ZDrpV1UB-0ejPX8qXHVX68OTiOsOy9TyOE"

PUSHOVER_USER_KEY = "u5ms4u3kroaxc5o137vyjduh75dny5"
PUSHOVER_API_TOKEN = "ak49tjwy5k3r1gcjueerxjsdytzydu"

SPOTIFY_PLAYLISTS = {
    "Playlist 1": "5JuDEwARqrHwBTctDA85lL",
    "Playlist 2": "5j8oVJtXvZqa01lVNM7vEe"
}

CHECK_INTERVAL = 600  # 10 minutes

DATA_FILE = "/data/playlist_data.json"

# --- FUNCTIONS --- #

def ensure_data_dir():
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)

def get_access_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
    }
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN
    }
    response = requests.post(url, headers=headers, data=data)
    response.raise_for_status()
    return response.json()["access_token"]

def get_playlist_tracks(playlist_id, token):
    headers = {"Authorization": f"Bearer {token}"}

    # Step 1: Get playlist total count
    metadata_url = f"https://api.spotify.com/v1/playlists/{playlist_id}"
    metadata_response = requests.get(metadata_url, headers=headers)
    metadata_response.raise_for_status()
    total_tracks = metadata_response.json()["tracks"]["total"]

    # Step 2: Calculate where to start (last 20)
    offset = max(total_tracks - 20, 0)

    # Step 3: Fetch the actual last 20 tracks
    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?offset={offset}&limit=20"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    items = response.json()['items']

    return [
        {
            "id": item['track']['id'],
            "name": item['track']['name'],
            "artist": item['track']['artists'][0]['name']
        }
        for item in items if item.get('track')
    ]



def send_pushover_notification(message):
    data = {
        "token": PUSHOVER_API_TOKEN,
        "user": PUSHOVER_USER_KEY,
        "message": message
    }
    requests.post("https://api.pushover.net/1/messages.json", data=data)

def load_previous_data():
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r") as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}
    return {}

def save_current_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f)

# --- MAIN LOOP --- #

def main():
    print("Starting Spotify Playlist Watcher")
    ensure_data_dir()

    while True:
        access_token = get_access_token()
        previous_data = load_previous_data()
        current_data = {}

        for name, playlist_id in SPOTIFY_PLAYLISTS.items():
            print(f"Checking {name}...")
            tracks = get_playlist_tracks(playlist_id, access_token)
            track_ids = [t['id'] for t in tracks]
            current_data[name] = track_ids
        
            prev_track_ids = previous_data.get(name, [])
        
            new_tracks = [t for t in tracks if t['id'] not in prev_track_ids]
        
            if new_tracks:
                message = f"🎵 {len(new_tracks)} new song(s) added to {name}:\n"
                #message += "\n".join([f"- {t['name']} by {t['artist']}" for t in new_tracks])
                print(message)
                send_pushover_notification(message)
            else:
                print(f"No new songs detected in {name}.")

        save_current_data(current_data)
        print("Playlist snapshots saved! Sleeping...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
