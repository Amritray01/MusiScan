from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    FIREBASE_CREDENTIALS_PATH: str
    FIREBASE_PROJECT_ID: str = None

    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_USERNAME: str = None
    ELASTICSEARCH_PASSWORD: str = None

    CORS_ALLOWED_ORIGINS: str

    TRACKS_CLEAN_PATH: str
    ARTISTS_CLEAN_PATH: str
    ALBUMS_CLEAN_PATH: str

    SECRET_KEY: str

    CHECK_NEW_SONGS_INTERVAL: float = 1.0  # minutes
    CHECK_TOP_ARTIST_INTERVAL: float = 1.0  # minutes

    @property
    def new_songs_interval_seconds(self):
        return self.CHECK_NEW_SONGS_INTERVAL * 60


    class Config:
        env_file = ".env"

settings = Settings()