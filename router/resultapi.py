from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List

router = APIRouter()

class SurveyQuestion(BaseModel):
    id: int
    content: str
    answer: str

class SurveyResponse(BaseModel):
    type: str
    questions: List[SurveyQuestion]
    token: str

class SurveyResult(BaseModel):
    point: float
    token: str

@router.post("/survey_result/")
async def process_survey_result(survey: SurveyResponse):
    gt_points = 0
    vdt_points = 0
    vdti_points = 0
    bcvh_points = 0
    cnxh_points = 0
    k_points = 0
    for question in survey.questions:
        if question.answer == "Có" and question.id >= 16 and question.id <= 20:
            k_points += 1
        elif question.id >= 1 and question.id <= 15:
            if question.answer == "Không" and question.id >= 1 and question.id <= 3:
                gt_points += 1
            elif question.answer == "Không" and question.id >= 4 and question.id <= 7:
                vdt_points += 1
            elif question.answer == "Không" and question.id >= 8 and question.id <= 11:
                vdti_points += 1
            elif question.answer == "Không" and question.id >= 12 and question.id <= 15:
                bcvh_points += 1
    if gt_points == 2 or vdt_points == 2 or bcvh_points == 2 or cnxh_points == 2 or k_points == 1:
        total_points = 1
    else:
        total_points = 0
    
    result = SurveyResult(point=total_points, token=survey.token)
    return result
