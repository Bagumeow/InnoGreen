# import sys
# sys.path.insert(0, r'D:\E\InnoDumpling\innogreen-be\tools_h')

# from tools import *
from tools.tools import *
from fastapi import  FastAPI, HTTPException, status, Depends, APIRouter

# app=FastAPI()
# @app.get("/user", response_model=User)

router = APIRouter()

@router.get("/user", response_model=User)
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


# if __name__ == '__main__':
#     import uvicorn
#     uvicorn.run(app, host="127.0.0.1", port=8000)
