from pydantic import BaseModel
   
class Item(BaseModel):
    item: str
    status: str
    
class Todo(BaseModel):
    id: int
    item: str
    class Config:
        Schema_extra = {
        "Example": {
            "id": 1,
            "item": "¡Esquema de ejemplo!"
            }
        }