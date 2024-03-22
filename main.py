from tools.tools import *
from fastapi import FastAPI
from router import  users,current_user
import os
from dotenv import load_dotenv
load_dotenv('.env')
app = FastAPI()

@app.get("/")
def router():
    return {"message": "API from Dumplings team project"}

app.include_router(users.router)
app.include_router(current_user.router)
# app.include_router(patients.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=os.getenv("HOST"), port=8123)	