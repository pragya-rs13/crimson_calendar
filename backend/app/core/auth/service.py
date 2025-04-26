from app.security.auth import create_access_token, create_refresh_token
from app.security.hashing import verify_password
from fastapi import HTTPException, Response

def login_user(username: str, password: str, response: Response): # replace with LoginRequest later
    # verify credentials
    user = get_user_from_db(username)
    if not user or not verify_password(user.password, password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = create_access_token({"sub": user.username})
    refresh_token = create_refresh_token({"sub": user.username})
    
    # set cookies here
    response.set_cookie(
        key="access_token",
        value=access_token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        httponly=True,
        samesite="lax",
        secure=False
    )
    
    return {"message": "Logged in successfully"}

def get_user_from_db(username: str):
    return None