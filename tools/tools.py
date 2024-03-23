from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import psycopg2
import os

from dotenv import load_dotenv
load_dotenv('.env')


# SECRET_KEY = os.getenv("SECRET_KEY")
# ALGORITHM = os.getenv("ALGORITHM")
# ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
# DB_NAME = os.getenv("DB_NAME")
# DB_USER = os.getenv("DB_USER")
# DB_PASS = os.getenv("DB_PASS")
# DB_HOST = os.getenv("DB_HOST")
# DB_PORT = os.getenv("DB_PORT")

SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = '30'



DB_NAME =  "IUH-InnoGL"
DB_HOST= "aws-0-ap-southeast-1.pooler.supabase.com"
DB_PORT= "5432"
DB_USER= "postgres.vfkzqxldkzddopenrihb"
DB_PASS= "Dumplings@1123!!"


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash the password
def get_password_hash(password):
    return pwd_context.hash(password)

def create_connection():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                # pgbouncer=True
                                )
        print("Database connected successfully")
    except:
        print("Database not connected successfully")
    return conn

def create_cursor(conn):
    return conn.cursor()


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Union[str, None] = None
    
class User(BaseModel):
    username: str
    role: Union[str, None] = None
    full_name: Union[str, None] = None
    phone_number : Union[str, None] = None
    gender : Union[bool, None] = None
    email: Union[str, None] = None
    age: Union[int, None] = None
    address: Union[str, None] = None

class Patient(BaseModel):
    user_id : int 
    name_p: Union[str, None] = None
    age_p : Union[int, None] = None
    address_p : Union[str, None] = None
    path_img_char : Union[str, None] = None 
    note_case : Union[str, None] = None
    detail_case : Union[str, None] = None
    treatment : Union[str, None] = None


class UserInDB(User):
    hashed_password: str


def get_user(conn, username: str):
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    cursor.execute('SELECT * FROM users WHERE username=%s', (username,))
    result = cursor.fetchone()
    if result:
        return UserInDB(username=result[1],hashed_password=result[2],role=result[3],full_name=result[4],phone_number=result[5],
                        gender=result[6],email=result[7],age=result[8],address=result[9])

def check_dupli_user_or_email(conn, username: str, email: str):
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    cursor.execute('SELECT * FROM users WHERE username=%s OR email=%s', (username,email))
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False    


def authenticate_user(conn, username: str, password: str):
    user = get_user(conn, username)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt