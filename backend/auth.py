import firebase_admin
from firebase_admin import credentials, auth
from fastapi import HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from config import settings

# Initialize Firebase App
cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
firebase_admin.initialize_app(cred)

security = HTTPBearer()

async def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    """Verify Firebase JWT token and return decoded user info."""
    try:
        token = credentials.credentials
        decoded_token = auth.verify_id_token(token)
        return decoded_token  # contains uid, email, admin flag, etc.
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication token")


def check_admin(decoded_token: dict):
    """Only allow admin users."""
    if not decoded_token.get("admin", False):
        raise HTTPException(status_code=403, detail="Admin access required")
