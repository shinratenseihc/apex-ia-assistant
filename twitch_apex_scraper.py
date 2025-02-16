import requests
import json

# ⚡️ Remplace par tes credentials Twitch
CLIENT_ID = "TON_CLIENT_ID"
CLIENT_SECRET = "TON_CLIENT_SECRET"

def get_access_token():
    url = "https://id.twitch.tv/oauth2/token"
    params = {
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
        "grant_type": "client_credentials"
    }
    response = requests.post(url, params=params)
    data = response.json()
    return data["access_token"]

def get_apex_streams(access_token):
    url = "https://api.twitch.tv/helix/streams"
    headers = {
        "Client-ID": CLIENT_ID,
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "game_id": "511224",  # ID du jeu Apex Legends
        "language": "fr",  # Optionnel, pour filtrer les streams FR
        "first": 20  # Nombre max de streams récupérés
    }
    response = requests.get(url, headers=headers, params=params)
    return response.json()

def filter_solo_streams(streams):
    solo_streams = []
    for stream in streams.get("data", []):
        title = stream["title"].lower()
        if "solo" in title or "1v1" in title:
            solo_streams.append({
                "title": stream["title"],
                "viewer_count": stream["viewer_count"],
                "streamer": stream["user_name"]
            })
    return solo_streams

def main():
    access_token = get_access_token()
    streams = get_apex_streams(access_token)
    solo_streams = filter_solo_streams(streams)
    
    print("\n🔹 Streamers Apex Solo en Live :\n")
    for stream in solo_streams:
        print(f"🎮 {stream['streamer']} | Viewers: {stream['viewer_count']} | Titre: {stream['title']}")

if __name__ == "__main__":
    main()
