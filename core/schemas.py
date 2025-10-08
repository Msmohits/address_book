from pydantic import BaseModel, Field, field_validator


class AddressBase(BaseModel):
    name: str
    street: str
    city: str
    latitude: float = Field(..., ge=-90, le=90)
    longitude: float = Field(..., ge=-180, le=180)

    @field_validator("latitude", "longitude", mode="before")
    def round_coordinates(cls, v):
        return round(v, 4)


class AddressCreate(AddressBase):
    pass


class Address(AddressBase):
    id: int

    class Config:
        from_attributes = True
