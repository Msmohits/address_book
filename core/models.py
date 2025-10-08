from sqlalchemy import Column, Integer, String, Float, UniqueConstraint
from services.db import Base


class Address(Base):
    __tablename__ = "addresses"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    street = Column(String)
    city = Column(String)
    latitude = Column(Float)
    longitude = Column(Float)

    __table_args__ = (
        UniqueConstraint(
            "name", "street", "latitude", "longitude", name="uix_name_lat_lon"
        ),
    )
