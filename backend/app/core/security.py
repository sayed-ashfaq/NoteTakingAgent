
import jwt
from jwt import PyJWKClient
from fastapi import Depends, HTTPException, Security, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.config import settings

# Clerk JWKS URL
CLERK_JWKS_URL = f"https://api.clerk.dev/v1/jwks" 
# Or from publishable key -> domain? 
# Usually https://<instance>.clerk.accounts.dev/.well-known/jwks.json
# BUT for simplicity, if user has instance domain, use it.
# Settings approach: CLERK_ISSUER should be configured.

security = HTTPBearer()

def verify_token(credentials: HTTPAuthorizationCredentials = Security(security)):
    token = credentials.credentials
    try:
        # Use PyJWKClient to fetch and cache keys
        jwks_client = PyJWKClient(settings.CLERK_ISSUER + "/.well-known/jwks.json")
        signing_key = jwks_client.get_signing_key_from_jwt(token)
        
        payload = jwt.decode(
            token,
            signing_key.key,
            algorithms=["RS256"],
            audience=None, # Clerk audience verification optional/context dependent
            issuer=settings.CLERK_ISSUER
        )
        return payload
    except jwt.PyJWTError as e:
        raise HTTPException(status_code=401, detail=f"Invalid token: {e}")
    except Exception as e:
        raise HTTPException(status_code=401, detail="Could not validate credentials")

def get_current_user_id(payload: dict = Depends(verify_token)) -> str:
    return payload.get("sub")
