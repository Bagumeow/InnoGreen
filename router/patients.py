from tools.tools import *
# from tools import *
from fastapi import  FastAPI,status ,APIRouter,Depends
from .current_user import *

# app=FastAPI()
# @app.post("/user/create_profile", status_code=status.HTTP_201_CREATED)

router = APIRouter()
@router.post("/user/create_patient_profile/", status_code=status.HTTP_201_CREATED)
async def create_patient_profile(patient : Patient, access_token: str = Depends(oauth2_scheme)): 

    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    token_data = decode_bearer_token(access_token)
    id_user,_ = get_user(conn, token_data.email)
    table_name = "patients"
    columns= "user_id, name_patient, age_patient, address_patient, path_img_chart, note_case, detail, treatment"
    insert_query = f'INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)'
    data_insert = (id_user,patient.name_patient,patient.age_patient,patient.address_patient,patient.path_img_chart,patient.note_case,patient.detail, patient.treatment)
    cursor.execute(insert_query, data_insert)
    conn.commit()
    conn.close()
    return {"message": "Create patient profile successfully"}

# if __name__ == "__main__":
#     import uvicorn
#     uvicorn.run(app, host="0.0.0.0", port=8000)	