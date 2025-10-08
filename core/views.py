from fastapi import Depends, HTTPException
from utils.auth import validate_token
from sqlalchemy.orm import Session
from core.schemas import AddressBase
from core.models import Address
from fastapi.responses import JSONResponse
from utils.calc_dist import calculate_distance
from services.db import get_db
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from fastapi.encoders import jsonable_encoder


def init_address_api(app):
    @app.post(
        "/address/create", dependencies=[Depends(validate_token)], response_model=AddressBase
    )
    async def create_address(address: AddressBase, db: Session = Depends(get_db)):
        try:
            new_address = Address(**address.model_dump())
            db.add(new_address)
            db.commit()
            db.refresh(new_address)
        except IntegrityError:
            db.rollback()  # Important!
            raise HTTPException(
                status_code=400, detail="Address with this name already exists"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
        return JSONResponse(
            content={
                "message": "Address created",
                "data": jsonable_encoder(new_address),
            },
            status_code=201,
        )

    @app.get(
        "/address/{address_id}",
        dependencies=[Depends(validate_token)],
        response_model=AddressBase,
    )
    async def get_address(address_id: int, db: Session = Depends(get_db)):
        address = db.get(Address, address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        return JSONResponse(
            content={
                "message": "Address fetched successfully",
                "data": jsonable_encoder(address),
            },
            status_code=200,
        )

    @app.put(
        "/address/{address_id}",
        dependencies=[Depends(validate_token)],
        response_model=AddressBase,
    )
    async def update_address(
        address_id: int, address: AddressBase, db: Session = Depends(get_db)
    ):
        try:
            existing_address = db.get(Address, address_id)
            if not existing_address:
                raise HTTPException(status_code=404, detail="Address not found")
            for key, value in address.model_dump().items():
                setattr(existing_address, key, value)
            db.commit()
            db.refresh(existing_address)
            return JSONResponse(
                content={
                    "message": "Address updated",
                    "data": jsonable_encoder(existing_address),
                },
                status_code=200,
            )
        except IntegrityError:
            db.rollback()  # Important!
            raise HTTPException(
                status_code=400, detail="Address with this name already exists"
            )
        except SQLAlchemyError as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))

    @app.delete(
        "/address/{address_id}",
        dependencies=[Depends(validate_token)],
        response_model=dict,
    )
    async def delete_address(address_id: int, db: Session = Depends(get_db)):
        address = db.get(Address, address_id)
        if not address:
            raise HTTPException(status_code=404, detail="Address not found")
        db.delete(address)
        db.commit()
        return JSONResponse(content={"message": "Address deleted"}, status_code=200)

    @app.get(
        "/addresses/nearby",
        dependencies=[Depends(validate_token)],
        response_model=list[AddressBase],
    )
    def get_addresses_within_distance(
        lat: float, lon: float, distance_km: float, db: Session = Depends(get_db)
    ):
        all_addresses = db.query(Address).all()
        nearby = []
        for addr in all_addresses:
            dist = calculate_distance(lat, lon, addr.latitude, addr.longitude)
            if dist <= distance_km:
                nearby.append(addr)
        return JSONResponse(
            content={
                "message": "Addresses fetched successfully",
                "data": jsonable_encoder(nearby),
                "count": len(nearby),
            },
            status_code=200,
        )
