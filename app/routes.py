from fastapi import APIRouter, Depends
from sqlalchemy import select, func
from geoalchemy2.functions import ST_DWithin, ST_Distance, ST_MakePoint, ST_X, ST_Y
from geoalchemy2.types import Geography
from app.db import get_db
from app.models import Rack
from app.schemas import RackResponse

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
