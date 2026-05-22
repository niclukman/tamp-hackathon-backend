from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_MakePoint, ST_X, ST_Y
from geoalchemy2.types import Geography
from app.db import get_db
from app.models import Rack, ParkingZone
from app.schemas import RackResponse,ParkingCheckRequest, ParkingCheckResponse

router = APIRouter()

@router.get("/racks/nearby", response_model=list[RackResponse])
async def get_nearby_racks(
    lat: float,
    lng: float,
    radius_m: float=500,
    limit=10,
    db=Depends(get_db)
):
    target = func.cast(ST_MakePoint(lng, lat), Geography)

    query = (
        select(
            Rack,
            ST_X(Rack.geom).label("longitude"),
            ST_Y(Rack.geom).label("latitude"),
            ST_Distance(func.cast(Rack.geom, Geography), target).label("distance")
        )
        .where(ST_DWithin(func.cast(Rack.geom, Geography), target, radius_m))
        .order_by("distance")
        .limit(limit)
    )

    result = await db.execute(query)
    rows = result.mappings().all()

    return [
        RackResponse(
            id=row.Rack.id,
            name=row.Rack.name,
            longitude=row.longitude,
            latitude=row.latitude,
            distance=row.distance
        )
        for row in rows
    ]


@router.post("/parking/validate", response_model=ParkingCheckResponse)
async def validate_parking_location(
    payload: ParkingCheckRequest,
    db=Depends(get_db)
):
    #Generate a spatial geometry Point with WGS84 projection layout (SRID 4326)
    bike_point = func.ST_SetSRID(ST_MakePoint(payload.longitude, payload.latitude), 4326)

   #Query to find if ANY whitelisted polygon contains this point
    query = (
        select(ParkingZone)
        .where(func.ST_Contains(ParkingZone.geom, bike_point))
        .limit(1)
    )

    result = await db.execute(query)
    matched_zone = result.scalars().first()

    if matched_zone:
        return ParkingCheckResponse(
            is_whitelisted=True,
            message="Success! You are parked in a valid designated area.",
            zone_name=matched_zone.name
        )
    
    return ParkingCheckResponse(
        is_whitelisted=False,
        message="Invalid Location: You must park your bicycle within a whitelisted parking zone.",
        zone_name=None
    )