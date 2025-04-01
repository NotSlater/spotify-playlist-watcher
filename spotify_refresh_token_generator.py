import requests
import base64
import urllib.parse
import webbrowser
from http.server import HTTPServer, BaseHTTPRequestHandler

# --- Step 1: Get user input dynamically ---
print("🎵 Spotify Refresh Token Generator\n")

CLIENT_ID = input("Enter your Spotify Client ID: ").strip()
CLIENT_SECRET = input("Enter your Spotify Client Secret: ").strip()

REDIRECT_URI = "http://localhost:8080/callback"
SCOPE = "playlist-read-private playlist-read-collaborative"

# --- Step 2: Build the authorization URL ---
params = {
    "client_id": CLIENT_ID,
    "response_type": "code",
    "redirect_uri": REDIRECT_URI,
    "scope": SCOPE
}

url = "https://accounts.spotify.com/authorize?" + urllib.parse.urlencode(params)

print("\nOpening Spotify authorization page...")
webbrowser.open(url)

# --- Step 3: Wait for Spotify to redirect to localhost ---
class RedirectHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        query = urllib.parse.urlparse(self.path).query
        params = urllib.parse.parse_qs(query)
        code = urllib.parse.unquote(params.get("code", [""])[0])

        # Immediately exchange for refresh token
        auth_header = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode()
        headers = {
            "Authorization": f"Basic {auth_header}",
            "Content-Type": "application/x-www-form-urlencoded"
        }
        data = {
            "grant_type": "authorization_code",
            "code": code,
            "redirect_uri": REDIRECT_URI
        }
        response = requests.post("https://accounts.spotify.com/api/token", headers=headers, data=data)
        response_data = response.json()

        refresh_token = response_data.get("refresh_token", "Error: Refresh token not found")

        # Store refresh token for terminal too
        self.server.refresh_token = refresh_token

        # Display refresh token directly on the web page
        self.wfile.write(f"""
        <html>
            <head><title>Spotify Token Generator</title></head>
            <body style="font-family:sans-serif; background:#1e1e1e; color:white; display:flex; justify-content:center; align-items:center; height:100vh;">
                <div style="background:#2c2c2c; padding:30px; border-radius:8px; box-shadow:0 2px 10px rgba(0,0,0,0.5); text-align:center; max-width:600px;">
                    <h1 style="color:white; margin-bottom: 5px;">Trackify</h1>
                    <h2 style="color: #1DB954;">&#9989; Refresh Token Generated</h2>
                    <p>Please copy your Refresh Token and proceed to the terminal:</p>
                    <div style="background:#444; padding:10px; border-radius:5px; margin:15px 0; word-break:break-all;">
                        <code>{refresh_token}</code>
                    </div>
                    <button onclick="navigator.clipboard.writeText('{refresh_token}'); alert('Copied!')"
                    style="background:#1DB954; border:none; padding:8px 12px; border-radius:4px; cursor:pointer; color:black; font-weight:bold;">
                        Copy to Clipboard
                    </button>
                    <p style="margin-top:20px; color: #aaaaaa;">You may now close this page.</p>
                    <hr style="margin-top:20px; border:0; border-top:1px solid #444;">
                    <small style="color:gray;">Made by NotSlater | &copy; 2025 | MIT License</small>
                </div>
            </body>
        </html>
        """.encode())


server = HTTPServer(('localhost', 8080), RedirectHandler)
print("Waiting for Spotify authorization (check your browser)...")
server.handle_request()
refresh_token = server.refresh_token

# --- Step 5: Show result ---
print("You may now exit the terminal if you have copied your Refresh Token.\n")
#print("\n✅ Your Refresh Token:")
#print(refresh_token)

print("!! Note: Rerunning this script will force you to change the refresh token in main.py !!")
