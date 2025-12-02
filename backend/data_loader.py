import pandas as pd
from elasticsearch import Elasticsearch, helpers
from config import settings

es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="D:/Coding/elasticsearch/elasticsearch-8.11.0/config/certs/http_ca.crt",
    basic_auth=("elastic", "your_password")
)

def load_tracks(file_path):
    df = pd.read_csv(file_path)

    actions = []
    for _, row in df.iterrows():
        actions.append({
            "_index": "songs",
            "_id": row["track_id"],
            "_source": row.to_dict()
        })

    helpers.bulk(es, actions)
    print(f"Loaded {len(actions)} tracks")


def load_artists(file_path):
    df = pd.read_csv(file_path)

    actions = []
    for _, row in df.iterrows():
        actions.append({
            "_index": "artists",
            "_id": row["artist_id"],
            "_source": row.to_dict()
        })

    helpers.bulk(es, actions)
    print(f"Loaded {len(actions)} artists")


def load_albums(file_path):
    df = pd.read_csv(file_path)

    actions = []
    for _, row in df.iterrows():
        actions.append({
            "_index": "albums",
            "_id": row["album_id"],
            "_source": row.to_dict()
        })

    helpers.bulk(es, actions)
    print(f"Loaded {len(actions)} albums")


def load_all_clean():
    load_tracks("data/cleaned/tracks_clean.csv")
    load_artists("data/cleaned/artists_clean.csv")
    load_albums("data/cleaned/albums_clean.csv")


if __name__ == "__main__":
    load_all_clean()
