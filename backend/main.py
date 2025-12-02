# backend/main.py

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes.admin import admin_router
from routes.user import user_router
from triggers import start_triggers
from elastic import es

app = FastAPI(
    title="Music Search & Favorites System",
    description="FastAPI + Elasticsearch + Firebase Auth",
    version="1.0.0"
)

# ----------------------------------------------------------------------
# CORS
# ----------------------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------------------------------------------------
# ROUTERS
# ----------------------------------------------------------------------
# Final prefix structure:
# /api/user/...   (public + authenticated user routes)
# /api/admin/...  (admin-only actions)
app.include_router(user_router, prefix="/api/user", tags=["User"])
app.include_router(admin_router, prefix="/api/admin", tags=["Admin"])

# ----------------------------------------------------------------------
# STARTUP EVENTS
# ----------------------------------------------------------------------
@app.on_event("startup")
def startup_events():
    print("🚀 Starting system...")

    # Start cron triggers (top artist, new songs)
    try:
        start_triggers()
        print("✓ APScheduler triggers started")
    except Exception as e:
        print("⚠ Trigger startup error:", e)

    # Verify Elasticsearch connectivity
    try:
        health = es.cluster.health()
        print("✓ Elasticsearch connected:", health["status"])
    except Exception as e:
        print("❌ Elasticsearch error:", e)


# ----------------------------------------------------------------------
# ROOT ENDPOINT
# ----------------------------------------------------------------------
@app.get("/")
def root():
    return {
        "service": "Spotify NoSQL API Running",
        "elasticsearch_status": es.cluster.health(),
        "available_endpoints": {
            "USER ROUTES": [
                "GET /api/user/songs",
                "GET /api/user/albums",
                "GET /api/user/artists",
                "GET /api/user/alerts",
                "GET /api/user/search?q=",
                "GET /api/user/autocomplete?q=",
                "POST /api/user/favorite",
                "GET /api/user/favorites",
                "DELETE /api/user/favorite",
            ],
            "ADMIN ROUTES": [
                "POST /api/admin/artist",
                "POST /api/admin/album",
                "POST /api/admin/song",
            ]
        }
    }
