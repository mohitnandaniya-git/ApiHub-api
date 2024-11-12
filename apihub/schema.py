from pydantic import BaseModel

class TaskSchema(BaseModel):
    model: str
    stream: bool = False
    prompt: str
