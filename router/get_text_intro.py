import sys
sys.path.append('./')
from tools.tools import *
from fastapi import FastAPI, Depends, HTTPException, status, APIRouter

router = APIRouter()
@router.post("/info")
async def register():
    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("""SELECT * FROM web_benefit
        """)
    infors = [table for table in cursor.fetchall()]
    list_of_dicts = [{"id_loiich": tup[0], "thongtin": tup[1], "chitiet": tup[2]} for tup in infors]
    return list_of_dicts