# 🎵 Trackify - A Spotify Playlist Tracking Bot

[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](https://www.python.org/)
[![Spotify Web API](https://img.shields.io/badge/Spotify-API-1DB954?logo=spotify&logoColor=white)](https://developer.spotify.com/)
[![Pushover](https://img.shields.io/badge/Pushover-Notifications-blueviolet)](https://pushover.net)
[![Deployment](https://img.shields.io/badge/Deployed%20on-Railway-0B0D0E?logo=railway&logoColor=white)](https://railway.app/)

---

## 📚 Table of Contents
- [About](#about)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Installation & Setup](#installation--setup)

---

## 📖 About

A lightweight Python bot that automatically monitors one or more Spotify playlists and sends you instant push notifications via Pushover when new songs are added.

---

## ✨ Features
- ✅ Detects newly added songs
- ✅ Sends instant notifications with song title & artist
- ✅ Tracks multiple playlists
- ✅ Automatically refreshes Spotify tokens (no manual input required)
- ✅ Railway-ready (free cloud hosting)
- ✅ Configurable check interval

---

## ⚙️ Tech Stack

| Tool | Purpose |
|------|---------|
| Python | Core programming language |
| Spotify Web API | Playlist data access |
| Pushover API | Mobile Push notifications |
| Railway | Cloud hosting |
| JSON | Local data storage (playlist snapshots) |

---

## 🚀 Installation & Setup

### 1️⃣ Create a Spotify Developer Application
1. Go to the [Spotify Developer Dashboard](https://developer.spotify.com/dashboard)
2. Create a new app and fill it in:
   - `Trackify`
   - `Tracks playlists on psotify`
3. Under Redirect URIs, add:
   - `http://localhost:8080/callback`
4. Under API/SDKs, select:
   - `Web API`
2. Go to the app and hit settings and copy:
   - `Client ID`
   - `Client Secret`

### 2️⃣ Create a Pushover Application
1. Download [Pushover](https://pushover.net/apps/build) on your device
2. Create a new app
3. Copy your:
- `User Key`
- `API Token/Key`

### 3️⃣ Generate Spotify Refresh Token
Follow the prompts to generate a permanent refresh token.  
This prevents you from having to generate a new Spotify API key every hour.
```bash
python spotify_refresh_token_generator.py
```

### 4️⃣ Fork the Repository
1. Fork this repository to your own GitHub account
2. Fill these fields:
```bash
CLIENT_ID = "your_client_id"
CLIENT_SECRET = "your_client_secret"
REFRESH_TOKEN = "your_refresh_token"

PUSHOVER_USER_KEY = "your_pushover_user_key"
PUSHOVER_API_TOKEN = "your_pushover_api_token"

SPOTIFY_PLAYLISTS = {
    "My Playlist": "your_playlist_id"
}
```
You can also add multiple playlists like this:
```bash
SPOTIFY_PLAYLISTS = {
    "Playlist 1": "playlist_id_1",
    "Playlist 2": "playlist_id_2"
}
```

### 5️⃣ Connect to Railway
1. Sign into [Railway](https://railway.com) using github
2. Select the forked repo in Railway
3. Let it run
