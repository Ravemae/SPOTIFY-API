import requests
from fastapi import FastAPI, HTTPException
from typing import Optional

app = FastAPI()

# Function to authenticate with Spotify and obtain access token
def authenticate_client(client_id: str, client_secret: str) -> str:
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
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to authenticate with Spotify")
    access_token = response.json().get("access_token")
    return access_token

# Function to retrieve user's playlists from Spotify
def get_user_playlists(access_token: str, user_id: Optional[str] = None) -> list:
    playlists_url = f"https://api.spotify.com/v1/me/playlists" if not user_id else f"https://api.spotify.com/v1/users/{user_id}/playlists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(playlists_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to fetch user playlists from Spotify")
    playlists_data = response.json().get("items", [])
    playlist_names = [playlist['name'] for playlist in playlists_data]
    return playlist_names

# Function to search for tracks on Spotify
def search_tracks(access_token: str, query: str) -> list:
    search_url = f"https://api.spotify.com/v1/search?q={query}&type=track"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    response = requests.get(search_url, headers=headers)
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Failed to search for tracks on Spotify")
    search_results = response.json().get("tracks", {}).get("items", [])
    track_names = [track['name'] for track in search_results]
    return track_names

# Endpoint to authenticate with Spotify
@app.get("/authenticate")
async def authenticate_spotify(client_id: str, client_secret: str):
    access_token = authenticate_client(client_id, client_secret)
    return {"access_token": access_token}

# Endpoint to retrieve user's playlists
@app.get("/playlists")
async def fetch_playlists(access_token: str, user_id: Optional[str] = None):
    playlists = get_user_playlists(access_token, user_id)
    return {"playlists": playlists}

# Endpoint to search for tracks
@app.get("/search")
async def search_spotify_tracks(access_token: str, query: str):
    tracks = search_tracks(access_token, query)
    return {"tracks": tracks}
