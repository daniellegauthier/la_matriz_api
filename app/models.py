from pydantic import BaseModel
from typing import List

class PhraseRequest(BaseModel):
    phrase: str
    length: int = 6
    momentum: str = 'original'

class PhraseResponse(BaseModel):
    seed_words: List[str]
    rgb_sequence: List[List[int]]
    image_url: str
