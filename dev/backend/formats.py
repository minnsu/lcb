from typing import Optional
from pydantic import BaseModel

class Input(BaseModel):
    text: str

class Setting(BaseModel):
    storage_path: str
    model_path: str
    temperature: float
    top_p: float
    repetition_penalty: float
    max_new_tokens: int

class Option(BaseModel):
    search: str
    file_path: str
    text_context: str
