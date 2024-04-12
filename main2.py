import requests
from fastapi import FastAPI
from typing import Optional

app = FastAPI()

# Function to authenticate with Spotify and obtain access token
def authenticate_client(client_id: str, client_secret: str) -> Optional[str]:
    token_url = "https://accounts.spotify.com/api/token"
    client_credentials = f"{client_id}:{client_secret}"
    base64_client_credentials = b64encode(client_credentials.encode()).decode()
    headers = {
        "Authorization": f"Basic {base64_client_credentials}"
    }
    data = {
        "grant_type": "client_credentials"
    }
    response = requests.post(token_url, data=data, headers=headers)
    if response.status_code == 200:
        return response.json().get("access_token")
    else:
        return None

# Function to retrieve user's playlists from Spotify
def get_user_playlists(access_token: str, user_id: Optional[str] = None) -> list:
    playlists_url = f"https://api.spotify.com/v1/me/playlists" if not user_id else f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(playlists_url, headers=headers)
    if response.status_code == 200:
        return [playlist['name'] for playlist in response.json().get("items", [])]
    else:
        return []

# Function to search for tracks on Spotify
def search_tracks(access_token: str, query: str) -> list:
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code == 200:
        return [track['name'] for track in response.json().get("tracks", {}).get("items", [])]
    else:
        return []

# Endpoint to authenticate with Spotify
@app.get("/authenticate")
async def authenticate_spotify(client_id: str, client_secret: str):
    access_token = authenticate_client(client_id, client_secret)
    return {"access_token": access_token} if access_token else {"error": "Failed to authenticate with Spotify"}

# Endpoint to retrieve user's playlists
@app.get("/playlists")
async def fetch_playlists(access_token: str, user_id: Optional[str] = None):
    return {"playlists": get_user_playlists(access_token, user_id)}

# Endpoint to search for tracks
@app.get("/search")
async def search_spotify_tracks(access_token: str, query: str):
    return {"tracks": search_tracks(access_token, query)}
