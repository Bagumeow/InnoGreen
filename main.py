from tools.tools import *
from fastapi import FastAPI
from router import  users,current_user
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, __version__
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv


load_dotenv('.env')
app = FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")

html = f"""
<!DOCTYPE html>
<html>
    <head>
        <title>FastAPI on Vercel</title>
        <link rel="icon" href="/static/favicon.ico" type="image/x-icon" />
    </head>
    <body>
        <div class="bg-gray-200 p-4 rounded-lg shadow-lg">
            <h1>Hello from FastAPI@{__version__}</h1>
        </div>
    </body>
</html>
"""

@app.get("/")
async def root():
    return HTMLResponse(html)
@app.get("/")
def router():
    return {"message": "API from Dumplings team project"}

app.include_router(users.router)
app.include_router(current_user.router)
# app.include_router(patients.router)


