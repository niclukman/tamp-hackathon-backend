from pydantic import BaseModel

class RackResponse(BaseModel):
    id: int
    name: str
    longitude: float
    latitude: float
    distance: float

    class Config:
        from_attributes = True


class ParkingCheckRequest(BaseModel):
    latitude: float
    longitude: float


class ParkingCheckResponse(BaseModel):
    is_whitelisted: bool
    message: str
    zone_name: str | None = None
    
