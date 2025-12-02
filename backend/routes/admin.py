from fastapi import APIRouter, HTTPException
from models import Artist, Album, Song
from elastic import es

admin_router = APIRouter()


# ------------------ ADD ARTIST ------------------
@admin_router.post("/artist")
def add_artist(artist: Artist):
    if es.exists(index="artists", id=artist.artist_id):
        raise HTTPException(400, "Artist ID already exists.")

    es.index(index="artists", id=artist.artist_id, document=artist.dict())
    return {"message": "Artist added", "id": artist.artist_id}


# ------------------ ADD ALBUM ------------------
@admin_router.post("/album")
def add_album(album: Album):
    if es.exists(index="albums", id=album.album_id):
        raise HTTPException(400, "Album ID already exists.")

    # Validate parent artist
    if not es.exists(index="artists", id=album.artist_id):
        raise HTTPException(404, "Artist not found.")

    es.index(index="albums", id=album.album_id, document=album.dict())
    return {"message": "Album added", "id": album.album_id}


# ------------------ ADD SONG ------------------
@admin_router.post("/song")
def add_song(song: Song):

    # Validate album exists
    if not es.search(index="albums",
                     body={"query": {"term": {"title.keyword": song.album_name}}})["hits"]["hits"]:
        raise HTTPException(404, "Album does not exist. Create album first.")

    es.index(index="songs", id= song.track_id, document=song.dict())
    return {"message": "Song added", "id": song.track_id}


# ------------------ UPDATE SONG ------------------
@admin_router.put("/song/{track_id}")
def update_song(track_id: str, song: Song):
    if not es.exists(index="songs", id=track_id):
        raise HTTPException(404, "Song not found")

    es.update(index="songs", id=track_id, doc=song.dict())
    return {"message": "Song updated", "id": track_id}


# ------------------ DELETE SONG ------------------
@admin_router.delete("/song/{track_id}")
def delete_song(track_id: str):
    es.delete(index="songs", id=track_id, ignore=[404])
    return {"message": "Song deleted"}
