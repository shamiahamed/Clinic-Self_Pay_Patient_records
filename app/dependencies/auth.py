from fastapi import Depends, HTTPException, status, Header
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
import jwt

security = HTTPBearer()

# For Keycloak/RS256, you'd normally need a Public Key. 
# For now, we set options to skip verification so you can test.
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    application_id: str = Header(None, alias="application-id")
):
    try:
        token = credentials.credentials
        
        # We use options={"verify_signature": False} to allow the Keycloak token 
        # without needing the RSA Public Key right now.
        payload = jwt.decode(token, options={"verify_signature": False})

        # Keycloak specific claims:
        # 'sub' is the unique User ID
        # 'preferred_username' is the login name (vineeth93822)
        user_id = payload.get("sub")
        username = payload.get("preferred_username")
        
        # Check roles in the token
        roles = payload.get("realm_access", {}).get("roles", [])

        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid token: No user ID found"
            )

        # Return the user info to your controller
        return {
            "user_id": user_id,
            "username": username,
            "roles": roles,
            "application_id": application_id
        }

    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Authentication failed: {str(e)}"
        )