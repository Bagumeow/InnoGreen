from tools_BE import *
from fastapi import  FastAPI,status ,APIRouter,Depends
from current_user import get_current_user

# router = APIRouter()
# @router.post("/user/create_profile/", status_code=status.HTTP_201_CREATED)
app=FastAPI()
@app.post("/user/create_profile", status_code=status.HTTP_201_CREATED)
async def create_patient_profile(patient : Patient,access_token: str = Depends(oauth2_scheme)):
    user = get_current_user(access_token)

    conn = create_connection()
    cursor = create_cursor(conn)

    table_name = "patients"
    columns= "user_id, name_p, age_p, address_p, path_img_char, note_case, detail_case, treatment"
    insert_query = f'INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    data_insert = (user.user_id,patient.name_p,patient.age_p,patient.address_p,patient.path_img_char,patient.note_case,patient.detail_case,patient.treatment)
    cursor.execute(insert_query, data_insert)
    conn.commit()
    conn.close()
    return {"message": "Create patient profile successfully"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)	