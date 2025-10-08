from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

authenticate = HTTPBearer()


def validate_token(credentials: HTTPAuthorizationCredentials = Depends(authenticate)):
    token = credentials.credentials
    if token != "X4M8P2Q9Z7":
        raise HTTPException(status_code=403, detail="Invalid or missing token")
