from tools.tools import *
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import datetime, timedelta, timezone

# app = FastAPI()
router = APIRouter()
class UserCreate(BaseModel):
    username: str
    password: str
    role: Union[str, None] = None
    full_name: Union[str, None] = None
    phone_number : Union[str, None] = None
    gender : Union[bool, None] = None
    re_password : Union[str, None] = None
    email: Union[str, None] = None
    age: Union[int, None] = None
    address: Union[str, None] = None
    
# @app.post("/register/",response_model=User, status_code=status.HTTP_201_CREATED)
@router.post("/register/",response_model=User, status_code=status.HTTP_201_CREATED)
async def register(user: UserCreate):
    conn = create_connection()
    cursor = create_cursor(conn)

    if check_dupli_user_or_email(conn, user.username, user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Tài Khoản hoặc Email đã tồn tại!!!")
    if (user.password != user.re_password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Nhập lại mật khẩu phải trùng với mật khẩu")
    
    table_name = "users"
    columns= "username, hashed_password, role, full_name, phone_number, gender, email, age, address"
    insert_query = f'INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)'
    data_insert = (user.username,get_password_hash(user.password),user.role, user.full_name,user.phone_number,user.gender, user.email,user.age,user.address) 
    cursor.execute(insert_query, data_insert)

    conn.commit()
    result = get_user(conn, user.username)
    conn.close()
    if result:
        return result
    
@router.post("/login")
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    conn = create_connection()
    user = authenticate_user(conn, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data={"sub": user.username}, expires_delta=access_token_expires)
    conn.close()
    return {"access_token": access_token, "token_type": "bearer"}


