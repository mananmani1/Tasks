from pydantic import BaseModel
from typing import List, Dict

class DatasetBase(BaseModel):
    id: str
    extracted_data: List[Dict]

    class Config:
        from_attributes = True
