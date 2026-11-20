from pydantic import BaseModel,Field
from typing import Literal

class ResearchBrief(BaseModel):
    summary:str
    competitors:list[str]
    key_observation:list[str]
    sources: list[str]
    missing_information: list[str]


class CriticSchema(BaseModel):
    decision:Literal['approved','need_improvement']
    feedback:str
    suggestion:list[str]
    confidence_score:int=Field(ge=0,le=100,description="Confidence in the review decision, from 0 to 100")

