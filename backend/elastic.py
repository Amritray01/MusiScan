from elasticsearch import Elasticsearch
from config import settings

# Elasticsearch client
es = Elasticsearch(
    "https://localhost:9200",
    ca_certs="D:/Coding/elasticsearch/elasticsearch-8.11.0/config/certs/http_ca.crt",
    basic_auth=("elastic", "elastic_password")
)

# ----------------------- Index Mappings -----------------------

songs_mapping = {
    "settings": {
        "analysis": {
            "analyzer": {
                "autocomplete": {
                    "type": "custom",
                    "tokenizer": "standard",
                    "filter": ["lowercase", "autocomplete_filter"]
                }
            },
            "filter": {
                "autocomplete_filter": {"type": "edge_ngram", "min_gram": 2, "max_gram": 20}
            }
        }
    },
    "mappings": {
        "properties": {
            "track_id": {"type": "keyword"},
            "track_name": {
                "type": "text",
                "fields": {
                    "autocomplete": {"type": "text", "analyzer": "autocomplete"},
                    "keyword": {"type": "keyword"}
                }
            },
            "artists": {
                "type": "text",
                "fields": {
                    "autocomplete": {"type": "text", "analyzer": "autocomplete"},
                    "keyword": {"type": "keyword"}
                }
            },
            "album_name": {"type": "keyword"},
            "track_genre": {"type": "keyword"},
            "popularity": {"type": "integer"},
            "duration_ms": {"type": "integer"},
            "danceability": {"type": "float"},
            "energy": {"type": "float"},
            "acousticness": {"type": "float"},
            "instrumentalness": {"type": "float"},
            "liveness": {"type": "float"},
            "release_date": {"type": "date", "format": "yyyy-MM-dd||epoch_millis"}
        }
    }
}

artists_mapping = {
    "mappings": {
        "properties": {
            "name": {"type": "keyword"},
            "popularity": {"type": "integer"},
            "song_count": {"type": "integer"},
            "genres": {"type": "keyword"}
        }
    }
}

favorites_mapping = {
    "mappings": {
        "properties": {
            "user_id": {"type": "keyword"},
            "item_type": {"type": "keyword"},
            "item_value": {"type": "keyword"}
        }
    }
}

alerts_mapping = {
    "mappings": {
        "properties": {
            "alert_type": {"type": "keyword"},
            "message": {"type": "text"},
            "data": {"type": "object"},
            "timestamp": {"type": "date"}
        }
    }
}

indices = {
    "songs": songs_mapping,
    "artists": artists_mapping,
    "favorites": favorites_mapping,
    "alerts": alerts_mapping
}

# ----------------------- Index Creation -----------------------

def create_indices():
    for name, mapping in indices.items():
        if not es.indices.exists(index=name):
            es.indices.create(index=name, body=mapping)
            print(f"Created index: {name}")
        else:
            print(f"Index already exists: {name}")

if __name__ == "__main__":
    create_indices()
