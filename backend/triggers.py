from apscheduler.schedulers.background import BackgroundScheduler
from elasticsearch import Elasticsearch
from datetime import datetime
from config import settings

es = Elasticsearch([settings.ELASTICSEARCH_HOST])


def new_songs_trigger():
    """Check for new songs in last 24 hours."""
    query = {
        "query": {
            "range": {
                "release_date": {
                    "gte": "now-1d/d"
                }
            }
        }
    }

    result = es.search(index="songs", body=query)

    count = result["hits"]["total"]["value"]
    if count > 0:
        alert = {
            "alert_type": "new_songs",
            "message": f"{count} new songs released in last 24 hours!",
            "data": {
                "count": count,
                "songs": [hit["_source"]["track_name"] for hit in result["hits"]["hits"][:5]],
            },
            "timestamp": datetime.now(),
        }
        es.index(index="alerts", document=alert)


def top_artist_trigger():
    """Determine top trending artist using popularity."""
    agg_query = {
        "size": 0,
        "aggs": {
            "top_artist": {
                "terms": {
                    "field": "artists.keyword",
                    "size": 1,
                },
                "aggs": {
                    "avg_popularity": {"avg": {"field": "popularity"}},
                },
            }
        }
    }

    result = es.search(index="songs", body=agg_query)
    bucket = result["aggregations"]["top_artist"]["buckets"]

    if bucket:
        top = bucket[0]
        alert = {
            "alert_type": "top_artist",
            "message": f"🔥 {top['key']} is now the top trending artist!",
            "data": {
                "artist": top["key"],
                "popularity": top["avg_popularity"]["value"],
            },
            "timestamp": datetime.now(),
        }
        es.index(index="alerts", document=alert)


def start_triggers():
    """Start scheduled cron triggers."""
    scheduler = BackgroundScheduler()
    scheduler.add_job(new_songs_trigger, "cron", hour=0, minute=0)
    scheduler.add_job(top_artist_trigger, "cron", hour=0, minute=5)
    scheduler.start()
