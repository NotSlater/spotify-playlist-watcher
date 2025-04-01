import requests
import json
import time
import os
import base64

# --- CONFIG --- #
CLIENT_ID = "your_client_id" # Go to https://developer.spotify.com/dashboard
CLIENT_SECRET = "your_client_secret"
REFRESH_TOKEN = "your_refresh_token" # Generate a Spotify Refresh Token

PUSHOVER_USER_KEY = "your_pushover_user_key"
PUSHOVER_API_TOKEN = "your_pushover_api_token"

SPOTIFY_PLAYLISTS = {
    "My Playlist": "your_playlist_id" # https://open.spotify.com/playlist/your_playlist_id?si=****************
}

CHECK_INTERVAL = 600  # Default: 10 minutes

DATA_FILE = "playlist_data.json"

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
                message += "\n".join([f"- {t['name']} by {t['artist']}" for t in new_tracks]) # You may choose to comment this out
                print(message)
                send_pushover_notification(message)
            else:
                print(f"No new songs detected in {name}.")

        save_current_data(current_data)
        print("Playlist snapshots saved! Sleeping...\n")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
