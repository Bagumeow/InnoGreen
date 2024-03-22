from tools.tools import *
from fastapi import  HTTPException, status, Depends, APIRouter
router = APIRouter()

@router.post("/user", response_model=User)
async def get_current_user(access_token: str = Depends(oauth2_scheme)):
    conn = create_connection()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError:
        raise credentials_exception
    user = get_user(conn, token_data.username)
    if user is None:
        raise credentials_exception
    conn.close()
    return user

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
