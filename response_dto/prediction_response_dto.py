from pydantic import BaseModel

class PredictionResponseDto(BaseModel):
    filename: str
    contentype: str
    likely_class: str