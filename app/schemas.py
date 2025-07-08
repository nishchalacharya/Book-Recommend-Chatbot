from pydantic import BaseModel

class BookQuery(BaseModel):
    query: str
    top_k: int = 1
