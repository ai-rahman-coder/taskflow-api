## Real JWT-based auth implementation using python-jose and passlib. Replace with real user database later.
from fastapi import Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(HTTPBearer())):    
    token = credentials.credentials

    payload = decode_access_token(token)

    if not payload:
        raise HTTPException(status_code=401, detail="Invalid or expired token")
    
    return {"id": payload["user_id"], "role": payload["role"]}



## Fake auth for testing purposes. Replace with real JWT-based auth later.
# from fastapi import Depends, HTTPException
# from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

# security = HTTPBearer()

# def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
#     token = credentials.credentials
#     print(f"Received token: {token}")

#     try:
#         role, user_id = token.split("_")
#         user_id = int(user_id)
#     except:
#         raise HTTPException(status_code=401, detail="Invalid authorization format")   
    
#     if role not in ["admin", "user"]:
#         raise HTTPException(status_code=401, detail="Invalid role")
    
#     return {"id": user_id, "role": role}