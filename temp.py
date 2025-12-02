import pandas as pd
import random
import string

# tiny id generator
def tiny_id(length=None):
    if length is None:
        length = random.choice([4,5,6])
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))


df = pd.read_csv("dataset.csv")

# remove unwanted columns
cols_to_remove = [
    "track_id", "key", "loudness", "mode", 
    "speechiness", "valence", "tempo"
]
df = df.drop(columns=cols_to_remove)

# stratified sampling setup
genres = df["track_genre"].unique()
selected_rows = []
per_genre = max(1, 500 // len(genres))   # approx rows per genre

# STEP 1: stratified sampling
for g in genres:
    sub = df[df["track_genre"] == g]
    take = min(per_genre, len(sub))
    selected_rows.append(sub.sample(take, random_state=42))

df500 = pd.concat(selected_rows)

# STEP 2: if less than 500 rows, fill the gap
if len(df500) < 500:
    needed = 500 - len(df500)
    extra = df.drop(df500.index).sample(needed, random_state=42)
    df500 = pd.concat([df500, extra])

# Final cleanup: ensure exactly 500 rows
df500 = df500.sample(500, random_state=42)  # SAFE NOW

# ---- normalization into artists/albums/tracks -----

artists_dict = {}
albums_dict = {}
tracks_list = []

for _, row in df500.iterrows():

    artist_name = row["artists"]
    artist_id = artist_name.lower().replace(" ", "_")[:6] + tiny_id(2)

    if artist_id not in artists_dict:
        artists_dict[artist_id] = {
            "artist_id": artist_id,
            "name": artist_name,
            "genres": [row["track_genre"]],
            "popularity": int(row["popularity"])
        }

    album_name = row["album_name"]
    album_id = (album_name.lower().replace(" ", "_")[:6]
                + "_" + tiny_id(3))

    if album_id not in albums_dict:
        albums_dict[album_id] = {
            "album_id": album_id,
            "title": album_name,
            "artist_id": artist_id,
            "release_date": "2000-01-01"
        }

    track_id = tiny_id()

    tracks_list.append({
        "track_id": track_id,
        "title": row["track_name"],
        "artist_id": artist_id,
        "album_id": album_id,
        "popularity": int(row["popularity"]),
        "duration_ms": int(row["duration_ms"]),
        "danceability": float(row["danceability"]),
        "energy": float(row["energy"]),
        "acousticness": float(row["acousticness"]),
        "instrumentalness": float(row["instrumentalness"]),
        "liveness": float(row["liveness"]),
        "track_genre": row["track_genre"]
    })


artists_df = pd.DataFrame(artists_dict.values())
albums_df = pd.DataFrame(albums_dict.values())
tracks_df = pd.DataFrame(tracks_list)

artists_df.to_csv("artists_clean.csv", index=False)
albums_df.to_csv("albums_clean.csv", index=False)
tracks_df.to_csv("tracks_clean.csv", index=False)

print("SUCCESS → 500 rows created + normalized into artist/album/track tables")
