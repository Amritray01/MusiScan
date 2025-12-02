from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# ---------------- SONG ------------------
class Song(BaseModel):
    id: Optional[str] = None
    track_id: str
    track_name: str
    artists: str
    album_name: str
    track_genre: str
    popularity: int
    duration_ms: int
    danceability: float
    energy: float
    acousticness: float
    instrumentalness: float
    liveness: float
    release_date: str 
class Artist(BaseModel):
    name: str
    popularity: int
    song_count: int
    genres: List[str]
class Album(BaseModel):
    album_id: str
    title: str
    artist_id: str
    release_date: Optional[str]
class Favorite(BaseModel):
    user_id: str
    item_type: str   # "artist", "album", "track"
    item_value: str  # ID of the item
class Alert(BaseModel):
    alert_type: str
    message: str
    data: dict
    timestamp: datetime