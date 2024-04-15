# from tools import *
from tools.tools import *
from fastapi import  FastAPI, status, APIRouter, Depends
from .current_user import *

router = APIRouter()
@router.get("/get_question_patient/", status_code=status.HTTP_201_CREATED)
async def get_question_patient(id_patient: str, access_token: str = Depends(oauth2_scheme)): 
    # Call the function to get questions based on patient ID
    questions = get_questions_by_patient_id(id_patient)
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No questions found for the provided patient ID")
    
    return questions