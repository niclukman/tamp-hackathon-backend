from pydantic import BaseModel

class RackResponse(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float
    distance: float

    class Config:
        from_attributes = True
    
