from pydantic import BaseModel, Field

class PostCreateSchema(BaseModel):
    text: str = Field(..., max_length=1_048_576)  # Обмеження в 1 МБ
