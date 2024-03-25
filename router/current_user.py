from tools.tools import *
# from tools import *
from fastapi import  HTTPException, status, Depends, APIRouter
router = APIRouter()

@router.post("/user", response_model=UserInDB)
async def get_current_user(access_token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    conn = create_connection()
    token_data = decode_bearer_token(access_token)
    _,user = get_user(conn, token_data.email)
    if user is None:
        raise credentials_exception
    conn.close()
    return user

# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)
