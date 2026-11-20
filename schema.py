from pydantic import BaseModel

class ResearchBrief(BaseModel):
    summary:str
    competitors:list[str]
    key_observation:list[str]
    sources: list[str]
    missing_information: list[str]
